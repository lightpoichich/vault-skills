# Mise à niveau d'un vault installé

Quand le plugin évolue, ses gabarits changent ; un vault déjà installé ne reçoit rien de lui-même.
Cette procédure lui apporte les changements sans toucher à ce que l'utilisateur a écrit. Elle
s'appuie sur `hooks/vault-upgrade.py`, sans modèle de langage, et sur la fiche
d'installation `_Meta/installation.md`.

## Ce qui est géré

| Unité | Mode | Pourquoi |
|---|---|---|
| `_personas/cos/.claude/skills/brief-du-jour/` (tous ses fichiers) | copie | posé tel quel ; une amélioration du brief doit arriver dans le vault |
| `_Meta/hooks.conf` | copie | posé tel quel ; ses commentaires documentent les nouveaux réglages |
| `CLAUDE.md` racine, blocs `carte` et `regles` | bloc | le périmètre et le ton viennent du plan, la carte et les règles du plugin |
| `_Meta/Schema.md`, bloc `conventions` | bloc | les types viennent du plan, les conventions générales du plugin |
| `_personas/cos/CLAUDE.md`, bloc `regles` | bloc | le rôle et les zones s'ajustent à l'usage ; les règles d'écriture et le hors-périmètre restent ceux du plugin |

`_personas/cos/capacites-a-construire.md` appartient à l'utilisateur dès l'installation et n'est
pas géré. Le texte hors des balises `socle second-cerveau` n'est jamais lu ni touché.

## 1. Dresser l'état

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-upgrade.py" check --vault "{vault}"
```

Le script rend, pour chaque unité, l'un des cas suivants, puis les migrations en attente et les
versions du vault et du plugin.

| Cas | Sens | Suite |
|---|---|---|
| à jour | identique au gabarit actuel | rien |
| remplaçable | jamais modifié depuis l'intégration, gabarit changé | remplacé par `apply` |
| nouveau | fichier ajouté au gabarit, dossier présent dans le vault | ajouté par `apply` |
| personnalisé, gabarit inchangé | modifié par l'utilisateur, rien de neuf côté plugin | rien |
| fusion à proposer | modifié par l'utilisateur et gabarit changé | fusion assistée, étape 4 |
| inconnu | pas d'empreinte dans la fiche d'installation (vault installé avant ce mécanisme) | revue assistée, étape 4 |
| balises absentes | bloc introuvable dans le fichier du vault | revue assistée, étape 4 |
| absent, retiré du gabarit | fichier supprimé par l'utilisateur, ou plus fourni par le plugin | signalé, jamais recréé ni supprimé |

## 2. Présenter le plan

Simulation : `vault-upgrade.py apply --vault "{vault}"`. Montrer en quelques lignes ce qui sera
remplacé ou ajouté, les migrations et leurs fichiers, les unités à revoir. Attendre un go explicite.

## 3. Appliquer

Si le vault est un dépôt git (`git -C "{vault}" rev-parse --is-inside-work-tree` réussit), proposer
un commit du vault. Sinon, n'en proposer aucun : le script copie de toute façon les fichiers qu'il
touche. Puis :

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/hooks/vault-upgrade.py" apply --vault "{vault}" --apply
```

Le script copie d'abord les fichiers touchés dans
`${XDG_STATE_HOME:-~/.local/state}/second-cerveau/mise-a-niveau/`, remplace le remplaçable, applique
les migrations, met la fiche d'installation à jour. Il n'écrit jamais un fichier personnalisé.

Migrations : chacune est déclarée dans le script (identifiant, version, contrôle, action),
idempotente, et inscrite dans la fiche d'installation une fois appliquée. `5.0.0-noms-skills` réécrit les noms de
skills retirés, entre accents graves, dans le `CLAUDE.md` racine, les `CLAUDE.md` des personas et les
fichiers des skills du vault ; une fiche ordinaire garde son historique.

## 4. Fusion assistée

Pour chaque unité en fusion, inconnue ou sans balises :

1. Lire la version du vault et le gabarit actuel (`skills/installer/assets/`), montrer l'écart en
   clair : ce que le plugin apporte, ce que l'utilisateur a personnalisé.
2. Proposer une version fusionnée qui garde les personnalisations et intègre les apports. Pour des
   balises absentes, proposer de les poser autour de la section correspondante.
3. Écrire seulement sur validation, puis déclarer la fusion faite :
   `vault-upgrade.py accept --vault "{vault}" --apply {unité}`.
4. Si l'utilisateur garde sa version telle quelle, la déclarer aussi par `accept` : le gabarit
   actuel est tenu pour intégré, et le signal cesse jusqu'au prochain changement du plugin.

## 5. Rendre compte

Unités remplacées et ajoutées, migrations appliquées, fusions faites ou refusées, chemin de la
sauvegarde. Un vault sans fiche d'installation en reçoit une à sa première mise à niveau : les unités
identiques au gabarit y sont notées intégrées, les autres restent à revoir, rien n'est écrasé.

## Signal

Le bilan de démarrage signale un vault sans fiche d'installation, et un vault dont une unité est remplaçable, en
fusion ou nouvelle, ou qui a une migration en attente. Une fois la fiche d'installation posée et la mise à niveau
faite, il ne dit plus rien. `UPGRADE_REMINDER=0` dans `_Meta/hooks.conf` coupe le signal.
