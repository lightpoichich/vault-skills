---
name: interview-vault
description: >-
  Mène l'interview de cartographie PARA d'une activité et écrit 00-Inbox/plan-vault.md, le plan
  que kickstart-vault exécute ensuite. S'adapte aux réponses du dirigeant sans questionnaire figé
  et n'écrit rien hors de 00-Inbox/. S'utilise quand l'utilisateur dit « cartographier mon
  activité », « préparer mon vault », « faire l'interview PARA », « monter mon second cerveau »
  sur un vault vide. Pour matérialiser le plan, voir kickstart-vault.
---

# Interview Vault

Transforme une activité, en tête du dirigeant et éparse dans ses outils, en un plan de vault
structuré selon PARA. Le livrable unique est `00-Inbox/plan-vault.md`, que `kickstart-vault`
exécute ensuite pour poser le squelette ; viennent après `kickstart-persona` (les agents) puis
`vault-skill-creator` (les compétences). Ce skill n'écrit que dans `00-Inbox/` : il ne crée ni
dossier PARA, ni fiche, ni persona, ni skill.

## Partis pris

- **Généraliste, jamais profilé.** Ne pas demander de catégorie (« tech ou non-tech », « grande
  boîte ou TPE ») : la structure se dérive des réponses. Une suggestion (Area, source, compétence,
  type de fiche) n'est proposée que si elle fait écho à ce qui a été décrit ; les réservoirs sont
  dans `references/cartographie-guide.md`.
- **On pose le cadre, pas le contenu.** Capturer ce que le dirigeant dit, ne rien inventer. Si une
  réponse manque, écrire « à creuser en S1 » et avancer.
- **L'actionnabilité prime sur le sujet.** Le critère de classement PARA est l'actionnabilité, pas
  le thème. Ce qui ne finit jamais est une Area (« stratégie ») ; ce qui a une fin et un livrable
  est un Project (« finaliser le plan stratégique 2027 »). Surveiller cette confusion à chaque phase.

## Langue

Le dirigeant n'est pas un développeur. Tout ce qui s'affiche et tout texte livré suit ces règles :

- **Français propre.** Ne pas employer scaffold(er), bundle, alias, quick win, input, deal, mapping,
  shell, lazy-pull. Dire installer ou monter, ensemble prêt à l'emploi, raccourci, gain rapide,
  matière, affaire ou dossier, correspondance, fiche vide structurée, « au fil des besoins ».
- **Un terme de structure s'explique une fois**, à sa première occurrence, puis le mot suffit :
  `frontmatter` (l'en-tête d'une note), kebab-case (nom de fichier en minuscules avec tirets),
  `wikilink` (un lien `[[…]]`), persona (un assistant spécialisé), compétence (une routine automatisée).
- **Pas de jargon dans un titre de section du plan.** En cas de doute, la phrase doit être comprise
  par quelqu'un qui n'a jamais ouvert un terminal.

## Cadre PARA

- **Projects** : un effort avec une fin et un livrable (« préparer le conseil de juin »).
- **Areas** : une responsabilité continue (« finance », « fiabilité prod »). Viser 4 à 7 ; au-delà,
  proposer de consolider, et accepter 8 si le dirigeant tient à la distinction.
- **Resources** : un référentiel réutilisable (méthodes, trames, runbooks, benchmarks, ADR).
- **Archive** : ce qui est clos. On déplace, on ne supprime pas.
- **Inbox** : zone tampon de capture brute.

## Déroulé

### Phase 0. Cadre

Se présenter, poser le cadre PARA en une ou deux phrases, annoncer le déroulé : matière première,
interview en quatre phases, irritants, profil de ton, plan. Si un `~/.claude/CLAUDE.md` global
existe, l'utiliser pour se caler sur le contexte (rôle, charge) sans poser de question de profil.
Vérifier que le déroulé est compris, puis demander le premier élément de matière première.

### Étape 1. Matière première

Demander successivement ces six éléments et écrire chaque fichier dans `00-Inbox/matiere-premiere/`
(créer le dossier si besoin) avant de demander le suivant. L'interview ne démarre pas tant que les
six fichiers ne sont pas écrits.

