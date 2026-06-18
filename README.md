# vault-skills

Skills Claude Code pour monter et faire vivre un second cerveau : un vault Obsidian
structuré en PARA, peuplé par des personas Claude qui le lisent et l'écrivent au quotidien.

La plupart des seconds cerveaux meurent en cimetière de notes : on y capture sans jamais
relire. Le pari de ce pack est inverse. Un vault tient quand un agent l'écrit et le lit en
boucle, et c'est cette boucle que les skills construisent.

Le pack sort de missions d'accompagnement réelles auprès de dirigeants. Les principes plus
bas ne sont pas théoriques, ce sont ceux qui ont survécu au contact des utilisateurs.

## Installation

Dans Claude Code :

```
/plugin marketplace add https://github.com/lightpoichich/vault-skills
/plugin install second-cerveau@vault-skills
```

Un seul plugin embarque tout le pack. Pour les mises à jour :

```
/plugin marketplace update vault-skills
```

## Le cheminement au quotidien

Les skills ne se lancent pas au hasard : ils s'enchaînent le long du cycle de vie d'un vault.
On l'amorce **une fois**, on le fait vivre **chaque jour**, on l'entretient **au signal**.

```
AMORÇAGE  (une seule fois, dans l'ordre)
   interview-vault ─▶ kickstart-vault ─▶ kickstart-persona ─▶ vault-skill-creator
      le plan            le vault           les agents          leurs compétences
                            │
                            └─ pose déjà une persona « Chief of Staff » (cos) utilisable tout de suite

QUOTIDIEN  (en boucle, à chaque session de travail)
   ┌─ matin ───────────────────────────────────────────────┐
   │  brief-du-jour   priorités · alertes · agenda · todos  │
   └────────────────────────────────────────────────────────┘
                            │
                            ▼   au fil du travail, quand le besoin tire
        import-note      une note / URL / doc entre au bon endroit
        nouveau-projet   un chantier naît — ou se complète
                            │
                            ▼   fin de session
        sync-vault       répercute décisions & statuts, garde les fiches concises

AU SIGNAL  (quand quelque chose le déclenche)
        extraire-trame   une pratique revient ≥ 2 fois  ─▶  trame réutilisable
        gerer-area       l'épine dorsale bouge           ─▶  naître / renommer / scinder / archiver
        audit-vault      contrôle technique mensuel du contenant
```

**Lecture du schéma.** L'amorçage est une chaîne : chaque skill consomme la sortie du
précédent (l'interview produit le plan, le plan devient le vault, le vault accueille les
agents, les agents reçoivent leurs compétences). Le quotidien est une boucle ouverte :
`brief-du-jour` ouvre la journée, `import-note` et `nouveau-projet` se déclenchent à la
demande au milieu du travail, `sync-vault` la referme proprement. Les skills « au signal »
ne sont pas planifiés : ils répondent à un évènement (une répétition repérée, une
responsabilité qui change, le rituel mensuel).

**Tu peux travailler hors du vault.** Les skills du quotidien se lancent depuis n'importe
quel dossier — y compris un dossier projet sur ton disque, en dehors du vault. Ils retrouvent
le vault par son chemin absolu, et `nouveau-projet` relie ce dossier de travail à sa fiche.

## Les skills, un par un

Le pack compte onze skills, répartis en trois familles selon le moment du cycle de vie.
Déplie chaque skill pour le détail.

### Famille 1 — Amorcer *(create)*

La chaîne d'amorçage, dans l'ordre : d'abord le plan, puis le squelette, puis les agents,
puis leurs compétences. On la déroule une seule fois, au démarrage d'un vault.

<details>
<summary><b>interview-vault</b> — l'interview qui dessine ton vault</summary>

Le premier maillon. Une conversation guidée qui cartographie ton activité (tes domaines de
responsabilité, tes projets, tes outils, tes irritants) et en tire `00-Inbox/plan-vault.md`,
le plan que la suite exécutera.

Le skill est **adaptatif** : il ne te demande jamais « tu es tech ou pas ? ». Un DG, un CTO
ou un artisan obtiennent chacun la structure qui colle à leur métier, sans questionnaire figé.
Il n'écrit que dans `00-Inbox/` et ne crée aucune fiche — il prépare, il ne construit pas.

**Tu le lances quand** tu pars d'un vault vide et que tu veux poser sa structure avant de la
matérialiser.

</details>

<details>
<summary><b>kickstart-vault</b> — le scaffold du vault depuis le plan</summary>

Transforme le `plan-vault.md` en vault réel : l'arborescence PARA, `_Meta/Schema.md` (le
contrat qui garde les fiches cohérentes dans le temps), la gouvernance, le `CLAUDE.md` racine,
et les fiches-coquilles de tes Areas et Projects — le tout en *generate-don't-write* : il pose
la structure, **jamais du faux contenu métier**.

