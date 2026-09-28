# vault-skills

Plugin Claude Code `second-cerveau` pour créer et maintenir un second cerveau : un vault Obsidian organisé selon la méthode PARA, lu et mis à jour par des personas Claude. Le pack réunit onze skills, un skill de persona (`brief-du-jour`) et quatre hooks. Il a été construit au fil de missions d'accompagnement de dirigeants conduites en 2025 et 2026.

## Prérequis

- **Claude Code** : le pack s'installe comme plugin, depuis la marketplace de ce dépôt.
- **bash et python3** : les hooks et le script de localisation du vault en dépendent. `jq` n'est pas requis.
- **git** : nécessaire pour relier un dépôt de code à sa fiche projet (`sync-repo`, rappel de synchronisation).
- **Obsidian** : facultatif. Le vault est un dossier de fichiers Markdown, et Obsidian sert à le consulter et à suivre les wikilinks.

## Installation

### Par le plugin

Dans Claude Code :

```
/plugin marketplace add https://github.com/lightpoichich/vault-skills
/plugin install second-cerveau@vault-skills
```

Le plugin `second-cerveau` contient tous les skills et tous les hooks. Pour installer une nouvelle version :

```
/plugin marketplace update vault-skills
```

### Installation manuelle

```bash
git clone https://github.com/lightpoichich/vault-skills.git
cp -R vault-skills/skills/* ~/.claude/skills/
```

Relancer ensuite Claude Code. Cette voie installe les skills seuls. Les quatre hooks et le script `hooks/vault-resolve.py` ne sont pas installés. Les skills localisent alors le vault en remontant jusqu'à un dossier `_Meta/`, ou par le chemin déclaré dans `~/.claude/CLAUDE.md`.

## Cycle de vie d'un vault

Les skills couvrent trois phases. L'amorçage se fait une fois, dans l'ordre, et chaque skill consomme la sortie du précédent. L'usage quotidien suit une boucle ouverte le matin par `brief-du-jour` et refermée en fin de session par `sync-vault` ou `sync-repo`. L'entretien répond à un événement, à l'exception d'`audit-vault`, prévu en rituel mensuel.

| Phase | Skill | Déclencheur | Résultat |
|---|---|---|---|
| Amorçage | `interview-vault` | démarrage du vault | plan du vault dans `00-Inbox/plan-vault.md` |
| Amorçage | `kickstart-vault` | plan validé | arborescence PARA, Schema, gouvernance, persona Chief of Staff (`cos`) |
| Amorçage | `kickstart-persona` | besoin d'un agent supplémentaire | persona dans `_personas/{slug}/` |
| Amorçage | `vault-skill-creator` | routine récurrente d'une persona | skill rangé dans la persona ou à la racine du vault |
| Usage quotidien | `brief-du-jour` | le matin | brief daté : priorités, alertes, agenda, todos, éléments à valider |
| Usage quotidien | `import-note` | note, URL ou document à ranger | note classée dans la zone PARA adéquate |
| Usage quotidien | `nouveau-projet` | ouverture d'un chantier | fiche projet reliée à son area et à son dépôt de code |
| Usage quotidien | `sync-vault` | fin de session dans le vault | décisions, statuts et todos répercutés dans les fiches |
| Usage quotidien | `sync-repo` | fin de session dans un dépôt de code | même répercussion, limitée à la fiche projet du dépôt |
| Entretien | `extraire-trame` | pratique répétée au moins deux fois | trame réutilisable dans `30-Resources/` |
| Entretien | `gerer-area` | responsabilité créée, scindée, fusionnée ou disparue | area créée, renommée, scindée, fusionnée ou archivée |
| Entretien | `audit-vault` | rituel mensuel | rapport daté dans `00-Inbox/`, puis traitement par lots après validation |

`brief-du-jour` ne figure pas dans `skills/`. Il est livré dans les assets de `kickstart-vault`, qui le dépose dans la persona Chief of Staff au moment du scaffold. Il ne s'active que depuis cette persona.

## Travail depuis un dépôt de code

Les skills d'usage quotidien fonctionnent aussi depuis un dossier situé hors du vault, par exemple le dépôt de code d'un projet client. Le script `hooks/vault-resolve.py` localise le vault et la fiche projet correspondante, en lecture seule.