| # | Demande (ouverte, aux mots du dirigeant) | Fichier |
|---|---|---|
| 1 | Contexte court : rôle, taille d'équipe, charge, ce qui pèse aujourd'hui | `contexte.md` |
| 2 | Thèmes mentaux actuels : les sujets qui structurent déjà sa tête | `themes-actuels.md` |
| 3 | Où vivent ses notes aujourd'hui (Notion, OneNote, fichiers `.md`, Apple Reminders, Projects Claude) | `notes-actuelles.md` |
| 4 | Outils où vit l'information d'équipe (Slack, Notion, DataDog, Gmail, GitHub, Granola, Outlook) | `sources-equipe.md` |
| 5 | Skills, MCP, slash commands, connecteurs déjà en place | `outillage-actuel.md` |
| 6 | Trois à cinq chantiers transverses en cours | `chantiers-en-cours.md` |

La demande est ouverte, le fichier cible reste canonique : demander « où vivent tes notes ? »,
jamais « montre-moi ton OneNote », et ranger la réponse dans `notes-actuelles.md` quel que soit
l'outil nommé. Sans matière pour un élément, écrire « néant pour l'instant » et avancer.

### Étape 2. Interview en quatre phases

Consulter `references/cartographie-guide.md` pour le superset d'Areas, les heuristiques Resources
et types de fiches, le réservoir de cas d'usage et la dérivation des compétences.

**Phase 1, Projects (3 à 4 questions).** Partir de `chantiers-en-cours.md`. Pour chaque chantier,
valider qu'il a une fin et un livrable, identifier deadline et parties prenantes. S'il est
continu, le reclasser en Area et le dire.

**Phase 2, Areas (5 à 7 questions).** Partir de `themes-actuels.md`. Pour chaque thème, vérifier
qu'il s'agit d'une responsabilité continue, puis creuser : objets récurrents, fréquence (au moins
hebdomadaire pour qualifier une Area), outils actuels. Chercher ensuite les Areas manquantes :
piocher dans le superset du guide seulement celles qui font écho, les proposer pour vérification.
Au-delà de 7, proposer de consolider sans l'imposer.

Boucle de validation obligatoire avant la Phase 3 : montrer une ébauche partielle (Projects et
Areas), laisser corriger, compléter, supprimer. N'avancer qu'une fois validée.

**Phase 3, Resources (4 à 5 questions).** Quelles méthodes, trames, runbooks, ADR, frameworks,
benchmarks sont réutilisés d'un chantier à l'autre ? Quels documents de référence sont consultés
tels quels, y compris les documents bruts (CGV, contrats types, plaquettes, charte graphique) ?
Pour chaque document existant, noter où il vit aujourd'hui (dossier Drive, page Notion, PDF qui
circule par mail, classeur papier) : le plan le liste avec son emplacement, ce qui permet de le
faire entrer plus tard, un par un, sans migration en masse. Proposer ensuite une sous-arborescence
de `30-Resources/` (2 à 4 sous-dossiers) et choisir avec le dirigeant la logique, par type ou par
domaine (heuristique dans le guide). Prévoir `references-externes/` pour les renvois.

**Phase 4, Sources et compétences (3 à 4 questions).**
- **Sources existantes.** Pour chaque source nommée à l'Étape 1 : quelle zone du vault elle
  alimente, et s'il s'agit d'une migration (le contenu entre) ou d'un renvoi (la source de vérité
  reste dehors, référencée dans `references-externes/`). Noter si un connecteur est branché (MCP
  ou API joignable). Par défaut une source est « à brancher » ; `kickstart-vault` n'écrit `actif`
  dans `_Meta/sources.md` que si le branchement est attesté.
- **Compétences à construire.** Un irritant chronophage donne une compétence (une routine
  automatisée), pas un rôle. Les dériver des Top 5 irritants (Étape 3) et des sources, jamais d'un
  catalogue. Pour chacune, noter ce qu'elle lit (Areas, Resources, source) et ce qu'elle écrit
  (zone, type de fiche).
