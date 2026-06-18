# Contrat de sortie : `00-Inbox/plan-vault.md`

Ce fichier est l'**interface** entre `interview-vault` (producteur) et `kickstart-vault`
(consommateur). `kickstart-vault` lit ce plan **section par section** pour générer l'arborescence,
`_Meta/Schema.md`, `_Meta/governance.md`, le `CLAUDE.md` racine et les shells. **Produire toutes les
sections, dans cet ordre, avec ces titres** (le lecteur repère par le sens, mais coller au gabarit
évite toute ambiguïté).

> Règle d'or : **kebab-case** pour tous les noms de dossiers d'Areas / Projects / sous-zones
> Resources. Une Area = un **dossier** `20-Areas/{slug}/` (le shell viendra dedans). Pas de fiche à
> plat.

## Gabarit (à recopier puis remplir)

````markdown
---
type: plan
status: draft
date: {YYYY-MM-DD}
---

# Plan d'implémentation vault — {Nom} ({Contexte})

> {Une ligne de périmètre : ce que le vault couvre, ce qu'il exclut. Mentionner l'isolation si
> l'activité comporte des données sensibles.}

## Arborescence proposée

```text
00-Inbox/
  └── matiere-premiere/
10-Projects/
20-Areas/
  ├── {area-slug-1}/
  ├── {area-slug-2}/
  └── ...
30-Resources/
  ├── {sous-zone-1}/
  ├── {sous-zone-2}/
  └── references-externes/
40-Archive/
_Meta/
```

## Projects (avec deadline)
- **{Nom}** — {deadline} — {livrable} — {parties prenantes}
- ...

## Areas (responsabilités continues)

### {area-slug-1}
- **Objets récurrents** : {liste}
- **Fréquence** : {cadence réelle}
- **Outils actuels** : {outils}

### {area-slug-2}
- ...

## Resources

### {sous-zone-1}/  *(état : surtout à créer / à constituer / existant)*
- {nom} — {usage} — {où il vit aujourd'hui | « à créer »}

### {sous-zone-2}/
- ...

### references-externes/  *(renvois, jamais de copie)*
- {source} — {localisation} — {🔒 si sensible}

**Logique d'organisation retenue** : {par type / par domaine — et pourquoi (volume, usage réel)}

## Conventions frontmatter suggérées
- **`project`** : `type, status, deadline, livrable, parties-prenantes, area, tags`
- **`area`** : `type, objets, cadence, outils, tags`
- **`meeting`** : `type, date, participants, lien, décisions, actions`
- {ajouter les types qui correspondent à l'activité : `adr`, `incident`, `brief`, `contact`,
  `draft`, `resource`, `moc`… — voir heuristique dans cartographie-guide.md}
- **Nommage** : kebab-case · **Wikilinks** pour les relations

## Mapping sources existantes → vault
- **{Source 1}** : {quoi → quelle zone ; migration ou renvoi ; **connecteur** : `à brancher` par
  défaut, `actif` seulement si le branchement (MCP/API joignable) est attesté}
- **{Source 2}** : ...

## Compétences à construire (skills) → personas

> Un irritant donne une **compétence** (une routine à automatiser), pas un rôle. On liste d'abord les
> compétences, puis on les **regroupe par persona**. Par défaut tout sous le **Chief of Staff** ; une
> persona à part seulement si zones / voix / garde-fous franchement distincts.

### Persona : chief-of-staff *(par défaut — porte tout sauf cas particulier)*
- **{compétence-slug}** — sert l'irritant n°{X} — lit {Areas / Resources / source} → écrit `{type}`
- ...

### Persona : {autre-slug} *(uniquement si zones/voix/garde-fous distincts — préciser la raison)*
- **{compétence-slug}** — sert l'irritant n°{Y} — lit {🔒 source} → écrit `{type}`

## Gouvernance & isolation (`_Meta`)
- **Périmètre** : {ce que le vault couvre / exclut}
- **Politique d'accès des agents** : {règle, pas une liste d'agents — par défaut lecture/écriture
  dans les zones non sensibles ; les éléments 🔒 jamais copiés, interdits sans règle explicite}
- **Isolation technique** : {local / pas de dépôt public / cloud maîtrisé — selon sensibilité}

## Profil de ton (comment t'adresser)
> Comment les assistants du vault s'adressent au dirigeant. `kickstart-vault` l'écrit tel quel dans
> la section `## Ton` du `CLAUDE.md` racine → **hérité par toutes les personas**. Quatre curseurs ;
> garder la formulation choisie par le dirigeant (pas une catégorie).
- **Vocabulaire** : {parle métier, zéro jargon — jamais de noms de fichiers, de structure interne ni
  de termes d'outil ↔ les termes techniques sont OK, je m'y retrouve}
- **Longueur** : {va à l'essentiel, listes courtes ↔ développe, explique le pourquoi}
- **Décision** : {propose, je valide ↔ décide et agis, dis-moi après ↔ informe-moi seulement}
- **Registre** : {sobre et factuel ↔ chaleureux} · {tutoiement | vouvoiement} · {acquiesce ↔ challenge mes décisions}

## Cas d'usage prioritaires (Top 5 irritants → compétences, par impact)
> Priorisés par impact (temps récupérable). Le signal vient du dirigeant ; l'estimation `~h/sem` est
> de l'arithmétique (fréquence × temps × part automatisable), **marquée « à valider »** — jamais un
> chiffre inventé. On capte le temps, pas le coût ni le prix.
1. {irritant} → {compétence} — fréq {x/sem} · temps unitaire {durée} · répétable {oui | cas-par-cas} · équipe {×N | non} → **~{h/sem} libérées (à valider)**
2. ...

**Priorisation par impact** : {ordre des compétences à construire d'abord, du plus fort temps récupérable au plus faible}
````

## Règles de remplissage

- **Frontmatter exact** : `type: plan`, `status: draft`, `date` au format `YYYY-MM-DD`.
- **Les 7 sections requises** que `kickstart-vault` lit : *Arborescence proposée*, *Projects*,
  *Areas*, *Resources*, *Conventions frontmatter suggérées*, *Mapping sources existantes → vault*,
  *Compétences à construire (skills) → personas*. **Aucune ne doit manquer.**
- **Gouvernance & isolation** : à **ne jamais sauter**. Si l'utilisateur n'en a pas parlé, la
  **synthétiser** depuis les signaux de sensibilité (sources RH, contrats, finances, données
  clients) repérés dans la matière première et le mapping. Marquer 🔒 les éléments sensibles.
- **Profil de ton** : remplir les 4 curseurs avec les **mots du dirigeant** issus de l'Étape 3bis,
  pas une catégorie (jamais « non-tech »). Le curseur **Vocabulaire** détermine combien de structure
  interne un assistant a le droit de nommer — c'est lui qui calibre la narration. Si la passe n'a pas
  eu lieu, laisser la section telle quelle : `kickstart-vault` posera un défaut marqué « à valider ».
- **Resources** : toujours des **sous-zones** (pas une liste à plat) + la ligne **« Logique
  d'organisation retenue »** + une sous-zone `references-externes/`. **Chaque document existant
  porte son emplacement actuel** (Drive, Notion, PDF, papier…) — il alimentera les `_index.md` de
  `kickstart-vault` et l'entrée une par une via l'import. Un item « à créer » reste sans emplacement.
- **Conventions frontmatter** : ne lister que les types qui **correspondent à l'activité**. Toujours
  inclure `project`, `area`, `meeting`. Ajouter `adr` si décisions techniques à tracer, `incident`
  si prod/oncall, `brief` si agent de point quotidien, `contact` si partenaires/clients récurrents,
  `draft` si production de texte, `resource`/`moc` au besoin. **La liste n'est pas fermée** : si une
  fiche récurrente réelle ne rentre dans aucun type connu, **créer un type métier** (kebab-case) —
  voir l'heuristique « types frontmatter » du guide et ses garde-fous (vraie fiche récurrente,
  adossée à une compétence, pas de doublon).
- **Areas** : 4 à 7, en kebab-case, chacune avec objets / fréquence / outils.
- **Cohérence types ↔ compétences** : tout type de fiche cité dans *Compétences à construire*
  (« écrit `X` ») **doit** figurer dans *Conventions frontmatter suggérées*. Sinon `kickstart-vault`
  ne le mettra pas au Schema et la compétence écrira un type inconnu. Vérifier ce recoupement avant
  d'écrire le plan (ex. une compétence de point quotidien qui écrit un `brief` → déclarer le type `brief`).
- **Cas d'usage prioritaires** : chaque item porte son signal d'impact (fréquence, temps unitaire,
  répétabilité, projetable-équipe) + une estimation `~h/sem libérées` **marquée « à valider »** ; ne
  chiffrer que le **répétable** ; **aucun coût ni prix** (le skill capte le temps, pas l'argent).
- **N'inventer aucune valeur** : tout vient des réponses de l'interview. Un champ sans réponse →
  « à creuser en S1 ».
