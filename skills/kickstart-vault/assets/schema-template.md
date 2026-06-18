---
type: moc
topic: schema
updated: {YYYY-MM-DD}
---

# Schema — contrat frontmatter du vault

> Le contrat qui garde le vault cohérent dans le temps. Tout agent qui écrit une fiche lit
> d'abord ce fichier. Ne garder que les types réellement utiles à CE vault (issus du plan) ;
> ajouter un type plutôt que détourner un existant.

## Conventions générales
- **Nommage** : `kebab-case` pour tous les fichiers et dossiers.
- **Relations** : `[[wikilinks]]` entre fiches, jamais de chemins en dur.
- **Un type par fiche**, déclaré dans le frontmatter.

## Types de fiches

<!-- Garder uniquement les types présents dans la section "Conventions frontmatter" du plan.
     Ci-dessous les plus courants, à adapter/élaguer. -->

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
Effort avec une fin et un livrable. Le champ optionnel `dossier-travail` relie une fiche projet à un
dossier de travail externe (filesystem, hors vault) : lancé depuis ce dossier, l'outillage retrouve la
fiche par ce chemin (résolution dossier↔fiche depuis l'extérieur du vault).
```yaml
type: project
status: { active | done }
deadline: { YYYY-MM-DD | "à préciser" }
livrable: { ... }
parties-prenantes: [ ... ]
area: "[[{area liée}]]"
dossier-travail: { chemin absolu du dossier de travail externe | absent }   # optionnel — relie un dossier filesystem à cette fiche
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

### `adr` — décision (technique ou autre)
```yaml
type: adr
status: { proposed | accepted | superseded }
date: {YYYY-MM-DD}
décideurs: [ ... ]
```
Corps : Contexte · Décision · Conséquences · Alternatives.

### `resource`
Référentiel réutilisable (trame, runbook, benchmark, méthodo).
```yaml
type: resource
domaine: { ... }
tags: [resource]
```

### `draft` — livrable externe en attente de validation
> Réservé à ce qui **sort du vault vers un tiers** (mail, courrier, proposition, post). Le savoir
> interne (fiche, résumé, avancement, synthèse) ne passe **pas** par là : il s'écrit directement
> (voir `governance.md`, « Savoir vs Livrable »).
```yaml
type: draft
canal: { mail | contrat | admin | autre }
destinataire: { ... }
lien: "[[{projet ou client rattaché}]]"   # requis : où la trace sera classée une fois envoyé
date: {YYYY-MM-DD}                          # requis : date de création, sert à repérer les périmés
statut: { en-attente | validé | envoyé | archivé | abandonné }
sensibilité: { normal | confidentiel }
```
Cycle de vie : `en-attente` → `validé` (humain) → `envoyé` (humain) → **archivé** comme trace sur
`lien`, ou **abandonné** si périmé. `_drafts/` ne garde jamais un état terminal — `sync-vault` l'en sort.

### `audit` — rapport d'audit du vault (éphémère)
Produit par `audit-vault` dans `00-Inbox/`, écrasé au jour le jour, purgé par les audits suivants.
```yaml
type: audit
date: {YYYY-MM-DD}
findings: { critical: N, warnings: N, infos: N }
```

<!-- Types optionnels selon le plan : `brief` (date, priorités, alertes, agenda, todos),
     `incident` (date, sévérité, services, statut, timeline, post-mortem), `moc` (index). -->

## Confidentialité
- Marquer toute fiche/section sensible avec le tag/emoji **🔒** et suivre `governance.md`.
- Les sources sensibles externes ne sont **pas copiées** : voir `references-externes/`.
