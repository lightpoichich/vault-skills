---
name: installer
description: >-
  Installe un second cerveau en une commande, dans le dossier du futur vault : entretien de
  cartographie de l'activité, plan à valider, puis structure du vault (arborescence PARA, Schema,
  gouvernance, fiches vides, persona Chief of Staff et son brief), encarts du CLAUDE.md global
  posés avec accord, puis rapatriement facultatif de l'historique (projets Claude.ai, exports de
  notes). Reprend là où l'installation s'est arrêtée. Se lance par la commande
  /second-cerveau:installer.
disable-model-invocation: true
---

# Installer

Une commande, deux phases et un point d'arrêt entre elles, puis une phase facultative de
rapatriement de l'historique. L'entretien produit
`00-Inbox/plan-vault.md` ; le dirigeant le relit et le valide ; la structure l'exécute. Le plan est
le seul passage entre les deux phases : une installation coupée reprend depuis lui.

Le dirigeant n'est pas un développeur. Chaque phase porte ses règles de langue (section « Langue »
de `references/entretien.md`, section « Langue du dirigeant » de `references/structure.md`), avec
les anglicismes à remplacer dans `references/langue-dirigeant.md`.

## Procédure

### 1. Situer l'installation
Le dossier courant est la racine du futur vault : le confirmer en une phrase et noter son chemin
absolu. Puis reprendre là où l'on en est :

| État du dossier | Suite |
|---|---|
| ni `00-Inbox/plan-vault.md` ni `_Meta/Schema.md` | phase 1, l'entretien |
| `00-Inbox/plan-vault.md` présent, pas de `_Meta/Schema.md` | point d'arrêt : proposer de relire le plan, puis phase 2 sur go |
| `_Meta/Schema.md` présent | vault déjà installé : proposer la mise à niveau (`references/mise-a-niveau.md`), compléter ce qui manque sans rien écraser (phase 2 en ré-exécution), ou `audit-vault` pour un contrôle |

Un dossier déjà rempli de fichiers sans rapport avec un vault se signale avant de commencer.

### 2. Phase 1 : l'entretien
Dérouler `references/entretien.md` : matière première, interview en quatre phases, cas d'usage,
profil de ton, écriture du plan. Cette phase n'écrit que dans `00-Inbox/`. Si le dirigeant a des
projets dans l'app Claude, l'export de son compte se demande dès la matière première, et sa mémoire
peut pré-remplir les premiers fichiers, fait par fait confirmés.

### 3. Point d'arrêt : valider le plan
Résumer le plan et demander sa relecture. Rien n'est structuré sans un go explicite du dirigeant ;
une correction du plan se fait dans le fichier, puis on reprend ici.

### 4. Phase 2 : la structure
Dérouler `references/structure.md` : arborescence, couche `_Meta`, `CLAUDE.md` racine, réglages des
garde-fous, fiches vides d'areas et de projets, Resources, persona Chief of Staff, compte-rendu
d'installation et encarts du `~/.claude/CLAUDE.md` global proposés.

### 5. Phase 3 : rapatrier l'historique (facultative)
Proposer une fois de rapatrier l'historique cité dans `notes-actuelles.md` : dérouler
`references/migration.md` (une voie par source, règles du lot tirées du plan, tableau de reprise
validé, mode lot de `ranger`). Le dirigeant peut refuser ou reporter ; un tableau en cours se
reprend dans une session suivante.

### 6. Passer la main
Après la synthèse, orienter vers l'usage : lancer `cos` pour le Chief of Staff et son brief ; dire
« nouvelle persona » ou « crée un skill pour mon Chief of Staff » pour étendre l'équipe
(`assistants`) ; dire « importe cette note » pour faire entrer un contenu (`ranger`).

## Garde-fous
- **Rien d'inventé** : la structure vient du plan et de la matière première du dirigeant, jamais de
  l'environnement de l'auteur du skill.
- **Non destructif** : en ré-exécution, compléter sans écraser une fiche existante sans
  confirmation, et tout signaler dans le compte-rendu.
- **Écritures hors du vault limitées** au raccourci `cos`, à l'approbation des imports et aux
  encarts du `~/.claude/CLAUDE.md` acceptés par le dirigeant.

## Références
- `references/entretien.md` : phase 1, déroulé de l'interview et écriture du plan.
- `references/cartographie-guide.md` : réservoirs d'Areas, heuristiques Resources, types de fiches,
  gouvernance, cas d'usage, dérivation des compétences.
- `references/plan-vault-contract.md` : gabarit du plan et règles de remplissage, interface entre
  les deux phases.
- `references/structure.md` : phase 2, de l'arborescence au compte-rendu.
- `references/migration.md` : phase 3 facultative, voie par source, règles du lot tirées du plan.
- `references/plan-vault-format.md` : lecture du plan par la phase 2, défauts quand une section
  manque.
- `references/langue-dirigeant.md` : anglicismes à remplacer, termes internes à taire, exemples.
- `references/imports-et-hooks.md` : `@imports` et leur approbation, hooks du plugin et
  `hooks.conf`, sync git facultatif.
- `references/compte-rendu.md` : gabarit de `00-Inbox/compte-rendu-installation.md` et des encarts.
- `references/mise-a-niveau.md` : mise à niveau d'un vault installé (tampon, cas par fichier et par
  bloc, migrations, fusion assistée).
- `assets/` : gabarits du vault, réglages des hooks, persona Chief of Staff et `brief-du-jour`.
