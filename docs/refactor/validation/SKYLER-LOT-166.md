# SKYLER V2 — LOT 166 : caractérisation de la couche IA optionnelle (briefs)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-166`
(base : `integration/vertex-skyler-v2` @ `3280552`, lot 165 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié.

## 1. Cible

`vertex/ai/briefs.py` (178 lignes, ratio 0.33) — la couche IA
OPTIONNELLE : traduction FR des news, mini-profils d'entreprise,
libellés/descriptions. Dégradation propre sans clé (IA Anthropic →
Google gratuit → texte d'origine). Testée entièrement HORS LIGNE :
`_google_fr` monkeypatché selon son contrat (« None si échec »),
aucun appel Anthropic ni Google réel.

## 2. Ce qui est figé (`tests/test_ai_briefs_lot166.py`, 10 tests)

```text
available — la clé doit être RÉELLE : absence, placeholder
  (sk-ant-xxxx…) et mauvais préfixe REJETÉS ; vraie forme acceptée
fr_news sans clé — repli Google avec CACHE (mêmes titres → aucun
  second appel) ; DÉSALIGNEMENT de lignes (1 réponse pour 2
  titres) → titres ANGLAIS d'origine (fidélité > traduction) ;
  échec réseau → titres d'origine, why None ; liste vide intacte
company_brief — sans résumé OU sans clé → {} (dégradation propre,
  jamais un profil inventé)
fr_label — traduit + CACHÉ (1 seul appel) ; échec → libellé
  d'origine ; vide intact
fr_desc — Google OK → traduction ; échec → texte d'origine
  (jamais perdu) ; vide intact
_google_fr('') → None
```

## 3. Preuves

```text
python -m pytest tests/test_ai_briefs_lot166.py -q → 10 passed
python -m pytest tests/ -q → 2281 passed, 2 skipped (2271 + 10)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 167 : ai/copilot.py (159 l, 0.37 — lacunes seulement, 5 tests
existants) OU data/company.py (340 l, 0.39) OU legacy_adapter
(272 l, à découper). Mini-bilan 166-170 au lot 170.
