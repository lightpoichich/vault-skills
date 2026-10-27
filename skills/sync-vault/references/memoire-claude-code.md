# La mémoire native de Claude Code

Le vault est le fonds, consultable dans Obsidian. La mémoire native de Claude Code est la couche de
rappel : un digest chargé au démarrage de chaque session lancée depuis le même dossier, personas
comprises. Claude Code y écrit aussi seul en cours de session : sans curation, elle grossit, se
périme et finit par contredire le vault. `sync-vault` la tient en mode vault et n'en fait qu'un tri
de frontière en mode projet.

## Faits Claude Code

Vérifiés sur Claude Code 2.1.311 ; à revérifier si le comportement change.
- **Emplacement** : `~/.claude/projects/{racine de la copie de travail, non-alphanumériques en -}/memory/`.
  La racine suit git : toutes les personas d'un vault sous git partagent la mémoire du vault. Dans un
  vault sans git, chaque dossier de persona a probablement sa propre mémoire.
  `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-memory.py" where` rend le chemin réel.
- **Chargement** : seul `MEMORY.md` est chargé, tronqué à 200 lignes et 25 000 caractères. Les fichiers
  thématiques sont lus à la demande, 200 au plus dans le rappel, les plus récents d'abord.
- **Réglages** : `autoMemoryEnabled` (et la variable `CLAUDE_CODE_DISABLE_AUTO_MEMORY`) active ou coupe
  la mémoire. `autoMemoryDirectory` la déplace : la première source qui le définit l'emporte, dans
  l'ordre `.claude/settings.local.json` de la racine git, `.claude/settings.json` du seul dossier de
  lancement (ces deux-là lus seulement si le dossier est de confiance ; le dialogue de confiance
  l'annonce), puis les réglages utilisateur. Une valeur ni absolue ni en `~/` est rejetée et le dossier
  par défaut s'applique.
  `autoDreamEnabled` règle une consolidation en arrière-plan propre à Claude Code. Ces réglages
  appartiennent à l'utilisateur : les signaler, ne jamais éditer `settings.json`.
- **Subagents** : un subagent ne charge pas la mémoire de la session principale. Une persona lancée
  en subagent reçoit ce qu'elle doit savoir par son prompt ou par le vault. Son champ `memory` lui
  donne une mémoire propre ; en portée projet, elle vit dans `{vault}/.claude/agent-memory/{nom}/`,
  versionnée avec le vault.

## Quoi y mettre

| Va en mémoire (rappel) | Va ailleurs |
|---|---|
| Priorités courantes, statut des projets actifs en une ligne, avec un pointeur vers la fiche | Le détail : la fiche du vault |
| Qui-est-qui (parties prenantes clés) | La fiche contact complète |
| Un piège ou une recette de l'environnement de travail (outil, machine, accès) | Un piège technique propre à un dépôt : le dépôt lui-même (`.claude/rules/`, hors de ce plugin) |
| Une préférence en attente de promotion | La règle durable : sa cible (table « Skill d'abord ») |

Jamais en mémoire : le sensible (RH nominatif, M&A, chiffres non publics, contenu 🔒, identifiants).
La mémoire est rechargée en clair dans chaque session, personas comprises.

## Budget

`_Meta/hooks.conf` : `MEMORY_MAX_LINES` (120) et `MEMORY_MAX_KB` (16, soit 16 000 caractères), environ
60 % du plafond réel. Une
ligne d'index par mémoire, `- [Titre](fichier.md) — accroche`, le détail dans le fichier. Le bilan de
démarrage signale le dépassement. Au-delà de 200 lignes ou 25 000 caractères, la fin de l'index n'est
plus chargée du tout.

## Curation en mode vault

`vault-memory.py check --vault {vault}` établit les faits : budget, index désynchronisé, pointeurs
vers le vault (cassés, archivés, déplacés, ambigus), sensible apparent (fichier, ligne et type, jamais le
contenu), quasi-doublons, `curation_due`, et `needs_curation` qui les résume. Une curation complète a
lieu quand `needs_curation` est vrai, c'est-à-dire quand `check` signale quelque chose ou quand `curation_due` est vrai
(dernière sauvegarde plus vieille que `MEMORY_CURATION_DAYS`, 30 jours). Sinon, ajouter ou mettre à
jour suffit. Ordre de la curation complète :

1. **Sauvegarder** : `vault-memory.py backup`. Aucune suppression ni réécriture sans cette copie,
   dont le chemin figure au compte rendu. La mémoire n'est pas versionnée.
2. **Retirer le sensible**, toujours en premier : le passage sort du fichier, ou le fichier entier
   si le sensible en est le sujet. Renvoi vers la fiche 🔒 au plus. Les sorties du script ne citent
   que le fichier et la ligne ; ne recopier le contenu nulle part, compte rendu compris.
3. **Rendre les faits au vault** : un fait d'état (statut, décision, chiffre, contact) appartient à
   une fiche. Si la fiche le dit déjà, la mémoire devient une ligne-pointeur ou disparaît. Sinon, le
   fait entre d'abord dans la fiche, puis la mémoire devient pointeur. En cas de contradiction, la
   fiche fait foi : corriger la mémoire et signaler l'écart au compte rendu.
4. **Skill d'abord** : une règle (style, livrable, gouvernance) ne quitte la mémoire qu'une fois
   présente dans sa cible, vérifiée par recherche de texte. Voir la table ci-dessous.
5. **Pointeurs** : un pointeur `déplacé` (un seul candidat vivant) se corrige vers le nouveau chemin.
   Un pointeur `ambigu` (plusieurs fichiers du même nom) ne se corrige pas seul : le signaler. Un
   pointeur `archivé` ou `cassé` se signale ; la mémoire qui ne vit que de lui se retire.
6. **Budget** : fusionner les quasi-doublons rendus par `check`, raccourcir les accroches de l'index,
   retirer ce qui n'amorce plus rien. Règle du doute : une mémoire dont l'utilité est incertaine reste.

### Skill d'abord : où remonte une règle

| Règle en mémoire | Cible | Geste |
|---|---|---|
| Ton, style, registre | canon de style du vault (`_Meta/style.md` ou équivalent) ou skill de ton | proposition |
| Format ou contenu d'un livrable | skill qui produit ce livrable | proposition |
| Gouvernance, accès, garde-fou | `CLAUDE.md` racine, `_Meta/governance.md`, ou une permission (réglage utilisateur) | proposition |
| Préférence transversale de l'utilisateur | `CLAUDE.md` global de la machine | proposition |
| Routine d'une persona | `CLAUDE.md` ou skill de la persona | proposition |

Les cibles sont des zones protégées : `sync-vault` rédige la promotion (cible, texte exact à ajouter)
dans son compte rendu et l'écrit après validation. La mémoire reste en place jusqu'à ce que la cible
contienne la règle. Une règle répétée (quasi-doublon dans le dossier, ou d'un dossier mémoire à
l'autre selon `vault-memory.py inventory`) passe en tête des propositions.

## Tri de frontière en mode projet

Depuis un dépôt ou un dossier de travail relié, `sync-vault` ne cure pas la mémoire du dossier : il
en trie la frontière, sur `vault-memory.py check --vault {vault}` du dossier courant.
- Une préférence transversale (ton, façon de travailler, règle valable hors de ce projet) devient
  une ligne de « À répercuter » visant le style, le `CLAUDE.md` global ou le skill concerné.
- Un fait d'état du projet va dans la fiche projet, sans doublon en mémoire.
- Le sensible est retiré, après `vault-memory.py backup`.
- Aucune autre mémoire n'est supprimée : la session n'a qu'un contexte partiel, et une suppression
  serait définitive. Le savoir technique du dépôt reste en mémoire ; sa place durable,
  `.claude/rules/` dans le dépôt, relève d'un autre outillage.

## Plusieurs machines (option)

Par défaut, la mémoire est locale à la machine. Pour la partager, poser sur chaque machine, dans le
`.claude/settings.local.json` du vault (non versionné, propre à la machine, et lu en premier),
`"autoMemoryDirectory": "{chemin absolu du vault}/_Meta/memoire"`. Lu à la racine git, il couvre aussi
les sessions lancées depuis une persona. Le `.claude/settings.json` versionné ne convient pas : il n'est
lu que dans le dossier de lancement, donc pas depuis `_personas/{slug}/`, et il imposerait le même chemin
absolu à toutes les machines. Effets à accepter avant de le proposer :
- la mémoire est publiée avec le vault : zéro sensible, sans exception ;
- elle devient versionnée : une suppression se récupère dans l'historique git ;
- deux machines qui écrivent en même temps peuvent produire un conflit git sur `MEMORY.md` ;
- `_Meta/` est hors des contrôles de fiche des hooks ; `audit-vault` ne juge pas ces fichiers comme
  des fiches.
Le plugin ne pose jamais ce réglage : il le documente, et `audit-vault` signale l'état observé.

## Compte rendu

Chemin de la sauvegarde ; mémoires retirées, raccourcies, fusionnées ou devenues pointeurs ; faits
rendus au vault (fiche visée) ; promotions proposées (cible et texte) ; contradictions et pointeurs
signalés ; taille de l'index avant et après.
