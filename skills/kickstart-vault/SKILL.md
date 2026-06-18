---
name: kickstart-vault
description: >-
  Scaffolde un vault Obsidian PARA à partir d'un `plan-vault.md` (la sortie de l'interview
  de cartographie) : génère l'arborescence, `_Meta/Schema.md`, `_Meta/governance.md`, le
  `CLAUDE.md` racine et les shells d'Areas/Projects en *generate-don't-write* (zéro contenu
  inventé). Utilise ce skill dès que l'utilisateur a un `plan-vault.md` (souvent
  `00-Inbox/plan-vault.md`) et veut construire, initialiser, scaffolder ou « monter » son
  vault, sa structure PARA ou son « second cerveau » — ou dit « j'ai mon plan, crée la
  structure », « build my vault », « initialise le vault », « génère l'arborescence ».
  Autoportant et path-agnostique : fonctionne in-place dans n'importe quel dossier vault.
  NE PAS l'utiliser pour mener l'interview de cartographie (qui produit le plan-vault), ni
  pour créer une persona/agent ou démarrer un projet/client : il matérialise un plan-vault
  existant, rien d'autre.
---

# Kickstart Vault

Transforme un **plan** de vault en **vault réel**. C'est la suite directe du skill
`interview-vault` : cette interview a produit `00-Inbox/plan-vault.md` (+ de la matière
première dans `00-Inbox/matiere-premiere/`) ; ce skill **exécute** ce plan.

Le but n'est pas de remplir le vault — c'est d'en poser le **squelette propre et cohérent**
sur lequel l'usage va se greffer. Un vault scaffolté ce skill doit pouvoir tenir des années :
conventions homogènes, gouvernance posée d'emblée, et **rien d'inventé**.

## Pourquoi ces partis pris (à garder en tête tout du long)

- **Generate-don't-write.** On génère des *shells* (frontmatter + titres de sections + une
  ligne de but), jamais du contenu métier. Un vault à moitié vide mais structuré est sain ;
  un vault rempli de fausses fiches (faux incidents, faux ADR, faux comptes-rendus) est un
  mensonge qui pourrit la confiance. *Empty-but-structured beats full-but-fake.*
- **Chaque dossier a un consommateur.** On ne crée pas de structure « au cas où » : chaque
  Area et chaque Project listés dans le plan reçoivent une fiche-shell que des agents pourront
  lire et écrire, et vers laquelle les wikilinks résolvent.
- **Gouvernance avant la donnée.** On pose `_Meta/governance.md` (périmètre, ce que les
  agents peuvent lire/écrire, confidentialité 🔒, renvoi-jamais-copie) **avant** tout contenu.
  Sur un vault qui touchera du sensible, c'est le garde-fou qui protège toute la suite.
- **Le plan fait foi.** L'arborescence, les Areas, les Projects, les conventions viennent du
  `plan-vault.md` de **cet** utilisateur. On n'impose pas une structure préfabriquée.
- **Autoportant + in-place.** Ce skill ne dépend d'aucun vault tiers : ses gabarits sont dans
  `assets/`. Il scaffolde le **dossier courant** (ou celui qu'on lui donne). Il marche pour
  n'importe quel élève, sur sa machine, sans rien d'extérieur.
- **Non destructif.** Si des fichiers/dossiers existent déjà (ré-exécution), on **complète**,
  on n'écrase jamais sans demander.

## Comment parler au dirigeant (langue)

L'interlocuteur n'est **pas forcément un développeur**, et c'est le **Profil de ton du plan** (curseur
*Vocabulaire*) qui dit jusqu'où aller — pas une supposition. À défaut de profil : zéro tuyauterie.
Deux tiers, à ne pas confondre.

**1. Toujours banni, quel que soit le profil** (même un CTO ne veut pas ça) :
- **Les anglicismes gratuits.** Bannir : *scaffold(er), bundle, alias, quick win, input, deal, mapping,
  shell, lazy-pull, generate-don't-write*. Dire plutôt : installer/monter/poser, ensemble prêt-à-
  l'emploi, raccourci (de lancement), gain rapide, matière/informations, affaire, correspondance,
  fiche vide structurée, « au fil des besoins », « on pose le cadre, pas le contenu ».
