# SIGNAL OS · LOT 12 — « AUCUN GRAPHIQUE SANS QUESTION NI CONCLUSION »

Branche : `agent/vertex-signal-os-v1` · SW v218 → **v219** · Suite **3097 passed**

`CHARTS.md` pose une règle courte et testable. Je l'ai mesurée sur les **12
graphiques rendus** des 26 vues du produit. Ce lot raconte surtout **trois
fausses accusations**, dont une que j'avais déjà appliquée au produit.

---

## 1. Premier relevé : 12 sur 12 en échec

Un taux pareil trahit l'instrument, pas le produit.

### Fausse accusation n°1 — l'absence visuelle prise pour une absence

Le Chart Shell rend la question dans `.vx-chart-question` **uniquement quand il
n'y a pas de conclusion** :

```js
${opts.question && !opts.conclusion ? `<span class="vx-chart-question">…` :
  (opts.question ? `<span class="vx-sr-only">…` : '')}
```

Quand une conclusion existe, la question part en `.vx-sr-only` — délibérément,
pour ne pas la répéter au-dessus de la conclusion. Mon relevé cherchait la
classe visible. **12 → 3.**

### Fausse accusation n°2 — la carte la plus interne

« Put long » (Options / structures) : mon relevé lisait `cv.closest('.vx-card')`,
donc la carte **du graphique**. Un niveau au-dessus, la carte hôte porte le
titre « Payoff à l'échéance » et la question visible « Où gagne / perd la
structure selon le cours ? ». **3 → 2.**

### Fausse accusation n°3 — et celle-ci, je l'avais déjà appliquée

J'avais conclu que la conclusion du payoff **doublait** celle de sa carte hôte,
et je l'avais retirée du produit.

`querySelector` **traverse les descendants** : en interrogeant la carte hôte, je
relisais la conclusion **du graphique** et je la comptais à deux niveaux. La
carte hôte n'en a jamais eu.

Mesuré après le retrait : sur toute la vue Structures, **2 questions, zéro
conclusion**. Ce n'était pas un doublon en moins, c'était **la seule conclusion
en moins**. Rétabli.

> La leçon n'est pas « mieux mesurer ». C'est que **j'ai modifié le produit sur
> la foi d'un relevé que je n'avais pas contre-vérifié**, alors que les deux
> accusations précédentes du même relevé venaient d'être invalidées. Le bon
> réflexe était de suspecter l'instrument une troisième fois.

---

## 2. Ce que le même relevé a trouvé de vrai — deux défauts

### Marchés / breadth — « Tendance de participation »

Une question, **aucune conclusion**. Seul graphique de Marchés dans ce cas.

La conclusion est désormais **dérivée de la série tracée** (premier vs dernier
point de « > MM200 ») et **omise** si les deux bornes manquent. Une phrase
générique aurait été pire qu'une absence : elle aurait eu l'air d'une mesure.

### Portefeuille / risque — le donut « Secteurs »

**Ni question ni conclusion** — et la cause est structurelle : ce donut est le
seul graphique du produit monté dans une carte **bâtie à la main par la page**,
donc sans le gabarit `VXCharts.card` qui impose les deux.

Il reçoit la question de concentration et une conclusion qui **nomme le secteur
dominant et sa part réelle**, vide si le calcul ne tient pas.

---

## 3. Marchés — les rangs de `PAGES.md` §2

| rang | état |
| --- | --- |
| 1. Régime | couvert (`overview`) |
| 2. Indices / cross-asset | couvert (`overview`, `macro`) |
| 3. Leadership secteur/facteurs | couvert (`overview`, `sectors`) |
| 4. Breadth | couvert (`breadth`) |
| 5. Volatilité / stress | couvert (`volatility`) |
| 6. Calendrier macro pertinent | **domicilié ailleurs** |

Les cinq vues demandées existent et portent les noms canoniques. Le rang 6 n'est
pas dans Marchés : le calendrier vit sur **Aujourd'hui** (« Catalyseurs »). Même
arbitrage qu'au lot 11 pour l'équité — « une donnée = un seul domicile » prime
sur la liste des rangs.

---

## 4. Mesures — serveur `td-shell-v219` vérifié avant lecture

| relevé | avant | après |
| --- | --- | --- |
| graphiques rendus (26 vues) | 12 | 12 |
| sans question et/ou conclusion | **1** *(après correction des 2 instruments)* | **0** |

Suite **3097 passed**.

Gardien `tests/test_signal_os_graphiques_qc_lot12.py` — 4 tests, **8 mutations
sur 8 tuées** :

| mutation | résultat |
| --- | --- |
| question `sr-only` supprimée du Chart Shell | 1 échec |
| ternaire « simplifié » (question visible seulement) | 1 échec |
| conclusion du breadth retirée | 1 échec |
| garde des deux bornes retirée | 1 échec |
| conclusion générique au lieu d'une conclusion dérivée | 1 échec |
| question du donut retirée | 1 échec |
| conclusion du donut retirée | 1 échec |
| conclusion du payoff retirée | 1 échec |

Le premier test est celui qui compte le plus : si quelqu'un « simplifiait » le
ternaire du Chart Shell, **toutes** les questions des graphiques concluants
disparaîtraient du document — invisibles à l'écran *et* absentes pour les
lecteurs d'écran, sans qu'aucune page ne change.

---

## 5. Dette

- Rang 3 du Journal (grade / setup / horizon) et win/loss par bucket.
- Opportunités, Portefeuille (5 vues sur 6), Options : rangs non audités.
- `chart-theme-obsidian-copper.js` : nom qui ment.
- Étiquetage démo : figé en caractérisation.
- Aucun instrument ne détecte le rognage silencieux.
- 5 modules UI morts (146 Ko, 0 consommateur).
