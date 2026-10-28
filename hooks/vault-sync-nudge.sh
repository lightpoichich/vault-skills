#!/usr/bin/env bash
# vault-sync-nudge.sh — hook plugin H4 · événement Stop
#
# Rappel de répercussion en fin de tour, quand la session a produit assez de matière :
#   - cwd dans un vault                 → bloque l'arrêt UNE fois et demande d'invoquer `sync-vault` ;
#   - cwd dans un dossier projet relié  → idem, `sync-vault` en mode projet, ciblé sur la fiche résolue
#                                         (dépôt git ou dossier sans git relié par `dossier-travail:` — voir vault-resolve.py) ;
#   - ailleurs                          → no-op silencieux.
# Au Stop suivant (stop_hook_active=true), on laisse passer et on pose la nouvelle base.
# Une répercussion faite sans le rappel (sync-vault invoqué à la main, fiche projet écrite en mode projet) pose
# aussi une nouvelle base : le rappel ne redemande pas ce qui vient d'être fait.
#
# Seuils, lus dans `{vault}/_Meta/hooks.conf` : SYNC_MIN_KB (40) de transcript écrits depuis le dernier sync ET
# SYNC_MIN_MINUTES (20) écoulées. Opt-out : SYNC_NUDGE=0 (plus rien) ou SYNC_NUDGE=vault (pas depuis les dossiers de travail).
# Depuis un worktree git lié (sous-agent de ticket), pas de rappel sauf SYNC_NUDGE_WORKTREES=1.
# Marqueur par session : ${XDG_CACHE_HOME:-~/.cache}/second-cerveau/sync-nudge/<session_id>
# (contenu = taille du transcript au dernier sync, mtime = quand). Dépendances : bash + python3 (+ git dans un dépôt).

. "$(dirname "$0")/vault-lib.sh"
HOOK_INPUT="$(cat 2>/dev/null || true)"

session_id="$(stdin_field session_id)"; transcript="$(stdin_field transcript_path)"
[ -n "$session_id" ] && [ -f "$transcript" ] || exit 0
active="$(printf '%s' "$HOOK_INPUT" | python3 -c 'import sys,json
try: print("1" if json.load(sys.stdin).get("stop_hook_active") else "0")
except Exception: print("0")' 2>/dev/null)"

DIR="${CLAUDE_PROJECT_DIR:-}"; [ -n "$DIR" ] || DIR="$(stdin_field cwd)"; [ -n "$DIR" ] || exit 0
eval "$(python3 "$(dirname "$0")/vault-resolve.py" --shell "$DIR" 2>/dev/null)" || exit 0
case "${MODE:-none}" in vault|projet) ;; *) exit 0 ;; esac

case "$(vault_conf "$VAULT" SYNC_NUDGE 1)" in
  0|off|false|no|non) exit 0 ;;
  vault) [ "$MODE" = vault ] || exit 0 ;;
esac

# Worktree git lié (sous-agent de ticket : Paseo `~/.paseo/worktrees/`, `.claude/worktrees/`) : pas de rappel.
# Plusieurs builders parallèles écriraient la même fiche projet ; l'orchestrateur, dans le checkout principal,
# synchronise une fois. SYNC_NUDGE_WORKTREES=1 rétablit le rappel dans les worktrees.
if [ "$MODE" = projet ] && [ "$(vault_conf "$VAULT" SYNC_NUDGE_WORKTREES 0)" != 1 ]; then
  gd="$(git -C "$DIR" rev-parse --git-dir 2>/dev/null)"; gcd="$(git -C "$DIR" rev-parse --git-common-dir 2>/dev/null)"
  if [ -n "$gd" ] && [ -n "$gcd" ] && [ "$(cd "$DIR" && cd "$gd" && pwd -P)" != "$(cd "$DIR" && cd "$gcd" && pwd -P)" ]; then exit 0; fi
fi
MIN_KB="$(vault_conf "$VAULT" SYNC_MIN_KB 40)"; MIN_MIN="$(vault_conf "$VAULT" SYNC_MIN_MINUTES 20)"

dir="${XDG_CACHE_HOME:-$HOME/.cache}/second-cerveau/sync-nudge"; mkdir -p "$dir" 2>/dev/null || exit 0
marker="$dir/$session_id"
find "$dir" -type f -mtime +7 -delete 2>/dev/null
size=$(wc -c < "$transcript" | tr -d ' ')

