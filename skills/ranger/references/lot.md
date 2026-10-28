# Mode lot : ranger un ensemble

Pour un dossier, une archive ou un export Claude.ai : inventaire, manifeste validé en une fois,
exécution ligne par ligne et reprenable. Un élément isolé passe par le mode import
(`references/importer.md`).

Le lot ne vise pas à tout copier. Le principe du vault reste l'import à la demande : entre ce qui
nourrit un projet ou une area actifs ; le reste devient un renvoi ou s'ignore. La fenêtre de temps
et le périmètre se fixent avec l'utilisateur dans les règles du lot.

## 1. Inventorier

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-inventory.py" scan "{source}" --vault "{vault}" \
  --label {label} --manifeste "{vault}/00-Inbox/import-{label}.md"
```

- `{label}` : nom court de la source (`notion`, `drive-clients`, `claude`). Il préfixe les clés des
  fichiers ; le garder identique pour relancer un lot, sinon les doublons ne sont plus reconnus.
- Une archive est extraite hors du vault, dans `${XDG_STATE_HOME:-~/.local/state}/second-cerveau/import/`.
  Un dossier est lu en place. Un export Claude.ai est découpé en un fichier par projet, document et
  conversation (`references/claude-ai.md`).
- Le script rend un résumé (éléments par type, déjà dans le vault, doublons, vides, trop lourds,
  sensibles probables), écrit `inventaire.json` dans le dossier du lot et le squelette du manifeste.
  Un manifeste existant n'est jamais réécrit : c'est l'état du lot.
- Sans `CLAUDE_PLUGIN_ROOT`, le script n'est pas joignable. Pour un dossier de moins de 50 éléments,
  inventorier par `Glob` et écrire le manifeste à la main, mêmes colonnes, clés
  `{label}:{chemin relatif}`. Pour une archive ou un export Claude.ai, le signaler et s'arrêter.

## 2. Proposer

Lire `_Meta/Schema.md`, `governance.md`, `sources.md` et la carte des projets et areas. Puis :

1. **Règles du lot** d'abord : périmètre et fenêtre de temps, correspondances générales (« tout
   `Clients/Acme/` vers [[acme]] », « les conversations du projet Claude Refonte vers [[refonte-site]] »).
   Elles évitent de trancher ligne par ligne. Lancé par la phase 3 d'`installer`, le lot arrive avec
   des règles pré-remplies depuis le plan (rapprochement par le nom, à valider) : les relire plutôt
   que les réécrire.
2. **Chaque ligne `à décider`** : ouvrir l'élément (titre, premières lignes, échantillon pour un gros
   fichier) et remplir action et destination.

| Action | Pour | Destination |
|---|---|---|
| `copier` | référentiel ponctuel, document figé | note classée selon `references/classement.md` ; doc brut posé avec sa fiche compagnon |
| `distiller` | conversation, compte rendu, échange, journal de travail | fiche existante `[[slug]]` : faits, décisions, todos, contacts et récit daté |
| `renvoyer` | sensible 🔒, source vivante ailleurs, élément trop lourd | `30-Resources/references-externes/` ou lien dans la fiche concernée |
| `ignorer` | bruit, brouillon sans valeur, doublon, hors périmètre | rien |

- Un projet ou une area qui manque ne se crée pas en douce : l'inscrire dans les règles du lot
  (« créer le projet X »), il sera créé par `structurer` une fois le manifeste validé.
- Le marqueur `🔒?` du script est un indice sur le nom du fichier. Trancher à la lecture, avec
  `governance.md` : un 🔒 confirmé ne se copie ni ne se distille, il se renvoie.
- Une ligne incertaine garde l'action la plus prudente (`renvoyer` plutôt que `copier`) et se cite
  dans la synthèse.

## 3. Faire valider

Synthèse dans la conversation, cinq lignes au plus : nombre d'éléments par action, destinations
principales, contenants à créer, éléments 🔒, lignes incertaines nommées. L'utilisateur valide d'un
bloc ou corrige le fichier ; rien ne s'exécute sans un go explicite. Au go, passer les lignes
décidées en `validé` et proposer un commit git du vault.

## 4. Exécuter

Ordre : contenants à créer (`structurer`, invariants tirés des sources, « à préciser » sinon), puis
`copier` et `renvoyer`, puis `distiller` par date croissante, pour que l'état le plus récent
l'emporte.

- **Copier** : `references/classement.md`. Frontmatter du type cible avec `source: "{clé}"` et
  `created: {date de l'élément}` ; le hook d'écriture garde un `created` fourni et date `updated` du
  jour.
- **Distiller** : intégrer à la fiche cible selon `sync-vault/references/curation.md` (sections 1 à
  3 et 7) : l'état remplace le périmé, une décision garde sa date et sa raison, le récit daté entre
  dans `## Journal` à la date de l'élément. Chaque entrée reçoit une sous-ligne `  - source : {clé}`.
- **Renvoyer** : titre, emplacement d'origine (chemin ou URL de la source, jamais le dossier
  d'extraction, temporaire), une ligne de contexte, 🔒 si sensible, `source: "{clé}"`.
- Après chaque élément, mettre à jour sa ligne : `fait`, ou `erreur : {raison}`. Le manifeste est
  l'état du lot : une session coupée reprend à la première ligne `validé` (« reprends l'import »).
- Tous les vingt éléments environ, donner l'avancement en une ligne.

## 5. Clore

- Fiches allongées par la distillation : `vault-journal.py check`, puis rotation des fiches écrites
  si `JOURNAL_ROTATION=1` (`sync-vault/references/mode-vault.md`).
- Commit git du vault, avec l'identifiant du lot dans le message.
- Section `## Bilan` en tête du manifeste : éléments par action, erreurs, fiches touchées. Dans la
  conversation, la même chose en cinq lignes au plus.
- Proposer de ranger le manifeste en archive et de supprimer le dossier d'extraction, qui garde les
  données brutes hors du vault. Supprimer seulement sur accord.

## Garde-fous du lot
- Pas d'exécution sans manifeste validé ; pas de contenant créé hors des règles du lot.
- Chaque élément écrit porte sa clé `source:` : c'est elle qui empêche le doublon à la relance.
- Un 🔒 ne se copie ni ne se distille.
- Aucun chemin du dossier d'extraction dans une note : il disparaît.
