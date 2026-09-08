---
name: gerer-area
description: >-
  Gère le cycle de vie d'une area dans un vault déjà vivant : crée une nouvelle responsabilité
  (20-Areas/{slug}/ et fiche conforme au Schema), complète un shell vide, renomme, scinde, fusionne
  ou archive une area dont la responsabilité a disparu. Exécute un geste demandé ; le diagnostic
  appartient à audit-vault. S'utilise quand l'utilisateur dit « crée une area », « renomme / scinde
  / fusionne l'area X », « archive l'area X », « cette responsabilité n'existe plus », « l'area X
  est vide », ou reprend une suggestion d'audit. Pour scaffolder le vault entier, voir
  kickstart-vault.
---

# Gérer une area

Une area porte des projets (frontmatter `area:` et wikilink), des zones de personas et le brief :
chaque geste réécrit ces rattachements.

## Garde-fous

- **Plan puis exécution** pour tout geste multi-fichiers (renommer, scinder, fusionner, archiver) :
  construire le plan exhaustif, l'afficher, attendre la validation, proposer un commit git du
  vault, puis exécuter. Pas d'exécution directe, même sur une demande sans ambiguïté. Une
  découverte bloquante (projet actif rattaché, collision de noms) se traite avant d'agir, pas dans
  le rapport final.
- **Références structurelles seulement** : réécrire ce qui pointe vers l'area (wikilinks
  `[[slug]]`, frontmatter `area:`, chemins dans les zones des personas). Ne pas toucher aux champs
  sémantiques (`domaine:`, `tags:`, wording d'un titre) ni inventer de contenu ; en cas de doute sur
  un champ, demander.
- **Personas signalées, pas modifiées en silence** : tout changement à un
  `_personas/{slug}/CLAUDE.md` figure dans le plan. Si une persona se retrouve sans zone, alerter au
  lieu de la vider.
- **Cadre sans contenu** : à la naissance, un shell conforme et des sections vides. Le contenu entre
  par l'usage.
- **Renvoi, jamais copie pour le 🔒** (`governance.md`).

## Procédure

### 1. Localiser le vault
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé.

### 2. Aiguiller selon l'intention

| Demande | Geste | Procédure |
|---|---|---|
| « crée l'area X », « nouvelle responsabilité » | Naître | étapes 3 à 5 |
| « complète / remplis l'area X », « X est vide » | Compléter | étape 4, trous seulement |
| « renomme l'area X en Y » | Renommer | `references/restructurer.md` |
| « scinde X », « fusionne X et Y » | Scinder ou fusionner | `references/restructurer.md` |
| « archive X », « je ne m'en occupe plus » | Archiver | `references/archiver.md` |

Avant de créer, `Glob` sur `20-Areas/` et `40-Archive/`. Une area archivée du même nom : proposer
de désarchiver plutôt que recréer. Une area proche : le signaler et confirmer avant de créer.

### 3. Naître : recueillir les invariants
Lire le contrat `area` de `_Meta/Schema.md`, puis demander en une fois :
- le nom, qui donne le titre et le slug kebab-case ;
- la responsabilité en une ligne ;
- les objets récurrents, la cadence, les outils (ou « à préciser ») ;
- qui lit l'area : proposer de la rattacher aux zones d'une persona existante (lecture ou
  écriture), ce qui modifie son `CLAUDE.md` et se valide. Sans consommateur, créer quand même et le
  signaler.

### 4. Poser le shell (ou combler les trous)
- Créer `20-Areas/{slug}/{slug}.md`, jamais une fiche à plat. Frontmatter `type: area` rempli avec
  les invariants, titre, ligne de responsabilité, section `## Notes` vide. Laisser les hooks du
  vault poser `created` et `updated`.
- **Mode compléter** (shell posé par `kickstart-vault`) : comparer la fiche au contrat `area` du
  Schema, demander seulement les invariants manquants, remplir uniquement les champs et sections
  vides, sans réécrire ce qui est renseigné.

### 5. Raccrocher au vault
- **Projets existants concernés** : proposer de rattacher (frontmatter `area: "[[{slug}]]"` ; la
  fiche area liste ses projets en retour).
- **Nourrir**, en option : déléguer à `import-note` (note d'inbox, doc, URL qui fonde l'area).
- Mettre à jour un MOC ou un index s'il en existe un.
- Confirmer : chemin créé, frontmatter posé, rattachements, consommateur déclaré.

## Références
- `references/restructurer.md` : renommer, scinder, fusionner ; points de contact à recenser,
  mécanique transactionnelle.
- `references/archiver.md` : pré-checks bloquants, promotion en Resources, retrait des personas.
- Contrat `area` du vault : `_Meta/Schema.md`, lu à l'étape 3.
