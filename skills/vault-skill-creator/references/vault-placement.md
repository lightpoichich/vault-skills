# Placement et conventions vault

Détail de la Phase 0 de `vault-skill-creator` : situer le vault, choisir le tier, lire le backlog,
respecter les conventions du skill généré, porter un skill existant.

## 1. Détecter la racine du vault

Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé.

Tout chemin se déduit ensuite de la racine trouvée ; aucun chemin n'est codé en dur.

Si `mode` n'est pas `vault`, placer le skill dans `.claude/skills/` du dossier courant ou à
l'endroit demandé par l'utilisateur. Rien de ce qui suit ne s'applique ; ne pas plaquer une
structure vault sur un dossier qui n'en est pas un.

## 2. Les trois tiers

Claude Code charge les skills `.claude/skills/` du dossier de lancement et de chaque parent jusqu'à
la racine.

| Tier | Emplacement | Chargé quand | Pour quoi |
|---|---|---|---|
| Transverse | `{vault}/.claude/skills/{name}/` | partout dans le vault | capacité utile à toutes les personas (`import-note`, `audit-vault`) |
| Persona | `_personas/{slug}/.claude/skills/{name}/` | quand cette persona est lancée | capacité d'un rôle (`triage-mails` pour le Chief of Staff) |
| Machine | `~/.claude/skills/` | toutes sessions, hors vault | rien de propre à un vault |

Un skill de vault ne va pas en `~/.claude/skills/` : il y serait détaché du vault, hors de son
versioning et chargé hors contexte.

Il n'existe pas de skill au niveau d'une area (pas de `20-Areas/{slug}/.claude/skills/`). Une
capacité est portée par une persona ou transverse au vault.

### Choisir le tier

- cwd dans `_personas/{slug}/` : tier persona. C'est la posture par défaut, la persona étant lancée
  par son alias (`cd _personas/{slug}/ && claude`).
- cwd ailleurs dans le vault : probablement transverse. Confirmer : « cette capacité sert à une
  persona, ou à tout le vault ? ».

Test : la capacité a-t-elle un sens hors de cette persona ? Non, tier persona (le cas le plus
fréquent). Oui, tier transverse.

## 3. Le backlog de la persona

`kickstart-persona` pose `_personas/{slug}/capacites-a-construire.md` : une case à cocher par
routine récurrente, avec son input, son action, son livrable et sa fréquence.

- S'il existe, le lire en Phase 0, lister ce qui reste et proposer la routine la plus rentable (la
  plus fréquente ou la plus pénible).
- En fin de course, passer la case de `[ ]` à `[x]` et noter en fin de ligne l'emplacement du skill
  (`.claude/skills/{name}/`).
- S'il n'existe pas, encoder quand même et proposer de créer le backlog avec la routine déjà cochée,
  pour la trace.

## 4. Conventions du skill généré

- Nommage en kebab-case pour le dossier et pour le `name` ; `scripts/quick_validate.py` le vérifie.
- Frontmatter natif de skill : `name`, `description`, `compatibility` si utile. Pas de frontmatter
  de note vault (`type:`, `tags:`, `status:`) : un SKILL.md n'est pas une fiche Obsidian. Sous
  `.claude/`, il est exclu des hooks du vault, donc ni stamping `created`/`updated`, ni rappel
  frontmatter, ni rien à ajouter pour le Schema.
- La procédure hérite de la discipline vault de la persona, puisqu'elle s'exécute dans sa session :
  - routage par destination (`governance.md`, « Savoir vs Livrable ») : un livrable sortant (mail,
    courrier, proposition) va dans `00-Inbox/_drafts/` en `statut: en-attente` avec son `lien`, sans
    envoi automatique ;
  - un savoir interne (fiche, résumé, synthèse) s'écrit directement à sa place PARA ;
  - relations en `[[wikilinks]]`, pas de chemin en dur dans le contenu ;
  - lecture de `_Meta/Schema.md` avant toute écriture de note ;
  - renvoi, jamais copie : une source externe se référence dans `30-Resources/references-externes/`
    par un lien et une ligne de contexte ;
  - marqueur 🔒 pour le sensible ; pas de donnée confidentielle hors des zones autorisées de la
    persona.
- On pose le cadre, pas le contenu : encoder la procédure réelle issue de l'interview, sans étape,
  exemple, fichier ni cas que l'utilisateur n'a pas décrits.
- Sources explicites : la procédure dit d'où vient son input (zone du vault, connecteur, ou collage
  manuel avec un `TODO : brancher {source}`).

## 5. Porter un skill existant

Cas courant : un prompt ou un skill Claude Desktop (un `cr-aurae` qui résume une réunion) à
rapatrier dans le vault.

1. Récupérer la matière : le prompt ou la procédure existante, ses entrées et sorties typiques.
2. Placer au bon tier (section 2), presque toujours celui de la persona.
3. Renommer en kebab-case si besoin et écrire la `description` selon le gabarit du SKILL.md.
4. Réaligner sur les conventions (section 4). Les sorties « dans le chat » deviennent des écritures
   cadrées : drafts vers `00-Inbox/_drafts/`, traces sur la fiche projet. L'input se branche sur une
   zone du vault ou un connecteur plutôt que sur un collage systématique.
5. Tester en vrai dans la persona, ajuster, cocher le backlog.
