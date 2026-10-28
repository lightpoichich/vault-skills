---
name: sync-vault
description: >-
  Met à jour et consolide les fiches du vault à partir de la conversation en cours. Depuis le vault :
  décisions, statuts, todos, sections « À répercuter », sas 00-Inbox/_drafts/ et mémoire native de
  Claude Code. Depuis un dossier de travail relié à un projet, dépôt de code ou dossier sans git : la
  seule fiche projet, le reste déposé en « À répercuter ». Agit sans validation et réécrit plutôt
  qu'empiler. S'utilise quand l'utilisateur dit « sync le vault », « sync le projet », « mets à jour
  la fiche projet », « répercute ce qu'on a décidé », ou sur rappel du hook Stop en fin de tour.
---

# Sync vault

Un seul skill de répercussion, deux modes. Le mode vient du script de résolution, jamais d'une
déduction : depuis le vault, toutes les fiches ; depuis un dossier de travail relié, la seule fiche
projet.

## Entrées attendues
- La conversation en cours : décisions, statuts, todos, faits et contacts nouveaux. C'est le signal
  premier dans les deux modes.
- Le mode et la fiche rendus par `hooks/vault-resolve.py`.
- En mode vault : les sections `## À répercuter` des fiches projet, le sas `00-Inbox/_drafts/`,
  `30-Resources/` et le dossier mémoire de Claude Code. En mode projet : la fiche résolue et, dans
  un dépôt git, son historique.

## Procédure

### 1. Résoudre le mode
`python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode` (`vault`, `projet`,
`none`), `vault` (racine), `sheet` (fiche projet), `repo` (remote `origin`, vide hors dépôt git),
`subpath` et `match`.

Si `CLAUDE_PLUGIN_ROOT` est inconnu, appliquer la règle décrite dans la docstring du script :
- dans le vault : un ancêtre du dossier contient `_Meta/` ;
- sinon, vault : cibles des `@imports` du `CLAUDE.md` du dossier, sinon chemin absolu déclaré dans
  `~/.claude/CLAUDE.md`, sinon `~/vault` ;
- fiche : `repo:` égal au remote `origin` normalisé, sinon un `dossier-travail:` égal au dossier ou
  à un ancêtre, sinon, dans un dépôt git seulement, slug égal au nom du dossier.

Lire ensuite `_Meta/Schema.md` du vault trouvé.

### 2. Suivre le mode
- `mode: vault` : dérouler `references/mode-vault.md`.
- `mode: projet` : dérouler `references/mode-projet.md`. Une seule fiche est écrite, `sheet` ; ce
  qui concerne une autre fiche va dans sa section `## À répercuter`.
- `mode: none` : aucune fiche reliée. Proposer `structurer` (mode compléter si le projet existe
  sous un autre nom, sinon naître) et s'arrêter sans rien écrire.

### 3. Curer en écrivant
Pour chaque fiche écrite : intégrer les faits nouveaux à la bonne section, remplacer le périmé,
fusionner les redites, élaguer le bruit en préservant décisions et raison, statut courant,
engagements vivants et wikilinks. Quoi intégrer, garder et élaguer : `references/curation.md`,
sections 1 à 3. Le récit daté (réunion, avancement, échange) ne s'élague pas : il entre complet en
tête de `## Journal`, en ajout seul (`curation.md`, section 7). Les hooks du vault posent `updated`.

### 4. Rendre compte
Résumer après coup, avec le contenu que la référence du mode demande. Si rien de substantiel n'a
bougé et qu'aucune fiche n'a besoin d'être allégée, répondre seulement « Rien à répercuter. » et ne
rien écrire.

## Garde-fous
- Autonome : décider et écrire sans validation préalable, rendre compte après. Écraser, fusionner et
  réécrire sont autorisés ; empiler ne l'est pas.
- Règle du doute : un élément dont l'importance est incertaine se garde.
- Pas de fiche inventée : sans fiche résolue en mode projet, proposer `structurer`.
- Le sensible 🔒 ne se copie ni dans une fiche, ni dans « À répercuter », ni en mémoire ; renvoi
  seulement (`governance.md`).
- Respecter le contrat de `_Meta/Schema.md` pour tout frontmatter touché.

## Références
- `references/mode-vault.md` : procédure depuis le vault (sections « À répercuter », sas des drafts,
  `30-Resources/`, mémoire native).
- `references/mode-projet.md` : procédure depuis un dossier de travail relié (la fiche projet seule,
  historique git s'il existe, dépôt dans « À répercuter »).
- `references/curation.md` : quoi intégrer, garder et élaguer ; registre des sources ; veille de
  `30-Resources/` ; curation des drafts avec ses seuils.
- `references/memoire-claude-code.md` : où vit la mémoire native, comment vérifier qu'elle est
  active, quoi y distiller, plafond de rappel.
- `ranger/references/classement.md` : frontmatter, liens, renvoi plutôt que copie.
