# Classement : l'étage universel

Une fois le contenu en markdown propre, le ranger suit la même procédure quelle que soit la source.

## 1. Renvoi ou copie

La première décision, avant de ranger :

| Cas | Geste |
|-----|-------|
| Contenu ponctuel à capitaliser (article, note figée, doc de référence) | import : le contenu entre, transformé en fiche |
| Source de vérité vivante ailleurs (doc qui évolue, système externe) | renvoi : lien et contexte, le contenu reste à sa source |
| Sensible 🔒 (RH, contrats, finances non publiques) | renvoi seulement, jamais de copie |

Un renvoi va dans `30-Resources/references-externes/` : un titre, le lien, une ligne de contexte,
tag 🔒 si sensible. C'est la règle renvoi-jamais-copie de `governance.md`.

Deux cas particuliers :

- **Renvoi d'emplacement** : l'endroit permanent où vit le corpus d'un projet ou d'une area (dossier
  Drive du projet, workspace Notion, dossier Granola du client).
  - Le renvoi nomme le connecteur qui l'atteint, repris d'une ligne de `_Meta/sources.md` :
    « Dossier Drive {projet}, Livrables, via Google Drive ».
  - Il est wikilinké au projet ou à l'area (boucle de retour, section 5), pour que les skills y
    repuisent plus tard sans recoller le lien.
  - Il reste un pointeur, jamais une copie du contenu ; un emplacement 🔒 donne un renvoi sensible,
    jamais rapatrié.
- **Doc brut** : le document lui-même est le référentiel (PDF, CGV, design system, plaquette).
  L'import se fait en deux pièces.
  - Le fichier est posé tel quel dans `30-Resources/{sous-zone}/`, ou laissé à sa source s'il y vit
    et y évolue (renvoi).
  - Une fiche compagnon markdown vit à côté : `type: resource`, résumé en deux ou trois lignes (ce
    que c'est, quand s'en servir), `source:` vers le fichier, `[[wikilinks]]`. Sans fiche compagnon,
    rien ne wikilinke le fichier et rien ne le retrouve.

Le reste de cette page concerne le cas import.

## 2. Choisir la zone PARA

Déduire du contenu, proposer, confirmer :

- **Project** (`10-Projects/{slug}/`) : le contenu concerne un effort avec une fin et un livrable.
  L'ajouter au dossier du projet, comme source ou annexe, ou intégré à la fiche de suivi.
- **Area** (`20-Areas/{slug}/`) : une responsabilité continue. L'ajouter au dossier de l'area.
- **Resource** (`30-Resources/{sous-zone}/`) : un référentiel réutilisable, détaché d'un projet ou
  d'une area précise (méthode, article, modèle). Cas le plus fréquent pour un import « pour plus
  tard ».

Si l'utilisateur a déjà nommé la cible (« ajoute ça à mon projet X »), la respecter.

## 3. Enrichir avant de créer

- Chercher une fiche existante pertinente : `Glob` la zone cible, `Grep` un terme clé du contenu.
- Si une fiche pertinente existe, proposer d'y ajouter une section avec un sous-titre daté et la
  source, plutôt que créer un doublon.
- Sinon, créer une nouvelle fiche.

## 4. Frontmatter et nommage

- Lire `_Meta/Schema.md` pour le type cible. Le plus souvent `resource` :
  ```yaml
  type: resource
  source: {URL, lien Notion, chemin ou « collé le {date} »}
  tags: [...]
  ```
  Si l'import s'attache à un Project ou une Area, suivre le type de la fiche d'accueil.
- Titre de fichier en kebab-case, descriptif (`methode-priorisation-rice.md`, pas `note-1.md`).
- Laisser les hooks du vault poser `created` et `updated`.

## 5. Liens

- Relier en `[[wikilinks]]` vers les fiches déjà présentes que le contenu mentionne ou prolonge : le
  projet concerné, l'area parente, une ressource voisine.
- **Boucle de retour** : quand l'import naît d'un contexte précis (« pour le projet X », import
  pendant le travail sur une area) et atterrit en `30-Resources/`, le lien est bidirectionnel. La
  ressource pointe vers `[[{projet/area}]]` et la fiche du projet ou de l'area gagne le lien
  `[[{ressource}]]`. Une ressource que rien ne pointe est invisible au moment où on en a besoin.

## 6. Confirmer

Afficher la zone choisie, le chemin de la fiche, le type et un aperçu court (titre et deux ou trois
lignes). Ne rien écraser sans validation ; l'utilisateur garde la main sur le rangement.
