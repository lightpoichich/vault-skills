---
name: ranger
description: >-
  Fait entrer un savoir dans le vault et le classe dans la bonne zone PARA, avec frontmatter
  conforme au Schema et wikilinks : un contenu externe (URL, page Notion, fichier, texte collé), ou
  une pratique répétée dans le vault, généralisée en trame dans 30-Resources/. Pose un renvoi
  plutôt qu'une copie pour le sensible. S'utilise quand l'utilisateur dit « importe cette note »,
  « range cette page Notion / cet article », « ajoute ça à mon projet X », colle un texte à ranger,
  ou dit « fais-en une trame », « ça, je le refais à chaque fois ». Pour mettre à jour les fiches
  après une session, voir sync-vault.
---

# Ranger

Deux sources, un seul classement. Un contenu venu de l'extérieur s'importe ; une pratique déjà
réalisée plusieurs fois dans le vault se généralise en trame. Dans les deux cas, la zone PARA, le
frontmatter, les liens et la règle du renvoi suivent `references/classement.md`.

## Procédure

### 1. Localiser le vault
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `projet`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé.

### 2. Aiguiller

| Entrée | Mode | Procédure |
|---|---|---|
| URL, page Notion, fichier, texte collé, modèle qui existe déjà hors du vault | import | `references/importer.md` |
| pratique déjà faite au moins deux fois dans le vault (« fais-en une trame »), candidat signalé par `sync-vault` | trame | `references/trame.md` |

Un modèle venu de l'extérieur s'importe : la trame ne se fonde que sur des occurrences réelles du
vault.

### 3. Suivre le mode
Dérouler la référence du mode, puis confirmer le chemin, la zone et les liens posés.

## Garde-fous
- **Ranger, pas déverser** : un contenu posé sans frontmatter ni lien n'a rien rangé. Le travail est
  le classement.
- **Rien d'inventé** : un import enlève le bruit sans réécrire le fond ; chaque section d'une trame
  trace vers un cas réel.
- **Renvoi, jamais copie** pour une source 🔒 ou une source de vérité qui évolue ailleurs
  (`references/classement.md`, section 1, et `governance.md`).
- **Non destructif** : chercher une fiche existante avant de créer, enrichir plutôt que dupliquer,
  ne rien écraser sans demander.
- **Validation** : l'import confirme la zone cible quand elle n'est pas nommée ; la trame attend la
  validation de sa généralisation avant d'écrire.

## Références
- `references/importer.md` : procédure d'import, de la détection de l'entrée à la confirmation.
- `references/acquisition.md` : détecter la nature de l'entrée et l'acquérir par type ;
  `obsidian:defuddle` en option avec repli.
- `references/trame.md` : procédure de trame, des occurrences aux liens bidirectionnels.
- `references/generalisation.md` : critère de codification, commun, variantes et placeholders,
  inférence du rangement, garde-fous de la trame.
- `references/classement.md` : renvoi ou copie, renvoi d'emplacement, doc brut avec fiche
  compagnon, zone PARA, frontmatter, liens bidirectionnels.
