# Gabarit du compte-rendu d'installation

Fichier : `00-Inbox/compte-rendu-installation.md`, `type: note`. Écrit dans la langue du dirigeant
(`references/langue-dirigeant.md`) : c'est lui qui le lit. Remplacer chaque `{…}` par la valeur
réelle ; retirer une section sans matière. Les encarts sont ajoutés au `~/.claude/CLAUDE.md` si le dirigeant
l'a accepté (étape 13 de `references/structure.md`), sinon ils restent à coller.

````markdown
---
type: note
tags: [installation]
---

# Ton espace est en place

## Ce qui a été posé
- {Arbre créé : domaines, projets, ressources, dans les mots du dirigeant.}
- L'assistant Chief of Staff, lancé par le raccourci `cos`.
- La note `_Meta/derivation.md` : pourquoi ton espace est rangé ainsi. À ouvrir le jour où tu te le
  demandes, ou avant de changer la structure.

## Généré par défaut, à valider
- {Chaque élément posé sans information au plan : gouvernance synthétisée, ton par défaut, règles de
  fiches par défaut, lignes restées en attente dans `derivation.md`, registre des sources réduit à
  la ligne vault.}

## Points laissés « à creuser » par le plan
- {Points ouverts du plan, dont un éventuel domaine qui ressemble à un projet.}

## Prochaines étapes
- Ne pas remplir les fiches à la main : le contenu entre au fil des besoins.
- Compléter un projet quand il avance : compétence `structurer` (informations manquantes,
  contexte réel rattaché).
- Faire évoluer un domaine (naître, compléter, renommer, scinder, archiver) : compétence
  `structurer`.
- Donner ses compétences au Chief of Staff avec `assistants`, en partant des compétences
  listées au plan et des irritants prioritaires. Une compétence s'ajoute à un assistant existant ; on
  ne crée pas un assistant par compétence.
- Créer un nouvel assistant (`assistants`) seulement si une compétence réclame ses propres
  zones, sa propre voix ou ses propres garde-fous.
- Les documents de référence repérés à l'interview sont listés, avec leur emplacement, dans les
  `_index.md` de `30-Resources/`. Les faire entrer un par un, au moment du besoin, avec
  `ranger`.

## Ton assistant Chief of Staff
- Recharger le terminal (`source ~/.zshrc`, ou un nouvel onglet), taper `cos`, puis demander
  « fais-moi le brief du jour ». Le premier brief sort sur le seul contenu de l'espace, sans
  connecteur.
- `_personas/cos/` est un exemple à dupliquer : son identité (`CLAUDE.md`), son dossier de
  compétences (`.claude/skills/brief-du-jour/`) et sa liste de compétences à construire
  (`capacites-a-construire.md`).
- {Si l'approbation des imports n'a pas pu être posée : à la première session de `cos`, répondre
  « Yes, allow external imports ».}

## Écritures hors de ton espace
- Le raccourci `cos` a été ajouté à `{~/.zshrc | ~/.bashrc}`.
- {Si posée : l'autorisation de lire les règles de l'espace depuis le dossier de l'assistant a été
  inscrite dans `~/.claude.json`.}
- Rien d'autre n'a été modifié hors de l'espace.

## Garde-fous automatiques
Un bilan de santé au démarrage, un garde-fou à l'écriture des notes, un rappel de mise à jour en fin
de session : ils sont livrés par le plugin, tu n'as rien à lancer. Les messages « Santé du vault… »
viennent de là.

## Dans `~/.claude/CLAUDE.md`
Ce fichier est chargé dans toutes tes sessions, contrairement au `CLAUDE.md` de l'espace, chargé
seulement sous l'espace. Deux encarts, {ajoutés avec ton accord | à coller toi-même}.

Contexte personnel (rôle, enjeux, identité) :
```
{Encart tiré de matiere-premiere/contexte.md : rôle, charge, enjeux. Section retirée si le fichier
manque.}
```

Travailler depuis un dossier hors de l'espace :
```
Le vault (ta mémoire) est à {VAULT_ABS}. Tu travailles souvent dans des dossiers de travail hors
vault. Au démarrage dans un tel dossier :
1. cherche dans {VAULT_ABS}/10-Projects/ une fiche dont `repo` = le remote origin de ce dépôt, ou
   dont `dossier-travail` contient ce dossier ; si trouvée, charge-la comme contexte ;
2. sinon, si on fait clairement du travail projet, propose de lier (projet existant, ou
   `structurer`) ;
3. trace décisions et avancées dans la fiche ; pas de copie des livrables (renvoi, jamais copie) ;
4. `sync-vault` en fin de session (depuis un dossier de travail, la fiche projet seule ; le hook Stop
   du plugin le rappelle quand la session a assez de matière) ; lancé depuis le vault, il traite le
   reste ;
5. hors vault, utilise toujours le chemin absolu ci-dessus pour lire et écrire le vault.
```
````

La phrase « Le vault (ta mémoire) est à {VAULT_ABS} » reste telle quelle : `vault-resolve.py` la lit
dans le `CLAUDE.md` global pour retrouver le vault depuis un dossier de travail.
