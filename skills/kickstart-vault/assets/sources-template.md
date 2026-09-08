---
type: moc
topic: sources
updated: {YYYY-MM-DD}
---

# Sources : connecteurs du dirigeant

> Registre central des sources de données du vault. Les skills qui agrègent ou importent
> (`brief-du-jour`, `import-note`, et tout skill généré par `vault-skill-creator`) lisent ce fichier
> pour savoir d'où tirer leurs informations. Un skill n'invente pas de source : il résout ce qui est
> déclaré ici et dégrade proprement si une source manque.

## Le contrat

| source | type | statut | usage | accès |
|--------|------|--------|-------|-------|
| Projects + Areas actifs | vault | toujours | priorités, deadlines, contexte | read direct |
| {une ligne par source déclarée au plan} | {cloud, local} | {à brancher, actif, renvoi 🔒} | {slot servi} | {vide, ou heuristique} |

## Comment lire ce tableau

- **`type`** : d'où vient techniquement la donnée.
  - `vault` : une zone interne au vault, toujours joignable. C'est le socle.
  - `cloud` : un connecteur Claude ou serveur MCP distant (calendrier, réunions, messagerie, base de
    connaissances). Joignable si la connexion est active dans la session.
  - `local` : une commande qui tourne sur la machine (un export local, un outil en ligne de
    commande). Joignable seulement sur cette machine.
- **`statut`** : où en est le branchement.
  - `actif` : connexion vérifiée ; le connecteur est branché et joignable, le skill l'utilise
    directement.
  - `à brancher` : la source est nommée mais son connecteur n'est pas joignable ; le skill demande
    un collage manuel. C'est le statut par défaut tant que rien n'atteste le branchement.
  - `renvoi 🔒` : source sensible, référencée mais pas copiée dans le vault. Voir `governance.md`.
- **`usage`** : le slot d'un skill que la source sert (agenda, todos, meetings, messages).
- **`accès`** (optionnel) : l'heuristique pour requêter la source étroit (`read direct`, `scoper par
  date`, `filtrer par projet ou personne`, `borner le payload`, `jamais copié 🔒`). Elle ne porte pas
  le schéma de la source (champs, tables), qui se découvre à l'appel. Vide au départ, elle se remplit
  par l'usage quand un skill apprend la bonne requête.

## La règle de résolution

| Cas | Comportement du skill |
|---|---|
| source déclarée et joignable | l'utiliser |
| source déclarée, injoignable | demander un collage manuel, ou sauter le slot |
| source non déclarée | sauter le slot, le proposer comme amélioration |
| `renvoi 🔒` | référence seulement, sans copie |
