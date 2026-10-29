# Plugin second-cerveau pour Claude Code : guide d'utilisation

Le plugin `second-cerveau` installe et entretient un second cerveau : un dossier de notes, le vault, que Claude lit et met à jour pendant vos sessions de travail. L'installation pose la structure et des fiches vides ; le contenu entre ensuite au fil de l'usage.

Public : dirigeants et consultants qui travaillent avec Claude Code, dans le terminal ou dans l'app Claude. Guide à jour de la version 5.2.5, le 29/10/2026.

## Le plugin en bref

- **Une fois, à l'installation** : un entretien sur votre activité, un plan que vous validez, puis la structure du vault et un premier assistant, le Chief of Staff. Si vous utilisez l'app Claude, sa mémoire oriente l'entretien, et vos projets peuvent ensuite être rapatriés.
- **Chaque jour** : un brief le matin, des demandes en langage courant pour ranger et organiser, et une mise à jour des fiches en fin de session, lancée par Claude lui-même.
- **Chaque mois** : un contrôle du vault, que Claude vous rappelle.
- **À chaque nouvelle version** : la mise à jour du plugin, puis celle des fichiers du vault qu'il a posés.

## Prérequis

- Claude Code, dans le terminal ou dans l'app Claude (onglet Code).
- git et python3, utilisés par les automatismes du plugin.
- Obsidian, facultatif, pour lire les notes.

Aucun connecteur (agenda, messagerie, Notion) n'est requis : le plugin utilise ceux que vous déclarez.

## Installer le plugin

**Dans le terminal**, saisissez les deux commandes suivantes dans Claude Code, puis relancez-le.

```
/plugin marketplace add https://github.com/lightpoichich/vault-skills
```
```
/plugin install second-cerveau@vault-skills
```

**Dans l'app Claude**, ouvrez l'onglet Code et démarrez une session locale. Cliquez sur **+** à côté de la zone de saisie, puis **Add plugins** (ou **Plugins**, puis **Browse plugins**), et installez `second-cerveau` pour votre compte. Si le plugin n'apparaît pas dans la liste, ajoutez une fois sa source depuis un terminal : `claude plugin marketplace add https://github.com/lightpoichich/vault-skills`.

Le terminal et les sessions locales de l'app partagent les mêmes réglages : un plugin installé pour votre compte d'un côté est disponible de l'autre. Les sessions cloud de l'app ne chargent pas les plugins ; travaillez en session locale.

Saisissez ensuite `/` : les commandes du plugin apparaissent avec le préfixe `second-cerveau:`.

**Activez la mise à jour automatique**, une seule fois : dans une session du terminal, saisissez `/plugin`, ouvrez l'onglet **Marketplaces**, choisissez `vault-skills`, puis **Enable auto-update**. Le réglage vaut aussi pour l'app Claude. Sans lui, le plugin ne se met pas à jour seul, car Claude Code coupe cette option par défaut pour les plugins qui ne viennent pas d'Anthropic. L'installation du vault vous le rappelle si besoin.

## Créer votre vault

### Avant de commencer, si vous utilisez l'app Claude

Demandez l'export de votre compte Claude.ai (démarche dans « Rapatrier vos projets Claude.ai »). Avec lui, l'entretien part de ce que l'app sait déjà de vous et de vos projets : vous confirmez chaque élément au lieu de tout décrire. Sans export, Claude vous proposera de le demander au début de l'entretien.

### Étapes

