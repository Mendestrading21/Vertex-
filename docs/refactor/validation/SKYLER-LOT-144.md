# SKYLER V2 — LOT 144 : caractérisation du moteur de confluence multi-horizons

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-144`
(base : `integration/vertex-skyler-v2` @ `af74dc7`, lot 143 fusionné).
Retour aux caractérisations moteur — lot TESTS uniquement, aucun code
moteur ni UI modifié.

## 1. Cible

`vertex/engines/timeframes.py` (66 lignes) : le moteur de confluence
journalier × hebdomadaire qui contribue au score Vertex (`adj` borné
±5) et alimente le drapeau `mtf` du scan. **Aucun test direct**
n'existait — un des deux seuls moteurs à zéro référence dans tests/
(l'autre, `scorecard.py`, est un ancien moteur legacy).

## 2. Ce qui est figé (`tests/test_timeframes_lot144.py`, 13 tests)

```text
Les 5 états et leurs contributions exactes au score :
  ALIGNÉ HAUSSIER +5 · REPLI DANS TENDANCE +3 ·
  REBOND CONTRE-TENDANCE -4 · ALIGNÉ BAISSIER -5 · NEUTRE 0
  (NEUTRE = la branche la moins évidente : prix > EMA30 hebdo mais
   EMA10 hebdo qui se retourne — construite empiriquement)
Gardes d'entrée : < 32 semaines → None ; entrée non
  ré-échantillonnable (liste brute) → None — jamais de verdict
  sans historique, jamais d'exception
Contrat de sortie : 9 clés exactes, types (adj int borné ±5,
  weekly_rsi int 0-100, weekly_roc float, booléens réels),
  note non vide, cohérence stacked ⇒ above30
Comportement limite DOCUMENTÉ (pas un souhait) : série
  parfaitement plate → ALIGNÉ BAISSIER adj -5, RSI 100
  (prix == EMA30 → « au-dessus » False ; dn=0 → fillna(100)).
  Pathologique en réel ; le changer = décision explicite future.
```

Séries synthétiques déterministes (np.linspace) — on caractérise des
formes de marché, pas des titres ; aucune donnée inventée présentée
comme réelle.

## 3. Preuves

```text
python -m pytest tests/test_timeframes_lot144.py -q → 13 passed
python -m pytest tests/ -q → 1997 passed, 2 skipped (1984 + 13)
Aucun changement UI → pas de bump SW (v151 courante), pas de
validations navigateur requises
```

## 4. Suite

LOT 145 : caractérisation suivante (candidats : `scorecard.py` s'il
est encore servi, ou un moteur à 1 seule référence — analysis,
events, postmortem, pretrade…) + MINI-BILAN tournée 141-145.
