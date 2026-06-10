# Format de la fiche brief

Le brief est une fiche du vault de type `brief`. Forme **stable** (identique pour tous les
dirigeants) ; seul le **contenu** des sections varie selon les sources résolues.

## Gabarit

```markdown
---
type: brief
date: {YYYY-MM-DD}
---

# Brief — {jour} {date}

## Priorités
- {1 à 5 items : ce qui compte aujourd'hui, tiré du vault et des deadlines proches}
- {chaque projet/area cité en [[wikilink]]}

## Alertes
- {ce qui demande une réaction aujourd'hui : deadline imminente, action item d'une réunion de la
   veille, message clé en attente. Vide si rien — ne pas inventer.}

## Agenda
- {événements du jour, du slot agenda. Section OMISE si aucune source agenda déclarée/joignable.}

## Todos
- [ ] {tâches ouvertes du jour, du slot todos. Section OMISE si aucune source todos.}

## À valider
- {livrables en attente dans `00-Inbox/_drafts/` : `statut: en-attente` (ta validation) ou `validé`
   (prêt à envoyer). Chacun en [[wikilink]] vers son draft. Section OMISE si `_drafts/` est vide.}

---
> **Sources à brancher** : {liste des slots non déclarés ou injoignables — ex. « meetings veille
> (Granola à brancher), agenda (aucune source) ». Omettre la ligne si tout est branché.}
```

## Règles de remplissage

- **Generate-don't-write.** Ne remplir une section qu'avec des données **réelles** issues des
  sources. Pas de placeholder, pas d'item inventé pour « faire joli ». Une section sans matière est
  **omise** (Agenda/Todos) ou laissée vide avec une mention courte (Alertes : « rien d'urgent »).
- **Priorités a toujours du contenu** : c'est le slot vault, toujours présent. S'il est vide, c'est
  le signal qu'aucun projet n'est `active` — le dire franchement plutôt que broder.
- **Actionnable, pas narratif.** Des items courts, à la deuxième personne implicite. Pas de paragraphe
  de synthèse, pas de « voici ton brief… ». Le dirigeant scanne en 20 secondes.
- **Alertes = ce qui brûle**, pas un fourre-tout. Si un item peut attendre, il va en Priorités ou
  Todos, pas en Alertes.
- **Réunions de la veille** : on en tire les **engagements pris / décisions / relances**, jamais le
  compte rendu intégral (ça, c'est le rôle de la fiche meeting, pas du brief).
- **Le pied « Sources à brancher »** rend la dégradation **visible** : le dirigeant comprend qu'il
  manque de la matière et sait quoi connecter. C'est le moteur d'amélioration du système.
- **« À valider » ferme la boucle des livrables** : c'est le seul endroit où le dirigeant voit ce qui
  attend sa main dans `_drafts/`. Le brief **liste**, il ne valide ni n'envoie rien. Section omise si
  le sas est vide — pas de section vide « pour la forme ».

## Ton

**Contrainte de format** (vaut pour tous, quel que soit le ton du vault) : le brief est un outil de
pilotage, pas un rapport — items courts, actionnables, zéro formule de politesse, zéro méta-commentaire
sur le brief lui-même. Le **registre et le tutoiement/vouvoiement** suivent, eux, le ton hérité du
`CLAUDE.md` racine du vault (section *Ton*) ; à défaut : sobre, français, tutoiement.
