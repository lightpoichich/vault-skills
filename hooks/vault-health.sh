#!/usr/bin/env bash
# vault-health.sh — hook plugin H1 · événement SessionStart
#
# Bilan de santé du vault, injecté dans le contexte au démarrage de session.
# Capteur déterministe (proxies de fichiers) + auto-fix inerte (.DS_Store). Jamais de blocage.
# Rappel du rituel d'audit : dernier rapport audit-vault-{date}.md plus vieux que AUDIT_REMINDER_DAYS (30).
# Mise à niveau disponible : fiche d'installation `_Meta/installation.md` absente, ou gabarits changés (vault-upgrade.py check).
#
# Portée : le plugin est actif dans toute session Claude Code → racine = vault contenant le cwd
# (CLAUDE_PROJECT_DIR, sinon "cwd" du JSON stdin), en remontant jusqu'à trouver `_Meta/`.
# Hors vault : no-op silencieux. Config optionnelle : `{vault}/_Meta/hooks.conf` (voir vault-lib.sh).
# Dépendances : bash + python3. Pas de jq.

. "$(dirname "$0")/vault-lib.sh"
HOOKS_DIR="$(cd "$(dirname "$0")" && pwd)"
HOOK_INPUT="$(cat 2>/dev/null || true)"

VAULT="$(vault_root "${CLAUDE_PROJECT_DIR:-}")" || VAULT="$(vault_root "$(stdin_field cwd)")" || exit 0
cd "$VAULT" 2>/dev/null || exit 0

# Auto-fix inerte : purge des .DS_Store (jamais de dossier vide)
DSSTORE=$(find . -type f -name '.DS_Store' 2>/dev/null | wc -l | tr -d ' ')
[ "${DSSTORE:-0}" -gt 0 ] && find . -type f -name '.DS_Store' -delete 2>/dev/null

# Fiches au-dessus de leur budget de taille (rotation des journaux, voir vault-journal.py) : signalement seul.
JOURNAL_SUMMARY="$(python3 "$HOOKS_DIR/vault-journal.py" check --vault "$VAULT" --summary 2>/dev/null)"
# Mémoire native du dossier de lancement (budget de l'index, sensible apparent, voir vault-memory.py) : signalement seul.
LAUNCH_DIR="${CLAUDE_PROJECT_DIR:-$(stdin_field cwd)}"; [ -d "$LAUNCH_DIR" ] || LAUNCH_DIR="$VAULT"
MEMORY_SUMMARY="$(cd "$LAUNCH_DIR" 2>/dev/null && python3 "$HOOKS_DIR/vault-memory.py" check --vault "$VAULT" --summary 2>/dev/null)"
# Mise à niveau du vault (fiche d'installation absente, ou gabarits du plugin changés depuis l'intégration, voir vault-upgrade.py) :
# signalement seul, rien quand il n'y a rien à faire. UPGRADE_REMINDER=0 coupe le signal.
UPGRADE_SUMMARY=""
if [ "$(vault_conf "$VAULT" UPGRADE_REMINDER 1)" != 0 ]; then
  UPGRADE_SUMMARY="$(python3 "$HOOKS_DIR/vault-upgrade.py" check --vault "$VAULT" --summary 2>/dev/null)"
fi

DSSTORE="$DSSTORE" JOURNAL_SUMMARY="$JOURNAL_SUMMARY" MEMORY_SUMMARY="$MEMORY_SUMMARY" UPGRADE_SUMMARY="$UPGRADE_SUMMARY" \
INBOX_STALE_DAYS="$(vault_conf "$VAULT" INBOX_STALE_DAYS 14)" \
AUDIT_REMINDER_DAYS="$(vault_conf "$VAULT" AUDIT_REMINDER_DAYS 30)" \
EXCLUDE="$(vault_conf "$VAULT" EXCLUDE "")" \
python3 <<'PY'
import os, time, json, re, glob, hashlib

vault = os.getcwd()
stale_days = int(os.environ.get("INBOX_STALE_DAYS", "14") or 14)
dsstore = int(os.environ.get("DSSTORE", "0") or 0)
now = time.time()

# Exclusions structurelles + celles de _Meta/hooks.conf (préfixes relatifs, séparés par des virgules)
EXCLUDE = ["_Meta/", "_personas/", ".obsidian/", ".claude/", ".git/", "40-Archive/", "00-Inbox/"]
EXCLUDE += [e.strip().strip("/") + "/" for e in os.environ.get("EXCLUDE", "").split(",") if e.strip()]
def excluded(path):
    rel = os.path.relpath(path, vault).replace(os.sep, "/")
    return any(rel.startswith(d) or ("/" + d) in ("/" + rel) for d in EXCLUDE)

