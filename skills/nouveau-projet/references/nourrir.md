# Nourrir un projet — rattacher le contexte réel

« Configuré et nourri » ne veut pas dire « rempli de contenu généré ». Un projet neuf est nourri quand
il est **raccroché à ce qui existe déjà** — dans le vault et dans les sources du dirigeant — pas quand
on lui invente un faux brief.

## Quoi rattacher

| Source du contexte | Comment l'attacher |
|--------------------|--------------------|
| Une note de `00-Inbox/` où l'idée a germé | la classer dans le projet via `import-note`, puis `[[lien]]` depuis la fiche |
| La réunion où le projet a été décidé | cascade `_Meta/sources.md` (Granola/agenda si `actif`), sinon collage → `import-note` |
| Un fil d'emails, un doc, une URL | `import-note` (acquisition adaptée à l'entrée) |
| Une Area parente / un projet voisin déjà dans le vault | `[[wikilink]]` direct, pas de copie |
| Une trame ou un doc de référence déjà dans `30-Resources/` | `[[wikilink]]` direct depuis la fiche projet (proposer 1-3, pas déverser) |
| L'endroit permanent où vit le corpus du projet (dossier Drive, workspace Notion, dossier Granola) | **renvoi d'emplacement** nommant le connecteur (cf. `import-note/references/classement.md`), wikilinké au projet |

## La cascade (source-agnostique)

On lit `_Meta/sources.md` et on applique la règle du registre :

```
source déclarée + joignable    → l'utiliser
source déclarée + injoignable  → demander un collage manuel
source non déclarée            → sauter, le proposer comme amélioration
🔒                             → renvoi, jamais copie
```

Le **vault est toujours joignable** : même sans aucun connecteur, on peut rattacher une note d'inbox
existante. C'est la valeur plancher.

**Repuiser étroit avant de balayer large.** Si le projet porte déjà un **renvoi d'emplacement** (un
dossier/workspace nommant son connecteur, cf. `governance.md`), le **lire d'abord** : aller chercher au
bon endroit via le connecteur cité de `_Meta/sources.md`, plutôt qu'une recherche globale ou un collage.
Et **dans l'autre sens** : si nourrir fait découvrir un emplacement permanent (« tout le projet vit dans
ce dossier Drive »), le **poser comme renvoi d'emplacement** (délégué à `import-note`) — une fois, pour
que les prochaines sessions y repuisent seules. Cascade habituelle si l'emplacement est injoignable.

## Déléguer, ne pas dupliquer

L'acquisition d'un contenu externe (URL, Notion, fichier, collage) est **déjà** le métier
d'`import-note`. `nouveau-projet` ne réimplémente pas cette logique : il **invoque `import-note`** pour
chaque pièce de contexte à faire entrer, en lui indiquant le projet cible. `nouveau-projet` garde la
main sur le **shell** et les **rattachements** ; `import-note` gère l'**entrée** des contenus.

## Ne pas sur-nourrir

Rattacher 1–3 pièces de contexte réelles suffit à amorcer. Le reste se remplira au fil du projet
(c'est le rôle de `sync-vault` à chaque session). Mieux vaut un projet sobre et bien raccroché qu'une
fiche gonflée de contenu spéculatif.
