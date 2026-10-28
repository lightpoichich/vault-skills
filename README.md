# Plugin second-cerveau pour Claude Code : guide d'utilisation

Le plugin `second-cerveau` installe et entretient un second cerveau : un dossier de notes, le vault, que Claude lit et met à jour pendant vos sessions de travail. L'installation pose la structure et des fiches vides ; le contenu entre ensuite au fil de l'usage.

Public : dirigeants et consultants qui travaillent avec Claude Code. Guide à jour de la version 5.2.2, le 28/10/2026.

## Le plugin en bref

- **Une fois, à l'installation** : un entretien sur votre activité, un plan que vous validez, puis la structure du vault et un premier assistant, le Chief of Staff. Si vous utilisez l'app Claude, sa mémoire oriente l'entretien dès le départ. Votre historique (projets Claude.ai, export Notion, dossiers de notes) peut ensuite être rapatrié.
- **Chaque jour** : un brief le matin, des demandes en langage courant pour ranger et organiser, et une mise à jour des fiches en fin de session, lancée par Claude lui-même.
- **Chaque mois** : un contrôle du vault, que Claude vous rappelle.
- **À chaque nouvelle version** : la mise à jour du plugin, puis celle des fichiers du vault qu'il a posés.

## Prérequis

- Claude Code installé sur le poste.
- git et python3, utilisés par les automatismes du plugin.
- Obsidian, facultatif, pour lire et parcourir les notes.

Aucun connecteur (agenda, messagerie, Notion) n'est requis. Le plugin utilise ceux que vous déclarez et fonctionne sans eux.

## Installer le plugin

1. Dans Claude Code, saisissez les deux commandes suivantes.
   ```
   /plugin marketplace add https://github.com/lightpoichich/vault-skills
   /plugin install second-cerveau@vault-skills
   ```
2. Relancez Claude Code, puis saisissez `/`. Les commandes du plugin apparaissent avec le préfixe `second-cerveau:`.

## Créer votre vault

### Avant de commencer, si vous utilisez l'app Claude

Demandez l'export de votre compte Claude.ai (démarche dans « Rapatrier vos projets Claude.ai »). Il arrive par mail. Avec lui, Claude part de ce que l'app sait déjà de vous et de vos projets : l'entretien démarre sur vos sujets réels, et vous confirmez chaque élément au lieu de tout décrire. Ses projets pourront ensuite être rapatriés à l'étape 6. Sans export, l'installation se déroule normalement, et Claude vous proposera de le demander au début de l'entretien.

### Étapes

1. Créez un dossier vide, par exemple `~/vault`, et lancez-y Claude Code : `cd ~/vault && claude`.
2. Saisissez `/second-cerveau:installer`. Claude vous demande d'abord si vous avez un export Claude.ai, et le dossier où vous l'avez réuni. Il recueille ensuite votre contexte : rôle, charge, sujets du moment, outils et chantiers en cours. Avec l'export, il vous présente ce qu'il en a tiré, et vous confirmez ou corrigez chaque élément.
3. Claude mène ensuite un entretien sur vos projets, vos domaines de responsabilité, vos ressources et vos sources d'information. Il vous fait choisir les usages prioritaires et le ton des assistants, puis écrit un plan dans `00-Inbox/plan-vault.md`.
4. Relisez le plan et corrigez-le si besoin. Quand il vous convient, dites « c'est bon, monte le vault ». Claude crée les dossiers, les fiches vides et le Chief of Staff.
5. Claude propose d'ajouter deux encarts à `~/.claude/CLAUDE.md`, le fichier de consignes que Claude Code lit dans toutes vos sessions. Le premier décrit votre contexte ; le second permet à Claude de retrouver le vault depuis n'importe quel dossier. Si vous refusez, les encarts restent à coller depuis `00-Inbox/compte-rendu-installation.md`.
6. Claude propose enfin de rapatrier votre historique. Cette étape est facultative et peut se faire plus tard (voir « Importer un ensemble de documents »).
7. Ouvrez un nouveau terminal et saisissez `cos`. Claude démarre dans le rôle de Chief of Staff.

Si l'installation s'interrompt après l'écriture du plan, relancez `/second-cerveau:installer` dans le même dossier : Claude reprend à la relecture du plan.

### Contenu du vault après l'installation

| Dossier | Contenu |
|---|---|
| `00-Inbox/` | Notes à trier, briefs du matin, plan et compte rendu d'installation |
| `10-Projects/` | Un dossier par projet, avec une fin et un livrable |
| `20-Areas/` | Un dossier par domaine de responsabilité continue (finance, équipe, commercial) |
| `30-Resources/` | Trames, méthodes et références réutilisables |
| `40-Archive/` | Projets et domaines clos, déplacés sans suppression |
| `_Meta/` | Règles du vault : types de fiches, confidentialité, connecteurs déclarés, réglages |
| `_personas/` | Les assistants, dont le Chief of Staff (`_personas/cos/`) |

