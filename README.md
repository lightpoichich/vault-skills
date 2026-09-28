# vault-skills

Le plugin Claude Code `second-cerveau` crée et entretient un second cerveau : un dossier de notes que Claude lit et met à jour pendant les sessions de travail. Le plugin pose la structure et des fiches vides, et le contenu entre au fil de l'usage.

Public : dirigeants et consultants qui travaillent avec Claude Code. Page à jour de la version 3.0.2, le 28/09/2026.
Signaler un problème : [issues GitHub](https://github.com/lightpoichich/vault-skills/issues).

## Installer le plugin

Prérequis : Claude Code, git et python3 sur le poste. Obsidian est facultatif et sert à lire les notes.

1. Dans Claude Code, saisir les deux commandes suivantes.
   ```
   /plugin marketplace add https://github.com/lightpoichich/vault-skills
   /plugin install second-cerveau@vault-skills
   ```
2. Saisir `/` dans Claude Code. Les skills du plugin apparaissent dans la liste avec le préfixe `second-cerveau:`.

Pour installer une nouvelle version, saisir `/plugin marketplace update vault-skills`.

## Créer son vault

1. Créer un dossier vide pour le vault, par exemple `~/vault`, puis y lancer Claude Code : `cd ~/vault && claude`.
2. Dire « préparer mon vault ». Claude mène un entretien sur l'activité, puis écrit le plan dans `00-Inbox/plan-vault.md`.
3. Relire le plan, puis dire « crée la structure ». Claude crée les dossiers, les fiches vides et l'assistant Chief of Staff.
4. Ouvrir `00-Inbox/compte-rendu-installation.md` et coller ses deux encarts dans `~/.claude/CLAUDE.md`. Le second permet à Claude de retrouver le vault depuis n'importe quel dossier.
5. Ouvrir un nouveau terminal et saisir `cos`. Claude démarre dans le rôle de Chief of Staff.

## Utiliser le vault au quotidien

Les demandes se font en langage courant. La colonne du milieu donne une formulation reconnue pour chaque besoin.

| Besoin | Dire à Claude | Résultat |
|---|---|---|
| Faire le point du matin, depuis `cos` | « mon brief » | Brief du jour dans `00-Inbox/briefs/` |
| Ranger une note, une page web ou un document | « importe cette note » | Note classée dans le bon dossier |
| Ouvrir un projet | « créer le projet X » | Fiche projet dans `10-Projects/` |
| Enregistrer les décisions de la session | « sync le vault », ou « sync le projet » depuis un dossier de code | Décisions, statuts et tâches reportés dans les fiches |
| Transformer une pratique répétée en modèle | « fais-en une trame » | Modèle dans `30-Resources/` |
| Créer, renommer ou archiver un domaine de responsabilité | « crée une area » | Dossier dans `20-Areas/` |
| Ajouter un assistant spécialisé | « nouvelle persona » | Assistant lancé par son propre raccourci |
| Donner une routine à un assistant | « crée un skill pour mon Chief of Staff » | Procédure rangée dans le dossier de l'assistant |
| Contrôler le vault, une fois par mois | « audit du vault » | Rapport dans `00-Inbox/`, corrections après validation |

En fin de tour, après au moins 20 minutes de travail, Claude lance de lui-même la synchronisation des fiches.

## Signaler un problème

| Constat | Quoi faire |
|---|---|
| Depuis un dossier de code, Claude ne trouve pas le vault. | Vérifier que les encarts du compte rendu d'installation sont collés dans `~/.claude/CLAUDE.md`. |
| La commande `cos` est introuvable. | Ouvrir un nouveau terminal. Le raccourci ne s'applique qu'aux terminaux ouverts après l'installation. |
| « mon brief » ne produit rien. | Lancer Claude avec `cos`. Le brief n'existe que dans l'assistant Chief of Staff. |
| La synchronisation automatique gêne. | La désactiver dans `_Meta/hooks.conf` (réglage `SYNC_NUDGE=0`). |
| Autre problème | Ouvrir une [issue](https://github.com/lightpoichich/vault-skills/issues). |

## Glossaire

- **Vault** : dossier de notes Markdown, lisible dans Obsidian.
- **PARA** : classement en quatre zones : projets, domaines de responsabilité (areas), ressources et archives.
- **Persona** : assistant Claude doté d'un rôle, d'un périmètre et d'un raccourci de lancement.
- **Skill** : procédure que Claude lance quand une demande correspond à sa description.

## Pour l'équipe technique

Les hooks et leurs réglages, la liaison entre un dépôt de code et sa fiche projet, l'installation manuelle et la description complète de chaque skill sont dans [docs/reference-technique.md](docs/reference-technique.md).

`vault-skill-creator` adapte le `skill-creator` d'Anthropic. Sa licence est dans `skills/vault-skill-creator/LICENSE.txt`.

Conçu et maintenu par [Lucas Clément](https://devlc.co), delivery de produits digitaux et accompagnement Claude Code pour dirigeants.
