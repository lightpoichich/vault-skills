# Référence technique

Cette page complète le [README](../README.md) pour la personne qui installe, règle ou fait évoluer le plugin. Elle décrit les hooks, leurs réglages, la liaison entre un dossier de travail et sa fiche projet, et la description de chaque skill.

## Dépendances

- **bash et python3** : les hooks et le script `hooks/vault-resolve.py` en dépendent. `jq` n'est pas requis.
- **git** : nécessaire pour relier un dépôt de code à sa fiche par `repo:`. Un dossier sans git se relie par `dossier-travail:`.

## Mise à jour automatique

Claude Code coupe par défaut la mise à jour automatique des marketplaces qui ne viennent pas d'Anthropic, et un plugin ne peut pas l'activer pour ses utilisateurs. Le réglage se pose une fois, en session (`/plugin`, onglet **Marketplaces**, `vault-skills`, **Enable auto-update**, qui écrit `autoUpdate` dans `~/.claude/plugins/known_marketplaces.json`), ou par `"autoUpdate": true` sur l'entrée `vault-skills` d'`extraKnownMarketplaces` dans `~/.claude/settings.json`, prioritaire. `installer` vérifie ce réglage en lecture seule en fin d'installation et guide le dirigeant s'il manque. Source : code.claude.com, « Plugin loading reference », section « When auto-update runs », consultée le 28/10/2026.

## Installation manuelle

```bash
git clone https://github.com/lightpoichich/vault-skills.git
cp -R vault-skills/skills/* ~/.claude/skills/
```

Relancer ensuite Claude Code. Cette voie installe les skills seuls. Les quatre hooks et le script `hooks/vault-resolve.py` ne sont pas installés, et `installer` reste invocable par `/installer`. Les skills localisent alors le vault en remontant jusqu'à un dossier `_Meta/`, ou par le chemin déclaré dans `~/.claude/CLAUDE.md`.

## Cycle de vie d'un vault

Les skills couvrent trois phases. L'installation se fait une fois, par la commande `/second-cerveau:installer`, que Claude ne lance jamais de lui-même. L'usage quotidien suit une boucle ouverte le matin par `brief-du-jour` et refermée en fin de session par `sync-vault`, que le rappel de fin de tour déclenche le plus souvent. L'entretien répond à un événement, à l'exception d'`audit-vault`, prévu en rituel mensuel et rappelé par le bilan de démarrage.

| Phase | Skill | Déclencheur | Résultat |
|---|---|---|---|
| Installation | `installer` | commande `/second-cerveau:installer` dans le dossier du futur vault | entretien, plan validé dans `00-Inbox/plan-vault.md`, puis arborescence PARA, Schema, gouvernance, persona Chief of Staff (`cos`), puis rapatriement facultatif de l'historique (projets Claude.ai, exports de notes) par le mode lot de `ranger` |
| Installation et usage | `assistants` | besoin d'un assistant, ou routine récurrente d'une persona | persona dans `_personas/{slug}/`, ou skill rangé dans la persona ou à la racine du vault |
| Usage quotidien | `brief-du-jour` | le matin, depuis `cos` | brief daté : priorités, alertes, agenda, todos, éléments à valider |
| Usage quotidien | `ranger` | note, URL ou document à ranger ; dossier, archive ou export Claude.ai ; pratique répétée au moins deux fois | note classée dans la zone PARA adéquate ; lot importé après validation d'un manifeste ; trame réutilisable dans `30-Resources/` |
| Usage quotidien | `structurer` | ouverture, évolution ou fin d'un projet ou d'une area | fiche créée ou complétée, area renommée, scindée ou fusionnée, projet ou area archivé |
| Usage quotidien | `sync-vault` | fin de session dans le vault ou dans un dossier de travail relié | décisions, statuts et todos répercutés dans les fiches ; depuis un dossier de travail, dans la seule fiche projet |
| Entretien | `audit-vault` | rituel mensuel | rapport daté dans `00-Inbox/`, puis traitement par lots après validation |

`brief-du-jour` ne figure pas dans `skills/`. Il est livré dans les assets d'`installer`, qui le dépose dans la persona Chief of Staff à l'installation. Il ne s'active que depuis cette persona.

## Travail depuis un dossier de travail

Les skills d'usage quotidien fonctionnent aussi depuis un dossier situé hors du vault : le dépôt de code d'un projet client, ou un dossier sans git (OneDrive, Documents). Le script `hooks/vault-resolve.py` localise le vault et la fiche projet correspondante, en lecture seule.

