# {Nom du vault} : comment ce vault fonctionne

> Chargé par Claude à chaque session ouverte ici. Décrit le vault, pas la personne.
> Le contexte perso (rôle, enjeux, identité) vit dans le `~/.claude/CLAUDE.md` global, chargé dans
> toutes tes sessions. Seule exception : la section Ton, contrat d'adresse des assistants de ce
> vault, héritée par chaque persona.

**Périmètre** : {une ligne reprise du plan, le scope seulement, par exemple « activité
professionnelle X uniquement ; le perso vit dans un vault séparé »}.

## Carte du vault (PARA)
- `00-Inbox/` : capture brute, à trier.
- `10-Projects/` : efforts avec une fin et un livrable. Un projet est un dossier `{slug}/` contenant
  sa fiche principale `{slug}.md`, le fil de suivi.
- `20-Areas/` : responsabilités continues. Une area est un dossier `{slug}/` et sa fiche `{slug}.md`.
- `30-Resources/` : référentiel réutilisable et `references-externes/` (renvois).
- `40-Archive/` : clôturé ; on déplace, on ne supprime pas.
- `_Meta/` : `Schema.md` (contrat frontmatter), `governance.md` (règles d'accès et isolation),
  `sources.md` (registre des connecteurs), `derivation.md` (le pourquoi de la structure, à lire
  avant de la changer), `hooks.conf` (réglages des garde-fous).
- `_personas/` : les assistants spécialisés ; chacun déclare son périmètre lecture/écriture.
- `.claude/` : réglages techniques du vault. Rien à y toucher.

## Conventions
- Fichiers et dossiers en kebab-case.
- Frontmatter conforme à `_Meta/Schema.md`.
- Relations en `[[wikilinks]]`. Un `[[lien]]` désigne le fichier `lien.md`, résolu par son nom où
  qu'il soit dans le vault. Claude ne suit pas un wikilink automatiquement : pour consulter une fiche
  liée, localiser `lien.md` par son nom et l'ouvrir.
- Respecter `_Meta/governance.md` : confidentialité 🔒, renvoi jamais copie.

## Ton (comment t'adresser)

> Réglé avec toi à la cartographie, hérité par toutes les personas. Ajuste-le quand tu veux.

- **Vocabulaire** : {parle métier, zéro jargon, sans nom de fichier ni terme d'outil | les termes
  techniques sont OK, je m'y retrouve}.
- **Longueur** : {va à l'essentiel, listes courtes | développe, explique le pourquoi}.
- **Décision** : {propose, je valide | décide et agis, dis-moi après | informe-moi seulement}.
- **Registre** : {sobre et factuel | chaleureux} · {tutoiement | vouvoiement} · {acquiesce |
  challenge mes décisions}.

## Règle de travail : on pose le cadre, pas le contenu
On ne remplit pas les fiches à la main. Le contenu entre par l'usage : les personas écrivent, les
notes externes entrent quand un besoin se présente. Une fiche vide mais bien structurée est normale.

## Garde-fous automatiques
Quatre automatismes veillent sur le vault ; rien à lancer (réglages : `_Meta/hooks.conf`).
- **Au démarrage** : un bilan rapide s'il y a de quoi (Inbox qui traîne, notes sans `type`,
  `.DS_Store` nettoyés), et l'approbation des règles du vault pour une session lancée depuis une
  persona ou un dossier de travail.
- **Quand une note est écrite** : dates `created`/`updated` posées seules ; rappel si frontmatter
  absent ou nom hors kebab-case.
- **En fin de tour** : si la session a assez de matière, rappel de répercuter ce qui a bougé
  (`sync-vault` depuis le vault, `sync-repo` depuis un dossier de code relié à un projet).

Ce sont des rappels et de petites corrections sans risque, pas des blocages.

## Imports
@_Meta/Schema.md
@_Meta/governance.md
@_Meta/sources.md
