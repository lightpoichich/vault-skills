# Mode projet

Procédure de `sync-vault` quand la session tourne dans un dossier de travail hors vault, relié à
une fiche projet (`mode: projet`). Le dossier est un dépôt de code ou un dossier sans git (OneDrive,
Documents). Le suivi vit dans la fiche projet du vault, à un seul endroit : ce mode met à jour cette
fiche et laisse au mode vault des consignes pour le reste.

La règle « une seule fiche » est dure. Une session menée dans le dossier d'un client voit un
contexte partiel ; elle ne réécrit pas le reste du vault.

## 1. Lire
La fiche `sheet`, et le contrat `project` de `{vault}/_Meta/Schema.md` (champs et valeurs de ce
vault).

## 2. Repérer ce qui a bougé
- Conversation : décisions et leur raison, avancement, blocages, todos nés ou faits, changement de
  périmètre ou de deadline, faits et contacts nouveaux.
- Dans un dépôt git seulement : `git log --since="{updated de la fiche}" --format='%ad %s'
  --date=short` et `git status --short`. Les commits datent et confirment ; le non commité reste
  « en cours ». Hors git, la conversation est la seule source : ne lancer aucune commande git.

## 3. Écrire la fiche
- `## Suivi` : l'état courant en quelques lignes datées (où on en est, prochain pas, blocage).
  Remplacer, ne pas empiler ; le `## Suivi` décrit l'état courant, pas l'historique des sessions.
- `## Journal` : une entrée datée et complète en tête, pour le récit de la session (ce qui a été
  fait, constaté, échangé). Ajout seul, format de `curation.md`, section 7. Pas de rotation dans ce
  mode : le passage suivant depuis le vault s'en charge.
- `## Décisions` : une ligne par décision nouvelle, avec la raison. Les décisions existantes ne
  bougent pas, sauf revirement explicite.
- Todos : cocher le fait, ajouter le né, retirer le périmé.
- Frontmatter :
  - `status` seulement si l'utilisateur l'a dit (`paused`, `done`) ;
  - `repo:` posé s'il manque et que `repo` est non vide (`URL#sous-dossier` si `subpath` est non
    vide) ;
  - `dossier-travail:` jamais touché, c'est une indication propre à chaque poste.

## 4. Déposer ce qui déborde
Tout ce qui concerne une autre fiche va dans une section `## À répercuter` en fin de fiche projet,
une ligne par item, datée, cible en `[[wikilink]]` : « {date} · [[client]] : nouveau contact X
(rôle) », « {date} · [[tech]] : pattern Y à capitaliser ». Le mode vault la traite et la vide à son
prochain passage.

## 5. Rendre compte
Trois lignes au plus : ce qui a été mis à jour dans la fiche, ce qui a été déposé « À répercuter »,
le `repo:` posé le cas échéant.

## Garde-fous
- Une seule fiche, `sheet`. Fiche client, area, ressource, draft, mémoire de Claude Code : une ligne
  dans « À répercuter », pas d'écriture directe.
- Le commit n'est pas la vérité : la conversation prime, un changement non commité est « en cours »,
  pas « fait ».
