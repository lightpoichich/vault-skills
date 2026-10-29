# Expliquer une mise à niveau au dirigeant

La mise à niveau touche des fichiers que le dirigeant n'a pas écrits et des automatismes qu'il n'a
pas vus arriver. Une phrase comme « rotation des journaux activée » ou « migration 5.3.0 appliquée »
ne lui dit rien : ce guide dit quoi expliquer, dans quel ordre, et donne un texte de départ par
changement. Les règles de `langue-dirigeant.md` s'appliquent, avec le curseur Vocabulaire lu dans le
`CLAUDE.md` racine du vault (section du ton) ; sans indication, profil « métier sans jargon ».

## Principes

- **Jamais de sortie brute** : ni clé d'unité, ni cas du script (« remplaçable », « fusion »,
  « inconnu »), ni identifiant de migration, ni nom de script, ni JSON. Le chemin d'un fichier
  seulement si le profil l'autorise, et après avoir dit ce qu'est ce fichier.
- **Ouvrir par le pourquoi**, en deux phrases : le plugin a évolué depuis l'installation de l'espace ;
  certaines évolutions concernent des fichiers posés dans le vault ; rien ne bouge sans accord, et
  tout est sauvegardé avant.
- **Pour chaque changement, quatre temps**, en phrases courtes :
  1. ce que c'est : la fonction, décrite par son effet concret, jamais par son nom technique ;
  2. ce que ça change au quotidien, avec un exemple tiré du vault quand il existe (une fiche lourde
     citée par son nom, un réglage déjà personnalisé) ;
  3. ce qui ne change pas, et la garantie : rien de perdu, sauvegarde, comment revenir en arrière ou
     couper ;
  4. quand il le verra pour la première fois.
- **Regrouper par thème** au-delà de trois changements (automatismes, règles du vault, nettoyage),
  puis **une seule demande d'accord** à la fin, qui rappelle qu'un point peut être refusé.
- **Pendant l'application**, narrer le résultat, pas l'étape (`langue-dirigeant.md`, dernière
  section).
- **Au compte rendu**, dire où voir chaque changement (une fiche à ouvrir, une commande à essayer) et
  ce qui se passera de soi-même aux prochaines sessions.
- **Rester bref** : le dirigeant peut demander plus. Les détails techniques (budgets, noms de
  réglages) viennent seulement sur demande ou au profil « termes techniques OK ».

## Première mise à niveau d'un vault installé avant la 5.2.0

Le vault n'a pas de fiche d'installation : l'utilisateur a reçu des automatismes au fil des mises à
jour du plugin sans qu'on les lui présente. Avant le détail des changements, faire un tour court de
ce que le plugin fait désormais seul, une phrase chacun :

- au démarrage, un bilan rapide de l'espace (notes à trier qui traînent, fiches trop lourdes,
  mémoire de Claude trop chargée, contrôle mensuel à faire) ;
- à chaque note écrite, les dates de création et de modification tenues à jour ;
- en fin de session longue, la mise à jour des fiches avec ce qui a été décidé, lancée par Claude
  lui-même ;
- à cette occasion, l'allègement des fiches trop lourdes et l'entretien de la mémoire de Claude ;
- un rappel du contrôle mensuel de l'espace, et un rappel quand une nouvelle version apporte des
  changements comme ceux-ci.

Puis présenter la fiche d'installation : « Je crée aussi une fiche qui garde la trace de ce que le
plugin a posé dans ton espace. Aux prochaines versions, elle permettra de distinguer ce que tu as
personnalisé de ce qui peut être mis à jour sans te déranger. »

## Par changement

### Réglages des automatismes ajoutés (`_Meta/hooks.conf`, plan : « ajouté »)

- **Ce que c'est** : le fichier où se règlent les automatismes du plugin (à quel moment Claude
  propose de mettre les fiches à jour, à partir de quel poids une fiche est jugée lourde, ce qui est
  exclu des contrôles). Sans lui, des valeurs par défaut s'appliquent et l'allègement des fiches
  reste éteint.
