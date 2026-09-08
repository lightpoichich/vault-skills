# Guide de cartographie : superset d'Areas et heuristiques d'adaptation

Réservoirs et heuristiques, pas de questionnaire : on ne propose un élément que s'il fait écho à
ce que le dirigeant a décrit (matière première et réponses), on ne déroule jamais une liste, on
n'invente rien.

## Comment s'en servir

À la fin de la Phase 2 (Areas), après les thèmes spontanés du dirigeant, parcourir le superset
ci-dessous et ne retenir que les Areas qui font écho à son activité (un signal dans `contexte.md`,
`themes-actuels.md`, `sources-equipe.md` ou ses réponses). Les proposer pour vérification :
« tu n'as pas mentionné {X} ; est-ce une responsabilité continue pour toi ? ». S'il dit non, ne
pas insister.

## Superset d'Areas

Responsabilités continues qu'un dirigeant ou un cadre pourrait oublier de nommer. Le libellé final
est en kebab-case et collé à son vocabulaire.

**Pilotage et direction**
- gouvernance, instances (CA, comité de direction, CSE, board)
- relations direction, actionnaires, refinancement
- stratégie
- finance, budget, arbitrages

**Équipe et humain**
- management des équipes, 1:1, posture managériale
- recrutement (pipeline, fiches de poste, entretiens)
- RH, social, conformité sociale

**Relations externes**
- relations clients clés, partenaires
- communication externe, représentation, marque
- fournisseurs, contrats

**Technique** (si l'activité l'est)
- architecture, décisions techniques (ADR), dette technique
- fiabilité, observabilité, incidents, oncall
- delivery, gestion de projet, rituels
- roadmap produit, priorisation
- sécurité, conformité (données sensibles, RGPD)
- veille techno

**Métier et sectoriel** (dépend du domaine)
- veille sectorielle, réglementaire
- qualité, certifications, audits
- production, opérations, process métier

Ces familles ne sont pas exhaustives. Un artisan, un avocat, un médecin-chef auront des Areas
absentes de cette liste : les capturer telles qu'ils les nomment.

## Logique d'organisation des Resources (Phase 3)

Choisir avec le dirigeant, selon volume et usage :

- **Par type** (`methodologies/`, `runbooks/`, `adr/`, `benchmarks/`, `trames/`) quand le volume est
  modeste et les ressources transverses à plusieurs domaines. Défaut raisonnable.
- **Par domaine** (`reglementation/`, `rh-social/`, `finance/`) quand un domaine a un volume
  important et autonome, consulté comme un bloc.
- **`references-externes/`** dans tous les cas, pour les renvois : la source de vérité reste dehors
  (GitLab, Notion d'entreprise, Drive partagé), on référence sans copier.

## Types de fiches à proposer (Phase 4, Étape 4)

Ne lister dans le plan que les types qui correspondent à des fiches réelles de l'activité. Toujours
`project`, `area`, `meeting`. Puis, selon les signaux :

| Signal dans les réponses | Type à proposer |
|---|---|
| décisions techniques à tracer, ADR | `adr` |
| prod, incidents, oncall, post-mortems | `incident` |
| agent de point quotidien envisagé | `brief` |
| partenaires, clients, contacts récurrents | `contact` |
| production de texte (mails, contrats, déclarations) | `draft` |
| documents de référence réutilisables | `resource` |
| besoin d'index, cartes de notes | `moc` |

Le tableau n'est pas une liste fermée. Si l'activité produit une fiche récurrente qu'aucun type ne
couvre (un pilotage chiffré régulier donne `reporting`, un suivi de dossier juridique donne
`dossier`, un brief de veille donne `veille`), créer un type métier collé au vocabulaire du
dirigeant plutôt que tordre un type approchant. `_Meta/Schema.md` accueille tout type déclaré dans
le plan. Trois conditions avant d'en créer un :
1. **Fiche récurrente réelle**, pas un type « au cas où ».
2. **Adossé à une compétence** : un type créé est écrit par au moins une compétence du plan, sinon
   il n'a pas de producteur.
3. **Pas de doublon déguisé** : un compte-rendu reste `meeting`, un mail reste `draft`, une décision
   reste `decision` ou `adr`.

## Réservoir de cas d'usage (Étape 3)

Pour relancer un dirigeant qui sèche sur ses irritants : proposer deux ou trois cas qui font écho à
son activité, sans profiler (« tu es opérateur donc… » est proscrit). Postes où un dirigeant ou
une équipe récupère souvent du temps :

- **Service client, demandes entrantes** : triage et réponses types récurrentes.
- **Planning, production, ordonnancement** : replanification régulière sous contraintes.
- **Compta, trésorerie** : reporting mensuel répétitif, rapprochements.
- **Point quotidien** : compiler agenda, messages et en-cours à la main chaque matin.
- **Observabilité, suivi d'activité** : surveiller des tableaux de bord, trier ce qui sort.
- **Rédaction, reformatage** : mails, contrats, déclarations administratives récurrents.
- **Amont des offres** : analyser le contexte, reformuler les objectifs, structurer.
- **Base de connaissance** : retrouver la bonne information au lieu de la reconstruire.
- **Relances, suivi commercial** : détecter les dossiers sans nouvelle, tenir le CRM à jour.
- **Préparation de réunions, comptes-rendus** : board, comité, 1:1.
- **RH, social** : préparation d'entretiens, suivi, conformité.

Chaque cas retenu reçoit le même signal d'impact qu'un irritant spontané (fréquence, temps
unitaire, répétabilité, projetable à l'équipe).

## Dériver les compétences (Phase 4)

Pour chaque irritant, se demander : « une compétence qui lit {source} et écrit {fiche} dans {zone}
ferait-elle disparaître cet irritant ? ». Exemples de dérivation, à ne pas imposer :

- « je compile mon point du matin à la main », sources Slack, agenda, Notion : compétence
  `brief-du-jour`, lit Slack, l'agenda et les Areas actives, écrit une fiche `brief` dans
  `00-Inbox/briefs/`.
- « l'information se perd dans Slack » : compétence `capter-decisions`, lit Slack, écrit une fiche
  `decision`.
- « je relis et reformate chaque contrat ou mail » : compétence `redaction-reformatage`, lit l'Area
  ou le Project concerné et les trames, écrit un `draft`.
- « je prépare mes 1:1 à la dernière minute » : compétence `preparer-les-1-1`, lit l'Area
  management, écrit une fiche de préparation.

## Gouvernance et isolation (Étape 4)

Ne pas sauter cette section, même si le dirigeant n'en parle pas. Scanner les signaux de
sensibilité dans la matière première et la correspondance entre sources et zones :
- sources RH, contrats, finances non publiques, données clients, organigramme : marquer 🔒, renvoi
  jamais copie, interdits aux agents sans règle explicite ;
- périmètre clair (ce que le vault couvre et exclut), utile si le dirigeant garde un périmètre
  perso ou un autre vault séparé ;
- isolation technique selon l'enjeu (vault local, pas de dépôt public, pas de cloud non maîtrisé).

Formuler la politique d'accès comme une règle, jamais comme une liste d'agents nommés : la liste se
périme, la règle tient.
