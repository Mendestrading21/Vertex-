# SKYLER V2 — LOT 147 : caractérisation étendue de la couche stratégie

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-147`
(base : `integration/vertex-skyler-v2` @ `eb7eaa0`, lot 146 fusionné).
Caractérisation moteur — lot TESTS uniquement, aucun code moteur ni UI
modifié.

## 1. Cible

`vertex/engines/strategy_fit.py` (161 lignes, ratio de couverture
0.35 — le plus mince après analysis.py). SOURCE UNIQUE de la couche
stratégie : terminal.py:1059-1062 délègue `vehicle_of` /
`attach_vehicle` / `strat_score` (+ playbook, tilt) — c'est elle qui
choisit ACTION vs OPTION, re-pondère le score au profil offensif et
oriente les playbooks selon le climat. Le golden existant figeait les
chemins dorés uniquement.

## 2. Ce qui est figé (`tests/test_strategy_fit_lot147.py`, 17 tests)

```text
vehicle_of — les branches manquantes : AU CHOIX (zone o∈[1,2],
  ton gold) ; IV chère → ACTION avec message dédié « IV chère
  (62%) » ; OPTION expose le contrat complet {strike, exp, q,
  pop, pot}
strat_score — défauts EXACTS : score seul → 50 (st_* retombent
  sur le score, fund/risk/rs sur 50, régime inconnu pèse 12) ;
  ligne vide → plancher 22, jamais d'exception ; clamp à 0 sous
  l'empilement de pénalités
playbook_of — PRIORITÉ déclarée : une ligne qui matche Momentum
  Breakout ET Qualité forte reçoit le premier (ordre offensif
  assumé) ; les 6 playbooks atteignables un à un (contrat {ic,
  name, col, desc}) ; limite DOCUMENTÉE : Socle défensif exige un
  ext_atr EXPLICITE (absent → défaut 2 → jamais élu : le calme
  non prouvé n'est pas calme)
attach_vehicle — meilleur CALL par qualité, PUT ignoré même à
  qualité 99 ; board vide → ACTION « aucune option »
attach_strategy — repli plan.rr_res → vx_rr ; seuil rr_ok ≥ 2
  STRICT (1.99 échoue, 2.0 passe) ; plan prioritaire sur vx_rr ;
  R:R inconnu → rr None + rr_ok False (honnête)
strat_tilt — arithmétique exacte des 3 bandes : FAVORABLE 93
  (TREND 35 + RISK-ON 25 + breadth 18 + calme 15), NEUTRE 50
  (climat inconnu → round(12.5) bancaire = 12), DANGEREUX < 40 ;
  emphases et tailles de CALL par bande
```

## 3. Preuves

```text
python -m pytest tests/test_strategy_fit_lot147.py -q → 17 passed
python -m pytest tests/ -q → 2067 passed, 2 skipped (2050 + 17)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 148 : par ratio croissant — `postmortem.py` (0.61) puis
`market_lens.py` (0.66), `stats.py` (0.77).