- **Ce que ça change** : l'allègement automatique des fiches s'allume. Le dire ainsi : « Une fiche de
  domaine qui dépasse une vingtaine de Ko (une trentaine pour un projet) se relit en entier à chaque
  fois que Claude l'ouvre, ce qui ralentit et encombre son attention. Quand Claude met à jour une
  fiche trop lourde, les entrées les plus anciennes de sa section Journal partent, mot pour mot, dans
  un fichier d'archive par trimestre, rangé à côté de la fiche. La fiche garde où on en est, ses cinq
  derniers événements et un lien vers chaque archive. » Citer une fiche lourde du vault si le bilan de
  démarrage en signale une.
- **Garanties** : rien n'est résumé ni supprimé ; un contrôle vérifie, avant d'écrire, que chaque
  ligne se retrouve à l'identique ; une copie est gardée hors de l'espace. Seules les fiches qui ont
  une section Journal sont concernées ; les autres sont signalées, jamais modifiées. L'allègement se
  coupe sur simple demande.
- **Première fois** : à la prochaine mise à jour de fin de session qui touche une fiche trop lourde.
- **Refus** : si le dirigeant ne veut pas de ce fichier, `accept` le note comme refusé et il ne sera
  plus proposé.

### Réglages des automatismes remplacés (`_Meta/hooks.conf`, plan : « remplacé »)

Le fichier n'a jamais été modifié : la nouvelle version documente de nouveaux réglages. Nommer en
une phrase ce qu'apporte la différence (lire l'écart entre l'ancien et le nouveau gabarit), sans
lister les clés.

### Noms des commandes mis à jour (migration `5.0.0-noms-skills`)

« Les commandes du plugin ont été regroupées : dix sont devenues six. Tes phrases habituelles
marchent toujours. Je remplace seulement les anciens noms cités dans tes consignes et tes outils,
pour que Claude ne cherche pas une commande qui n'existe plus. Tes fiches gardent leur historique
tel quel. » La correspondance des noms seulement sur demande.

### Contrôles en double retirés (migration `5.3.0-hooks-locaux`)

« À l'installation de ton espace, deux contrôles automatiques, le bilan au démarrage et la tenue des
dates des notes, ont été copiés dans le vault. Le plugin les fournit lui-même depuis : dans une
session ouverte à la racine de l'espace, ils tournaient deux fois. Je retire les copies. Les
contrôles continuent, une seule fois, et désormais aussi depuis tes assistants. Les autres réglages
de Claude pour cet espace ne bougent pas, et les fichiers retirés sont sauvegardés. »

### Passages de règles à revoir ensemble (blocs `carte`, `regles`, `conventions`)

- **Ce que c'est** : trois passages des fichiers de règles viennent du plugin. Dans les consignes
  principales de l'espace : la carte (où se range quoi) et les règles de travail (ce que Claude fait
  de lui-même). Dans le fichier des types de fiches : les conventions d'écriture. Le reste de ces
  fichiers appartient au dirigeant.
- **Balises absentes** (vault installé avant ce mécanisme) : « Je ne sais pas encore quelle partie
  de ce fichier vient du plugin. Je te propose de poser deux repères invisibles autour du passage
  concerné : les prochaines versions mettront à jour ce passage seul, sans toucher au reste. »
- **Fusion** : montrer en clair ce que le plugin apporte et ce que le dirigeant avait ajouté, puis la
  version qui garde les deux. Nommer l'apport par son effet. Exemple pour les conventions : « Une
  fiche sépare désormais où on en est, en haut, de ce qui s'est passé, dans une section Journal où
  chaque événement est daté et ajouté en tête. C'est ce qui permet l'allègement sans rien perdre. »
- **Garder sa version** est un choix valable : la noter acceptée, le signal cesse jusqu'au prochain
  changement du plugin.

### Fichier remplacé ou ajouté, cas général

Pour une unité future sans entrée ici : lire l'écart entre le fichier du vault et le gabarit,
nommer l'apport par son effet en une phrase, dire si le dirigeant l'avait modifié. Puis ajouter son
entrée à ce guide dans la version du plugin qui l'introduit.

## Entretien du guide

Toute nouvelle unité gérée, tout nouvel effet signalé par le script et toute nouvelle migration
reçoit ici son entrée, dans la même version du plugin.
