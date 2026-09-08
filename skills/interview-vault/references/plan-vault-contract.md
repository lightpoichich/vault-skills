# Contrat de sortie : `00-Inbox/plan-vault.md`

Ce fichier est l'interface entre `interview-vault` (producteur) et `kickstart-vault`
(consommateur). `kickstart-vault` lit le plan section par section pour générer l'arborescence,
`_Meta/Schema.md`, `_Meta/governance.md`, le `CLAUDE.md` racine et les shells. Produire toutes les
sections, dans cet ordre, avec ces titres : le lecteur repère par le sens, mais coller au gabarit
évite toute ambiguïté.

Nommage : kebab-case pour tous les noms de dossiers (Areas, Projects, sous-zones Resources) et de
types métier. Une Area est un dossier `20-Areas/{slug}/`, jamais une fiche à plat.

## Gabarit (à recopier puis remplir)

````markdown
---
type: plan
status: draft
date: {YYYY-MM-DD}
---

# Plan d'implémentation vault : {Nom} ({Contexte})

> {Une ligne de périmètre : ce que le vault couvre, ce qu'il exclut. Mentionner l'isolation si
> l'activité comporte des données sensibles.}

## Arborescence proposée

```text
00-Inbox/
  matiere-premiere/
10-Projects/
20-Areas/
  {area-slug-1}/
  {area-slug-2}/
  ...
30-Resources/
  {sous-zone-1}/
  {sous-zone-2}/
  references-externes/
40-Archive/
_Meta/
```

## Projects (avec deadline)
- **{Nom}** : {deadline} ; {livrable} ; {parties prenantes}
- ...

## Areas (responsabilités continues)

### {area-slug-1}
- **Objets récurrents** : {liste}
- **Fréquence** : {cadence réelle}
- **Outils actuels** : {outils}

### {area-slug-2}
- ...

## Resources

### {sous-zone-1}/  *(état : à créer, à constituer ou existant)*
- {nom} : {usage} ; {où il vit aujourd'hui, ou « à créer »}

### {sous-zone-2}/
- ...

### references-externes/  *(renvois, jamais de copie)*
- {source} : {localisation} ; {🔒 si sensible}

**Logique d'organisation retenue** : {par type ou par domaine, et pourquoi (volume, usage réel)}

## Conventions frontmatter suggérées
- **`project`** : `type, status, deadline, livrable, parties-prenantes, area, tags`
- **`area`** : `type, objets, cadence, outils, tags`
- **`meeting`** : `type, date, participants, lien, décisions, actions`
- {types propres à l'activité : `adr`, `incident`, `brief`, `contact`, `draft`, `resource`, `moc`
  ou un type métier ; voir cartographie-guide.md}
- **Nommage** : kebab-case ; **wikilinks** pour les relations

## Mapping sources existantes et zones du vault
- **{Source 1}** : {quoi, vers quelle zone ; migration ou renvoi ; connecteur `à brancher` par
  défaut, `actif` seulement si le branchement (MCP ou API joignable) est attesté}
- **{Source 2}** : ...

## Compétences à construire (skills) et personas

> Un irritant donne une compétence (une routine à automatiser), pas un rôle. Les compétences sont
> listées d'abord, puis regroupées par persona.

### Persona : chief-of-staff *(par défaut : porte tout sauf cas particulier)*
- **{compétence-slug}** : sert l'irritant n°{X} ; lit {Areas, Resources, source} ; écrit `{type}`
- ...

### Persona : {autre-slug} *(seulement si zones, voix ou garde-fous distincts ; préciser la raison)*
- **{compétence-slug}** : sert l'irritant n°{Y} ; lit {🔒 source} ; écrit `{type}`

## Gouvernance et isolation (`_Meta`)
- **Périmètre** : {ce que le vault couvre et exclut}
- **Politique d'accès des agents** : {une règle, pas une liste d'agents : par défaut lecture et
  écriture dans les zones non sensibles ; les éléments 🔒 jamais copiés, interdits sans règle explicite}
- **Isolation technique** : {local, pas de dépôt public, cloud maîtrisé, selon sensibilité}

## Profil de ton (comment t'adresser)
> Comment les assistants du vault s'adressent au dirigeant. `kickstart-vault` le reporte tel quel
> dans le `CLAUDE.md` racine, hérité par toutes les personas. Garder la formulation du dirigeant.
- **Vocabulaire** : {parle métier, zéro jargon, ou les termes techniques sont OK}
- **Longueur** : {va à l'essentiel, listes courtes, ou développe et explique le pourquoi}
- **Décision** : {propose et je valide, ou décide et agis puis dis-moi, ou informe-moi seulement}
- **Registre** : {sobre et factuel ou chaleureux} ; {tutoiement ou vouvoiement} ; {acquiesce ou challenge mes décisions}

## Cas d'usage prioritaires (Top 5 irritants, par impact)
> Priorisés par temps récupérable. Le signal vient du dirigeant ; l'estimation en heures par
> semaine est marquée « à valider ».
1. {irritant} : compétence {slug} ; fréquence {x/sem} ; temps unitaire {durée} ; répétable {oui ou
   cas par cas} ; équipe {×N ou non} ; **~{h/sem} libérées (à valider)**
2. ...

**Priorisation par impact** : {ordre des compétences à construire, du plus fort temps récupérable au plus faible}
````

## Règles de remplissage

- **Frontmatter exact** : `type: plan`, `status: draft`, `date` au format `YYYY-MM-DD`.
- **Dix sections**, toutes présentes. `kickstart-vault` lit telles quelles les sept premières
  (Arborescence proposée, Projects, Areas, Resources, Conventions frontmatter suggérées, Mapping
  sources, Compétences à construire et personas). Si Gouvernance et isolation, Profil de ton ou Cas
  d'usage prioritaires manquent, il synthétise un défaut marqué « à valider » ; les produire quand
  même.
- **Gouvernance et isolation** : si le dirigeant n'en a pas parlé, la synthétiser depuis les signaux
  de sensibilité (sources RH, contrats, finances, données clients) repérés dans la matière première
  et le mapping. Marquer 🔒 les éléments sensibles.
- **Profil de ton** : remplir les quatre curseurs avec les mots du dirigeant issus de l'Étape 3bis,
  jamais une catégorie. Si la passe n'a pas eu lieu, laisser la section telle quelle.
- **Resources** : toujours des sous-zones, la ligne « Logique d'organisation retenue » et une
  sous-zone `references-externes/`. Chaque document existant porte son emplacement actuel (Drive,
  Notion, PDF, papier) : il alimente les `_index.md` de `kickstart-vault` et l'entrée un par un via
  l'import. Un item « à créer » reste sans emplacement.
- **Conventions frontmatter** : ne lister que les types qui correspondent à l'activité, toujours
  avec `project`, `area`, `meeting`. Signaux et conditions de création d'un type métier dans
  cartographie-guide.md.
- **Areas** : 4 à 7, chacune avec objets, fréquence, outils.
- **Cohérence entre types et compétences** : tout type de fiche cité dans « Compétences à
  construire » (« écrit `X` ») figure dans « Conventions frontmatter suggérées », sinon
  `kickstart-vault` ne le met pas au Schema et la compétence écrit un type inconnu. Vérifier ce
  recoupement avant d'écrire le plan (une compétence de point quotidien qui écrit un `brief`
  implique le type `brief`).
- **Regroupement en personas** : par défaut toutes les compétences se rangent sous le Chief of
  Staff, la persona généraliste que `kickstart-vault` pose d'office ; trois compétences de capture
  et de synthèse donnent un seul Chief of Staff, pas trois personas. Une persona dédiée seulement si
  une compétence réclame des zones, une voix ou des garde-fous distincts ; signal le plus fiable :
  la gouvernance (sources 🔒 finance, RH, contrats avec leurs propres garde-fous) ou une voix
  particulière (commerciale, juridique). Les personas ainsi isolées se créent ensuite avec
  `kickstart-persona`, les compétences avec `vault-skill-creator`.
- **Chiffrage des cas d'usage** : chaque item porte son signal d'impact (fréquence, temps unitaire,
  répétabilité, projetable à l'équipe) et une estimation d'heures libérées par semaine égale à
  fréquence × temps unitaire × part automatisable (× N si projeté à l'équipe), fourchette basse,
  marquée « à valider ». Ne chiffrer que le répétable : une tâche au cas par cas reste un irritant
  listé, sans estimation. Ni coût ni prix : le skill capte le temps, la valorisation se fait en
  aval. Pas de réponse : « à creuser en S1 ».
- **Aucune valeur inventée** : tout vient des réponses de l'interview. Un champ sans réponse :
  « à creuser en S1 ».
