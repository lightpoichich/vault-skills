# Phase 3 : rapatrier l'historique

Facultative et reportable. Elle suit la structure : les projets et les areas du plan existent, chaque
élément rapatrié a donc une destination. Au dirigeant, parler de « rapatrier » et de « tableau de
reprise », pas de lot ni de manifeste.

Le principe du vault vaut ici aussi : seul ce qui nourrit un projet ou une area du plan entre dans
le vault ; le reste devient un renvoi ou s'ignore.

## 1. Proposer une voie par source

Relire `00-Inbox/matiere-premiere/notes-actuelles.md` et `outillage-actuel.md`, puis proposer une
voie pour chaque source citée :

| Source | Voie |
|---|---|
| projets Claude.ai, archives de l'export disponibles | mode lot sur le dossier de l'export (`ranger/references/claude-ai.md`, section 2) |
| projets Claude.ai, export pas encore disponible | prompt de passation, un projet à la fois (`ranger/references/claude-ai.md`, section 1), ou export lancé maintenant et repris plus tard |
| export Notion, dossier Drive ou OneDrive, notes `.md`, fichiers | mode lot sur le dossier ou l'archive (`ranger/references/lot.md`) |
| source vivante atteinte par un connecteur (Notion en ligne, Drive) | renvoi d'emplacement posé en phase 2 dans `30-Resources/references-externes/`, contenu tiré à la demande ensuite |
| outil sans export lisible (OneNote, Apple Notes) | export manuel vers un dossier de fichiers si le dirigeant y tient, sinon rien |

Proposer aussi la fenêtre de temps (par exemple les douze derniers mois). Le dirigeant choisit les
sources à traiter maintenant ; les autres restent notées pour plus tard.

## 2. Pré-remplir les règles du lot depuis le plan

Pour chaque source retenue, lancer l'inventaire avec le vault, désormais structuré :

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-inventory.py" scan "{source}" --vault "{vault}" \
  --label {label} --manifeste "{vault}/00-Inbox/import-{label}.md"
```

Puis remplir la section « Règles du lot » du tableau de reprise à partir du plan, avant toute
décision ligne par ligne :

- **Rapprochement par le nom** : un projet Claude.ai, ou un dossier, dont le nom correspond à un
  projet ou une area du plan y est rattaché, avec ses documents (« projet Claude {nom} et ses
  documents vers [[{slug}]] »). Chaque règle de ce type porte la mention « rapprochement par le
  nom, à valider ».
- **Conversations** : elles suivent le projet que leur titre, leur résumé et leurs dates désignent ;
  sans projet identifiable, `ignorer` est proposé.
- **Mémoire générale et `/profile.md`** : comparer avec le `contexte.md` écrit à l'entretien.
  Seuls les faits nouveaux sont proposés pour l'encart de contexte du `~/.claude/CLAUDE.md`, sur
  accord.
- **Fenêtre et périmètre** retenus à l'étape 1.

Dérouler ensuite `ranger/references/lot.md`, étapes 2 à 5 : proposer ligne par ligne, faire valider
le tableau, exécuter, clore.

## 3. Reporter ou clore

- La phase s'arrête à tout moment sans rien perdre : le tableau de reprise reste dans `00-Inbox/`
  et « reprends l'import » la poursuit dans une session suivante. Un export pas encore téléchargé
  se signale avec l'échéance de ses liens, 24 heures après leur création.
- Compléter `00-Inbox/compte-rendu-installation.md` d'une section « Historique rapatrié » : sources
  traitées, tableaux de reprise en cours, sources laissées de côté.

## Garde-fous
- La phase se propose une fois et ne bloque pas la fin de l'installation : le dirigeant peut la
  refuser ou la reporter.
- Rien ne s'écrit sans tableau de reprise validé ; un projet ou une area absent du plan ne se crée
  que par une règle du lot validée.
- Un élément 🔒 ne se copie ni ne se distille, il se renvoie.
