---
name: extraire-trame
description: >-
  Capitalise une pratique récurrente du vault en trame réutilisable dans 30-Resources/ : retrouve
  les occurrences réelles, Archive comprise, en extrait la forme commune sans rien inventer, la
  range dans la bonne sous-zone et la lie à ses fiches sources. Propose la généralisation et attend
  la validation avant d'écrire. S'utilise quand l'utilisateur dit « ça, je le refais à chaque
  fois », « fais-en une trame », « on a déjà fait ça trois fois », « capitalise cette méthode », ou
  reprend un candidat signalé par sync-vault. Pour un modèle qui existe déjà hors du vault, voir
  import-note.
---

# Extraire une trame

Codifier en `30-Resources/` la forme commune d'une pratique déjà réalisée plusieurs fois dans le
vault. Les docs bruts et les modèles venus de l'extérieur relèvent d'`import-note`.

## Garde-fous

- **Rien d'inventé** : chaque section de la trame trace vers au moins un cas réel du vault.
  Critère de codification, variantes et placeholders dans `references/generalisation.md`.
- **Savoir, pas livrable** : une trame reste dans le vault, donc écriture directe sans passage par
  `_drafts/` (`governance.md`). La validation demandée porte sur le jugement de généralisation,
  pas sur une sortie vers un tiers.
- **Pas de 🔒 dans une trame** : règle détaillée dans `references/generalisation.md`, section
  garde-fous.
- **Vocabulaire de l'utilisateur** : dire « trame », « modèle », « méthode », pas « template » ni
  « pattern ».

## Procédure

### 1. Localiser le vault
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé.

### 2. Cerner le candidat
Partir de ce que l'utilisateur désigne (« la façon dont je prépare mes comités ») ou d'un candidat
à trame signalé par le compte-rendu de `sync-vault`. Reformuler en une ligne ce qu'on cherche à
codifier et le faire confirmer.

### 3. Retrouver les occurrences réelles
`Grep` et `Glob` dans `10-Projects/`, `20-Areas/` et `40-Archive/` : un projet clos est une
occurrence valide. Lister les occurrences trouvées avec leurs chemins. Appliquer le critère de
codification de `references/generalisation.md` (deux occurrences au moins).

### 4. Généraliser
Suivre `references/generalisation.md` : squelette commun, variantes conditionnelles,
`{placeholders}` à la place des spécifiques. Montrer la proposition complète et la faire valider
avant d'écrire. C'est le seul moment où ce skill attend l'utilisateur.

### 5. Placer
Inférer la logique de rangement depuis l'arborescence existante de `30-Resources/`, par type ou par
domaine (table de signaux dans `references/generalisation.md`). Proposer la sous-zone et un nom
kebab-case : `trame-{objet}.md`, ou le nom que l'utilisateur donne à cette pratique.

### 6. Frontmatter
Poser le `type: resource` de ce vault d'après `_Meta/Schema.md`, plus `source:` listant les cas
fondateurs en `[[wikilinks]]`. Si le Schema n'a pas de type `resource`, ajouter le bloc minimal au
Schema (sa propre consigne : ajouter un type plutôt qu'en détourner un) et le signaler.

### 7. Wikilinks bidirectionnels
Poser les liens décrits dans `references/generalisation.md` : la trame liste ses cas sources,
chaque fiche source gagne une ligne `Trame : [[{trame}]]`, le `_index.md` de la sous-zone est mis à
jour s'il existe.

### 8. Confirmer
Afficher le chemin créé, les occurrences fondatrices et les liens posés.

## Références
- `references/generalisation.md` : critère de codification, méthode commun / variantes /
  placeholders, inférence du rangement, liens bidirectionnels, garde-fous (🔒, cas unique, trame
  existante à enrichir).
- `import-note/references/classement.md` : classement universel (frontmatter, liens, renvoi ou
  copie).
