# Généraliser — des occurrences réelles à la trame réutilisable

La généralisation est le cœur du skill, et son risque : une trame trop abstraite ne sert à rien,
une trame trop collée à un cas n'est pas réutilisable. La règle de discipline : **tout ce qui est
dans la trame doit tracer vers un cas réel ; tout ce qui varie entre les cas doit être visible.**

## 1. Le critère de codification : ≥ 2 occurrences réelles

| Situation | Geste |
|-----------|-------|
| ≥ 2 occurrences trouvées dans le vault | codifier |
| 1 seule occurrence | le dire, proposer d'**attendre la récidive** — `sync-vault` la signalera |
| 1 seule occurrence mais le dirigeant insiste | codifier, et marquer dans la trame : « établie sur un seul cas ({wikilink}) — à affiner au prochain usage » |
| 0 occurrence (la pratique vit hors du vault) | ce n'est pas une extraction : proposer `import-note` (le modèle existe déjà ailleurs) ou noter la pratique au fil de l'usage |

Pourquoi 2 : avec un seul cas, on ne sait pas distinguer **ce qui est la méthode** de **ce qui était
les circonstances**. La deuxième occurrence révèle le commun.

## 2. La méthode : commun / variantes / placeholders

1. **Squelette commun** — les étapes, sections ou questions présentes dans *tous* les cas. C'est le
   corps de la trame, dans l'ordre où les cas le déroulent.
2. **Variantes** — ce qui est présent dans *certains* cas seulement, avec sa condition :
   `**Si {contexte} :** {l'étape ou la section supplémentaire}`. Une variante sans condition
   identifiable → la signaler au dirigeant plutôt que trancher seul.
3. **Placeholders** — les spécifiques de chaque cas (noms, dates, montants, interlocuteurs)
   deviennent des `{placeholders}` nommés par leur rôle : `{client}`, `{échéance}`, `{décideur}`.

Exemple (avant → après) :

```markdown
<!-- Cas 1 (10-Projects/rachat-dupont/) : « Relancé Dupont à J+7 par mail, puis appel à J+14 » -->
<!-- Cas 2 (40-Archive/cession-martin/) : « Relance Martin J+7 mail ; J+15 appel ; J+21 courrier » -->

## Relance
1. J+7 — mail de relance à {interlocuteur}
2. J+14 — appel
**Si pas de réponse à l'appel :** J+21 — courrier (vu sur [[cession-martin]])
```

Ce qu'aucun cas ne contient n'entre pas dans la trame — même si « ça semblerait logique ». Une
intuition d'amélioration se propose à part (« les cas ne le font pas, veux-tu l'ajouter ? »), jamais
en silence.

## 3. Où ranger : inférer la logique depuis l'arborescence

La logique d'organisation de `30-Resources/` a été choisie à l'interview, mais la source fiable est
**l'arborescence réelle** (le plan-vault peut avoir été trié depuis). Signaux :

| Sous-dossiers observés | Logique | Rangement de la trame |
|------------------------|---------|----------------------|
| `methodologies/`, `trames/`, `runbooks/`, `benchmarks/`, `templates/` | **par type** | la sous-zone du type (souvent `methodologies/` ou `trames/`) |
| `juridique/`, `rh-social/`, `finance/`, noms de domaines métier | **par domaine** | la sous-zone du domaine que la trame sert |
| Mixte ou ambigu | — | proposer, laisser trancher |

Toujours **proposer** la sous-zone, jamais l'imposer. Si aucune sous-zone ne convient, en proposer
une nouvelle (kebab-case) plutôt que de poser la trame à plat dans `30-Resources/`.

`references-externes/` n'accueille **jamais** une trame : c'est la zone des renvois.

## 4. Les liens bidirectionnels

- **Dans la trame** — frontmatter `source:` + une ligne en fin de fiche :
  `Établie sur : [[{cas-1}]], [[{cas-2}]]`.
- **Dans chaque fiche source** — une ligne près du passage concerné : `Trame : [[{trame}]]`.
- **Dans le `_index.md`** de la sous-zone, s'il existe — cocher l'item s'il y figurait
  (`- [x] {nom} — [[{trame}]]`), sinon l'ajouter coché.

C'est ce qui empêche la trame de devenir orpheline : une ressource que rien ne pointe est invisible
au moment où on en aurait besoin.

## 5. Garde-fous

- **Rien d'inventé** : chaque élément de la trame trace vers un cas ; les ajouts spéculatifs sont
  proposés explicitement, jamais glissés.
- **Pas de 🔒** : aucun nom, chiffre ou donnée sensible d'un cas dans la trame — les placeholders
  remplacent, les wikilinks renvoient (`governance.md`).
- **Pas de codification du cas unique** sans accord explicite (et marquage).
- **Non destructif** : si une trame proche existe déjà dans `30-Resources/`, proposer de
  l'**enrichir** avec les nouvelles occurrences plutôt que d'en créer une deuxième.
