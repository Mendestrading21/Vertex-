# SKYLER V2 — LOT 148 : caractérisation étendue du post-mortem du Journal

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-148`
(base : `integration/vertex-skyler-v2` @ `571a952`, lot 147 fusionné).
Caractérisation moteur — lot TESTS uniquement, aucun code moteur ni UI
modifié.

## 1. Cible

`vertex/engines/postmortem.py` (151 lignes, ratio 0.61) — fonction
PURE servie par `/api/journal/postmortem` (desk.py:113) et affichée
dans Journal/Discipline : stats réelles des trades clôturés +
drapeaux de discipline dérivés des chiffres. Les tests existants
figent le scénario principal ; les bords n'étaient pas couverts.

## 2. Ce qui est figé (`tests/test_postmortem_lot148.py`, 10 tests)

```text
Coercition numérique : cost=True REJETÉ (bool est un int en Python,
  la garde _num le refuse — un flag ne devient jamais un coût) ;
  chaînes numériques '1000' acceptées ; 'inf' rejeté ; coût nul ou
  négatif inexploitable ; entrée non-dict sautée
Comportements limites DOCUMENTÉS : break-even (pnl 0) classé PERTE
  (un trade qui ne gagne rien n'est pas un gagnant) → win_rate 0,
  PF None (pas de ÷0) ; échantillon 100 % gagnant → PF None
  (honnête — indéfini, PAS infini), narrative sans phrase PF,
  aucun drapeau + « Aucun drapeau » énoncé
Drapeaux : « win rate élevé (67 %) mais P&L négatif » déclenché
  par 2 petits gains + 1 grosse perte ; récidives TRIÉES par
  nombre de pertes décroissant (Y×3 avant X×2, Z×1 exclu)
Dates : inversées → valeur absolue (9 j) ; non parsables → None
  EXCLU de la moyenne (pas de 0 inventé)
Journal : les 8 DERNIÈRES erreurs notées gardées, texte tronqué
  à 140 caractères
Contrat : mêmes clés plein/vide (+ reason côté vide),
  generator='deterministic' partout ; agrégation by_type exacte
```

## 3. Preuves

```text
python -m pytest tests/test_postmortem_lot148.py -q → 10 passed
python -m pytest tests/ -q → 2077 passed, 2 skipped (2067 + 10)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 149 : `market_lens.py` (0.66) puis `stats.py` (0.77) ;
MINI-BILAN 146-150 au lot 150.
