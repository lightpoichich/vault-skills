---
name: assistants
description: >-
  Construit l'équipe d'assistants du vault : crée une persona (rôle, périmètre de lecture et
  d'écriture, garde-fous, raccourci terminal, backlog de routines) après une découverte du
  quotidien, puis lui ajoute une compétence, un skill placé dans la persona ou à la racine du vault
  avec ses sources de données. S'utilise quand l'utilisateur dit « crée-moi un agent », « nouvelle
  persona », « je veux un assistant RH », « crée un skill pour mon Chief of Staff », « encode mon
  triage-mails », ou pioche dans capacites-a-construire.md. Pour installer le vault, voir
  /second-cerveau:installer.
---

# Assistants

Deux gestes, dans cet ordre : créer une persona pose son identité (qui elle est, ce qu'elle lit et
écrit, ce qu'elle s'interdit) ; ajouter une compétence lui donne une routine, une à la fois, quand
le besoin est réel. L'identité vit dans `_personas/{slug}/CLAUDE.md`, les compétences dans
`_personas/{slug}/.claude/skills/`.

## Procédure

### 1. Localiser le vault
Localiser le vault : `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-resolve.py" "$PWD"` rend `mode`
(`vault`, `projet`, `none`) et `vault` (racine). Si `CLAUDE_PLUGIN_ROOT` est inconnu, remonter jusqu'à
un dossier contenant `_Meta/`, sinon prendre le chemin absolu du vault déclaré dans
`~/.claude/CLAUDE.md`. Lire ensuite `_Meta/Schema.md` du vault trouvé.

Créer une persona demande un vault installé (`CLAUDE.md`, `_Meta/Schema.md` et `_personas/` à la
racine) ; sinon, s'arrêter et orienter vers `/second-cerveau:installer`. Ajouter une compétence
reste possible hors d'un vault : la Phase 0 de `references/ajouter-competence.md` traite ce cas.

### 2. Aiguiller

| Demande | Geste | Procédure |
|---|---|---|
| « crée-moi un agent », « nouvelle persona », « ajoute un assistant RH » | 1. créer une persona | `references/creer-persona.md` |
| « crée un skill pour {persona} », « encode mon triage-mails », une ligne de `capacites-a-construire.md`, « porte mon skill Desktop dans le vault » | 2. ajouter une compétence | `references/ajouter-competence.md` |

Une demande qui mêle les deux (« un assistant RH qui trie mes candidatures ») commence par le geste
1 ; la routine entre au backlog, puis le geste 2 se propose pour la plus rentable.

### 3. Suivre le geste
Dérouler la référence du geste jusqu'à son récap.

## Garde-fous
- **Rien d'inventé** : la persona reprend le rôle et les zones décrits par l'utilisateur ; la
  compétence encode une routine qu'il a nommée.
- **L'échange d'abord** : découverte avant de fixer une persona, confirmation avant d'écrire une
  ligne de SKILL.md. C'est le moment où une mauvaise hypothèse se rattrape.
- **Non destructif et idempotent** : demander avant d'écraser une persona ou un skill existant ; ne
  pas dupliquer un alias.
- Pas de `~/.claude/skills/` pour un skill de vault.

## Références
- `references/creer-persona.md` : geste 1, de la découverte au récap (slug, structure, `CLAUDE.md`,
  alias, imports, backlog).
- `references/discovery-interview.md` : les quatre tours de la découverte, exemples de questions.
- `references/persona-design.md` : où vit une persona, pourquoi son `CLAUDE.md` reste minimal,
  choix des zones.
- `references/ajouter-competence.md` : geste 2, du placement au raccord au backlog.
- `references/vault-placement.md` : détection du vault, tableau des tiers, backlog, conventions du
  skill généré, portage d'un skill Desktop.
- `assets/persona-claude-template.md` : gabarit du `CLAUDE.md` de persona.

Le geste 2 adapte le `skill-creator` d'Anthropic ; licence dans `LICENSE.txt`.
