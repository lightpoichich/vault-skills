# Acquisition : l'étage variable

Transformer n'importe quelle entrée en markdown propre, prêt à classer. Aucun connecteur n'est
présupposé.

## Détecter la nature de l'entrée

| Indice | Nature | Acquisition |
|--------|--------|-------------|
| Commence par `http://` ou `https://`, domaine Notion (`notion.so`) | page Notion | connecteur Notion, sinon export |
| Commence par `http(s)://`, autre domaine | URL ou article web | `obsidian:defuddle` si disponible, sinon WebFetch et nettoyage à la main |
| Chemin de fichier (`/…`, `~/…`, `./…`, extension `.md`, `.txt`, `.pdf`) | fichier local | lecture directe |
| Bloc de texte fourni dans la conversation | texte collé | tel quel |

En cas d'ambiguïté (un lien qui pourrait être l'un ou l'autre), demander plutôt que deviner.

## Acquérir par type

### URL ou article web
- Si le skill `obsidian:defuddle` est disponible, l'invoquer : il extrait le contenu utile en
  markdown sans le bruit de navigation. Sinon, WebFetch puis nettoyage à la main (navigation,
  publicités, pieds de page).
- Garder le titre et l'URL d'origine pour le frontmatter (`source:`).

### Page Notion
- Regarder `_Meta/sources.md` : si Notion est déclaré `actif`, tenter le connecteur via
  `ToolSearch` (requête `notion fetch page`) et récupérer le contenu de la page.
- Si Notion n'est pas déclaré actif, ou si le connecteur ne répond pas, demander à l'utilisateur
  un export markdown de la page ou un collage. Ne pas bloquer sur l'absence de MCP.
- Conserver l'URL Notion comme `source:`.

### Fichier local
- Lire le fichier (`Read`). Pour un `.pdf`, utiliser la lecture native ; pour `.md` et `.txt`, le
  contenu est déjà propre.
- L'origine `source:` est le chemin du fichier.

### Texte collé
- Le contenu fourni dans la conversation est la matière. Sans source externe, `source:` peut rester
  vide ou porter une mention (« collé le {date} »).

## Dans tous les cas

- **Conserver l'origine** : URL, lien Notion ou chemin alimente le champ `source:` de la fiche, pour
  la traçabilité et un éventuel renvoi.
- **Ne pas sur-nettoyer** : enlever le bruit sans réécrire le fond. Reformuler ou condenser est hors
  périmètre de l'import.
- **Sensibilité d'abord** : si la source est `renvoi 🔒` ou le contenu manifestement sensible, ne pas
  acquérir pour copie ; basculer sur un renvoi (`classement.md` et `governance.md`).