- **Localisation du vault** : le script lit d'abord les `@imports` du `CLAUDE.md` du dossier et de ses dossiers parents, puis les `@imports` et les chemins absolus cités dans `~/.claude/CLAUDE.md`, puis `~/vault`.
- **Localisation de la fiche projet** : dans `10-Projects/`, le script retient d'abord la fiche dont le champ `repo:` correspond au remote `origin` du dépôt, puis celle dont le champ `dossier-travail:` contient le dossier ou un de ses parents, puis, dans un dépôt git seulement, celle dont le slug correspond au nom du dossier. Hors git, seul `dossier-travail:` relie : un dossier nommé comme une fiche ne s'y relie pas par hasard.
- **Liaison** : `structurer` pose les champs `repo:` et `dossier-travail:` dans la fiche. Un projet situé dans un sous-dossier du dépôt porte le suffixe `#sous-dossier`, par exemple `https://github.com/org/repo#apps/api`.
- **Plusieurs postes** : `dossier-travail:` accepte une liste, un chemin par poste, par exemple `dossier-travail: [/Users/x/OneDrive/Client, /mnt/c/Users/x/OneDrive/Client]`. Lancé depuis un nouveau poste, `structurer` ajoute le chemin courant. Un chemin égal au dossier personnel ou à l'un de ses parents est ignoré.

## Hooks du plugin

Le plugin installe quatre hooks, actifs dans toute session Claude Code. Hors d'un vault ou d'un dossier relié à un vault, ils ne produisent rien.

