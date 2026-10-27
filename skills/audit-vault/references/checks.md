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

## Mémoire native de Claude Code

Sources : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-memory.py" inventory --vault {vault}` (tous les
dossiers mémoire de la machine) et `vault-memory.py check --vault {vault} {dossier}` pour chacun. Lecture
seule. Le rapport cite des noms de fichiers, des numéros de ligne, des compteurs et les pointeurs tels
que le script les rend (masqués quand ils sont reconnus comme sensibles), jamais un extrait de mémoire :
il est écrit dans le vault et peut contenir ce que la mémoire ne devait pas. Un pointeur marqué `code`
(cité entre accents graves) et cassé ou archivé est probablement un exemple : le signaler en info ; marqué `code` et déplacé, c'est un vrai pointeur à corriger.

| Check | Heuristique | Sévérité | Lot |
|---|---|---|---|
| Index tronqué au chargement | `truncated` : plus de 200 lignes ou 25 000 caractères, quel que soit le budget réglé | critique | B : `sync-vault` depuis le vault pour le dossier du vault ; C pour un dossier de dépôt |
| Index au-dessus du budget | `over_budget` (`MEMORY_MAX_LINES`, `MEMORY_MAX_KB`), `alert` au-delà de 150 lignes ou 20 000 caractères | alerte | idem |
| Sensible apparent | `sensitive[]` : secret, IBAN, téléphone, fiche confidentielle citée | critique | C : retrait après `vault-memory.py backup`, fichier par fichier, validé |
| Pointeur déplacé | `pointers[]` de type `déplacé` : un seul fichier vivant de ce nom | info | A : corriger le chemin dans la mémoire, après sauvegarde |
| Pointeur ambigu | `pointers[]` de type `ambigu` : plusieurs fichiers du même nom | info | C : l'humain désigne la bonne fiche |
| Pointeur archivé ou cassé | `pointers[]` de type `archivé` ou `cassé` | alerte | C : retirer ou réécrire la mémoire |
| Index désynchronisé | `index.missing_files` ou `index.unindexed` | info | A : retirer l'entrée orpheline, indexer le fichier |
| Règle répétée | `duplicates[]` dans un dossier, `cross_repeats[]` d'un dossier à l'autre | alerte | C : promotion vers sa cible (`sync-vault/references/memoire-claude-code.md`, « Skill d'abord ») |
| Curation en retard | `curation_due` sur le dossier du vault | info | B : `sync-vault` depuis le vault |
| Mémoire déplacée ou partagée | `inventory` montre un dossier `autoMemoryDirectory` | info | constat seul : dire où vit la mémoire et si elle est versionnée |

Un dossier de dépôt (`goodloop`, par exemple) qui dépasse son budget par du savoir technique légitime
reste en lot C : sa place durable est `.claude/rules/` dans le dépôt, hors de ce plugin.

## Taille des fiches

Source : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-journal.py" check` (JSON, lecture seule). Budgets
et sections de journal lus dans `_Meta/hooks.conf` (`JOURNAL_MAX_KB_{TYPE}`, `JOURNAL_SECTIONS`).

| Check | Heuristique | Sévérité | Lot |
|---|---|---|---|
| Fiche au-dessus du budget, rotable | `over[]` avec `entries` > 0 ; les `warnings` (entrées épinglées sans date en tête, liens relatifs) se recopient au rapport | alerte | A : `vault-journal.py rotate` en simulation dans le rapport, puis `rotate --apply --force` sur les fiches validées. Le script déplace mot pour mot et vérifie la non-perte |
| Fiche au-dessus du budget, bloquée | `over[]` avec `blocked` : pas de section de journal, bloc de code non fermé ou qui déborde de son entrée, section qui mêle puces et `###`, paragraphe intercalé, ou fiche qui reste au-dessus du budget après rotation (sections protégées ou entrées sans date trop lourdes). Une fiche peut relever des deux lignes : rotation d'abord, restructuration ensuite | alerte | C : restructuration assistée, ci-dessous |
| Skill de vault qui écrit un récit daté hors journal | `SKILL.md` d'un skill du vault (racine ou `_personas/*/.claude/skills/`) qui ajoute des entrées datées dans une section d'état (`## Suivi`, `## Réunions`, `## Discussions`) | info | C : aligner le skill sur la règle `## Journal` du Schema |

Restructuration assistée d'une fiche bloquée, une fiche à la fois, après validation de son plan :
1. Copier la fiche hors du vault (`/tmp/{slug}.avant.md`).
2. Proposer la restructuration : le récit daté passe dans `## Journal` (par exemple un `## Suivi`
   devenu journal est renommé, et un `## Suivi` court réécrit l'état courant), chaque entrée reçoit
   sa date complète en tête (`AAAA-MM-JJ`, année comprise : une date `JJ/MM` reprise du titre se
   complète d'après le contexte, et se demande à l'humain en cas de doute), les sections mixtes
   sont séparées. Aucun texte n'est résumé ni retiré.
3. Après écriture, contrôler :
   `vault-journal.py verify --loose --before /tmp/{slug}.avant.md --after {fiche}`. Une ligne
   manquante annule la restructuration : restaurer la copie et signaler.
4. Lancer ensuite la rotation en simulation, puis en écriture sur validation.

Hors audit, territoire de `sync-vault` : candidats à trame, ressources à indexer dans `_index.md`,
renvois externes périmés, fiches verbeuses à consolider.

## Sévérités : la règle de tri

- **critique** : le système ment ou casse (lien qui ne résout pas, fiche illisible par les agents,
  persona pointant dans le vide).
- **alerte** : la dérive installée (stale, archivable, area qui se déforme).
- **info** : le cosmétique et le préventif (pollution, purges, signaux relatifs).
