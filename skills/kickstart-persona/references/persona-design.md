# Concevoir une persona — guide de référence

À lire si tu hésites sur le périmètre d'une persona, son architecture, ou son lien au vault.
Ce guide explique le **pourquoi** derrière les choix de `kickstart-persona`.

## Qu'est-ce qu'une persona (et ce que ce n'est pas)

Une persona est un **rôle incarné** : une instance de Claude lancée avec un `CLAUDE.md` qui lui
donne une identité (rôle, ton), un périmètre (ce qu'elle lit/écrit) et des garde-fous. On lui
parle comme à un collaborateur spécialisé : « Chief of Staff, prépare-moi la relance du projet X ».

Ce n'est **pas** :
- une fiche de connaissance (ça, c'est du contenu PARA, ça vit dans `10-Projects/` ou `20-Areas/`) ;
- un dépôt de mémoire (une persona ne stocke rien — elle produit et consomme le contenu du vault) ;
- un assistant généraliste (sans périmètre, une persona vaut à peine mieux que Claude nu).

## Où vit une persona — l'archi vault-centric

Dans un vault-centric (le modèle par défaut pour un non-développeur), **tout vit dans le vault**,
y compris les agents. Une seule source de vérité, pas de repos éparpillés.

```
{vault}/
├── 00-Inbox/ 10-Projects/ 20-Areas/ 30-Resources/ 40-Archive/   # le contenu PARA (la mémoire)
├── _Meta/                  # Schema.md (contrat frontmatter), gouvernance
├── _personas/              # les agents = des OUTILS, pas de la mémoire
│   ├── cos/
│   │   ├── CLAUDE.md        # identité + périmètre de cette persona
│   │   └── .claude/skills/  # capacités PROPRES à cette persona
│   └── rh/
├── .claude/skills/         # capacités CROSS-CUTTING (servent toutes les personas)
└── CLAUDE.md               # carte du vault, héritée par toutes les personas
```

**Règle d'or** : tout ce qui a valeur de mémoire vit dans le vault ; les personas (`_personas/`)
agissent sur cette mémoire sans la stocker. C'est pourquoi une persona n'a jamais de fiche dans
`20-Areas/` : elle n'est pas un sujet à documenter, c'est un outil qui documente.

## Les 3 emplacements de skills (et pourquoi ça compte)

Claude Code charge les skills de projet **hiérarchiquement** : depuis le dossier de lancement en
remontant jusqu'à la racine du dépôt. Comme le vault entier est un seul dépôt, ça donne trois
emplacements aux rôles nets :

| Emplacement | Chargé quand | Pour quoi |
|---|---|---|
| `{vault}/.claude/skills/` (racine) | partout dans le vault | skills transverses : `kickstart-persona`, `kickstart-projet`, `import-note` |
| `_personas/{slug}/.claude/skills/` | seulement quand on lance cette persona | capacités propres : `triage-mails` (CoS), `lecture-pv-cse` (RH) |
| `~/.claude/skills/` (hors vault) | toutes les sessions, toute la machine | rien de spécifique au vault — skills inter-contextes |

`kickstart-persona` ne crée que le dossier `_personas/{slug}/.claude/skills/` **vide**. C'est
`skill-creator` qui le remplira, une capacité à la fois. Un skill qui n'a de sens que pour une
persona va **dans** cette persona ; il ne fuite pas dans les autres.

## Identité vs capacités — pourquoi on sépare

Le shell (identité) se pose une fois ; les capacités (skills) s'ajoutent au fil des besoins réels.
On résiste à la tentation de pré-écrire les skills « parce qu'on les imagine utiles » : un skill
écrit sans cas d'usage concret est presque toujours mal calibré. Le bon réflexe : créer la persona
nue, l'utiliser sur de vrais cas, et **quand un geste se répète** (« je refais ce triage chaque
lundi »), en faire un skill via `skill-creator`. La persona reste vivante et collée au réel.

**Le pont concret.** La découverte capture les tâches récurrentes dans un backlog persistant
(`_personas/{slug}/capacites-a-construire.md`). Chacune devient ensuite une **procédure exacte** —
étapes, format de sortie, garde-fous — encodée comme un skill via `skill-creator`, créé **dans
`_personas/{slug}/.claude/skills/`** (le tier persona-spécifique du tableau ci-dessus). Le rôle dans
le `CLAUDE.md` dit *ce que* la persona fait ; les skills disent *comment*. On ne met jamais le
« comment » d'une tâche dans le `CLAUDE.md` : sa place est un skill, rattaché à cette persona.

## Choisir les zones de lecture/écriture

Le périmètre est ce qui rend une persona utile. Deux principes :

- **Lire large, écrire étroit.** Une persona a souvent besoin de voir beaucoup pour bien répondre
  (tous les projets, les areas pertinentes), mais ne devrait écrire qu'à des endroits précis et
  prévisibles (`00-Inbox/_drafts/` pour les brouillons, la fiche du projet concerné pour les
  traces). Plus le périmètre d'écriture est resserré, plus l'utilisateur garde le contrôle.
- **Le périmètre doit suivre le rôle, pas l'inverse.** Un Chief of Staff transverse lit les
  projets et les areas de gouvernance ; un RH lit les fiches du personnel et les PV ; un Métier
  lit les appels d'offres. Ne pas ouvrir « tout le vault » par défaut — un périmètre flou dilue
  l'utilité et augmente le risque d'écriture au mauvais endroit.

Si l'utilisateur hésite (fréquent quand il découvre son propre vault), lire la carte du `CLAUDE.md`
racine et **proposer** un périmètre cohérent avec le rôle, puis laisser valider.

## Chevauchements entre personas

Deux personas peuvent légitimement lire les mêmes zones, et même écrire au même endroit
(`00-Inbox/_drafts/` est un point de dépôt commun naturel). Ce n'est pas une erreur. Le seul cas à
**signaler** : quand deux personas écrivent dans la même fiche de suivi, au risque de se marcher
dessus. On le mentionne, on ne bloque pas — c'est à l'utilisateur de décider si c'est voulu.

## Pourquoi le `CLAUDE.md` de la persona reste minimal

Claude Code remonte l'arborescence et charge le `CLAUDE.md` racine du vault automatiquement : la
carte, les conventions (kebab-case, wikilinks, frontmatter), le renvoi vers le Schema. La persona
**hérite** de tout ça. Y recopier la carte du vault ou les conventions, c'est créer un doublon qui
se périmera dès que le vault évoluera. Le `CLAUDE.md` de la persona ne porte donc que l'irréductible :
son rôle, son ton, son périmètre, ses interdits. Court par conception.