Il fait deux choses de plus qui rendent le vault vivant dès la première minute : il installe
deux garde-fous automatiques (un bilan de santé au démarrage, un garde-fou à l'écriture), et
il dépose une persona **Chief of Staff** par défaut (alias terminal `cos`) livrée avec le
skill `brief-du-jour`. Tu tapes `cos`, tu demandes ton brief, ça marche — sans aucun
connecteur.

**Tu le lances quand** l'interview a produit ton plan et que tu veux bâtir la structure.

</details>

<details>
<summary><b>kickstart-persona</b> — un nouvel agent dans ton vault</summary>

Crée le *shell* d'une persona Claude : son identité dans `_personas/{slug}/CLAUDE.md` (son
rôle, son ton, ce qu'elle a le droit de lire et d'écrire, ses garde-fous), un alias terminal
pour la lancer en un mot, et un backlog de routines à encoder plus tard.

À ce stade, **l'identité d'abord, les capacités ensuite** : la persona sait qui elle est et où
elle a le droit d'agir, mais elle n'a pas encore de compétences métier. C'est volontaire — on
ne crée pas une persona par tâche, on ajoute des compétences à une persona existante.

**Tu le lances quand** tu veux un assistant dédié (RH, Métier, Veille, Commercial…) au-delà du
Chief of Staff par défaut.

</details>

<details>
<summary><b>vault-skill-creator</b> — encode une routine en compétence</summary>

Prend une routine récurrente (« mon triage de mails du lundi », « ma prépa de comité ») et
l'encode en skill concret, placé automatiquement au bon endroit :
`_personas/{slug}/.claude/skills/` si la compétence appartient à un agent, racine du vault si
elle est transverse.

Il demande **toujours d'où viennent les données** de la routine et propose l'accès qui va avec
(connecteur, import) plutôt que de supposer. C'est un fork du `skill-creator` officiel
d'Anthropic — voir Attribution.

**Tu le lances quand** tu veux donner une vraie compétence métier à une persona, en partant
des routines listées dans son backlog.

</details>

### Famille 2 — Faire vivre *(run)*

Le quotidien, une fois le vault posé. Ces skills lisent le registre `_Meta/sources.md` (les
connecteurs que tu as déclarés) et s'adaptent à ce qui est branché. Sans aucun connecteur, le
vault suffit toujours à produire un résultat utile.

<details>
<summary><b>brief-du-jour</b> — le battement quotidien</summary>

Agrège ton agenda, tes todos, les réunions de la veille, tes messages et l'état de ton vault
en une fiche `00-Inbox/briefs/{date}.md` : Priorités, Alertes, Agenda, Todos — et une section
« À valider » quand des livrables attendent ton feu vert.

Il est **porté par la persona Chief of Staff** : il ne s'active que lancé depuis `cos`, pas
globalement. Et il **dégrade proprement** — si une source manque (pas de connecteur agenda,
par exemple), il produit quand même un brief utile à partir du vault seul.

**Tu le lances quand** tu ouvres ta journée et veux savoir où tu en es. (« fais-moi le brief »,
« quoi de neuf ce matin ».)

</details>

<details>
<summary><b>import-note</b> — fait entrer une note au bon endroit</summary>

Fait entrer un contenu externe — une URL, une page Notion, un fichier, un texte collé — dans
le vault, transformé en fiche propre : la bonne zone PARA, un frontmatter conforme au Schema,
et des `[[wikilinks]]` vers les fiches liées.

C'est le **lazy-pull** : une note entre **quand un besoin la tire**, pas en bloc le premier
jour. Un import qui atterrit dans `00-Inbox/` sans rangement n'a rien importé — le vrai travail,
c'est le classement. Pour le sensible, il pose un renvoi, jamais une copie.

**Tu le lances quand** tu veux ranger un article, un doc ou une page dans ton vault.

</details>

<details>
<summary><b>nouveau-projet</b> — fait naître (ou complète) un chantier</summary>

Crée le foyer d'un projet sur un vault déjà vivant : le dossier `10-Projects/{slug}/`, sa fiche
liée à l'Area parente, puis le rattachement du contexte réel qui existe déjà (la note où l'idée
est née, la réunion de décision, un fil d'emails) via `import-note`. Il n'invente aucun contenu.

Le même geste **complète** une coquille déjà posée : il ne remplit que les trous, sans jamais
réécrire l'existant. Et lancé depuis un dossier de travail hors vault, il relie ce dossier à la
fiche (champ `dossier-travail`) — la prochaine fois que tu ouvres ce dossier, le projet se
recharge tout seul.

**Tu le lances quand** tu ouvres un nouveau chantier, ou qu'un projet existant est resté vide.

</details>

<details>
<summary><b>extraire-trame</b> — capitalise une pratique récurrente</summary>

Fait émerger le savoir qui existe en creux dans ton vault. Quand une pratique revient (au moins
**deux occurrences réelles**), il en extrait la forme commune et la capitalise en trame
réutilisable dans `30-Resources/`, avec les `[[wikilinks]]` vers les cas fondateurs.

Chaque section de la trame **trace vers un cas réel** — rien d'inventé, aucune donnée sensible
ne migre. C'est un skill **consultatif** : la généralisation est un jugement, donc il propose et
tu valides avant écriture.

