# Les checks — heuristiques, seuils, exemptions

Tout est **lecture seule**. Les seuils sont des défauts raisonnables : les annoncer dans le
rapport, les ajuster si l'utilisateur en demande d'autres.

## Famille 1 — Intégrité structurelle

| Check | Heuristique | Sévérité | Lot |
|---|---|---|---|
| Wikilinks cassés | extraire tous les `[[cible]]` (`grep -o`), comparer aux noms de fichiers `.md` du vault ; une cible sans fichier = cassé | 🚨 | C (créer la fiche ? corriger le lien ? l'audit ne devine pas) |
| Frontmatter absent / type inconnu | fiche sans `---` d'ouverture, ou `type:` absent ou hors des types du Schema | 🚨 | A si le type est évident d'après l'emplacement et le contenu existant (fiche dans `20-Areas/x/` qui parle d'une réunion → `type: meeting`) ; sinon C. **Ne renseigner que `type:` — jamais inventer les autres champs** |
| Champs requis vides | comparer le frontmatter aux champs du contrat de son type dans le Schema | ⚠️ | C (les valeurs sont du contenu, pas de la mécanique) |
| Naming hors kebab-case | majuscules, espaces, accents dans les noms de fichiers/dossiers | ⚠️ | A (renommer + réécrire les wikilinks entrants — transactionnel) |
| Fiche à plat | `20-Areas/x.md` ou `10-Projects/x.md` sans dossier (la convention : dossier + fiche homonyme) | ⚠️ | A (créer le dossier, déplacer) |
| Pollution | `.DS_Store` et équivalents, dossiers vides (hors squelette PARA de premier niveau) | 💡 | A |
| Orphelines | fiche `.md` sans **aucun** lien entrant (`grep` de son nom dans les autres fiches) | 💡 | C (rattacher ? archiver ?) |

**Exemptions orphelines** (jamais des findings) : `_Meta/*`, `CLAUDE.md` (vault et personas),
fiches principales d'area/projet (le dossier les porte), briefs, rapports d'audit, `_index.md`.

## Famille 2 — Fraîcheur / archivage

| Check | Heuristique | Sévérité | Lot |
|---|---|---|---|
| Projet à archiver | `status: active` avec deadline dépassée, **ou** aucune modification depuis > 30 j (frontmatter `updated`, sinon date la plus récente trouvée dans la fiche) | ⚠️ | C si le projet semble vivant ailleurs (cité dans un brief récent → proposer de **recaler la deadline**) ; B sinon (archivage — déplacer vers `40-Archive/`, `status: done`, après accord) |
| Inbox stale | note de `00-Inbox/` (hors briefs et audits du mois) non triée depuis > 14 j | ⚠️ | C (le tri d'une capture est un jugement — proposer `import-note`) |
| Briefs anciens | `00-Inbox/briefs/` au-delà des 7 derniers jours | 💡 | A (purge — les briefs sont éphémères par contrat) |
| Vieux audits | rapports `audit-vault-*.md` antérieurs au jour courant | 💡 | A (auto-hygiène : l'audit purge les siens) |

## Famille 3 — Squelette (areas + personas)

C'est le diagnostic que `gerer-area` attend : l'audit **détecte**, `gerer-area` **exécute**.

D'abord construire la **carte des consommateurs** : pour chaque area de `20-Areas/`, qui la
lit ? — une persona (`grep` du chemin de l'area dans les `_personas/*/CLAUDE.md`) ou un projet
actif (`area: "[[slug]]"` dans `10-Projects/`).

| Check | Heuristique | Sévérité | Lot |
|---|---|---|---|
| Area sans consommateur | ni persona ni projet actif ne la référence | ⚠️ | B (→ `gerer-area` : rattacher à une persona, ou archiver) |
| Area morte | aucune fiche du dossier modifiée depuis > 60 j **et** aucun projet actif rattaché | ⚠️ | B (→ `gerer-area` pour archiver) |
| Area obèse | nombre de fiches très au-dessus des autres areas (signal **relatif** — le dire comme tel, pas de seuil absolu) | 💡 | B (→ `gerer-area` pour scinder — consultatif) |
| Zone de persona invalide | un chemin déclaré dans les zones d'un `_personas/*/CLAUDE.md` qui ne correspond à aucun dossier | 🚨 | C (créer l'area ? retirer la ligne ? la persona est source de vérité de son périmètre — décision humaine) |
| Persona sans zone | persona dont plus aucune zone ne résout | 🚨 | C |

**Ne PAS auditer ici** (territoire `sync-vault`) : candidats à trame, ressources à indexer dans
`_index.md`, renvois externes périmés, fiches verbeuses à consolider.

## Sévérités — la règle de tri

- **🚨** : le système ment ou casse (lien qui ne résout pas, fiche illisible par les agents,
  persona pointant dans le vide).
- **⚠️** : la dérive installée (stale, archivable, squelette qui se déforme).
- **💡** : le cosmétique et le préventif (pollution, purges, signaux relatifs).
