---
name: nouveau-projet
description: >-
  Crée un projet dans un vault Obsidian déjà structuré, ou complète un projet encore vide : pose
  10-Projects/{slug}/{slug}.md avec un frontmatter type: project conforme au Schema, relie l'Area
  parente et le dossier de travail, puis rattache le contexte réel existant
  (note d'inbox, réunion, fil d'emails) via import-note, sans rien inventer. S'utilise quand
  l'utilisateur dit « lancer un nouveau projet », « créer le projet X », « ouvrir un chantier »,
  « complète le projet X », « le projet X est vide ». Pour faire entrer une note isolée sans créer de
  projet, voir import-note.
---

# Nouveau projet

## Entrées attendues
- Le nom du projet à créer, ou le slug d'un projet existant à compléter.
- Le dossier courant, s'il est hors du vault : c'est le dossier de travail candidat à relier.
- Le contexte réel à rattacher, s'il existe : note d'inbox, réunion, fil d'emails, doc, URL.

## Procédure

### 1. Localiser le vault
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé : son contrat `type: project`
fixe les champs à poser.

Si le dossier courant est hors du vault (`mode` égal à `repo` ou `none`), noter son chemin absolu :
c'est le dossier de travail à relier à l'étape 4. Lancé depuis l'intérieur du vault, il n'y a pas de
dossier de travail et les champs `repo:` et `dossier-travail:` sont omis.

### 2. Recueillir les invariants
Si la demande vise un projet existant (« complète le projet X », « X est vide »), passer à
l'étape 3 : seuls les trous seront demandés.

Demander à l'utilisateur, en une fois, ce qui remplit le frontmatter `type: project` :
- le nom du projet, dont dérivent le titre et le slug en kebab-case ;
- le livrable et le critère de fin ;
- la deadline, ou « à préciser » ;
- les parties prenantes ;
- l'Area parente, à choisir parmi les `20-Areas/` existants. Un projet sans area reste possible, le
  signaler.

### 3. Chercher l'existant
`Glob` sur `10-Projects/` et `Grep` sur un terme clé du nom, `40-Archive/` compris. Trois cas :
- **Introuvable** : mode naître, dérouler les étapes 4 à 7.
- **Trouvé** : mode compléter. Lire la fiche, la comparer au contrat `project` du Schema, demander
  seulement les invariants manquants, puis reprendre aux étapes 4 (liaison au dossier de travail
  seule) à 7. Remplir uniquement les champs et sections vides. Une fiche trouvée dans `40-Archive/`
  se désarchive plutôt que d'être recréée.
- **Projet proche mais distinct** : le signaler et confirmer avant de créer, pour éviter le doublon.

### 4. Poser le shell et relier le dossier de travail
- Créer `10-Projects/{slug}/` et la fiche `10-Projects/{slug}/{slug}.md`, jamais à plat.
- Frontmatter `type: project` rempli avec les invariants de l'étape 2 : `status: active`,
  `deadline`, `livrable`, `parties-prenantes`, `area: "[[{area}]]"`, `tags: [project]`. Les hooks du
  vault posent `created` et `updated`.
- Corps : titre, une ligne de résumé, puis trois sections vides : `## Objectif`, `## Suivi`,
  `## Décisions`.
- Relier le dossier de travail noté à l'étape 1 : suivre la checklist de
  `references/liaison-depot.md`. En mode compléter, elle s'applique aussi à une fiche sans `repo:`
  ni `dossier-travail:`.

### 5. Nourrir
Proposer de rattacher le contexte réel du projet : une note de `00-Inbox/` où l'idée a germé, la
réunion où il a été décidé, un fil d'emails, un doc, une URL. Déléguer l'acquisition à
`import-note`, puis lier le résultat depuis la fiche projet en `[[wikilinks]]`. Quoi rattacher et
comment : `references/nourrir.md`.

### 6. Raccrocher au vault
- Wikilink bidirectionnel : la fiche projet pointe vers `[[{area}]]`, la fiche de l'Area parente (ou
  son MOC) gagne un lien vers le projet.
- Ressources : balayer `30-Resources/` (noms de fichiers et `_index.md` des sous-zones) et proposer
  un à trois `[[wikilinks]]` vers ce qui sert le projet (trame, runbook, doc de référence). Zéro
  lien vaut mieux qu'un lien décoratif.
- Mettre à jour un MOC ou un index de projets s'il en existe un.

### 7. Confirmer
Afficher le chemin créé, le frontmatter posé, les rattachements faits et la liaison au dépôt. Ne
rien écraser sans validation.

## Garde-fous
- Poser le cadre, pas le contenu : sections vides, rien d'inventé, le suivi se remplit par l'usage.
- Chercher l'existant avant de créer ; enrichir plutôt que dupliquer ; ne pas réécrire un champ déjà
  renseigné.
- Le sensible 🔒 se rattache en renvoi, jamais en copie (`governance.md`).

## Références
- `references/liaison-depot.md` : checklist pour poser `repo:` et `dossier-travail:` et approuver
  les imports du `CLAUDE.md` du dépôt.
- `references/nourrir.md` : quoi rattacher, règle de résolution des sources, délégation à
  `import-note`.
- `import-note/references/classement.md` : frontmatter, liens, renvoi d'emplacement, renvoi plutôt
  que copie.