**Tu le lances quand** tu te dis « ça, je le refais à chaque fois » — ou quand `sync-vault` te
signale un candidat à trame.

</details>

<details>
<summary><b>gerer-area</b> — gère l'épine dorsale du vault</summary>

Une Area (un domaine de responsabilité continu) ne se termine jamais, mais elle évolue : elle
grossit, se scinde, en absorbe une voisine, ou meurt quand la responsabilité disparaît.
`gerer-area` couvre tout ce cycle de vie : faire naître, compléter, renommer, scinder,
fusionner, archiver.

Les gestes qui touchent plusieurs fichiers suivent un **plan validé avant exécution** (jamais
de modification partielle en silence), et l'archivage a des pré-checks bloquants : un projet
encore actif doit être réaffecté d'abord, un contenu utile promu en Resource. À la naissance,
il pose la question anti-cimetière : **qui va la lire ?**

**Tu le lances quand** la structure de tes responsabilités bouge.

</details>

### Famille 3 — Entretenir *(maintain)*

Les skills qui gardent le vault vrai et propre dans la durée. Leur intention est la fiabilité,
pas la production de valeur — c'est ce qui les distingue de la famille « faire vivre ».

<details>
<summary><b>sync-vault</b> — le curateur autonome</summary>

Réconcilie les fiches avec la réalité du travail en cours — décisions prises, statuts qui
changent, todos nés ou faits — **et les garde concises** : il consolide, réécrit et élague le
bruit au lieu d'empiler. Un vault utile est à jour *et* dense, pas un journal qui gonfle jusqu'à
noyer le signal.

Il agit **seul, sans demander de validation**, et rend compte après coup. Il entretient deux
mémoires : les fiches du vault, et la mémoire native de Claude Code (le petit digest rappelé au
démarrage de chaque session). Il gère aussi la sortie des livrables en attente — mais ne valide
ni n'envoie jamais à ta place.

**Tu le lances quand** une session a fait bouger des choses et que tu veux les répercuter.
(« sync le vault », « mets à jour le vault ».)

</details>

<details>
<summary><b>audit-vault</b> — le contrôle technique périodique</summary>

Là où `sync-vault` cure le *contenu* au fil de l'eau, `audit-vault` inspecte le *contenant*. Il
détecte en lecture seule (wikilinks cassés, fiches orphelines, frontmatter hors Schema, projets
à archiver, Areas mortes ou obèses…), produit un rapport daté dans `00-Inbox/`, et **n'agit que
sur ta validation**.

Trois lots de traitement : les fixes mécaniques en un seul oui (avec un filet git), les gestes
de structure délégués au skill dédié (`gerer-area`), et les décisions de fond laissées à
l'humain. Un fix mécanique restaure une règle — il n'invente jamais de contenu.

**Tu le lances quand** tu veux faire le point, sur un rituel mensuel ou un « c'est le bazar ».

</details>

## Principes de conception

- **Generate-don't-write.** Les skills génèrent structure, schémas et shells. Jamais de
  faux contenu métier.
- **Lazy-pull plutôt que migration big-bang.** Une note entre dans le vault quand un besoin
  la tire, pas en bloc le premier jour.
- **Chaque dossier a un consommateur.** Une structure que personne ne lit est un cimetière
  en construction.
- **Gouvernance d'abord.** Le périmètre, les données sensibles et les règles d'accès des
  agents sont posés au scaffold, avant le moindre contenu.
- **Sources déclarées, pas codées en dur.** La variabilité des connecteurs vit dans
  `_Meta/sources.md` ; un skill tente la source déclarée et bascule sur un collage manuel
  si elle manque.
- **Travailler hors du vault.** Les skills retrouvent le vault par son chemin absolu déclaré
  dans le `~/.claude/CLAUDE.md` global : on peut les lancer depuis n'importe quel dossier de
  travail (un dossier projet sur le disque, hors du vault) sans qu'ils échouent. `nouveau-projet`
  relie alors ce dossier à sa fiche via le champ `dossier-travail`, et la fiche du projet se
  recharge automatiquement la prochaine fois qu'on ouvre ce dossier.

## Installation manuelle (sans plugin)

```bash
git clone https://github.com/lightpoichich/vault-skills.git
cp -R vault-skills/skills/* ~/.claude/skills/
```

Puis relancer Claude Code. À noter : `brief-du-jour` n'apparaît pas dans `skills/`, il
voyage dans le bundle de `kickstart-vault`, qui le dépose dans la persona Chief of Staff
au moment du scaffold.

## Attribution

`vault-skill-creator` est une adaptation du `skill-creator` officiel © Anthropic
(marketplace claude-plugins-official) : placement vault automatique, étape « sources de
données », évaluation rendue optionnelle. Le moteur et les scripts d'origine sont
conservés ; la licence est dans `skills/vault-skill-creator/LICENSE.txt`.

---

Construit par [Lucas Clément](https://devlc.co), delivery de produits digitaux et
accompagnement Claude Code pour dirigeants.
