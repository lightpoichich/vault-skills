# Résolution des slots

Comment le brief passe d'un **registre de sources déclaré** à des **données concrètes**, sans jamais
présupposer un connecteur. C'est le mécanisme qui rend le skill portable d'un dirigeant à l'autre.

## Le registre `_Meta/sources.md`

Le skill lit ce tableau. Exemple d'un vault bien branché :

```
| source          | type  | statut     | usage           |
|-----------------|-------|------------|-----------------|
| Projects+Areas  | vault | toujours   | priorités       |
| Google Calendar | cloud | actif      | agenda          |
| Apple Reminders | local | actif      | todos           |
| Granola         | cloud | à brancher | meetings veille |
| Slack           | cloud | actif      | messages clés   |
```

- **`type`** — `vault` (zone interne, toujours joignable) · `cloud` (MCP / connecteur Claude distant)
  · `local` (commande sur la machine).
- **`statut`** — `actif` · `à brancher` · `renvoi 🔒`.
- **`usage`** — rattache la source à un **slot** du brief. Les slots canoniques : `agenda`, `todos`,
  `meetings veille`, `messages`, `priorités` (vault). Un `usage` libre est rattaché au slot le plus
  proche, ou ajouté en contexte.
- **`accès`** *(colonne optionnelle — peut être absente)* — l'heuristique pour requêter la source
  **étroit**. Quand elle est là, **l'appliquer à l'appel** : un `accès: scoper par date` sur Granola =
  **un seul appel borné à la veille** au lieu d'un list-all puis filtre. Absente → appel par défaut.

### Si le registre est absent

Poser ce stub minimal et prévenir l'utilisateur :

```
# Sources — connecteurs du dirigeant

| source         | type  | statut   | usage     |
|----------------|-------|----------|-----------|
| Projects+Areas | vault | toujours | priorités |

> Déclare ici tes connecteurs (agenda, todos, réunions, messages) pour enrichir le brief.
> type : cloud (MCP) · local (commande) · vault.  statut : actif · à brancher · renvoi 🔒.
```

Le brief tourne alors sur le vault seul — utile mais minimal.

## La cascade de résolution

Pour **chaque slot** dont le brief a besoin :

```
source déclarée + joignable    → l'utiliser
source déclarée + injoignable  → demander un collage manuel, ou sauter le slot
source non déclarée            → sauter le slot, le proposer en pied de brief
🔒 (renvoi)                    → ne jamais agréger ni copier ; référence seulement
```

Règle d'or : **un slot manquant n'est jamais une erreur.** Le brief se construit avec ce qui est là,
et signale en pied ce qui manque. Il ne bloque jamais, ne se plaint jamais, ne hardcode jamais.

## Acquérir chaque type de source

### `vault` — le socle (toujours)
- `Glob` les Projects (`10-Projects/*/*.md`) ; ne garder que `status: active` (lire le frontmatter).
- Repérer les **deadlines proches** (champ `deadline`/`échéance` dans le frontmatter, à venir ou
  dépassées) → alimentent **Priorités** et **Alertes**.
- Survoler les Areas (`20-Areas/*/*.md`) pour les fils chauds (dernière mise à jour récente).
- Citer chaque projet/area en `[[wikilink]]`.

### `cloud` — connecteur / MCP (tenter, ne pas présupposer)
- Le skill **ne connaît pas** les noms de MCP en dur. Il part du **nom de la source** déclaré dans le
  registre (« Granola », « Google Calendar », « Slack »…).
- **Tenter** de trouver l'outil correspondant via `ToolSearch` (ex. requête `granola meetings`,
  `google calendar events`, `slack messages`). Si un outil MCP est disponible, l'appeler pour la
  fenêtre pertinente (agenda du jour ; réunions/messages depuis la veille).
- **S'il ne répond pas** (pas connecté dans cette session, droits manquants, budget) → ne pas
  insister : demander un **collage manuel** (« colle ton agenda du jour / les messages clés ») ou
  sauter le slot. Le noter en pied.

### `local` — commande sur la machine (tenter, dégrader)
- Le registre peut noter la commande (ex. Apple Reminders via `osascript`). L'exécuter en lecture
  seule pour récupérer les todos ouverts.
- Si la commande échoue (autre machine, droits) → collage manuel ou saut.

## Fenêtres de temps par slot

- **agenda** → événements du **jour**.
- **todos** → tâches **ouvertes** (échéance ≤ aujourd'hui en priorité).
- **meetings veille** → réunions **depuis le dernier brief** (par défaut : depuis hier) → on en tire
  les **action items**, pas le verbatim.
- **messages** → messages clés **non traités depuis la veille** dans les canaux suivis.

## Sécurité

- Toute source `renvoi 🔒` : **jamais** lue pour agrégation, **jamais** recopiée. Si une donnée
  sensible apparaît incidemment dans un collage, ne pas la verser dans la fiche — la résumer en
  neutre ou la référencer.
- Respect strict de `_Meta/governance.md`.
