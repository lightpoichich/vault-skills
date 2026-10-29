# Mode vault

Procédure de `sync-vault` quand la session tourne dans le vault (`mode: vault`). Le skill agit sur
toutes les fiches que la session a touchées, traite ce que les sessions de projet ont déposé et
tient le sas, les Resources et la mémoire native. Les commits récents du vault, s'il a un dépôt git,
complètent la conversation sans être requis.

## 1. Repérer ce qui a bougé et ce qui dérive
- Les mouvements du travail : décisions, changements de statut, deadlines, todos nés ou faits, faits
  et contacts nouveaux.
- Les sections `## À répercuter` des fiches projet (`Grep` sur `10-Projects/`), déposées par le mode
  projet : chaque ligne vise une autre fiche (client, area, ressource, mémoire). Les traiter, puis
  retirer la section une fois vide.
- Les fiches qui se sont chargées : sections redondantes, informations périmées, todos faits depuis
  longtemps, verbiage.
- Une source externe à réconcilier (un transcript, par exemple) : lire `_Meta/sources.md` et
  appliquer sa règle de résolution. Tenir le registre vrai dans les deux sens, sur joignabilité
  constatée dans la session : `curation.md`, section 4.

## 2. Réconcilier, consolider et écrire
Pour chaque fiche concernée (`Glob` ou `Grep` pour la retrouver, `_Meta/Schema.md` pour son type) :
appliquer la curation de `curation.md`, sections 1 à 3, puis écrire directement : frontmatter mis à
jour, sections réécrites ou fusionnées, élagages.

## 3. Curer le sas `00-Inbox/_drafts/`
Les drafts sont des livrables sortants, pas du savoir. `sync-vault` gère leur sortie du sas
(archiver l'envoyé en trace sur son `lien`, archiver l'abandonné), jamais leur validation ni leur
envoi. États, seuils et gestes : `curation.md`, section 6.

## 4. Veiller sur `30-Resources/`
Tenue de registre autonome : `_index.md` cochés, wikilinks cassés réparés, liens bidirectionnels
maintenus sur les ressources touchées par la session. Le reste (candidats à trame, orphelines,
renvois périmés) se signale au compte rendu sans action. Détail dans `curation.md`, section 5.

## 5. Tenir la mémoire native de Claude Code
Le vault est le fonds ; la mémoire native est le rappel chargé au démarrage de chaque session.
- Vérifier que la mémoire auto est active. Si elle ne l'est pas, le signaler à l'utilisateur en une
  ligne et ne pas éditer `settings.json`.
- Lancer `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-memory.py" check --vault {vault}`. S'il signale
  un dépassement, du sensible, des pointeurs ou des doublons, ou si `curation_due` est vrai, dérouler
  la curation complète de `memoire-claude-code.md` (sauvegarde d'abord). Sinon, seulement ajouter ou
  mettre à jour l'essentiel transversal : priorités, statut des projets actifs en une ligne avec
  pointeur, qui-est-qui.
- Budget, cibles de promotion et règles : `memoire-claude-code.md`.

## 6. Faire tourner les journaux
Si `_Meta/hooks.conf` porte `JOURNAL_ROTATION=1`, lancer sur les fiches écrites pendant ce passage :
`python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-journal.py" rotate --apply {fiche…}`. Le script ne touche
qu'aux fiches au-dessus de leur budget, déplace mot pour mot et vérifie la non-perte avant d'écrire.
Ne jamais déplacer d'entrée à la main. Sans `JOURNAL_ROTATION=1`, ne rien lancer.

## 7. Rendre compte
Fiches mises à jour, consolidées et élaguées, sections « À répercuter » vidées, drafts curés,
signalements Resources, entrées de mémoire, rotation (entrées déplacées et blocages rendus par le
script) : chemins et nature des changements.

La première fois qu'un automatisme agit dans ce vault, l'expliquer en deux ou trois phrases avant le
détail, dans la langue du dirigeant (`installer/references/langue-dirigeant.md`) :
- **Allègement d'une fiche**, quand la fiche n'avait pas encore de sous-dossier `journal/` : la fiche
  dépassait son poids, ses entrées de journal les plus anciennes sont parties mot pour mot dans une
  archive du trimestre, rangée à côté d'elle ; elle garde son état, ses cinq derniers événements et
  un lien vers l'archive ; rien n'est résumé ni perdu.
- **Première curation de la mémoire**, quand aucune sauvegarde n'existait : ce qu'est la mémoire de
  Claude (des notes courtes qu'il relit à chaque session), pourquoi elle est entretenue (au-delà
  d'une certaine longueur, les notes récentes ne se chargent plus), la sauvegarde faite avant, et ce
  qui attend une validation.
Un blocage se dit par sa cause et son remède (« un commentaire placé au milieu du journal empêche de
le découper : je peux le déplacer en tête de fiche »), jamais par le message du script.
