#!/usr/bin/env bash
# vault-sync-nudge.sh — hook plugin H4 · événement Stop
#
# Rappel de répercussion en fin de tour, quand la session a produit assez de matière :
#   - cwd dans un vault            → bloque l'arrêt UNE fois et demande d'invoquer `sync-vault` ;
#   - cwd dans un dépôt git relié  → idem avec `sync-repo`, ciblé sur la fiche projet résolue
#                                    (`repo:` = remote origin, sinon `dossier-travail:`, sinon slug — voir vault-resolve.py) ;
#   - ailleurs                     → no-op silencieux.
# Au Stop suivant (stop_hook_active=true), on laisse passer et on pose la nouvelle base.
#
# Seuils, lus dans `{vault}/_Meta/hooks.conf` : SYNC_MIN_KB (40) de transcript écrits depuis le dernier sync ET
# SYNC_MIN_MINUTES (20) écoulées. Opt-out : SYNC_NUDGE=0 (plus rien) ou SYNC_NUDGE=vault (pas depuis les dépôts).
# Marqueur par session : ${XDG_CACHE_HOME:-~/.cache}/second-cerveau/sync-nudge/<session_id>
# (contenu = taille du transcript au dernier sync, mtime = quand). Dépendances : bash + python3 (+ git côté dépôt).

. "$(dirname "$0")/vault-lib.sh"
HOOK_INPUT="$(cat 2>/dev/null || true)"

session_id="$(stdin_field session_id)"; transcript="$(stdin_field transcript_path)"
[ -n "$session_id" ] && [ -f "$transcript" ] || exit 0
active="$(printf '%s' "$HOOK_INPUT" | python3 -c 'import sys,json
try: print("1" if json.load(sys.stdin).get("stop_hook_active") else "0")
except Exception: print("0")' 2>/dev/null)"

DIR="${CLAUDE_PROJECT_DIR:-}"; [ -n "$DIR" ] || DIR="$(stdin_field cwd)"; [ -n "$DIR" ] || exit 0
eval "$(python3 "$(dirname "$0")/vault-resolve.py" --shell "$DIR" 2>/dev/null)" || exit 0
case "${MODE:-none}" in vault|repo) ;; *) exit 0 ;; esac

case "$(vault_conf "$VAULT" SYNC_NUDGE 1)" in
  0|off|false|no|non) exit 0 ;;
  vault) [ "$MODE" = vault ] || exit 0 ;;
esac
MIN_KB="$(vault_conf "$VAULT" SYNC_MIN_KB 40)"; MIN_MIN="$(vault_conf "$VAULT" SYNC_MIN_MINUTES 20)"

dir="${XDG_CACHE_HOME:-$HOME/.cache}/second-cerveau/sync-nudge"; mkdir -p "$dir" 2>/dev/null || exit 0
marker="$dir/$session_id"
find "$dir" -type f -mtime +7 -delete 2>/dev/null
size=$(wc -c < "$transcript" | tr -d ' ')

if [ "$active" = 1 ]; then echo "$size" > "$marker"; exit 0; fi   # le tour de sync vient de finir → nouvelle base
[ -f "$marker" ] || echo 0 > "$marker"                             # première fin de tour → base = début de session

base=$(cat "$marker" 2>/dev/null || echo 0); now=$(date +%s)
mtime=$(stat -c %Y "$marker" 2>/dev/null || stat -f %m "$marker" 2>/dev/null || echo "$now")
grown_kb=$(( (size - base) / 1024 )); elapsed_min=$(( (now - mtime) / 60 ))
[ "$grown_kb" -ge "$MIN_KB" ] && [ "$elapsed_min" -ge "$MIN_MIN" ] || exit 0

if [ "$MODE" = vault ]; then
  reason="Garde-fou vault : cette session a produit du travail depuis le dernier sync (${grown_kb} Ko de transcript, ${elapsed_min} min). Avant de rendre la main, invoque le skill sync-vault pour répercuter dans le vault ce qui a bougé dans cette conversation (décisions, statuts, todos, faits, contacts) et alléger les fiches touchées. Si rien de substantiel n'a bougé, dis-le en une ligne et termine."
else
  reason="Garde-fou vault : cette session dans le dépôt ${REPO:-$DIR} a produit du travail depuis le dernier sync (${grown_kb} Ko de transcript, ${elapsed_min} min). Avant de rendre la main, invoque le skill sync-repo pour mettre à jour la fiche projet ${SHEET} (avancement, décisions, todos, statut) à partir de cette conversation et des commits récents — cette fiche seulement, le reste va dans sa section « À répercuter ». Si rien de substantiel n'a bougé, dis-le en une ligne et termine."
fi
printf '%s' "$reason" | python3 -c 'import json,sys; print(json.dumps({"decision":"block","reason":sys.stdin.read()}, ensure_ascii=False))'
exit 0