if [ "$active" = 1 ]; then echo "$size" > "$marker"; exit 0; fi   # le tour de sync vient de finir → nouvelle base
[ -f "$marker" ] || echo 0 > "$marker"                             # première fin de tour → base = début de session

measure() {
  base=$(cat "$marker" 2>/dev/null || echo 0); now=$(date +%s)
  mtime=$(stat -c %Y "$marker" 2>/dev/null || stat -f %m "$marker" 2>/dev/null || echo "$now")
  grown_kb=$(( (size - base) / 1024 )); elapsed_min=$(( (now - mtime) / 60 ))
  [ "$grown_kb" -ge "$MIN_KB" ] && [ "$elapsed_min" -ge "$MIN_MIN" ]
}
measure || exit 0

# Seuils atteints : chercher dans le transcript, depuis la base, une répercussion faite sans le rappel
# (sync-vault invoqué à la main, ou fiche projet écrite directement en mode projet). La dernière trouvée
# devient la nouvelle base (position et heure), puis les seuils sont remesurés depuis elle.
python3 - "$transcript" "$marker" "$base" "${SHEET:-}" <<'PY' 2>/dev/null
import json, os, re, sys
from datetime import datetime
transcript, marker, base, sheet = sys.argv[1], sys.argv[2], int(sys.argv[3] or 0), sys.argv[4]
sheet = os.path.realpath(sheet) if sheet else ""
SYNC = re.compile(r"(^|:)sync-(vault|repo)$")
SLASH = re.compile(r"<command-name>/?(?:[\w-]+:)?sync-(?:vault|repo)</command-name>")
hit = None
with open(transcript, "rb") as fh:
    if base:
        fh.seek(base - 1)
        if fh.read(1) != b"\n": fh.readline()   # base au milieu d'une ligne : la sauter
    while True:
        line = fh.readline()
        if not line: break
        if b"sync-" not in line and not (sheet and os.path.basename(sheet).encode() in line): continue
        try: d = json.loads(line)
        except Exception: continue
        content = (d.get("message") or {}).get("content")
        found = False
        if d.get("type") == "user":
            text = content if isinstance(content, str) else " ".join(
                c.get("text", "") for c in content or [] if isinstance(c, dict) and c.get("type") == "text")
            found = bool(SLASH.search(text or ""))
        elif d.get("type") == "assistant" and isinstance(content, list):
            for c in content:
                if not isinstance(c, dict) or c.get("type") != "tool_use": continue
                inp = c.get("input") or {}
                if c.get("name") == "Skill" and SYNC.search(str(inp.get("skill", ""))): found = True
                if sheet and c.get("name") in ("Write", "Edit", "MultiEdit") and inp.get("file_path") \
                        and os.path.realpath(inp["file_path"]) == sheet: found = True
        if found: hit = (fh.tell(), d.get("timestamp") or "")
if hit:
    offset, ts = hit
    try: when = datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp()
    except Exception: when = None
    with open(marker, "w") as out: out.write(f"{offset}\n")
    if when: os.utime(marker, (when, when))
PY
measure || exit 0

if [ "$MODE" = vault ]; then
  reason="Garde-fou vault : cette session a produit du travail depuis le dernier sync (${grown_kb} Ko de transcript, ${elapsed_min} min). Avant de rendre la main, invoque le skill sync-vault pour répercuter dans le vault ce qui a bougé dans cette conversation (décisions, statuts, todos, faits, contacts) et alléger les fiches touchées. Si rien de substantiel n'a bougé, réponds seulement « Rien à répercuter. » et termine."
else
  if git -C "$DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then where="dans le dépôt ${REPO:-$DIR}"; from="de cette conversation et des commits récents"
  else where="dans le dossier $DIR"; from="de cette conversation"; fi
  reason="Garde-fou vault : cette session $where a produit du travail depuis le dernier sync (${grown_kb} Ko de transcript, ${elapsed_min} min). Avant de rendre la main, invoque le skill sync-vault (mode projet) pour mettre à jour la fiche projet ${SHEET} (avancement, décisions, todos, statut) à partir $from : cette fiche seulement, le reste va dans sa section « À répercuter ». Si rien de substantiel n'a bougé, réponds seulement « Rien à répercuter. » et termine."
fi
printf '%s' "$reason" | python3 -c 'import json,sys; print(json.dumps({"decision":"block","reason":sys.stdin.read()}, ensure_ascii=False))'
exit 0
