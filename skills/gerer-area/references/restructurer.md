# Restructurer une area — renommer, scinder, fusionner

Gestes multi-fichiers : le squelette du vault bouge. **Toujours** le pattern plan-puis-exécute —
jamais d'exécution directe, même sur la demande la plus simple en apparence.

## Le pattern transactionnel (commun aux trois gestes)

### 1. Recenser les points de contact
Avant tout plan, `Grep` l'ancien slug sur **tout le vault** pour construire la liste exhaustive :

| Point de contact | Quoi chercher | Quoi réécrire |
|---|---|---|
| Dossier + fiche principale | `20-Areas/{old}/{old}.md` | déplacer/renommer (fiche = slug du dossier) |
| Frontmatter de la fiche area | `area: {old}` | nouveau slug |
| Wikilinks partout | `[[{old}]]` (corps, briefs, meetings…) | `[[{new}]]` |
| Projets rattachés | frontmatter `area: "[[{old}]]"` | nouveau wikilink |
| Personas | `20-Areas/{old}/` dans les zones des `_personas/*/CLAUDE.md` | nouveau chemin |
| Notes contenues dans le dossier | wikilinks internes vers `[[{old}]]` | nouveau wikilink |

**Périmètre strict — références structurelles seulement.** Ne touchent PAS au plan : les champs
sémantiques (`domaine:`, `tags:`, `topic:`…) même s'ils contiennent le mot de l'ancien slug, le
wording des titres et du contenu, les mots du langage courant qui ressemblent au slug (« les
finances de la boîte » n'est pas `[[finance]]`). En cas de doute : poser la question dans le
plan, ne pas trancher seul.

### 2. Afficher le plan, attendre la validation
Liste exhaustive : déplacements, fichiers modifiés (avec le type de modification), CLAUDE.md de
personas touchés (mis en évidence), questions ouvertes. **Attendre le « go » du dirigeant.**

### 3. Filet git
Proposer un commit du vault **avant** d'exécuter (le git local existe par design —
`kickstart-vault` l'initialise). Refus → continuer, mais le noter dans le rapport.

### 4. Exécuter, puis rapporter
Dérouler mécaniquement le plan validé, rien d'autre. Un fichier qui résiste (introuvable,
conflit) → **s'arrêter et signaler**, jamais d'exécution partielle silencieuse. Rapport final :
chaque action faite, vérification `Grep` zéro référence résiduelle à l'ancien slug.

## Renommer
Le cas direct du pattern : un seul old → un seul new. Vérifier d'abord que le nouveau slug est
libre (`20-Areas/` et `40-Archive/`).

## Scinder
La répartition est un **jugement**, pas une mécanique — posture consultative (comme
`extraire-trame`) :
1. Lire la fiche et le contenu du dossier ; **proposer** la répartition : quelles notes, quels
   projets rattachés, quels objets récurrents vont dans quelle area fille. Le dirigeant arbitre.
2. Les areas filles naissent par la procédure « naître » du SKILL.md (invariants + question
   « qui la lit ? » pour chacune).
3. Puis pattern transactionnel : moves des notes, réécriture des `area:` des projets selon
   l'arbitrage, zones des personas (l'ancienne zone éclate en deux — demander quelle persona
   suit quelle fille), wikilinks.
4. L'ancienne fiche area : archiver le dossier devenu vide (voir `archiver.md`, cas simple) —
   ses wikilinks entrants sont réécrits vers la fille pertinente pendant le plan.

## Fusionner
Symétrique : deux dossiers convergent vers un (existant ou né pour l'occasion).
- **Collisions de noms de fichiers** entre les deux dossiers → renommage proposé dans le plan,
  jamais d'écrasement.
- Les deux fiches principales → une seule : frontmatters fusionnés champ à champ (réunion des
  `objets:`/`outils:`, cadence la plus fréquente), corps **concaténés sous des sections
  distinctes** — on ne synthétise pas, on ne perd rien ; le dirigeant élaguera (ou `sync-vault`).
- Wikilinks des deux anciens slugs → le slug cible ; zones des personas réunies.