1. Créez un dossier vide, par exemple `~/vault`, et ouvrez-y une session : `cd ~/vault && claude` dans le terminal, ou ce dossier comme dossier de projet dans l'app Claude.
2. Saisissez `/second-cerveau:installer`. Claude demande d'abord si vous avez un export Claude.ai, puis votre contexte : rôle, charge, sujets du moment, outils, chantiers.
3. Claude mène un entretien sur vos projets, vos domaines de responsabilité, vos ressources et vos sources d'information, puis écrit un plan dans `00-Inbox/plan-vault.md`.
4. Relisez et corrigez le plan. Quand il vous convient, dites « c'est bon, monte le vault » : Claude crée les dossiers, les fiches vides et le Chief of Staff.
5. Claude propose d'ajouter à `~/.claude/CLAUDE.md`, le fichier de consignes lu dans toutes vos sessions, un encart sur votre contexte et un encart qui lui permet de retrouver le vault depuis n'importe quel dossier. Sans votre accord, les encarts restent à coller depuis `00-Inbox/compte-rendu-installation.md`.
6. Claude propose de rapatrier votre historique. Cette étape est facultative et peut se faire plus tard.
7. Lancez le Chief of Staff : `cos` dans un nouveau terminal, ou une session ouverte sur le dossier `_personas/cos` dans l'app Claude.

Une installation interrompue après l'écriture du plan reprend à sa relecture : relancez `/second-cerveau:installer` dans le même dossier.

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

Le rôle de chaque dossier, les déplacements d'une information de l'un à l'autre et la façon dont Claude s'en sert pour trouver le bon contexte sont expliqués, schémas à l'appui, dans [Comprendre l'organisation du vault](docs/comprendre-para.md).

## Les skills du vault

Un skill est une procédure que Claude lance de lui-même quand votre demande lui correspond. Vous n'avez pas à retenir leurs noms : la colonne de droite donne des formulations reconnues, et une phrase proche fonctionne aussi.

| Skill | Ce qu'il fait | Exemple de demande |
|---|---|---|
| `installer` | Installe le vault (entretien, plan, structure, Chief of Staff), rapatrie l'historique, puis met le vault à niveau à chaque version | commande `/second-cerveau:installer`, la seule à saisir vous-même |
| `ranger` | Fait entrer un contenu : une note, un dossier entier, un export Claude.ai, ou une trame tirée d'une pratique répétée | « importe cette note », « importe ce dossier », « fais-en une trame » |
| `structurer` | Crée, complète, renomme, scinde, fusionne ou archive un projet ou un domaine de responsabilité | « créer le projet X », « archive le projet X », « crée une area » |
| `sync-vault` | Reporte dans les fiches les décisions, statuts, tâches et contacts de la session | « sync le vault », ou lancé seul en fin de session |
| `audit-vault` | Contrôle le vault sans le modifier, puis propose des corrections | « audit du vault » |
| `assistants` | Crée un assistant spécialisé et lui donne des routines | « nouvelle persona », « crée un skill pour mon Chief of Staff » |
| `brief-du-jour` | Rédige le brief du matin ; propre au Chief of Staff | « mon brief », depuis le Chief of Staff |

## Une journée avec le vault

- **Le matin** : depuis le Chief of Staff, dites « mon brief ». Le brief du jour s'écrit dans `00-Inbox/briefs/` : priorités, alertes, agenda, tâches et éléments à valider, tirés du vault et des connecteurs déclarés dans `_Meta/sources.md`.
- **Pendant la journée** : rangez vos documents, ouvrez et clôturez vos projets par les demandes de la section « Les skills du vault ». Un document confidentiel n'est jamais copié : le vault garde un lien, une ligne de contexte et la mention 🔒.
- **En fin de session** : après au moins 20 minutes d'échange, Claude met les fiches à jour de lui-même, sauf si vous venez de le demander. Quand rien n'a changé, il répond « Rien à répercuter. ».

### Depuis un dossier de projet

Le vault suit aussi le travail mené ailleurs, dans le dépôt de code d'un client ou un dossier OneDrive. Ouvrez une session dans ce dossier et dites « créer le projet X », ou « complète le projet X » si la fiche existe : Claude relie le dossier à la fiche. En fin de session, il met à jour cette fiche seule et note ce qui concerne les autres dans sa section « À répercuter ».

## Importer un ensemble de documents

