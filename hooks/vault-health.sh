#!/usr/bin/env bash
# vault-health.sh — hook plugin H1 · événement SessionStart
#
# Bilan de santé du vault, injecté dans le contexte au démarrage de session.
# Capteur déterministe (proxies de fichiers) + auto-fix inerte (.DS_Store). Jamais de blocage.
#
# Portée : le plugin est actif dans toute session Claude Code → racine = vault contenant le cwd
# (CLAUDE_PROJECT_DIR, sinon "cwd" du JSON stdin), en remontant jusqu'à trouver `_Meta/`.
# Hors vault : no-op silencieux. Config optionnelle : `{vault}/_Meta/hooks.conf` (voir vault-lib.sh).
# Dépendances : bash + python3. Pas de jq.

. "$(dirname "$0")/vault-lib.sh"
HOOK_INPUT="$(cat 2>/dev/null || true)"

VAULT="$(vault_root "${CLAUDE_PROJECT_DIR:-}")" || VAULT="$(vault_root "$(stdin_field cwd)")" || exit 0
cd "$VAULT" 2>/dev/null || exit 0

# Auto-fix inerte : purge des .DS_Store (jamais de dossier vide)
DSSTORE=$(find . -type f -name '.DS_Store' 2>/dev/null | wc -l | tr -d ' ')
[ "${DSSTORE:-0}" -gt 0 ] && find . -type f -name '.DS_Store' -delete 2>/dev/null

DSSTORE="$DSSTORE" \
INBOX_STALE_DAYS="$(vault_conf "$VAULT" INBOX_STALE_DAYS 14)" \
EXCLUDE="$(vault_conf "$VAULT" EXCLUDE "")" \
python3 <<'PY'
import os, time, json, re, glob

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

# Notes sans type (hors exclusions)
no_type = 0
for path in glob.glob(os.path.join(vault, "**", "*.md"), recursive=True):
    base = os.path.basename(path)
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
if not segs:
    raise SystemExit(0)  # vault sain : pas de bruit

print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Santé du vault : " + " · ".join(segs) + "."
}}, ensure_ascii=False))
PY
exit 0
