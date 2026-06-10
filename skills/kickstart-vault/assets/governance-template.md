---
type: moc
topic: governance
updated: {YYYY-MM-DD}
---

# Gouvernance & isolation du vault

> Posé **avant** tout contenu. **Règles durables** que tout agent respecte — pas un instantané.
> Sur un vault qui touche du sensible, c'est ce fichier qui protège la confiance dans le système.
>
> ⚠️ Si ce fichier a été **généré par défaut** (le plan ne contenait pas de section
> gouvernance), le relire et l'ajuster — surtout le périmètre et la liste 🔒.

## Périmètre
- Ce vault couvre : **{périmètre repris du plan — ex. "activité professionnelle X uniquement"}**.
- Hors périmètre : **{ce qui vit ailleurs — ex. "le perso, dans un vault séparé"}**. Aucune
  fusion des contextes.

## Savoir vs Livrable — la règle d'écriture
Toute écriture se range selon sa **destination**, pas selon qui l'écrit :
- **Savoir** — reste dans le vault (fiche, résumé de contexte, avancement, synthèse) → **écriture
  directe et autonome**, sans validation. C'est le rôle du vault de se tenir à jour seul.
- **Livrable** — sort vers un tiers (mail, courrier, proposition, post) → déposé dans
  `00-Inbox/_drafts/` en `type: draft` / `statut: en-attente`, **validé par un humain**. **Jamais
  d'envoi automatique.**

**Cycle de sortie des livrables** (porté par `sync-vault`, autonome) : un draft `envoyé` est archivé
comme **trace** sur son projet/client (champ `lien`) — le vault garde l'historique de ce qui a été
communiqué ; un draft resté `en-attente` trop longtemps est remonté dans le brief puis archivé
« abandonné ». `_drafts/` est un **sas de transit**, jamais un dépôt qui s'accumule. `sync-vault` ne
**valide** ni n'**envoie** jamais un livrable de lui-même — il ne réagit qu'aux statuts posés par l'humain.

## Accès des agents — la règle, pas la liste
- Par défaut, un agent lit/écrit **uniquement** dans les zones **non sensibles** que sa propre
  fiche l'autorise.
- **Le périmètre lecture/écriture concret de chaque agent est déclaré dans son
  `_personas/{slug}/CLAUDE.md`** — c'est la **source de vérité**, mise à jour là où l'agent vit.
  Ce fichier-ci **ne nomme AUCUN agent** — ni liste, ni tableau, ni parenthèse type
  « (agents prévus : …) » (ça se périmerait dès qu'on en ajoute/retire un). Il pose la règle ;
  les personas portent le détail.
- Tout accès à un élément **🔒** exige une autorisation explicite, fiche par fiche.

## Confidentialité 🔒
- Les éléments **🔒** (ex. RH, contrats, org chart, finances non publiques) ne sont **jamais
  copiés** dans le vault — uniquement référencés. **Interdits aux agents** sans règle explicite.
- Toute fiche ou section sensible porte le marqueur 🔒.

## Renvoi, jamais copie
- Les sources de vérité externes vivent **là où elles sont**. Le vault en garde un **renvoi**
  dans `30-Resources/references-externes/` : un lien + une ligne de contexte, **zéro contenu
  recopié**. Le vault référence, il ne duplique pas.
- Les **connecteurs** du dirigeant (MCP, sources locales) sont déclarés dans `_Meta/sources.md` —
  le registre que les skills lisent pour savoir d'où tirer leurs informations. Une source marquée `renvoi 🔒`
  dans ce registre **n'est jamais agrégée ni copiée** par un skill, seulement référencée.

## Sauvegarde & confidentialité technique
- {Stratégie de backup choisie par l'utilisateur — à compléter.}
- Pas de dépôt public ni de cloud non maîtrisé si le vault contient du sensible.
