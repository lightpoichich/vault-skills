# Réconcilier et consolider

`sync-vault` fait deux gestes en un : intégrer ce qui a bougé et garder la fiche concise. Une fiche
utile est à jour et dense.

## 1. Ce qu'on intègre

| Mouvement repéré | Fiche cible | Geste |
|------------------|-------------|-------|
| Décision prise | Project ou Area (section Décisions) ; fiche `adr` si le Schema l'a | inscrire la décision et sa raison en une ligne |
| Statut qui change (projet livré, en pause) | fiche Project | mettre `status` à jour et le refléter dans le résumé |
| Deadline qui bouge | fiche Project | remplacer `deadline`, avec la raison si utile |
| Todo fait ou nouveau | fiche porteuse | retirer le fait, ajouter le neuf |
| Fait structurant, contact, périmètre | fiche la plus proche | intégrer à la bonne section |

## 2. Ce qu'on garde

Le vault sert de contexte aux personas et aux sessions futures. On préserve :
- les décisions et leur raison ;
- le statut courant et les engagements vivants (deadlines, todos ouverts) ;
- les faits structurants (chiffres, contraintes, parties prenantes) ;
- les `[[wikilinks]]` qui raccrochent la fiche au reste du vault.

## 3. Ce qu'on élague ou réécrit

- **Redites** : deux sections qui disent la même chose se fusionnent en une, à jour.
- **Périmé** : une information remplacée par une plus récente se remplace, sans empiler.
- **Bruit** : retirer les étapes intermédiaires sans valeur de contexte, les todos faits depuis
  longtemps et le verbiage.
- **Historique** : garder la trace d'une décision (le quoi et le pourquoi), pas le log des
  micro-étapes qui y ont mené.
- **Décision renversée** : quand une nouvelle décision contredit une antérieure, garder une ligne de
  revirement `~~X~~ remplacé par Y le {date} : X abandonné car {raison}`, pour ne pas reproposer X
  plus tard. Une information simplement périmée (deadline, statut, todo faite) se remplace sans
  trace.

Règle du doute : un élément dont l'importance est incertaine se garde. Le curateur n'élague que ce
qui est clairement redondant ou mort.

## 4. Registre des sources

Quand une source externe est réconciliée, `_Meta/sources.md` se lit et sa règle de résolution
s'applique : déclarée et joignable, utiliser ; injoignable, sauter ; non déclarée, sauter ; 🔒,
renvoi. Le vault est toujours joignable.

Le registre se tient vrai dans les deux sens, sur joignabilité constatée dans la session (sonde
`ToolSearch` positive ou usage réussi), jamais sur parole :
- **Démoter ou élaguer** : un `statut` déclaré `actif` mais injoignable repasse `à brancher` ; un
  indice `accès` périmé est retiré. Signaler sans broder.
- **Promouvoir ou ajouter** : une source `à brancher` qui répond passe `actif` ; un connecteur
  joignable absent du registre y entre en ligne `actif`.
- **Ne rien inventer** : ni `usage`, ni schéma de la source ; `accès` seulement si une heuristique
  d'appel étroit a émergé du sondage. Une source `renvoi 🔒` n'est jamais promue.

## 5. Veiller sur `30-Resources/`

`30-Resources/` porte les trames, les docs bruts (PDF, CGV, design system) et les renvois externes.
`sync-vault` y sépare deux gestes.

Ce qu'il fait seul (tenue de registre) :
- `_index.md` des sous-zones : cocher un item dont la ressource existe désormais, réparer un
  wikilink cassé par un renommage.
- Une ressource touchée par la session (trame utilisée dans un projet, doc consulté) : poser ou
  maintenir le wikilink bidirectionnel entre la fiche d'usage et la ressource.

Ce qu'il signale au compte-rendu, sans action :
- **Candidat à trame** : une forme répétée dans au moins deux Projects ou Areas (même structure de
  document, même checklist, même déroulé) : « candidate à `extraire-trame` ». La généralisation est
  un jugement qui revient à l'utilisateur.
- **Ressource orpheline durable** : zéro wikilink entrant et aucun usage repérable : candidate à
  l'archive. Ne pas déplacer une Resource vers `40-Archive/` seul, rien ne distingue une trame
  dormante d'une trame morte.
- **Renvoi externe possiblement périmé** : un renvoi de `references-externes/` dont la source a
  bougé (lien mort évoqué en session, outil abandonné), ou un renvoi d'emplacement dont le
  connecteur ou la coordonnée ne répond plus : à vérifier, le pointeur peut être momentanément
  injoignable.

## 6. Curer le sas `00-Inbox/_drafts/`

Les fiches `type: draft` sont des livrables externes (mail, courrier, proposition, post) qui
attendent la main de l'humain. `sync-vault` gère leur sortie du sas, pour que `_drafts/` ne
s'accumule pas.

| État repéré | Geste |
|-------------|-------|
| `statut: envoyé` | Archiver en trace : sortir la fiche de `_drafts/` vers le dossier de son `lien` (projet ou client), passer `statut: archivé`. Le vault garde « ce qui a été communiqué le {date} ». |
| `statut: en-attente`, `date` de plus de 14 jours environ | Laisser remonter dans le brief (« À valider ») ; ne rien archiver tant que l'humain peut encore agir. |
| `statut: en-attente`, `date` de plus de 30 jours environ | Archiver `abandonné` dans `40-Archive/`. Un draft ne se supprime pas sans trace. |
| `statut: validé`, pas encore envoyé | Ne rien faire ; il attend l'envoi par l'humain, le brief le remonte. |

Garde-fous propres aux drafts :
- Ne pas faire avancer un statut côté humain : ni `en-attente` vers `validé`, ni `validé` vers
  `envoyé`.
- Ne pas archiver un livrable encore `en-attente` ou `validé` : il peut encore partir.
- Un draft sans `lien` exploitable ne peut pas être classé en trace : le signaler au compte-rendu
  plutôt que deviner une destination.
