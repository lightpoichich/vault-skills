---
name: kickstart-persona
description: >-
  Génère le *shell* d'une persona Claude dans un vault Obsidian vault-centric : crée
  `_personas/{slug}/CLAUDE.md` (rôle, ton, zones de lecture/écriture, garde-fous) + le dossier
  `.claude/skills/` de la persona, et pose un alias terminal pour la lancer en un mot. Utilise
  ce skill dès que l'utilisateur veut ajouter un agent/une persona à son vault — Chief of Staff,
  RH, Métier, Veille, ou n'importe quel rôle — ou dit « crée-moi un agent », « nouvelle persona »,
  « ajoute un CoS », « je veux un assistant RH dans mon vault », « monte-moi une persona métier ».
  Path-agnostique et autoportant : détecte la racine du vault et n'écrit aucun chemin codé en dur.
  Ne génère QUE l'identité (le shell) — les capacités métier (skills) s'ajoutent ensuite via
  `skill-creator`. NE PAS l'utiliser pour scaffolder le vault lui-même (c'est `kickstart-vault`),
  ni pour créer un projet/une fiche PARA, ni pour écrire un skill métier.
---

# Kickstart Persona

Crée le **shell** d'une persona Claude dans un vault Obsidian vault-centric. Une persona, c'est
un rôle incarné : un `CLAUDE.md` qui définit **qui elle est** (rôle, ton), **ce qu'elle voit et
touche** (zones de lecture/écriture dans le vault) et **ce qu'elle s'interdit**. Ce skill pose
cette identité — rien de plus. Les **capacités** (les skills métier qu'elle sait exécuter)
viennent après, une par une, via `skill-creator`.

La distinction identité / capacités est le cœur du design : on construit un agent une fois
(son shell), puis on lui ajoute des compétences au fil des besoins réels. Mélanger les deux
mène à des personas figées qu'on réécrit à la main — exactement ce qu'on veut éviter.

**Le contrat en deux temps** (à garder clair tout du long) :
- **Ici (kickstart-persona)** : l'interview capture **qui** est la persona (rôle, ton, périmètre)
  et **ce qui revient** (le backlog de tâches récurrentes). On pose l'identité, on note les routines —
  on n'en code aucune.
- **Ensuite (skill-creator)** : chaque routine devient une **procédure exacte encodée comme un skill**,
  créé **dans `_personas/{slug}/.claude/skills/`** (le tier persona-spécifique). C'est là que vit le
  « comment » — étape par étape, format de sortie, garde-fous propres à la tâche. La persona y gagne
  ses bras, une compétence à la fois, et ces skills restent rattachés à elle (ils ne fuient pas dans
  les autres personas).

Autrement dit : l'interview fixe le périmètre, les skills portent les procédures. Ne jamais essayer
d'écrire la procédure d'une tâche dans le `CLAUDE.md` de la persona — sa place est un skill.

> **Frontière stricte** : `kickstart-persona` **ne crée aucun skill** et **n'invoque pas**
> `skill-creator`. Il s'arrête à l'identité (le `CLAUDE.md`) + le backlog (la liste des routines).
> La création des skills est une **étape séparée et ultérieure**, faite une par une avec
> `skill-creator`, dans `_personas/{slug}/.claude/skills/`. Le dossier `.claude/skills/` reste donc
> **vide** à la sortie de ce skill — c'est normal et voulu.

## Pourquoi ces partis pris (à garder en tête tout du long)

- **Generate-don't-write.** On génère le shell à partir de ce que l'utilisateur décrit (rôle,
  zones), jamais en inventant des responsabilités ou des compétences qu'il n'a pas nommées. Et
  on **ne pré-écrit aucun skill métier** : si on se surprend à coder un `triage-mails.md` à la
  main, c'est le signal qu'il faut lancer `skill-creator`, pas écrire un fichier.
- **Tout agent vit dans `_personas/{slug}/`.** Une persona est un **outil**, pas de la mémoire :
  elle agit sur le vault, elle n'y stocke pas de connaissance. Donc jamais de fiche dans
  `20-Areas/`, jamais d'agent « résident » d'une Area. La règle d'or du vault — *tout ce qui a
  valeur de mémoire vit dans le vault, les personas le produisent ou le consomment* — en dépend.
- **Le `CLAUDE.md` de la persona est un minimum, pas un doublon.** Claude Code remonte
  l'arborescence et charge le `CLAUDE.md` racine du vault (la carte, les conventions, le Schema,
  **et le ton**) **automatiquement**. La persona n'a donc qu'à porter ce qui lui est propre : son
  rôle, son périmètre, et **un écart de ton seulement s'il est justifié** par le rôle (le ton de base
  est hérité du racine — voir étape 6). Recopier la carte, les conventions ou le ton du vault dans
  chaque persona, c'est créer de la dette qui se périme.
