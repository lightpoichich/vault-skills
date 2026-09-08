---
name: sync-repo
description: >-
  Répercute une session de travail menée **depuis un dépôt de code** (dossier de travail hors vault)
  dans **la seule fiche projet** du vault qui lui correspond : avancement, décisions, todos, statut —
  à partir de la conversation en cours et des commits récents. Retrouve la fiche par la clé `repo:`
  (remote git), sinon `dossier-travail:`, sinon le slug ; ne crée jamais de fiche. Tout ce qui
  déborde de la fiche projet (fiche client, area, ressource, mémoire) est **déposé dans sa section
  « À répercuter »** que `sync-vault` traite ensuite depuis le vault. **Autonome, sans validation**,
  concis et jamais append-only. Utilise ce skill dès que l'utilisateur, dans un repo, dit « mets à
  jour la fiche projet », « répercute dans le vault », « sync le projet », ou quand le hook Stop du
  plugin le rappelle en fin de tour. NE PAS l'utiliser depuis l'intérieur du vault ni pour curer
  d'autres fiches que celle du projet (`sync-vault`), pour relier un dépôt à un nouveau projet
  (`nouveau-projet`), ni pour faire entrer un document (`import-note`).
---

# Sync repo

La version **réduite et ciblée** de `sync-vault`, pour les sessions qui se passent dans un dépôt de
code. Le dépôt importe le vault (règle de liaison, `@~/vault/…` dans son `CLAUDE.md`) mais il n'est
pas le lieu du suivi : le suivi vit dans la fiche projet du vault, et **nulle part ailleurs** (pas de
fiche locale au dépôt, qui doublonnerait et divergerait — `governance.md`, une information vit à un
seul endroit).

Famille 3 (Entretenir). Périmètre volontairement étroit : **une fiche, celle du projet**. La
curation du reste du vault demande la vue d'ensemble d'une persona ; ce skill lui laisse des
consignes plutôt que de décider à sa place.

## Principe à garder en tête

- **Une seule fiche.** Celle que la résolution désigne. Jamais la fiche client, l'area, une
  ressource, un draft, la mémoire de Claude Code, ni un 🔒 : pour ça, une ligne dans « À répercuter ».
- **Jamais de fiche inventée.** Aucune fiche résolue → proposer `nouveau-projet` (qui relie le
  dépôt) et s'arrêter.
- **Autonome, pas append-only.** Même discipline que `sync-vault` (`sync-vault/references/curation.md`) :
  remplacer le périmé, fusionner les redites, garder décisions + raison, statut courant, engagements
  vivants. Le `## Suivi` décrit **l'état courant**, pas l'historique des sessions.
- **Le commit n'est pas la vérité.** Le signal premier est la conversation. Le `git log` complète ;
  un changement non commité est « en cours », pas « fait ».
- **Bookkeeping autorisé.** Poser `repo:` quand il manque (clé portable entre machines) ; ne jamais
  toucher `dossier-travail:` (indication propre à un poste).

## Procédure

### 1. Résoudre la fiche
Lancer le résolveur du plugin depuis le dossier courant :
```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"
```
Il rend `mode` (`vault` / `repo` / `none`), `vault`, `sheet`, `repo` (remote origin), `subpath`, `match`.
- `mode: repo` → la fiche est `sheet`. Continuer.
- `mode: vault` → on est dans le vault : c'est `sync-vault` qui s'applique, le dire et s'arrêter.
- `mode: none` → pas de fiche reliée : proposer `nouveau-projet` (mode compléter si un projet existe
  sous un autre nom, sinon naître) et s'arrêter. Ne rien écrire.

Si `CLAUDE_PLUGIN_ROOT` est inconnu, appliquer la même règle à la main : `git remote get-url origin`
normalisé (sans schéma, `user@`, `.git`) comparé aux `repo:` des fiches `type: project` de
`10-Projects/` (suffixe `#sous-dossier` = le projet vit dans un sous-dossier du dépôt), sinon
`dossier-travail:` égal au dossier ou à un ancêtre, sinon slug = nom du dossier. Le vault se trouve par
les `@imports` du `CLAUDE.md` du dépôt, sinon par le chemin absolu déclaré dans `~/.claude/CLAUDE.md`.

### 2. Lire
La fiche, et le contrat `project` de `{vault}/_Meta/Schema.md` (champs et valeurs de **ce** vault).

### 3. Repérer ce qui a bougé
- **Conversation** : décisions (et leur raison), avancement, blocages, todos nés ou faits, changement
  de périmètre ou de deadline, faits et contacts nouveaux.
- **Dépôt** : `git log --since="{updated de la fiche}" --format='%ad %s' --date=short` et
  `git status --short`. Les commits datent et confirment ; le non-commité reste « en cours ».

### 4. Écrire la fiche (overwrite autorisé)
- **`## Suivi`** : l'état courant en quelques lignes datées (où on en est, prochain pas, blocage).
  Remplacer, ne pas empiler.
- **`## Décisions`** : une ligne par décision nouvelle, avec la raison. Les décisions existantes ne
  bougent pas, sauf si elles sont explicitement revenues.
- **Todos** : cocher le fait, ajouter le né, retirer le périmé.
- **Frontmatter** : `status` seulement si l'utilisateur l'a dit (`paused`, `done`) ; `repo:` posé
  s'il manque et que le dépôt a un remote `origin` (`URL#sous-dossier` si le dossier courant n'est
  pas la racine du dépôt). Laisser le hook du plugin poser `updated`.
- **Rien à écrire** si rien de substantiel n'a bougé : le dire en une ligne.

### 5. Déposer ce qui déborde
Tout ce qui concerne une autre fiche va dans une section **`## À répercuter`** en fin de fiche projet,
une ligne par item, datée, avec la cible en `[[wikilink]]` : « 2026-09-08 · [[client]] : nouveau
contact X (rôle) » ; « 2026-09-08 · [[tech]] : pattern Y à capitaliser ». `sync-vault` la traite et la
vide à son prochain passage depuis le vault. Ne jamais y mettre de 🔒.

### 6. Rendre compte
Trois lignes au plus : ce qui a été mis à jour dans la fiche, ce qui a été déposé « À répercuter »,
et le `repo:` posé le cas échéant.
