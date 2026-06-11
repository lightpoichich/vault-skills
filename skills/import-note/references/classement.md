# Classement — l'étage universel

Une fois le contenu en markdown propre, le ranger est **identique pour tous les dirigeants**. C'est le
vrai travail de l'import : sans classement, on n'a fait que déplacer du texte.

## 1. Renvoi ou copie ?

La première décision, avant de ranger quoi que ce soit :

| Cas | Geste |
|-----|-------|
| Contenu **ponctuel à capitaliser** (article, note figée, doc de référence) | **import** : on fait entrer le contenu transformé en fiche |
| Source de vérité **vivante** ailleurs (doc qui évolue, système externe) | **renvoi** : lien + contexte, le contenu reste sa source |
| **Sensible 🔒** (RH, contrats, finances non publiques) | **renvoi seulement**, jamais de copie |

Un **renvoi** va dans `30-Resources/references-externes/` : un titre, le lien, une ligne de contexte,
tag 🔒 si sensible. C'est la matérialisation de **renvoi-jamais-copie** (`governance.md`).

**Cas particulier — le doc brut** (PDF, CGV, design system, plaquette…) : quand le document
**lui-même** est le référentiel — pas un contenu à transformer en fiche — l'import se fait en deux
pièces : le **fichier posé tel quel** dans `30-Resources/{sous-zone}/` (ou laissé à sa source s'il
y vit et y évolue → renvoi), et une **fiche compagnon** markdown à côté (`type: resource`, résumé
en 2-3 lignes de ce que c'est et quand s'en servir, `source:` → le fichier, `[[wikilinks]]`). Sans
fiche compagnon, un PDF est invisible : rien ne le wikilinke, rien ne le retrouve au bon moment.

Le reste de cette page concerne le cas **import**.

## 2. Choisir la zone PARA

Déduire du contenu, **proposer**, confirmer :

- **Project** (`10-Projects/{slug}/`) — le contenu concerne un effort avec une **fin et un livrable**.
  L'ajouter au dossier du projet (souvent comme source/annexe, ou intégré à la fiche de suivi).
- **Area** (`20-Areas/{slug}/`) — une **responsabilité continue** (un domaine récurrent). L'ajouter au
  dossier de l'area.
- **Resource** (`30-Resources/{sous-zone}/`) — un **référentiel réutilisable**, détaché d'un projet ou
  d'une area précise (méthode, article, modèle). Cas le plus fréquent pour un import « pour plus tard ».

Si l'utilisateur a déjà nommé la cible (« ajoute ça à mon projet X »), la respecter.

## 3. Enrichir avant de créer

- **Chercher** une fiche existante pertinente : `Glob` la zone cible, `Grep` un terme clé du contenu.
- Si une fiche pertinente existe → **proposer d'y ajouter** une section (avec un sous-titre daté et la
  source) plutôt que de créer un doublon.
- Sinon → créer une nouvelle fiche.

## 4. Frontmatter et nommage

- **Lire `_Meta/Schema.md`** pour le type cible. Le plus souvent `resource` :
  ```yaml
  type: resource
  source: {URL / lien Notion / chemin / « collé le {date} »}
  tags: [...]
  ```
  Si l'import s'attache à un Project/Area, suivre le type de la fiche d'accueil.
- **Titre de fichier en kebab-case**, descriptif (`methode-priorisation-rice.md`, pas `note-1.md`).
- Laisser les hooks du vault poser `created`/`updated` — ne pas les écrire à la main.

## 5. Liens

- Relier en **`[[wikilinks]]`** vers les fiches déjà présentes que le contenu mentionne ou prolonge
  (le projet concerné, l'area parente, une ressource voisine).
- **Boucle de retour** : quand l'import naît d'un contexte précis (« pour le projet X », import
  pendant qu'on travaille une Area) et atterrit en `30-Resources/`, le lien est **bidirectionnel** —
  la ressource pointe vers `[[{projet/area}]]`, ET la fiche du projet/area gagne le lien
  `[[{ressource}]]`. Une ressource que rien ne pointe sera invisible au moment où on en aura besoin.
- Un import bien classé **se raccroche** au reste du vault : il n'est pas une île.

## 6. Confirmer

Afficher : la zone choisie, le chemin de la fiche, le type, et un aperçu court (titre + 2-3 lignes).
**Ne rien écraser** sans validation. L'utilisateur garde la main sur le rangement.
