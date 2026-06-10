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
/plugin marketplace add lightpoichich/vault-skills
/plugin install second-cerveau@vault-skills
```

Un seul plugin embarque tout le pack. Pour les mises à jour :

```
/plugin marketplace update vault-skills
```

## Le cycle de vie : trois familles

### Famille 1 — Amorcer (*create*)

La chaîne d'amorçage, dans l'ordre : d'abord le plan, puis le squelette, puis les agents,
puis leurs compétences.

1. **interview-vault** mène l'interview de cartographie d'activité et produit
   `00-Inbox/plan-vault.md`, le plan que la suite exécute. Le skill est adaptatif : un DG,
   un CTO ou un artisan obtiennent chacun la structure qui colle à leur métier, sans
   questionnaire figé.
2. **kickstart-vault** scaffolde le vault PARA depuis ce plan : arborescence,
   `_Meta/Schema.md` (le contrat frontmatter), gouvernance, `CLAUDE.md` racine. Il pose
   aussi une persona Chief of Staff par défaut (alias `cos`), livrée avec le skill
   `brief-du-jour`. Le vault est donc utilisable dès le scaffold.
3. **kickstart-persona** crée le shell d'une persona supplémentaire (RH, Métier, Veille…) :
   son identité dans `_personas/{slug}/CLAUDE.md`, un alias terminal, et un backlog de
   routines à encoder. Aucune capacité métier à ce stade, l'identité d'abord.
4. **vault-skill-creator** encode chaque routine du backlog en skill concret, placé
   automatiquement au bon endroit (`_personas/{slug}/.claude/skills/`, ou racine du vault
   quand c'est transverse). Il demande toujours d'où viennent les données et propose
   l'accès qui va avec (connecteur, import). C'est un fork du skill-creator officiel
   Anthropic, voir Attribution.

### Famille 2 — Faire vivre (*run*)

Le quotidien, une fois le vault posé. Ces skills lisent le registre `_Meta/sources.md`
(les connecteurs déclarés de l'utilisateur) et s'adaptent à ce qui est branché. Sans aucun
connecteur, le vault suffit toujours à produire un résultat utile.

- **brief-du-jour** est le battement quotidien : il agrège agenda, todos, réunions de la
  veille, messages et vault en une fiche `00-Inbox/briefs/{date}.md` (Priorités, Alertes,
  Agenda, Todos). Il est porté par la persona Chief of Staff, pas installé globalement.
- **import-note** fait entrer une note externe (URL, page Notion, fichier, texte collé) au
  bon endroit du vault, frontmatter et `[[wikilinks]]` compris. C'est le lazy-pull : une
  note entre quand on en a besoin.
- **nouveau-projet** fait naître un projet sur un vault vivant : le dossier
  `10-Projects/{slug}/`, la fiche liée à son Area, puis le rattachement du contexte réel
  existant via `import-note`. Il n'invente aucun contenu.

### Famille 3 — Entretenir (*maintain*)

- **sync-vault** est le curateur du vault. Il réconcilie les fiches avec la réalité du
  travail en cours (décisions, statuts, todos) et les garde concises : il consolide et
  élague au lieu d'empiler. Il alimente aussi la mémoire native de Claude Code pour le
  rappel en début de session.

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
