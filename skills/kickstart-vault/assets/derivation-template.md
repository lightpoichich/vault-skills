---
type: moc
topic: derivation
updated: {YYYY-MM-DD}
---

# Pourquoi ton espace est organisé ainsi

> La mémoire de comment cet espace a été monté et pourquoi il a cette forme. Les autres fiches
> `_Meta/` disent ce que sont les règles ; celle-ci dit pourquoi elles sont là.
> Tu n'as pas besoin de la lire pour travailler. Ouvre-la quand tu te demandes pourquoi c'est rangé
> comme ça, ou avant de changer la structure (la fin du fichier dit comment).
> Posée au montage à partir de ce que tu as décrit lors de la cartographie. Si tu fais évoluer ton
> espace, mets-la à jour.

## Les quatre familles (PARA)

Ton espace est rangé en quatre familles.

- **Projets** : ce qui a une fin et un livrable ; ça se termine, puis s'archive.
- **Domaines** : tes responsabilités continues ; ça ne se termine pas, ça s'entretient.
- **Ressources** : ce qui ressert ; modèles, documents de référence, renvois vers tes outils.
- **Archive** : ce qui est clos ; on déplace, on ne supprime pas.

Le tri tient à une question : est-ce que ça a une date de fin ? Une date de fin fait un Projet. Pas
de date de fin, mais une responsabilité, fait un Domaine. Cette question garde l'espace lisible
quand il grossit.

## Pourquoi tes domaines et tes projets

Ils viennent de ta cartographie d'activité, pas d'un modèle générique.

- **Domaines retenus** : {liste reprise du plan}. Raison : {ce que la cartographie a fait ressortir
  comme responsabilités récurrentes}.
- **Projets ouverts au montage** : {liste reprise du plan, ou « aucun pour l'instant »}.
- {Point d'attention signalé au montage, par exemple « X est noté comme domaine mais ressemble à un
  projet : à retrancher si besoin ». Sinon retirer cette ligne.}

Toute fiche est vide mais structurée au départ : on pose le cadre, le contenu entre au fil des
besoins.

## Pourquoi ces règles d'écriture

- **On range par destination** : ce qui reste ici (savoir) s'écrit directement ; ce qui part vers
  quelqu'un (mail, proposition, post) passe par un sas et n'est pas envoyé sans ta validation.
  L'espace se tient à jour seul sans agir à ta place. Détail : `_Meta/governance.md`.
- **On référence, on ne recopie pas** : tes documents de vérité restent là où ils vivent ; ici on
  garde un renvoi. Deux copies finiraient par se contredire.
- **Confidentialité 🔒** : {posture retenue au montage, par exemple « le sensible (RH, contrats)
  n'entre pas, seulement référencé », ou « pas d'enjeu sensible particulier »}.

## Pourquoi un assistant Chief of Staff par défaut

Un assistant généraliste est posé au montage ; tu le lances en tapant `cos`. Il produit le brief du
jour dès la première session, sur le seul contenu de l'espace. Il sert aussi de modèle quand tu
voudras un assistant dédié à un rôle précis.

## Faire évoluer cette structure

La forme suit ton activité. Chaque geste a sa compétence :

- **Ajouter ou compléter un projet** : `nouveau-projet`.
- **Faire naître, renommer, scinder, fusionner ou archiver un domaine** : `gerer-area`.
- **Ajouter un assistant dédié à un rôle** : `kickstart-persona`.
- **Repenser l'organisation en profondeur** : refaire la cartographie avec `interview-vault`, puis
  remonter la structure.

Après un changement de structure, mettre cette note à jour.
