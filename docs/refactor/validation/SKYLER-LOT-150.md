# SKYLER V2 — LOT 150 : caractérisation du digest de session + bilan de tournée

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-150`
(base : `integration/vertex-skyler-v2` @ `743ab6d`, lot 149 fusionné).
Caractérisation moteur — lot TESTS uniquement, aucun code moteur ni UI
modifié. Clôture de la file « moteurs minces ».

## 1. Cible

`vertex/engines/session_digest.py` (116 lignes, ratio 0.80 — dernier
de la file) — fonction pure servie par `/api/session/digest`
(session_api.py), affichée en tête d'Aujourd'hui : état de session,
régime lisible, opportunités actionnables, prochain catalyseur,
confiance des données.

## 2. Ce qui est figé (`tests/test_session_digest_lot150.py`, 8 tests)

```text
Régime — gardes : RISK-ON + S&P en CHOP → NEUTRE/wait (un risk-on
  dans un marché haché n'est pas un feu vert) ; RISK-OFF
  prioritaire même seul (et un market_ctx seul suffit à 'ready') ;
  score /100 branché sur l'UNIQUE source market_lens.climate
  (93 sur le contexte porteur du lot 149 — jamais réinventé)
Catalyseurs — dte True (bool), 'demain' (texte) et entrée brute
  ignorés SANS masquer les valides ; tri croissant (le plus
  proche gagne) ; count = les datés seulement
Âge — scan_ts booléen → None (pas d'âge fantôme, même garde que
  le lot 142 côté UI) ; ts réel → entier en secondes
Dégradé — build(None, None) → 'analyzing', confidence None,
  régime None/idle ; top borné à 3 (le compte reste complet) ;
  décision sans symbol et entrée brute exclues
Contrat — clés exactes du digest et de chaque sous-objet,
  generator='deterministic'
```

## 3. Preuves

```text
python -m pytest tests/test_session_digest_lot150.py -q → 8 passed
python -m pytest tests/ -q → 2098 passed, 2 skipped (2090 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. MINI-BILAN tournée 146-150 (voir aussi STATUS.md)

5 lots, PR #179 → #183, suite 2033 → 2098 passed (+65 tests), SW
stable v151. La file des moteurs par couverture croissante est
ÉPUISÉE : analysis (0.19→couvert), strategy_fit (0.35), postmortem
(0.61), market_lens (0.66), stats (0.77), session_digest (0.80).
Découvertes clés documentées par des tests : divergence des seuils
FAVORABLE 62 (climat) vs 65 (tilt) ; Spearman à rangs ordinaux
(série constante → 1.0) ; break-even classé perte ; profit factor
None jamais infini ; booléens rejetés partout par les gardes
numériques ; Socle défensif exige un ext_atr explicite.

## 5. Suite

LOT 151 : nouvelle direction — caractériser les modules minces HORS
engines/ (vertex/quant/, vertex/market/, vertex/services/) par le
même critère de ratio, en commençant par le plus utile au produit.
