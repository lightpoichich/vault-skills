# La mémoire native de Claude Code — l'alimenter depuis sync-vault

Le vault est le **fonds** (tout, consultable dans Obsidian). La mémoire native de Claude Code est la
**couche de rappel** : un petit digest chargé automatiquement au démarrage de chaque session, pour que
les personas partent en connaissant l'essentiel sans relire le vault. `sync-vault` tient les deux à
jour.

## Où elle vit

- Dossier : `~/.claude/projects/<projet>/memory/` — **scopé au projet** (la clé est le répertoire de
  travail : si le dirigeant lance Claude depuis son vault, la mémoire est celle du vault, partagée par
  toutes les personas lancées là).
- Contenu : `MEMORY.md` (l'**index**, seul fichier rechargé au démarrage) + des fichiers `.md`
  thématiques (lus à la demande quand c'est pertinent).
- **Ne pas coder le chemin en dur.** Quand la mémoire est active, Claude Code rappelle son chemin en
  tête de session — l'utiliser. Forme canonique : le chemin du répertoire de travail, `/` remplacés
  par des `-`, sous `~/.claude/projects/`.

## L'activer (la « mise à jour »)

- Réglage : `"autoMemoryEnabled": true` dans `settings.json` (activé par défaut ; coupé par la variable
  d'environnement `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`).
- **Si la mémoire est désactivée, on peut écrire dans `memory/` mais rien ne sera rappelé** : poser le
  flag à `true` avant tout. Le vérifier/activer une fois, puis maintenir.
- Optionnel : `autoMemoryDirectory` redéfinit le dossier mémoire (chemin absolu ou `~/`).

## Quoi y mettre (et quoi laisser au vault)

| Va en mémoire Claude Code (rappel) | Reste dans le vault (fonds) |
|---|---|
| Priorités courantes, focus du moment | Le détail des projets, le suivi complet |
| Statut des projets actifs en **une ligne** | Les décisions avec leur contexte long |
| Décisions et préférences **durables et transversales** | Notes, comptes-rendus, ressources |
| Qui-est-qui (parties prenantes clés) | Fiches contacts complètes |

La mémoire est un **digest d'amorçage**, pas une copie du vault. Test : si une persona doit le savoir
dès la première seconde de sa prochaine session, ça va en mémoire ; sinon, ça reste dans le vault.

## Comment l'écrire

- Écrire directement des `.md` dans `memory/` (pas d'outil dédié) et **maintenir une ligne d'index**
  dans `MEMORY.md` : `- [Titre](fichier.md) — accroche`.
- `MEMORY.md` est le **seul** fichier rechargé au démarrage, et son rappel est plafonné (~200 lignes /
  25 Ko) : le garder **court**. Le détail va dans les fichiers thématiques (lus à la demande) ou dans
  le vault.
- Frontmatter : **facultatif** (non requis pour le rappel). Si le projet en utilise déjà un, garder la
  convention locale ; sinon, du markdown clair suffit.

## Discipline (mêmes garde-fous que pour les fiches)

- **Pas append-only** : remplacer le périmé, fusionner les redites, élaguer ce qui n'amorce plus rien.
- **Jamais de 🔒** : la mémoire est rechargée en clair à chaque session — le sensible n'y entre pas
  (renvoi seulement, comme dans le vault).
- **Autonome** : `sync-vault` décide et écrit ; il rend compte après.
