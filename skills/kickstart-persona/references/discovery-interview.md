# Mener la découverte : guide d'entretien

Matière pour creuser (questions, relances, reformulation) sans transformer l'échange en
interrogatoire. Les questions ci-dessous sont des exemples de formulation à adapter, pas un
questionnaire à dérouler. Adapte le registre aux mots de ton interlocuteur. Les quatre tours mènent
au trio de convergence fixé dans le SKILL.md : rôle en une phrase, deux à quatre tâches
récurrentes, périmètre lecture/écriture.

## Tour 1 : partir du réel, pas du rôle

Ne pas demander « quel rôle veux-tu ? ». Faire raconter le quotidien, en piochant deux ou trois
angles :

- « Raconte-moi une semaine type. Où part ton temps, concrètement ? »
- « Quelles tâches reviennent chaque semaine et que tu fais un peu en pilote automatique ? »
- « Les trois dernières choses que tu aurais aimé ne pas avoir à faire toi-même ? »
- « Qu'est-ce qui te sature, t'agace, ou que tu repousses sans arrêt ? »
- « Quels documents ou messages tu produis encore et encore, avec le même genre de structure ? »
- « Si tu avais un bras droit dès demain matin, tu lui confierais quoi en premier ? »

Pour un profil métier précis (RH, juridique, commercial), orienter vers ce domaine : « sur le volet
RH, qu'est-ce qui te prend du temps : les contrats, la lecture de PV, les réponses aux questions de
l'équipe ? ».

## Tour 2 : creuser le vague

Les premières réponses sont souvent trop générales pour cadrer. Relancer jusqu'au concret en
demandant l'exemple récent :

| Réponse vague | Relance pour concrétiser |
|---|---|
| « M'aider à gérer mes projets » | « Gérer comment ? Les suivre, relancer les gens, préparer des points ? Donne-moi le dernier exemple. » |
| « Trier mes mails » | « Trier pour en faire quoi : prioriser, classer, répondre ? Tu en reçois combien par jour, et lesquels te coûtent le plus ? » |
| « Préparer mes réunions » | « Quelle réunion, à quelle fréquence ? Tu pars de quoi (notes, mails, doc) et tu veux quel livrable en sortie ? » |
| « Du support juridique » | « Sur quels actes : relecture de contrats, lecture de PV, veille ? Le dernier en date ? » |

Le bon signal : pour chaque tâche, on peut nommer l'entrée (ce qu'on lui donne), l'action, le
livrable (ce qui sort) et la fréquence. Si l'un manque, relancer.

## Tour 3 : reformuler et faire valider

À intervalles réguliers, rejouer sa compréhension en une formulation nette et laisser corriger :

> « Si je résume : cette persona te décharge du tri de l'inbox et du suivi des projets transverses,
> et elle te produit des brouillons de relance et une synthèse hebdo. C'est bien ça, ou il manque
> quelque chose ? »

La reformulation fait émerger les oublis (« ah oui, et aussi… ») et corrige les malentendus avant
qu'ils ne se figent dans le `CLAUDE.md`.

## Tour 4 : dériver le périmètre

Quand les tâches sont claires, les traduire en périmètre à partir de la carte du `CLAUDE.md`
racine. Raisonner à voix haute et proposer :

> « Pour suivre tes projets et préparer tes points, elle a besoin de lire `10-Projects/` et
> `20-Areas/gouvernance/`. Pour ses brouillons, elle écrit dans `00-Inbox/_drafts/` et nulle part
> ailleurs. Ça te va, ou il y a d'autres dossiers qu'elle devrait voir ? »

Lire large, écrire étroit (voir `persona-design.md`). Ne proposer que des dossiers qui existent ;
pas de zone « au cas où ».

## Savoir s'arrêter

- **Converger** dès que rôle, tâches et périmètre sont nets ; ne pas allonger pour le principe.
- **Ne pas sur-cadrer** : quatre tâches récurrentes suffisent pour un shell. Le reste vient à l'usage.
- **Personne déjà précise** dès le départ (rôle et zones clairs) : sauter les tours de creusage,
  une reformulation de validation, puis générer.
- **Personne qui sèche** sur ses tâches : relancer d'abord avec les angles du Tour 1 et la carte du
  vault. En dernier recours seulement, proposer à partir d'archétypes courants (Chief of Staff, RH,
  Métier) et faire réagir : corriger une proposition est plus facile que partir d'une page blanche.

## Exemple : de vague à net

**Départ (vague)** : « Je voudrais un assistant qui m'aide au quotidien sur le cabinet. »

**Après découverte (net)** :
- Rôle : bras droit opérationnel qui me décharge du suivi et de la rédaction courante.
- Tâches récurrentes : (1) triage de l'inbox du matin, sortie une liste priorisée et des brouillons
  de réponse ; (2) suivi hebdo des projets transverses, sortie des relances à valider ; (3)
  préparation des points de gouvernance, sortie une note d'une page à partir des fiches projet.
- Périmètre : lit `10-Projects/`, `20-Areas/gouvernance/` ; écrit `00-Inbox/_drafts/`.
- Backlog de capacités (pour `vault-skill-creator`, plus tard) : `triage-inbox`, `relance-projets`,
  `prep-gouvernance`.