- **Les termes internes de ce SKILL** (*shell, bundle, generate-don't-write, idempotent, skill caché,
  asset figé*) sont pour toi, le modèle — **jamais répétés** au dirigeant. Ce sont eux qui ont fait
  déraper la narration testée (« je copie le **bundle figé**, y compris le **skill caché** » ; « l'alias
  `cos`, chemin absolu, **idempotent** »).
- **Pas de jargon dans un NOM de fichier livré** (`compte-rendu-installation.md`, pas `scaffold-report.md`).

**2. Calibré sur le curseur *Vocabulaire* du plan** — combien de **structure interne** tu surfaces :
PARA, `_Meta`, `Schema`, `frontmatter`, `slug`, chemins de fichiers, « couche ». Au profil *zéro
jargon* (défaut), tu **n'en nommes aucun** ; au profil *termes techniques OK*, tu peux. Dans tous les
cas : un terme de structure conservé = **expliqué une fois** puis réutilisé (`frontmatter` = l'en-tête
d'une note ; `wikilink` = un lien `[[…]]` ; `persona` = un assistant spécialisé).

**Narrer le résultat et la valeur, pas l'étape technique en direct.** Le dirigeant n'a pas besoin du
commentaire du chantier. Avant → après (profil zéro jargon) :
- ❌ « Maintenant la **couche `_Meta`** — le contrat qui tient le vault. Je génère le **Schema**. »
  → ✅ « Je pose les règles qui garderont ton espace cohérent dans le temps. »
- ❌ « **Squelette PARA posé** (generate-don't-write : shells structurés) : **6 Areas** en `{slug}/{slug}.md`. »
  → ✅ « Ton espace est en place : tes 6 domaines de responsabilité, prêts à se remplir au fil de l'usage. »
- ❌ « Je pose l'**alias terminal `cos`** (chemin absolu, idempotent). »
  → ✅ « J'ajoute un raccourci : tu lanceras ton assistant en tapant `cos`. »

## Entrées attendues

1. **`plan-vault.md`** — requis. Par défaut `00-Inbox/plan-vault.md` dans le dossier courant.
   S'il est ailleurs, demander le chemin. **S'il n'existe pas**, ne pas inventer : indiquer
   à l'utilisateur de lancer d'abord le skill **`interview-vault`** (l'interview de cartographie
   qui produit ce plan).
2. **`00-Inbox/matiere-premiere/`** — optionnel mais précieux. Les fichiers bruts de
   l'interview (`contexte.md`, `themes-actuels.md`, `notes-actuelles.md`, `sources-equipe.md`,
   `outillage-actuel.md`, `chantiers-en-cours.md`). On les **lit pour le contexte** (remplir
   le `CLAUDE.md` racine, calibrer la gouvernance), jamais pour les recopier en fiches.

Le format exact d'un `plan-vault.md` et des fichiers de matière première est décrit dans
`references/plan-vault-format.md` — **le lire avant de parser** si le plan dévie du gabarit
attendu.

## Procédure

### 1. Localiser et lire les entrées
- Trouver le `plan-vault.md` (cwd `00-Inbox/` par défaut). Confirmer que le dossier courant
  est bien la racine du vault à scaffolder.
- Lire le plan **en entier**. Lire `00-Inbox/matiere-premiere/*` s'il existe.
- Repérer les sections du plan : *Arborescence proposée*, *Projects*, *Areas*, *Resources*,
  *Conventions frontmatter*, *Mapping sources*, *Compétences à construire (skills) → personas*,
  *Top 5 irritants*, et une éventuelle section *Gouvernance / isolation*.

### 2. Passe de cohérence (rapide, non bloquante)
- Vérifier le piège **Area-as-Project** : une « Area » avec une date de fin / un livrable
  unique est probablement un Project (et vice-versa). Le **signaler** à l'utilisateur, ne pas
  trancher d'autorité — le plan reste la source de vérité.
- Si une section attendue manque (ex. pas de conventions frontmatter, pas de gouvernance),
  prévoir un **défaut raisonnable** (cf. assets) et le **marquer** comme « généré par défaut,
  à valider » dans le rapport final. Ne jamais bloquer.

### 3. Créer l'arborescence (exactement celle du plan)
- Reproduire le bloc *Arborescence proposée* du plan : `10-Projects/`, `20-Areas/{areas}`,
  `30-Resources/{sous-zones}`, `40-Archive/`, `_Meta/`, et `00-Inbox/` (déjà là).
- Ajouter `_personas/` (dossier des personas). Il **ne reste pas vide** : l'étape 10bis y pose une
  persona **Chief of Staff** par défaut (la lentille généraliste, livrée avec le skill
  `brief-du-jour`) — un exemple amorcé que le dirigeant lance tout de suite, et qu'il duplique
  ensuite via `kickstart-persona` pour ses autres rôles.
- Tous les noms en **kebab-case**.

### 4. Générer la couche `_Meta` (la première qui compte)
- **`_Meta/Schema.md`** — depuis `assets/schema-template.md`, en ne gardant que les types
  présents dans la section *Conventions frontmatter* du plan (project, area, meeting, adr,
  brief, incident, draft, resource, moc…) et en reprenant leurs champs. C'est le contrat qui
  garde le vault cohérent dans le temps. **La liste du gabarit n'est pas fermée** : si le plan
  déclare un **type métier** absent du gabarit (ex. `reporting`, `dossier`, `veille`), le **reprendre
  tel quel** — ne jamais l'écarter au motif qu'il n'est pas pré-rédigé. Lui donner un bloc minimal
  (`type` + `tags` + les champs nommés au plan). Ne pas dupliquer un type sous un autre nom.
- **`_Meta/governance.md`** — depuis `assets/governance-template.md`. Reprendre la section
  *Gouvernance / isolation* du plan si elle existe ; sinon la **synthétiser** depuis les
  signaux (données sensibles de la matière première). Ce fichier pose des **règles durables**,
  pas un instantané : périmètre du vault, convention 🔒 confidentiel, **renvoi-jamais-copie**,
  refus par défaut sur le sensible. **Ne nommer AUCUN agent dans ce fichier** — ni tableau, ni
  liste, ni parenthèse type « (agents prévus : …) ». Toute mention d'agents se périme dès qu'on
  en ajoute/retire un. Le périmètre lecture/écriture **concret** de chaque agent vit dans son
  propre `_personas/{slug}/CLAUDE.md` (source de vérité, mise à jour là où l'agent vit) ;
  `governance.md` ne fait que **pointer** vers cette règle, sans citer d'agent.
- **`_Meta/sources.md`** — depuis `assets/sources-template.md`. C'est le **registre des connecteurs**
  du dirigeant : la table que les skills (`brief-du-jour`, `import-note`, et tout skill généré
  ensuite) lisent pour savoir d'où tirer leurs informations. **Toujours poser la ligne `vault`** (socle,
  toujours joignable). Pour chaque source nommée dans le *Mapping sources* du plan, ajouter une ligne
  (`type` cloud/local, `statut`, `usage`) ; une source sensible passe en `renvoi 🔒`.
  - **`statut` = `à brancher` par défaut.** Ne poser `actif` **que si** le plan atteste explicitement
    que le connecteur est **déjà branché et joignable**. Qu'une source soit *nommée* (l'activité s'en
    sert) ne veut pas dire que son **connecteur** (MCP, API) existe dans la session : `actif` signifie
    **connexion vérifiée**, pas « source qui existe ». Au moindre doute → `à brancher`. Un registre qui
    ment (`actif` pour un connecteur fantôme) casse la cascade des skills (« déclaré + joignable →
    l'utiliser » devient faux) ; un `à brancher` trop prudent coûte juste un collage manuel que le
    dirigeant lève en passant la ligne à `actif` une fois branché. On erre **du côté sûr**.
  - **Generate-don't-write** : n'inscrire aucune source que le plan ne nomme pas. Si le plan n'a pas de
    *Mapping sources*, ne poser que la ligne `vault` et le signaler dans le rapport (le dirigeant — ou un
    skill, à la première exécution — complétera quand il branchera ses connecteurs).
  - **Colonne `accès` optionnelle** (heuristique « comment requêter étroit » : `scoper par date`,
    `filtrer par projet`…). La laisser **vide** (`—`) sauf si le plan atteste une heuristique claire :
    elle se remplit par l'usage, jamais par invention, et ne porte **jamais le schéma** de la source.
- **`_Meta/derivation.md`** — depuis `assets/derivation-template.md`. C'est le **« pourquoi »** du
  vault : il trace sa forme (PARA, *ses* Areas/Projects, ses règles d'écriture, le CoS par défaut) à
  ce que le dirigeant a décrit à la cartographie. Là où Schema/governance/sources disent **ce que sont**
  les règles, lui dit **pourquoi** elles sont là — ce qui rend l'espace explicable au dirigeant et
  guide ses choix le jour où il voudra le faire évoluer. **Generate-don't-write tient toujours** : la
  rationale *universelle* (pourquoi PARA, pourquoi le vide-structuré) explique le **système**, elle
  n'invente aucun contenu métier ; les parties *spécifiques* ({tes domaines}, {ta posture 🔒}) sont
  **reprises du plan**, jamais inventées — si le plan ne dit rien sur un point, laisser le placeholder
  ou retirer la ligne, ne pas broder. **Langage simple, calibré sur le curseur *Vocabulaire*** comme
  tout le reste : ce fichier est lu par le dirigeant, son but est pédagogique — zéro jargon interne.
  Le principe : **le vault embarque sa propre justification**, tenue **courte** à dessein. À la fin du
  fichier, la section *Faire évoluer* renvoie aux bonnes compétences (`nouveau-projet`, `gerer-area`,
  `kickstart-persona`, `interview-vault`).

### 5. Générer le `CLAUDE.md` racine (mécanique du vault, pas la bio)
- Depuis `assets/vault-claude-template.md`. Court. Il porte la **mécanique du vault** : une ligne
  de périmètre (reprise du plan), la carte du vault, les conventions (kebab-case, wikilinks
  **+ comment les suivre**, frontmatter), la règle **generate-don't-write**, et les `@imports`
  de `_Meta/Schema.md`, `_Meta/governance.md` et `_Meta/sources.md` — les **contrats** que l'agent
  doit suivre à chaque session. **Ne PAS `@importer` `_Meta/derivation.md`** : c'est le *pourquoi*
  (pédagogique, consulté à la demande), pas un contrat opérationnel — l'imposer à chaque session
  coûterait des tokens pour rien. Il est seulement **listé** dans la carte du vault.
- **Section `## Ton`** : remplir les 4 curseurs depuis la section *Profil de ton* du plan, en
  reprenant les mots du dirigeant. **Si le plan ne l'a pas** (passe de ton non faite), poser le
  **défaut prudent** — *métier sans jargon · concis · propose, je valide · sobre + tutoiement,
  acquiesce* — et le marquer « généré par défaut, à valider » dans le compte-rendu (étape 11). Ce
  ton est hérité par le CoS et toute persona ; c'est ce qui calibre la narration (voir la règle de
  langue ci-dessous). C'est la **seule** part « personne » que porte ce fichier, à dessein.
- **Ne pas** y mettre la bio/identité de l'utilisateur (rôle, taille d'équipe, enjeux perso) :
  ça change peu et c'est valable partout → sa place est le `~/.claude/CLAUDE.md` **global**,
  chargé dans toutes ses sessions. Le CLAUDE.md du vault décrit **le vault, pas la personne**.
  (Le rapport, étape 11, recommandera de verser ce contexte au global.)