- **Localisation du vault** : le script lit d'abord les `@imports` du `CLAUDE.md` du dossier et de ses dossiers parents, puis les `@imports` et les chemins absolus cités dans `~/.claude/CLAUDE.md`, puis `~/vault`.
- **Localisation de la fiche projet** : dans `10-Projects/`, le script retient d'abord la fiche dont le champ `repo:` correspond au remote `origin` du dépôt, puis celle dont le champ `dossier-travail:` correspond au dossier, puis celle dont le slug correspond au nom du dossier.
- **Liaison** : `nouveau-projet` pose les champs `repo:` et `dossier-travail:` dans la fiche. Un projet situé dans un sous-dossier du dépôt porte le suffixe `#sous-dossier`, par exemple `https://github.com/org/repo#apps/api`.

## Descriptions des skills

Chaque entrée reprend mot pour mot la description du `SKILL.md`, c'est-à-dire le texte que Claude Code lit pour décider de lancer le skill. Les formulations entre guillemets sont des exemples de demandes qui le déclenchent. Les skills d'usage quotidien lisent `_Meta/sources.md` et utilisent les connecteurs qui y sont déclarés.

<!-- SKILLS:BEGIN -->
### Amorçage

- **`interview-vault`** : Mène l'interview de cartographie PARA d'une activité et écrit 00-Inbox/plan-vault.md, le plan que kickstart-vault exécute ensuite. S'adapte aux réponses du dirigeant sans questionnaire figé et n'écrit rien hors de 00-Inbox/. S'utilise quand l'utilisateur dit « cartographier mon activité », « préparer mon vault », « faire l'interview PARA », « monter mon second cerveau » sur un vault vide. Pour matérialiser le plan, voir kickstart-vault.
- **`kickstart-vault`** : Scaffolde un vault Obsidian PARA à partir du plan-vault.md produit par interview-vault : arborescence, Schema, governance, CLAUDE.md racine, fiches vides d'Areas et de Projects, persona Chief of Staff avec brief-du-jour. S'utilise quand l'utilisateur a un plan-vault.md et dit « crée la structure », « initialise le vault », « génère l'arborescence », « monte mon second cerveau ». Pour mener l'interview qui produit le plan, voir interview-vault.
- **`kickstart-persona`** : Crée le shell d'une persona Claude dans un vault Obsidian : _personas/{slug}/CLAUDE.md (rôle, périmètre lecture/écriture, garde-fous), dossier .claude/skills/ vide et alias terminal. Part d'une découverte du quotidien avant de fixer le rôle. S'utilise quand l'utilisateur dit « crée-moi un agent », « nouvelle persona », « ajoute un Chief of Staff », « je veux un assistant RH dans mon vault ». Pour donner des compétences à la persona, voir vault-skill-creator.
- **`vault-skill-creator`** : Crée un skill Claude Code à partir d'une routine récurrente d'une persona et le place dans le vault Obsidian : dans _personas/{slug}/.claude/skills/ pour une capacité de persona, à la racine du vault pour une capacité transverse. Interroge sur les données lues par la procédure et propose l'accès (MCP ou import). S'utilise quand l'utilisateur dit « encode mon triage-mails », « crée un skill pour mon Chief of Staff », « porte mon skill Desktop dans le vault », ou pioche dans capacites-a-construire.md. Pour créer le vault ou une persona, voir kickstart-vault et kickstart-persona.

### Usage quotidien

