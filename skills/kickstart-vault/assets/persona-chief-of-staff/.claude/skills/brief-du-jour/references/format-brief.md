# Format de la fiche brief

Le brief est une fiche du vault de type `brief`. La forme est stable ; seul le contenu des sections
varie selon les sources résolues.

## Gabarit

```markdown
---
type: brief
date: {YYYY-MM-DD}
status: done
---

# Brief du {jour} {date}

## Priorités
- {1 à 5 items : ce qui compte aujourd'hui, tiré du vault et des deadlines proches ; chaque projet
  ou area en [[wikilink]]}

## Alertes
- {ce qui demande une réaction aujourd'hui : deadline imminente, action d'une réunion de la veille,
  message clé en attente ; « rien d'urgent » si rien}

## Agenda
- {événements du jour ; section omise sans source agenda déclarée et joignable}

## Todos
- [ ] {tâches ouvertes du jour ; section omise sans source todos}

## À valider
- {livrables en attente dans `00-Inbox/_drafts/` : `statut: en-attente` (à valider) ou `validé`
  (prêt à envoyer), chacun en [[wikilink]] vers son draft ; section omise si `_drafts/` est vide}

---
> Sources à brancher : {slots non déclarés ou injoignables, par exemple « meetings veille (connecteur
> à brancher), agenda (aucune source) » ; ligne omise si tout est branché}
```

## Règles de remplissage

- **Données réelles seulement** : pas de placeholder ni d'item inventé. Une section sans matière est
  omise (Agenda, Todos, À valider) ou porte une mention courte (Alertes : « rien d'urgent »).
- **Priorités a toujours du contenu** : c'est le slot vault. Si aucun projet n'est `active`, le dire
  tel quel.
- **Items courts et actionnables**, à la deuxième personne implicite. Pas de paragraphe de synthèse,
  pas de formule d'ouverture ni de méta-commentaire sur le brief : il se lit d'un coup d'œil.
- **Alertes** : ce qui demande une réaction aujourd'hui. Un item qui peut attendre va en Priorités ou
  Todos. Un sujet vit dans une seule section.
- **Réunions de la veille** : en tirer les engagements pris, décisions et relances, pas le compte
  rendu, qui appartient à la fiche meeting.
- **Pied « Sources à brancher »** : rend la dégradation visible et dit au dirigeant quoi connecter.
- **À valider** : le seul endroit où le dirigeant voit ce qui attend dans `_drafts/`. Le brief liste ;
  il ne valide ni n'envoie.
- **Registre** : celui du `CLAUDE.md` racine du vault (section Ton), tutoiement ou vouvoiement
  compris ; à défaut, sobre, français, tutoiement.