- **Carte au niveau PARA strict** : la carte du vault liste les **dossiers de premier niveau**
  (`00-Inbox/`, `10-Projects/`, `20-Areas/`, `30-Resources/`, `40-Archive/`, `_Meta/`,
  `_personas/`) + la nomenclature `{slug}/{slug}.md`. **N'énumère PAS les sous-dossiers
  spécifiques** (ex. pas de « `briefs/` pour les briefs matinaux ») : ils naissent et changent
  avec l'usage, les inscrire dans la carte la fait rôtir. La ligne **Périmètre** ne porte que le
  **scope** (ce que couvre le vault), pas le rôle/identité.

### 5bis. Poser les garde-fous (hooks de santé)
Installer les deux hooks **déterministes** qui maintiennent le vault sain dans le temps. Ce sont
la *couche garantie* qui complète la *couche advisory* du `CLAUDE.md`/`Schema.md` (que le modèle
*essaie* de suivre) : eux s'exécutent **quoi que le modèle décide**, sur des événements du cycle de
vie. Fichiers **génériques** (non dérivés du plan) → on les **copie tels quels** depuis `assets/hooks/`.
- Créer `{vault}/.claude/hooks/`, y copier les 2 scripts (`vault-health.sh`, `vault-note-guard.sh`),
  puis les rendre exécutables (`chmod +x`).
