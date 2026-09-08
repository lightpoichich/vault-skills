# La mémoire native de Claude Code

Le vault est le fonds, consultable dans Obsidian. La mémoire native de Claude Code est la couche de
rappel : un digest court chargé au démarrage de chaque session, pour que les personas partent en
connaissant l'essentiel sans relire le vault. `sync-vault` tient les deux à jour.

## Où elle vit

Les points suivants dépendent de Claude Code et sont à vérifier sur la version installée.
- Dossier : `~/.claude/projects/{projet}/memory/`, scopé au répertoire de travail de lancement.
  Lancée depuis le vault, la mémoire est celle du vault, partagée par toutes les personas qui y
  sont lancées.
- Contenu : `MEMORY.md`, l'index et seul fichier rechargé au démarrage, plus des fichiers `.md`
  thématiques lus à la demande.
- Chemin : ne pas le coder en dur. Quand la mémoire est active, Claude Code rappelle son chemin en
  tête de session ; l'utiliser. Forme attendue : le chemin du répertoire de travail, `/` remplacés
  par `-`, sous `~/.claude/projects/`.

## Vérifier qu'elle est active

- Signe d'activation : le chemin du dossier mémoire est rappelé en tête de session, ou le contenu de
  `MEMORY.md` apparaît dans le contexte de démarrage.
- Réglage : `autoMemoryEnabled` dans `settings.json`, coupé par la variable d'environnement
  `CLAUDE_CODE_DISABLE_AUTO_MEMORY` ; un réglage `autoMemoryDirectory` peut déplacer le dossier.
  Noms et valeurs à vérifier sur la version installée.
- Si la mémoire est inactive, écrire dans `memory/` ne produit aucun rappel. Le signaler à
  l'utilisateur en une ligne et ne pas éditer `settings.json` : ce geste lui revient.

## Quoi y mettre

| Va en mémoire (rappel) | Reste dans le vault (fonds) |
|---|---|
| Priorités courantes, focus du moment | Le détail des projets, le suivi complet |
| Statut des projets actifs en une ligne | Les décisions avec leur contexte long |
| Décisions et préférences durables et transversales | Notes, comptes-rendus, ressources |
| Qui-est-qui (parties prenantes clés) | Fiches contacts complètes |

Test : si une persona doit le savoir dès la première seconde de sa prochaine session, ça va en
mémoire ; sinon, ça reste dans le vault.

## Comment l'écrire

- Écrire directement des `.md` dans `memory/`, sans outil dédié, et maintenir une ligne d'index par
  fichier dans `MEMORY.md` : `- [Titre](fichier.md)` suivi d'une accroche.
- Le rappel de `MEMORY.md` est plafonné (ordre de grandeur : 200 lignes ou 25 Ko, à vérifier sur la
  version installée) : le garder court. Le détail va dans les fichiers thématiques ou dans le vault.
- Frontmatter facultatif. Si le dossier en utilise déjà un, garder la convention locale ; sinon du
  markdown clair suffit.

## Discipline

- Même discipline que pour les fiches : remplacer le périmé, fusionner les redites, élaguer ce qui
  n'amorce plus rien.
- La mémoire est rechargée en clair à chaque session : le sensible 🔒 n'y entre pas, renvoi
  seulement.
