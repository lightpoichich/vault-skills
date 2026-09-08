---
type: moc
topic: governance
updated: {YYYY-MM-DD}
---

# Gouvernance et isolation du vault

> Posé avant tout contenu. Règles durables que tout agent respecte, pas un instantané.

## Périmètre
- Ce vault couvre : {périmètre repris du plan, par exemple « activité professionnelle X uniquement »}.
- Hors périmètre : {ce qui vit ailleurs, par exemple « le perso, dans un vault séparé »}. Pas de
  fusion des contextes.

## Savoir et livrable : la règle d'écriture
Toute écriture se range selon sa destination, pas selon qui l'écrit.
- **Savoir** : reste dans le vault (fiche, résumé de contexte, avancement, synthèse). Écriture
  directe et autonome, sans validation ; le vault se tient à jour seul.
- **Livrable** : sort vers un tiers (mail, courrier, proposition, post). Déposé dans
  `00-Inbox/_drafts/` en `type: draft`, `statut: en-attente`, validé par un humain. Pas d'envoi
  automatique.
- **Cycle de sortie** (porté par `sync-vault`) : un draft `envoyé` est archivé comme trace sur son
  projet ou client (champ `lien`) ; un draft resté `en-attente` trop longtemps est remonté dans le
  brief puis archivé « abandonné ». `_drafts/` est un sas de transit, pas un dépôt. `sync-vault` ne
  valide ni n'envoie un livrable ; il réagit aux statuts posés par l'humain.

## Accès des agents
- Par défaut, un agent lit et écrit uniquement dans les zones non sensibles que sa propre fiche
  l'autorise.
- Ce fichier ne nomme aucun agent ; chaque `_personas/{slug}/CLAUDE.md` déclare son périmètre.
- Tout accès à un élément 🔒 exige une autorisation explicite, fiche par fiche.

## Confidentialité 🔒
- Les éléments 🔒 (par exemple RH, contrats, organigramme, finances non publiques) ne sont pas
  copiés dans le vault, uniquement référencés. Ils sont interdits aux agents sans règle explicite.
- Toute fiche ou section sensible porte le marqueur 🔒.

## Renvoi, jamais copie
- Les sources de vérité externes vivent là où elles sont. Le vault en garde un renvoi dans
  `30-Resources/references-externes/` : un lien et une ligne de contexte, sans contenu recopié.
- Les connecteurs sont déclarés dans `_Meta/sources.md`, le registre que les skills lisent. Une
  source `renvoi 🔒` n'est ni agrégée ni copiée par un skill.
- **Renvoi d'emplacement** : l'endroit permanent où vit le corpus d'un projet ou d'une area (dossier
  Drive, workspace Notion, dossier de réunions) est un pointeur stable, pas un catalogue du contenu.
  Il nomme le connecteur qui l'atteint, repris d'une ligne de `sources.md`, et il est wikilinké au
  projet ou à l'area. Un pointeur qui ne répond plus est signalé par `sync-vault`, pas supprimé.

## Index et vues : requête plutôt que liste
- Un index tenu à la main dérive dès qu'on oublie de l'éditer. Pour voir toutes les fiches d'un type
  ou d'un statut, on écrit une vue (`.base` Obsidian, requête sur le frontmatter), qui reste exacte
  sans maintenance manuelle.
- Un index à la main n'est légitime que s'il est consommé par un outil qui ne sait pas requêter (par
  exemple un `CLAUDE.md` externe qui l'importe). Il porte alors en tête « généré par …, ne pas
  éditer à la main » et un script le régénère depuis le frontmatter.
- Les `_index.md` de `30-Resources/` sont une liste de capitalisation (cases à cocher, emplacement
  actuel d'un document), pas un index de contenu : ils se remplissent par l'usage.

## Sauvegarde et confidentialité technique
- {Stratégie de sauvegarde choisie, à compléter.}
- Pas de dépôt public ni de cloud non maîtrisé si le vault contient du sensible.
