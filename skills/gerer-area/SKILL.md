---
name: gerer-area
description: >-
  Gère le cycle de vie complet d'une Area dans un vault Obsidian **déjà vivant** : fait **naître**
  une nouvelle responsabilité (`20-Areas/{slug}/` + fiche conforme au Schema), **complète** un
  shell vide, **renomme**, **scinde**, **fusionne**, ou **archive** une area dont la
  responsabilité a disparu. Utilise ce skill dès que l'utilisateur dit « crée une area »,
  « nouvelle area », « renomme / scinde / fusionne l'area X », « archive l'area X », « cette
  responsabilité n'existe plus », « l'area X est vide », ou qu'un audit suggère une
  restructuration d'areas. **Transverse**, 100 % vault (aucun connecteur requis). **Réactif** :
  il exécute un geste demandé — le diagnostic de dérive appartient aux skills d'hygiène. NE PAS
  l'utiliser pour scaffolder le vault entier (`kickstart-vault`), créer un projet
  (`nouveau-projet`), faire entrer une note externe (`import-note`), ni répercuter une session
  (`sync-vault`).
---

# Gérer une area

Le geste qui gère **l'épine dorsale** du vault. Une area, contrairement à un projet, ne se
termine jamais : elle naît rarement, mais elle **évolue** — grossit, se scinde, absorbe une
voisine, ou meurt quand la responsabilité disparaît. Et tout s'y rattache : les projets (par
frontmatter `area:` + wikilink), les personas (par leurs zones de lecture/écriture), le brief.
Toucher une area, c'est toucher le squelette.

## Principes à garder en tête

- **Plan-puis-exécute pour tout geste multi-fichiers** (renommer, scinder, fusionner, archiver) :
  on construit le plan exhaustif, on l'affiche, **on attend la validation**, on propose un commit
  git du vault, puis on exécute. **Jamais d'exécution directe** — même si la demande semble sans
  ambiguïté. Une découverte bloquante (projet actif rattaché, collision de noms) se traite
  **avant** d'agir, pas dans le rapport final.
- **Références structurelles seulement.** On réécrit ce qui *pointe* vers l'area : wikilinks
  `[[slug]]`, frontmatter `area:`, chemins dans les zones des personas. On ne touche **jamais**
  aux champs sémantiques (`domaine:`, `tags:`, le wording d'un titre) et on n'invente aucun
  contenu — en cas de doute sur un champ, demander.
- **Les personas sont signalées, jamais modifiées en silence.** Tout changement à un
  `_personas/{slug}/CLAUDE.md` apparaît dans le plan, et si une persona se retrouve **sans zone**,
  on alerte au lieu de la vider.
- **Generate-don't-write.** À la naissance : un shell conforme, des sections vides. Le contenu
  entre par l'usage.
- **Renvoi-jamais-copie pour le 🔒** (voir `governance.md`).

## Procédure

### 1. Localiser le vault
Remonter depuis le dossier courant jusqu'à la racine (présence de `CLAUDE.md` + `_Meta/Schema.md`).

**Si la remontée ne trouve aucune racine** (cwd hors du vault — un dossier de travail externe sur le
filesystem), utiliser le **chemin absolu du vault** déclaré dans le `~/.claude/CLAUDE.md` global (règle
de liaison) plutôt que d'échouer : lire et écrire le vault à ce chemin absolu.

### 2. Aiguiller selon l'intention

| Demande | Geste | Procédure |
|---|---|---|
| « crée l'area X », « nouvelle responsabilité » | **Naître** | étapes 3-5 ci-dessous |
| « complète / remplis l'area X », « X est vide » | **Compléter** | étape 4 (trous seulement) |
| « renomme l'area X en Y » | **Renommer** | `references/restructurer.md` |
| « scinde X », « fusionne X et Y » | **Scinder / fusionner** | `references/restructurer.md` |
| « archive X », « je ne m'en occupe plus » | **Archiver** | `references/archiver.md` |

Avant de créer : `Glob` sur `20-Areas/` (et `40-Archive/` → proposer de **désarchiver** plutôt
que recréer). Une area proche existe → le signaler et confirmer avant de créer.

### 3. Naître — recueillir les invariants (court, interactif)
Lire le contrat `area` de `_Meta/Schema.md` (source de vérité de **ce** vault), puis demander —
sans noyer le dirigeant :
- **nom** (→ titre + slug `kebab-case`) ;
- **la responsabilité en une ligne** (ce que couvre l'area) ;
- **objets récurrents**, **cadence**, **outils** (ou « à préciser »).

**La question anti-cimetière : « qui la lit ? »** Chaque dossier a un consommateur. Proposer de
rattacher l'area aux zones d'une persona existante (lecture et/ou écriture — c'est une
modification de son `CLAUDE.md`, à valider). Aucun consommateur → créer quand même, mais le
signaler explicitement : une area que rien ne lit est un cimetière en devenir.

### 4. Poser le shell (ou combler les trous)
- Créer `20-Areas/{slug}/{slug}.md` — **jamais une fiche à plat**. Frontmatter `type: area`
  rempli avec les invariants, titre, la ligne de responsabilité, section `## Notes` vide.
  Laisser les hooks du vault poser `created`/`updated`.
- **Mode compléter** (shell posé par `kickstart-vault`) : comparer la fiche au contrat `area` du
  Schema, demander **seulement les invariants manquants**, remplir uniquement les champs et
  sections vides. **Non destructif** — ne jamais réécrire ce qui est renseigné.

### 5. Raccrocher au vault
- **Projets existants concernés** : proposer de rattacher (frontmatter `area: "[[{slug}]]"` +
  wikilink bidirectionnel — la fiche area liste ses projets).
- **Nourrir** en option : déléguer à `import-note` (note d'inbox, doc, URL qui fonde l'area).
- Mettre à jour un MOC/index s'il en existe un.
- Confirmer : chemin créé, frontmatter posé, rattachements, consommateur déclaré.

## Références
- `references/restructurer.md` — renommer, scinder, fusionner : la mécanique transactionnelle.
- `references/archiver.md` — pré-checks bloquants, promotion en Resources, retrait des personas.
- Contrat `area` du vault : `_Meta/Schema.md` (lu à l'étape 3).
