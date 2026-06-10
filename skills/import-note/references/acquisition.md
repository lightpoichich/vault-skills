# Acquisition — l'étage variable

C'est ici que vit la variabilité entre dirigeants. Le but : transformer **n'importe quelle entrée**
en **markdown propre**, prêt à classer. Aucun connecteur n'est présupposé — on s'adapte à ce qui
arrive.

## Détecter la nature de l'entrée

| Indice | Nature | Acquisition |
|--------|--------|-------------|
| Commence par `http://` / `https://`, domaine Notion (`notion.so`) | **page Notion** | connecteur Notion ou export |
| Commence par `http(s)://`, autre domaine | **URL / article web** | `obsidian:defuddle` |
| Chemin de fichier (`/…`, `~/…`, `./…`, extension `.md`/`.txt`/`.pdf`) | **fichier local** | lecture directe |
| Bloc de texte fourni dans la conversation | **texte collé** | tel quel |

En cas d'ambiguïté (un lien qui pourrait être l'un ou l'autre), **demander** plutôt que deviner.

## Acquérir par type

### URL / article web → `obsidian:defuddle`
- Invoquer le skill **`obsidian:defuddle`** : il extrait le contenu utile en markdown et enlève le
  bruit (navigation, pubs, pieds de page). C'est préférable à un fetch brut, qui ramène du HTML sale.
- Garder le **titre** et l'**URL d'origine** pour le frontmatter (`source:`).

### Page Notion → connecteur si déclaré, sinon export
- Regarder `_Meta/sources.md` : si Notion est déclaré `actif`, **tenter** le connecteur via
  `ToolSearch` (requête `notion fetch page`) et récupérer le contenu de la page.
- Si Notion n'est **pas** déclaré actif, ou si le connecteur ne répond pas → demander à l'utilisateur
  un **export markdown** de la page (ou un collage). Ne pas bloquer sur l'absence de MCP.
- Conserver l'URL Notion comme `source:`.

### Fichier local → lecture directe
- Lire le fichier (`Read`). Pour un `.pdf`, utiliser la lecture native ; pour `.md`/`.txt`, le contenu
  est déjà propre.
- L'origine `source:` = le chemin du fichier.

### Texte collé → tel quel
- Le contenu fourni dans la conversation est la matière. Pas de source externe → `source:` peut être
  vide ou une mention (« collé le {date} »).

## Toujours

- **Conserver l'origine.** URL, lien Notion, ou chemin : il alimente le champ `source:` de la fiche,
  pour la traçabilité et un éventuel renvoi.
- **Ne pas sur-nettoyer.** On enlève le bruit, on ne réécrit pas le fond. Reformuler/condenser, c'est
  le rôle d'un autre skill (`reformuler`), pas de l'import.
- **Sensibilité d'abord.** Si la source est `renvoi 🔒` ou le contenu manifestement sensible, ne pas
  acquérir pour copie — basculer sur un renvoi (voir `classement.md` et `governance.md`).
