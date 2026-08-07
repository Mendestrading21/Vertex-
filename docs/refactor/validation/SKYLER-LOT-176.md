# SKYLER V2 — LOT 176 : clôture de la tournée « honnêteté des routes »

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-176`
(base : `integration/vertex-skyler-v2` @ `a1767ba`, lot 175 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

Les trois lacunes minces restantes de la tournée, en un lot :
l'entonnoir (`opportunities_api.py`), le copilote POST
(`ai_api.py` /api/copilot/ask) et le Live Engine (`live_api.py`).

## 2. Ce qui est figé (`tests/test_routes_closure_lot176.py`, 8 tests)

```text
/api/opportunities/funnel — 7 étages exacts (universe → eligible →
  radar → priority → actionable → followed → positions) ; moteur en
  panne → 500 avec structure VIDE + erreur nommée ({stages: [],
  roles: [], error: 'ValueError: boom'}) — jamais un entonnoir à
  moitié inventé
/api/copilot/ask (POST) — body vide OU JSON corrompu → HTTP 200
  {ok: false, error: 'question vide', answer/source: null} — jamais
  une 500 ; question sans clé → repli déterministe DOUBLEMENT
  étiqueté (label « Moteurs déterministes (Claude non configuré ou
  indisponible) » ET l'étiquette dans la réponse elle-même — le
  contenu varie selon le scan, l'étiquette jamais)
/api/live/report — contrat {lines, requested, ts}, vide honnête à
  froid ; /api/live/refresh?domains=prices, news , → parsing purge
  espaces et segments vides en gardant l'ordre (requested exact) ;
  domaine inconnu → kicked False, rien relancé, demande tracée
Invariant — aucun verbe d'ordre dans les 3 modules
```

Leçon d'ordre de suite encodée : `kicked` dépend de l'état du moteur
(occupé → pas de relance) et la réponse du copilote dépend des
données laissées par les tests précédents — les tests figent les
INVARIANTS stables (parsing, étiquettes), pas les états transitoires.

## 3. Preuves

```text
python -m pytest tests/test_routes_closure_lot176.py -q → 8 passed
python -m pytest tests/ -q → 2383 passed, 2 skipped (2375 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

La tournée « honnêteté des routes » est CLOSE (171-176 : positions,
decision, tracking, planning+search, session, funnel+copilot+live).
LOT 177 : nouvelle direction au survey — candidats : pages UI
extraites (vertex/ui/pages/), outils d'audit (tools/), ou modules
restants à couverture partielle hors routes.