## Une journée avec le vault

Les demandes se font en langage courant. Les phrases ci-dessous sont des exemples reconnus ; une formulation proche fonctionne aussi.

### Le matin : le brief

Depuis `cos`, dites « mon brief ». Claude écrit le brief du jour dans `00-Inbox/briefs/` : priorités, alertes, agenda, tâches et éléments à valider. Il s'appuie sur le vault et sur les connecteurs déclarés dans `_Meta/sources.md`. Sans connecteur, le brief porte sur le vault seul.

### Pendant la journée : ranger et organiser

| Besoin | Phrase à dire | Résultat |
|---|---|---|
| Ranger une note, une page web, une page Notion ou un document | « importe cette note », suivi du lien, du fichier ou du texte | Note classée dans le bon dossier et reliée aux fiches concernées |
| Importer un dossier, une archive ou un export complet | « importe ce dossier », suivi de son chemin | Tableau de reprise à valider, puis notes classées |
| Transformer une pratique répétée en modèle | « fais-en une trame » | Trame dans `30-Resources/`, construite à partir des cas réels du vault |
| Ouvrir un projet | « créer le projet X » | Fiche projet dans `10-Projects/`, rattachée à son domaine |
| Compléter un projet resté vide | « complète le projet X » | Champs manquants demandés puis remplis |
| Clore un projet | « archive le projet X » | Projet déplacé dans `40-Archive/` après votre validation |
| Créer, renommer, scinder ou archiver un domaine | « crée une area », « renomme l'area X » | Dossier dans `20-Areas/`, liens et assistants mis à jour après votre validation |

Un document confidentiel n'est jamais copié dans le vault. Claude y pose un renvoi : le lien, une ligne de contexte et la mention 🔒.

### En fin de session : la mise à jour des fiches

Claude reporte dans les fiches les décisions, statuts, tâches et contacts de la conversation. Vous pouvez le demander à tout moment par « sync le vault ».

Sans demande de votre part, Claude lance cette mise à jour de lui-même en fin de tour, après au moins 20 minutes d'échange depuis la précédente. Il ne la relance pas si vous venez de la faire. Quand rien n'a changé, il répond « Rien à répercuter. ».

## Travailler depuis un dossier de projet

Le vault suit aussi le travail mené ailleurs : le dépôt de code d'un projet client, ou un dossier sans git (OneDrive, Documents).

1. Lancez Claude Code dans ce dossier et dites « créer le projet X », ou « complète le projet X » si la fiche existe déjà. Claude relie le dossier à la fiche projet.
2. En fin de session, Claude met à jour cette fiche seule. Ce qui concerne d'autres fiches est noté dans sa section « À répercuter », et reporté à la prochaine mise à jour lancée depuis le vault.

Un même projet peut être relié depuis plusieurs postes : Claude ajoute le chemin de chaque poste à la fiche.

## Importer un ensemble de documents

Un export Notion, un dossier Drive ou d'anciennes notes s'importent en une seule opération.

1. Dites « importe ce dossier » en donnant son chemin, ou celui de l'archive `.zip`. Claude dresse l'inventaire et écrit un tableau de reprise dans `00-Inbox/import-{nom}.md` : une ligne par document, avec l'action proposée et sa destination.
2. Relisez le tableau. Vous pouvez corriger une ligne ou poser une règle générale, par exemple « tout le dossier `Clients/Acme/` va dans le projet Acme ». Rien n'est écrit dans le vault avant votre validation.
3. Claude exécute le tableau ligne par ligne et note où il en est. Une session interrompue reprend par « reprends l'import ».

Quatre actions sont possibles pour chaque document :

- **Copier** : le document entre dans le vault, classé et relié à ses fiches.
- **Distiller** : Claude reporte dans la fiche concernée les décisions, faits, tâches et événements datés d'un échange ou d'un compte rendu, sans copier le texte entier.
- **Renvoyer** : le vault garde un lien et une ligne de contexte ; le contenu reste à sa source. C'est la règle pour tout document confidentiel.
- **Ignorer** : le document n'entre pas.

Par défaut, seul ce qui sert un projet ou un domaine actif entre dans le vault ; le reste devient un lien ou s'ignore. Relancer le même import ne crée aucun doublon. Les archives sont décompressées hors du vault.

## Rapatrier vos projets Claude.ai