- **Identité one-shot, capacités incrémentales.** Le shell se pose en une fois. Les skills
  s'ajoutent quand un besoin réel émerge (« je refais ce triage chaque lundi » → un skill). C'est
  ce qui garde les personas vivantes au lieu de sur-spécifiées d'avance.
- **Path-agnostique + autoportant.** Ce skill ne connaît aucun vault en particulier. Il
  **détecte la racine du vault** depuis le dossier courant et en déduit le chemin absolu pour
  l'alias. Aucun chemin codé en dur (ni `~/mon-vault`, ni le vault de quelqu'un d'autre) : il
  marche pour n'importe quel élève, sur sa machine.
- **Non destructif + idempotent.** Si la persona existe déjà, on demande avant d'écraser. Si
  l'alias est déjà là, on ne le duplique pas. Une ré-exécution complète ce qui manque, sans
  casser l'existant.

## Prérequis (à vérifier, pas à supposer)

La persona se greffe sur un vault déjà scaffolté. Avant tout, **vérifier** que la racine du
vault contient :

- `CLAUDE.md` (la carte du vault — la persona en héritera)
- `_Meta/Schema.md` (le contrat frontmatter — la persona devra le respecter en écrivant)
- `_personas/` (le dossier des agents, même vide)

Si ces trois éléments sont absents (et introuvables en remontant l'arborescence), **s'arrêter** :
le vault n'est pas prêt. Diriger l'utilisateur vers `kickstart-vault` pour le scaffolder d'abord.
Ne jamais créer une persona « dans le vide ».

> Note : `kickstart-vault` a déjà posé une persona **Chief of Staff** par défaut (`_personas/cos/`,
> livrée avec `brief-du-jour`) comme exemple amorcé. Donc `_personas/` n'est en général pas vide au
> premier passage ici. Si l'utilisateur relance pour un CoS, l'étape 4 le détectera et proposera
> compléter/écraser/annuler — c'est l'exemple à dupliquer pour ses autres rôles, pas à recréer.

## La découverte (l'interview) — creuser la réalité avant de cadrer

Une persona ne vaut que si elle est taillée sur le travail réel de la personne. Demander froidement
« quel rôle ? quelles zones ? » produit une persona générique et tiède, vite abandonnée. L'enjeu de
cette phase est de **comprendre la réalité métier** — où part le temps, ce qui se répète, ce qu'on
rêverait de déléguer — puis d'en **déduire** un rôle net et un périmètre justifié. C'est une
conversation, pas un formulaire : plusieurs tours, on creuse, on reformule. C'est aussi le moment
le plus précieux du skill — ne pas le brader pour aller vite scaffolder.

Conduis-la dans cet esprit (banque de questions et techniques de relance dans
`references/discovery-interview.md`) :

1. **Partir du réel, pas du rôle.** Plutôt que « quel est le rôle ? », faire raconter le quotidien :
   où part le temps, quelles tâches reviennent chaque semaine, quels livrables se refont sans cesse,
   qu'est-ce qui sature ou agace. Demander des exemples concrets et récents (« les trois dernières
   choses que tu aurais aimé ne pas avoir à faire toi-même »). On part de SON activité — un dirigeant
   de cabinet, un fondateur, un responsable n'ont pas les mêmes irritants.
2. **Creuser quand c'est vague.** « Aide-moi à gérer mes projets » n'est pas exploitable : relancer
   pour le rendre concret — quels projets, quelle action exacte, à quelle fréquence, avec quelles
   infos en entrée et quel livrable en sortie. Ne pas se contenter de la première réponse ; une ou
   deux relances ciblées valent mieux qu'un périmètre flou.