- **Regroupement en personas.** Appliquer la règle de `references/plan-vault-contract.md` : tout
  sous le Chief of Staff par défaut, une persona à part seulement si zones, voix ou garde-fous
  distincts. Présenter : « voici tes compétences ; elles tiennent sous ton Chief of Staff, sauf
  {X} qui mérite sa persona parce que {raison} ».

Boucle de validation obligatoire, volet par volet et dans l'ordre : la correspondance entre sources
et zones, puis les compétences, puis le regroupement en personas. Validation explicite avant
chaque volet suivant, jamais une synthèse validée d'un bloc.

### Étape 3. Cas d'usage prioritaires

Demander les cinq choses qui lui coûtent le plus de temps aujourd'hui. Chaque irritant est la
matière d'une compétence, pas d'un rôle. Pour chacun, capter le signal d'impact : fréquence (par
semaine ou par mois), temps unitaire à la main, répétabilité (même tâche ou cas par cas),
projetable à l'équipe (combien de personnes). Une tâche au cas par cas reste un irritant, pas une
automatisation ; le dire.

Si le dirigeant sèche, proposer deux ou trois cas du réservoir du guide (« beaucoup de dirigeants
récupèrent du temps sur {X}, {Y} ; l'un de ces postes te parle ? »). Le plan en tire une
estimation d'heures libérées par semaine selon la règle de chiffrage de
`references/plan-vault-contract.md`. Sortie : des cas d'usage priorisés par impact.

### Étape 3bis. Profil de ton

Régler comment les assistants du vault s'adresseront au dirigeant. Le résultat va dans la section
« Profil de ton » du plan, que `kickstart-vault` reporte dans le `CLAUDE.md` racine, hérité par
toutes les personas. Présenter les quatre curseurs d'un coup et laisser le dirigeant se placer
avec ses propres mots :

- **Vocabulaire** : parle-moi métier, zéro jargon ni nom de fichier, ou les termes techniques sont OK.
- **Longueur** : va à l'essentiel, listes courtes, ou développe et explique le pourquoi.
- **Décision** : propose et je valide, ou décide et agis puis dis-moi, ou informe-moi seulement.
- **Registre** : sobre et factuel ou chaleureux ; tutoiement ou vouvoiement ; acquiesce ou challenge-moi.

Le curseur Vocabulaire dit comment on parle, jamais ce qu'on construit. Reformuler le placement en
une ligne. Sans préférence, le noter : `kickstart-vault` posera un défaut prudent marqué « à valider ».

### Étape 4. Écrire `00-Inbox/plan-vault.md`

Rédiger le plan selon le gabarit de `references/plan-vault-contract.md`, sections et titres
compris : `kickstart-vault` lit ce fichier pour tout générer. Synthétiser la section Gouvernance
et isolation depuis les signaux (sources RH, contrats, finances, marqués 🔒) même si le dirigeant
n'en a pas parlé.

### Handoff

Résumer le plan en quelques lignes (nombre d'Areas et de Projects, logique Resources, compétences
et regroupement en personas) et pointer la suite : « Ton plan est prêt dans
`00-Inbox/plan-vault.md`. Pour le matérialiser en vault réel (arborescence, Schema, gouvernance,
CLAUDE.md, hooks), lance `kickstart-vault`. »

## Garde-fous

- **Une question à la fois.** Reformuler la réponse avant d'enchaîner ; creuser si elle est floue.
  Ne pas regrouper deux sujets ou deux domaines dans la même question, même pour accélérer en fin
  de phase : si le temps presse, raccourcir la reformulation, pas la granularité des questions.
- **Écrire uniquement dans `00-Inbox/`** (le plan et `matiere-premiere/`). Ne pas toucher à
  `.claude/` ni à `_Meta/`.

## Références

- `references/cartographie-guide.md` : superset d'Areas, heuristiques Resources, types de fiches et
  gouvernance, réservoir de cas d'usage, dérivation des compétences.
- `references/plan-vault-contract.md` : gabarit du plan, règles de remplissage, règle de chiffrage,
  règle de regroupement en personas.