- Installer le bloc `hooks` de `assets/hooks/settings.hooks.json` dans `{vault}/.claude/settings.json`.
  **Non destructif** : si le fichier existe déjà, le **lire et fusionner** la seule clé `hooks` (ne
  jamais écraser des permissions/réglages présents) ; sinon le créer avec ce seul bloc.
  **Idempotent** : à une ré-exécution, **ne pas dupliquer** un hook déjà présent — pour chaque
  événement, n'ajouter l'entrée que si aucune ne pointe déjà vers le même script `vault-*.sh`.
- Les scripts sont **path-agnostiques** (`$CLAUDE_PROJECT_DIR`) et **zéro-config** : rien à
  personnaliser. Dépendances : `bash` + `python3` (présents sur WSL/macOS), pas de `jq`.

Ce que font les hooks (à résumer à l'utilisateur, en non-tech) : un **bilan de santé** au démarrage
(Inbox qui traîne, notes sans `type`, `.DS_Store` purgés) ; un **garde-fou à l'écriture** (dates
`created`/`updated` posées seules, rappel si frontmatter absent ou nom hors kebab-case).
Ce sont des **nudges + auto-fix inertes** : jamais de blocage d'action, jamais de suppression de contenu.

### 6. Générer les shells d'Areas
- **Nomenclature stricte** : chaque Area est un **dossier** `20-Areas/{area-slug}/` contenant sa
  **fiche principale** `20-Areas/{area-slug}/{area-slug}.md` — **jamais** une fiche à plat
  `20-Areas/{area-slug}.md`. Le dossier accueillera plus tard les sous-éléments (meetings,
  sources) ; la fiche `{slug}.md` est le point d'entrée et le fil de suivi.
