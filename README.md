# vault-skills

Skills Claude Code pour monter et faire vivre un second cerveau : un vault Obsidian structuré en PARA, lu et écrit au quotidien par des personas Claude. Le pack est issu de missions d'accompagnement de dirigeants menées en 2025 et 2026.

## Installation

Dans Claude Code :

```
/plugin marketplace add https://github.com/lightpoichich/vault-skills
/plugin install second-cerveau@vault-skills
```

Un seul plugin embarque tout le pack. Pour les mises à jour :

```
/plugin marketplace update vault-skills
```

## Le cycle de vie d'un vault

Les skills s'enchaînent le long du cycle de vie du vault. On l'amorce une fois, on le fait vivre chaque jour, on l'entretient au signal.

```
AMORCER      une seule fois, dans l'ordre
             interview-vault        le plan
             kickstart-vault        le vault, avec une persona Chief of Staff (cos) prête à l'emploi
             kickstart-persona      les agents supplémentaires
             vault-skill-creator    leurs compétences

FAIRE VIVRE  à chaque session de travail
             brief-du-jour          le matin : priorités, alertes, agenda, todos
             import-note            une note, une URL ou un doc entre au bon endroit
             nouveau-projet         un chantier naît ou se complète
             sync-vault             fin de session : décisions et statuts répercutés, fiches gardées concises
             sync-repo              même geste depuis un dossier de code, sur la seule fiche projet

ENTRETENIR   quand quelque chose le déclenche
             extraire-trame         une pratique revient au moins deux fois
             gerer-area             une responsabilité naît, se scinde, fusionne ou disparaît
             audit-vault            contrôle technique mensuel du contenant
```

L'amorçage est une chaîne : chaque skill consomme la sortie du précédent. Le quotidien est une boucle : `brief-du-jour` ouvre la journée, `import-note` et `nouveau-projet` se déclenchent à la demande, `sync-vault` la referme. Un hook du plugin rappelle `sync-vault` en fin de tour quand la session a produit assez de matière, ou `sync-repo` depuis un dépôt de code relié. Les skills d'entretien répondent à un événement, pas à un calendrier, sauf `audit-vault`.

Les skills du quotidien se lancent depuis n'importe quel dossier, y compris un dossier de code hors du vault. Ils retrouvent le vault par le chemin absolu déclaré dans le `CLAUDE.md` global, et `nouveau-projet` relie le dossier de travail à sa fiche projet.

## Les skills

Chaque entrée reprend la description du skill telle que Claude Code la lit pour décider de le déclencher.

<!-- SKILLS:BEGIN -->
### Amorcer

La chaîne d'amorçage, dans l'ordre. On la déroule une seule fois, au démarrage d'un vault.

- **`interview-vault`** : Mène l'interview de cartographie PARA d'une activité et écrit 00-Inbox/plan-vault.md, le plan que kickstart-vault exécute ensuite. S'adapte aux réponses du dirigeant sans questionnaire figé et n'écrit rien hors de 00-Inbox/. S'utilise quand l'utilisateur dit « cartographier mon activité », « préparer mon vault », « faire l'interview PARA », « monter mon second cerveau » sur un vault vide. Pour matérialiser le plan, voir kickstart-vault.
- **`kickstart-vault`** : Scaffolde un vault Obsidian PARA à partir du plan-vault.md produit par interview-vault : arborescence, Schema, governance, CLAUDE.md racine, fiches vides d'Areas et de Projects, persona Chief of Staff avec brief-du-jour. S'utilise quand l'utilisateur a un plan-vault.md et dit « crée la structure », « initialise le vault », « génère l'arborescence », « monte mon second cerveau ». Pour mener l'interview qui produit le plan, voir interview-vault.
- **`kickstart-persona`** : Crée le shell d'une persona Claude dans un vault Obsidian : _personas/{slug}/CLAUDE.md (rôle, périmètre lecture/écriture, garde-fous), dossier .claude/skills/ vide et alias terminal. Part d'une découverte du quotidien avant de fixer le rôle. S'utilise quand l'utilisateur dit « crée-moi un agent », « nouvelle persona », « ajoute un Chief of Staff », « je veux un assistant RH dans mon vault ». Pour donner des compétences à la persona, voir vault-skill-creator.
- **`vault-skill-creator`** : Crée un skill Claude Code à partir d'une routine récurrente d'une persona et le place dans le vault Obsidian : dans _personas/{slug}/.claude/skills/ pour une capacité de persona, à la racine du vault pour une capacité transverse. Interroge sur les données lues par la procédure et propose l'accès (MCP ou import). S'utilise quand l'utilisateur dit « encode mon triage-mails », « crée un skill pour mon Chief of Staff », « porte mon skill Desktop dans le vault », ou pioche dans capacites-a-construire.md. Pour créer le vault ou une persona, voir kickstart-vault et kickstart-persona.