def has_type(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(2000)
    except Exception:
        return True  # illisible : on ne nudge pas
    if not head.startswith("---"):
        return False
    parts = head.split("\n")
    end = next((i for i in range(1, len(parts)) if parts[i].strip() == "---"), None)
    if end is None:
        return False
    return re.search(r"(?m)^type:\s*\S", "\n".join(parts[1:end])) is not None

# Inbox : compte + âge de la plus ancienne (matière première ignorée)
inbox_count, inbox_oldest = 0, 0.0
inbox = os.path.join(vault, "00-Inbox")
if os.path.isdir(inbox):
    for root, dirs, files in os.walk(inbox):
        if "matiere-premiere" in os.path.relpath(root, vault).replace(os.sep, "/"):
            dirs[:] = []; continue
        for fn in files:
            if fn.endswith(".md") and not fn.startswith("."):
                inbox_count += 1
                inbox_oldest = max(inbox_oldest, (now - os.path.getmtime(os.path.join(root, fn))) / 86400.0)

# Notes sans type (hors exclusions), et dates des rapports d'audit-vault où qu'ils soient rangés
no_type = 0
audit_dates = []
for path in glob.glob(os.path.join(vault, "**", "*.md"), recursive=True):
    base = os.path.basename(path)
    m = re.fullmatch(r"audit-vault-(\d{4}-\d{2}-\d{2})\.md", base)
    if m:
        try: audit_dates.append(time.mktime(time.strptime(m.group(1), "%Y-%m-%d")))
        except ValueError: pass
    if base in ("CLAUDE.md", "README.md") or base.startswith("_") or base.endswith("-template.md"):
        continue
    if excluded(path) or has_type(path):
        continue
    no_type += 1

# .md égarés à la racine du vault
stray = sum(1 for p in glob.glob(os.path.join(vault, "*.md"))
            if os.path.basename(p) not in ("CLAUDE.md", "README.md") and not os.path.basename(p).startswith("_"))

segs = []
if inbox_count and inbox_oldest >= stale_days:
    segs.append(f"{inbox_count} note(s) Inbox, plus vieille {int(inbox_oldest)}j")
if no_type: segs.append(f"{no_type} sans type")
if stray: segs.append(f"{stray} .md égaré(s) à la racine")
if dsstore: segs.append(f"{dsstore} .DS_Store purgé(s)")
if os.environ.get("JOURNAL_SUMMARY"): segs.append(os.environ["JOURNAL_SUMMARY"])
if os.environ.get("MEMORY_SUMMARY"): segs.append(os.environ["MEMORY_SUMMARY"])
if os.environ.get("UPGRADE_SUMMARY"): segs.append(os.environ["UPGRADE_SUMMARY"])

# Rituel d'audit : dernier rapport audit-vault-{date}.md plus vieux que AUDIT_REMINDER_DAYS (0 coupe le rappel).
# Sans aucun rapport, le délai court depuis la première session vue sur ce vault par cette machine.
audit_days = int(os.environ.get("AUDIT_REMINDER_DAYS", "30") or 0)
if audit_days > 0:
    if audit_dates:
        age = int((now - max(audit_dates)) / 86400)
        if age >= audit_days: segs.append(f"dernier audit il y a {age} j (audit-vault)")
    else:
        state = os.path.join(os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state"),
                             "second-cerveau", "audit",
                             hashlib.sha256(os.path.realpath(vault).encode("utf-8", "surrogatepass")).hexdigest()[:12])
        try:
            with open(state) as fh: first_seen = float(fh.read().strip())
        except Exception:
            first_seen = now
            try:
                os.makedirs(os.path.dirname(state), exist_ok=True)
                with open(state, "w") as fh: fh.write(f"{int(now)}\n")
            except OSError: pass
        age = int((now - first_seen) / 86400)
        if age >= audit_days: segs.append(f"aucun audit depuis {age} j (audit-vault)")
if not segs:
    raise SystemExit(0)  # vault sain : pas de bruit

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Santé du vault : " + " · ".join(segs) + ". Si tu en parles à l'utilisateur, "
                         "fais-le en langage courant : ce que recouvre chaque point, pourquoi il compte, ce qui "
                         "peut être fait, sans les termes techniques de ce bilan."
}}, ensure_ascii=False))
PY
exit 0
