---
name: import-note
description: >-
  Fait entrer une note ou un contenu externe dans le vault **au bon endroit** (lazy-pull) : détecte
  la nature de l'entrée (URL/article, page Notion, fichier local, texte collé), l'acquiert proprement,
  puis la classe dans la bonne zone PARA (Project / Area / Resource) avec un frontmatter conforme au
  Schema et des `[[wikilinks]]`. Utilise ce skill dès que l'utilisateur dit « importe cette note »,
  « range cette page Notion / cet article / cette URL dans le vault », « fais entrer ce doc », « ajoute
  ça à mon projet / mon area X », « classe ce contenu », colle un texte à ranger, ou pointe un lien /
  un fichier à intégrer. **Transverse** (utile depuis n'importe quelle persona) et **source-agnostique**
  : il s'adapte à l'entrée et n'exige aucun connecteur précis. NE PAS l'utiliser pour le brief du jour
  (`brief-du-jour`), pour scaffolder le vault (`kickstart-vault`), pour créer une persona
  (`kickstart-persona`), ni pour de la capture brute non classée (ça, c'est `00-Inbox/` direct).
---

# Import note

Le **lazy-pull** : tirer un contenu externe **dans** le vault, transformé en fiche utile, **quand ça
vaut le coup** — au lieu de migrer en masse (le big-bang qui pourrit un vault). On importe une chose à
la fois, au moment où on en a besoin, et on la **range** bien.

Le skill sépare nettement deux étages :
- **Acquisition** (variable) — d'où vient le contenu change tout le temps (URL, Notion, fichier,
  collage). Cet étage absorbe la variabilité.
- **Classement** (universel) — une fois le contenu en markdown propre, le ranger est **identique**
  pour tous : zone PARA, frontmatter Schema, wikilinks, titre kebab-case.

## Principe à garder en tête

- **Lazy-pull, pas big-bang.** Une note à la fois, à la demande. On ne « migre » jamais une source
  entière.
- **Ranger, pas déverser.** Un import qui atterrit dans `00-Inbox/` sans frontmatter ni lien n'a rien
  importé. Le travail, c'est le **classement**.
- **Renvoi-jamais-copie pour le sensible et le vivant.** Une source 🔒 ou une source de vérité qui
  continue d'évoluer ailleurs → on pose un **renvoi**, pas une copie (voir `references/classement.md`).
- **Non destructif.** On ne crée pas un doublon d'une fiche existante : on cherche d'abord, on propose
  d'enrichir l'existant avant d'ajouter du neuf.

## Procédure

### 1. Localiser le vault
Détecter la racine (présence de `CLAUDE.md` + `_Meta/Schema.md`) en remontant depuis le dossier
courant.

### 2. Détecter la nature de l'entrée
URL web · page Notion · fichier local (`.md`, `.txt`, `.pdf`…) · texte collé directement. Heuristiques
dans `references/acquisition.md`. En cas d'ambiguïté, demander.

### 3. Acquérir (étage variable)
Selon la nature (détail dans `references/acquisition.md`) :
- **URL / article** → invoquer le skill `obsidian:defuddle` pour extraire un markdown propre (sans le
  bruit de navigation).
- **Page Notion** → si `_Meta/sources.md` déclare Notion `actif`, utiliser le connecteur (tenté via
  `ToolSearch`) ; sinon demander un export / un collage.
- **Fichier local** → lecture directe.
- **Texte collé** → tel quel.
- Conserver l'**origine** (URL, lien, chemin) pour la traçabilité.

### 4. Vérifier la sensibilité
Si la source est marquée `renvoi 🔒` dans `_Meta/sources.md`, ou si le contenu est manifestement
sensible (RH, contrats, finances non publiques) → **ne pas copier** : créer un **renvoi** dans
`30-Resources/references-externes/` (lien + contexte, tag 🔒) et s'arrêter là. Voir `governance.md`.

### 5. Classer (étage universel)
Suivre `references/classement.md` :
- Déterminer la **zone PARA** cible : Project (a une fin/livrable) · Area (responsabilité continue) ·
  Resource (référentiel réutilisable). **Proposer** et confirmer avec l'utilisateur.
- **Chercher une fiche existante** pertinente (`Glob`/`Grep`) avant d'en créer une : enrichir plutôt
  que dupliquer.
- Lire `_Meta/Schema.md`, poser le frontmatter du type adéquat (souvent `resource`), un titre
  **kebab-case**, et des `[[wikilinks]]` vers les fiches liées — **bidirectionnels** quand l'import
  est motivé par un projet/area : la fiche d'accueil gagne aussi le lien. Renseigner `source:` avec
  l'origine.
- **Doc brut** (PDF, CGV, design system…) dont le fichier *est* le référentiel → le poser tel quel
  dans `30-Resources/{sous-zone}/` avec une **fiche compagnon** markdown (voir
  `references/classement.md`) — jamais un fichier orphelin sans fiche.

### 6. Écrire et confirmer
Écrire la fiche (ou l'ajout). **Non destructif** : pas d'écrasement sans demander. Confirmer le chemin
et la zone, afficher un aperçu court.

## Références
- `references/acquisition.md` — détecter la nature de l'entrée et l'acquérir par type.
- `references/classement.md` — choisir la zone PARA, le frontmatter, les liens, et la règle
  renvoi-vs-copie.
