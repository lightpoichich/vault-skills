# Plugin second-cerveau pour Claude Code : guide d'utilisation

Le plugin `second-cerveau` installe et entretient un second cerveau : un dossier de notes, le vault, que Claude lit et met à jour pendant vos sessions de travail. L'installation pose la structure et des fiches vides ; le contenu entre ensuite au fil de l'usage.

Public : dirigeants et consultants qui travaillent avec Claude Code. Guide à jour de la version 5.0.0, le 28/10/2026.

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

## Mettre à jour le plugin

Saisissez `/plugin marketplace update vault-skills`, puis relancez Claude Code.

La version 5.0.0 regroupe dix skills en six. Les phrases habituelles restent valables ; seuls les noms changent.

| Avant la 5.0.0 | Depuis la 5.0.0 |
|---|---|
| `interview-vault`, `kickstart-vault` | commande `/second-cerveau:installer` |
| `kickstart-persona`, `vault-skill-creator` | `assistants` |
| `import-note`, `extraire-trame` | `ranger` |
| `nouveau-projet`, `gerer-area` | `structurer` |

Après cette mise à jour, dites « audit du vault ». L'audit repère les assistants de votre vault dont une procédure appelle encore un ancien nom, et propose la correction.

## Créer votre vault

1. Créez un dossier vide, par exemple `~/vault`, et lancez-y Claude Code : `cd ~/vault && claude`.
2. Saisissez `/second-cerveau:installer`. Claude recueille d'abord six éléments de contexte : votre rôle et votre charge, les sujets qui vous occupent, l'endroit où vivent vos notes et l'information de l'équipe, les outils déjà en place et vos chantiers transverses. Il mène ensuite un entretien sur vos projets, vos domaines de responsabilité, vos ressources et vos sources, puis vous fait choisir les usages prioritaires et le ton des assistants. Il écrit enfin un plan dans `00-Inbox/plan-vault.md`.
3. Relisez le plan et corrigez-le si besoin. Quand il vous convient, dites « c'est bon, monte le vault ». Claude crée les dossiers, les fiches vides et un premier assistant, le Chief of Staff.
4. En fin d'installation, Claude propose d'ajouter deux encarts à `~/.claude/CLAUDE.md`, le fichier de consignes que Claude Code lit dans toutes vos sessions. Le premier décrit votre contexte, le second permet à Claude de retrouver le vault depuis n'importe quel dossier. Si vous refusez, les encarts restent à coller depuis `00-Inbox/compte-rendu-installation.md`.
5. Ouvrez un nouveau terminal et saisissez `cos`. Claude démarre dans le rôle de Chief of Staff.

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
| Transformer une pratique répétée en modèle | « fais-en une trame » | Trame dans `30-Resources/`, construite à partir des cas réels du vault |
| Ouvrir un projet | « créer le projet X » | Fiche projet dans `10-Projects/`, rattachée à son domaine |
| Compléter un projet resté vide | « complète le projet X » | Champs manquants demandés puis remplis |
| Clore un projet | « archive le projet X » | Projet déplacé dans `40-Archive/` après validation du plan |
| Créer, renommer, scinder ou archiver un domaine | « crée une area », « renomme l'area X » | Dossier dans `20-Areas/`, liens et assistants mis à jour après validation |

Un document confidentiel n'est jamais copié dans le vault. Claude y pose un renvoi : le lien, une ligne de contexte et la mention 🔒.

### En fin de session : la synchronisation

Claude reporte dans les fiches les décisions, statuts, tâches et contacts de la conversation. Vous pouvez le demander à tout moment par « sync le vault ».

Sans demande de votre part, Claude lance la synchronisation de lui-même en fin de tour, après au moins 20 minutes d'échange depuis la précédente. Il ne la relance pas si vous venez de la faire. Quand rien n'a changé, il répond « Rien à répercuter. ».

## Travailler depuis un dossier de projet

Le vault suit aussi le travail mené ailleurs : le dépôt de code d'un projet client, ou un dossier sans git (OneDrive, Documents).

1. Lancez Claude Code dans ce dossier et dites « créer le projet X », ou « complète le projet X » si la fiche existe déjà. Claude relie le dossier à la fiche projet.
2. En fin de session, Claude met à jour cette fiche seule. Ce qui concerne d'autres fiches est déposé dans sa section « À répercuter », traitée à la prochaine synchronisation depuis le vault.

Un même projet peut être relié depuis plusieurs postes : Claude ajoute le chemin de chaque poste à la fiche.

## Étendre l'équipe d'assistants

