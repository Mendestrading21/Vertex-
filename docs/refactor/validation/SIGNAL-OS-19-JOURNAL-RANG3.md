# SIGNAL OS · LOT 19 — LE RANG 3 DU JOURNAL, INSTRUIT AVANT D'ÊTRE CONSTRUIT

Branche : `agent/vertex-signal-os-v1` · SW v224 → **v225** · Suite **3107 passed**

`PAGES.md` §7 rang 3 demande « les résultats **par grade / setup / horizon** ».
C'était la dernière dette de structure des huit espaces, annoncée depuis le
lot 12. Ce lot la ferme — mais **pas** en construisant les trois axes.

---

## 1. J'ai lu la donnée avant d'écrire la carte

Schéma réel d'une entrée de journal, mesuré dans `vx-entities.js` :

```js
{ id, ticker, tf, dir, reason, entry, stop, tp, risk, emo, conf, disc,
  trigger, result, exit, pnl, lesson, mistake, date, auto, kind, strike,
  invested, recovered }
```

| axe demandé | champ | constructible ? |
| --- | --- | --- |
| horizon | `tf` | **oui** |
| setup | `trigger` | **oui** (vide sur les clôtures automatiques) |
| win/loss | `result` (`WIN`/`LOSS`) | **oui** |
| **grade** | — | **le champ n'existe pas** |

### Pourquoi le grade n'est pas fabriqué

Deux chemins existaient, et les deux coûtent plus que l'axe ne rapporte :

1. **Étendre le schéma du bureau** — c'est une donnée **personnelle**
   synchronisée en last-writer-wins, dont un push partiel remplace le blob
   entier (`CLAUDE.md` §6). Ajouter un champ pour une carte de lecture engage
   un contrat de persistance.
2. **Aller le chercher côté moteur** — le grade S+/S/A/B est un score
   **moteur**, sur des recommandations. Le rang 1 de cette page sépare
   explicitement les deux sources : « aucun chiffre ne passe de l'une à
   l'autre ». Croiser un grade moteur avec un résultat déclaré à la main
   produirait un taux de réussite **par grade** que rien ne justifie.

> Le rang demandait trois axes. La donnée en porte deux. Le troisième est
> **dit absent dans la carte elle-même**, pas seulement dans ce rapport — une
> absence expliquée à l'écran, pas une absence rangée dans un document que
> l'utilisateur ne lit pas.

---

## 2. Ce qui est construit — `loadBuckets()`

`vertex/ui/pages/performance_page.py` · carte « Résultats par horizon et par
setup », hôte `#vx-pf-buckets`, vue `overview`.

- Ne compte que les décisions **résolues** (`result === 'WIN' || 'LOSS'`) — une
  décision en cours n'est pas une perte.
- Deux blocs : `tf` et `trigger`, six modalités au plus, triées par effectif.
- Chaque ligne : gagnants / perdants, taux, **et l'effectif** — un « 100 % » sur
  une décision se lit pour ce qu'il vaut.
- État vide honnête sous 3 décisions résolues, avec l'action « Ouvrir la
  chronologie ».
- Les entrées sans `trigger` sont étiquetées **« non renseigné »**, jamais
  fondues dans un setup nommé, et leur nombre est rapporté sous le bloc —
  ce sont les clôtures journalisées automatiquement.
- Pied de carte : effectif total **et** la raison de l'absence du grade.

---

## 3. Mesures — serveur `td-shell-v225` vérifié avant lecture

Vérification préalable : `curl /sw.js` → `td-shell-v225`. Un premier serveur
répondait encore en **v224** (instance restée en vie) ; sans ce contrôle
j'aurais mesuré la version d'avant et conclu que la carte n'existait pas.

| relevé | 1440 | 768 | 390 |
| --- | --- | --- | --- |
| erreurs de page | **0** | **0** | **0** |
| débordement de page | non | non | non |
| lignes rendues (7 décisions semées) | 8 | 8 | 8 |
| titre + question + pied | présents | présents | présents |

Jeu de contrôle semé (7 décisions résolues, dont 2 sans déclencheur) :

| bloc | rendu | somme |
| --- | --- | --- |
| horizon | swing 2/1 · position 1/1 · intraday 1/0 · non renseigné 0/1 | 7 ✓ |
| setup | cassure 1/1 · non renseigné 1/1 · gap 1/1 · pullback 1/0 | 7 ✓ |

Note rendue : « 2 entrée(s) sans déclencheur — clôtures journalisées
automatiquement. » — cohérente avec les 2 entrées semées à `trigger` vide.

Sur le jeu **démo tel quel** (journal vide), la carte rend son état vide et rien
d'autre : aucun chiffre inventé pour remplir la place.

---

## 4. Gardien — `tests/test_signal_os_journal_rangs_lot11.py` (+3 tests, 9 au total)

| mutation | résultat |
| --- | --- |
| carte retirée de l'appel `overview` | 1 échec |
| `grouper('tf')` retiré | 1 échec |
| filtre WIN/LOSS retiré | 1 échec |
| découpage par grade ajouté | 1 échec |
| explication de l'absence du grade retirée | 1 échec |
| étiquette « non renseigné » retirée | 1 échec |
| décompte des entrées sans déclencheur retiré | 1 échec |

### La portée trop large, dixième occurrence

Ma première version vérifiait l'appel par `'loadBuckets()' in src`. Elle
restait **verte** quand on retirait l'appel : `function loadBuckets(){` contient
la chaîne `loadBuckets()` — les caractères `(){` incluent `()`. La déclaration
satisfaisait le test censé prouver que la carte s'affiche.

Remplacé par une lecture de **la ligne de dispatch** :

```python
dispatch = src[src.index("if(VIEW==='overview')"):]
dispatch = dispatch[:dispatch.index('\n')]
assert 'loadBuckets();' in dispatch
```

Mutation re-jouée : `[carte retiree] -> 1 failed, 8 passed`.

C'est la dixième fois dans cette refonte qu'une assertion mesure plus large que
son objet, et la plus discrète : la chaîne cherchée était syntaxiquement
présente **dans un tout autre rôle**.

---

## 5. État de la dette après ce lot

Les huit espaces sont audités rang par rang. Il reste **une** zone non mesurée :

- `/analysis/<ticker>` — l'ouvrir déclenche `/api/ticker/<sym>`, appel sortant
  interdit dans cet environnement. Non mesuré, et dit comme tel plutôt que
  déclaré conforme.