| Hook | Événement | Rôle |
|---|---|---|
| `vault-health.sh` | démarrage de session | injecte un bilan de santé dans le contexte (notes d'Inbox anciennes, notes sans `type`, fiches au-dessus de leur budget de taille, mémoire native au-dessus de son budget ou au contenu sensible apparent, dernier audit trop ancien, mise à niveau du vault disponible) et supprime les fichiers `.DS_Store` |
| `vault-approve-imports.sh` | démarrage de session | approuve pour le dossier courant les imports du vault, que Claude Code ignorerait sinon comme imports externes |
| `vault-note-guard.sh` | après l'écriture d'une note | renseigne `created` et `updated` dans un frontmatter existant, signale un frontmatter absent ou un nom de fichier hors kebab-case |
| `vault-sync-nudge.sh` | fin de tour | demande une fois `sync-vault` depuis le vault ou depuis un dossier de travail relié, quand les seuils de volume et de durée sont atteints ; un `sync-vault` lancé à la main, ou une fiche projet écrite directement depuis son dossier de travail, repart les seuils à zéro ; aucun rappel depuis un worktree git lié |

### Réglages des hooks

Les réglages se placent dans `{vault}/_Meta/hooks.conf`. `installer` y copie le gabarit `skills/installer/assets/hooks/hooks.conf`.

- **`EXCLUDE`** : chemins du vault ignorés par le bilan de santé et par le garde-fou d'écriture.
- **`INBOX_STALE_DAYS`** : ancienneté, en jours, à partir de laquelle une note d'Inbox est signalée (14 par défaut).
- **`APPROVE_EXTERNAL_IMPORTS`** : la valeur `0` désactive l'approbation automatique des imports.
- **`SYNC_MIN_KB`** et **`SYNC_MIN_MINUTES`** : seuils du rappel de synchronisation, 40 Ko de transcript et 20 minutes depuis la dernière synchronisation par défaut. Les deux seuils doivent être atteints.
- **`SYNC_NUDGE`** : la valeur `0` supprime le rappel, la valeur `vault` le limite aux sessions ouvertes dans le vault.
- **`AUDIT_REMINDER_DAYS`** : délai, en jours, au-delà duquel le bilan de santé signale le dernier rapport `audit-vault-{date}.md` (30 par défaut, `0` coupe le rappel). Sans aucun rapport, le délai court depuis la première session ouverte sur ce vault par la machine.
- **`UPGRADE_REMINDER`** : la valeur `0` coupe le signal de mise à niveau disponible (fiche d'installation `_Meta/installation.md` absente, ou unité remplaçable, en fusion ou nouvelle, ou migration en attente). Voir « Mise à niveau des vaults installés ».
- **`JOURNAL_ROTATION`**, **`JOURNAL_MAX_KB_{TYPE}`**, **`JOURNAL_MAX_KB`**, **`JOURNAL_SECTIONS`**, **`JOURNAL_KEEP`** : rotation des journaux de fiche, voir plus bas. Sans ces clés : rotation coupée, 20 Ko pour une area, 30 Ko pour un projet, section `Journal`, 5 entrées gardées. Le gabarit `hooks.conf` de `installer` pose `JOURNAL_ROTATION=1` : un nouveau vault a la rotation active.
- **`MEMORY_MAX_LINES`**, **`MEMORY_MAX_KB`**, **`MEMORY_CURATION_DAYS`** : budget de l'index de la mémoire native (120 lignes et 16 000 caractères par défaut, environ 60 % du plafond de Claude Code) et délai de curation complète (30 jours). Voir plus bas.
- **`SYNC_NUDGE_WORKTREES`** : la valeur `1` rétablit le rappel dans les worktrees git liés. Par défaut, les sous-agents qui traitent des tickets en parallèle dans des worktrees ne reçoivent pas de rappel, et l'orchestrateur synchronise une seule fois depuis le checkout principal.

### Rotation des journaux de fiche

Une fiche d'area ou de projet tient son état courant dans ses sections ordinaires et son récit daté dans `## Journal`, en ajout seul. Quand elle dépasse son budget de taille, `hooks/vault-journal.py` sort les entrées les plus anciennes, mot pour mot, vers `{dossier de la fiche}/journal/{slug}-{AAAA}-T{n}.md`, et tient l'index `## Journaux` en fin de fiche. Le script n'utilise pas de modèle de langage.

- **Commandes** : `vault-journal.py check` liste les fiches au-dessus du budget : `blocked` dit ce qui empêche d'y revenir, `warnings` ce qui reste signalé sans bloquer. `vault-journal.py rotate {fiche}` simule ; `--apply` écrit, et seulement si `JOURNAL_ROTATION=1` (ou `--force`). `vault-journal.py verify --before {copie} --after {fichiers}` vérifie qu'aucune ligne n'a été perdue. `--loose` tolère un titre d'étiquette de structure renommé (Suivi, Réunions, Notes…) et une ligne d'au moins 12 caractères complétée sur place ; une ligne plus courte doit se retrouver à l'identique.
- **Ce qui bouge** : une entrée est une puce de premier niveau avec ses sous-lignes, ou un bloc `###`. Seules les sections listées dans `JOURNAL_SECTIONS` sont rotables. La date d'une entrée est celle qui ouvre sa ligne de tête, avec l'année (`AAAA-MM-JJ` ou `JJ/MM/AAAA`). Une entrée sans cette date (absente, sans année, placée plus loin dans le titre, ou à plus d'un an de ses deux voisines) reste dans la fiche et se signale. Une section ne bouge pas si un `###` suit des entrées en puces, si une puce datée apparaît sous un `###`, ou si un paragraphe ou un bloc de code s'intercale en colonne 0 entre deux entrées. Une fiche dont un bloc de code reste ouvert, ou déborde de son entrée, ne bouge pas du tout.
- **Sûreté** : la fiche réduite, entrées réinsérées, doit redonner l'original à l'octet près, et chaque ligne doit se retrouver dans la fiche ou ses journaux. Une copie des fichiers touchés va dans `${XDG_STATE_HOME:-~/.local/state}/second-cerveau/rotation/`. Le contenu de la fiche et des journaux est comparé à la lecture avant le commit, puis après l'écriture sur disque du fichier temporaire, juste avant chaque remplacement : une modification concurrente annule tout, journaux déjà écrits compris. Seule reste la fenêtre de quelques microsecondes entre ce contrôle et le remplacement. L'écriture passe par un fichier temporaire synchronisé sur disque, et garde les droits du fichier remplacé. Dans un vault git, seuls les chemins touchés sont commités, avant et après.
- **Déclenchement** : `sync-vault`, en mode vault, lance la rotation sur les fiches qu'il vient d'écrire. Une planification reste possible, par cron ou par une routine Paseo, en appelant le script du plugin installé :

```bash
PLUGIN="$(python3 -c 'import json,os;d=json.load(open(os.path.expanduser("~/.claude/plugins/installed_plugins.json")));print(d["plugins"]["second-cerveau@vault-skills"][0]["installPath"])')"
python3 "$PLUGIN/hooks/vault-journal.py" rotate --apply --all --vault ~/vault
```

Le chemin du plugin change à chaque version, d'où la lecture de `installPath` plutôt qu'un chemin écrit en dur.

### Mémoire native de Claude Code

Claude Code recharge `MEMORY.md` dans chaque session lancée depuis le même dossier, personas comprises, en le tronquant à 200 lignes et 25 000 caractères. Il y écrit aussi seul en cours de session. `hooks/vault-memory.py` établit l'état de cette mémoire, en lecture seule ; `sync-vault` et `audit-vault` tranchent.

- **Commandes** : `vault-memory.py where` rend le dossier mémoire du dossier courant. `inventory` liste tous les dossiers mémoire de la machine, avec leur part du plafond et les règles répétées d'un dossier à l'autre. `check {dossier}` rend le budget, l'index désynchronisé, les pointeurs vers le vault (cassés, archivés, déplacés vers un seul candidat, ambigus), le sensible apparent (fichier, ligne et type, jamais le contenu ; un pointeur reconnu comme sensible est masqué, la détection restant heuristique), les quasi-doublons et la curation due. `backup {dossier}` copie le dossier dans `${XDG_STATE_HOME:-~/.local/state}/second-cerveau/memoire/`.
- **Depuis le vault** : `sync-vault` cure la mémoire quand `check` signale quelque chose ou tous les 30 jours. Il sauvegarde d'abord, retire le sensible, rend les faits aux fiches et ne laisse qu'un pointeur, et ne retire une règle qu'une fois promue dans sa cible (skill, canon de style, `CLAUDE.md`, gouvernance), sur validation.
- **Depuis un dossier de travail** : `sync-vault` trie seulement la frontière. Une préférence transversale part en « À répercuter », un fait d'état va dans la fiche projet, le sensible est retiré. Rien d'autre n'est supprimé. Le savoir technique d'un dépôt a sa place durable dans `.claude/rules/` du dépôt, hors de ce plugin.
- **Plusieurs machines** : la mémoire est locale par défaut. Pour la partager, poser sur chaque machine `"autoMemoryDirectory": "{vault}/_Meta/memoire"` dans le `.claude/settings.local.json` du vault, non versionné. Dans un dossier de confiance, Claude Code lit ce réglage dans le `settings.local.json` de la racine git, puis dans le `.claude/settings.json` du seul dossier de lancement, puis dans les réglages utilisateur ; une valeur ni absolue ni en `~/` est rejetée. Le `settings.local.json` de la racine couvre donc aussi les sessions lancées depuis une persona. La mémoire est alors publiée et versionnée avec le vault, donc sans aucun sensible. Le plugin ne pose jamais ce réglage.
- **Subagents** : un subagent ne charge pas la mémoire de la session principale. Une persona lancée en subagent reçoit son contexte par son prompt ou par le vault ; son champ `memory` en portée projet range sa mémoire propre dans `{vault}/.claude/agent-memory/{nom}/`.

### Import en lot

Le mode lot de `ranger` s'appuie sur `hooks/vault-inventory.py`, sans modèle de langage :

```bash
python3 hooks/vault-inventory.py scan {dossier ou archive.zip} --vault {vault} --label {nom} --manifeste {vault}/00-Inbox/import-{nom}.md
```

- **Sans vault** : sans `--vault`, l'inventaire se fait seul, sans détection des éléments déjà importés. C'est le cas de l'entretien d'installation, qui lit la mémoire d'un export Claude.ai avant que le vault n'ait son `_Meta/`.
- **Extraction** : une archive est extraite dans `${XDG_STATE_HOME:-~/.local/state}/second-cerveau/import/{lot}/`, hors du vault, en refusant les chemins absolus et les remontées. Un dossier est lu en place.
- **Export Claude.ai** : reconnu sous ses deux formes, archive unique ou dossier réunissant le manifeste et une archive par catégorie (`projects`, `memories`, `conversations`, `light_metadata`). Découpé en un fichier markdown par projet (description, instructions, mémoire du projet, liste des documents), par document de connaissance, par fichier de mémoire hors projet et par conversation (résumé, messages, outils nommés, sans la réflexion interne). Le manifeste, qui porte les liens de téléchargement, est écarté. Lecture tolérante d'un format non documenté.
- **Clés** : `{label}:{chemin relatif}` pour un fichier, `claude:projet:{uuid}`, `claude:document:{uuid}`, `claude:conversation:{uuid}`, `claude:memoire:{chemin}` pour un export Claude.ai. La clé est posée en `source:` de la note écrite, ou en sous-ligne `source :` d'une entrée de journal. Une clé déjà présente dans le vault marque l'élément comme importé ; un même `--label` est donc requis pour relancer un lot.
- **Signalements** : doublons de contenu dans le lot, éléments vides, éléments au-delà de `--max-mb` (20 par défaut), noms de fichier évoquant une donnée sensible (indice à juger, pas une détection).
- **Sorties** : `inventaire.json` dans le dossier du lot, résumé sur la sortie standard, squelette du manifeste dans le vault. Un manifeste existant n'est réécrit qu'avec `--force` : il porte l'état du lot.

### Mise à niveau des vaults installés

`hooks/vault-upgrade.py` apporte à un vault installé les changements des gabarits d'`installer`, sans modèle de langage. Procédure complète : `skills/installer/references/mise-a-niveau.md`.

- **Commandes** : `check` rend l'état en JSON (`--summary` : une ligne, rien s'il n'y a rien à faire). `stamp`, `apply` et `accept {unité}` simulent par défaut et écrivent avec `--apply`.
- **Fiche d'installation** : `_Meta/installation.md` (`type: moc`) porte la version du plugin intégrée, les migrations appliquées et, par unité, l'empreinte du gabarit intégré. `installer` la pose en dernière écriture de la phase de structure.
- **Unités** : copies telles quelles (`_personas/cos/.claude/skills/brief-du-jour/`, `_Meta/hooks.conf`) et blocs entre `<!-- socle second-cerveau : début {id} -->` et `<!-- socle second-cerveau : fin {id} -->` (`CLAUDE.md` racine, `_Meta/Schema.md`, `_personas/cos/CLAUDE.md`). Le texte hors balises n'est jamais lu ni touché. `capacites-a-construire.md` n'est pas géré.
- **Cas** : à jour, remplaçable (jamais modifié depuis l'intégration, gabarit changé), personnalisé, fusion à proposer (modifié et gabarit changé, jamais écrit par le script), nouveau, absent, retiré du gabarit, inconnu (pas d'empreinte), balises absentes. `apply` ne remplace que le remplaçable et ajoute le nouveau, après copie des fichiers touchés dans `${XDG_STATE_HOME:-~/.local/state}/second-cerveau/mise-a-niveau/`. `accept` déclare une fusion faite, ou une version personnelle conservée.
- **Migrations** : déclarées dans le script (identifiant, version, contrôle, action), idempotentes, inscrites dans la fiche d'installation. `5.0.0-noms-skills` réécrit les noms retirés, entre accents graves, dans le `CLAUDE.md` racine, ceux des personas et les fichiers des skills du vault ; sa table concorde avec celle d'`audit-vault`, vérifiée par les tests.
- **Vault sans fiche d'installation** : la première mise à niveau note intégrées les unités identiques au gabarit, laisse les autres inconnues et n'écrase rien.

### Synchronisation git d'un vault partagé

`skills/installer/assets/hooks/vault-git-sync.sh` est un gabarit facultatif, distinct des hooks du plugin. Il synchronise par git un vault partagé entre un poste de travail et une machine sans écran qui exécute des agents. Il fait un pull au démarrage de session, un commit local en fin de tour, et un push déclenché par un minuteur externe. Il ne s'exécute que sous Linux. `installer` le propose quand le plan du vault mentionne une telle machine, et son installation dans `{vault}/.claude/hooks/` se fait à la main.

## Principes de conception

- **Structure d'abord** : les skills génèrent l'arborescence, les schémas et des fiches vides. Le contenu entre dans le vault par l'usage.
- **Import à la demande** : une note entre dans le vault quand un besoin concret la justifie. Le vault n'est pas rempli en bloc au démarrage.
- **Un lecteur par dossier** : chaque area doit avoir un consommateur identifié. Une area sans consommateur est signalée dès sa création.
- **Gouvernance à l'installation** : le périmètre, les données sensibles et les accès des agents sont fixés à la création du vault.
- **Sources déclarées** : les connecteurs disponibles sont listés dans `_Meta/sources.md`. Un skill utilise les sources déclarées et produit un résultat réduit quand l'une d'elles manque. Le pack fonctionne sans aucun connecteur.
- **Information unique** : une information vit à un seul endroit. Le suivi d'un projet est tenu dans sa fiche du vault, et le dépôt de code n'en porte pas de copie. Les sources externes sont référencées par lien.

## Descriptions des skills

Chaque entrée reprend mot pour mot la description du `SKILL.md`, c'est-à-dire le texte que Claude Code lit pour décider de lancer le skill. Les formulations entre guillemets sont des exemples de demandes qui le déclenchent. Les skills d'usage quotidien lisent `_Meta/sources.md` et utilisent les connecteurs qui y sont déclarés.

<!-- SKILLS:BEGIN -->
### Installation

- **`installer`** : Installe un second cerveau en une commande, dans le dossier du futur vault : entretien de cartographie de l'activité, plan à valider, puis structure du vault (arborescence PARA, Schema, gouvernance, fiches vides, persona Chief of Staff et son brief), encarts du CLAUDE.md global posés avec accord, puis rapatriement facultatif de l'historique (projets Claude.ai, exports de notes). Reprend là où l'installation s'est arrêtée. Se lance par la commande /second-cerveau:installer.
- **`assistants`** : Construit l'équipe d'assistants du vault : crée une persona (rôle, périmètre de lecture et d'écriture, garde-fous, raccourci terminal, backlog de routines) après une découverte du quotidien, puis lui ajoute une compétence, un skill placé dans la persona ou à la racine du vault avec ses sources de données. S'utilise quand l'utilisateur dit « crée-moi un agent », « nouvelle persona », « je veux un assistant RH », « crée un skill pour mon Chief of Staff », « encode mon triage-mails », ou pioche dans capacites-a-construire.md. Pour installer le vault, voir /second-cerveau:installer.

### Usage quotidien

- **`brief-du-jour`** : Produit le brief du jour dans 00-Inbox/briefs/{date}.md (Priorités, Alertes, Agenda, Todos, À valider) à partir du vault et des sources déclarées dans _Meta/sources.md, en dégradant proprement si une source manque. S'utilise quand l'utilisateur dit « mon brief », « le point du matin », « qu'est-ce que j'ai aujourd'hui ». Pour faire entrer une note, voir ranger.
- **`ranger`** : Fait entrer un savoir dans le vault et le classe dans la bonne zone PARA, avec frontmatter conforme au Schema et wikilinks : un contenu externe, un lot entier (dossier, archive, export Claude.ai) validé en une fois, ou une pratique répétée généralisée en trame. Renvoi plutôt que copie pour le sensible. S'utilise quand l'utilisateur dit « importe cette note », « range cette page Notion », « ajoute ça à mon projet X », « importe ce dossier », « rapatrie mes projets Claude », « reprends l'import », « fais-en une trame ». Pour mettre à jour les fiches après une session, voir sync-vault.
- **`structurer`** : Crée et fait évoluer les contenants du vault, projets et areas : pose une fiche conforme au Schema, complète un shell vide, relie un projet à son dossier de travail, renomme, scinde, fusionne ou archive. S'utilise quand l'utilisateur dit « créer le projet X », « lancer un nouveau projet », « ouvrir un chantier », « complète le projet X », « archive ce projet », « crée une area », « renomme / scinde / fusionne l'area X », « je ne m'occupe plus de X ». Pour faire entrer une note ou un document, voir ranger.
- **`sync-vault`** : Met à jour et consolide les fiches du vault à partir de la conversation en cours. Depuis le vault : décisions, statuts, todos, sections « À répercuter », sas 00-Inbox/_drafts/ et mémoire native de Claude Code. Depuis un dossier de travail relié à un projet, dépôt de code ou dossier sans git : la seule fiche projet, le reste déposé en « À répercuter ». Agit sans validation et réécrit plutôt qu'empiler. S'utilise quand l'utilisateur dit « sync le vault », « sync le projet », « mets à jour la fiche projet », « répercute ce qu'on a décidé », ou sur rappel du hook Stop en fin de tour.

### Entretien

- **`audit-vault`** : Contrôle technique d'un vault Obsidian PARA : wikilinks cassés, orphelines, frontmatter hors Schema, nommage, Inbox stale, projets à archiver, areas mortes, personas invalides, fiches trop lourdes, mémoire native de Claude Code. Produit un rapport daté dans 00-Inbox/ puis propose le traitement par lots, sans écrire avant validation. S'utilise quand l'utilisateur dit « audit du vault », « fais le ménage », « c'est le bazar », « cette fiche est trop lourde », « fais le point sur la mémoire », ou sur rituel mensuel. Pour répercuter la session en cours, voir sync-vault.

<!-- SKILLS:END -->

## Attribution

Le geste « ajouter une compétence » d'`assistants` adapte le `skill-creator` officiel d'Anthropic, publié dans la marketplace `claude-plugins-official`. L'adaptation ajoute le placement automatique dans le vault et une étape « sources de données », et retire la boucle d'évaluation (scripts, agents, visualiseurs) : une mesure chiffrée passe par le `skill-creator` officiel, s'il est installé. La licence figure dans `skills/assistants/LICENSE.txt`.
