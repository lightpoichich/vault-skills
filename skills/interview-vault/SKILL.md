---
name: interview-vault
description: >-
  Mène l'interview de cartographie d'activité (PARA) qui produit `00-Inbox/plan-vault.md` — le plan
  d'implémentation que `kickstart-vault` exécute ensuite. C'est le **premier maillon** de la chaîne
  d'amorçage d'un vault Obsidian (second cerveau). Utilise ce skill dès que l'utilisateur veut
  « cartographier mon activité », « construire / dessiner la base de mon vault », « préparer mon
  vault », « faire l'interview PARA », « monter mon second cerveau », ou démarre un vault vide et
  veut en poser la structure avant de la matérialiser. Skill **généraliste et adaptatif** : il ne
  demande jamais « tu es tech ou non-tech ? » — il s'adapte aux réponses, de sorte qu'un DG, un CTO
  ou un artisan obtiennent chacun le plan qui colle à leur métier. NE PAS l'utiliser si le vault est
  déjà structuré (c'est alors un audit / une refonte, pas une cartographie initiale), ni pour
  matérialiser le plan (c'est `kickstart-vault`), ni pour créer une persona (`kickstart-persona`)
  ou un skill métier (`vault-skill-creator`).
---

# Interview Vault

Mène l'**interview de cartographie** qui transforme une activité (en tête de l'utilisateur, éparse
dans ses outils) en un **plan de vault** structuré selon PARA. Le livrable unique est
`00-Inbox/plan-vault.md` — le plan que `kickstart-vault` exécutera pour poser le squelette réel.

C'est le **premier maillon** de l'amorçage d'un vault :

```
interview-vault  →  kickstart-vault  →  kickstart-persona  →  vault-skill-creator
(le plan)           (le squelette)      (les agents)          (les compétences)
```

Ce skill **n'écrit que dans `00-Inbox/`**. Il ne crée ni dossier PARA, ni fiche, ni persona, ni
skill. Il cartographie, il propose, il consigne le plan. La matérialisation, c'est l'étape d'après.

## Pourquoi ces partis pris (à garder en tête tout du long)

- **Généraliste, jamais profilé.** On ne demande pas une catégorie (« tech / non-tech », « grande
  boîte / TPE »). On part de l'activité réelle et on **dérive** la bonne structure des réponses. Le
  même skill doit produire un plan radicalement différent pour un DG conseil et pour un CTO — parce
  que leurs réponses diffèrent, pas parce qu'on a coché une case. Les suggestions (Areas, sources,
  compétences, types de fiches) sont **proposées seulement si elles résonnent** avec ce qui a été décrit.
  Référence d'appui : `references/cartographie-guide.md`.
- **Generate-don't-write.** On capture ce que l'utilisateur dit, on ne l'invente pas. Si une réponse
  manque, on écrit « à creuser en S1 » et on avance. Le plan est un squelette de décisions, pas un
  contenu rempli d'office.
- **L'actionnabilité prime sur le sujet.** Le critère de classement PARA n'est pas le thème mais
  l'actionnabilité — d'où la vigilance permanente sur le piège Areas-as-Projects (voir plus bas).
- **Une question à la fois.** Pas de questionnaire en bloc. On reformule la réponse avant de passer
  à la suivante ; si c'est flou, on creuse. C'est ce qui fait émerger la vraie structure.

## Comment parler au dirigeant (langue)

L'interlocuteur est un **dirigeant, pas un développeur**. Tout ce qui s'affiche à l'écran et tout
texte livré (le plan, les résumés) suit ces règles :

- **Français propre, zéro anglicisme gratuit.** Bannir, à l'oral comme à l'écrit : *scaffold(er),
  bundle, alias, quick win, input, deal, mapping, shell, lazy-pull, generate-don't-write*. Dire
  plutôt : installer/monter, ensemble prêt-à-l'emploi, raccourci, gain rapide, matière/informations,
  affaire/dossier, correspondance, fiche vide structurée, « au fil des besoins », « on pose le cadre,
  pas le contenu ».
