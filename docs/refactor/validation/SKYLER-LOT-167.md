# SKYLER V2 — LOT 167 : caractérisation étendue du copilote d'analyse

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-167`
(base : `integration/vertex-skyler-v2` @ `fa98671`, lot 166 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/ai/copilot.py` (159 lignes, ratio 0.37) — le copilote qui
répond en français ANCRÉ dans les nombres réels. Les 5 tests
existants (test_copilot.py) couvrent l'ancrage, le repli honnête et
le prompt anti-ordre ; ce lot fige les LACUNES. Anthropic entièrement
mocké — aucun appel réseau.

## 2. Ce qui est figé (`tests/test_copilot_lot167.py`, 8 tests)

```text
_positions_for — desk réel : cap à 20 positions, filtre par
  symbole, stop repris du snapshot d'entrée, entrées brutes
  exclues ; desk illisible → [] (jamais inventé)
build_context — sans symbole → SEULEMENT digest + positions (ni
  positioning ni flow ni synthesis) ; post-mortem chiffré INCLUS
  quand des trades clôturés existent (total_pnl 300 exact)
answer — symbole NORMALISÉ (majuscules, tronqué à 12) ; chemin
  Claude mocké : succès → source 'claude' avec étiquette
  « estimation, pas une donnée broker » + readonly True ; texte
  VIDE ou EXCEPTION API → repli déterministe étiqueté « Moteurs
  déterministes » (jamais d'exception propagée) ; contexte
  indisponible → ok False avec erreur honnête et answer None
  (pas de réponse inventée)
```

## 3. Preuves

```text
python -m pytest tests/test_copilot_lot167.py -q → 8 passed
python -m pytest tests/ -q → 2289 passed, 2 skipped (2281 + 8)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 168 : data/company.py (340 l, 0.39) OU legacy_adapter partie 1
(272 l) OU data/universe.py (324 l, 0.56). Mini-bilan 166-170 au
lot 170.
