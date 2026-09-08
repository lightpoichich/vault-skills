---
name: import-note
description: >-
  Fait entrer une note ou un contenu externe dans le vault, une note à la fois : détecte la nature
  de l'entrée (URL, page Notion, fichier local, texte collé), l'acquiert, puis la classe dans la
  zone PARA adéquate avec frontmatter conforme au Schema et wikilinks. Pose un renvoi plutôt qu'une
  copie pour le sensible et le vivant. S'utilise quand l'utilisateur dit « importe cette note »,
  « range cette page Notion / cet article dans le vault », « fais entrer ce doc », « ajoute ça à mon
  projet X », ou colle un texte à ranger. Pour capitaliser une pratique déjà dans le vault, voir
  extraire-trame.
---

# Import note

Deux étages : l'acquisition varie avec la source (URL, Notion, fichier, collage), le classement est
identique pour tous (zone PARA, frontmatter Schema, wikilinks, titre kebab-case).

## Garde-fous

- **Ranger, pas déverser** : un import posé dans `00-Inbox/` sans frontmatter ni lien n'a rien
  importé. Le travail est le classement.
- **Renvoi, jamais copie** pour une source 🔒 ou une source de vérité qui évolue ailleurs
  (`references/classement.md`, section 1, et `governance.md`).
- **Non destructif** : chercher une fiche existante avant de créer, proposer d'enrichir plutôt que
  dupliquer, ne rien écraser sans demander.

## Procédure

### 1. Localiser le vault
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé.

### 2. Détecter la nature de l'entrée
URL web, page Notion, fichier local (`.md`, `.txt`, `.pdf`) ou texte collé. Heuristiques dans
`references/acquisition.md`. En cas d'ambiguïté, demander.

### 3. Acquérir
Acquérir selon `references/acquisition.md` et conserver l'origine (URL, lien, chemin) pour le champ
`source:`. Enlever le bruit sans réécrire le fond.

### 4. Vérifier la sensibilité
Si la source est marquée `renvoi 🔒` dans `_Meta/sources.md`, ou si le contenu est manifestement
sensible (RH, contrats, finances non publiques), ne pas copier. Créer un renvoi dans
`30-Resources/references-externes/` (lien, contexte, tag 🔒) et s'arrêter là.

### 5. Classer
Suivre `references/classement.md` :
- Déterminer la zone PARA cible : Project (effort avec une fin et un livrable), Area
  (responsabilité continue), Resource (référentiel réutilisable). Proposer et confirmer avec
  l'utilisateur ; si la cible est déjà nommée (« ajoute ça à mon projet X »), la respecter.
- Chercher une fiche existante pertinente (`Glob`, `Grep`) avant d'en créer une.
- Poser le frontmatter du type adéquat d'après `_Meta/Schema.md` (souvent `resource`), un titre
  kebab-case, `source:` avec l'origine, et des `[[wikilinks]]` vers les fiches liées. Quand l'import
  est motivé par un projet ou une area, la fiche d'accueil gagne aussi le lien.
- Un doc brut dont le fichier est lui-même le référentiel suit le cas particulier de
  `references/classement.md` : fichier posé avec fiche compagnon.

### 6. Écrire et confirmer
Écrire la fiche ou l'ajout. Confirmer le chemin et la zone, afficher un aperçu court.

## Références
- `references/acquisition.md` : détecter la nature de l'entrée et l'acquérir par type ;
  `obsidian:defuddle` en option avec repli.
- `references/classement.md` : renvoi ou copie, renvoi d'emplacement, doc brut avec fiche
  compagnon, zone PARA, frontmatter, liens bidirectionnels.
