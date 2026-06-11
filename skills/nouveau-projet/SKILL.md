---
name: nouveau-projet
description: >-
  Crée un nouveau projet dans un vault Obsidian **déjà vivant** : génère le dossier
  `10-Projects/{slug}/` et sa fiche `{slug}.md` (frontmatter `type: project` conforme au Schema du
  vault, wikilink vers l'Area parente), puis **nourrit** le projet en y rattachant le contexte réel
  existant (note d'inbox, réunion, fil d'emails) via `import-note` — sans rien inventer. Utilise ce
  skill dès que l'utilisateur veut « lancer un nouveau projet », « créer le projet X », « ajouter un
  projet », « démarrer un dossier projet », « ouvrir un chantier » dans son vault. **Transverse**
  (depuis n'importe quelle persona) et **source-agnostique** (lit `_Meta/sources.md`, dégrade
  proprement). NE PAS l'utiliser pour scaffolder le vault entier (`kickstart-vault`, qui pose les
  Projects au moment de l'amorçage), pour faire entrer une note externe déjà existante
  (`import-note`), pour créer une persona (`kickstart-persona`), ni pour répercuter une session dans
  le vault (`sync-vault`).
---

# Nouveau projet

Faire **naître** un projet dans un vault déjà vivant. Le jumeau d'`import-note` : import-note fait
*entrer* un contenu qui existe déjà ; `nouveau-projet` fait *naître* un effort neuf, lui pose son foyer
(dossier + fiche), puis le raccroche au contexte réel.

C'est un geste de **Famille 2 (faire vivre)**, pas d'amorçage : `kickstart-vault` génère les shells de
Projects une seule fois, au scaffold. Ici on ajoute un projet *après*, à la demande, sans relancer
l'interview de cartographie.

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
Demander — sans noyer le dirigeant — ce qui remplit le frontmatter `type: project` :
- **nom** du projet (→ titre + slug `kebab-case`) ;
- **livrable + critère de fin** (ce qui dira « c'est terminé ») ;
- **deadline** (ou « à préciser ») ;
- **parties prenantes** ;
- **Area parente** : la responsabilité continue à laquelle le projet se rattache (proposer parmi les
  `20-Areas/` existants ; un projet sans area est possible, mais le signaler).

### 3. Vérifier le non-doublon
`Glob` sur `10-Projects/` et `Grep` un terme clé du nom (penser aussi à `40-Archive/`). Si un projet
proche existe → proposer de **l'enrichir** (ou de désarchiver) plutôt que de recréer.

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
