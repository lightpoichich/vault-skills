# Concevoir une persona : guide de référence

À lire en cas d'hésitation sur le périmètre d'une persona, son architecture ou son lien au vault.

## Ce qu'est une persona

Un rôle incarné : une instance de Claude lancée avec un `CLAUDE.md` qui lui donne une identité
(rôle), un périmètre (ce qu'elle lit et écrit) et des garde-fous. On lui parle comme à un
collaborateur spécialisé : « Chief of Staff, prépare-moi la relance du projet X ».

Ce n'est pas :
- une fiche de connaissance (contenu PARA, qui vit dans `10-Projects/` ou `20-Areas/`) ;
- un dépôt de mémoire (une persona ne stocke rien, elle produit et consomme le contenu du vault) ;
- un assistant généraliste : sans périmètre, elle n'apporte rien de plus qu'une session Claude nue.

## Où vit une persona

Dans un vault-centric, tout vit dans le vault, y compris les agents : une seule source de vérité.

```
{vault}/
├── 00-Inbox/ 10-Projects/ 20-Areas/ 30-Resources/ 40-Archive/   # le contenu PARA (la mémoire)
├── _Meta/                  # Schema.md (contrat frontmatter), gouvernance
├── _personas/              # les agents : des outils, pas de la mémoire
│   ├── cos/
│   │   ├── CLAUDE.md        # identité et périmètre de cette persona
│   │   └── .claude/skills/  # capacités propres à cette persona
│   └── rh/
├── .claude/skills/         # capacités transverses (servent toutes les personas)
└── CLAUDE.md               # carte du vault, héritée par toutes les personas
```

Tout ce qui a valeur de mémoire vit dans le vault ; les personas (`_personas/`) agissent sur cette
mémoire sans la stocker. Une persona n'a donc jamais de fiche ni de dossier dans `20-Areas/` : elle
n'est pas un sujet à documenter, c'est un outil qui documente.

Ne pas confondre lieu de stockage et périmètre fonctionnel. La règle ci-dessus porte sur le
stockage. Elle n'interdit pas une persona ancrée sur une Area : un RH dont la lentille principale
est `20-Areas/rh/` (il y lit, il y documente) est le cas typique ; il produit de la mémoire dans
l'Area sans en stocker dans `_personas/rh/`. Ce qui justifie une telle persona, ce sont des routines
récurrentes sur cette Area (triage, synthèses de PV, relances), jamais la simple existence du
dossier : on ne crée pas une persona par Area.

## Les trois emplacements de skills

Claude Code charge les skills de projet hiérarchiquement, du dossier de lancement jusqu'à la racine
du dépôt. Le vault entier étant un seul dépôt, trois emplacements ont chacun un rôle net :

| Emplacement | Chargé quand | Pour quoi |
|---|---|---|
| `{vault}/.claude/skills/` (racine) | partout dans le vault | skills transverses : `kickstart-persona`, `nouveau-projet`, `import-note` |
| `_personas/{slug}/.claude/skills/` | seulement quand on lance cette persona | capacités propres : `triage-mails` (CoS), `lecture-pv-cse` (RH) |
| `~/.claude/skills/` (hors vault) | toutes les sessions, toute la machine | rien de spécifique au vault ; skills inter-contextes |

`kickstart-persona` ne crée que le dossier `_personas/{slug}/.claude/skills/`, vide. C'est
`vault-skill-creator` qui le remplit, une capacité à la fois. Un skill qui n'a de sens que pour une
persona va dans cette persona ; il ne fuit pas dans les autres.

## Identité et capacités

Le shell (identité) se pose une fois ; les capacités (skills) s'ajoutent au fil des besoins réels.
Un skill écrit sans cas d'usage concret est presque toujours mal calibré : créer la persona nue,
l'utiliser sur de vrais cas, et quand un geste se répète (« je refais ce triage chaque lundi »), en
faire un skill via `vault-skill-creator`.

Le pont concret : la découverte capture les tâches récurrentes dans un backlog persistant
(`_personas/{slug}/capacites-a-construire.md`). Chacune devient ensuite une procédure exacte
(étapes, format de sortie, garde-fous) encodée comme un skill dans
`_personas/{slug}/.claude/skills/`. Le rôle du `CLAUDE.md` dit ce que la persona fait ; les skills
disent comment. Le « comment » d'une tâche ne va jamais dans le `CLAUDE.md`.

## Choisir les zones de lecture et d'écriture

- **Lire large, écrire étroit.** Une persona a souvent besoin de voir beaucoup pour bien répondre
  (tous les projets, les Areas pertinentes), mais n'écrit qu'à des endroits précis et prévisibles
  (`00-Inbox/_drafts/` pour les brouillons, la fiche du projet concerné pour les traces). Plus le
  périmètre d'écriture est resserré, plus l'utilisateur garde le contrôle.
- **Le périmètre suit le rôle.** Un Chief of Staff transverse lit les projets et les Areas de
  gouvernance ; un RH lit les fiches du personnel et les PV ; un Métier lit les appels d'offres. Ne
  pas ouvrir tout le vault par défaut : un périmètre flou dilue l'utilité et augmente le risque
  d'écriture au mauvais endroit.

Si l'utilisateur hésite (fréquent quand il découvre son propre vault), lire la carte du `CLAUDE.md`
racine, proposer un périmètre cohérent avec le rôle, puis laisser valider.

## Chevauchements entre personas

Deux personas peuvent lire les mêmes zones et écrire au même endroit (`00-Inbox/_drafts/` est un
point de dépôt commun). Le seul cas à signaler : deux personas qui écrivent dans la même fiche de
suivi, au risque de se marcher dessus. Le mentionner sans bloquer ; l'utilisateur décide.

## Le `CLAUDE.md` de la persona reste minimal

Claude Code remonte l'arborescence et charge automatiquement le `CLAUDE.md` racine du vault : la
carte, les conventions (kebab-case, wikilinks, frontmatter), le renvoi vers le Schema et le ton. La
persona hérite de tout cela. Y recopier la carte ou les conventions crée un doublon qui se périme
dès que le vault évolue. Le `CLAUDE.md` de la persona ne porte que l'irréductible : son rôle, son
périmètre, ses interdits, et un écart de ton seulement s'il est justifié par le rôle.
