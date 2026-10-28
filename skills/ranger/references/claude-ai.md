# Rapatrier des projets Claude.ai

Deux entrées, complémentaires. Le prompt de passation donne l'état synthétisé d'un projet, sans
outillage. L'export du compte donne la matière brute de tous les projets, traitée en mode lot.

## 1. Prompt de passation : un projet à la fois

Donner à l'utilisateur ce prompt, à coller dans une nouvelle conversation de chaque projet
Claude.ai :

```
Produis l'état complet de ce projet pour le transférer dans mon second cerveau. Appuie-toi sur les
instructions du projet, ses documents et nos conversations passées dans ce projet. Réponds en
markdown, sans rien inventer : écris « inconnu » quand une information manque.

# {nom du projet}
## Objectif et livrable
## Statut au {date du jour}
## Décisions prises (date, décision, raison)
## Tâches ouvertes (tâche, responsable, échéance)
## Personnes et organisations impliquées (nom, rôle)
## Documents de référence (nom, contenu en une ligne)
## Instructions du projet (texte intégral)
## Chronologie (date, événement)
```

L'utilisateur colle la réponse dans Claude Code (« importe cette passation dans le projet X »).
Traiter le texte comme une distillation vers la fiche cible, selon l'étape 4 de `references/lot.md` :
état et décisions dans les sections de la fiche, chronologie dans `## Journal`, clé
`claude:passation:{slug du projet}` en source. Sans fiche cible, proposer `structurer`. Les
instructions du projet nourrissent la section de contexte de la fiche, ou une proposition de
persona par `assistants` quand elles décrivent un rôle durable.

La qualité dépend de ce que le projet Claude.ai retrouve de ses conversations passées : sans
recherche dans l'historique, la réponse se limite aux instructions, aux documents et à la
conversation en cours.

## 2. Export du compte : tous les projets, en mode lot

Démarche de l'utilisateur, d'après l'aide Claude (support.claude.com, article 9450526) et un export
réel du 2026-10-28 :

1. Sur le web ou dans Claude Desktop, pas sur mobile : Settings, Privacy, « Export data ».
2. Le lien reçu par mail donne un fichier manifeste (`manifest-….json`, version 1.0) qui liste une
   archive par catégorie : `light_metadata`, `projects`, `memories`, `frames`, `conversations`, chacune
   découpée en parties (`projects-000.zip`). Ouvrir chaque lien connecté au compte et télécharger
   l'archive en entier du premier coup : un lien expire 24 heures après sa création et peut cesser de
   fonctionner dès sa première utilisation.
3. Réunir les archives dans un même dossier, manifeste compris.
4. En Team ou Enterprise, l'export doit d'abord être autorisé par un propriétaire de l'organisation.

Puis « importe cet export », en donnant le dossier : mode lot (`references/lot.md`) avec le label
`claude`. Le script reconnaît l'export et le découpe. Contenu constaté le 2026-10-28 : un fichier par
projet (description, instructions, documents de connaissance), une mémoire générale, une mémoire par
projet actif, des fichiers de mémoire rangés par domaine, personne et projet, les conversations avec
leur résumé. Correspondances par défaut :

| Élément | Proposition |
|---|---|
| `projet claude` | projet ou area du vault, existant ou créé par `structurer` ; la mémoire du projet donne son état courant, à distiller en premier ; description et instructions vers la fiche, ou proposition de persona ; le projet d'exemple d'Anthropic s'ignore |
| `document claude` | `copier` dans le dossier du projet ou `30-Resources/` s'il est figé, `renvoyer` s'il vit ailleurs |
| `conversation claude` | `distiller` vers la fiche du projet ; `ignorer` pour un échange sans décision ni fait durable |
| `mémoire claude` | mémoire générale et `profile` : proposer un ajout à l'encart de contexte du `~/.claude/CLAUDE.md`, sur accord ; fichier de domaine (`/areas/…`) : `distiller` vers l'area ; fichier de personne (`/people/…`) : `distiller` vers la fiche de la personne ou de l'organisation |
| `métadonnées claude` | `ignorer` (compte, historique de connexion) |

- L'export ne relie pas une conversation à son projet : proposer l'attribution au manifeste
  d'après le titre, le résumé et les dates, et la faire valider.
- Une pièce jointe n'apporte que son texte extrait ; un fichier sans contenu est signalé dans la
  conversation découpée.
- Format non documenté par Anthropic : le script lit les champs connus et ignore les autres. Un
  élément manquant (instructions, documents) se signale dans la synthèse.
- À l'installation, l'export se demande dès le cadre de l'entretien ; sa mémoire oriente
  l'interview et pré-remplit la matière première, fait par fait confirmée
  (`installer/references/entretien.md`, section « Historique Claude.ai ») ; l'import se fait en
  phase 3 (`installer/references/migration.md`).