Dites « rapatrie mes projets Claude ». Deux voies sont possibles, et elles se combinent.

- **Un projet à la fois** : Claude vous donne un texte de passation à coller dans une nouvelle conversation de chaque projet Claude.ai. Collez ensuite la réponse dans Claude Code : « importe cette passation dans le projet X ». L'état du projet, ses décisions, ses tâches et ses instructions entrent dans la fiche correspondante.
- **Tous les projets d'un coup** : demandez l'export de votre compte dans Claude.ai (Settings, Privacy, « Export data », sur le web ou dans Claude Desktop). Le mail reçu donne un fichier qui liste plusieurs archives à télécharger : projets, conversations, mémoires et informations de compte. Téléchargez chaque archive en entier dès l'ouverture de son lien, qui expire au bout de 24 heures et peut ne servir qu'une fois. Réunissez les archives dans un même dossier, puis dites « importe cet export » en donnant le chemin de ce dossier. L'import suit la démarche de la section précédente.

L'export ne précise pas à quel projet appartient chaque conversation : Claude propose le rattachement dans le tableau de reprise, et vous le validez. La mémoire de chaque projet Claude.ai, qui résume son état, est reportée en priorité dans la fiche du projet.

## Étendre l'équipe d'assistants

- **Créer un assistant** : dites « nouvelle persona » ou « je veux un assistant RH ». Claude vous fait décrire votre quotidien, en déduit le rôle et les dossiers que l'assistant lit et écrit, puis crée son raccourci de lancement. Les tâches récurrentes repérées sont notées dans `_personas/{nom}/capacites-a-construire.md`.
- **Donner une routine à un assistant** : dites « crée un skill pour mon Chief of Staff », ou choisissez une ligne de `capacites-a-construire.md`. Claude pose quelques questions (déclenchement, résultat attendu, données utilisées), confirme avec vous avant d'écrire, puis teste la routine sur un cas réel.

## Automatismes du plugin

Quatre automatismes tournent dans vos sessions, sans commande à lancer. Hors d'un vault ou d'un dossier relié, ils ne font rien.

- **Bilan de démarrage** : au lancement, Claude reçoit l'état du vault. Il est averti des notes de `00-Inbox/` non triées depuis plus de 14 jours, des notes sans type, des fiches au-dessus de leur taille cible, d'une mémoire de Claude Code trop chargée, d'un dernier audit de plus de 30 jours et d'une mise à niveau disponible.
- **Contrôle des notes** : à chaque écriture, les dates de création et de modification sont tenues à jour ; un en-tête absent ou un nom de fichier non conforme est signalé.
- **Accès aux règles du vault** : un assistant ou un dossier de projet lit les règles de `_Meta/` sans demande d'autorisation à chaque session.
- **Mise à jour des fiches en fin de tour** : décrite dans « En fin de session : la mise à jour des fiches ».

Deux opérations accompagnent la mise à jour des fiches depuis le vault :

- **Allègement des fiches** : quand une fiche dépasse sa taille cible (30 Ko pour un projet, 20 Ko pour un domaine), ses entrées de journal les plus anciennes sont déplacées mot pour mot dans le sous-dossier `journal/` de la fiche. Rien n'est supprimé.
- **Rangement de la mémoire de Claude Code** : Claude Code tient sa propre mémoire entre les sessions. Claude en retire les données sensibles et reporte les faits durables dans les fiches du vault.

## Contrôle mensuel

Une fois par mois, dites « audit du vault ». Claude vérifie le vault sans rien modifier (liens cassés, fiches orphelines, projets à clore, domaines inactifs, assistants mal configurés, fiches trop lourdes) et écrit un rapport daté dans `00-Inbox/`. Les corrections se font ensuite avec votre accord : les corrections simples en une seule validation, les autres une par une. Les décisions qui vous reviennent restent dans le rapport. Claude vous rappelle l'audit quand le dernier date de plus de 30 jours.

## Mettre à jour le plugin et le vault

### Le plugin

Saisissez `/plugin marketplace update vault-skills`, puis relancez Claude Code.

### Les fichiers du vault posés par le plugin

Une nouvelle version peut améliorer les fichiers posés à l'installation : le Chief of Staff, son brief, les règles communes du vault. Claude est averti au démarrage qu'une mise à niveau est disponible. Pour l'appliquer, saisissez `/second-cerveau:installer` dans le vault.

- Un fichier que vous n'avez jamais modifié est remplacé par sa nouvelle version.
- Un fichier que vous avez personnalisé n'est jamais écrasé : Claude vous montre la différence et propose une version qui garde vos ajouts, appliquée seulement avec votre accord.
- Dans les fichiers de règles (le `CLAUDE.md` du vault, celui du Chief of Staff et le schéma des fiches), seules les parties marquées `socle second-cerveau` appartiennent au plugin. Ce que vous écrivez en dehors n'est jamais touché.
- Un changement de règle d'une version, comme le renommage des skills de la 5.0.0, est appliqué au passage.