Un export Notion, un dossier Drive ou d'anciennes notes s'importent en une seule opération.

1. Dites « importe ce dossier » en donnant son chemin ou celui de l'archive `.zip`. Claude écrit un tableau de reprise dans `00-Inbox/import-{nom}.md` : une ligne par document, avec l'action proposée et sa destination.
2. Corrigez une ligne ou posez une règle générale, par exemple « tout `Clients/Acme/` va dans le projet Acme ». Rien n'est écrit avant votre validation.
3. Claude exécute le tableau ligne par ligne. Une session interrompue reprend par « reprends l'import ».

Chaque document est **copié** (classé et relié à ses fiches), **distillé** (ses décisions, faits et événements datés vont dans la fiche concernée, sans le texte entier), **renvoyé** (un lien et une ligne de contexte, règle de tout document confidentiel) ou **ignoré**. Par défaut, seul ce qui sert un projet ou un domaine actif entre dans le vault. Relancer le même import ne crée aucun doublon ; les archives sont décompressées hors du vault.

## Rapatrier vos projets Claude.ai

Dites « rapatrie mes projets Claude ». Deux voies, qui se combinent :

- **Un projet à la fois** : Claude vous donne un texte de passation à coller dans une nouvelle conversation de chaque projet Claude.ai. Collez la réponse dans Claude Code : « importe cette passation dans le projet X ».
- **Tous les projets d'un coup** : dans Claude.ai, ouvrez Settings, Privacy, « Export data ». Le mail reçu liste plusieurs archives (projets, conversations, mémoires, informations de compte). Téléchargez chacune en entier dès l'ouverture de son lien, valable 24 heures et parfois une seule fois, réunissez-les dans un dossier, puis dites « importe cet export » avec le chemin du dossier.

Claude propose dans le tableau de reprise le projet de chaque conversation, que l'export ne précise pas, et reporte en priorité la mémoire de chaque projet, qui résume son état.

## Automatismes du plugin

Hors d'un vault ou d'un dossier relié, ils ne font rien.

- **Bilan de démarrage** : Claude est averti des notes à trier depuis plus de 14 jours, des fiches trop lourdes, d'une mémoire de Claude Code trop chargée, d'un audit qui date de plus de 30 jours et d'une mise à niveau disponible.
- **Contrôle des notes** : les dates de création et de modification sont tenues à jour ; un nom de fichier non conforme est signalé.
- **Accès aux règles** : un assistant ou un dossier de projet lit les règles de `_Meta/` sans autorisation à redonner.
- **Mise à jour des fiches en fin de session**, décrite plus haut. Elle déplace aussi, mot pour mot, les entrées de journal les plus anciennes d'une fiche trop lourde vers son sous-dossier `journal/`, et retire les données sensibles de la mémoire de Claude Code.

## Contrôle mensuel

Dites « audit du vault ». Claude vérifie le vault sans le modifier (liens cassés, projets à clore, domaines inactifs, assistants mal configurés, fiches trop lourdes) et écrit un rapport daté dans `00-Inbox/`. Les corrections simples se valident d'un bloc, les autres une par une ; les décisions qui vous reviennent restent dans le rapport.

## Mettre à jour le plugin et le vault

**Le plugin** : avec la mise à jour automatique, chaque nouvelle version est téléchargée pendant une session et chargée à la suivante. Sans elle, saisissez dans un terminal `claude plugin marketplace update vault-skills`, puis `claude plugin update second-cerveau@vault-skills`, et relancez Claude Code ou l'app.

**Les fichiers du vault posés par le plugin** (le Chief of Staff, son brief, les règles communes) : quand une version les améliore, Claude en est averti au démarrage. Saisissez `/second-cerveau:installer` dans le vault.

