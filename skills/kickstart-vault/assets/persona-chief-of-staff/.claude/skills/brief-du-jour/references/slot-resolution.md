# Résolution des slots

Comment le brief passe du registre `_Meta/sources.md` à des données concrètes, sans présupposer de
connecteur. La lecture des colonnes (`type`, `statut`, `usage`, `accès`) est décrite dans
`_Meta/sources.md` lui-même ; ce fichier ne la répète pas.

## Exemple de registre

Les noms de sources ci-dessous sont des exemples ; seul le registre du vault fait foi.

```
| source          | type  | statut     | usage           | accès          |
|-----------------|-------|------------|-----------------|----------------|
| Projects+Areas  | vault | toujours   | priorités       | read direct    |
| Calendrier      | cloud | actif      | agenda          | scoper au jour |
| Réunions        | cloud | à brancher | meetings veille |                |
| Export tâches   | local | actif      | todos           | {commande}     |
```

- Slots canoniques : `agenda`, `todos`, `meetings veille`, `messages`, `priorités` (vault). Un `usage`
  libre est rattaché au slot le plus proche, ou ajouté en contexte.
- Quand la colonne `accès` est renseignée, l'appliquer à l'appel : `scoper par date` sur une source
  de réunions donne un seul appel borné à la veille, pas un list-all filtré ensuite. Absente : appel
  par défaut.

## Si le registre est absent

Poser ce stub et prévenir le dirigeant :

```
# Sources : connecteurs du dirigeant

| source         | type  | statut   | usage     |
|----------------|-------|----------|-----------|
| Projects+Areas | vault | toujours | priorités |

> Déclarer ici les connecteurs (agenda, todos, réunions, messages) pour enrichir le brief.
> type : cloud (MCP), local (commande), vault. statut : actif, à brancher, renvoi 🔒.
```

Le brief tourne alors sur le vault seul.

## La cascade de résolution

| Cas | Comportement |
|---|---|
| source déclarée et joignable | l'utiliser |
| source déclarée, injoignable | demander un collage manuel, ou sauter le slot |
| source non déclarée | sauter le slot, le proposer en pied de brief |
| `renvoi 🔒` | référence seulement, ni agrégation ni copie |

Un slot manquant n'est pas une erreur : le brief se construit avec ce qui est là et signale le manque
en pied.

## Acquérir chaque type de source

### `vault`
- Lister les Projects (`10-Projects/*/*.md`) et ne garder que `status: active` (frontmatter).
- Repérer les deadlines proches (champ `deadline` ou `échéance`, à venir ou dépassées) ; elles
  alimentent Priorités et Alertes.
- Survoler les Areas (`20-Areas/*/*.md`) pour les fils chauds (mise à jour récente).
- Citer chaque projet ou area en `[[wikilink]]`.

### `cloud`
- Aucun nom de MCP n'est fixé dans le skill : partir du nom de la source tel que déclaré dans le
  registre.
- Chercher l'outil par `ToolSearch` avec le nom de la source et le slot. Exemple à adapter au nom
  déclaré : pour une source « Calendrier » servant `agenda`, une requête comme `calendar events`.
- Si un outil répond, l'appeler sur la fenêtre pertinente (agenda du jour ; réunions et messages
  depuis la veille).
- S'il ne répond pas (non connecté dans la session, droits manquants), ne pas insister : demander un
  collage manuel (« colle ton agenda du jour, les messages clés ») ou sauter le slot, et le noter en
  pied.

### `local`
- La colonne `accès` peut noter la commande. L'exécuter en lecture seule pour récupérer les données
  du slot (par exemple les todos ouverts).
- Si elle échoue (autre machine, droits), collage manuel ou saut.

## Fenêtres de temps par slot

- **agenda** : événements du jour.
- **todos** : tâches ouvertes, échéance au plus tard aujourd'hui en priorité.
- **meetings veille** : réunions depuis le dernier brief (par défaut depuis hier) ; en tirer les
  actions, pas le verbatim.
- **messages** : messages clés non traités depuis la veille dans les canaux suivis.

## Sécurité

- Une source `renvoi 🔒` n'est ni lue pour agrégation ni recopiée. Si une donnée sensible apparaît
  dans un collage, ne pas la verser dans la fiche : la résumer en neutre ou la référencer.
- Respecter `_Meta/governance.md`.