- **Un terme de structure = expliqué une seule fois, puis réutilisé.** À la première occurrence,
  une parenthèse d'explication ; ensuite le mot suffit : `frontmatter` (l'en-tête d'une note),
  kebab-case (nom de fichier en minuscules-avec-tirets), `wikilink` (un lien `[[…]]`), `persona`
  (un assistant spécialisé), `compétence`/*skill* (une routine qu'on automatise).
- **Jamais de jargon dans un titre de section du plan** que le dirigeant relira.
- En cas de doute : la phrase doit être comprise par quelqu'un qui n'a jamais ouvert un terminal.

## Quand utiliser / quand ne pas utiliser

**Utiliser** quand :
- Le vault est vide ou quasi-vide et l'utilisateur veut en dessiner la structure avant de la bâtir.
- On est dans un dossier qui contient (ou contiendra) `00-Inbox/`, `10-Projects/`, `20-Areas/`…
- L'utilisateur prévoit d'y brancher des agents/personas plus tard.

**Ne pas utiliser** si :
- Le vault est **déjà structuré** (Areas en place, fiches existantes) → c'est un audit ou une
  refonte, pas une cartographie initiale.
- L'utilisateur veut **matérialiser** un plan déjà écrit → c'est `kickstart-vault`.
- Il veut créer un **agent** (`kickstart-persona`) ou un **skill métier** (`vault-skill-creator`).

## Le cadre PARA (à appliquer et à expliquer si besoin)

- **Projects** — un effort avec **une fin et un livrable** (ex. « préparer le conseil de juin »).
- **Areas** — une **responsabilité continue sans fin** (ex. « finance », « fiabilité prod »).
  Viser **4 à 7** (8 à la rigueur si le dirigeant tient à une distinction réelle après que tu lui
  as proposé de consolider — sa préférence l'emporte).
- **Resources** — un **référentiel réutilisable** (méthodos, trames, runbooks, benchmarks, ADR).
- **Archive** — ce qui est clos (on **déplace**, on ne supprime pas).
- **Inbox** — zone tampon de capture brute.

> **Piège n°1 — Areas-as-Projects.** La confusion la plus fréquente : traiter une Area comme un
> Project. « Stratégie » n'est jamais « finie » → c'est une Area ; « finaliser le plan stratégique
> 2027 » a une fin → c'est un Project. Reste vigilant tout du long : si l'utilisateur nomme quelque
> chose qui ne finit jamais, c'est une Area.

---

## Déroulé

### Phase 0 — Cadre & déroulé

Se présenter brièvement, poser le cadre PARA (ci-dessus, en une ou deux phrases adaptées au niveau
de l'utilisateur), annoncer le déroulé (matière première → interview en 4 phases → irritants → profil
de ton → plan).
**Aucune question de profil.** Si un `~/.claude/CLAUDE.md` global existe, l'utiliser pour se caler
sur le contexte (rôle, charge) sans jamais demander de catégorie. Vérifier que l'utilisateur a
compris le déroulé, puis demander le premier élément de matière première.

### Étape 1 — Matière première (avant toute interview)

Demander **successivement** ces 6 éléments et écrire le contenu brut **au fil** dans
`00-Inbox/matiere-premiere/` (créer le dossier si besoin). **Écrire chaque fichier avant de demander
le suivant.** Ne pas démarrer l'interview tant que les 6 fichiers ne sont pas écrits.

| # | Demande (ouverte, à adapter aux mots de l'utilisateur) | Fichier cible (canonique) |
|---|---|---|
| 1 | Contexte court : rôle, taille d'équipe, charge, ce qui pèse aujourd'hui | `contexte.md` |
| 2 | Thèmes mentaux actuels : les sujets qui structurent déjà sa tête | `themes-actuels.md` |
| 3 | Où vivent ses notes aujourd'hui (Notion, OneNote, `.md` en vrac, Apple Reminders, Projects Claude…) | `notes-actuelles.md` |
| 4 | Sources d'équipe / outils où vit l'information (Slack, Notion, DataDog, Gmail, GitHub, Granola, Outlook…) | `sources-equipe.md` |
| 5 | Skills / MCP / slash commands / connecteurs déjà en place | `outillage-actuel.md` |
| 6 | 3-5 chantiers transverses en cours (efforts en attente d'avancée) | `chantiers-en-cours.md` |

**La demande est ouverte, le fichier cible reste canonique.** On ne fléchera jamais une question par
outil (« montre-moi ton OneNote ») : on demande « où vivent tes notes ? » et on range la réponse dans
`notes-actuelles.md`, que la stack nommée soit OneNote, Obsidian ou un tiroir de Post-it. Si
l'utilisateur n'a rien pour un élément (ex. aucun outillage Claude en place), écrire le fichier avec
« néant pour l'instant » et avancer.

### Étape 2 — Interview en 4 phases

Une question à la fois, reformuler avant d'enchaîner. Consulter `references/cartographie-guide.md`
pour le **superset d'Areas** et les **heuristiques d'adaptation** (quand proposer quoi).

**Phase 1 — Projects (3-4 questions).** Partir de `chantiers-en-cours.md`. Pour chaque chantier,
valider qu'il a **une fin et un livrable** ; identifier deadline et parties prenantes. Si finalement
c'est continu → le **reclasser en Area** (et le dire).

**Phase 2 — Areas (5-7 questions).** Partir de `themes-actuels.md`. Pour chaque thème, vérifier que
c'est une **responsabilité continue** (pas un Project déguisé), puis creuser : **objets récurrents**,
**fréquence** (≥ 1×/semaine pour qualifier d'Area), **outils actuels**. Ensuite, chercher les Areas
qui **pourraient manquer** : piocher dans le superset du guide **uniquement celles qui résonnent**
avec ce qui a été décrit, les **proposer pour vérification** — ne jamais dérouler toute la liste ni
inventer une Area qui ne parle pas à l'utilisateur. Viser 4 à 7 Areas au total ; si on dépasse,
**proposer de consolider** (deux thèmes proches fusionnent), mais ne jamais l'imposer.

> **Boucle de validation — obligatoire avant la Phase 3.** Produire une **ébauche partielle**
> (Projects + Areas identifiés), la montrer, laisser l'utilisateur corriger / compléter / supprimer.
> N'avancer qu'une fois validée.

**Phase 3 — Resources (3-4 questions).** Quelles méthodos, trames, runbooks, ADR, frameworks,
benchmarks réutilise-t-il d'un chantier à l'autre ? Quels documents de référence sont consultés sans
bouger ? À partir des réponses, proposer une **sous-arborescence** pour `30-Resources/` (2-4
sous-dossiers) et **choisir avec l'utilisateur** la logique — **par type** (`methodologies/`,
`runbooks/`, `adr/`, `benchmarks/`) ou **par domaine** — selon son volume et son usage réels (heuristique
dans le guide). Prévoir `references-externes/` pour les renvois (jamais de copie).

**Phase 4 — Sources & compétences à construire (3-4 questions).**
- **Sources existantes** : pour chaque source nommée (à l'Étape 1), **quelle zone du vault** elle
  alimente, et si c'est une **migration** (le contenu entre dans le vault) ou un **renvoi** (la source
  de vérité reste dehors → `references-externes/`). Noter aussi si un **connecteur est déjà branché**
  (MCP/API joignable) ou si la source est juste *utilisée* sans connecteur : par défaut, on consigne
  une source comme **« à brancher »** — `kickstart-vault` n'écrira `actif` dans `_Meta/sources.md` que
  si le branchement est attesté. Qu'une source existe ne veut pas dire que son connecteur est en place.
- **Compétences (skills) à construire** : un irritant chronophage donne une **compétence** (une
  routine qu'on automatisera), **pas un rôle**. Les dériver des Top 5 irritants + des sources (voir
  Étape 3 et le guide), pas d'un catalogue. Pour chacune : ce qu'elle **lit** (quelles Areas /
  Resources) et ce qu'elle **écrit** (quelle zone, quel type de fiche).
- **Regrouper en personas — étape de synthèse.** Les compétences ne sont pas une à une un assistant.
  Une **persona** naît d'un **groupe de compétences qui partagent une même lentille** : mêmes zones
  de lecture/écriture, même posture, même voix. **Par défaut, tout se range sous le Chief of Staff**
  (la persona généraliste posée d'office par `kickstart-vault`). On n'isole une persona dédiée que si
  une compétence réclame des **zones, une voix ou des garde-fous franchement distincts** (ex. une
  compétence qui lit des sources sensibles 🔒 finance/RH mérite sa propre lentille). Présenter au
  dirigeant : « voici tes compétences ; elles tiennent toutes sous ton Chief of Staff, sauf {X} qui
  mérite sa persona à part parce que {raison de zone/voix} ».

> **Boucle de validation — obligatoire en Phase 4, volet par volet.** Ne jamais clore cette phase
> sur une synthèse unique validée d'un bloc. Présenter et faire valider **séparément, dans l'ordre** :
> (1) la correspondance sources → zones (migration ou renvoi), (2) les compétences pressenties,
> (3) le regroupement en personas. Un volet à la fois, validation explicite avant de passer au
> suivant — exactement comme la boucle Projects + Areas avant la Phase 3.

### Étape 3 — Top 5 irritants

En clôture, demander les **5 choses qui bouffent le plus de temps** aujourd'hui. Chaque irritant est
la matière directe d'une **compétence (skill)** à construire — pas d'un rôle. Le regroupement de ces
compétences en personas se fait ensuite (Phase 4, étape de synthèse).

### Étape 3bis — Profil de ton (passe courte)

Avant d'écrire le plan, **régler comment les assistants du vault s'adresseront au dirigeant**. Sans
cette passe, le ton est posé au hasard et dérive vers le jargon (ce qui rend un assistant illisible
pour qui ne veut pas de tuyauterie, et trop bavard pour qui la maîtrise). Le résultat ira dans la
section *Profil de ton* du plan, puis dans le `CLAUDE.md` racine du vault — **hérité par toutes les
personas**.

Présenter les **4 curseurs** d'un coup (calibration rapide, pas une question lourde par curseur) et
laisser le dirigeant se placer avec ses propres mots :

- **Vocabulaire** — *parle-moi métier, zéro jargon ni nom de fichier* ↔ *les termes techniques sont OK*.
- **Longueur** — *va à l'essentiel, listes courtes* ↔ *développe, explique le pourquoi*.
- **Décision** — *propose, je valide* ↔ *décide et agis, dis-moi après* ↔ *informe-moi seulement*.
- **Registre** — *sobre et factuel* ↔ *chaleureux* · *tutoiement / vouvoiement* · *acquiesce* ↔ *challenge-moi*.

> **Ce n'est PAS un profilage.** Le curseur Vocabulaire dit *comment on parle*, jamais *ce qu'on
> construit* : la structure du vault reste dérivée des réponses métier (cf. « généraliste, jamais
> profilé », plus haut). Un DG conseil et un CTO se placeront différemment sur Vocabulaire — et c'est
> exactement le but : la même question, deux réponses, deux tons. On ne coche pas « tech / non-tech ».

Reformuler le placement retenu en une ligne, puis l'écrire dans la section *Profil de ton* du plan
(Étape 4). Si le dirigeant n'a pas de préférence, le noter : `kickstart-vault` posera un défaut prudent
(métier sans jargon, concis, propose-je-valide, sobre + tutoiement) marqué « à valider ».

### Étape 4 — Écrire `00-Inbox/plan-vault.md`

Rédiger le plan complet en **respectant à la lettre** le gabarit de `references/plan-vault-contract.md`.
Ce gabarit est le **contrat d'interface** : `kickstart-vault` lit ce fichier pour tout générer. Toute
section manquante ou mal nommée casse l'étape suivante. Détailler en particulier la **Gouvernance /
isolation** (périmètre, données sensibles 🔒, isolation) — à **synthétiser depuis les signaux** même
si l'utilisateur n'en a pas parlé spontanément (sources RH, contrats, finances → marquer 🔒).

### Handoff

Une fois `plan-vault.md` écrit, le résumer en quelques lignes (X Areas, Y Projects, la logique
Resources retenue, les compétences pressenties et leur regroupement en personas) et **pointer la
suite explicitement** :

> « Ton plan est prêt dans `00-Inbox/plan-vault.md`. Pour le matérialiser en vault réel (arborescence,
> Schema, gouvernance, CLAUDE.md, hooks), lance **`kickstart-vault`**. »

---

## Garde-fous

- **Une question à la fois**, jamais un questionnaire en bloc. Reformuler systématiquement avant
  d'enchaîner. **Jamais deux sujets ou deux domaines regroupés dans la même question, même « pour
  accélérer » en fin de phase** — si le temps presse, on raccourcit la reformulation, pas la
  granularité des questions.
- **N'invente pas.** Si l'utilisateur n'a pas la réponse, écrire « à creuser en S1 » et passer.
- **Surveille le piège Areas-as-Projects** à chaque phase.
- **Écris uniquement dans `00-Inbox/`** (le plan + `matiere-premiere/`). Ne crée aucune fiche PARA,
  aucun dossier d'Area/Project, aucune persona, aucun skill.
- **Ne touche pas** à `.claude/` ni à `_Meta/`. Si tu les vois, laisse-les tranquilles.
- **Respecte le contrat de sortie** (`references/plan-vault-contract.md`) — c'est ce qui garantit que
  `kickstart-vault` saura lire le plan.
