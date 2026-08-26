# G2 · #783 — Le seul vrai doublon n'était pas un doublon de code

Gardien : `tests/test_vertex_1_0_domaines_convergence.py` (6 tests, 3/3 mutations)
Carte   : `docs/vertex-1.0/inventory/DOMAIN_MAP.md` (#787)

---

## Ce que G2 demandait, et ce que la mesure a répondu

> « Plusieurs domaines se recouvrent (`company/companies`, `data/data_sources`,
> `portfolio/positions/tracking`) … adapters de compatibilité puis **retrait
> prouvé** des doublons. »

La carte des domaines a déjà réfuté la prémisse au sens large : **aucune dispute
de fichier**, et des recouvrements d'**un seul symbole** par paire. Restait la
question que la carte ne pouvait pas trancher — *ces quatre homonymes sont-ils
le même travail fait deux fois ?*

| symbole | paquets | verdict mesuré |
| --- | --- | --- |
| `get` | data / data_sources | profil d'entreprise `(sym, demo, allow_fetch, brief)` vs paquet analyste `(sym, ttl, force)` — **collision de nom** |
| `assess` | portfolio / positions | stress historique d'un panier vs santé d'une thèse — **collision** |
| `build` | portfolio / tracking | risque d'un panier vs cohorte d'options — **collision** |
| `mae_mfe` | positions / tracking | **la même notion financière, calculée deux fois** |

Trois noms génériques qui se rencontrent, **un seul vrai doublon**.

---

## Pourquoi ce doublon-là comptait

Deux calculs de la même mesure, ce n'est pas de la duplication de code : c'est
**deux réponses possibles à la même question**. Mesuré sur sept entrées, elles
divergeaient sur trois :

```text
entrée                    positions.calculator      tracking.returns
base NÉGATIVE             mae -220 · mfe -200       None · None
None dans la série        TypeError                 valeurs filtrées
chaîne numérique          TypeError                 coercée
```

**La première ligne est la faute.** `if not cost_basis` rejette `0` et `None`,
mais **laisse passer un négatif** — et rend alors un MAE/MFE parfaitement
plausible tiré d'une entrée absurde. C'est exactement ce que « aucune donnée
financière inventée » interdit, et c'est **plus dangereux qu'un plantage** :
un plantage se voit.

Le contexte aggrave le cas. `positions.calculator.mae_mfe` est **exporté dans
`__all__` et couvert par un test, mais aucun chemin de production ne l'appelle** :
`recalculator` n'utilise que `enrich_stock`, `enrich_option` et
`portfolio_weights`. Les trois seuls appels vivants vont à `tracking.returns`.
C'était un piège posé pour le prochain appelant — la même famille que
`performance_ledger`, du code qui se donne l'air vivant.

---

## La convergence

Le calcul de MAE/MFE est **délégué** à `vertex.tracking.returns`, seule
implémentation vivante. Le nom exporté et son contrat (`mae`/`mfe`) sont
conservés : c'est l'« adapter de compatibilité » que l'issue demande, pas une
suppression.

La coercion vient de **la même source** que le calcul délégué. Sans cela, les
deux fonctions accepteraient des entrées différentes et le désaccord reviendrait
par la bande — une convergence qui ne tiendrait qu'un temps.

Après : **les sept cas s'accordent**.

---

## Ce qui n'a PAS été fusionné, et pourquoi

`drawdown_from_peak` reste calculé localement. Ce n'est pas un oubli :

```text
drawdown_from_peak   drawdown MAXIMAL subi sur le chemin    [100,120,90,110] -> -25,00
drawdown_from_high   drawdown COURANT depuis le plus haut   [100,120,90,110] ->  -8,33
```

Deux **métriques**, pas deux implémentations. Les fusionner « pour converger »
aurait remplacé une mesure par une autre et fait disparaître une information du
produit — le contraire du service rendu. Un test tient ce contre-exemple.

C'est la nuance que le mot « converger » cache : *deux fonctions qui portent le
même nom ne font pas forcément la même chose, et deux fonctions qui font la même
chose ne portent pas forcément le même nom.* Seule la mesure sépare les deux.

---

## Campagne de mutation

| mutation | résultat |
| --- | --- |
| la garde du négatif retombe (`ref <= 0` → `ref == 0`) | **crie** |
| le calcul est recopié au lieu d'être délégué | **crie** |
| `drawdown_from_peak` remplacé par le drawdown courant | **crie** |

**3/3.** La deuxième mérite un mot : recopier le calcul corrigé aurait « convergé »
le résultat du jour et rouvert la divergence au premier ajustement. C'est la
délégation qui tient dans le temps, pas l'égalité des valeurs à un instant.

---

## Ce que cette mesure ne dit pas

- Elle porte sur les **quatre** symboles que la carte a signalés. Deux paquets
  peuvent faire le même travail sous des noms **différents** — cette
  duplication-là échappe à une comparaison par nom.
- `positions.calculator.mae_mfe` reste sans appelant de production. Sa
  **suppression** relève de `CLEANUP_POLICY.md` et d'une décision humaine ; la
  preuve de non-usage est consignée ici.
- Les livrables G2 « schéma versionné et migrations » et « journal append-only
  des décisions » ne sont pas couverts par ce lot.
