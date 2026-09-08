# Généraliser : des occurrences réelles à la trame réutilisable

Règle de discipline : tout ce qui est dans la trame trace vers un cas réel, et tout ce qui varie
entre les cas reste visible.

## 1. Le critère de codification : deux occurrences réelles au moins

| Situation | Geste |
|-----------|-------|
| Deux occurrences ou plus trouvées dans le vault | codifier |
| Une seule occurrence | le dire, proposer d'attendre la récidive ; `sync-vault` la signalera |
| Une seule occurrence mais l'utilisateur insiste | codifier, et marquer dans la trame : « établie sur un seul cas ({wikilink}), à affiner au prochain usage » |
| Aucune occurrence (la pratique vit hors du vault) | ce n'est pas une extraction : proposer `import-note` (le modèle existe déjà ailleurs) ou noter la pratique au fil de l'usage |

Avec un seul cas, on ne distingue pas la méthode des circonstances ; la deuxième occurrence révèle
le commun.

## 2. La méthode : commun, variantes, placeholders

1. **Squelette commun** : les étapes, sections ou questions présentes dans tous les cas. C'est le
   corps de la trame, dans l'ordre où les cas le déroulent.
2. **Variantes** : ce qui est présent dans certains cas seulement, avec sa condition, sous la forme
   `**Si {contexte} :** {l'étape ou la section supplémentaire}`. Une variante sans condition
   identifiable se signale à l'utilisateur plutôt que d'être tranchée seul.
3. **Placeholders** : les spécifiques de chaque cas (noms, dates, montants, interlocuteurs)
   deviennent des `{placeholders}` nommés par leur rôle : `{client}`, `{échéance}`, `{décideur}`.

Exemple. Cas 1 (`10-Projects/rachat-dupont/`) : « Relancé Dupont à J+7 par mail, puis appel à
J+14 ». Cas 2 (`40-Archive/cession-martin/`) : « Relance Martin J+7 mail ; J+15 appel ; J+21
courrier ». Trame obtenue :

```markdown
## Relance
1. J+7 : mail de relance à {interlocuteur}
2. J+14 : appel
**Si pas de réponse à l'appel :** J+21, courrier (vu sur [[cession-martin]])
```

Ce qu'aucun cas ne contient n'entre pas dans la trame, même si l'ajout semble logique. Une
intuition d'amélioration se propose à part (« les cas ne le font pas, veux-tu l'ajouter ? »),
jamais en silence.

## 3. Où ranger : inférer la logique depuis l'arborescence

La source fiable est l'arborescence réelle de `30-Resources/`, pas le plan-vault initial. Signaux :

| Sous-dossiers observés | Logique | Rangement de la trame |
|------------------------|---------|----------------------|
| `methodologies/`, `trames/`, `runbooks/`, `benchmarks/`, `templates/` | par type | la sous-zone du type (souvent `methodologies/` ou `trames/`) |
| `juridique/`, `rh-social/`, `finance/`, noms de domaines métier | par domaine | la sous-zone du domaine que la trame sert |
| Mixte ou ambigu | indéterminée | proposer, laisser trancher |

Proposer la sous-zone sans l'imposer. Si aucune sous-zone ne convient, en proposer une nouvelle en
kebab-case plutôt que de poser la trame à plat dans `30-Resources/`. `references-externes/`
n'accueille pas de trame : c'est la zone des renvois.

## 4. Les liens bidirectionnels

- **Dans la trame** : frontmatter `source:` et une ligne en fin de fiche,
  `Établie sur : [[{cas-1}]], [[{cas-2}]]`.
- **Dans chaque fiche source** : une ligne près du passage concerné, `Trame : [[{trame}]]`.
- **Dans le `_index.md`** de la sous-zone, s'il existe : cocher l'item s'il y figurait
  (`- [x] {nom} : [[{trame}]]`), sinon l'ajouter coché.

Une ressource que rien ne pointe est invisible au moment où on en aurait besoin.

## 5. Garde-fous

- **Rien d'inventé** : chaque élément de la trame trace vers un cas ; les ajouts spéculatifs sont
  proposés explicitement, jamais glissés.
- **Pas de 🔒** : aucun nom, chiffre ou donnée sensible d'un cas dans la trame. Les placeholders
  remplacent, les wikilinks renvoient (`governance.md`).
- **Cas unique** : pas de codification sans accord explicite de l'utilisateur, et marquage dans
  la trame.
- **Non destructif** : si une trame proche existe déjà dans `30-Resources/`, proposer de
  l'enrichir avec les nouvelles occurrences plutôt que d'en créer une deuxième.
