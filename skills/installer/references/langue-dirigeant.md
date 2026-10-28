# Langue du dirigeant

Le dirigeant n'est pas forcément développeur. Le curseur Vocabulaire du profil de ton du plan dit
jusqu'où nommer la structure interne ; sans profil, aucune structure interne n'est nommée.

## Toujours remplacé, quel que soit le profil

| À remplacer | Dire plutôt |
|---|---|
| scaffold, scaffolder | installer, monter, poser |
| bundle | ensemble prêt à l'emploi |
| alias | raccourci de lancement |
| quick win | gain rapide |
| input | matière, informations |
| deal | affaire |
| mapping | correspondance |
| shell | fiche vide structurée |
| lazy-pull | au fil des besoins |
| generate-don't-write | on pose le cadre, pas le contenu |

- Les termes internes du skill (shell, bundle, generate-don't-write, idempotent, skill caché, asset
  figé) servent au modèle et ne sont pas répétés au dirigeant. Dérives constatées à l'usage : « je
  copie le bundle figé, y compris le skill caché » ; « l'alias `cos`, chemin absolu, idempotent ».
- Pas de jargon dans le nom d'un fichier livré : `compte-rendu-installation.md`, pas
  `scaffold-report.md`.

## Calibré sur le curseur Vocabulaire

- Le curseur règle la quantité de structure interne nommée : PARA, `_Meta`, Schema, frontmatter,
  slug, chemins de fichiers, « couche ».
- Profil « métier sans jargon » (défaut) : n'en nommer aucune.
- Profil « termes techniques OK » : les nommer est permis.
- Dans les deux cas, un terme de structure conservé est expliqué une fois puis réutilisé :
  `frontmatter`, l'en-tête d'une note ; `wikilink`, un lien `[[…]]` ; `persona`, un assistant
  spécialisé.

## Narrer le résultat, pas l'étape technique

Le dirigeant n'a pas besoin du commentaire du chantier. Exemples au profil « métier sans jargon » :

- Avant : « Maintenant la couche `_Meta`, le contrat qui tient le vault. Je génère le Schema. »
  Après : « Je pose les règles qui garderont ton espace cohérent dans le temps. »
- Avant : « Squelette PARA posé (generate-don't-write : shells structurés) : 6 Areas en
  `{slug}/{slug}.md`. »
  Après : « Ton espace est en place : tes 6 domaines de responsabilité, prêts à se remplir au fil
  de l'usage. »
- Avant : « Je pose l'alias terminal `cos` (chemin absolu, idempotent). »
  Après : « J'ajoute un raccourci : tu lanceras ton assistant en tapant `cos`. »
