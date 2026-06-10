# Placement & conventions vault (référence)

Ce document détaille la **Phase 0** de `vault-skill-creator` : comment situer un vault, choisir le
bon emplacement pour un skill, respecter les conventions du vault, et porter un skill existant. À
lire quand tu hésites sur le *tier* ou une convention.

---

## 1. Détecter la racine du vault

Un vault vault-centric (celui que produisent `kickstart-vault` + `kickstart-persona`) se reconnaît à
trois marqueurs présents ensemble à sa racine : `CLAUDE.md`, `_Meta/Schema.md`, `_personas/`. On
remonte l'arborescence depuis le dossier courant jusqu'à les trouver :

```bash
d="$PWD"
while [ "$d" != "/" ]; do
  if [ -f "$d/CLAUDE.md" ] && [ -f "$d/_Meta/Schema.md" ] && [ -d "$d/_personas" ]; then
    VAULT_ABS="$d"; break
  fi
  d="$(dirname "$d")"
done
echo "${VAULT_ABS:-HORS-VAULT}"
```

C'est **exactement** le snippet de `kickstart-persona` — même contrat, même résultat, pour rester
cohérent dans toute la famille. Tout chemin se déduit ensuite de `$VAULT_ABS` (jamais de chemin codé
en dur, jamais le vault d'un autre).

**Si `HORS-VAULT`** : pas de vault détecté → se comporter comme le skill-creator officiel (placement
au choix de l'utilisateur ou dans le cwd). Rien de ce qui suit ne s'applique. Ne pas tenter de
« forcer » une structure vault dans un dossier qui n'en est pas un.

---

## 2. Les trois tiers de skills (où un skill peut vivre)

Claude Code charge les skills `.claude/skills/` du dossier de lancement **et de chaque parent**
jusqu'à la racine. D'où trois étages, du plus large au plus rattaché :

| Tier | Emplacement | Chargé quand | Pour quoi |
|---|---|---|---|
| **Transverse (vault)** | `{vault}/.claude/skills/` | partout dans le vault | capacités utiles à toutes les personas : `import-note`, `capture`, `audit-vault` |
| **Persona-spécifique** | `_personas/{slug}/.claude/skills/` | seulement quand on lance cette persona | la capacité d'un rôle : `triage-mails` (CoS), `relecture-pv-cse` (RH) |
| **Machine-global** | `~/.claude/skills/` (hors vault) | toutes sessions, toute machine | rien de spécifique à un vault — **à éviter pour un skill de vault** |

**Règle d'or :** un skill de vault ne va **jamais** en `~/.claude/skills/` global. Il y serait
détaché du vault, non versionné avec lui, et chargé même hors contexte. C'est précisément le défaut
du skill-creator vanilla qu'on corrige ici.

### Choisir entre persona-spécifique et transverse

Le cwd tranche le plus souvent tout seul, parce que la posture de travail par défaut est de lancer la
persona via son alias (`{slug}` fait `cd _personas/{slug}/ && claude`) :

- **cwd dans `_personas/{slug}/`** → presque toujours **persona-spécifique**. Cible :
  `_personas/{slug}/.claude/skills/{name}/`.
- **cwd à la racine du vault** (ou ailleurs dans le vault hors persona) → probablement **transverse**.
  Cible : `{vault}/.claude/skills/{name}/`. **Confirmer** : « cette capacité ne sert qu'à une persona,
  ou à tout le vault ? ».

Le bon test mental : *« est-ce que cette capacité a du sens en dehors de cette persona ? »* Si non →
persona-spécifique (le défaut, et le plus fréquent). Si oui (un utilitaire de vault) → transverse.

> Cohérent avec la décision d'archi « tout agent vit dans `_personas/` » : il n'existe **pas** de
> skill au niveau d'une Area (ex. pas de `20-Areas/rh-social/.claude/skills/`). Une capacité est soit
> portée par une persona, soit transverse au vault. Rien entre les deux.

---

## 3. Lire le backlog de la persona

`kickstart-persona` pose, pour chaque persona, un `_personas/{slug}/capacites-a-construire.md` : la
liste des routines récurrentes à encoder en skills, au format
`- [ ] **{tâche}** — input : … · action : … · livrable : … · fréquence : …`.

C'est le **pont** vers ce skill : s'il existe, le lire en Phase 0, lister ce qui reste à faire, et
proposer d'attaquer la routine la plus rentable (la plus fréquente ou la plus pénible). En fin de
course, **cocher la case** correspondante (voir SKILL.md, « Raccord au backlog »).

Si le backlog n'existe pas (persona créée sans tâche nette, ou skill demandé à la volée), pas de
blocage : on encode quand même, et on propose de créer/compléter le backlog pour la trace.

---

## 4. Conventions que le skill généré doit respecter

- **Nommage en kebab-case** (`triage-mails`, `relecture-pv-cse`) — pour le dossier du skill comme
  pour son `name`. (Déjà validé par `scripts/quick_validate.py`.)
- **Frontmatter natif de skill** : `name` + `description` (+ `compatibility` si vraiment utile).
  **Jamais** de frontmatter de note vault (`type:`, `tags:`, `status:`…). Un SKILL.md n'est pas une
  fiche Obsidian. Comme il vit sous `.claude/`, il est exclu des hooks du vault — donc pas de stamping
  `created`/`updated` ni de nudge frontmatter à craindre, et rien à ajouter pour « se conformer au
  Schema ».
- **La procédure hérite de la discipline vault de la persona** (elle s'exécute dans sa session) :
  - **routage par destination** : un output qui est un **livrable** sortant (mail, courrier,
    proposition…) → `00-Inbox/_drafts/` en `statut: en-attente` + `lien`, **jamais d'envoi
    automatique** ; un output qui est du **savoir** interne (fiche, résumé, synthèse) → écriture
    **directe** au bon endroit PARA (voir `governance.md`, « Savoir vs Livrable ») ;
  - relations entre fiches en `[[wikilinks]]`, jamais de chemins en dur dans le contenu ;
  - **lire `_Meta/Schema.md`** avant d'écrire une note, pour respecter le contrat frontmatter ;
  - **renvoi-jamais-copie** : une source externe se référence (lien + une ligne de contexte dans
    `30-Resources/references-externes/`), elle ne se recopie pas dans le vault ;
  - marqueur **🔒** pour le sensible ; ne pas faire fuiter de données confidentielles hors des zones
    autorisées de la persona.
- **Generate-don't-write** : encoder la procédure *réelle* issue de l'interview. Ne pas inventer
  d'étapes, d'exemples, de fichiers ou de cas que l'utilisateur n'a pas décrits. Un skill brodé ment
  sur ce que la persona sait faire.
- **Sources de données explicites** : la procédure doit dire d'où vient son input (zone du vault, MCP,
  ou collage manuel avec un `TODO : brancher le MCP X`).

---

## 5. Porter un skill existant (ex. depuis Claude Desktop)

Cas courant : l'utilisateur a déjà un « skill » ou un prompt qui marche sur Claude Desktop (ex. un
`cr-aurae` qui résume une réunion) et veut le **rapatrier dans le vault**.

1. **Récupérer la matière** : le prompt/procédure existant, ses entrées et sorties typiques.
2. **Re-héberger au bon tier** (Phase 0) : presque toujours `_personas/{slug}/.claude/skills/{name}/`.
3. **Renommer en kebab-case** si besoin, et donner une `description` qui déclenche bien.
4. **Réaligner sur les conventions vault** (section 4) : remplacer les sorties « dans le chat » par
   des écritures cadrées (drafts → `00-Inbox/_drafts/`, traces → la fiche projet), brancher l'input
   sur une zone du vault ou un MCP plutôt que sur un copier-coller systématique.
5. **Tester en vrai** dans la persona (cf. SKILL.md, « Évaluation optionnelle »), ajuster, cocher le
   backlog.

Le portage n'est pas un copier-coller : c'est l'occasion de faire passer un prompt « Desktop » au
régime vault (placement, données, discipline).
