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

## Déléguer, ne pas dupliquer

L'acquisition d'un contenu externe (URL, Notion, fichier, collage) est **déjà** le métier
d'`import-note`. `nouveau-projet` ne réimplémente pas cette logique : il **invoque `import-note`** pour
chaque pièce de contexte à faire entrer, en lui indiquant le projet cible. `nouveau-projet` garde la
main sur le **shell** et les **rattachements** ; `import-note` gère l'**entrée** des contenus.

## Ne pas sur-nourrir

Rattacher 1–3 pièces de contexte réelles suffit à amorcer. Le reste se remplira au fil du projet
(c'est le rôle de `sync-vault` à chaque session). Mieux vaut un projet sobre et bien raccroché qu'une
fiche gonflée de contenu spéculatif.