- Fiche depuis `assets/area-shell-template.md`, frontmatter `type: area` rempli depuis le plan
  (objets récurrents, cadence, outils). Corps = titres de sections vides + une ligne de but.
  **Aucun contenu inventé.**

### 7. Générer les shells de Projects
- **Même nomenclature stricte que les Areas** : chaque Project est un **dossier**
  `10-Projects/{projet-slug}/` contenant sa **fiche principale**
  `10-Projects/{projet-slug}/{projet-slug}.md` — **jamais** une fiche à plat
  `10-Projects/{projet-slug}.md`. La fiche `{slug}.md` suit l'avancement du projet ; le dossier
  accueillera ses sources, meetings, livrables.
- Fiche depuis `assets/project-shell-template.md`, frontmatter `type: project` (status, deadline,
  livrable, parties-prenantes, wikilink vers l'Area liée si le plan le précise).

### 8. Resources (légère)
- Créer les sous-dossiers de `30-Resources/` du plan. Dans chaque sous-zone, un `_index.md` qui
  **liste les items du plan en cases à cocher** (TODO de capitalisation). Pour un item **existant
  ailleurs** (un PDF sur Drive, des CGV, une charte), reporter son emplacement tel que le plan le
  donne : `- [ ] {nom} — {usage} — vit aujourd'hui : {emplacement}`. Pour un item « à créer »,
  case simple. Pas de contenu, jamais de copie : la liste se remplit par l'usage (entrée **une par
  une** via l'import, jamais de migration en masse).

### 9. Renvois externes (si mapping sources présent)
- Dans `30-Resources/references-externes/` (le créer si besoin), poser des **renvois-shells**
  pour les sources du *Mapping sources* : un titre + le lien/emplacement + une ligne de
  contexte, **tag 🔒 si sensible**. Jamais de copie du contenu. C'est la matérialisation du
  principe renvoi-jamais-copie.

### 10. Laisser la matière première en place
- Ne pas déplacer ni transformer `00-Inbox/matiere-premiere/` : c'est de la capture brute, elle
  sera tirée vers les fiches au fil de l'usage (lazy-pull). Le skill ne fait que la lire.

### 10bis. Poser la persona Chief of Staff par défaut (lentille généraliste)
Pour qu'un vault fraîchement scaffoldé soit **utilisable tout de suite** — pas un squelette inerte
— on y dépose une persona **Chief of Staff** générique, qui embarque le skill `brief-du-jour`. Deux
bénéfices : le dirigeant lance `cos` et obtient son brief dès la première minute (sur le seul vault,
sans aucun connecteur) ; et `_personas/cos/` lui sert d'**exemple vivant** de la structure du système
(identité + `.claude/skills/` peuplé + backlog), qu'il dupliquera ensuite via `kickstart-persona`.

C'est un **asset figé** : on copie un bundle prêt, on **n'invoque pas** `kickstart-persona` (sa
découverte interactive n'a pas de sens pour un rôle générique) ni `vault-skill-creator` (`brief-du-jour`
existe déjà). Le CoS suit exactement les conventions de `kickstart-persona` pour rester un exemple fidèle.

- **Idempotence** : si `_personas/cos/` existe déjà (ré-exécution, ou CoS créé à la main), **ne pas
  écraser** — compléter ce qui manque et le signaler dans le rapport. Sinon, le créer.
- **Copier le bundle** `assets/persona-chief-of-staff/` → `{vault}/_personas/cos/`, **y compris** le
  dossier caché `.claude/skills/brief-du-jour/` (le skill complet voyage avec la persona). Le
  `CLAUDE.md` du CoS est posé **tel quel** : ses zones sont au niveau PARA (lit large, écrit étroit),
  génériques, donc valables pour n'importe quel dirigeant — rien à dériver du plan, rien d'inventé.
  Il hérite du `CLAUDE.md` racine du vault (carte, conventions, Schema).
- **Poser l'alias terminal `cos`** (même mécanique que `kickstart-persona` : chemin **absolu**,
  idempotent, détection du shell). La racine absolue du vault est celle scaffoldée à l'étape 1.
  ```bash
  VAULT_ABS="$(pwd)"                                  # racine du vault (cf. étape 1)
  RC="$HOME/.zshrc"; [ -n "$BASH_VERSION" ] && RC="$HOME/.bashrc"
  LINE="alias cos=\"cd '$VAULT_ABS/_personas/cos' && claude\""
  grep -q "alias cos=" "$RC" 2>/dev/null || echo "$LINE" >> "$RC"
  ```
  C'est la **seule** écriture hors du vault que fait ce skill — la signaler dans le rapport (étape 11).
