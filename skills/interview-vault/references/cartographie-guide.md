# Guide de cartographie — superset d'Areas & heuristiques d'adaptation

Outillage de l'**adaptativité** du skill. Rien ici n'est profilé « tech / non-tech ». C'est **un seul
superset** et un jeu d'heuristiques : on ne **propose** un élément que s'il **résonne** avec ce que
l'utilisateur a décrit (matière première + réponses). On ne déroule jamais une liste, on ne force
jamais une suggestion, on n'invente rien.

## Comment s'en servir

À la fin de la **Phase 2 (Areas)**, après avoir traité les thèmes spontanés de l'utilisateur,
parcourir mentalement le superset ci-dessous et **ne retenir que les Areas qui font écho** à son
activité (un signal dans `contexte.md`, `themes-actuels.md`, `sources-equipe.md` ou ses réponses).
Les proposer **pour vérification** : « tu n'as pas mentionné {X} — est-ce une responsabilité
continue pour toi, ou non ? ». S'il dit non, on n'insiste pas.

## Superset d'Areas (réservoir, pas une checklist à dérouler)

Responsabilités continues qu'un dirigeant/cadre **pourrait** oublier de nommer. Le libellé final est
en kebab-case et collé à son vocabulaire.

**Pilotage & direction**
- gouvernance / instances (CA, comité de direction, CSE, board)
- relations direction / actionnaires / refinancement
- stratégie (continue — pas le « plan stratégique 2027 » qui, lui, est un Project)
- finance / budget / arbitrages

**Équipe & humain**
- management des équipes / 1:1 / posture managériale
- recrutement (pipeline, fiches de poste, entretiens)
- RH / social / conformité sociale

**Relations externes**
- relations clients clés / partenaires
- communication externe / représentation / marque
- vendors / fournisseurs / contrats

**Technique** (si l'activité l'est)
- architecture / décisions techniques (ADR) / dette technique
- fiabilité / observabilité / incidents / oncall
- delivery / gestion de projet / rituels
- roadmap produit / priorisation
- sécurité / conformité (données sensibles, RGPD)
- veille techno

**Métier / sectoriel** (très dépendant du domaine)
- veille sectorielle / réglementaire
- qualité / certifications / audits
- production / opérations / process métier

> Ces familles ne sont pas exhaustives et ne sont pas des cases à cocher. Un artisan, un avocat, un
> médecin-chef auront des Areas absentes de cette liste : **les capturer telles qu'ils les nomment**.
> Le superset sert à **ne rien oublier d'évident**, pas à plaquer un modèle.

## Heuristique — logique d'organisation des Resources (Phase 3)

Choisir **avec** l'utilisateur, selon volume et usage :

- **Par type** (`methodologies/`, `runbooks/`, `adr/`, `benchmarks/`, `trames/`) — quand le volume est
  modeste et les ressources transverses à plusieurs domaines. Défaut raisonnable pour la plupart.
- **Par domaine** (`reglementation/`, `rh-social/`, `finance/`…) — quand un domaine a un volume
  important et autonome, consulté comme un bloc.
- Toujours prévoir **`references-externes/`** pour les renvois (la source de vérité reste dehors :
  GitLab, Notion entreprise, Drive partagé… → on **référence, on ne copie pas**).

## Heuristique — types frontmatter à proposer (Phase 4 / Étape 4)

Ne lister dans le plan que les types **qui correspondent à des fiches réelles** de l'activité.
Toujours : `project`, `area`, `meeting`. Puis, **selon les signaux** :

| Signal dans les réponses | Type à proposer |
|---|---|
| décisions techniques à tracer, ADR | `adr` |
| prod, incidents, oncall, post-mortems | `incident` |
| agent de point quotidien envisagé | `brief` |
| partenaires / clients / contacts récurrents | `contact` |
| production de texte (mails, contrats, déclarations) | `draft` |
| documents de référence réutilisables | `resource` |
| besoin d'index / cartes de notes | `moc` |