Avant toute écriture, Claude propose une sauvegarde git du vault et garde une copie des fichiers modifiés hors du vault. Pour un vault installé avant la version 5.2.0, la première mise à niveau dresse l'état des lieux sans remplacer aucun fichier.

### Passage à la version 5.0.0

La version 5.0.0 a regroupé dix skills en six. Les phrases habituelles restent valables ; seuls les noms ont changé.

| Avant la 5.0.0 | Depuis la 5.0.0 |
|---|---|
| `interview-vault`, `kickstart-vault` | commande `/second-cerveau:installer` |
| `kickstart-persona`, `vault-skill-creator` | `assistants` |
| `import-note`, `extraire-trame` | `ranger` |
| `nouveau-projet`, `gerer-area` | `structurer` |

## Réglages

Les réglages se placent dans `_Meta/hooks.conf`, une ligne `CLÉ=valeur` par réglage.

| Réglage | Effet | Défaut |
|---|---|---|
| `SYNC_NUDGE=0` | Supprime la mise à jour automatique des fiches en fin de tour | active |
| `SYNC_NUDGE=vault` | Limite cette mise à jour automatique aux sessions ouvertes dans le vault | active partout |
| `SYNC_MIN_MINUTES` | Durée minimale entre deux mises à jour automatiques | 20 |
| `INBOX_STALE_DAYS` | Âge, en jours, à partir duquel une note de `00-Inbox/` est signalée | 14 |
| `AUDIT_REMINDER_DAYS` | Âge, en jours, du dernier audit avant rappel ; `0` supprime le rappel | 30 |
| `UPGRADE_REMINDER=0` | Supprime l'avertissement de mise à niveau disponible | actif |
| `JOURNAL_ROTATION=0` | Suspend l'allègement automatique des fiches | actif dans un vault créé par le plugin |

Les autres réglages sont décrits dans la [référence technique](docs/reference-technique.md).

## Résoudre un problème

| Constat | Action |
|---|---|
| `/second-cerveau:installer` n'apparaît pas. | Vérifiez l'installation par `/plugin`, puis relancez Claude Code. |
| Depuis un dossier de code, Claude ne trouve pas le vault. | Vérifiez que les encarts du compte rendu d'installation figurent dans `~/.claude/CLAUDE.md`. |
| La commande `cos` est introuvable. | Ouvrez un nouveau terminal. Le raccourci ne s'applique qu'aux terminaux ouverts après l'installation. |
| « mon brief » ne produit rien. | Lancez Claude avec `cos`. Le brief appartient à l'assistant Chief of Staff. |
| Claude répond souvent « Rien à répercuter. ». | Augmentez `SYNC_MIN_MINUTES` dans `_Meta/hooks.conf`. |
| Claude indique qu'il ne connaît pas encore les fichiers posés dans le vault. | Saisissez une fois `/second-cerveau:installer` dans le vault : la mise à niveau dresse l'état des lieux et l'avertissement cesse. |
| Autre problème | Ouvrez une [issue GitHub](https://github.com/lightpoichich/vault-skills/issues). |

## Glossaire

- **Vault** : dossier de notes Markdown, lisible dans Obsidian.
- **PARA** : classement des notes en projets, domaines de responsabilité (areas), ressources et archives.
- **Fiche** : note principale d'un projet ou d'un domaine, qui porte son état, ses décisions et son journal.
- **Persona** : assistant Claude doté d'un rôle, d'un périmètre de lecture et d'écriture, et d'un raccourci de lancement.
- **Skill** : procédure que Claude lance quand une demande correspond à sa description.
- **Trame** : modèle réutilisable tiré d'une pratique déjà réalisée plusieurs fois.
- **Tableau de reprise** : liste des documents d'un import, avec l'action et la destination de chacun, que vous validez avant l'écriture.

## Documentation technique et licence

Les automatismes et leurs réglages complets, le script d'inventaire des imports, l'outil de mise à niveau, la liaison entre un dossier de travail et sa fiche projet, l'installation manuelle et la description de chaque skill figurent dans la [référence technique](docs/reference-technique.md).

Le skill `assistants` adapte en partie le `skill-creator` d'Anthropic. Sa licence figure dans `skills/assistants/LICENSE.txt`.

Conçu et maintenu par [Lucas Clément](https://devlc.co), delivery de produits digitaux et accompagnement Claude Code pour dirigeants.
