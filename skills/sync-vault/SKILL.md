---
name: sync-vault
description: >-
  Curateur autonome du vault : à tout moment, réconcilie les fiches avec la réalité du travail
  (décisions, statuts, todos, faits/contacts nouveaux) **et les garde concises** — il met à jour,
  consolide, réécrit et élague le bruit accumulé pour éviter la surcharge append-only, tout en
  préservant ce qui compte pour le contexte. **Cure aussi le sas `00-Inbox/_drafts/`** : archive les
  livrables envoyés en trace sur leur projet/client et balaie les périmés — sans jamais valider ni
  envoyer à la place de l'humain. **Agit seul, sans validation humaine, et peut écraser**
  quand c'est plus propre. Utilise ce skill dès que l'utilisateur dit « sync le vault », « mets à jour
  le vault », « on a oublié le vault », « répercute ce qu'on a décidé », « consolide / nettoie / allège
  le vault », ou quand le vault s'est chargé et doit être remis au propre. **Transverse** et
  **source-agnostique** : il raisonne sur la conversation en cours (pas besoin de git côté dirigeant)
  et lit `_Meta/sources.md` si une source externe doit être réconciliée. Famille « Entretenir »
  (maintain) : garde le vault **vrai et sobre** et alimente la **mémoire native de Claude Code**
  (auto-recall) pour que les personas rappellent l'essentiel d'une session à l'autre, en veillant à ce
  qu'elle soit active. NE PAS l'utiliser pour faire entrer une note externe
  (`import-note`), pour le brief du jour (`brief-du-jour`), pour créer un projet (`nouveau-projet`), ni
  pour un audit/diagnostic structural large produisant un rapport (skills d'hygiène à venir).
---

# Sync vault

Le **curateur autonome** du vault. À tout moment, `sync-vault` réconcilie les fiches avec la réalité du
travail et les garde **concises et utiles** : il met à jour, consolide, réécrit ce qui doit l'être, et
élague le bruit accumulé — tout en préservant ce qui compte pour le contexte. Il agit **seul**, sans
demander de validation.

C'est un skill de **Famille 3 (Entretenir)** : son intention est la **fiabilité et la sobriété** du
vault. Un vault utile est à jour *et* dense — pas un journal append-only qui gonfle jusqu'à noyer le
signal sous lequel les personas et les sessions futures doivent retrouver le contexte.

## Les deux mémoires

`sync-vault` entretient **deux couches** : (1) les **fiches du vault** — le fonds, tout, consultable
dans Obsidian ; (2) la **mémoire native de Claude Code** — la couche de *rappel*, un petit digest
chargé automatiquement au démarrage de chaque session, pour que les personas partent en connaissant
l'essentiel sans relire le vault. Le fonds est exhaustif ; le rappel est court et trié. Mécanisme et
détails : `references/memoire-claude-code.md`.

## Quand il agit

Invocable **à n'importe quel moment** — il n'est lié à aucune fin de session. Le signal de « ce qui a
bougé », pour un dirigeant non-tech, n'est pas un commit : **c'est ce qui s'est dit et décidé dans la
conversation en cours**, dont le modèle a le contexte. (Si le vault a un dépôt git, les commits
récents *peuvent* compléter le signal — optionnel, jamais requis.)

## Principe à garder en tête

- **Autonome.** `sync-vault` décide et écrit **sans demander de validation**. Il rend compte *après*.
- **Pas append-only.** Il peut **écraser, fusionner, réécrire** : c'est son rôle d'empêcher les fiches
  de gonfler. On remplace le périmé, on fusionne les redites, on retire le bruit.
- **Garder l'essentiel pour le contexte.** Décisions (+ leur raison), statut courant, engagements
  vivants, faits structurants, liens `[[]]`. Dans le doute sur l'importance d'un élément → **garder**.
- **Rien à faire = ne rien forcer.** Si rien n'a bougé et qu'aucune fiche n'a besoin d'être allégée, le
  dire et s'arrêter.
- **Les drafts sont des livrables, pas du savoir.** `sync-vault` les fait **sortir** du sas (archive
  l'envoyé en trace, balaie le périmé) mais ne les **valide ni ne les envoie** jamais — la gate humaine
  tient. Le savoir interne, lui, s'écrit directement (pas de draft).
- **La mémoire de Claude Code reste un digest.** On y distille l'essentiel transversal et on la garde
  courte (budget de rappel limité) — jamais le contenu détaillé du vault, jamais de 🔒.
- **Garde-fous non négociables.** Le sensible 🔒 n'est **jamais** copié ni exposé (renvoi seulement,
  `governance.md`). On respecte le contrat du `_Meta/Schema.md`.

## Procédure

### 1. Localiser le vault
Remonter jusqu'à la racine (présence de `CLAUDE.md` + `_Meta/Schema.md`).

### 2. Repérer ce qui a bougé et ce qui dérive
- Les **mouvements** du travail : décisions, changements de statut, deadlines, todos nés/faits, faits
  et contacts nouveaux (conversation en cours ; + commits si dépôt git).
- Les **fiches qui se sont chargées** : sections redondantes, infos périmées, todos faits depuis
  longtemps, verbiage qui noie le contexte.

Si une source externe doit être réconciliée (ex. un transcript), lire `_Meta/sources.md` et appliquer
la cascade. En passant, **garder le registre vrai dans les deux sens** — toujours sur joignabilité
**constatée dans la session**, jamais sur parole :
- **Démoter / élaguer** : un `statut` qui ment (déclaré `actif` mais injoignable) repasse `à brancher` ;
  un indice `accès` périmé est élagué. Signaler sans broder, ne jamais inventer de schéma.
- **Promouvoir / ajouter** (geste symétrique) : une source déclarée `à brancher` qui s'est révélée
  **joignable** (sonde `ToolSearch` positive ou usage réussi pendant la réconciliation) passe `actif` ;
  un connecteur observé joignable mais **absent** du registre y est ajouté en ligne `actif`. Ne jamais
  inventer le `usage` ; ne remplir `accès` que si une heuristique d'appel étroit a émergé du sondage.
  Une source `renvoi 🔒` n'est **jamais** promue.

### 3. Réconcilier et consolider (voir `references/curation.md`)
Pour chaque fiche concernée (`Glob`/`Grep` pour la retrouver ; `_Meta/Schema.md` pour le type) :
- **intégrer** les faits nouveaux à la bonne section ;
- **remplacer** le périmé par l'à-jour (ne pas empiler) ;
- **fusionner** les redites en une formulation dense et courante ;
- **élaguer** le bruit, en **préservant l'essentiel** pour le contexte.

### 4. Écrire (directement, overwrite autorisé)
Appliquer les changements **sans validation préalable** : mises à jour de frontmatter, sections
réécrites/fusionnées, élagages. Laisser les hooks poser `updated`. Ne jamais toucher au 🔒 autrement
qu'en renvoi.

### 5. Curer le sas `00-Inbox/_drafts/` (livrables sortants, voir `references/curation.md`)
Les drafts sont des **livrables externes** en attente (mail, courrier, proposition…), pas du savoir.
`sync-vault` gère leur **sortie**, jamais leur validation :
- **`statut: envoyé`** → **archiver en trace** : sortir la fiche de `_drafts/` vers le dossier de son
  `lien` (projet/client), passer `statut: archivé`. Bookkeeping interne → autonome, autorisé.
- **`statut: en-attente` périmé** (`date` ancienne, ~14 j sans bouger) → le laisser remonter par le
  brief ; au-delà d'un seuil long (~30 j) → archiver `abandonné` dans `40-Archive/`. **Jamais supprimé
  sans trace.**
- **Garde-fou** : ne **jamais** passer un draft `en-attente → validé` ni `validé → envoyé` (décisions
  humaines), ne **jamais** archiver un livrable encore en attente de validation.

### 5bis. Veiller sur `30-Resources/` (voir `references/curation.md`)
Tenue de registre **autonome** : `_index.md` cochés quand la ressource existe, wikilinks cassés
réparés, liens bidirectionnels maintenus sur les ressources touchées par la session. Le reste se
**signale au compte-rendu, jamais traité seul** : formes répétées (candidates à `extraire-trame` —
l'extraction reste un geste humain), ressources orphelines (candidates archive), renvois externes
possiblement périmés.

### 6. Alimenter la mémoire native de Claude Code (voir `references/memoire-claude-code.md`)
- **L'activer si besoin** : s'assurer que la mémoire auto est active (`autoMemoryEnabled: true` dans
  `settings.json`) et l'activer sinon — sans ça, ce qui est écrit ne sera pas rappelé.
- **Distiller l'essentiel transversal** dans le dossier mémoire du projet (`MEMORY.md` + fichiers
  thématiques) : priorités courantes, statut des projets actifs en une ligne, décisions et préférences
  durables, qui-est-qui. Pas le détail (il reste dans le vault) — juste ce qu'une persona doit savoir
  **dès le démarrage** de sa prochaine session.
- **Garder `MEMORY.md` court** (seul fichier rechargé au démarrage, rappel plafonné ~200 lignes /
  25 Ko) : remplacer le périmé, fusionner, élaguer — même discipline anti append-only que pour les
  fiches. Jamais de 🔒 en mémoire.

### 7. Rendre compte
Résumer **après coup** ce qui a été mis à jour, consolidé et élagué — **fiches du vault, drafts curés,
signalements Resources (candidats à trame, orphelines, renvois à vérifier) et entrées de mémoire
Claude Code** (chemins + nature des changements), pour que le dirigeant garde la visibilité.

## Références
- `references/curation.md` — quoi intégrer, quoi garder, quoi élaguer/réécrire ; et les garde-fous.
- `references/memoire-claude-code.md` — la mémoire native de Claude Code : où elle vit, comment
  l'activer, quoi y distiller.
- Classement / frontmatter / liens : `import-note/references/classement.md`.
