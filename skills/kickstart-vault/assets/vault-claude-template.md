# {Nom du vault} — comment ce vault fonctionne

> Chargé par Claude à chaque session ouverte ici. Décrit **le vault, pas la personne**.
> Le contexte perso (rôle, enjeux, identité) vit dans le `~/.claude/CLAUDE.md` **global**,
> chargé dans toutes tes sessions — pas ici. **Seule exception : le ton ci-dessous** — c'est le
> contrat d'adresse des assistants *de ce vault*, qui doit être hérité par chaque persona.

**Périmètre** : {une ligne reprise du plan — le **scope** uniquement (ce que couvre le vault),
pas le rôle/identité. Ex. « activité professionnelle X uniquement ; le perso vit dans un vault
séparé ».}

<!-- Carte au niveau PARA STRICT : uniquement les dossiers de 1er niveau ci-dessous.
     N'ajoute AUCUN sous-dossier spécifique (ex. pas de "briefs/") — ça rôtit avec l'usage. -->
## Carte du vault (PARA)
- `00-Inbox/` — capture brute, à trier.
- `10-Projects/` — efforts avec une fin et un livrable. **Un projet = un dossier `{slug}/`
  contenant sa fiche principale `{slug}.md`** (le fil de suivi).
- `20-Areas/` — responsabilités continues. **Une area = un dossier `{slug}/` + sa fiche
  `{slug}.md`.**
- `30-Resources/` — référentiel réutilisable + `references-externes/` (renvois).
- `40-Archive/` — clôturé (on déplace, on ne supprime pas).
- `_Meta/` — `Schema.md` (contrat frontmatter), `governance.md` (règles d'accès & isolation),
  `sources.md` (registre des connecteurs : d'où les compétences tirent leurs informations).
- `_personas/` — les personas, tes assistants spécialisés (vides au départ) ; chacun déclare son
  périmètre lecture/écriture.
- `.claude/` — réglages techniques du vault (les garde-fous ci-dessous). Rien à y toucher.

## Conventions
- Fichiers et dossiers en **kebab-case**.
- Frontmatter conforme à `_Meta/Schema.md`.
- Relations en **[[wikilinks]]**. Un `[[lien]]` désigne le fichier `lien.md` (résolu par son
  **nom**, où qu'il soit dans le vault). **Claude ne suit pas un wikilink automatiquement** en
  lisant un `.md` : pour consulter une fiche liée, **localise `lien.md` par son nom et ouvre-le**.
- Respecter `_Meta/governance.md` : confidentialité 🔒, renvoi-jamais-copie.

## Ton (comment t'adresser)

> Comment les assistants de ce vault te parlent. Réglé avec toi à la cartographie.
> **Hérité par toutes les personas** (le Chief of Staff et les suivantes). Ajuste-le quand tu veux.

- **Vocabulaire** : {parle métier, zéro jargon — jamais de noms de fichiers, de structure interne ni
  de termes d'outil ↔ les termes techniques sont OK, je m'y retrouve}.
- **Longueur** : {va à l'essentiel, listes courtes ↔ développe, explique le pourquoi}.
- **Décision** : {propose, je valide ↔ décide et agis, dis-moi après ↔ informe-moi seulement}.
- **Registre** : {sobre et factuel ↔ chaleureux} · {tutoiement | vouvoiement} · {acquiesce ↔ challenge mes décisions}.

## Règle de travail : on pose le cadre, pas le contenu
On ne remplit pas les fiches à la main. Le contenu **entre par l'usage** : les personas écrivent,
on fait entrer les notes externes quand un besoin se présente (au fil des besoins). Une fiche vide
mais bien structurée est normale.

## Garde-fous automatiques
Deux petits automatismes veillent sur la santé du vault — tu n'as **rien à lancer** :
- **Au démarrage** : un bilan rapide apparaît s'il y a de quoi (Inbox qui traîne, notes sans
  `type`, fichiers `.DS_Store` nettoyés au passage).
- **Quand une note est écrite** : ses dates `created`/`updated` sont posées toutes seules ; un
  rappel s'affiche si la note n'a pas de frontmatter ou si son nom n'est pas en kebab-case.

Ce sont des **rappels** (et de petites corrections sans risque), pas des blocages : tu gardes la main.

## Imports
@_Meta/Schema.md
@_Meta/governance.md
@_Meta/sources.md
