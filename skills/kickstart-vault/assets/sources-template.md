# Sources — connecteurs du dirigeant

> Registre central des sources de données du vault. Les skills qui agrègent ou importent
> (`brief-du-jour`, `import-note`, et tout skill généré par `vault-skill-creator`) **lisent ce
> fichier** pour savoir d'où tirer leurs informations. Un skill n'invente jamais une source : il
> résout ce qui est déclaré ici, et **dégrade proprement** si une source manque.

## Le contrat

| source | type | statut | usage | accès |
|--------|------|--------|-------|-------|
| Projects + Areas actifs | vault | toujours | priorités, deadlines, contexte | read direct |
{lignes dérivées du *Mapping sources* du plan-vault, une par source nommée — voir ci-dessous}

## Comment lire ce tableau

- **`type`** — d'où vient techniquement la donnée :
  - `vault` : une zone interne au vault. **Toujours joignable.** C'est le socle.
  - `cloud` : un connecteur Claude / serveur MCP distant (Google Calendar, Granola, Gmail, Notion,
    Slack…). Joignable si la connexion est active dans la session.
  - `local` : une commande qui tourne sur la machine (ex. Apple Reminders via `osascript`, un export
    local). Joignable seulement sur cette machine.
- **`statut`** — où en est le branchement :
  - `actif` : connexion **vérifiée** — le connecteur (MCP, API) est branché et joignable, le skill
    l'utilise directement. À ne mettre que si c'est réellement le cas.
  - `à brancher` : la source est nommée mais son connecteur n'est pas (encore) joignable → le skill
    demandera un collage manuel en attendant. **C'est le statut par défaut tant que rien n'atteste le
    branchement** : qu'une source existe ne veut pas dire que son connecteur est en place.
  - `renvoi 🔒` : source sensible. **Jamais copiée** dans le vault, seulement référencée. Voir
    `governance.md`.
- **`usage`** — à quel « slot » d'un skill la source répond (agenda, todos, meetings, messages…).
- **`accès`** *(optionnel)* — l'**heuristique** pour requêter cette source **étroit** plutôt que de tout
  rapatrier : `read direct`, `scoper par date`, `filtrer par projet/personne`, `payload long → toujours
  borner`, `jamais copié 🔒`. C'est un **comment-requêter-bien**, **jamais le schéma** de la source
  (champs, tables) : le schéma est *live* (un MCP est auto-descriptif, on le découvre à l'appel), le
  figer ici le ferait **dériver**. Vide / `—` = pas d'heuristique connue. Une source `actif` sans `accès`
  marche très bien — la colonne se remplit **par l'usage**, quand un skill apprend la bonne requête.

## La règle de résolution (pour les skills qui lisent ce fichier)

```
source déclarée + joignable    → l'utiliser
source déclarée + injoignable  → demander un collage manuel (ou sauter le slot)
source non déclarée            → sauter le slot, le proposer comme amélioration
🔒                             → renvoi jamais copie (référence seulement)
```

<!--
GÉNÉRATION (kickstart-vault) :
- Toujours poser la ligne `vault` (socle). Ne jamais l'inventer : Projects/Areas existent par construction.
- Pour CHAQUE source nommée dans le *Mapping sources* du plan-vault, ajouter une ligne :
  `| {source} | {cloud|local} | {statut} | {usage déduit du plan} | {accès ou vide} |`
  statut = `à brancher` PAR DÉFAUT ; `actif` UNIQUEMENT si le plan atteste que le connecteur est
  déjà branché et joignable (source nommée ≠ connecteur en place). Au moindre doute → `à brancher`.
- `accès` = laisser VIDE (`—`) sauf si le plan donne une heuristique d'accès explicite (« scoper par
  date », « filtrer par projet »…). Ne JAMAIS inventer le schéma de la source ; cette colonne se remplit
  par l'usage (un skill qui sonde la source y consigne ce qu'il apprend). 🔒 → `jamais copié 🔒`.
- Source marquée sensible dans le plan / la gouvernance → statut `renvoi 🔒`.
- Generate-don't-write : n'inscrire AUCUNE source que le dirigeant n'a pas nommée. Pas de catalogue
  d'exemples en dur dans le fichier généré. Si le plan n'a pas de *Mapping sources*, ne poser que la
  ligne `vault` et signaler dans le rapport que le dirigeant complétera ce fichier quand il branchera
  ses connecteurs (ou qu'un skill le complétera à la première exécution).
-->
