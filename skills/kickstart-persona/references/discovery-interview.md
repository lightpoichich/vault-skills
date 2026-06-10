# Mener la découverte — guide d'entretien

La qualité d'une persona se joue ici. Une persona cadrée sur le travail réel de la personne est
utilisée tous les jours ; une persona générique est abandonnée en une semaine. Ce guide donne la
matière pour creuser — questions, relances, reformulation — sans transformer l'échange en
interrogatoire. Adapte au registre de ton interlocuteur : un dirigeant non-technique parle de son
métier, pas de dossiers et de zones.

## L'objectif de l'échange

Sortir de la conversation avec trois choses nettes :
1. **Un rôle en une phrase** — ce dont la persona décharge la personne.
2. **2 à 4 tâches récurrentes concrètes** qui justifient ce rôle (input → action → livrable, fréquence).
3. **Un périmètre lecture/écriture** ancré sur des dossiers réels du vault.

Tant que l'un des trois est flou, on continue. Quand les trois sont clairs, on reformule une
dernière fois et on génère.

## Tour 1 — partir du réel (pas du rôle)

Ne demande pas « quel rôle veux-tu ? ». Fais raconter le quotidien. Quelques angles d'attaque (en
piocher 2-3, pas tout dérouler) :

- « Raconte-moi une semaine type. Où part ton temps, concrètement ? »
- « Quelles tâches reviennent chaque semaine et que tu fais un peu en pilote automatique ? »
- « Les trois dernières choses que tu aurais aimé ne pas avoir à faire toi-même ? »
- « Qu'est-ce qui te sature, t'agace, ou que tu repousses sans arrêt ? »
- « Quels documents ou messages tu produis encore et encore, avec à chaque fois le même genre de structure ? »
- « Si tu avais un bras droit dès demain matin, tu lui refilerais quoi en premier ? »

Pour un profil métier précis (RH, juridique, commercial…), orienter vers ce domaine : « sur le
volet RH, qu'est-ce qui te prend du temps — les contrats, la lecture de PV, les réponses aux
questions de l'équipe ? ».

## Tour 2 — creuser le vague

Les premières réponses sont souvent trop générales pour cadrer quoi que ce soit. Relancer jusqu'au
concret. Quand tu entends une formule vague, demande l'exemple récent :

| Réponse vague | Relance pour concrétiser |
|---|---|
| « M'aider à gérer mes projets » | « Gérer comment ? Tu penses à les suivre, relancer les gens, préparer des points ? Donne-moi le dernier exemple. » |
| « Trier mes mails » | « Trier pour en faire quoi — prioriser, classer, répondre ? Tu reçois combien par jour, et lesquels te coûtent le plus ? » |
| « Préparer mes réunions » | « Quelle réunion, à quelle fréquence ? Tu pars de quoi (notes, mails, doc) et tu veux quel livrable en sortie ? » |
| « Du support juridique » | « Sur quels actes concrètement — relecture de contrats, lecture de PV, veille ? Le dernier en date ? » |

Le bon signal : pour chaque tâche, tu peux nommer **l'input** (ce qu'on lui donne), **l'action**
(ce qu'elle fait), **le livrable** (ce qui sort) et **la fréquence**. Si l'un manque, relance.

## Tour 3 — reformuler et faire valider

À intervalles réguliers, rejoue ta compréhension en une formulation nette, et laisse corriger :

> « Si je résume : cette persona te décharge du tri de l'inbox et du suivi des projets transverses,
> et elle te produit des brouillons de relance et une synthèse hebdo. C'est bien ça, ou il manque
> quelque chose ? »

La reformulation n'est pas une politesse : c'est l'outil qui fait émerger les oublis (« ah oui, et
aussi… ») et corrige les malentendus avant qu'ils ne se figent dans le `CLAUDE.md`.

## Tour 4 — dériver le périmètre

Quand les tâches sont claires, traduis-les en périmètre, en t'appuyant sur la carte du `CLAUDE.md`
racine. Raisonne à voix haute et propose :

> « Pour suivre tes projets et préparer tes points, elle a besoin de lire `10-Projects/` et
> `20-Areas/gouvernance/`. Pour ses brouillons, elle écrit dans `00-Inbox/_drafts/` et nulle part
> ailleurs. Ça te va, ou il y a d'autres dossiers qu'elle devrait voir ? »

Principe **lire large, écrire étroit** (cf. `persona-design.md`). Ne propose que des dossiers qui
existent ; n'invente pas de zone « au cas où ».

## Savoir s'arrêter

- **Converge** dès que rôle + 2-4 tâches + périmètre sont nets — n'allonge pas pour le principe.
- **Ne sur-cadre pas** : 4 tâches récurrentes suffisent largement pour un shell. Le reste viendra
  à l'usage.
- **Si la personne est déjà précise** dès le départ (elle arrive avec un rôle et des zones clairs),
  saute les tours de creusage : une seule reformulation de validation, puis génère.
- **Si la personne sèche** sur ses tâches, propose à partir d'archétypes courants (Chief of Staff,
  RH, Métier) et de la carte du vault, puis fais réagir — c'est plus facile de corriger une
  proposition que de partir d'une page blanche.

## Exemple : vague → net

**Départ (vague)** : « Je voudrais un assistant qui m'aide au quotidien sur le cabinet. »

**Après découverte (net)** :
- Rôle : *bras droit opérationnel qui me décharge du suivi et de la rédaction courante.*
- Tâches récurrentes : (1) triage de l'inbox du matin → liste priorisée + brouillons de réponse ;
  (2) suivi hebdo des projets transverses → relances à valider ; (3) prépa des points de
  gouvernance → note d'1 page à partir des fiches projet.
- Périmètre : lit `10-Projects/`, `20-Areas/gouvernance/` ; écrit `00-Inbox/_drafts/`.
- Backlog de capacités (pour skill-creator, plus tard) : `triage-inbox`, `relance-projets`,
  `prep-gouvernance`.
