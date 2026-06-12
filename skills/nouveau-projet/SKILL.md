---
name: nouveau-projet
description: >-
  Crée **ou complète** un projet dans un vault Obsidian **déjà vivant** : génère
  `10-Projects/{slug}/{slug}.md` (frontmatter `type: project` conforme au Schema, wikilink vers
  l'Area parente), puis **nourrit** le projet du contexte réel existant (note d'inbox, réunion, fil
  d'emails) via `import-note` — sans rien inventer. Sur un shell déjà posé (par `kickstart-vault`
  au scaffold), même geste : invariants manquants + nourrir, sans écraser l'existant. Utilise ce
  skill dès que l'utilisateur veut « lancer un nouveau projet », « créer le projet X », « ouvrir un
  chantier », ou dit « complète / initialise / remplis le projet X », « le projet X est vide ».
  **Transverse** et **source-agnostique** (lit `_Meta/sources.md`, dégrade proprement). NE PAS
  l'utiliser pour scaffolder le vault entier (`kickstart-vault` pose les shells une fois — ce skill
  les complète ensuite), pour faire entrer une note externe isolée (`import-note`), pour créer une
  persona (`kickstart-persona`), ni pour répercuter une session (`sync-vault`).
---

# Nouveau projet

Faire **naître** un projet dans un vault déjà vivant — ou **compléter** un projet qui n'est encore
qu'un shell. Le jumeau d'`import-note` : import-note fait *entrer* un contenu qui existe déjà ;
`nouveau-projet` fait *naître* un effort neuf, lui pose son foyer (dossier + fiche), puis le raccroche
au contexte réel. Le même geste, appliqué à une fiche déjà posée, la complète.

C'est un geste de **Famille 2 (faire vivre)**, pas d'amorçage : `kickstart-vault` génère les shells de
Projects une seule fois, au scaffold — des coquilles volontairement vides. Ici on ajoute un projet
*après*, à la demande, sans relancer l'interview de cartographie — et c'est aussi ici que ces shells
se remplissent, au fil de l'eau.

## Principe à garder en tête

- **Generate-don't-write.** On pose le shell (dossier, fiche, frontmatter, sections vides). On ne
  remplit pas le suivi avec du contenu inventé — il se remplira au fil du projet.
- **Nourrir avec du réel, pas du fabriqué.** « Configuré et nourri » = rattacher le contexte qui
  existe déjà (la note où l'idée est née, la réunion, le fil d'emails), pas générer un faux brief.
- **Non destructif.** On cherche un projet existant avant d'en créer un ; on enrichit plutôt que
  dupliquer.
- **Renvoi-jamais-copie pour le sensible.** Le 🔒 se rattache en renvoi, jamais en copie (voir
  `import-note` et `governance.md`).

## Procédure

### 1. Localiser le vault
Remonter depuis le dossier courant jusqu'à la racine (présence de `CLAUDE.md` + `_Meta/Schema.md`).

### 2. Recueillir les invariants (court, interactif)
Si la demande vise un projet existant (« complète le projet X », « X est vide »), passer directement
à l'étape 3 : on ne demandera que les trous.

Demander — sans noyer le dirigeant — ce qui remplit le frontmatter `type: project` :
- **nom** du projet (→ titre + slug `kebab-case`) ;
- **livrable + critère de fin** (ce qui dira « c'est terminé ») ;
- **deadline** (ou « à préciser ») ;
- **parties prenantes** ;
- **Area parente** : la responsabilité continue à laquelle le projet se rattache (proposer parmi les
  `20-Areas/` existants ; un projet sans area est possible, mais le signaler).

### 3. Chercher l'existant — l'aiguillage naître / compléter
`Glob` sur `10-Projects/` et `Grep` un terme clé du nom (penser aussi à `40-Archive/` → proposer de
**désarchiver** plutôt que recréer). Trois cas :
- **Introuvable** → mode **naître** : dérouler les étapes 4 à 7.
- **Trouvé** (shell scaffoldé par `kickstart-vault`, ou fiche maigre) → mode **compléter** : lire la
  fiche et la comparer au contrat `project` de `_Meta/Schema.md`, demander **seulement les invariants
  manquants** (étape 2 réduite aux trous), puis reprendre aux étapes 5-7 (nourrir, raccrocher,
  confirmer). **Non destructif** : remplir uniquement les champs et sections vides — ne jamais
  réécrire ce qui est déjà renseigné.
- **Projet proche mais distinct** → le signaler et confirmer avant de créer, pour éviter le doublon.

### 4. Scaffolder le shell
- **Lire `_Meta/Schema.md`** pour le contrat `project` de **ce** vault (les champs peuvent varier d'un
  vault à l'autre) — c'est la source de vérité au moment de l'écriture.
- Créer le dossier `10-Projects/{slug}/` et la fiche `10-Projects/{slug}/{slug}.md` (jamais à plat).
- Structure du shell : frontmatter `type: project` rempli avec les invariants de l'étape 2 (`status:
  active`, `deadline`, `livrable`, `parties-prenantes`, `area: "[[{area}]]"`, `tags: [project]`),
  puis titre, une ligne de résumé, et les sections **vides** `## Objectif` · `## Suivi` ·
  `## Décisions`. Laisser les hooks du vault poser `created`/`updated`.

### 5. Nourrir (source-agnostique — voir `references/nourrir.md`)
Proposer de rattacher le **contexte réel** du projet :
- une note de `00-Inbox/` où l'idée a germé ;
- la réunion où il a été décidé (cascade `_Meta/sources.md` : Granola/agenda si déclaré actif, sinon
  collage manuel) ;
- un fil d'emails, un doc, une URL.

Déléguer l'acquisition à **`import-note`** (ne pas redupliquer la logique URL/Notion/fichier/collage),
puis lier le résultat depuis la fiche projet en `[[wikilinks]]`. Rien d'inventé, jamais de copie du 🔒.

### 6. Raccrocher au vault
- Wikilink **bidirectionnel** : la fiche projet pointe vers `[[{area}]]`, et la fiche de l'Area parente
  (ou son MOC) gagne un lien vers le projet.
- **Ressources pertinentes** : balayer `30-Resources/` (noms de fichiers + `_index.md` des
  sous-zones), **proposer** 1-3 `[[wikilinks]]` vers ce qui sert ce projet — une trame, un runbook,
  un doc de référence (CGV, design system…). Proposer seulement ce qui résonne — jamais de liste
  déversée, zéro lien vaut mieux qu'un lien décoratif.
- Mettre à jour un MOC/index de projets s'il en existe un.

### 7. Confirmer
Afficher le chemin créé, le frontmatter posé, les rattachements faits, et un aperçu court. Ne rien
écraser sans validation.

## Références
- `references/nourrir.md` — quoi rattacher, et comment déléguer l'acquisition à `import-note`.
- Contrat `project` du vault : `_Meta/Schema.md` (lu à l'étape 4).
- Classement universel (frontmatter, liens, renvoi-vs-copie) : `import-note/references/classement.md`.
