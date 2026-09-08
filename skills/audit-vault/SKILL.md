---
name: audit-vault
description: >-
  Contrôle technique d'un vault Obsidian PARA : wikilinks cassés, fiches orphelines, frontmatter
  hors Schema, noms hors kebab-case, pollution, Inbox stale, projets à archiver, areas mortes ou
  sans consommateur, zones de personas invalides. Produit un rapport daté dans 00-Inbox/ puis
  propose le traitement par lots, sans écrire avant validation. S'utilise quand l'utilisateur dit
  « audit du vault », « fais le ménage », « fais le point sur le vault », « qu'est-ce qui traîne »,
  « c'est le bazar », « wikilinks cassés », ou sur rituel mensuel. Pour répercuter la session en cours dans les fiches,
  voir sync-vault.
---

# Audit vault

Trois phases séparées : détecter en lecture seule, rapporter dans un fichier, agir sur validation.

## Garde-fous

- **Détection en lecture seule** : pendant les phases 1 et 2, la seule écriture admise est le
  rapport. Pas de suppression, de frontmatter complété ni de note reclassée au passage.
- **Réparer sans inventer** : un fix mécanique restaure une règle du Schema (renommer, supprimer la
  pollution). Il ne fabrique aucun contenu : ni date « à préciser », ni section ajoutée, ni
  reclassement. Ce qui demande un jugement va en lot B ou C.
- **Frontière avec `sync-vault`** : candidats à trame, renvois externes périmés et consolidation des
  fiches sont son territoire, pas celui de l'audit.

## Procédure

### 1. Localiser le vault et détecter
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé : il fixe les types et les
champs requis.

Dérouler les trois groupes de checks de `references/checks.md` :
1. **Intégrité structurelle** : liens, orphelines, frontmatter, nommage, structure, pollution.
2. **Fraîcheur et archivage** : Inbox stale, projets à archiver, briefs et audits anciens, index
   désynchronisés.
3. **Areas et personas** : areas mortes, obèses ou sans consommateur, zones de personas invalides.

### 2. Écrire le rapport, donner la synthèse
Rapport `00-Inbox/audit-vault-{YYYY-MM-DD}.md`, écrasé si l'audit est relancé le même jour :
- frontmatter `type: audit`. Si le Schema ne connaît pas ce type, inscrire son ajout au lot A ; le
  Schema ne se modifie pas pendant cette phase ;
- findings groupés par sévérité `critique`, `alerte`, `info` (règle de tri dans
  `references/checks.md`). Pour chacun : la fiche concernée, le constat en une ligne, l'action
  proposée et son lot :
  - **Lot A, mécanique** : restauration d'une règle sans jugement ni contenu inventé.
  - **Lot B, délégué** : le geste appartient à un skill dédié (`gerer-area` pour archiver ou scinder
    une area, `nouveau-projet` pour un shell à compléter, `sync-vault` pour le contenu).
  - **Lot C, décision humaine** : recaler une deadline, trancher un lien cassé, créer ou non une
    zone de persona.

Dans la conversation, synthèse compacte de cinq lignes au plus, sans recopier le rapport :
```
Audit vault : N fiches scannées (critique X, alerte Y, info Z).
Critique : [[fiche]], constat et action courte (trois détaillés au plus).
Alerte et info : compteurs et exemples nommés.
Rapport : 00-Inbox/audit-vault-{date}.md. Lot A prêt (n fixes mécaniques), on traite ?
```
Sans finding : `Vault propre : N fiches scannées.` et s'arrêter là.

### 3. Agir, seulement sur validation
- **Lot A** : présenter la liste d'un bloc, un seul oui suffit. Proposer un commit git du vault,
  exécuter exactement la liste, rendre un rapport d'exécution. Si un fichier résiste, le signaler
  sans improviser.
- **Lot B** : proposer un par un de lancer le skill dédié. Chaque skill applique sa propre
  discipline (pré-checks, plan, validation) ; ne pas refaire son travail à sa place.
- **Lot C** : rester dans le rapport, sans relance ni exécution.
- Si l'utilisateur décline, le rapport reste et c'est tout.

## Références
- `references/checks.md` : heuristiques par groupe, seuils par défaut ajustables à la demande,
  exemptions, règle de tri des sévérités.
