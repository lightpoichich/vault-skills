# Format attendu : `plan-vault.md` + matière première

Ce skill consomme la sortie d'une **interview de cartographie** (PARA). Voici à quoi
ressemblent ses livrables, pour savoir où lire chaque information. Un plan réel peut dévier ;
parser par **sens des sections**, pas par position exacte.

## `00-Inbox/plan-vault.md`

Frontmatter typique :
```yaml
---
type: plan
status: draft
date: {YYYY-MM-DD}
---
```

Sections (titres indicatifs — repérer par le sens) :

| Section | Ce qu'on en tire | Vers quoi |
|---|---|---|
| **Arborescence proposée** | l'arbre de dossiers exact (Areas, sous-zones Resources) | étape 3 — création des dossiers |
| **Projects (avec deadline)** | un projet par ligne : nom — deadline — livrable — parties prenantes | étape 7 — shells de Projects |
| **Areas (responsabilités continues)** | par Area : objets récurrents, fréquence/cadence, outils actuels | étape 6 — shells d'Areas |
| **Resources** | sous-zones + items prévus (avec **emplacement actuel** pour l'existant — champ optionnel, un plan ancien sans emplacement reste valide) + logique (par type / par domaine) | étapes 3 & 8 |
| **Conventions frontmatter suggérées** | les types de fiches et leurs champs (project, area, meeting, adr…) | étape 4 — `_Meta/Schema.md` |
| **Mapping sources existantes → vault** | quelle source alimente quelle zone (Notion, Slack, DataDog, Gmail…) | étape 9 — renvois externes |
| **Compétences à construire (skills) → personas** | par compétence : ce qu'elle lit / écrit (`type`), regroupée par persona | étape 4 — types au Schema + politique d'accès |
| **Gouvernance / isolation** *(pas toujours présente)* | périmètre, données sensibles, accès des personas, 🔒 | étape 4 — `_Meta/governance.md` |
| **Profil de ton** *(pas toujours présente)* | les 4 curseurs : vocabulaire, longueur, décision, registre | étape 5 — section `## Ton` du `CLAUDE.md` racine |
| **Top 5 irritants** | priorités d'usage | rapport — oriente les prochaines compétences à construire |

> Si la section **Gouvernance / isolation** est absente : la synthétiser (étape 4) depuis les
> signaux de sensibilité de la matière première et des compétences listées. Ne jamais sauter la
> gouvernance.

> Si la section **Profil de ton** est absente : poser à l'étape 5 le défaut prudent (métier sans
> jargon, concis, propose-je-valide, sobre + tutoiement) et le marquer « à valider » dans le rapport.

## `00-Inbox/matiere-premiere/` (optionnel)

Fichiers bruts produits par l'interview, **lus pour le contexte uniquement** :

| Fichier | Sert à |
|---|---|
| `contexte.md` | remplir le contexte du `CLAUDE.md` racine (rôle, charge, enjeux) |
| `themes-actuels.md` | recouper les Areas |
| `notes-actuelles.md` | comprendre d'où le contenu migrera (lazy-pull plus tard) |
| `sources-equipe.md` | calibrer la gouvernance + les renvois externes (sources sensibles) |
| `outillage-actuel.md` | connaître skills/MCP/connecteurs déjà en place |
| `chantiers-en-cours.md` | recouper les Projects |

Ne **jamais** recopier ces fichiers en fiches : ce sont des sources de contexte, pas du contenu
validé. Ils restent dans `00-Inbox/` pour un tri ultérieur.
