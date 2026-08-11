# SKYLER V2 — LOT 154 : caractérisation classification & pipeline d'actualités

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-154`
(base : `integration/vertex-skyler-v2` @ `a4207d0`, lot 153 fusionné).
Lot TESTS uniquement, aucun code moteur ni UI modifié. Deux modules
zéro-test combinés (servis par daily_brief, §15).

## 1. Cibles

`vertex/market/news_impact.py` (61 lignes) — classement par
mots-clés déterministes + score d'importance + direction POTENTIELLE
(jamais une causalité affirmée). `vertex/market/news_pipeline.py`
(51 lignes) — normalisation/validation : titre + source + heure
requis, rejets COMPTÉS jamais masqués, dédup, tri. Note sécurité :
ces modules ne produisent pas de HTML — l'assainissement XSS reste
chez news_plus.sanitize_news() (déjà couvert, 34 tests).

## 2. Ce qui est figé (`tests/test_news_impact_pipeline_lot154.py`, 20 tests)

```text
classify — priorité du PREMIER match (MACRO gagne sur RESULTATS
  dans un titre mixte), les 5 catégories + défaut ENTREPRISE,
  titre None/vide → ENTREPRISE ; LIMITE DOCUMENTÉE : matching par
  SOUS-CHAÎNE (pas par mot entier) — le mot-clé 'ai' matche dans
  « mountain »/« rain » → SECTEUR ; passer aux frontières de mots
  = décision explicite
score_importance — arithmétique EXACTE : base 30, corroborations
  +10/unité plafonnées +30, portefeuille +25, MACRO/POLITIQUE +10,
  RESULTATS/GUIDANCE +15, |sentiment| ≥ 0.5 → +5, plafond 100
potential_impact — seuils EXACTS ±0.15 (0.15 NEUTRE, 0.16
  POSITIF_POTENTIEL), confiance plafonnée 0.7 (humble), sentiment
  illisible → INCONNUE 0.0
pipeline.collect — rejets COMPTÉS (titre vide, sans source/heure,
  non-dict → rejected 3, jamais masqués) ; doublon fusionné en
  corroborations 2 → importance 80 recomposée ; sym normalisé
  MAJUSCULES ; fr vide → None honnête ; tri importance
  décroissante ; état vide → contrat honnête {[], 0, 0, None}
```

## 3. Preuves

```text
python -m pytest tests/test_news_impact_pipeline_lot154.py -q → 20 passed
python -m pytest tests/ -q → 2161 passed, 2 skipped (2141 + 20)
Aucun changement UI → pas de bump SW (v151 courante)
```

## 4. Suite

LOT 155 : `vertex/market/editorial.py` (202 l, ratio 0.34) OU
`vertex/quant/scoring.py` (140 l, 0.59) + MINI-BILAN 151-155
obligatoire.
