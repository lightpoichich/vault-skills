#!/usr/bin/env bash
# vault-lib.sh — fonctions communes aux hooks du plugin second-cerveau. Sourcé, jamais exécuté.
#
# Un vault = un dossier contenant `_Meta/`. Les hooks du plugin tournent dans TOUTE session Claude Code
# (le plugin est actif partout) : ils doivent être no-op, silencieux et instantanés hors d'un vault.
#
# Config optionnelle : `{vault}/_Meta/hooks.conf` (KEY=VALUE, une par ligne, # commentaires) :
#   EXCLUDE=20-Areas/donnees-importees,outillage     chemins relatifs (préfixes) ignorés par H1 santé et H2 garde-fou écriture
#   INBOX_STALE_DAYS=14             seuil d'ancienneté d'une note d'Inbox (H1)
#   APPROVE_EXTERNAL_IMPORTS=0      H3 : ne plus approuver soi-même les imports du vault dans ~/.claude.json
#   SYNC_MIN_KB=40                  H4 : Ko de transcript écrits depuis le dernier sync avant de rappeler sync-vault
#   SYNC_MIN_MINUTES=20             H4 : minutes écoulées depuis le dernier sync (les deux seuils doivent être atteints)
#   SYNC_NUDGE=0|vault              H4 : 0 = aucun rappel ; vault = rappel depuis le vault seulement, pas depuis les dossiers de travail
#   SYNC_NUDGE_WORKTREES=1          H4 : rappeler aussi depuis un worktree git lié (par défaut, un worktree de ticket ne rappelle pas)
#   AUDIT_REMINDER_DAYS=30          H1 : âge du dernier rapport audit-vault au-delà duquel le bilan le signale (0 coupe le rappel)
#   JOURNAL_ROTATION=1              vault-journal.py : autorise la rotation écrite des journaux de fiche (0 par défaut)
#   JOURNAL_MAX_KB_{TYPE}=Ko        budget de taille par type de fiche (AREA=20, PROJECT=30 par défaut) ; H1 signale le dépassement
#   JOURNAL_MAX_KB=30               budget des autres types, seulement pour une fiche qui a une section de journal
#   JOURNAL_SECTIONS=Journal        sections rotables (liste blanche) ; tout le reste de la fiche est protégé
#   JOURNAL_KEEP=5                  entrées les plus récentes jamais déplacées, par section
#   MEMORY_MAX_LINES=120            vault-memory.py : budget de l'index MEMORY.md en lignes (plafond Claude Code : 200)
#   MEMORY_MAX_KB=16                budget de l'index en milliers de caractères (plafond Claude Code : 25 000) ; H1 signale le dépassement
#   MEMORY_CURATION_DAYS=30         curation complète due par sync-vault au-delà de ce délai depuis la dernière sauvegarde

# vault_root <chemin> → imprime la racine du vault contenant <chemin>, rien si aucune. Remonte jusqu'à /.
vault_root() {
  local d="$1"
  [ -n "$d" ] || return 1
  [ -d "$d" ] || d="$(dirname "$d")"
  while [ "$d" != / ] && [ -n "$d" ]; do
    [ -d "$d/_Meta" ] && { printf '%s\n' "$d"; return 0; }
    d="$(dirname "$d")"
  done
  return 1
}

# vault_conf <racine> <clé> <défaut> → valeur de la clé dans _Meta/hooks.conf, sinon le défaut.
vault_conf() {
  local f="$1/_Meta/hooks.conf" v
  [ -f "$f" ] && v="$(sed -n "s/^[[:space:]]*$2[[:space:]]*=[[:space:]]*//p" "$f" | tail -1 | sed 's/[[:space:]]*#.*$//; s/[[:space:]]*$//')"
  printf '%s\n' "${v:-$3}"
}

# stdin_field <clé JSON de premier niveau ou tool_input.x> → valeur (chaîne vide si absente).
stdin_field() {
  printf '%s' "$HOOK_INPUT" | python3 -c '
import sys, json
try: d = json.load(sys.stdin)
except Exception: sys.exit(0)
k = sys.argv[1]
if k.startswith("tool_input."):
    d = d.get("tool_input") or {}; k = k.split(".", 1)[1]
v = d.get(k, "")
print(v if isinstance(v, str) else "")' "$1" 2>/dev/null
}
