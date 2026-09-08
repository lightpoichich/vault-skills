---
name: kickstart-persona
description: >-
  Crée le shell d'une persona Claude dans un vault Obsidian : _personas/{slug}/CLAUDE.md (rôle,
  périmètre lecture/écriture, garde-fous), dossier .claude/skills/ vide et alias terminal. Part
  d'une découverte du quotidien avant de fixer le rôle. S'utilise quand l'utilisateur dit
  « crée-moi un agent », « nouvelle persona », « ajoute un Chief of Staff », « je veux un assistant
  RH dans mon vault ». Pour donner des compétences à la persona, voir vault-skill-creator.
---

# Kickstart Persona

Une persona est un rôle incarné : un `CLAUDE.md` dans `_personas/{slug}/` qui dit qui elle est
(rôle), ce qu'elle lit et écrit dans le vault, et ce qu'elle s'interdit. Ce skill pose cette
identité et un dossier `.claude/skills/` vide, puis note les routines récurrentes dans un backlog.
Il ne crée aucun skill et n'invoque pas `vault-skill-creator` : chaque routine devient ensuite un
skill dans `_personas/{slug}/.claude/skills/`, une à la fois, quand le besoin est réel. Le skill
détecte la racine du vault et n'écrit aucun chemin codé en dur : il travaille sur le vault de la
personne devant lui.

## Partis pris

- **Identité ici, capacités ensuite.** Le `CLAUDE.md` dit ce que la persona fait ; les skills
  disent comment. Ne pas écrire la procédure d'une tâche dans le `CLAUDE.md`. Se surprendre à coder
  un `triage-mails.md` est le signal de lancer `vault-skill-creator`, pas d'écrire un fichier.
- **Rien d'inventé.** Le shell reprend le rôle et les zones que l'utilisateur a décrits, sans
  responsabilité ni compétence qu'il n'a pas nommée. Une section sans matière reste au minimum.
- **Non destructif et idempotent.** Demander avant d'écraser une persona existante ; ne pas
  dupliquer un alias présent. Une ré-exécution complète ce qui manque sans casser l'existant.

Où vit une persona, pourquoi son `CLAUDE.md` reste minimal et comment choisir ses zones :
`references/persona-design.md`.

## Prérequis

La persona se greffe sur un vault déjà installé. La racine doit contenir `CLAUDE.md`,
`_Meta/Schema.md` et `_personas/`. Sinon, s'arrêter et orienter vers `kickstart-vault`.

`kickstart-vault` pose une persona Chief of Staff par défaut (`_personas/cos/`, livrée avec
`brief-du-jour`) : `_personas/` n'est donc en général pas vide au premier passage. Si l'utilisateur
relance pour un Chief of Staff, l'étape 4 le détecte et propose compléter, écraser ou annuler.

## La découverte

Demander le rôle et les zones directement produit un périmètre flou. Faire d'abord raconter le
quotidien, puis déduire rôle et périmètre. Les quatre tours (partir du réel, creuser le vague,
reformuler et faire valider, dériver le périmètre), les exemples de questions et les relances sont
dans `references/discovery-interview.md` ; les questions y sont des exemples de formulation, pas un
questionnaire.

Converger quand trois choses sont nettes : le rôle en une phrase, deux à quatre tâches récurrentes
concrètes qui le justifient, un périmètre lecture/écriture ancré sur des dossiers réels. Tant que
l'une reste vague, continuer. Si la personne répond d'emblée de façon précise et complète, une
reformulation de validation suffit. Les tâches récurrentes mises au jour forment le backlog de
capacités (étape 8), pas des skills.

## Procédure

### 1. Localiser le vault

Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter
jusqu'à un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé.

