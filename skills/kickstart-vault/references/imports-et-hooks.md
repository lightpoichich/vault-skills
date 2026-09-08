# Imports du `CLAUDE.md` racine et garde-fous du plugin

## Les `@imports`

- Les imports du `CLAUDE.md` racine sont relatifs (`@_Meta/Schema.md`, `@_Meta/governance.md`,
  `@_Meta/sources.md`). Lancés depuis la racine du vault, ils sont internes au cwd et chargés sans
  rien demander.
- Lancés depuis un sous-dossier (`_personas/{slug}/`, dossier de travail), Claude Code les tient pour
  externes et les ignore en silence tant que ce dossier n'est pas approuvé dans `~/.claude.json`
  (clé `hasClaudeMdExternalIncludesApproved`). Le dialogue « Allow external CLAUDE.md file
  imports? » n'apparaît qu'en session interactive ; en mode `-p`, SDK ou pilotage à distance, il
  n'est pas affiché.
- Un chemin absolu via symlink (`@~/vault/…`) est externe même depuis la racine : ne pas en mettre
  dans le `CLAUDE.md` racine.
- `_Meta/derivation.md` n'est pas importé : c'est le pourquoi du vault, consulté à la demande ;
  l'imposer à chaque session coûterait des tokens sans contrat opérationnel en retour. Il est
  seulement listé dans la carte du vault.

### Approbation pour le Chief of Staff

- Le hook `vault-approve-imports.sh` du plugin pose l'approbation au démarrage d'une session, avec
  effet à la session suivante. Pour que la première session du CoS charge déjà Schema, governance et
  sources, la poser au scaffold :
  ```bash
  "${CLAUDE_PLUGIN_ROOT}/hooks/vault-approve-imports.sh" "$VAULT_ABS/_personas/cos"
  ```
- La commande est idempotente et n'écrit dans `~/.claude.json` que si chaque import externe se
  résout dans un vault.
- Sans `CLAUDE_PLUGIN_ROOT` (installation sans plugin), le dirigeant lance `cos` une fois en
  interactif et répond « Yes, allow external imports » ; le compte-rendu le dit.

## Les quatre hooks du plugin

Ils sont déclarés dans `hooks/hooks.json` à la racine du plugin, actifs dans toute session où le
plugin est chargé, quel que soit le cwd, et se mettent à jour avec lui. Ils forment la couche
garantie : ils s'exécutent sur des événements du cycle de vie, quoi que le modèle décide, en
complément de la couche advisory (`CLAUDE.md`, `Schema.md`) que le modèle essaie de suivre. Hors
d'un vault (aucun `_Meta/` en remontant depuis le cwd ou le fichier écrit), ils sont no-op,
silencieux et instantanés.

| Hook | Événement | Ce qu'il fait | Réglage dans `hooks.conf` |
|---|---|---|---|
| Bilan de santé (`vault-health.sh`) | `SessionStart` | Inbox qui traîne, notes sans `type`, `.DS_Store` purgés. | `INBOX_STALE_DAYS`, `EXCLUDE` |
| Garde-fou d'écriture (`vault-note-guard.sh`) | `PostToolUse` sur Write et Edit | Pose `created` et `updated` ; rappel si frontmatter absent ou nom hors kebab-case. La racine est déduite du fichier écrit : une note du vault modifiée depuis un autre dossier est gardée aussi. | `EXCLUDE` |
| Approbation des imports (`vault-approve-imports.sh`) | `SessionStart` | Quand le dossier de lancement hérite d'un `CLAUDE.md` dont les `@imports` sortent du cwd et se résolvent dans un vault, pose `hasClaudeMdExternalIncludesApproved` pour ce dossier. Rien pour un import hors vault. | `APPROVE_EXTERNAL_IMPORTS=0` pour couper |
| Rappel de sync (`vault-sync-nudge.sh`) | `Stop` | Quand le transcript a grossi de `SYNC_MIN_KB` Ko et que `SYNC_MIN_MINUTES` minutes ont passé depuis le dernier sync, retient l'arrêt une fois et demande `sync-vault` (depuis le vault) ou `sync-repo` (depuis un dépôt relié à une fiche projet par `repo:` ou `dossier-travail:`). Ailleurs, rien. | `SYNC_MIN_KB`, `SYNC_MIN_MINUTES` ; `SYNC_NUDGE=0` coupe, `SYNC_NUDGE=vault` garde le rappel depuis le vault seulement |

- Ce sont des rappels et des corrections inertes : pas de blocage définitif, pas de suppression de
  contenu.
- Dépendances : `bash` et `python3` ; pas de `jq`.
- Ne rien copier dans `{vault}/.claude/hooks/` ni ajouter à `{vault}/.claude/settings.json`. Un vault
  qui porte encore `vault-health.sh` ou `vault-note-guard.sh` en local les fait tourner deux fois :
  proposer de retirer les entrées locales et les scripts.
- `{vault}/_Meta/hooks.conf` se copie depuis `assets/hooks/hooks.conf` tel quel, sans rien
  décommenter. Les exclusions (`EXCLUDE=`) sont un choix d'usage, pas de scaffold : elles servent
  quand une zone reçoit des données opérationnelles importées qu'il ne faut ni stamper ni compter.
- Pour le dirigeant, une phrase suffit : un bilan de santé au démarrage, un garde-fou à l'écriture,
  un rappel de répercussion en fin de tour ; rien à lancer.

## Sync git, opt-in hors plugin

`assets/hooks/vault-git-sync.sh` est un gabarit pour un vault qui vit aussi sur une machine sans
écran (serveur d'agents) : commit local au `Stop`, pull au `SessionStart`, push par un cron. Le
proposer seulement si le plan mentionne un tel montage. Il se copie dans `{vault}/.claude/hooks/` et
se branche à la main dans `{vault}/.claude/settings.json`.

## Portée de `brief-du-jour`

`brief-du-jour` vit dans `_personas/cos/.claude/skills/` et n'est actif que lancé depuis
`_personas/cos/` (`cd _personas/cos && claude` charge ce dossier de skills). Depuis la racine du
vault ou une autre persona, il ne se déclenche pas : le brief est le battement du Chief of Staff,
pas un skill global du plugin.
