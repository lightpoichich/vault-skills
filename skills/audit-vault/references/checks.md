# Les checks : heuristiques, seuils, exemptions

Tout est en lecture seule. Les seuils sont des défauts : les annoncer dans le rapport et les
ajuster si l'utilisateur en demande d'autres.

## Intégrité structurelle

| Check | Heuristique | Sévérité | Lot |
|---|---|---|---|
| Wikilinks cassés | extraire tous les `[[cible]]` (`grep -o`), comparer aux noms de fichiers `.md` du vault ; une cible sans fichier est cassée | critique | C : créer la fiche ou corriger le lien, l'audit ne devine pas |
| Frontmatter absent ou type inconnu | fiche sans `---` d'ouverture, ou `type:` absent ou hors des types du Schema | critique | A si le type est évident d'après l'emplacement et le contenu (une fiche de `20-Areas/x/` qui relate une réunion reçoit `type: meeting`), sinon C. Ne renseigner que `type:`, sans inventer les autres champs |
| Champs requis vides | comparer le frontmatter aux champs du contrat de son type dans le Schema | alerte | C : les valeurs sont du contenu, pas de la mécanique |
| Nommage hors kebab-case | majuscules, espaces, accents dans les noms de fichiers et de dossiers | alerte | A : renommer et réécrire les wikilinks entrants dans la même transaction |
| Fiche à plat | `20-Areas/x.md` ou `10-Projects/x.md` sans dossier ; la convention est dossier plus fiche homonyme | alerte | A : créer le dossier, déplacer |
| Pollution | `.DS_Store` et équivalents, dossiers vides hors squelette PARA de premier niveau | info | A |
| Noms de fichiers en double | deux fiches `.md` homonymes dans le vault (hors `CLAUDE.md`, `SKILL.md`, `_index.md`) ; tout `[[wikilink]]` vers ce nom est ambigu | alerte | C : renommer l'objet secondaire (`{slug}-case-study`, `crm-{slug}`, suffixe du projet) et réécrire ses liens entrants ; l'audit ne choisit pas lequel |
| Note datée à plat dans un projet | fichier `YYYY-MM-DD-*.md` ou `*-YYYY-MM-DD.md` à la racine de `10-Projects/{slug}/` ; la convention est `meetings/` ou `research/`, date en préfixe | info | A : déplacer dans `meetings/` si `type: meeting`, sinon `research/` ; date en préfixe ; réécrire les wikilinks entrants |
| Orphelines | fiche `.md` sans lien entrant (`grep` de son nom dans les autres fiches) | info | C : rattacher ou archiver |

Exemptions orphelines, jamais des findings : `_Meta/*`, `CLAUDE.md` (vault et personas), fiches
principales d'area et de projet (le dossier les porte), briefs, rapports d'audit, `_index.md`.

## Fraîcheur et archivage

| Check | Heuristique | Sévérité | Lot |
|---|---|---|---|
| Projet à archiver | `status: active` avec deadline dépassée, ou aucune modification depuis plus de 30 jours (frontmatter `updated`, sinon date la plus récente trouvée dans la fiche) | alerte | C si le projet semble vivant ailleurs (cité dans un brief récent) : proposer de recaler la deadline. B sinon : archivage vers `40-Archive/` avec `status: done`, après accord |
| Inbox stale | note de `00-Inbox/` (hors briefs et audits du mois) non triée depuis plus de 14 jours | alerte | C : le tri d'une capture est un jugement, proposer `import-note` |
| Briefs anciens | `00-Inbox/briefs/` au-delà des 7 derniers jours | info | A : purge, les briefs sont éphémères par contrat |
| Vieux audits | rapports `audit-vault-*.md` antérieurs au jour courant | info | A : l'audit purge les siens |
| Index à la main désynchronisé | un `MOC-*.md` ou index de liens dont les cibles diffèrent des fiches existantes de son périmètre (listées mais absentes, existantes non listées) | alerte | B si l'index est consommé et régénérable (`sync-vault` ou le script qui le génère) ; sinon C : le remplacer par une vue `.base` |

## Areas et personas

C'est le diagnostic que `gerer-area` attend : l'audit détecte, `gerer-area` exécute.

Construire d'abord la carte des consommateurs. Pour chaque area de `20-Areas/`, chercher qui la
lit : une persona (`grep` du chemin de l'area dans les `_personas/*/CLAUDE.md`) ou un projet actif
(`area: "[[slug]]"` dans `10-Projects/`).

| Check | Heuristique | Sévérité | Lot |
|---|---|---|---|
| Area sans consommateur | ni persona ni projet actif ne la référence | alerte | B, `gerer-area` : rattacher à une persona, ou archiver |
| Area morte | aucune fiche du dossier modifiée depuis plus de 60 jours et aucun projet actif rattaché | alerte | B, `gerer-area` pour archiver |
| Area obèse | nombre de fiches hors de proportion avec les autres areas ; signal relatif, à dire comme tel, sans seuil absolu | info | B, `gerer-area` pour scinder, consultatif |
| Racine d'area chargée | plus de 8 fiches environ à plat à la racine de `20-Areas/{slug}/` : des flux ou de l'historique se sont posés à côté des référentiels | info | B, `gerer-area` : sous-dossiers de flux, historique vers `40-Archive/` |
| Zone de persona invalide | un chemin déclaré dans les zones d'un `_personas/*/CLAUDE.md` qui ne correspond à aucun dossier | critique | C : créer l'area ou retirer la ligne ; la persona est source de vérité de son périmètre |
| Persona sans zone | persona dont plus aucune zone ne résout | critique | C |

Hors audit, territoire de `sync-vault` : candidats à trame, ressources à indexer dans `_index.md`,
renvois externes périmés, fiches verbeuses à consolider.

## Sévérités : la règle de tri

- **critique** : le système ment ou casse (lien qui ne résout pas, fiche illisible par les agents,
  persona pointant dans le vide).
- **alerte** : la dérive installée (stale, archivable, area qui se déforme).
- **info** : le cosmétique et le préventif (pollution, purges, signaux relatifs).
