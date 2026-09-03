#!/usr/bin/env bash
# vault-note-guard.sh — hook plugin H2 · événement PostToolUse (matcher Write|Edit|MultiEdit)
#
# Garde-fou à l'écriture d'une note .md d'un vault.
#  - Auto-fix : stamp `created:` (si absent) et `updated:` (à aujourd'hui) dans le frontmatter
#    existant. Jamais de création de frontmatter, jamais de rename.
#  - Nudge    : frontmatter absent / nom pas en kebab-case (rename = suggestion).
#
# Portée : le plugin est actif dans toute session Claude Code → la racine est déduite du FICHIER
# écrit (remontée jusqu'à `_Meta/`), pas du cwd. Une note du vault écrite depuis un repo client
# (symlink) est donc gardée ; un .md hors vault est ignoré. Config : `{vault}/_Meta/hooks.conf`.
# Dépendances : bash + python3. Pas de jq.

. "$(dirname "$0")/vault-lib.sh"
HOOK_INPUT="$(cat 2>/dev/null || true)"

FILE="$(stdin_field tool_input.file_path)"; [ -n "$FILE" ] || FILE="$(stdin_field tool_input.path)"
[ -n "$FILE" ] || exit 0
case "$FILE" in *.md) ;; *) exit 0 ;; esac
[ -f "$FILE" ] || exit 0
FILE="$(cd "$(dirname "$FILE")" 2>/dev/null && pwd -P)/$(basename "$FILE")"   # résout le symlink ~/vault
VAULT="$(vault_root "$FILE")" || exit 0                                         # hors vault → ignorer

REL="${FILE#"$VAULT"/}"
case "$REL" in
  _Meta/*|.obsidian/*|.claude/*|.git/*) exit 0 ;;
esac
IFS=, read -ra EXCL <<<"$(vault_conf "$VAULT" EXCLUDE "")"
for e in "${EXCL[@]}"; do e="${e## }"; e="${e%% }"; e="${e%/}"; [ -n "$e" ] && case "$REL" in "$e"/*|*/"$e"/*) exit 0 ;; esac; done
BASE="$(basename "$FILE")"
case "$BASE" in CLAUDE.md|README.md|*-template.md|_*) exit 0 ;; esac   # _index.md & fichiers structurels

FILE="$FILE" python3 <<'PY'
import os, re, json, datetime

path = os.environ["FILE"]
today = datetime.date.today().isoformat()
try:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
except Exception:
    raise SystemExit(0)

base = os.path.basename(path); stem = base[:-3]
nudges = []
lines = text.split("\n")

has_fm = text.startswith("---")
end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None) if has_fm else None
if end is None:
    has_fm = False

if has_fm:
    fm = lines[1:end]; changed = False
    if not any(re.match(r"^created:\s*", ln) for ln in fm):
        fm.append(f"created: {today}"); changed = True
    for i, ln in enumerate(fm):
        if re.match(r"^updated:\s*", ln):
            if ln.strip() != f"updated: {today}":
                fm[i] = f"updated: {today}"; changed = True
            break
    else:
        fm.append(f"updated: {today}"); changed = True
    if changed:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(["---"] + fm + ["---"] + lines[end + 1:]))
        except Exception:
            pass
else:
    nudges.append("note sans frontmatter (le Schema attend au moins `type` et `tags`)")

if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", stem):
    nudges.append(f"nom `{base}` pas en kebab-case, pense à renommer (attention aux wikilinks)")

if nudges:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "Garde-fou note : " + " ; ".join(nudges) + "."
    }}, ensure_ascii=False))
PY
exit 0