> **Le tableau est un réservoir, pas une liste fermée.** Si l'activité produit une fiche
> **récurrente et réelle** qu'aucun type ci-dessus ne couvre (ex. un pilotage chiffré régulier →
> `reporting` ; un suivi de dossier juridique → `dossier` ; un brief de veille → `veille`), **créer
> un type métier** — en kebab-case, collé au vocabulaire du dirigeant — plutôt que de tordre un type
> approchant. Le `_Meta/Schema.md` accueille n'importe quel type déclaré dans le plan, et rien en aval
> ne le bloque. Trois garde-fous avant d'en créer un :
> 1. **Vraie fiche récurrente, pas un type « au cas où »** — même discipline que pour les Areas : on
>    ne déclare que ce qui correspond à un usage réel et répété.
> 2. **Adossé à une compétence** — un type créé doit être **écrit par au moins une compétence** du
>    plan (sinon il n'a pas de producteur ; c'est la cohérence types ↔ compétences du contrat).
> 3. **Pas de doublon déguisé** — ne pas réinventer sous un autre nom un type existant : un
>    compte-rendu reste `meeting`, un mail reste `draft`, une décision reste `decision`/`adr`.

## Heuristique — dériver les compétences (skills), puis les regrouper en personas (Phase 4)

**Un irritant donne une compétence, pas un rôle.** C'est l'erreur à ne pas commettre : un irritant
chronophage = une **routine à automatiser** (une compétence / *skill*), surtout pas « une persona de
plus ». Les compétences **émergent des Top 5 irritants et des sources**, jamais d'un catalogue.
Méthode : pour chaque irritant, se demander « une compétence qui lit {source} et écrit {fiche} dans
{zone} ferait-elle disparaître cet irritant ? ».

Exemples de dérivation (illustratifs — **ne pas les imposer**) :
- « je compile mon point du matin à la main » + sources Slack/agenda/Notion → compétence
  **brief-du-jour** (lit Slack + agenda + Areas actives → écrit une fiche `brief` dans `00-Inbox/briefs/`).
- « l'info se perd dans Slack » → compétence **capter-décisions** (lit Slack → écrit une fiche `decision`).
- « je relis et reformate chaque contrat / mail » → compétence **rédaction-reformatage** (lit
  l'Area/Project concerné + les trames → écrit un `draft`).
- « je prépare mes 1:1 à la dernière minute » → compétence **préparer-les-1:1** (lit l'Area management →
  écrit une fiche de prép).

Pour chaque compétence : noter **ce qu'elle lit** et **où elle écrit** (zone + type de fiche).

### Puis : regrouper en personas (l'étape qui dérive les rôles)

Une **persona** (= un assistant spécialisé) n'est PAS dérivée d'un irritant. Elle **émerge d'un
groupe de compétences qui partagent une même lentille** : mêmes zones de lecture/écriture, même
posture, même voix. La règle de décision :

- **Par défaut, toutes les compétences se rangent sous le Chief of Staff** — la persona généraliste
  que `kickstart-vault` pose d'office. Trois compétences de capture/synthèse (brief, capter-décisions,
  compte-rendu de réunion) = **un seul** Chief of Staff qui les porte, pas trois personas.
- **On n'isole une persona dédiée que si une compétence réclame des zones, une voix ou des garde-fous
  franchement distincts.** Signal le plus fiable : la **gouvernance**. Une compétence qui lit des
  sources sensibles 🔒 (finance, RH, contrats) avec ses propres garde-fous, ou qui écrit avec une voix
  particulière (commerciale, juridique), justifie sa propre lentille. Sinon → Chief of Staff.

Rien de plus à ce stade : les compétences se construisent ensuite avec `vault-skill-creator`, et une
nouvelle persona ne se crée (`kickstart-persona`) **que** quand le regroupement l'exige.

## Heuristique — gouvernance & isolation (Étape 4)

Ne jamais sauter cette section, même si l'utilisateur n'en parle pas. Scanner les signaux de
sensibilité dans la matière première et le mapping :
- sources **RH**, **contrats**, **finances non publiques**, **données clients**, **org chart** →
  marquer 🔒, **renvoi jamais copie**, interdits aux agents sans règle explicite.
- périmètre clair (ce que le vault couvre **et exclut**) — utile si l'utilisateur garde un périmètre
  perso ou un autre vault séparé.
- isolation technique selon enjeu (vault local, pas de dépôt public, pas de cloud non maîtrisé).

Formuler la politique d'accès comme **une règle**, jamais comme une liste d'agents nommés (la liste
se périme ; la règle tient).
