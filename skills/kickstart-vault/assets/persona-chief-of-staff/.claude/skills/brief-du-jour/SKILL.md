---
name: brief-du-jour
description: >-
  Génère le brief du jour du dirigeant : agrège ses sources déclarées (`_Meta/sources.md`) —
  agenda, todos, réunions de la veille, messages, et le vault (Projects/Areas actifs) — en une
  fiche `00-Inbox/briefs/{date}.md` avec les sections Priorités / Alertes / Agenda / Todos
  (+ « À valider » quand des livrables attendent dans `_drafts/`).
  Utilise ce skill dès que l'utilisateur dit « brief », « brief du jour », « mon point du matin »,
  « fais-moi le brief », « quoi de neuf aujourd'hui / ce matin », « qu'est-ce que j'ai aujourd'hui »,
  ou lance sa session du matin et veut savoir où il en est. **Source-agnostique** : il ne présuppose
  aucun connecteur — il lit le registre `_Meta/sources.md` et **dégrade proprement** quand une source
  manque (le vault suffit toujours à produire un brief utile). NE PAS l'utiliser pour importer une
  note externe (`import-note`), ni pour un audit/revue du vault (skills d'hygiène), ni pour rédiger
  un texte (`reformuler`).
---

# Brief du jour

Le **battement quotidien** du second cerveau. Le dirigeant lance sa session du matin, demande son
brief, et obtient une fiche datée qui répond à : *où j'en suis, qu'est-ce qui brûle, qu'est-ce que
j'ai aujourd'hui, qu'est-ce que je dois faire.*

Le skill est **figé sur sa forme** (les 4 sections, l'écriture de la fiche `brief`) mais **agnostique
sur ses sources** : il ne sait pas d'avance si le dirigeant a Google Calendar ou Outlook, Granola ou
rien. Il lit le registre `_Meta/sources.md`, **résout chaque slot** selon ce qui est déclaré et
joignable, et **saute proprement** ce qui manque. C'est ce qui le rend portable d'un dirigeant à
l'autre sans le réécrire.

## Principe à garder en tête

- **Le vault est le socle.** Projects + Areas actifs sont toujours là → le brief a **toujours** une
  valeur plancher, même avec zéro connecteur branché. Une source externe **enrichit**, elle ne
  conditionne jamais l'existence du brief.
- **On ne présuppose aucune source.** Tout vient de `_Meta/sources.md`. Le skill n'a aucun nom de MCP
  en dur : il **tente** la source déclarée et **dégrade** si elle ne répond pas.
- **Discipline vault.** Aucune donnée 🔒 recopiée (renvoi seulement), pas d'envoi automatique, dates
  et relations en `[[wikilinks]]`, lire `_Meta/Schema.md` avant d'écrire.

## Procédure

### 1. Localiser le vault
Détecter la racine en remontant depuis le dossier courant (présence de `CLAUDE.md` + `_Meta/Schema.md`).
Travailler à cette racine.

### 2. Lire le registre de sources
Lire `_Meta/sources.md`.
- **Absent** (vault scaffoldé avant ce skill, ou jamais rempli) → poser un stub minimal avec la seule
  ligne `vault` (depuis le gabarit décrit dans `references/slot-resolution.md`), **prévenir**
  l'utilisateur que le brief tournera sur le vault seul, et lui proposer de déclarer ses connecteurs
  dans ce fichier pour enrichir les prochains briefs.
- **Présent** → en extraire les slots : chaque ligne donne une `source`, un `type`, un `statut`, un
  `usage`. L'`usage` rattache la source à un slot du brief (agenda, todos, meetings, messages…).

### 3. Résoudre chaque slot
Pour chaque slot, appliquer la **cascade de résolution** (détaillée dans
`references/slot-resolution.md`) :
- `vault` → toujours : scanner les Projects `status: active` et les Areas, repérer deadlines proches
  et fils chauds.
- source `cloud` `actif` → **tenter** le connecteur (via `ToolSearch` sur le nom de la source) ;
  s'il répond, l'utiliser ; sinon demander un collage.
- source `local` `actif` → exécuter la commande déclarée ; si elle échoue, demander un collage.
- `à brancher` / injoignable → **demander un collage manuel** ou sauter le slot.
- non déclarée → sauter, et la lister en pied de brief comme amélioration.
- `renvoi 🔒` → **ne jamais agréger ni copier** : référence seulement.

### 4. Assembler le brief
Composer les 4 sections selon `references/format-brief.md` :
- **Priorités** — depuis le vault (deadlines proches, projets qui avancent/bloquent).
- **Alertes** — ce qui demande une réaction aujourd'hui (deadline imminente, action item d'une réunion
  de la veille, message clé en attente).
- **Agenda** — le slot agenda (sinon section omise).
- **Todos** — le slot todos (sinon section omise).
- **À valider** — les livrables qui attendent ta main : scanner `00-Inbox/_drafts/` et lister les
  `statut: en-attente` (+ les `validé` prêts à partir). Source vault, toujours dispo ; section omise si
  `_drafts/` est vide. C'est le point de contact qui ferme la boucle des drafts.

Terminer par un pied **« Sources à brancher »** listant les slots non déclarés ou injoignables, pour
que le dirigeant voie ce qui enrichirait son brief.

### 5. Écrire la fiche
- Lire `_Meta/Schema.md` pour le frontmatter du type `brief`.
- Écrire `00-Inbox/briefs/{date}.md` (date du jour, format ISO). Créer `00-Inbox/briefs/` si absent.
- **Non destructif** : si la fiche du jour existe déjà, proposer de la compléter/regénérer, ne pas
  écraser en silence.
- Relier les projets/areas cités en `[[wikilinks]]`. Aucune donnée 🔒 dans la fiche.

### 6. Restituer
Afficher le brief dans la session (le dirigeant le lit là, pas seulement dans Obsidian) et confirmer
le chemin de la fiche écrite.

## Références
- `references/slot-resolution.md` — la cascade de résolution, le gabarit `sources.md`, et comment
  acquérir chaque `type` de source (vault / cloud / local).
- `references/format-brief.md` — le gabarit de la fiche `brief` et comment chaque section se remplit.
