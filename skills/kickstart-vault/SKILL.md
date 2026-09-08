---
name: kickstart-vault
description: >-
  Scaffolde un vault Obsidian PARA à partir du plan-vault.md produit par interview-vault :
  arborescence, Schema, governance, CLAUDE.md racine, fiches vides d'Areas et de Projects, persona
  Chief of Staff avec brief-du-jour. S'utilise quand l'utilisateur a un plan-vault.md et dit « crée
  la structure », « initialise le vault », « génère l'arborescence », « monte mon second cerveau ».
  Pour mener l'interview qui produit le plan, voir interview-vault.
---

# Kickstart Vault

Ce skill exécute le `plan-vault.md` produit par `interview-vault` : il pose le squelette du vault dans
le dossier courant, à partir des gabarits de `assets/`, sans inventer de contenu. Un vault vide mais
structuré est le résultat attendu ; le contenu entre ensuite par l'usage. Les gabarits deviennent des
fichiers du vault du dirigeant, lus à chaque session : ils ne portent que des règles durables.

## Langue du dirigeant

- Le curseur Vocabulaire du profil de ton du plan fixe la quantité de structure interne nommée
  (PARA, `_Meta`, frontmatter, slug, chemins). Sans profil, n'en nommer aucune.
- Les termes internes du skill (shell, bundle, generate-don't-write, idempotent, asset, scaffold)
  servent au modèle et ne sont pas répétés au dirigeant.
- Un terme de structure conservé est expliqué une fois, puis réutilisé.
- Narrer le résultat et la valeur, pas l'étape technique en cours.
- Aucun jargon dans le nom d'un fichier livré (`compte-rendu-installation.md`).

Anglicismes à remplacer et exemples avant/après : `references/langue-dirigeant.md`.

## Entrées attendues

- `plan-vault.md`, requis, par défaut `00-Inbox/plan-vault.md` du dossier courant. S'il est
  ailleurs, demander le chemin. S'il n'existe pas, ne rien scaffolder : indiquer au dirigeant de
  lancer `interview-vault`.
- `00-Inbox/matiere-premiere/`, optionnel : les fichiers bruts de l'interview, lus pour le contexte
  (gouvernance, encart de contexte du compte-rendu), jamais recopiés en fiches.
- Le format des deux entrées et les défauts à appliquer quand une section manque :
  `references/plan-vault-format.md`.

## Procédure

### 1. Localiser et lire les entrées
- Confirmer que le dossier courant est la racine du vault à scaffolder ; noter son chemin absolu
  (`VAULT_ABS`).
- Lire le plan en entier, puis `00-Inbox/matiere-premiere/*` s'il existe.
- Repérer les sections du plan par leur sens, pas par leur position (table dans
  `references/plan-vault-format.md`).

### 2. Passe de cohérence
- Signaler une Area qui a une date de fin ou un livrable unique (probablement un Project), et
  l'inverse. Le dirigeant tranche ; le plan reste la source de vérité.
- Si une section attendue manque, appliquer le défaut de `references/plan-vault-format.md` et le
  marquer « généré par défaut, à valider » dans le compte-rendu. Ne pas bloquer.

### 3. Créer l'arborescence
- Reproduire le bloc *Arborescence proposée* du plan : `10-Projects/`, `20-Areas/{areas}`,
  `30-Resources/{sous-zones}`, `40-Archive/`, `_Meta/` ; `00-Inbox/` existe déjà.
- Ajouter `_personas/` ; l'étape 12 y pose la persona Chief of Staff.
- Chaque Area et chaque Project du plan reçoit une fiche (étapes 7 et 8) ; aucun dossier « au cas
  où ».
- Tous les noms en kebab-case.

### 4. Générer la couche `_Meta`
Cette couche se pose avant toute fiche.
- `_Meta/Schema.md` depuis `assets/schema-template.md`. Garder les types de la section *Conventions
  frontmatter* du plan et ceux que la section *Compétences à construire* lit ou écrit. Les types
  d'outillage `moc`, `note`, `brief`, `draft` et `audit` restent toujours : les fichiers `_Meta/`,
  le compte-rendu, `brief-du-jour`, le sas `_drafts/` et `audit-vault` les utilisent. Un type métier
  absent du gabarit (`incident`, `reporting`, `veille`) est repris tel quel avec un bloc minimal :
  `type`, `tags` et les champs nommés au plan. Ne pas dupliquer un type sous un autre nom.
- `_Meta/governance.md` depuis `assets/governance-template.md`. Reprendre la section *Gouvernance /
  isolation* du plan ; sinon la synthétiser depuis les signaux de sensibilité de la matière
  première. Ne nommer aucun agent : le périmètre de chaque agent vit dans son
  `_personas/{slug}/CLAUDE.md`.
- `_Meta/sources.md` depuis `assets/sources-template.md`. Poser la ligne `vault`, puis une ligne par
  source nommée dans le *Mapping sources* du plan (`type`, `statut`, `usage`, `accès`). Aucune source
  que le plan ne nomme pas ; sans *Mapping sources*, la ligne `vault` seule, signalée dans le
  compte-rendu.
  - `statut` : `à brancher` par défaut. `actif` seulement si le plan atteste que le connecteur est
    branché et joignable, car un `actif` faux casse la cascade des skills. `renvoi 🔒` pour une
    source sensible.
  - `accès` : vide sauf heuristique explicite au plan ; jamais le schéma de la source.
- `_Meta/derivation.md` depuis `assets/derivation-template.md`. Les parties spécifiques (domaines,
  projets, posture 🔒) sont reprises du plan ; sans information, retirer la ligne ou laisser le
  placeholder. Langage calibré sur le curseur Vocabulaire : le dirigeant le lit.

### 5. Générer le `CLAUDE.md` racine
- Depuis `assets/vault-claude-template.md` : périmètre (le scope repris du plan, pas le rôle), carte
  du vault, conventions, règle « on pose le cadre, pas le contenu », garde-fous, imports.
- Carte au niveau PARA strict : dossiers de premier niveau et nomenclature `{slug}/{slug}.md`,
  aucun sous-dossier spécifique (ils changent avec l'usage).
- Section `## Ton` : quatre curseurs depuis le *Profil de ton* du plan, avec les mots du dirigeant.
  Pour chaque placeholder `{a | b}` du gabarit, ne garder qu'une valeur. Sans profil, défaut de
  `references/plan-vault-format.md`, marqué « à valider ». Le gabarit tutoie ; passer au
  vouvoiement si le profil le demande.
- Pas de bio (rôle, équipe, enjeux) : sa place est le `~/.claude/CLAUDE.md` global, le compte-rendu
  le recommande.
- `@imports` relatifs (`@_Meta/…`) de `Schema.md`, `governance.md` et `sources.md`, tels que dans le
  gabarit ; pas de chemin absolu via symlink ; ne pas importer `derivation.md`, consulté à la
  demande. Mécanique et approbation des imports : `references/imports-et-hooks.md`.

### 6. Poser les réglages des garde-fous
Les quatre hooks (bilan de santé, garde-fou d'écriture, approbation des imports, rappel de sync)
sont livrés par le plugin et actifs partout ; détail et réglages dans `references/imports-et-hooks.md`.
- Ne rien copier dans `{vault}/.claude/hooks/` ni ajouter à `settings.json`. Si le vault porte encore
  des scripts locaux (`vault-health.sh`, `vault-note-guard.sh`), proposer de les retirer : ils
  tourneraient deux fois.
- Copier `assets/hooks/hooks.conf` vers `{vault}/_Meta/hooks.conf` tel quel, sans rien décommenter.
- Proposer `assets/hooks/vault-git-sync.sh` seulement si le plan mentionne un vault partagé avec une
  machine sans écran.

### 7. Générer les shells d'Areas
- Une Area est un dossier `20-Areas/{slug}/` avec sa fiche `20-Areas/{slug}/{slug}.md` ; jamais une
  fiche à plat.
- Fiche depuis `assets/area-shell-template.md`, frontmatter rempli depuis le plan (objets, cadence,
  outils), corps réduit aux titres et à une ligne de but.

### 8. Générer les shells de Projects
- Même nomenclature : `10-Projects/{slug}/{slug}.md`.
- Fiche depuis `assets/project-shell-template.md` : `status`, `deadline`, `livrable`,
  `parties-prenantes`, `area` en wikilink si le plan le précise.

### 9. Resources
- Créer les sous-dossiers de `30-Resources/` du plan. Dans chacun, un `_index.md` liste les items du
  plan en cases à cocher.
- Item existant ailleurs : `- [ ] {nom} : {usage} ; vit aujourd'hui : {emplacement}`. Item à créer :
  case simple. Aucune copie : l'entrée se fait un item à la fois, par `import-note`.

### 10. Renvois externes
- Si le plan a un *Mapping sources* : dans `30-Resources/references-externes/`, un renvoi par source
  (titre, lien ou emplacement, une ligne de contexte, 🔒 si sensible). Pas de copie du contenu.

### 11. Laisser la matière première en place
- Ne pas déplacer ni transformer `00-Inbox/matiere-premiere/` : elle est tirée vers les fiches au fil
  de l'usage.

### 12. Poser la persona Chief of Staff
Le bundle `assets/persona-chief-of-staff/` est figé : ni `kickstart-persona` ni `vault-skill-creator`
ne sont invoqués. Le CoS suit les conventions de `kickstart-persona` et sert d'exemple à dupliquer ;
`brief-du-jour` voyage avec lui et n'est actif que lancé depuis `_personas/cos/`.
- Si `_personas/cos/` existe, compléter ce qui manque sans écraser, et le signaler.
- Copier le bundle vers `{vault}/_personas/cos/`, dossier caché `.claude/skills/brief-du-jour/`
  inclus. Le `CLAUDE.md` du CoS est posé tel quel : ses zones sont au niveau PARA, valables pour tout
  dirigeant.
- Poser le raccourci terminal `cos` (chemin absolu, idempotent, détection du shell) :
  ```bash
  VAULT_ABS="$(pwd)"                                  # racine du vault (étape 1)
  RC="$HOME/.zshrc"; [ -n "$BASH_VERSION" ] && RC="$HOME/.bashrc"
  LINE="alias cos=\"cd '$VAULT_ABS/_personas/cos' && claude\""
  grep -q "alias cos=" "$RC" 2>/dev/null || echo "$LINE" >> "$RC"
  ```
- Approuver les imports du vault pour le CoS :
  `"${CLAUDE_PLUGIN_ROOT}/hooks/vault-approve-imports.sh" "$VAULT_ABS/_personas/cos"`. Sans
  `CLAUDE_PLUGIN_ROOT`, le compte-rendu indique le geste manuel (`references/imports-et-hooks.md`).
- Le raccourci et cette approbation sont les seules écritures hors du vault ; le compte-rendu les
  signale.

### 13. Écrire le compte-rendu d'installation
- Créer `00-Inbox/compte-rendu-installation.md` selon le gabarit de `references/compte-rendu.md` :
  arbre créé, lot « généré par défaut, à valider », points « à creuser » du plan, prochaines étapes,
  mode d'emploi du CoS, garde-fous, deux encarts à coller dans le `~/.claude/CLAUDE.md` global.
- Ne pas modifier `~/.claude/CLAUDE.md` : les encarts sont livrés à coller.
- Afficher une synthèse au dirigeant, dans la langue de la section « Langue du dirigeant ».

## Garde-fous

- Aucun contenu métier inventé : pas de candidat, de décision, d'incident ni de chiffre. Si le plan et
  la matière première ne disent rien, la section reste vide.
- Sans `plan-vault.md`, ne rien scaffolder.
- Ré-exécution ou dossier déjà peuplé : compléter, ne pas écraser une fiche existante sans
  confirmation, tout signaler dans le compte-rendu.
- Beaucoup d'Areas ou de Projects : tout générer, et rappeler dans le compte-rendu le principe
  « élargir par l'usage » : peu d'Areas vivantes valent mieux que beaucoup de dossiers vides.
- Vault sans enjeu de confidentialité : `governance.md` légère (périmètre, accès des agents), sans
  multiplier les 🔒.
- Aucune dépendance à l'environnement de l'auteur du skill : tout vient du plan du dirigeant et de
  `assets/`.

## Références

- `references/plan-vault-format.md` : structure du `plan-vault.md` et de la matière première, étape
  qui consomme chaque section, défauts quand une section manque (gouvernance, ton, conventions,
  sources).
- `references/langue-dirigeant.md` : anglicismes à remplacer, termes internes à taire, calibrage sur
  le curseur Vocabulaire, exemples avant/après.
- `references/imports-et-hooks.md` : mécanique des `@imports` et de leur approbation, les quatre
  hooks du plugin et leurs réglages (`hooks.conf`), le sync git opt-in, la portée de `brief-du-jour`.
- `references/compte-rendu.md` : gabarit de `00-Inbox/compte-rendu-installation.md`, encarts à
  coller dans le `CLAUDE.md` global.
