---
name: extraire-trame
description: >-
  Capitalise une pratique récurrente du vault en **trame réutilisable** dans `30-Resources/` :
  retrouve les occurrences réelles (Projects/Areas/Archive), en extrait la forme commune — rien
  d'inventé, chaque section vient des cas réels —, la range dans la bonne sous-zone et pose les
  `[[wikilinks]]` bidirectionnels (trame ↔ fiches sources). Utilise ce skill dès que l'utilisateur
  dit « ça, je le refais à chaque fois », « fais-en une trame / un modèle », « on a déjà fait ça
  trois fois », « capitalise cette méthode », « transforme ça en modèle réutilisable », ou reprend
  un candidat à trame signalé par `sync-vault`. **Consultatif** (la généralisation est un jugement :
  il propose, le dirigeant valide avant écriture), **transverse**, et ne lit que le vault (aucun
  connecteur requis). NE PAS l'utiliser pour faire entrer un contenu externe — y compris un doc
  brut, un PDF ou un modèle qui existe déjà ailleurs (`import-note`) —, pour créer un projet
  (`nouveau-projet`), pour la curation autonome du vault (`sync-vault`, qui *signale* les candidats
  à trame mais n'extrait jamais), ni pour rédiger un livrable sortant (sas `00-Inbox/_drafts/`).
---

# Extraire une trame

Faire **émerger** un savoir qui existe en creux dans le vault. Le troisième geste de la Famille 2 :
`import-note` fait *entrer* un contenu qui existe dehors, `nouveau-projet` fait *naître* un effort
neuf, `extraire-trame` fait *émerger* la forme commune de ce qui a déjà été fait plusieurs fois — et
la codifie en **trame réutilisable** dans `30-Resources/`.

Une trame n'est qu'une partie de ce qui vit dans `30-Resources/` : le dossier accueille aussi des
**docs bruts** entrés par `import-note` (PDF, CGV, design system, plaquettes…) et des renvois
externes. Ce skill ne produit que les trames — la part du référentiel qui **naît de l'usage**.

## Principe à garder en tête

- **Generate-don't-write, version extraction.** Chaque section de la trame **trace vers au moins un
  cas réel** du vault. Ce qui diverge entre les cas devient une **variante signalée** (« si
  {contexte} → … »), pas une moyenne inventée. Ce qu'aucun cas ne couvre n'existe pas dans la trame.
- **≥ 2 occurrences réelles avant de codifier.** Une pratique vue une seule fois n'est pas encore une
  trame : le dire, proposer d'attendre la récidive. Codifier sur un cas unique seulement si le
  dirigeant insiste — et le marquer dans la trame.
- **Une trame = du savoir, pas un livrable.** Destination = le vault → **écriture directe**, pas de
  passage par `_drafts/` (règle Savoir vs Livrable, `governance.md`). La validation demandée ici
  porte sur le **jugement de généralisation**, pas sur une sortie vers un tiers.
- **Jamais de 🔒 dans une trame.** La généralisation retire les spécifiques par construction : aucun
  nom, chiffre ou donnée sensible d'un cas ne migre dans la trame. Les `{placeholders}` remplacent,
  les `[[wikilinks]]` renvoient.

## Procédure

### 1. Localiser le vault
Remonter depuis le dossier courant jusqu'à la racine (présence de `CLAUDE.md` + `_Meta/Schema.md`).

### 2. Cerner le candidat
Ce que l'utilisateur désigne (« la façon dont je prépare mes comités »), ou un **candidat à trame**
signalé par le compte-rendu de `sync-vault`. Reformuler en une ligne ce qu'on cherche à codifier, et
le faire confirmer.

### 3. Retrouver les occurrences réelles
`Grep`/`Glob` dans `10-Projects/`, `20-Areas/` **et `40-Archive/`** (un projet clos est une
occurrence valide). Lister les occurrences trouvées, avec leurs chemins. Moins de 2 → appliquer le
critère ci-dessus.

### 4. Généraliser (voir `references/generalisation.md`)
Extraire le **squelette commun** (étapes, sections, questions types), marquer les **variantes**,
remplacer les spécifiques par des `{placeholders}`. **Montrer la proposition complète et la faire
valider avant d'écrire** — c'est le seul moment où ce skill attend l'humain.

### 5. Placer
Inférer la logique de rangement depuis l'**arborescence existante** de `30-Resources/` — sous-zones
par type (`methodologies/`, `trames/`, `runbooks/`…) ou par domaine (table de signaux dans le
guide). Proposer la sous-zone et un nom **kebab-case** (`trame-{objet}.md`, ou le nom que le
dirigeant donne à cette pratique).

### 6. Frontmatter
Lire `_Meta/Schema.md` et poser le `type: resource` de **ce** vault, plus `source:` listant les cas
fondateurs en `[[wikilinks]]`. Si le Schema n'a pas de type `resource` → ajouter le bloc minimal au
Schema (sa propre consigne : ajouter un type plutôt qu'en détourner un) et le signaler.

### 7. Wikilinks bidirectionnels
- La trame liste ses cas sources (`[[…]]`) — d'où elle vient.
- Chaque fiche source gagne une ligne `Trame : [[{trame}]]` près du passage concerné — la prochaine
  fois qu'on rouvre ce dossier, la trame est sous les yeux.
- Mettre à jour le `_index.md` de la sous-zone s'il existe (cocher ou ajouter l'item).

### 8. Confirmer
Afficher le chemin créé, les occurrences fondatrices, les liens posés.

S'adresser au dirigeant dans ses mots : « trame », « modèle », « méthode » — pas *template* ni
*pattern*.

## Références
- `references/generalisation.md` — critère de codification, méthode commun/variantes/placeholders,
  inférence du rangement, garde-fous.
- Classement universel (frontmatter, liens, renvoi-vs-copie) : `import-note/references/classement.md`.
