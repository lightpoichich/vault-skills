#!/usr/bin/env bash
# vault-git-sync.sh — template OPT-IN (pas un hook du plugin) : sync git d'un vault sur une machine
# headless (VM d'agents). À copier dans `{vault}/.claude/hooks/` et brancher soi-même (voir kickstart-vault §5bis).
# Trois modes :
#   pull  (SessionStart)  → pull --rebase --autostash
#   (défaut, Stop)        → commit LOCAL seulement ; amende le commit auto précédent tant qu'il n'est pas poussé
#   push  (timer 10 min)  → commit si besoin, puis pull --rebase + push si quelque chose est en attente
# Gate Linux : sur le poste (Mac), un client git type Obsidian Git fait le travail ; le hook ne tourne que sur la VM.
[ "$(uname)" = Linux ] || exit 0
cd "$(git -C "${CLAUDE_PROJECT_DIR:-.}" rev-parse --show-toplevel 2>/dev/null)" || exit 0   # cwd persona → racine
exec 9>.git/vault-sync.lock; flock -w 60 9 || exit 0   # hook et timer ne se marchent pas dessus

msg="vault: $(hostname) $(date +%F' '%H:%M)"
commit() {
  git add -A; git diff --cached --quiet && return 0
  if git log -1 --format=%s | grep -q '^vault: ' && ! git merge-base --is-ancestor HEAD @{u} 2>/dev/null
  then git commit -q --amend -m "$msg"     # commit auto pas encore poussé → on l'écrase
  else git commit -qm "$msg"; fi
}
sync() { git pull -q --rebase --autostash || { git rebase --abort; echo "vault: conflit git, résoudre à la main" >&2; return 1; }; git push -q; }

case "${1:-}" in
  pull) git pull -q --rebase --autostash || git rebase --abort ;;
  push) commit; git merge-base --is-ancestor HEAD @{u} 2>/dev/null || sync ;;
  *)    commit ;;
esac
