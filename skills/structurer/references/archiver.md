# Archiver une area ou un projet

Ce qui est clos part en `40-Archive/` (on déplace, on ne supprime pas) et ce qui reste utile est
promu en `30-Resources/`. Plan, validation et filet git suivent les garde-fous du `SKILL.md`.
Rangement dans l'archive : suivre l'existant de `40-Archive/` (sous-dossier `projects/` ou `areas/`
s'il existe), sinon `40-Archive/{slug}/`.

## Area : la responsabilité disparaît

### 1. Pré-checks, avant le plan et bloquants

Dans cet ordre, avant de rien déplacer :

1. **Projets actifs rattachés.** `Grep` le frontmatter `area: "[[{slug}]]"` sur `10-Projects/`.
   Tout projet `status: active` bloque : demander où le réaffecter en proposant les areas
   existantes, un projet vivant ne pointe pas vers une archive. L'utilisateur peut décider que le
   projet s'archive aussi ; il se traite alors avec `status: done` et déplacement vers
   `40-Archive/`. Tant que ce n'est pas tranché, l'area n'est pas archivée.
2. **Contenu encore utile.** Parcourir le dossier de l'area. Une note qui sert au-delà de la
   responsabilité morte (trame, référentiel, benchmark) : proposer sa promotion en `30-Resources/`
   (frontmatter `type: resource`, wikilinks repris).
3. **Personas.** Repérer chaque `_personas/*/CLAUDE.md` qui déclare une zone sur cette area ; le
   retrait fait partie du plan. Si une persona se retrouve sans aucune zone, alerter : l'utilisateur
   décide de la retirer ou de la repointer, pas le skill.

### 2. Le plan
Réaffectations décidées, promotions vers Resources, déplacement de `20-Areas/{slug}/` vers
`40-Archive/{slug}/`, retraits de zones des personas, devenir des wikilinks entrants. Validation,
puis commit git proposé.

### 3. Exécution
- Réaffecter les projets et promouvoir les notes décidées avant le déplacement, pour que les
  chemins restent vrais.
- Déplacer le dossier entier vers `40-Archive/{slug}/`.
- Marquer la fiche : le Schema ne prévoit pas de `status` pour `area`. Poser une ligne « Archivée
  le {date}, {raison en quelques mots} » en tête de corps, frontmatter inchangé (pas de champ hors
  Schema).
- Retirer la zone des personas concernées (changement listé au plan).
- Ne pas réécrire les wikilinks entrants `[[{slug}]]` : ils résolvent par nom et l'historique
  (briefs passés, meetings) continue de pointer vers la fiche archivée.

### 4. Rapport
Actions faites, projets réaffectés, notes promues, personas modifiées, alerte « persona sans
zone » le cas échéant.

## Projet : livré, abandonné ou en sommeil

### 1. Pré-checks, avant le plan
1. **Raison.** Livré, abandonné ou mis en sommeil : la demander si elle n'est pas dite. Un projet
   « en sommeil » qui reprendra garde souvent `status: active` avec une deadline recalée ; le
   proposer avant d'archiver.
2. **Restes à répercuter.** Une section `## À répercuter` non vide ou des todos ouverts se traitent
   d'abord : les reporter là où ils vivent encore (area, autre projet) ou les clore, sur décision.
3. **Contenu encore utile.** Une méthode réutilisable est candidate à une trame (`ranger`, mode
   trame) ; un référentiel est promu en `30-Resources/`.
4. **Dossier de travail relié.** Une fiche avec `repo:` ou `dossier-travail:` cesse d'être trouvée
   depuis ce dossier une fois archivée : le résolveur ne cherche que dans `10-Projects/`. Le
   signaler ; depuis ce dossier, `sync-vault` ne proposera plus rien.
5. **Personas.** Une zone de persona sur le dossier du projet se retire, changement listé au plan.

### 2. Le plan
Statut final, report des restes, promotions, déplacement de `10-Projects/{slug}/` vers l'archive,
zones de personas retirées. Validation, puis commit git proposé.

### 3. Exécution
- Reporter les restes et promouvoir les notes décidées avant le déplacement.
- Frontmatter : `status: done`, ou le statut d'abandon que prévoit le Schema ; sans tel statut,
  `done` et la raison dans le corps.
- Poser « Archivé le {date}, {raison en quelques mots} » en tête de corps.
- Déplacer le dossier entier, sous-dossiers compris (`meetings/`, `journal/`).
- Ne pas réécrire les wikilinks entrants : la fiche d'area et l'historique continuent de résoudre
  par nom. Dans la liste des projets de l'area, marquer le projet comme archivé.

### 4. Rapport
Actions faites, restes reportés, notes promues, dossier de travail délié, personas modifiées.
