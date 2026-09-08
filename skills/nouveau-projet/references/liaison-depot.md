# Liaison au dossier de travail

Checklist stricte, appliquée à l'étape 4 de `nouveau-projet` quand la session est lancée depuis un
dossier hors du vault. Les points s'exécutent dans l'ordre ; un point non applicable se saute sans
rien poser à la place. La règle de résolution `repo:` puis `dossier-travail:` puis slug est portée
par `hooks/vault-resolve.py` ; ce fichier dit seulement comment poser les clés que le résolveur lit.

1. Vérifier les champs existants de la fiche. Un `repo:` ou un `dossier-travail:` déjà renseigné ne
   se réécrit pas ; si les deux existent, passer au point 5.
2. Poser `dossier-travail: {chemin absolu du dossier courant}`. C'est l'indication humaine, propre
   au poste ; elle n'est pas la clé de résolution entre machines.
3. Si le dossier est dans un dépôt git avec un remote `origin` (`git remote get-url origin` répond),
   poser `repo:` avec l'URL telle que git la rend, par exemple `https://github.com/org/repo` ou
   `git@github.com:org/repo.git`. C'est la forme que `_Meta/Schema.md` attend (URL du remote). Le
   résolveur normalise lui-même les deux côtés (schéma, `user@`, suffixe `.git`, casse) : deux URL du
   même dépôt se reconnaissent quelle que soit leur écriture. `repo:` est la clé portable entre
   machines, lue par `sync-repo` et par le hook Stop du plugin.
4. Si le dossier courant n'est pas la racine du dépôt (`git rev-parse --show-toplevel` diffère de
   `$PWD`), suffixer `repo:` par `#{chemin relatif à la racine du dépôt}`, par exemple
   `https://github.com/org/repo#apps/api`.
5. Si le dossier de travail porte un `CLAUDE.md` qui importe le vault (`@~/vault/…`), approuver ses
   imports externes avec
   `"${CLAUDE_PLUGIN_ROOT}/hooks/vault-approve-imports.sh" "{chemin absolu du dossier courant}"`.
   Sans cette approbation, Claude Code ignore ces imports en silence à chaque
   session. La commande est idempotente et n'approuve que des cibles situées dans un vault ; le hook
   SessionStart du plugin ferait le même geste à la session suivante. Sans `CLAUDE.md` dans le
   dossier, rien à faire.
6. Confirmer à l'utilisateur en une ligne, avec les valeurs posées : « je relie ce dossier au projet
   {slug} ».

Sans dossier de travail (session lancée dans le vault), les deux champs sont omis. Ne rien inventer.