### Faire vivre

Le quotidien, une fois le vault posé. Ces skills lisent `_Meta/sources.md` et s'adaptent aux connecteurs déclarés.

- **`brief-du-jour`** : Produit le brief du jour dans 00-Inbox/briefs/{date}.md (Priorités, Alertes, Agenda, Todos, À valider) à partir du vault et des sources déclarées dans _Meta/sources.md, en dégradant proprement si une source manque. S'utilise quand l'utilisateur dit « mon brief », « le point du matin », « qu'est-ce que j'ai aujourd'hui ». Pour faire entrer une note, voir import-note.
- **`import-note`** : Fait entrer une note ou un contenu externe dans le vault, une note à la fois : détecte la nature de l'entrée (URL, page Notion, fichier local, texte collé), l'acquiert, puis la classe dans la zone PARA adéquate avec frontmatter conforme au Schema et wikilinks. Pose un renvoi plutôt qu'une copie pour le sensible et le vivant. S'utilise quand l'utilisateur dit « importe cette note », « range cette page Notion / cet article dans le vault », « fais entrer ce doc », « ajoute ça à mon projet X », ou colle un texte à ranger. Pour capitaliser une pratique déjà dans le vault, voir extraire-trame.
- **`nouveau-projet`** : Crée un projet dans un vault Obsidian déjà structuré, ou complète un projet encore vide : pose 10-Projects/{slug}/{slug}.md avec un frontmatter type: project conforme au Schema, relie l'Area parente et le dossier de travail, puis rattache le contexte réel existant (note d'inbox, réunion, fil d'emails) via import-note, sans rien inventer. S'utilise quand l'utilisateur dit « lancer un nouveau projet », « créer le projet X », « ouvrir un chantier », « complète le projet X », « le projet X est vide ». Pour faire entrer une note isolée sans créer de projet, voir import-note.
- **`sync-vault`** : Met à jour et consolide les fiches du vault à partir de la conversation en cours : décisions, statuts, todos, faits nouveaux, sections « À répercuter », sas 00-Inbox/_drafts/ et mémoire native de Claude Code. Agit sans validation et réécrit plutôt qu'empiler. S'utilise quand l'utilisateur dit « sync le vault », « mets à jour le vault », « répercute ce qu'on a décidé », « allège le vault », ou sur rappel du hook Stop en fin de tour. Depuis un dépôt de code, sync-repo s'applique à la place.
- **`sync-repo`** : Répercute une session menée depuis un dépôt de code dans la seule fiche projet du vault qui lui correspond : avancement, décisions, todos, statut, à partir de la conversation et des commits récents. Ce qui concerne d'autres fiches est déposé dans la section « À répercuter » de la fiche projet, que sync-vault traite ensuite. Ne crée jamais de fiche. S'utilise quand l'utilisateur, dans un dépôt, dit « mets à jour la fiche projet », « répercute dans le vault », « sync le projet », ou sur rappel du hook Stop en fin de tour. Depuis l'intérieur du vault, sync-vault s'applique à la place.

### Entretenir

Les skills qui gardent le vault vrai et propre dans la durée.

