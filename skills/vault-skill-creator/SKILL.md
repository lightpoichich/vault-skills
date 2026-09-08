---
name: vault-skill-creator
description: >-
  Crée un skill Claude Code à partir d'une routine récurrente d'une persona et le place dans le vault
  Obsidian : dans _personas/{slug}/.claude/skills/ pour une capacité de persona, à la racine du vault
  pour une capacité transverse. Interroge sur les données lues par la procédure et propose l'accès
  (MCP ou import). S'utilise quand l'utilisateur dit « encode mon triage-mails », « crée un skill pour
  mon Chief of Staff », « porte mon skill Desktop dans le vault », ou pioche dans
  capacites-a-construire.md. Pour créer le vault ou une persona, voir kickstart-vault et
  kickstart-persona.
---

# Vault Skill Creator

Entrées attendues : une routine à encoder (dite en session ou piochée dans le backlog de la
persona), la persona qui la portera, les données qu'elle lit. Sortie : un dossier de skill placé au
bon tier du vault, testé sur un cas réel, coché dans le backlog.

Déroulé :

1. Phase 0 : situer le vault, choisir le tier, lire le backlog.
2. Capturer l'intention et les sources de données, confirmer avant d'écrire.
3. Rédiger le SKILL.md.
4. Tester en vrai dans la persona ; ouvrir `references/eval-loop.md` seulement si une mesure est
   demandée.
5. Améliorer, répéter.
6. Cocher le backlog, faire le récap.

Repérer où l'utilisateur en est dans ce déroulé et reprendre à cette étape : un brouillon existant
part directement au test. Si l'utilisateur ne veut pas d'évaluation, suivre son rythme.

Adapter le vocabulaire à l'utilisateur : « évaluation » et « benchmark » passent ; « JSON » et «
assertion » se définissent en une proposition si rien n'indique qu'il les connaît.

## Phase 0 : contexte vault et placement

À faire avant toute interview. Détail dans `references/vault-placement.md` : détection du vault,
tableau des tiers, backlog, conventions du skill généré, portage d'un skill Desktop.

1. Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
   (`vault`, `repo`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter
   jusqu'à un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
   `~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé.
2. Si `mode` n'est pas `vault`, placer le skill où l'utilisateur le demande (par défaut
   `.claude/skills/` du dossier courant) ; le reste de la Phase 0 ne s'applique pas.
3. Choisir le tier. Un cwd dans `_personas/{slug}/` donne le tier persona, cible
   `_personas/{slug}/.claude/skills/{name}/`. Un cwd ailleurs dans le vault donne le tier
   transverse, cible `{vault}/.claude/skills/{name}/`, à confirmer : « cette capacité sert à
   {persona} seulement, ou à tout le vault ? ». Pas de `~/.claude/skills/` pour un skill de vault.
4. Lire `_personas/{slug}/capacites-a-construire.md` s'il existe et proposer la routine la plus
   rentable.
5. Annoncer le placement et sa raison en une phrase (« dans la persona {slug}, parce que la capacité
   n'a de sens que pour elle »).

## Créer le skill

### Capturer l'intention

La conversation contient souvent déjà la matière : irritants, compétences et sources cités juste
après `interview-vault` ou `kickstart-vault`. Ce contexte sert à préparer les réponses, pas à sauter
les questions. L'échange est le moment où une mauvaise hypothèse se rattrape : mauvais irritant,
format de sortie non voulu, source crue branchée qui ne l'est pas. Poser les cinq questions et faire
confirmer les réponses :

1. Que doit permettre ce skill ?
2. Quand se déclenche-t-il (phrases, contextes) ?
3. Quel format de sortie ?
4. Sur quelles données travaille la procédure, et d'où viennent-elles ? Voir « Sources de données et
   accès ».
5. Comment le tester ? Par défaut en vrai dans la persona ; la mesure quantitative se propose
   seulement si l'utilisateur veut chiffrer.

Point d'arrêt avant d'écrire une ligne de SKILL.md : présenter en quatre ou cinq lignes la routine
retenue, le déclenchement, le format de sortie, la source et sa stratégie d'accès. Si le backlog
compte plusieurs routines, demander laquelle plutôt que d'en choisir une. Attendre un go explicite.
La boucle brouillon, test, amélioration vient après ce go.

### Sources de données et accès

Faire préciser sur quoi travaille la procédure, puis classer chaque entrée.

- Dans le vault : la procédure lit les zones concernées (`20-Areas/{area}/meetings/`,
  `10-Projects/{slug}/`, `30-Resources/`), désignées par leur chemin, fiches liées en
  `[[wikilinks]]`.
- Hors du vault : proposer un accès plutôt qu'un collage manuel à vie. Réunions par le connecteur
  Granola ; mails par le connecteur Gmail ou Graph API, lecture seule souvent suffisante ; notes et
  docs par le connecteur Notion ou un import vers le vault (`import-note`, collage cadré).
- Ne pas forcer le montage d'un connecteur, budget API et droits IT étant des contraintes réelles.
  S'il n'est pas branché, faire tourner la procédure sur une entrée collée, noter `TODO : brancher
  {source}` dans le SKILL.md généré et proposer le branchement en amélioration.
- Le registre des connecteurs est `_Meta/sources.md`. Le skill généré le lit pour résoudre ses
  entrées hors vault et applique sa cascade : déclarée et joignable, l'utiliser ; déclarée et
  injoignable, collage manuel ; non déclarée, la proposer en amélioration ; `renvoi 🔒`, jamais
  copiée.
- Un statut `actif` dans le registre n'est pas une preuve de branchement : sonder la source
  (`ToolSearch`) ou la faire confirmer par l'utilisateur avant de bâtir le skill dessus. Si elle ne
  répond pas, la traiter comme injoignable et proposer de repasser sa ligne en `à brancher`, ou de
  partir sur un irritant dont la source est disponible.
- Une source absente du registre s'y ajoute (statut `à brancher`) au lieu d'être codée dans le
  SKILL.md : le registre reste la source de vérité et les autres skills en profitent.
- Si sonder la source révèle une requête non évidente (filtre par date, scope étroit, payload à
  borner), consigner cette heuristique dans la cellule `accès` de sa ligne. C'est un « comment
  requêter étroit », jamais le schéma de la source, redécouvert à l'appel.
- Consigner la stratégie d'accès retenue dans le SKILL.md généré. Exemple de référence :
  `brief-du-jour`, livré avec la persona Chief of Staff
  (`kickstart-vault/assets/persona-chief-of-staff/.claude/skills/brief-du-jour/`).

### Interview and research

Ask about edge cases, input and output formats, example files, success criteria and dependencies
before writing any test prompt. Check the available MCPs: they serve research (docs, similar skills,
best practices) and, in a vault, they feed the procedure with data (see « Sources de données et
accès »). Research in parallel via subagents when available, otherwise inline, so the user carries
less of the burden.

### Write the SKILL.md

Fill in from the interview:

- `name`: skill identifier, kebab-case, equal to the folder name.
- `description`: the only triggering mechanism; all "when to use" information lives here, not in the
  body. Follow the template below.
- `compatibility`: required tools or dependencies, rarely needed.
- The body: expected inputs, numbered procedure, guardrails specific to the skill, list of
  references.

Description template: plain text without markdown, third person, 400 to 600 characters, three
movements. First, what the skill does, in one sentence (the result, not the design argument).
Second, the verbatim triggers, main case first: « S'utilise quand l'utilisateur dit « a », « b », «
c ». ». Third, at most one exclusion toward the closest neighbour: « Pour Z, voir skill-w. ».

Vault guardrails for the generated skill (native skill frontmatter, discipline of the persona,
explicit sources): `references/vault-placement.md`, section 4.

#### Anatomy of a skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled resources (optional)
    ├── scripts/    executable code for deterministic or repetitive tasks
    ├── references/ docs loaded into context as needed
    └── assets/     files used in output (templates, icons, fonts)
```

#### Progressive disclosure

Three loading levels:

1. Metadata (`name` and `description`): always in context, about 100 words.
2. SKILL.md body: in context whenever the skill triggers, under 500 lines.
3. Bundled resources: loaded as needed; scripts execute without being loaded.

- Near 500 lines, add a layer of hierarchy with pointers on where to read next.
- Cite each reference file from the SKILL.md with guidance on when to read it.
- A reference over 300 lines gets a table of contents.
- A skill covering several domains or frameworks keeps one reference per variant (one file per cloud
  provider, for instance); the SKILL.md carries the workflow and the selection, Claude reads only
  the relevant file.

#### Principle of lack of surprise

A skill contains no malware, exploit code or content that could compromise system security. Its
contents do not surprise the user once described. Decline misleading skills and skills built for
unauthorized access or data exfiltration. A "roleplay as X" skill is fine.

#### Writing patterns

- Imperative form.
- Output formats: give the exact template under its heading (`## Report structure`, then the section
  list `# [Title]`, `## Executive summary`, `## Key findings`, `## Recommendations`).
- Examples: `**Example 1:**` then `Input:` and `Output:` lines; adapt the labels when the domain
  already uses the words input and output.
- Explain why a rule matters in one clause attached to it, rather than capitalised imperatives.
  Capitals and rigid structures are a signal to reframe.
- Make the skill general rather than tied to the interview examples. Draft, then reread with fresh
  eyes and improve.

## Tester le skill

Défaut vault : le test live, sans JSON, benchmark ni sous-agent. Après le brouillon :

1. Recharger le shell si l'alias vient d'être posé (`source ~/.zshrc` ou nouvel onglet).
2. Lancer la persona (`{slug}`), ou rester dans la session courante si on y est déjà.
3. Donner une tâche réelle qui doit déclencher le skill (« fais mon triage de ce matin »).
4. Regarder la sortie avec l'utilisateur, repérer ce qui cloche, ajuster le SKILL.md, recommencer.

Ouvrir `references/eval-loop.md` seulement sur demande explicite de mesure : skill lancé tous les
jours, comparaison de deux versions, problèmes de déclenchement. Il décrit les test cases, les runs
avec et sans skill, le grading, le benchmark, le viewer, la comparaison en aveugle, l'optimisation
de la description et les environnements sans sous-agents. Le présenter comme plus long, utile pour
un skill très réutilisé.

## Improving the skill

Applies after a live test as well as after a measured run.

1. Generalize from the feedback. The skill will run on many prompts; the few examples iterated on
   with the user are a fast proxy, not the target. Against a stubborn issue, try another framing or
   working pattern rather than an overfitted rule.
2. Keep the prompt lean. Read the transcripts, not only the outputs; remove what makes the model
   waste time.
3. Explain the why. Understand what the user meant, even from terse or frustrated feedback, and
   transmit that understanding into the instructions.
4. Look for repeated work. If every test run wrote the same helper script or took the same
   multi-step detour, bundle it once in `scripts/` and point the skill at it.

Thinking time is not the blocker: write a draft revision, then reread it before applying. Stop when
the user is happy, the feedback is empty, or progress stalls.

## Package

Packaging (`python -m scripts.package_skill <path/to/skill-folder>`) serves only to share the skill
outside the vault or to back it up. In the vault, the skill is versioned by git and active as soon
as the persona is relaunched. Run it only when the `present_files` tool is available, then point the
user to the resulting `.skill` file.

## Raccord au backlog et récap

1. Cocher la case dans `_personas/{slug}/capacites-a-construire.md` (`[ ]` en `[x]`) et noter en fin
   de ligne où le skill a atterri. Si la routine n'y figurait pas, proposer de l'ajouter cochée,
   pour la trace.
2. Afficher le récap :

```
Skill {name} créé :
- Emplacement : _personas/{slug}/.claude/skills/{name}/   (tier persona ; racine du vault si transverse)
- Données     : {zones du vault lues, connecteur proposé ou branché, ou entrée manuelle}
- Test        : lance `{slug}` et donne-lui « {tâche réelle déclenchante} »
- Backlog     : case « {routine} » cochée dans capacites-a-construire.md

Prochaine routine à encoder (depuis le backlog) : {la plus rentable suivante}
```

## Garde-fous

- Une routine à la fois ; pas de SKILL.md écrit sans interview ni go explicite.
- Pas de `~/.claude/skills/` pour un skill de vault.
- Le skill généré porte un frontmatter de skill, pas de note Obsidian.
- Évaluation quantitative, optimisation de description et packaging seulement sur demande, jamais
  par défaut.

## Références

- `references/vault-placement.md` : détection du vault, tableau des tiers, backlog, conventions du
  skill généré, portage d'un skill Desktop.
- `references/eval-loop.md` : boucle d'évaluation quantitative (test cases, runs, grading,
  benchmark, viewer, comparaison en aveugle, optimisation de la description, environnements
  Claude.ai et Cowork).
- `references/schemas.md` : tous les JSON (evals, eval_metadata, timing, metrics, grading, feedback,
  benchmark, notes, comparison, analysis, trigger eval set, history).
- `agents/grader.md`, `agents/comparator.md`, `agents/analyzer.md`, `agents/analyzer-benchmark.md` :
  consignes des sous-agents de la boucle d'évaluation, à lire au moment de les lancer.
