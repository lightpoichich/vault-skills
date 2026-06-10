#!/usr/bin/env bash
# vault-note-guard.sh — Hook H2 · evenement PostToolUse (matcher Write|Edit)
#
# Garde-fou a l'ecriture d'une note .md du vault.
#  - Auto-fix sur  : stamp `created:` (si absent) et `updated:` (a aujourd'hui) dans
#    le frontmatter existant. Jamais de creation de frontmatter, jamais de rename.
#  - Nudge         : frontmatter absent / nom pas en kebab-case (rename = suggestion).
#
# Path-agnostique. Dependances : bash + python3 (pas de jq requis).

INPUT="$(cat 2>/dev/null || true)"
VAULT="${CLAUDE_PROJECT_DIR:-}"

FILE="$(printf '%s' "$INPUT" | python3 -c 'import sys,json
d=json.load(sys.stdin)
ti=d.get("tool_input",{}) or {}
print(ti.get("file_path") or ti.get("path") or "")' 2>/dev/null || true)"

[ -n "$FILE" ] || exit 0
case "$FILE" in *.md) ;; *) exit 0 ;; esac
[ -f "$FILE" ] || exit 0

# Hors-vault -> ignorer (si la racine est connue)
if [ -n "$VAULT" ]; then
  case "$FILE" in "$VAULT"/*) ;; *) exit 0 ;; esac
fi

# Exclusions structurelles
case "$FILE" in
  */_Meta/*|*/.obsidian/*|*/.claude/*|*/.git/*) exit 0 ;;
esac
BASE="$(basename "$FILE")"
case "$BASE" in
  CLAUDE.md|README.md|*-template.md) exit 0 ;;
  _*) exit 0 ;;   # _index.md & fichiers structurels
esac

FILE="$FILE" python3 <<'PY'
import os, re, json, datetime

path = os.environ["FILE"]
today = datetime.date.today().isoformat()
try:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
except Exception:
    raise SystemExit(0)

base = os.path.basename(path)
stem = base[:-3]
nudges = []
lines = text.split("\n")

# Frontmatter present ? (bloc --- ... ---)
has_fm = text.startswith("---")
end = None
if has_fm:
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        has_fm = False

if has_fm:
    fm = lines[1:end]
    changed = False
    if not any(re.match(r"^created:\s*", ln) for ln in fm):
        fm.append(f"created: {today}")
        changed = True
    for i, ln in enumerate(fm):
        if re.match(r"^updated:\s*", ln):
            if ln.strip() != f"updated: {today}":
                fm[i] = f"updated: {today}"
                changed = True
            break
    else:
        fm.append(f"updated: {today}")
        changed = True
    if changed:
        new = ["---"] + fm + ["---"] + lines[end + 1:]
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(new))
        except Exception:
            pass
else:
    nudges.append("note sans frontmatter (le Schema attend au moins `type` et `tags`)")

# Nom kebab-case ?
if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", stem):
    nudges.append(f"nom `{base}` pas en kebab-case, pense a renommer (attention aux wikilinks)")

if nudges:
    msg = "Garde-fou note : " + " ; ".join(nudges) + "."
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": msg
    }}))
PY
exit 0