3. **Reformuler et faire valider.** Régulièrement, rejouer ce qu'on a compris en une formulation
   nette (« si je résume, cette persona te décharge de X et Y, et produit Z — c'est ça ? »). La
   reformulation fait émerger les trous et les malentendus : c'est là que le cadrage se fait vraiment.
4. **Dériver le périmètre des tâches, pas l'inverse.** Une fois les tâches récurrentes claires, en
   déduire ce que la persona doit **lire** (où vivent les infos nécessaires) et où elle **écrit** (où
   atterrissent ses productions). Proposer ce périmètre à partir de la carte du `CLAUDE.md` racine, le
   confirmer. (Voir `references/persona-design.md` : « lire large, écrire étroit ».)

Tu sais que tu peux converger quand tu peux énoncer, sans flou : le **rôle** en une phrase, **2 à 4
tâches récurrentes** concrètes qui le justifient, et un **périmètre** lecture/écriture ancré sur des
dossiers réels. Tant que l'un des trois reste vague, continue à creuser — c'est le cœur de la valeur.
À l'inverse, si la personne répond d'emblée de façon précise et complète, ne pas étirer l'échange
artificiellement : une reformulation pour valider, et on avance.

**Le nom** vient souvent tout seul du rôle ; sinon, le proposer (« on l'appelle “Chief of Staff” ? »).

**Ce qu'on en garde (et ce qu'on n'écrit pas).** La découverte sert à cadrer le *shell* — le rôle et
le périmètre. Les tâches récurrentes mises au jour ne deviennent **pas** des skills maintenant
(generate-don't-write) : elles forment le *backlog de capacités*, qu'on **persiste** dans
`_personas/{slug}/capacites-a-construire.md` (étape 8) pour qu'il ne se perde pas, et qu'on encodera
ensuite une à une via `skill-creator` dans le dossier `.claude/skills/` de la persona. On note les
routines ici, on code les procédures là-bas.

## Procédure

### 1. Détecter et valider la racine du vault
Depuis le dossier courant, **remonter** l'arborescence jusqu'à trouver la racine du vault (le
dossier qui contient à la fois `CLAUDE.md`, `_Meta/Schema.md` et `_personas/`). Mémoriser son
**chemin absolu** — il servira pour l'alias.

```bash
d="$PWD"
while [ "$d" != "/" ]; do
  if [ -f "$d/CLAUDE.md" ] && [ -f "$d/_Meta/Schema.md" ] && [ -d "$d/_personas" ]; then
    VAULT_ABS="$d"; break
  fi
  d="$(dirname "$d")"
done
echo "${VAULT_ABS:-INTROUVABLE}"
```

Si le résultat est `INTROUVABLE` → s'arrêter (cf. Prérequis) et orienter vers `kickstart-vault`.
Tout le reste de la procédure se fait **relativement à `$VAULT_ABS`**.

### 2. Mener la découverte (plusieurs tours)
Conduire la conversation décrite plus haut : partir du quotidien réel, creuser les réponses vagues
avec des relances ciblées, reformuler pour faire valider. Lire la carte du `CLAUDE.md` racine pour
proposer un périmètre ancré sur des dossiers réels. **Ne pas dériver vers la génération** tant que
le trio rôle + tâches récurrentes + périmètre n'est pas net. Garder en tête le backlog de tâches
récurrentes : il servira au résumé (étape 8) et à amorcer `skill-creator`.

### 3. Dériver le slug
Nom en kebab-case, avec les **abréviations naturelles** quand elles existent : « Chief of Staff »
→ `cos`, « RH » → `rh`, « Métier » → `metier`, « Veille réglementaire » → `veille-reglementaire`.
Si le slug n'est pas évident, le **proposer et demander confirmation** — c'est lui qui nommera
l'alias que l'utilisateur tapera tous les jours.

### 4. Vérifier que la persona n'existe pas déjà
```bash
ls "$VAULT_ABS/_personas/{slug}/" 2>/dev/null
```
Si le dossier existe → prévenir et demander : compléter, écraser, ou annuler. **Ne jamais
écraser un `CLAUDE.md` de persona existant sans accord explicite.**

### 5. Créer la structure
```bash
mkdir -p "$VAULT_ABS/_personas/{slug}/.claude/skills"
```
Le dossier `.claude/skills/` est volontairement **vide** : c'est le **tier persona-spécifique** où
`skill-creator` créera plus tard chaque routine sous forme de skill (chargé seulement quand on lance
cette persona). C'est l'emplacement qui garde les procédures rattachées à la persona. Ne rien y
mettre maintenant — l'identité d'abord, les capacités ensuite.

### 6. Générer le `CLAUDE.md` de la persona
Écrire `_personas/{slug}/CLAUDE.md` depuis `assets/persona-claude-template.md`, en remplissant
les emplacements avec le rôle et les zones issus de l'interview. **Rien d'inventé** au-delà de
ce que l'utilisateur a décrit : si une section n'a pas de matière, la laisser au minimum plutôt
que de broder. Garder le fichier court — il hérite du vault, il ne le réplique pas.
- **Ton : hérité, pas redéfini.** La section *Ton* renvoie au `CLAUDE.md` racine (« Suit le ton du
  vault »). N'y écrire un réglage que si le **rôle** réclame un **écart** franc du ton du vault (ex.
  une persona juridique plus formelle, une persona veille plus neutre). Dans ce cas seulement, le
  vérifier avec l'utilisateur en une question ; sinon, ne pas l'ouvrir — ce n'est pas dans le trio de
  convergence (rôle / tâches / périmètre).

### 7. Poser l'alias terminal (idempotent, path absolu)
Ajouter un alias qui lance la persona en un mot, avec le **chemin absolu détecté** (jamais un
chemin en dur d'un autre environnement). Détecter le shell de l'utilisateur et viser le bon
fichier de config ; ne pas dupliquer si l'alias existe déjà.

```bash
RC="$HOME/.zshrc"; [ -n "$BASH_VERSION" ] && RC="$HOME/.bashrc"
LINE="alias {slug}=\"cd '$VAULT_ABS/_personas/{slug}' && claude\""
grep -q "alias {slug}=" "$RC" 2>/dev/null || echo "$LINE" >> "$RC"
```
Indiquer à l'utilisateur de recharger son shell (`source "$RC"`) ou d'ouvrir un nouvel onglet
pour que `{slug}` soit actif.

### 8. Persister le backlog des capacités (le pont vers skill-creator)
La découverte a fait émerger les tâches récurrentes : ce sont les **procédures à encoder ensuite**.
Pour qu'elles ne se perdent pas à la fin de la session, les écrire dans
`_personas/{slug}/capacites-a-construire.md` — un backlog repris **de l'échange** (input → action →
livrable → fréquence), jamais inventé. Pour chacune, préciser qu'elle deviendra un skill créé via
`skill-creator` **dans `_personas/{slug}/.claude/skills/`**. Gabarit :

```markdown
# {Nom} — capacités à construire

> Backlog des routines à encoder en skills (via skill-creator) dans `.claude/skills/`.
> Ce ne sont PAS des capacités déjà en place — c'est un plan de route. Coche au fur et à mesure.

- [ ] **{tâche 1}** — input : {…} · action : {…} · livrable : {…} · fréquence : {…}
- [ ] **{tâche 2}** — …
```

C'est un **plan de route pour l'humain**, pas une capacité : ne jamais le formuler comme si la
persona savait déjà faire ces tâches. Si aucune tâche nette n'est ressortie de la découverte, **ne
pas créer le fichier** — proposer simplement de lancer skill-creator au prochain besoin réel.

### 9. Résumé
Afficher un récap clair :
```
Persona {Nom} créée :
- Identité   : _personas/{slug}/CLAUDE.md
- Capacités  : _personas/{slug}/.claude/skills/  (vide — à remplir via skill-creator)
- Backlog    : _personas/{slug}/capacites-a-construire.md  (les routines à encoder en skills)
- Lancement  : tape `{slug}` dans le terminal (après `source` de ton fichier shell) → session
               directe avec {Nom} chargé

Procédures à encoder ensuite (depuis le backlog — rien n'est codé) :
- {tâche récurrente 1 — la plus fréquente/pénible}
- {tâche récurrente 2}
- {tâche récurrente 3}

Prochaine étape : invoque skill-creator pour construire la première — je suggère
« {tâche la plus rentable} » — et crée-la dans _personas/{slug}/.claude/skills/.
```
Le récap relie clairement les deux temps : l'identité + le backlog sont posés ici ; les procédures
exactes arrivent comme skills dans le dossier de la persona. S'il n'y a pas de backlog, l'omettre.

## La discipline generate-don't-write, concrètement

Un bon shell de persona ressemble à ça — précis sur le périmètre, vide là où il n'y a pas encore
de matière :

```markdown
# Chief of Staff

## Rôle
Bras droit opérationnel : trie l'inbox, suit les projets transverses, rédige les drafts à valider.

## Zones vault
### Je lis
- 10-Projects/
- 20-Areas/gouvernance/
### J'écris dans
- 00-Inbox/_drafts/ (livrables sortants à valider)
- les fiches de 10-Projects/ (suivi d'avancement — savoir interne, écriture directe)
```

> Règle d'écriture d'une persona : **par destination, pas par auteur**. Un **livrable** (sort vers un
> tiers) → `_drafts/` + validation ; le **savoir** interne (suivi, synthèse) → écriture directe. Voir
> `governance.md`, « Savoir vs Livrable ».

Ce qu'on ne fait **jamais** : inventer des skills (« elle sait faire X, Y, Z »), des projets, des
contacts, des process que l'utilisateur n'a pas décrits. Une compétence non encore créée n'existe
pas — elle naîtra via `skill-creator` quand le besoin sera réel. Le shell honnête se remplit ;
le shell brodé ment sur ce que l'agent sait faire.

## Cas limites

- **Vault introuvable** (pas de `CLAUDE.md` / `_Meta/Schema.md` / `_personas/`) → stop, orienter
  vers `kickstart-vault`. Ne jamais scaffolder une persona hors d'un vault.
- **Persona déjà existante** → demander (compléter / écraser / annuler), ne pas écraser en
  silence.
- **Slug ambigu** (nom composé sans abréviation évidente) → proposer un slug et confirmer.
- **Utilisateur hésitant sur les zones** → proposer depuis la carte du vault, ne pas trancher à
  sa place ni tout ouvrir « au cas où » (un périmètre large dilue l'utilité de la persona).
- **Chevauchement de zones d'écriture entre personas** → le **signaler** (« RH et CoS écrivent
  tous deux dans `00-Inbox/_drafts/` — c'est ok si c'est voulu »), sans bloquer. Deux personas
  qui écrivent au même endroit n'est pas une erreur, juste un point d'attention.
- **Ni zsh ni bash détecté** (cas rare) → écrire la ligne d'alias et laisser l'utilisateur la
  placer dans le bon fichier, en l'expliquant.

## Transférabilité (pour un élève qui l'utilise seul)

Ce skill est conçu pour être **copié tel quel** dans n'importe quel `~/.claude/skills/` ou
`.claude/skills/` de vault. Il ne référence aucun vault, nom ou chemin extérieur : la racine est
**détectée** à l'exécution, le gabarit du `CLAUDE.md` vit dans `assets/`. Quand tu l'exécutes,
n'introduis aucune dépendance à l'environnement de l'auteur — reste path-agnostique et travaille
toujours sur le vault de la personne devant toi.

## Fichiers du skill
- `assets/persona-claude-template.md` — gabarit du `CLAUDE.md` d'une persona (à remplir depuis
  la découverte).
- `references/discovery-interview.md` — comment mener la découverte : banque de questions, relances
  pour creuser le vague, techniques de reformulation, signes qu'on peut converger, exemples de
  passage « vague → net ». **À lire** avant de mener l'interview.
- `references/persona-design.md` — guide de conception : qu'est-ce qu'une bonne persona, où elle
  vit dans l'archi vault-centric, les 3 emplacements de skills, comment choisir ses zones de
  lecture/écriture. **À lire** si tu hésites sur le périmètre ou l'architecture.
