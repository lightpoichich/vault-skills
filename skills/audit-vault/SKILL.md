---
name: audit-vault
description: >-
  Contrôle technique périodique d'un vault Obsidian PARA : détecte les wikilinks cassés, fiches
  orphelines, frontmatter hors Schema, naming hors kebab-case, pollution (.DS_Store, dossiers
  vides), Inbox stale, projets à archiver (inactifs, deadline dépassée), areas mortes / obèses /
  sans consommateur, personas aux zones invalides — produit un rapport daté dans `00-Inbox/`
  puis propose le traitement. Utilise ce skill dès que l'utilisateur dit « audit du vault »,
  « fais le ménage », « fais le point sur le vault », « c'est le bazar », « qu'est-ce qui
  traîne », « wikilinks cassés », ou sur rituel mensuel d'hygiène. **Transverse**, 100 % vault
  (aucun connecteur). NE PAS l'utiliser pour répercuter la session en cours (`sync-vault`),
  exécuter une restructuration d'area (`gerer-area`), compléter un projet (`nouveau-projet`),
  ni faire entrer du contenu (`import-note`).
---

# Audit vault

Le contrôle technique du **contenant** — là où `sync-vault` cure le **contenu** au fil des
sessions. Trois phases strictement séparées : **détecter** (lecture seule), **rapporter** (un
fichier, une synthèse courte), **agir** (seulement sur validation). C'est la réponse aux
« 3-4 h/mois » : un rituel outillé, pas de la vigilance diffuse.

## Principes à garder en tête

- **La détection est en lecture seule.** Pendant les phases 1-2, **aucune écriture** dans le
  vault (hors le rapport lui-même) : pas de suppression « évidente », pas de frontmatter
  complété au passage, pas de note reclassée parce que c'est tentant. Trouver n'est pas un
  mandat pour corriger.
- **Le rapport est un fichier, pas un déversement.** Les findings vivent dans
  `00-Inbox/audit-vault-{date}.md` ; la conversation n'en montre que la synthèse compacte.
- **Réparer n'est jamais inventer.** Un fix mécanique restaure une règle du Schema (renommer en
  kebab-case, supprimer la pollution) ; il ne fabrique aucun contenu (pas de `date: "à
  préciser"` inventée, pas de section ajoutée, pas de reclassement de note — ça, c'est du
  jugement → lots B/C).
- **Frontière sync-vault** : les candidats à trame, renvois externes périmés et la consolidation
  des fiches sont son territoire — ne pas dupliquer.

## Procédure

### 1. Localiser le vault et détecter
Remonter jusqu'à la racine (`CLAUDE.md` + `_Meta/Schema.md`). **Si la remontée ne trouve aucune racine**
(cwd hors du vault — un dossier de travail externe sur le filesystem), utiliser le **chemin absolu du
vault** déclaré dans le `~/.claude/CLAUDE.md` global (règle de liaison) plutôt que d'échouer. Lire le
Schema (source de vérité
des types et champs requis de **ce** vault). Dérouler les trois familles de checks de
`references/checks.md` :
1. **Intégrité structurelle** — liens, orphelines, frontmatter, naming, structure, pollution.
2. **Fraîcheur / archivage** — Inbox stale, projets à archiver, briefs et vieux audits.
3. **Squelette** — areas mortes / obèses / sans consommateur, zones de personas invalides.

### 2. Écrire le rapport, donner la synthèse
Rapport `00-Inbox/audit-vault-{YYYY-MM-DD}.md` (écrasé si relancé le même jour) :
- frontmatter `type: audit` — si le Schema ne connaît pas ce type, **inscrire son ajout au
  lot A** (règle du Schema : un type nouveau plutôt qu'un type détourné) — le Schema ne se
  modifie pas pendant la phase rapport, seule écriture admise : le rapport lui-même ;
- findings groupés par sévérité **🚨 / ⚠️ / 💡**, et pour chacun : la fiche concernée, le
  constat en une ligne, **l'action proposée**, et son **lot** :
  - **[A — mécanique]** : restauration de règle sans jugement ni contenu inventé ;
  - **[B — délégué]** : le geste appartient à un skill dédié (`gerer-area` pour archiver/scinder
    une area, `nouveau-projet` pour un shell à compléter, `sync-vault` pour le contenu) ;
  - **[C — décision humaine]** : recaler une deadline, trancher un lien cassé, créer ou non une
    zone de persona.

Dans la conversation, **synthèse compacte uniquement** (5 lignes max) :
```
🔍 Audit vault : N fiches (🚨 X · ⚠️ Y · 💡 Z)
🚨 Top critical : [[fiche]] — constat + action courte (max 3 détaillés)
⚠️ / 💡 : compteurs + exemples nommés
→ Rapport : 00-Inbox/audit-vault-{date}.md — lot A (n fixes mécaniques) prêt, on traite ?
```
0 finding → `✅ Vault clean : N fiches scannées.` et s'arrêter là. Ne **jamais** recopier le
rapport dans la conversation.

### 3. Agir — seulement sur validation
- **Lot A** (mécanique) : présenter la liste d'un bloc → **un seul oui** suffit → proposer un
  commit git du vault avant → exécuter exactement la liste, rien d'autre → rapport d'exécution.
  Un fichier qui résiste : signaler, ne pas improviser.
- **Lot B** (délégué) : proposer un par un de lancer le skill dédié — chaque skill applique sa
  propre discipline (pré-checks, plan, validation). Ne pas refaire son travail à sa place.
- **Lot C** : rester dans le rapport. Pas de relance, pas d'exécution.
- L'utilisateur décline → le rapport reste, c'est tout.

## Références
- `references/checks.md` — les heuristiques par famille, les seuils par défaut (ajustables à la
  demande), les exemptions (ce qui n'est PAS un finding).