- **Persona-porté, pas global** : `brief-du-jour` n'est actif que **lancé depuis le CoS**
  (`cd _personas/cos && claude` charge son `.claude/skills/`). Depuis la racine du vault ou une autre
  persona, il ne se déclenche pas — c'est voulu : le brief est le battement du Chief of Staff.

### 11. Écrire le compte-rendu d'installation
- Créer `00-Inbox/compte-rendu-installation.md` : l'arbre créé, ce qui a été **généré par défaut à
  valider**, les points où le plan disait « à creuser », et les **prochaines étapes** :
  *ne pas remplir les fiches à la main → le contenu entre au fil des besoins (les shells de Projects
  se complètent au fil de l'eau avec `nouveau-projet` : invariants manquants + contexte réel
  rattaché ; les Areas évoluent ensuite — naître, compléter, renommer, scinder, archiver — avec
  `gerer-area`) ; donner ses
  **compétences** au Chief of Staff via `vault-skill-creator` (en partant des compétences listées au
  plan) ; ne créer une **nouvelle persona** (`kickstart-persona`) que si une compétence réclame ses
  propres zones, sa propre voix ou ses propres garde-fous ; les **documents de référence repérés à
  l'interview** sont listés (avec leur emplacement) dans les `_index.md` de `30-Resources/` — les
  faire entrer **un par un, au moment où on en a besoin**, avec `import-note`, jamais tout d'un
  coup.* C'est la règle clé : **une compétence
  s'ajoute à une persona existante ; on ne crée pas une persona par compétence.**
- **Persona Chief of Staff posée** (étape 10bis) : l'indiquer clairement, avec le **mode d'emploi
  immédiat** — recharger le terminal (`source ~/.zshrc`, ou nouvel onglet) puis taper `cos` et demander
  « fais-moi le brief du jour » : le vault produit son premier brief sur-le-champ, sans aucun
  connecteur. Préciser que `_personas/cos/` est un **exemple** à dupliquer (identité +
  son dossier de compétences `.claude/skills/brief-du-jour/` + sa liste de compétences à construire
  `capacites-a-construire.md`), et que le skill a **ajouté un raccourci de lancement `cos`** au
  fichier de configuration du terminal (`~/.zshrc`/`.bashrc`) — la seule écriture hors du vault.
- **Signaler en une ligne** que `_Meta/derivation.md` a été posé — la note « pourquoi ton espace est
  rangé ainsi », à ouvrir le jour où il se le demande ou avant de changer la structure. Si des parties
  spécifiques (domaines, posture 🔒) ont gardé des **placeholders** faute d'info au plan, les ranger
  dans le lot « généré par défaut, à valider ».
