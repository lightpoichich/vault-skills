# Archiver une area — la responsabilité disparaît

Le mouvement PARA canonique : une area qui meurt part en `40-Archive/` (on déplace, on ne
supprime pas), et ce qui reste utile est promu en `30-Resources/`. Même discipline que
`restructurer.md` : plan-puis-exécute, validation, filet git.

## 1. Pré-checks — AVANT le plan, et bloquants

Dans cet ordre, **avant de rien déplacer** :

1. **Projets actifs rattachés.** `Grep` le frontmatter `area: "[[{slug}]]"` sur `10-Projects/`.
   Tout projet `status: active` → **bloquant** : demander où le réaffecter (proposer les areas
   existantes — un projet vivant ne pointe pas vers une archive). Le dirigeant peut décider que
   le projet s'archive aussi (alors il se traite : `status: done`, déplacement vers
   `40-Archive/`). Tant que ce n'est pas tranché, on n'archive pas l'area.
2. **Contenu encore utile.** Parcourir le dossier de l'area : une note qui sert au-delà de la
   responsabilité morte (trame, référentiel, benchmark) → **proposer sa promotion** en
   `30-Resources/` (frontmatter `type: resource`, wikilinks repris) plutôt que l'enterrer.
3. **Personas.** Repérer chaque `_personas/*/CLAUDE.md` qui déclare une zone sur cette area. Le
   retrait fait partie du plan. **Si une persona se retrouve sans aucune zone** → alerter : la
   persona n'a plus de raison d'être — c'est au dirigeant de décider (la retirer, la repointer),
   pas au skill.

## 2. Le plan
Réaffectations décidées, promotions vers Resources, déplacement `20-Areas/{slug}/` →
`40-Archive/{slug}/`, retraits de zones des personas, devenir des wikilinks entrants. Validation,
puis commit git proposé.

## 3. Exécution
- Réaffecter les projets / promouvoir les notes décidées (avant le move, pour que les chemins
  restent vrais).
- Déplacer le dossier **entier** vers `40-Archive/{slug}/`.
- Marquer la fiche : le Schema ne prévoit pas de `status` pour `area` → une ligne « Archivée le
  {date} — {raison en quelques mots} » en tête de corps, frontmatter inchangé (ne pas inventer
  de champ hors Schema).
- Retirer la zone des personas concernées (changement listé au plan).
- **Ne pas réécrire les wikilinks entrants** `[[{slug}]]` : ils résolvent par nom, l'historique
  (briefs passés, meetings) continue de pointer vers la fiche archivée — c'est voulu.

## 4. Rapport
Actions faites, projets réaffectés, notes promues, personas modifiées, alerte « persona sans
zone » le cas échéant.
