---
name: structurer
description: >-
  Crée et fait évoluer les contenants du vault, projets et areas : pose une fiche conforme au
  Schema, complète un shell vide, relie un projet à son dossier de travail, renomme, scinde,
  fusionne ou archive. S'utilise quand l'utilisateur dit « créer le projet X », « lancer un nouveau
  projet », « ouvrir un chantier », « complète le projet X », « archive ce projet », « crée une
  area », « renomme / scinde / fusionne l'area X », « je ne m'occupe plus de X ». Pour faire entrer
  une note ou un document, voir ranger.
---

# Structurer

Un seul skill pour les contenants du vault : les projets de `10-Projects/` et les areas de
`20-Areas/`. Le contenu des notes relève de `ranger` (faire entrer) et de `sync-vault` (mettre à
jour après une session).

## Procédure

### 1. Localiser le vault
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `projet`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé : ses contrats `project` et
`area` fixent les champs à poser.

### 2. Aiguiller

| Demande | Geste | Procédure |
|---|---|---|
| « créer le projet X », « nouveau projet », « ouvrir un chantier » | naître un projet | `references/projet.md` |
| « complète le projet X », « le projet X est vide » | compléter un projet | `references/projet.md`, mode compléter |
| « archive le projet X », « ce projet est terminé » | archiver un projet | `references/archiver.md`, section Projet |
| « crée l'area X », « nouvelle responsabilité » | naître une area | `references/area.md` |
| « complète l'area X », « l'area X est vide » | compléter une area | `references/area.md`, mode compléter |
| « renomme, scinde ou fusionne l'area X » | restructurer une area | `references/restructurer.md` |
| « archive l'area X », « je ne m'en occupe plus » | archiver une area | `references/archiver.md`, section Area |

Projet ou area : un effort avec une fin et un livrable est un projet ; une responsabilité continue
est une area. En cas de doute, poser la question en une phrase.

Avant de créer, chercher l'existant dans `10-Projects/`, `20-Areas/` et `40-Archive/`. Un homonyme
archivé se désarchive plutôt que d'être recréé ; un contenant proche se signale avant de créer.

### 3. Suivre la procédure du geste
Dérouler la référence désignée, puis confirmer : chemins créés ou déplacés, frontmatter posé,
rattachements faits.

## Garde-fous
- **Cadre sans contenu** : à la naissance, une fiche conforme et des sections vides ; le suivi entre
  par l'usage. Rien d'inventé.
- **Non destructif** : enrichir plutôt que dupliquer, ne pas réécrire un champ déjà renseigné, ne
  rien écraser sans validation.
- **Plan puis exécution** pour tout geste multi-fichiers (renommer, scinder, fusionner, archiver) :
  plan exhaustif affiché, validation, commit git du vault proposé, puis exécution.
- **Références structurelles seulement** : un déplacement réécrit ce qui pointe vers le contenant
  (wikilinks, frontmatter `area:`, chemins des zones de personas), jamais les champs sémantiques
  (`domaine:`, `tags:`, titre) ; en cas de doute sur un champ, demander.
- **Personas signalées** : tout changement à un `_personas/{slug}/CLAUDE.md` figure dans le plan,
  jamais en silence.
- Le sensible 🔒 se rattache en renvoi, jamais en copie (`governance.md`).

## Références
- `references/projet.md` : naître ou compléter un projet, relier le dossier de travail, nourrir,
  raccrocher au vault.
- `references/area.md` : naître ou compléter une area, rattacher projets et personas.
- `references/restructurer.md` : renommer, scinder, fusionner une area ; points de contact à
  recenser, mécanique transactionnelle.
- `references/archiver.md` : archiver une area ou un projet ; pré-checks, promotion en Resources,
  retrait des personas.
- `references/liaison-depot.md` : poser `repo:` et `dossier-travail:`, approuver les imports du
  `CLAUDE.md` d'un dépôt.
- `references/nourrir.md` : quoi rattacher à un projet neuf, délégation à `ranger`.