- **Créer un assistant** : dites « nouvelle persona » ou « je veux un assistant RH ». Claude vous fait décrire votre quotidien, en déduit le rôle et les dossiers que l'assistant lit et écrit, puis crée son raccourci de lancement. Les tâches récurrentes repérées sont notées dans `_personas/{nom}/capacites-a-construire.md`.
- **Donner une routine à un assistant** : dites « crée un skill pour mon Chief of Staff », ou choisissez une ligne de `capacites-a-construire.md`. Claude pose quelques questions (déclenchement, résultat attendu, données utilisées), confirme avec vous avant d'écrire, puis teste la routine sur un cas réel.

## Automatismes du plugin

Quatre automatismes tournent dans vos sessions, sans commande à lancer. Hors d'un vault ou d'un dossier relié, ils ne font rien.

- **Bilan de démarrage** : au lancement, Claude reçoit l'état du vault. Il signale les notes de `00-Inbox/` non triées depuis plus de 14 jours, les notes sans type, les fiches au-dessus de leur taille cible, une mémoire de Claude Code trop chargée et un dernier audit de plus de 30 jours.
- **Contrôle des notes** : à chaque écriture, les dates de création et de modification sont tenues à jour ; un en-tête absent ou un nom de fichier non conforme est signalé.
- **Accès aux règles du vault** : un assistant ou un dossier de projet lit les règles de `_Meta/` sans demande d'autorisation à chaque session.
- **Rappel de synchronisation** : décrit dans la section « En fin de session : la synchronisation ».

Deux opérations accompagnent la synchronisation depuis le vault :

- **Allègement des fiches** : quand une fiche dépasse sa taille cible (30 Ko pour un projet, 20 Ko pour un domaine), ses entrées de journal les plus anciennes sont déplacées mot pour mot dans le sous-dossier `journal/` de la fiche. Rien n'est supprimé.
- **Rangement de la mémoire de Claude Code** : Claude Code tient sa propre mémoire entre les sessions. La synchronisation en retire les données sensibles et reporte les faits durables dans les fiches du vault.

## Contrôle mensuel

Une fois par mois, dites « audit du vault ». Claude vérifie le vault en lecture seule (liens cassés, fiches orphelines, projets à clore, domaines inactifs, assistants mal configurés, fiches trop lourdes) et écrit un rapport daté dans `00-Inbox/`. Les corrections se font ensuite avec votre accord : les corrections mécaniques en une seule validation, les gestes plus lourds un par un. Les décisions qui vous reviennent restent dans le rapport. Le bilan de démarrage rappelle l'audit quand le dernier date de plus de 30 jours.

## Réglages

Les réglages se placent dans `_Meta/hooks.conf`, une ligne `CLÉ=valeur` par réglage.

| Réglage | Effet | Défaut |
|---|---|---|
| `SYNC_NUDGE=0` | Supprime la synchronisation automatique de fin de tour | rappel actif |
| `SYNC_NUDGE=vault` | Limite la synchronisation automatique aux sessions ouvertes dans le vault | rappel actif partout |
| `SYNC_MIN_MINUTES` | Durée minimale entre deux synchronisations automatiques | 20 |
| `INBOX_STALE_DAYS` | Âge, en jours, à partir duquel une note de `00-Inbox/` est signalée | 14 |
| `AUDIT_REMINDER_DAYS` | Âge, en jours, du dernier audit avant rappel ; `0` supprime le rappel | 30 |
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
| Autre problème | Ouvrez une [issue GitHub](https://github.com/lightpoichich/vault-skills/issues). |

## Glossaire

- **Vault** : dossier de notes Markdown, lisible dans Obsidian.
- **PARA** : classement des notes en projets, domaines de responsabilité (areas), ressources et archives.
- **Fiche** : note principale d'un projet ou d'un domaine, qui porte son état, ses décisions et son journal.
- **Persona** : assistant Claude doté d'un rôle, d'un périmètre de lecture et d'écriture, et d'un raccourci de lancement.
- **Skill** : procédure que Claude lance quand une demande correspond à sa description.
- **Trame** : modèle réutilisable tiré d'une pratique déjà réalisée plusieurs fois.

## Documentation technique et licence

Les automatismes et leurs réglages complets, la liaison entre un dossier de travail et sa fiche projet, l'installation manuelle et la description de chaque skill figurent dans la [référence technique](docs/reference-technique.md).

Le skill `assistants` adapte en partie le `skill-creator` d'Anthropic. Sa licence figure dans `skills/assistants/LICENSE.txt`.

Conçu et maintenu par [Lucas Clément](https://devlc.co), delivery de produits digitaux et accompagnement Claude Code pour dirigeants.
