# Nourrir un projet

Un projet est nourri quand il est raccroché à ce qui existe déjà, dans le vault et dans les sources
de l'utilisateur. On ne lui génère pas de brief.

## Quoi rattacher

| Source du contexte | Comment l'attacher |
|--------------------|--------------------|
| Une note de `00-Inbox/` où l'idée a germé | la classer dans le projet via `import-note`, puis `[[lien]]` depuis la fiche |
| La réunion où le projet a été décidé | connecteur déclaré dans `_Meta/sources.md` (Granola, agenda), sinon collage manuel, puis `import-note` |
| Un fil d'emails, un doc, une URL | `import-note`, qui adapte l'acquisition à l'entrée |
| Une Area parente ou un projet voisin déjà dans le vault | `[[wikilink]]` direct, pas de copie |
| Une trame ou un doc de référence de `30-Resources/` | `[[wikilink]]` direct depuis la fiche projet, un à trois liens |
| L'emplacement permanent du corpus (dossier Drive, workspace Notion, dossier Granola) | renvoi d'emplacement nommant le connecteur (`import-note/references/classement.md`), wikilinké au projet |

## Résolution des sources

Appliquer la règle de résolution de `_Meta/sources.md` (source déclarée, joignabilité, 🔒 en renvoi).
Le vault est toujours joignable : sans aucun connecteur, une note d'inbox existante se rattache
déjà.

Puiser étroit avant de balayer large :
- Si le projet porte déjà un renvoi d'emplacement (`governance.md`), le lire d'abord et chercher via
  le connecteur qu'il cite, plutôt qu'une recherche globale ou un collage.
- Si nourrir fait découvrir un emplacement permanent (« tout le projet vit dans ce dossier Drive »),
  le poser comme renvoi d'emplacement via `import-note`, une fois, pour que les sessions suivantes y
  puisent seules. Emplacement injoignable : règle de résolution habituelle.

## Déléguer à import-note

L'acquisition d'un contenu externe (URL, Notion, fichier, collage) est le métier d'`import-note`.
`nouveau-projet` l'invoque pour chaque pièce de contexte en indiquant le projet cible, et garde la
main sur le shell et les rattachements.

## Ne pas sur-nourrir

Une à trois pièces de contexte réelles suffisent à amorcer. Le reste se remplit au fil du projet,
par `sync-vault` à chaque session.
