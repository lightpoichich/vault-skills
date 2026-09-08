---
name: sync-repo
description: >-
  Répercute une session menée depuis un dépôt de code dans la seule fiche projet du vault qui lui
  correspond : avancement, décisions, todos, statut, à partir de la conversation et des commits
  récents. Ce qui concerne d'autres fiches est déposé dans la section « À répercuter » de la fiche
  projet, que sync-vault traite ensuite. Ne crée jamais de fiche. S'utilise quand l'utilisateur, dans
  un dépôt, dit « mets à jour la fiche projet », « répercute dans le vault », « sync le projet », ou
  sur rappel du hook Stop en fin de tour. Depuis l'intérieur du vault, sync-vault s'applique à la place.
---

# Sync repo

Le dépôt importe le vault (`@~/vault/…` dans son `CLAUDE.md`) mais le suivi vit dans la fiche projet
du vault, à un seul endroit. Ce skill met à jour cette fiche et laisse à `sync-vault` des consignes
pour le reste.

## Entrées attendues
- La conversation en cours, signal premier.
- Le dépôt : `git log` depuis la date `updated` de la fiche, `git status`.
- La fiche projet résolue par `hooks/vault-resolve.py`.

## Procédure

### 1. Résoudre la fiche
Localiser le vault et la fiche : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"`
rend `mode` (`vault`, `repo`, `none`), `vault`, `sheet`, `repo` (remote origin), `subpath` et
`match`.
- `mode: repo` : la fiche est `sheet`, continuer.
- `mode: vault` : la session est dans le vault, `sync-vault` s'applique ; le dire et s'arrêter.
- `mode: none` : aucune fiche reliée ; proposer `nouveau-projet` (mode compléter si un projet existe
  sous un autre nom, sinon naître) et s'arrêter sans rien écrire.

Si `CLAUDE_PLUGIN_ROOT` est inconnu, appliquer la règle décrite dans la docstring de
`hooks/vault-resolve.py` :
- vault : cibles des `@imports` du `CLAUDE.md` du dépôt, sinon chemin absolu déclaré dans
  `~/.claude/CLAUDE.md`, sinon `~/vault` ;
- fiche : `repo:` égal au remote `origin` normalisé, sinon `dossier-travail:` égal au dossier ou à
  un ancêtre, sinon slug égal au nom du dossier ;
- lire ensuite `_Meta/Schema.md` du vault trouvé.

### 2. Lire
La fiche, et le contrat `project` de `{vault}/_Meta/Schema.md` (champs et valeurs de ce vault).

### 3. Repérer ce qui a bougé
- Conversation : décisions et leur raison, avancement, blocages, todos nés ou faits, changement de
  périmètre ou de deadline, faits et contacts nouveaux.
- Dépôt : `git log --since="{updated de la fiche}" --format='%ad %s' --date=short` et
  `git status --short`. Les commits datent et confirment ; le non commité reste « en cours ».

### 4. Écrire la fiche
- `## Suivi` : l'état courant en quelques lignes datées (où on en est, prochain pas, blocage).
  Remplacer, ne pas empiler.
- `## Décisions` : une ligne par décision nouvelle, avec la raison. Les décisions existantes ne
  bougent pas, sauf revirement explicite.
- Todos : cocher le fait, ajouter le né, retirer le périmé.
- Frontmatter : `status` seulement si l'utilisateur l'a dit (`paused`, `done`) ; `repo:` posé s'il
  manque et que le dépôt a un remote `origin` (`URL#sous-dossier` si le dossier courant n'est pas la
  racine du dépôt) ; `dossier-travail:` jamais touché, c'est une indication propre au poste. Le hook
  du plugin pose `updated`.
- Rien de substantiel n'a bougé : le dire en une ligne, ne rien écrire.

### 5. Déposer ce qui déborde
Tout ce qui concerne une autre fiche va dans une section `## À répercuter` en fin de fiche projet,
une ligne par item, datée, cible en `[[wikilink]]` : « {date} · [[client]] : nouveau contact X
(rôle) », « {date} · [[tech]] : pattern Y à capitaliser ». `sync-vault` la traite et la vide à son
prochain passage depuis le vault.

### 6. Rendre compte
Trois lignes au plus : ce qui a été mis à jour dans la fiche, ce qui a été déposé « À répercuter »,
le `repo:` posé le cas échéant.

## Garde-fous
- Une seule fiche, celle que la résolution désigne. Fiche client, area, ressource, draft, mémoire de
  Claude Code : une ligne dans « À répercuter », pas d'écriture directe.
- Pas de fiche inventée : sans fiche résolue, proposer `nouveau-projet` et s'arrêter.
- Même discipline de curation que `sync-vault` (`sync-vault/references/curation.md`) : remplacer le
  périmé, fusionner les redites, garder décisions et raison, statut courant, engagements vivants. Le
  `## Suivi` décrit l'état courant, pas l'historique des sessions.
- Le commit n'est pas la vérité : la conversation prime, un changement non commité est « en cours »,
  pas « fait ».
- Le sensible 🔒 n'entre ni dans la fiche ni dans « À répercuter ».