Mémoriser la racine en `VAULT_ABS` (chemin absolu, il sert à l'alias) et y vérifier les prérequis.
Si `mode` vaut `none` ou qu'un prérequis manque, s'arrêter et orienter vers `kickstart-vault`. Tout
le reste se fait relativement à `$VAULT_ABS`.

### 2. Mener la découverte

Conduire la conversation de `references/discovery-interview.md`. Lire la carte du `CLAUDE.md`
racine pour proposer un périmètre ancré sur des dossiers réels. Ne pas passer à la génération tant
que le trio rôle, tâches récurrentes, périmètre n'est pas net. Le nom vient souvent du rôle ; sinon
le proposer (« on l'appelle “Chief of Staff” ? »).

### 3. Dériver le slug

Nom en kebab-case, avec les abréviations naturelles : « Chief of Staff » donne `cos`, « RH » donne
`rh`, « Métier » donne `metier`, « Veille réglementaire » donne `veille-reglementaire`. Si le slug
n'est pas évident, le proposer et demander confirmation : c'est l'alias que l'utilisateur tapera
chaque jour.

### 4. Vérifier que la persona n'existe pas

```bash
ls "$VAULT_ABS/_personas/{slug}/" 2>/dev/null
```
Si le dossier existe, prévenir et demander : compléter, écraser ou annuler. Ne pas écraser un
`CLAUDE.md` de persona sans accord explicite.

### 5. Créer la structure

```bash
mkdir -p "$VAULT_ABS/_personas/{slug}/.claude/skills"
```
Le dossier `.claude/skills/` reste vide : `vault-skill-creator` y créera chaque routine plus tard,
chargée seulement quand on lance cette persona.

### 6. Générer le `CLAUDE.md` de la persona

Écrire `_personas/{slug}/CLAUDE.md` depuis `assets/persona-claude-template.md`, en remplissant les
emplacements avec le rôle et les zones issus de la découverte. Garder le fichier court : il hérite
du `CLAUDE.md` racine, il ne le réplique pas.
- **Ton hérité.** La section Ton dit « Suit le ton du vault ». N'ajouter un écart que si le rôle le
  réclame (persona juridique plus formelle, persona veille plus neutre) ; dans ce cas seulement, le
  vérifier avec l'utilisateur en une question.

### 7. Poser l'alias terminal

Ajouter un alias qui lance la persona en un mot, avec le chemin absolu détecté. Détecter le shell
de l'utilisateur, viser le bon fichier de configuration, ne pas dupliquer si l'alias existe.

```bash
RC="$HOME/.zshrc"; [ -n "$BASH_VERSION" ] && RC="$HOME/.bashrc"
LINE="alias {slug}=\"cd '$VAULT_ABS/_personas/{slug}' && claude\""
grep -q "alias {slug}=" "$RC" 2>/dev/null || echo "$LINE" >> "$RC"
```
Indiquer à l'utilisateur de recharger son shell (`source "$RC"`) ou d'ouvrir un nouvel onglet.

### 7bis. Approuver les imports du vault pour la persona

Lancée depuis `_personas/{slug}/`, la persona hérite du `CLAUDE.md` racine, mais ses `@imports`
(`_Meta/Schema.md`, `governance.md`, `sources.md`) sortent du cwd. Claude Code les tient pour
externes et les ignore en silence tant que ce dossier n'est pas approuvé dans `~/.claude.json` ; le
dialogue « Allow external CLAUDE.md file imports? » n'apparaît pas en mode `-p`, SDK ou depuis un lanceur non interactif. Le
plugin pose l'approbation sans session interactive :

```bash
"${CLAUDE_PLUGIN_ROOT}/hooks/vault-approve-imports.sh" "$VAULT_ABS/_personas/{slug}"
```

Le script n'approuve que des imports qui se résolvent dans un vault et n'écrit rien sinon. Le hook
SessionStart du plugin ferait la même chose à la première session dans ce dossier, avec effet à la
suivante ; l'appel ici évite cette première session sans contrats. Sans plugin
(`CLAUDE_PLUGIN_ROOT` absent), le signaler : l'utilisateur lance `{slug}` une fois en interactif et
répond « Yes, allow external imports ».

### 8. Persister le backlog des capacités

Écrire les tâches récurrentes de la découverte dans `_personas/{slug}/capacites-a-construire.md`,
reprises de l'échange (entrée, action, livrable, fréquence), jamais inventées. Gabarit :

```markdown
# {Nom} : capacités à construire

> Backlog des routines à encoder en skills (via vault-skill-creator) dans `.claude/skills/`.
> Ce ne sont pas des capacités en place, c'est un plan de route. Cocher au fur et à mesure.

- [ ] **{tâche 1}** : entrée {…} ; action {…} ; livrable {…} ; fréquence {…}
- [ ] **{tâche 2}** : …
```

Ne pas formuler ce fichier comme si la persona savait déjà faire ces tâches. Si aucune tâche nette
n'est ressortie, ne pas créer le fichier et proposer `vault-skill-creator` au prochain besoin réel.

### 9. Résumé

```
Persona {Nom} créée :
- Identité   : _personas/{slug}/CLAUDE.md
- Capacités  : _personas/{slug}/.claude/skills/  (vide, à remplir via vault-skill-creator)
- Backlog    : _personas/{slug}/capacites-a-construire.md
- Lancement  : tape `{slug}` dans le terminal (après `source` de ton fichier shell)
- Imports    : contrats du vault (Schema, governance, sources) approuvés pour ce dossier dans ~/.claude.json

Procédures à encoder ensuite (rien n'est codé) :
- {tâche récurrente 1, la plus fréquente ou la plus pénible}
- {tâche récurrente 2}
- {tâche récurrente 3}

Prochaine étape : invoque vault-skill-creator pour construire « {tâche la plus rentable} »
dans _personas/{slug}/.claude/skills/.
```
Sans backlog, omettre la ligne Backlog et les deux derniers blocs.

## Cas limites

- **Vault introuvable** : s'arrêter, orienter vers `kickstart-vault`.
- **Persona déjà existante** : demander compléter, écraser ou annuler.
- **Slug ambigu** (nom composé sans abréviation évidente) : proposer un slug et confirmer.
- **Utilisateur hésitant sur les zones** : proposer depuis la carte du vault, sans trancher à sa
  place ni tout ouvrir « au cas où ».
- **Chevauchement de zones d'écriture entre personas** : le signaler (« RH et CoS écrivent tous
  deux dans `00-Inbox/_drafts/` ; c'est acceptable si c'est voulu »), sans bloquer.
- **Ni zsh ni bash détecté** : écrire la ligne d'alias et laisser l'utilisateur la placer dans le
  bon fichier.
- **`~/.claude.json` absent ou `CLAUDE_PLUGIN_ROOT` indisponible** (étape 7bis) : ne pas modifier
  le fichier à la main ; indiquer la voie interactive.