- **`brief-du-jour`** : Produit le brief du jour dans 00-Inbox/briefs/{date}.md (Priorités, Alertes, Agenda, Todos, À valider) à partir du vault et des sources déclarées dans _Meta/sources.md, en dégradant proprement si une source manque. S'utilise quand l'utilisateur dit « mon brief », « le point du matin », « qu'est-ce que j'ai aujourd'hui ». Pour faire entrer une note, voir import-note.
- **`import-note`** : Fait entrer une note ou un contenu externe dans le vault, une note à la fois : détecte la nature de l'entrée (URL, page Notion, fichier local, texte collé), l'acquiert, puis la classe dans la zone PARA adéquate avec frontmatter conforme au Schema et wikilinks. Pose un renvoi plutôt qu'une copie pour le sensible et le vivant. S'utilise quand l'utilisateur dit « importe cette note », « range cette page Notion / cet article dans le vault », « fais entrer ce doc », « ajoute ça à mon projet X », ou colle un texte à ranger. Pour capitaliser une pratique déjà dans le vault, voir extraire-trame.
- **`nouveau-projet`** : Crée un projet dans un vault Obsidian déjà structuré, ou complète un projet encore vide : pose 10-Projects/{slug}/{slug}.md avec un frontmatter type: project conforme au Schema, relie l'Area parente et le dossier de travail, puis rattache le contexte réel existant (note d'inbox, réunion, fil d'emails) via import-note, sans rien inventer. S'utilise quand l'utilisateur dit « lancer un nouveau projet », « créer le projet X », « ouvrir un chantier », « complète le projet X », « le projet X est vide ». Pour faire entrer une note isolée sans créer de projet, voir import-note.
- **`sync-vault`** : Met à jour et consolide les fiches du vault à partir de la conversation en cours : décisions, statuts, todos, faits nouveaux, sections « À répercuter », sas 00-Inbox/_drafts/ et mémoire native de Claude Code. Agit sans validation et réécrit plutôt qu'empiler. S'utilise quand l'utilisateur dit « sync le vault », « mets à jour le vault », « répercute ce qu'on a décidé », « allège le vault », ou sur rappel du hook Stop en fin de tour. Depuis un dépôt de code, sync-repo s'applique à la place.
- **`sync-repo`** : Répercute une session menée depuis un dépôt de code dans la seule fiche projet du vault qui lui correspond : avancement, décisions, todos, statut, à partir de la conversation et des commits récents. Ce qui concerne d'autres fiches est déposé dans la section « À répercuter » de la fiche projet, que sync-vault traite ensuite. Ne crée jamais de fiche. S'utilise quand l'utilisateur, dans un dépôt, dit « mets à jour la fiche projet », « répercute dans le vault », « sync le projet », ou sur rappel du hook Stop en fin de tour. Depuis l'intérieur du vault, sync-vault s'applique à la place.

### Entretien

- **`extraire-trame`** : Capitalise une pratique récurrente du vault en trame réutilisable dans 30-Resources/ : retrouve les occurrences réelles, Archive comprise, en extrait la forme commune sans rien inventer, la range dans la bonne sous-zone et la lie à ses fiches sources. Propose la généralisation et attend la validation avant d'écrire. S'utilise quand l'utilisateur dit « ça, je le refais à chaque fois », « fais-en une trame », « on a déjà fait ça trois fois », « capitalise cette méthode », ou reprend un candidat signalé par sync-vault. Pour un modèle qui existe déjà hors du vault, voir import-note.
- **`gerer-area`** : Gère le cycle de vie d'une area dans un vault déjà vivant : crée une nouvelle responsabilité (20-Areas/{slug}/ et fiche conforme au Schema), complète un shell vide, renomme, scinde, fusionne ou archive une area dont la responsabilité a disparu. Exécute un geste demandé ; le diagnostic appartient à audit-vault. S'utilise quand l'utilisateur dit « crée une area », « renomme / scinde / fusionne l'area X », « archive l'area X », « cette responsabilité n'existe plus », « l'area X est vide », ou reprend une suggestion d'audit. Pour scaffolder le vault entier, voir kickstart-vault.
- **`audit-vault`** : Contrôle technique d'un vault Obsidian PARA : wikilinks cassés, fiches orphelines, frontmatter hors Schema, noms hors kebab-case, pollution, Inbox stale, projets à archiver, areas mortes ou sans consommateur, zones de personas invalides. Produit un rapport daté dans 00-Inbox/ puis propose le traitement par lots, sans écrire avant validation. S'utilise quand l'utilisateur dit « audit du vault », « fais le ménage », « fais le point sur le vault », « qu'est-ce qui traîne », « c'est le bazar », « wikilinks cassés », ou sur rituel mensuel. Pour répercuter la session en cours dans les fiches, voir sync-vault.
<!-- SKILLS:END -->
## Hooks du plugin

Le plugin installe quatre hooks, actifs dans toute session Claude Code. Hors d'un vault ou d'un dépôt relié à un vault, ils ne produisent rien.