- Y **recommander** de placer le contexte personnel (rôle, enjeux, identité) dans le
  `~/.claude/CLAUDE.md` **global** plutôt que dans le vault, avec un court encart prêt à coller
  (tiré de `matiere-premiere/contexte.md` si présent). **Ne pas** modifier le global soi-même.
- Lister les **garde-fous installés** (hooks H1 bilan de santé / H2 garde-fou écriture) en **une
  phrase en langage simple**, pour que l'utilisateur ne soit pas surpris par les messages
  « Santé du vault… » et sache qu'il n'a rien à lancer.
- Afficher une synthèse à l'utilisateur en fin d'exécution.

## La discipline generate-don't-write, concrètement

Une fiche-shell bien faite, c'est :

```markdown
---
type: area
area: recrutement
objets: [pipeline candidats, fiches de poste, entretiens, closing]
cadence: continu
outils: [Notion]
tags: [area]
---

# Recrutement

> Responsabilité continue : {une ligne reprise du plan}.

## Objets récurrents
<!-- pipeline, fiches de poste, entretiens, closing -->

## Notes
```

Ce qu'on ne fait **jamais** : inventer un candidat, un poste, une décision, un incident, un
chiffre. Si l'info n'est pas dans le plan/la matière première, la section reste vide. Le vide
structuré est honnête et se remplit ; le faux est un piège.

## Cas limites

- **Pas de `plan-vault.md`** → stop : demander de lancer d'abord l'interview de cartographie.
  Ne jamais scaffolder « à l'aveugle ».
- **Plan incomplet** (section manquante) → défauts marqués « à valider », jamais de blocage.
- **Dossier déjà peuplé** (ré-exécution) → compléter ce qui manque, **ne pas écraser** une
  fiche existante sans confirmation explicite ; tout signaler dans le rapport.
- **Beaucoup d'Areas/Projects** → tout générer quand même (ce sont des shells légers), mais
  rappeler dans le rapport le principe « élargir par l'usage » : mieux vaut 3 Areas vivantes
  que 12 dossiers morts.
- **Area-as-Project** détecté → signaler, laisser l'utilisateur trancher.
- **Vault sans enjeu de confidentialité** → garder une `governance.md` légère (périmètre +
  accès agents), ne pas sur-charger en 🔒.

## Transférabilité (pour un élève qui l'utilise seul)

Ce skill est conçu pour être **copié tel quel** dans le `~/.claude/skills/` (ou le
`.claude/skills/` du vault) de n'importe qui. Il ne référence **aucun** vault, nom ou chemin
extérieur : tout vient du `plan-vault.md` de l'utilisateur et des gabarits `assets/`. Quand tu
l'exécutes, n'introduis aucune dépendance à l'environnement de l'auteur — reste path-agnostique
et lis toujours depuis le plan de la personne devant toi.

## Fichiers du skill
- `references/plan-vault-format.md` — structure attendue du `plan-vault.md` et de la matière
  première (à lire pour parser un plan qui dévie du gabarit).
- `assets/schema-template.md` — gabarit du contrat frontmatter `_Meta/Schema.md`.
- `assets/governance-template.md` — gabarit `_Meta/governance.md`.
- `assets/derivation-template.md` — gabarit `_Meta/derivation.md` (le *pourquoi* du vault : trace sa
  forme au plan, renvoie aux compétences d'évolution ; listé dans le `CLAUDE.md` racine mais non `@importé`).
- `assets/vault-claude-template.md` — gabarit du `CLAUDE.md` racine.
- `assets/area-shell-template.md` / `assets/project-shell-template.md` — gabarits de fiches-shells.
- `assets/hooks/vault-health.sh` — hook H1 (`SessionStart`) : bilan de santé + purge `.DS_Store`.
- `assets/hooks/vault-note-guard.sh` — hook H2 (`PostToolUse`) : stamp `created`/`updated` + nudges
  frontmatter/nommage.
- `assets/hooks/settings.hooks.json` — bloc `hooks` à fusionner (non destructif) dans le
  `.claude/settings.json` du vault.
- `assets/persona-chief-of-staff/` — bundle figé de la persona Chief of Staff posée par défaut
  (étape 10bis) : `CLAUDE.md` (identité, lentille généraliste), `capacites-a-construire.md` (backlog),
  et `.claude/skills/brief-du-jour/` (le skill du battement quotidien, livré *avec* la persona — c'est
  son seul lieu : il n'est volontairement pas un skill global du plugin).
