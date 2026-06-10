#!/usr/bin/env bash
# vault-health.sh — Hook H1 · evenement SessionStart
#
# Bilan de sante du vault, injecte dans le contexte au demarrage de session.
# Capteur deterministe (proxies de fichiers) + auto-fix inerte (.DS_Store).
#
# Path-agnostique : racine = $CLAUDE_PROJECT_DIR (sinon "cwd" du JSON stdin).
# Dependances : bash + python3 (present sur WSL/macOS). Pas de jq requis.
#
# --- Reglage ---
INBOX_STALE_DAYS=14   # une note d'Inbox plus vieille que ca est "stale"

INPUT="$(cat 2>/dev/null || true)"

# Racine du vault
VAULT="${CLAUDE_PROJECT_DIR:-}"
if [ -z "$VAULT" ] && [ -n "$INPUT" ]; then
  VAULT="$(printf '%s' "$INPUT" | python3 -c 'import sys,json
d=json.load(sys.stdin)
print(d.get("cwd",""))' 2>/dev/null || true)"
fi
[ -n "$VAULT" ] || exit 0
[ -d "$VAULT/_Meta" ] || exit 0   # no-op hors d'un vault

cd "$VAULT" 2>/dev/null || exit 0

# Auto-fix inerte : purge des .DS_Store (jamais de dossier vide)
DSSTORE=$(find . -type f -name '.DS_Store' 2>/dev/null | wc -l | tr -d ' ')
[ "${DSSTORE:-0}" -gt 0 ] && find . -type f -name '.DS_Store' -delete 2>/dev/null

# Mesures + sortie JSON (python pour la portabilite du calcul d'age)
DSSTORE="$DSSTORE" INBOX_STALE_DAYS="$INBOX_STALE_DAYS" python3 <<'PY'
import os, time, json, re, glob

vault = os.getcwd()
stale_days = int(os.environ.get("INBOX_STALE_DAYS", "14"))
dsstore = int(os.environ.get("DSSTORE", "0"))
now = time.time()

EXCLUDE = ("/_Meta/", "/_personas/", "/.obsidian/", "/.claude/", "/.git/", "/40-Archive/", "/00-Inbox/")
def excluded(path):
    p = "/" + os.path.relpath(path, vault).replace(os.sep, "/")
    return any(d in p for d in EXCLUDE)

def has_type(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            head = f.read(2000)
    except Exception:
        return True  # illisible : on ne nudge pas
    if not head.startswith("---"):
        return False
    parts = head.split("\n")
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end = i
            break
    if end is None:
        return False
    return re.search(r"(?m)^type:\s*\S", "\n".join(parts[1:end])) is not None

# Inbox : compte + age de la plus ancienne (matiere-premiere ignoree)
inbox_count = 0
inbox_oldest = 0.0
inbox = os.path.join(vault, "00-Inbox")
if os.path.isdir(inbox):
    for root, dirs, files in os.walk(inbox):
        rel = "/" + os.path.relpath(root, vault).replace(os.sep, "/")
        if "/matiere-premiere" in rel:
            dirs[:] = []
            continue
        for fn in files:
            if fn.endswith(".md") and not fn.startswith("."):
                inbox_count += 1
                age = (now - os.path.getmtime(os.path.join(root, fn))) / 86400.0
                if age > inbox_oldest:
                    inbox_oldest = age

# Notes sans type (hors exclusions)
no_type = 0
for path in glob.glob(os.path.join(vault, "**", "*.md"), recursive=True):
    base = os.path.basename(path)
    if base in ("CLAUDE.md", "README.md") or base.startswith("_") or base.endswith("-template.md"):
        continue
    if excluded(path):
        continue
    if not has_type(path):
        no_type += 1

# .md egares a la racine du vault
stray = 0
for path in glob.glob(os.path.join(vault, "*.md")):
    base = os.path.basename(path)
    if base in ("CLAUDE.md", "README.md") or base.startswith("_"):
        continue
    stray += 1

segs = []
if inbox_count and inbox_oldest >= stale_days:
    segs.append(f"{inbox_count} note(s) Inbox, plus vieille {int(inbox_oldest)}j")
if no_type:
    segs.append(f"{no_type} sans type")
if stray:
    segs.append(f"{stray} .md egare(s) a la racine")
if dsstore:
    segs.append(f"{dsstore} .DS_Store purge(s)")

if not segs:
    raise SystemExit(0)  # vault sain : pas de bruit

msg = "Sante du vault : " + " - ".join(segs) + "."
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": msg
}}))
PY
exit 0
