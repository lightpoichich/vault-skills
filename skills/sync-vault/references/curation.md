# Réconcilier et consolider — ce qu'on intègre, ce qu'on garde, ce qu'on élague

`sync-vault` fait deux choses en un geste : **intégrer** ce qui a bougé, et **garder la fiche concise**.
Une fiche utile est à jour ET dense — pas un journal append-only qui gonfle jusqu'à noyer le signal.

## 1. Ce qu'on intègre (réconciliation)

| Mouvement repéré | Fiche cible | Geste |
|------------------|-------------|-------|
| Décision prise | Project/Area (section Décisions) ; fiche `adr` si le Schema l'a | inscrire la décision + sa raison (1 ligne) |
| Statut qui change (projet livré, en pause) | fiche Project | mettre `status` à jour + le refléter dans le résumé |
| Deadline qui bouge | fiche Project | **remplacer** `deadline` (ne pas empiler) + raison si utile |
| Todo fait / nouveau | fiche porteuse | retirer le fait, ajouter le neuf |
| Fait structurant, contact, périmètre | fiche la plus proche | intégrer à la bonne section |

## 2. Ce qu'on garde (l'essentiel pour le contexte)

Le vault sert de **contexte** aux personas et aux sessions futures. On préserve toujours :
- les **décisions** et leur raison ;
- le **statut courant** et les engagements vivants (deadlines, todos ouverts) ;
- les **faits structurants** (chiffres, contraintes, parties prenantes) ;
- les `[[wikilinks]]` qui raccrochent la fiche au reste du vault.

## 3. Ce qu'on élague / réécrit (anti-surcharge)

`sync-vault` **n'est pas append-only** : il peut écraser et fusionner.
- **Redites** : deux sections qui disent la même chose → fusionner en une, à jour.
- **Périmé** : une info remplacée par une plus récente → **remplacer**, ne pas empiler.
- **Bruit** : étapes intermédiaires sans valeur de contexte, todos faits depuis longtemps, verbiage →
  retirer.
- **Historique** : on garde la trace d'une décision (le *quoi* + le *pourquoi*), pas le log de chaque
  micro-étape qui y a mené.

**Règle du doute** : si on hésite sur l'importance d'un élément → **garder**. Un curateur préserve le
signal ; il n'élague que ce qui est clairement redondant ou mort.

## 4. Curer le sas `00-Inbox/_drafts/` (livrables sortants)

Les fiches `type: draft` ne sont **pas du savoir** : ce sont des **livrables externes** (mail,
courrier, proposition, post) qui attendent la main de l'humain. `sync-vault` ne touche **jamais** à
leur validation — il gère seulement leur **sortie du sas**, pour que `_drafts/` ne s'accumule pas.

| État repéré | Geste |
|-------------|-------|
| `statut: envoyé` | **Archiver en trace** : sortir la fiche de `_drafts/` vers le dossier de son `lien` (projet/client), passer `statut: archivé`. Le vault garde « ce qui a été communiqué le {date} ». |
| `statut: en-attente`, `date` > ~14 j | Le laisser **remonter dans le brief** (« À valider ») — ne rien archiver tant que l'humain peut encore agir. |
| `statut: en-attente`, `date` > ~30 j | **Archiver `abandonné`** dans `40-Archive/`. Jamais supprimé sans trace. |
| `statut: validé` (pas encore envoyé) | Ne rien faire — il attend l'envoi par l'humain ; le brief le remonte. |

**Garde-fous spécifiques aux drafts :**
- Ne **jamais** faire avancer un statut côté humain : pas de `en-attente → validé`, pas de
  `validé → envoyé`. `sync-vault` ne valide ni n'envoie.
- Ne **jamais** archiver un livrable encore `en-attente` ou `validé` (il pourrait partir).
- Un draft sans `lien` exploitable ne peut pas être classé en trace → le signaler dans le compte rendu
  plutôt que de deviner une destination.

## Garde-fous (non négociables)

- **Sensible 🔒** : jamais copié dans une fiche, jamais exposé ; renvoi seulement (`governance.md`).
- **Cascade source** (si réconciliation d'une source externe) : déclarée + joignable → utiliser ;
  injoignable → sauter ; non déclarée → sauter ; 🔒 → renvoi. Le vault est toujours joignable.
- **Autonome** : `sync-vault` décide et écrit sans demander de validation. Il rend compte **après**.