| Hook | Événement | Rôle |
|---|---|---|
| `vault-health.sh` | démarrage de session | injecte un bilan de santé dans le contexte (notes d'Inbox anciennes, notes sans `type`) et supprime les fichiers `.DS_Store` |
| `vault-approve-imports.sh` | démarrage de session | approuve pour le dossier courant les imports du vault, que Claude Code ignorerait sinon comme imports externes |
| `vault-note-guard.sh` | après l'écriture d'une note | renseigne `created` et `updated` dans un frontmatter existant, signale un frontmatter absent ou un nom de fichier hors kebab-case |
| `vault-sync-nudge.sh` | fin de tour | demande une fois `sync-vault` depuis le vault, ou `sync-repo` depuis un dépôt relié, quand les seuils de volume et de durée sont atteints ; aucun rappel depuis un worktree git lié |

### Réglages des hooks

Les réglages se placent dans `{vault}/_Meta/hooks.conf`. `kickstart-vault` y copie le gabarit `skills/kickstart-vault/assets/hooks/hooks.conf`.

- **`EXCLUDE`** : chemins du vault ignorés par le bilan de santé et par le garde-fou d'écriture.
- **`INBOX_STALE_DAYS`** : ancienneté, en jours, à partir de laquelle une note d'Inbox est signalée (14 par défaut).
- **`APPROVE_EXTERNAL_IMPORTS`** : la valeur `0` désactive l'approbation automatique des imports.
- **`SYNC_MIN_KB`** et **`SYNC_MIN_MINUTES`** : seuils du rappel de synchronisation, 40 Ko de transcript et 20 minutes depuis la dernière synchronisation par défaut. Les deux seuils doivent être atteints.
- **`SYNC_NUDGE`** : la valeur `0` supprime le rappel, la valeur `vault` le limite aux sessions ouvertes dans le vault.
- **`SYNC_NUDGE_WORKTREES`** : la valeur `1` rétablit le rappel dans les worktrees git liés. Par défaut, les sous-agents qui traitent des tickets en parallèle dans des worktrees ne reçoivent pas de rappel, et l'orchestrateur synchronise une seule fois depuis le checkout principal.

### Synchronisation git d'un vault partagé

`skills/kickstart-vault/assets/hooks/vault-git-sync.sh` est un gabarit facultatif, distinct des hooks du plugin. Il synchronise par git un vault partagé entre un poste de travail et une machine sans écran qui exécute des agents. Il fait un pull au démarrage de session, un commit local en fin de tour, et un push déclenché par un minuteur externe. Il ne s'exécute que sous Linux. `kickstart-vault` le propose quand le plan du vault mentionne une telle machine, et son installation dans `{vault}/.claude/hooks/` se fait à la main.

## Principes de conception

- **Structure d'abord** : les skills génèrent l'arborescence, les schémas et des fiches vides. Le contenu entre dans le vault par l'usage.
- **Import à la demande** : une note entre dans le vault quand un besoin concret la justifie. Le vault n'est pas rempli en bloc au démarrage.
- **Un lecteur par dossier** : chaque area doit avoir un consommateur identifié. Une area sans consommateur est signalée dès sa création.
- **Gouvernance au scaffold** : le périmètre, les données sensibles et les accès des agents sont fixés à la création du vault.
- **Sources déclarées** : les connecteurs disponibles sont listés dans `_Meta/sources.md`. Un skill utilise les sources déclarées et produit un résultat réduit quand l'une d'elles manque. Le pack fonctionne sans aucun connecteur.
- **Information unique** : une information vit à un seul endroit. Le suivi d'un projet est tenu dans sa fiche du vault, et le dépôt de code n'en porte pas de copie. Les sources externes sont référencées par lien.

## Attribution

`vault-skill-creator` adapte le `skill-creator` officiel d'Anthropic, publié dans la marketplace `claude-plugins-official`. L'adaptation ajoute le placement automatique dans le vault et une étape « sources de données », et rend l'évaluation optionnelle. Le moteur et les scripts d'origine sont conservés. La licence figure dans `skills/vault-skill-creator/LICENSE.txt`.

Conçu et maintenu par [Lucas Clément](https://devlc.co), delivery de produits digitaux et accompagnement Claude Code pour dirigeants.