- **`extraire-trame`** : Capitalise une pratique récurrente du vault en trame réutilisable dans 30-Resources/ : retrouve les occurrences réelles, Archive comprise, en extrait la forme commune sans rien inventer, la range dans la bonne sous-zone et la lie à ses fiches sources. Propose la généralisation et attend la validation avant d'écrire. S'utilise quand l'utilisateur dit « ça, je le refais à chaque fois », « fais-en une trame », « on a déjà fait ça trois fois », « capitalise cette méthode », ou reprend un candidat signalé par sync-vault. Pour un modèle qui existe déjà hors du vault, voir import-note.
- **`gerer-area`** : Gère le cycle de vie d'une area dans un vault déjà vivant : crée une nouvelle responsabilité (20-Areas/{slug}/ et fiche conforme au Schema), complète un shell vide, renomme, scinde, fusionne ou archive une area dont la responsabilité a disparu. Exécute un geste demandé ; le diagnostic appartient à audit-vault. S'utilise quand l'utilisateur dit « crée une area », « renomme / scinde / fusionne l'area X », « archive l'area X », « cette responsabilité n'existe plus », « l'area X est vide », ou reprend une suggestion d'audit. Pour scaffolder le vault entier, voir kickstart-vault.
- **`audit-vault`** : Contrôle technique d'un vault Obsidian PARA : wikilinks cassés, fiches orphelines, frontmatter hors Schema, noms hors kebab-case, pollution, Inbox stale, projets à archiver, areas mortes ou sans consommateur, zones de personas invalides. Produit un rapport daté dans 00-Inbox/ puis propose le traitement par lots, sans écrire avant validation. S'utilise quand l'utilisateur dit « audit du vault », « fais le ménage », « fais le point sur le vault », « qu'est-ce qui traîne », « c'est le bazar », « wikilinks cassés », ou sur rituel mensuel. Pour répercuter la session en cours dans les fiches, voir sync-vault.
<!-- SKILLS:END -->

`brief-du-jour` n'est pas dans `skills/` : il voyage dans les assets de `kickstart-vault`, qui le dépose dans la persona Chief of Staff au moment du scaffold. Il ne s'active que depuis cette persona.

## Les hooks du plugin

Quatre hooks tournent dans toute session Claude Code et restent silencieux hors d'un vault.

| Hook | Moment | Rôle |
|---|---|---|
| `vault-health.sh` | démarrage de session | bilan de santé injecté dans le contexte (Inbox qui traîne, notes sans `type`), purge des `.DS_Store` |
| `vault-approve-imports.sh` | démarrage de session | approuve pour le dossier courant les imports du vault que Claude Code tiendrait sinon pour externes |
| `vault-note-guard.sh` | après l'écriture d'une note | pose `created` et `updated` dans un frontmatter existant, signale un frontmatter absent ou un nom hors kebab-case |
| `vault-sync-nudge.sh` | fin de tour | rappelle `sync-vault` depuis le vault, `sync-repo` depuis un dépôt relié, au-delà des seuils |

Réglages dans `{vault}/_Meta/hooks.conf` : `EXCLUDE`, `INBOX_STALE_DAYS`, `APPROVE_EXTERNAL_IMPORTS`, `SYNC_MIN_KB`, `SYNC_MIN_MINUTES`, `SYNC_NUDGE`. Le gabarit est dans `skills/kickstart-vault/assets/hooks/hooks.conf`.

## Principes de conception

- **On pose le cadre, pas le contenu.** Les skills génèrent structure, schémas et fiches vides. Le contenu entre par l'usage.
- **Lazy-pull.** Une note entre dans le vault quand un besoin la tire, pas en bloc le premier jour.
- **Chaque dossier a un consommateur.** Une area sans lecteur est signalée à sa création.
- **Gouvernance d'abord.** Périmètre, données sensibles et accès des agents sont posés au scaffold.
- **Sources déclarées.** Les connecteurs vivent dans `_Meta/sources.md`. Un skill utilise la source déclarée et dégrade proprement si elle manque.
- **Une information à un seul endroit.** Le suivi d'un projet vit dans sa fiche, pas dans le dépôt de code. Les sources externes sont référencées, jamais copiées.

## Installation manuelle (sans plugin)

```bash
git clone https://github.com/lightpoichich/vault-skills.git
cp -R vault-skills/skills/* ~/.claude/skills/
```

Puis relancer Claude Code. Les hooks ne sont pas installés par cette voie.

## Attribution

`vault-skill-creator` est une adaptation du `skill-creator` officiel d'Anthropic (marketplace claude-plugins-official) : placement automatique dans le vault, étape « sources de données », évaluation rendue optionnelle. Le moteur et les scripts d'origine sont conservés. Licence dans `skills/vault-skill-creator/LICENSE.txt`.

Construit par [Lucas Clément](https://devlc.co), delivery de produits digitaux et accompagnement Claude Code pour dirigeants.
