# Format attendu : `plan-vault.md` et matière première

Le skill consomme la sortie de l'interview de cartographie (`interview-vault`). Un plan réel peut
dévier du gabarit : repérer chaque section par son sens, pas par sa position.

## `00-Inbox/plan-vault.md`

Frontmatter :
```yaml
---
type: plan
status: draft
date: YYYY-MM-DD
---
```

Sections, avec ce qu'on en tire et l'étape de la procédure qui la consomme :

| Section | Ce qu'on en tire | Étape |
|---|---|---|
| Arborescence proposée | l'arbre de dossiers exact (Areas, sous-zones de Resources) | 3, création des dossiers |
| Projects (avec deadline) | un projet par ligne : nom, deadline, livrable, parties prenantes | 8, fiches de Projects |
| Areas (responsabilités continues) | par Area : objets récurrents, cadence, outils actuels | 7, fiches d'Areas |
| Resources | sous-zones, items prévus avec leur emplacement actuel quand il existe, logique de rangement (par type ou par domaine) | 3 et 9 |
| Conventions frontmatter suggérées | les types de fiches et leurs champs | 4, `_Meta/Schema.md` |
| Mapping sources existantes vers le vault | quelle source alimente quelle zone | 4, `_Meta/sources.md` ; 10, renvois externes |
| Compétences à construire, par persona | par compétence : ce qu'elle lit et écrit (`type`) | 4, types au Schema et politique d'accès |
| Gouvernance / isolation (facultative) | périmètre, données sensibles, accès des personas, 🔒 | 4, `_Meta/governance.md` |
| Profil de ton (facultative) | les quatre curseurs : vocabulaire, longueur, décision, registre | 5, section `## Ton` du `CLAUDE.md` racine |
| Top 5 irritants | priorités d'usage | 13, compte-rendu (prochaines compétences) |

L'emplacement actuel d'un item de Resources est facultatif : un plan ancien sans emplacement reste
valide.

## Défauts quand une section manque

Chaque défaut est marqué « généré par défaut, à valider » dans le compte-rendu.

- **Gouvernance / isolation absente** : synthétiser `governance.md` depuis les signaux de sensibilité
  de la matière première (`sources-equipe.md`) et des compétences listées. La gouvernance n'est pas
  sautée.
- **Profil de ton absent** : poser le défaut prudent. Vocabulaire : métier sans jargon. Longueur :
  concis. Décision : propose, je valide. Registre : sobre, tutoiement, acquiesce.
- **Conventions frontmatter absentes** : garder les types du gabarit `schema-template.md` utiles aux
  Areas et Projects du plan (`area`, `project`, `meeting`, `resource`) et les types d'outillage
  (`moc`, `note`, `brief`, `draft`, `audit`), sans type métier.
- **Mapping sources absent** : `sources.md` ne porte que la ligne `vault` ; pas de renvois externes.

## `00-Inbox/matiere-premiere/` (facultatif)

Fichiers bruts de l'interview, lus pour le contexte seulement :

| Fichier | Sert à |
|---|---|
| `contexte.md` | l'encart de contexte personnel du compte-rendu (rôle, charge, enjeux) |
| `themes-actuels.md` | recouper les Areas |
| `notes-actuelles.md` | comprendre d'où le contenu migrera plus tard |
| `sources-equipe.md` | calibrer la gouvernance et les renvois externes (sources sensibles) |
| `outillage-actuel.md` | connaître skills, MCP et connecteurs déjà en place |
| `chantiers-en-cours.md` | recouper les Projects |

Ces fichiers ne sont pas recopiés en fiches : ce sont des sources de contexte, pas du contenu validé.
Ils restent dans `00-Inbox/` pour un tri ultérieur.
