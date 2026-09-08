# Restructurer une area : renommer, scinder, fusionner

## Le pattern transactionnel, commun aux trois gestes

### 1. Recenser les points de contact
Avant tout plan, `Grep` l'ancien slug sur tout le vault pour construire la liste exhaustive :

| Point de contact | Quoi chercher | Quoi réécrire |
|---|---|---|
| Dossier et fiche principale | `20-Areas/{old}/{old}.md` | déplacer ou renommer ; la fiche porte le slug du dossier |
| Frontmatter de la fiche area | `area: {old}` | nouveau slug |
| Wikilinks partout | `[[{old}]]` dans les corps, briefs, meetings | `[[{new}]]` |
| Projets rattachés | frontmatter `area: "[[{old}]]"` | nouveau wikilink |
| Personas | `20-Areas/{old}/` dans les zones des `_personas/*/CLAUDE.md` | nouveau chemin |
| Notes contenues dans le dossier | wikilinks internes vers `[[{old}]]` | nouveau wikilink |

Périmètre strict, références structurelles seulement. Restent hors du plan : les champs
sémantiques (`domaine:`, `tags:`, `topic:`) même s'ils contiennent le mot de l'ancien slug, le
wording des titres et du contenu, les mots du langage courant qui ressemblent au slug (« les
finances de la boîte » n'est pas `[[finance]]`). En cas de doute, poser la question dans le plan
sans trancher seul.

### 2. Afficher le plan, attendre la validation
Liste exhaustive : déplacements, fichiers modifiés avec le type de modification, `CLAUDE.md` de
personas touchés (mis en évidence), questions ouvertes. Attendre le « go » de l'utilisateur.

### 3. Filet git
Proposer un commit du vault avant d'exécuter ; `kickstart-vault` initialise le git local. En cas
de refus, continuer et le noter dans le rapport.

### 4. Exécuter, puis rapporter
Dérouler mécaniquement le plan validé, rien d'autre. Si un fichier résiste (introuvable, conflit),
s'arrêter et signaler ; pas d'exécution partielle silencieuse. Rapport final : chaque action
faite, vérification par `Grep` qu'il ne reste aucune référence à l'ancien slug.

## Renommer
Le cas direct du pattern : un seul ancien slug vers un seul nouveau. Vérifier d'abord que le
nouveau slug est libre dans `20-Areas/` et `40-Archive/`.

## Scinder
La répartition est un jugement, pas une mécanique : le skill propose, l'utilisateur arbitre.
1. Lire la fiche et le contenu du dossier ; proposer la répartition : quelles notes, quels projets
   rattachés, quels objets récurrents vont dans quelle area fille.
2. Les areas filles naissent par la procédure « naître » du SKILL.md (invariants et consommateur
   pour chacune).
3. Puis pattern transactionnel : déplacement des notes, réécriture des `area:` des projets selon
   l'arbitrage, zones des personas (l'ancienne zone éclate en deux, demander quelle persona suit
   quelle fille), wikilinks.
4. L'ancienne fiche area : archiver le dossier devenu vide (`archiver.md`, cas simple) ; ses
   wikilinks entrants sont réécrits vers la fille pertinente pendant le plan.

## Fusionner
Deux dossiers convergent vers un seul, existant ou né pour l'occasion.
- **Collisions de noms de fichiers** entre les deux dossiers : renommage proposé dans le plan, pas
  d'écrasement.
- **Fiches principales** : une seule à l'arrivée. Frontmatters fusionnés champ à champ (réunion des
  `objets:` et `outils:`, cadence la plus fréquente), corps concaténés sous des sections
  distinctes, sans synthèse ni perte ; l'utilisateur ou `sync-vault` élaguera.
- **Wikilinks et zones** : les deux anciens slugs pointent vers le slug cible ; zones des personas
  réunies.
