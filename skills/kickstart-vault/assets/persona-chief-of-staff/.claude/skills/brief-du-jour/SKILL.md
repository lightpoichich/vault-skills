---
name: brief-du-jour
description: >-
  Produit le brief du jour dans 00-Inbox/briefs/{date}.md (Priorités, Alertes, Agenda, Todos, À
  valider) à partir du vault et des sources déclarées dans _Meta/sources.md, en dégradant proprement
  si une source manque. S'utilise quand l'utilisateur dit « mon brief », « le point du matin »,
  « qu'est-ce que j'ai aujourd'hui ». Pour faire entrer une note, voir import-note.
---

# Brief du jour

Le brief répond en une fiche datée à quatre questions : où j'en suis, qu'est-ce qui brûle, qu'est-ce
que j'ai aujourd'hui, qu'est-ce que je dois faire. Sa forme est fixe (les sections, la fiche
`brief`) ; ses sources viennent du registre `_Meta/sources.md`, sans nom de connecteur en dur. Le
vault (Projects et Areas actifs) suffit à produire un brief ; une source externe l'enrichit.

## Procédure

### 1. Localiser le vault
Remonter depuis le dossier courant jusqu'au dossier qui contient `_Meta/` ; c'est la racine.
Travailler là.

### 2. Lire le registre de sources
- `_Meta/sources.md` absent : poser le stub de `references/slot-resolution.md` (la seule ligne
  `vault`), prévenir le dirigeant que le brief tourne sur le vault seul et lui proposer d'y déclarer
  ses connecteurs.
- Présent : en extraire les slots. Chaque ligne donne `source`, `type`, `statut`, `usage`, parfois
  `accès` ; l'`usage` rattache la source à un slot du brief (agenda, todos, meetings, messages).

### 3. Résoudre chaque slot
Cascade détaillée dans `references/slot-resolution.md`.
- `vault` : scanner les Projects `status: active` et les Areas ; repérer deadlines proches et fils
  chauds.
- `cloud` `actif` : tenter le connecteur (`ToolSearch` sur le nom de la source) ; s'il répond,
  l'utiliser ; sinon demander un collage.
- `local` `actif` : exécuter la commande déclarée en lecture seule ; si elle échoue, demander un
  collage.
- `à brancher` ou injoignable : demander un collage manuel, ou sauter le slot.
- Non déclarée : sauter, et la lister en pied de brief comme amélioration.
- `renvoi 🔒` : référence seulement, ni agrégation ni copie.

### 4. Assembler le brief
Gabarit et règles de remplissage dans `references/format-brief.md`.
- **Priorités** : depuis le vault (deadlines proches, projets qui avancent ou bloquent).
- **Alertes** : ce qui demande une réaction aujourd'hui (deadline imminente, action d'une réunion de
  la veille, message clé en attente).
- **Agenda** : le slot agenda ; section omise sans source.
- **Todos** : le slot todos ; section omise sans source.
- **À valider** : les livrables en attente dans `00-Inbox/_drafts/` (`statut: en-attente`, plus les
  `validé` prêts à partir), en attente de la validation du dirigeant. Source vault ; section omise si
  le sas est vide.
- Pied « Sources à brancher » : les slots non déclarés ou injoignables.

### 5. Écrire la fiche
- Lire `_Meta/Schema.md` pour le frontmatter du type `brief`.
- Écrire `00-Inbox/briefs/{YYYY-MM-DD}.md` ; créer le dossier s'il manque.
- Si la fiche du jour existe, proposer de la compléter ou de la regénérer ; ne pas écraser en
  silence.
- Relier projets et areas cités en `[[wikilinks]]`. Pas de donnée 🔒 dans la fiche.

### 6. Restituer
Afficher le brief dans la session et confirmer le chemin de la fiche écrite.

## Garde-fous
- Un slot manquant n'est pas une erreur : le brief se construit avec ce qui est là et signale le
  reste en pied.
- Pas de donnée 🔒 recopiée, pas d'envoi automatique ; le brief liste les livrables, il ne les valide
  ni ne les envoie.
- Rédiger un texte pour un tiers est hors périmètre : cela passe par le sas `00-Inbox/_drafts/`.

## Références
- `references/slot-resolution.md` : la cascade de résolution, le stub `sources.md`, l'acquisition par
  type de source, les fenêtres de temps par slot.
- `references/format-brief.md` : le gabarit de la fiche `brief` et les règles de remplissage.