- Un fichier jamais modifié est remplacé par sa nouvelle version.
- Un fichier personnalisé n'est jamais écrasé : Claude montre la différence et propose une version qui garde vos ajouts, appliquée avec votre accord.
- Dans les fichiers de règles, seules les parties marquées `socle second-cerveau` appartiennent au plugin ; le reste n'est jamais touché.

Dans un vault suivi par git, Claude propose un commit avant toute écriture ; dans tous les cas, le plugin garde hors du vault une copie des fichiers qu'il remplace. Pour un vault installé avant la version 5.2.0, la première mise à niveau dresse l'état des lieux sans remplacer aucun fichier.

La version 5.0.0 a renommé les skills ; les phrases habituelles restent valables.

| Avant la 5.0.0 | Depuis la 5.0.0 |
|---|---|
| `interview-vault`, `kickstart-vault` | `/second-cerveau:installer` |
| `kickstart-persona`, `vault-skill-creator` | `assistants` |
| `import-note`, `extraire-trame` | `ranger` |
| `nouveau-projet`, `gerer-area` | `structurer` |

## Réglages

Dans `_Meta/hooks.conf`, une ligne `CLÉ=valeur` par réglage.

| Réglage | Effet | Défaut |
|---|---|---|
| `SYNC_NUDGE=0` | Supprime la mise à jour automatique des fiches en fin de session | active |
| `SYNC_MIN_MINUTES` | Durée minimale entre deux mises à jour automatiques | 20 |
| `AUDIT_REMINDER_DAYS` | Âge du dernier audit avant rappel, en jours ; `0` supprime le rappel | 30 |
| `UPGRADE_REMINDER=0` | Supprime l'avertissement de mise à niveau disponible | actif |
| `JOURNAL_ROTATION=0` | Suspend l'allègement automatique des fiches | actif |

Les autres réglages figurent dans la [référence technique](docs/reference-technique.md).

## Résoudre un problème

| Constat | Action |
|---|---|
| `/second-cerveau:installer` n'apparaît pas. | Vérifiez l'installation par `/plugin`, relancez Claude Code, et travaillez en session locale dans l'app. |
| Depuis un dossier de code, Claude ne trouve pas le vault. | Vérifiez que les encarts du compte rendu d'installation figurent dans `~/.claude/CLAUDE.md`. |
| La commande `cos` est introuvable. | Ouvrez un nouveau terminal, ou ouvrez le dossier `_personas/cos` dans l'app Claude. |
| « mon brief » ne produit rien. | Lancez le Chief of Staff : le brief lui appartient. |
| Claude répond souvent « Rien à répercuter. ». | Augmentez `SYNC_MIN_MINUTES`. |
| Claude indique qu'il ne connaît pas encore les fichiers posés dans le vault. | Saisissez une fois `/second-cerveau:installer` dans le vault. |
| Autre problème | Ouvrez une [issue GitHub](https://github.com/lightpoichich/vault-skills/issues). |

## Glossaire

- **Vault** : dossier de notes Markdown, lisible dans Obsidian.
- **PARA** : classement en projets, domaines de responsabilité (areas), ressources et archives.
- **Fiche** : note principale d'un projet ou d'un domaine : état, décisions, journal.
- **Persona** : assistant Claude doté d'un rôle, d'un périmètre et d'un raccourci de lancement.
- **Trame** : modèle réutilisable tiré d'une pratique déjà réalisée plusieurs fois.
- **Tableau de reprise** : liste des documents d'un import, avec l'action et la destination de chacun, validée avant l'écriture.

## Documentation technique et licence

Réglages complets, scripts d'inventaire et de mise à niveau, liaison d'un dossier de travail, installation manuelle et description de chaque skill : [référence technique](docs/reference-technique.md).

Le skill `assistants` adapte en partie le `skill-creator` d'Anthropic ; sa licence figure dans `skills/assistants/LICENSE.txt`.

Conçu et maintenu par [Lucas Clément](https://devlc.co), delivery de produits digitaux et accompagnement Claude Code pour dirigeants.
