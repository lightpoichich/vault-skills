---
type: moc
topic: schema
updated: {YYYY-MM-DD}
---

# Schema : contrat frontmatter du vault

> Tout agent qui écrit une fiche lit d'abord ce fichier. Ajouter un type plutôt que détourner un
> existant.

## Conventions générales
- **Nommage** : `kebab-case` pour tous les fichiers et dossiers.
- **Relations** : `[[wikilinks]]` entre fiches, pas de chemins en dur.
- **Un type par fiche**, déclaré dans le frontmatter.
- **Date en préfixe** : `YYYY-MM-DD-{sujet}` pour les fiches datées (réunions, comptes rendus,
  audits), ce qui donne le tri chronologique.
- **Nom de fichier unique** dans tout le vault : un `[[wikilink]]` résout par nom.
- **Objets homonymes** : suffixer ou préfixer l'objet secondaire (`{slug}-case-study.md`,
  `crm-{slug}.md`).
- **Sous-dossiers d'un projet** : créés au besoin, nommés par leur nature : `meetings/` (notes de
  réunion datées, `type: meeting`), `research/` (notes de travail, audits, plans), `livrables/`
  (figé, ce qui est parti chez le tiers).
- **Pas de note datée à plat** à la racine d'un projet : sa place est `meetings/` ou `research/`.
- **Racine d'une area** : ses référentiels courants seulement ; les flux (réunions, dossiers, posts,
  briefs) vivent en sous-dossiers ; l'historique clos part en `40-Archive/`.

## Types de fiches

### `area`
Responsabilité continue, sans fin.
```yaml
type: area
area: {slug}
objets: [ ... ]      # objets récurrents
cadence: { quotidien | hebdo | mensuel | continu }
outils: [ ... ]
tags: [area]
```

### `project`
Effort avec une fin et un livrable. `repo` et `dossier-travail`, optionnels, relient la fiche à un
dossier de travail hors vault ; l'outillage (`nouveau-projet`, `sync-repo`, hook Stop) résout par
`repo`, puis `dossier-travail`, puis le slug.
```yaml
type: project
status: { active | done }
deadline: { YYYY-MM-DD | "à préciser" }
livrable: { ... }
parties-prenantes: [ ... ]
area: "[[{area liée}]]"
repo: { URL du remote git[#sous-dossier] }        # optionnel, clé portable entre machines
dossier-travail: { chemin absolu sur le poste }    # optionnel, propre à une machine
tags: [project]
```

### `meeting`
```yaml
type: meeting
date: {YYYY-MM-DD}
participants: [ ... ]
lien: "[[{projet ou area}]]"
décisions: [ ... ]
actions: [ ... ]
```

### `adr` : décision (technique ou autre)
```yaml
type: adr
status: { proposed | accepted | superseded }
date: {YYYY-MM-DD}
décideurs: [ ... ]
```
Corps : Contexte, Décision, Conséquences, Alternatives.

### `incident`
```yaml
type: incident
date: {YYYY-MM-DD}
sévérité: { ... }
services: [ ... ]
statut: { ... }
```
Corps : Timeline, Post-mortem.

### `resource`
Référentiel réutilisable (trame, runbook, benchmark, méthodo).
```yaml
type: resource
domaine: { ... }
tags: [resource]
```

### `brief`
Brief du jour, écrit par `brief-du-jour` dans `00-Inbox/briefs/{YYYY-MM-DD}.md`.
```yaml
type: brief
date: {YYYY-MM-DD}
status: { draft | done }
```

### `draft` : livrable externe en attente de validation
Réservé à ce qui sort du vault vers un tiers (mail, courrier, proposition, post). Le savoir interne
(fiche, résumé, avancement, synthèse) s'écrit directement (voir `governance.md`, « Savoir et
livrable »).
```yaml
type: draft
canal: { mail | contrat | admin | autre }
destinataire: { ... }
lien: "[[{projet ou client rattaché}]]"   # requis : où la trace sera classée une fois envoyé
date: {YYYY-MM-DD}                          # requis : date de création, sert à repérer les périmés
statut: { en-attente | validé | envoyé | archivé | abandonné }
sensibilité: { normal | confidentiel }
```
Cycle de vie : `en-attente`, puis `validé` (humain), puis `envoyé` (humain), puis `archivé` comme
trace sur `lien`, ou `abandonné` si périmé. `_drafts/` ne garde pas d'état terminal : `sync-vault`
l'en sort.

### `note`
Note de travail scopée à un projet, une area ou l'inbox (recherche, préparation, compte-rendu
d'installation). Préférer un type dédié quand il existe.
```yaml
type: note
tags: [ ... ]
```

### `audit` : rapport d'audit du vault (éphémère)
Produit par `audit-vault` dans `00-Inbox/`, écrasé au jour le jour, purgé par les audits suivants.
```yaml
type: audit
date: {YYYY-MM-DD}
findings: { critical: N, warnings: N, infos: N }
```

### `moc`
Fiche de `_Meta/` (Schema, governance, sources, derivation) ou index.
```yaml
type: moc
topic: { ... }
updated: {YYYY-MM-DD}
```

## Confidentialité
- Marquer toute fiche ou section sensible du marqueur 🔒 et suivre `governance.md`.
- Les sources sensibles externes ne sont pas copiées : voir `references-externes/`.
