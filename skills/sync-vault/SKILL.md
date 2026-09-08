---
name: sync-vault
description: >-
  Met à jour et consolide les fiches du vault à partir de la conversation en cours : décisions,
  statuts, todos, faits nouveaux, sections « À répercuter », sas 00-Inbox/_drafts/ et mémoire native
  de Claude Code. Agit sans validation et réécrit plutôt qu'empiler. S'utilise quand l'utilisateur dit
  « sync le vault », « mets à jour le vault », « répercute ce qu'on a décidé », « allège le vault »,
  ou sur rappel du hook Stop en fin de tour. Depuis un dépôt de code, sync-repo s'applique à la place.
---

# Sync vault

## Entrées attendues
- La conversation en cours : décisions, statuts, todos, faits et contacts nouveaux. C'est le signal
  premier ; les commits récents du vault, s'il a un dépôt git, le complètent sans être requis.
- Les sections `## À répercuter` déposées par `sync-repo` dans les fiches projet.
- Le sas `00-Inbox/_drafts/`, le dossier `30-Resources/` et le dossier mémoire de Claude Code.

## Procédure

### 1. Localiser le vault
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé. Si `mode` vaut `repo`, le
geste attendu est `sync-repo` : le dire et s'arrêter.

### 2. Repérer ce qui a bougé et ce qui dérive
- Les mouvements du travail : décisions, changements de statut, deadlines, todos nés ou faits, faits
  et contacts nouveaux.
- Les sections `## À répercuter` des fiches projet (`Grep` sur `10-Projects/`) : chaque ligne vise
  une autre fiche (client, area, ressource, mémoire). Les traiter, puis retirer la section une fois
  vide.
- Les fiches qui se sont chargées : sections redondantes, informations périmées, todos faits depuis
  longtemps, verbiage.
- Une source externe à réconcilier (un transcript, par exemple) : lire `_Meta/sources.md` et
  appliquer sa règle de résolution. Tenir le registre vrai dans les deux sens, sur joignabilité
  constatée dans la session : `references/curation.md`, section 4.

### 3. Réconcilier et consolider
Pour chaque fiche concernée (`Glob` ou `Grep` pour la retrouver, `_Meta/Schema.md` pour son type) :
intégrer les faits nouveaux à la bonne section, remplacer le périmé, fusionner les redites, élaguer
le bruit en préservant décisions, statut courant, engagements vivants et wikilinks. Quoi intégrer,
garder et élaguer : `references/curation.md`, sections 1 à 3.

### 4. Écrire
Appliquer directement : frontmatter mis à jour, sections réécrites ou fusionnées, élagages. Les
hooks du vault posent `updated`.

### 5. Curer le sas `00-Inbox/_drafts/`
Les drafts sont des livrables sortants, pas du savoir. `sync-vault` gère leur sortie du sas
(archiver l'envoyé en trace sur son `lien`, archiver l'abandonné), jamais leur validation ni leur
envoi. États, seuils et gestes : `references/curation.md`, section 6.

### 6. Veiller sur `30-Resources/`
Tenue de registre autonome : `_index.md` cochés, wikilinks cassés réparés, liens bidirectionnels
maintenus sur les ressources touchées par la session. Le reste (candidats à trame, orphelines,
renvois périmés) se signale au compte-rendu sans action. Détail dans `references/curation.md`,
section 5.

### 7. Alimenter la mémoire native de Claude Code
Le vault est le fonds ; la mémoire native est le rappel chargé au démarrage de chaque session.
- Vérifier que la mémoire auto est active. Si elle ne l'est pas, le signaler à l'utilisateur en une
  ligne et ne pas éditer `settings.json`.
- Distiller dans `MEMORY.md` et ses fichiers thématiques l'essentiel transversal qu'une persona doit
  savoir dès le démarrage : priorités courantes, statut des projets actifs en une ligne, décisions
  et préférences durables, qui-est-qui.
- Garder `MEMORY.md` court, même discipline que pour les fiches. Emplacement, plafond et contenu
  attendu : `references/memoire-claude-code.md`.

### 8. Rendre compte
Résumer après coup : fiches mises à jour, consolidées et élaguées, drafts curés, signalements
Resources, entrées de mémoire (chemins et nature des changements). Si rien n'a bougé et qu'aucune
fiche n'a besoin d'être allégée, le dire en une ligne et s'arrêter.

## Garde-fous
- Autonome : décider et écrire sans validation préalable, rendre compte après. Écraser, fusionner et
  réécrire sont autorisés ; empiler ne l'est pas.
- Règle du doute : un élément dont l'importance est incertaine se garde.
- Le sensible 🔒 ne se copie ni dans une fiche ni en mémoire ; renvoi seulement (`governance.md`).
- Respecter le contrat de `_Meta/Schema.md` pour tout frontmatter touché.

## Références
- `references/curation.md` : quoi intégrer, garder et élaguer ; registre des sources ; veille de
  `30-Resources/` ; curation des drafts avec ses seuils.
- `references/memoire-claude-code.md` : où vit la mémoire native, comment vérifier qu'elle est
  active, quoi y distiller, plafond de rappel.
- `import-note/references/classement.md` : frontmatter, liens, renvoi plutôt que copie.
