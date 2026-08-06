# SKYLER V2 — LOT 120 : amélioration graphique n°2 — lignes ultra propres (Marchés) + mini-bilan 116-120

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-120`
(base : `integration/vertex-skyler-v2` @ `6531929`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE utilisateur : chaque graphique le plus propre et
le plus beau possible — dégradés pros, pas de chiffres empilés.**
Moteurs INTACTS — diff = chart-core.js + bump SW + gardiens + docs.
(Lot démarré immédiatement sur message utilisateur, sans attendre le
réveil — le réveil arrivera en doublon.)

## 1. Diagnostic (capture AVANT, /markets)

« Indices — performance comparée » : 4 traits épais uniformes, deux
séries quasi identiques visuellement, identité seulement par la légende
éloignée en bas. « Série de référence » : dégradé à 3 arrêts un peu
plat, trait 2 px.

## 2. Améliorations (vertex/static/vertex/js/charts/chart-core.js)

```text
C.endDotsPlugin — chaque série se termine par un POINT NET dans sa
  couleur (halo léger) + son NOM court collé au bout de la ligne :
  l'œil suit une courbe jusqu'à son identité, sans aller-retour
  avec la légende (padding droit 54 pour la place)
C.softGlowPlugin — halo néon très doux sous chaque trait (blur 4) :
  la matière Neon Glass sans bruit
C.multiLine — traits AFFINÉS 2 → 1.6 px, plugins de finition branchés
C.area — dégradé vertical 4 ARRÊTS (59→2E→12→00) : descente plus
  douce, jamais un aplat · trait 2 → 1.8 px
Bénéfice transversal : multiLine/area servent Marchés, Analyse,
  Portefeuille, Options — toutes les pages héritent de la finition
Aucun littéral couleur nouveau · gardien lot 52 mis à jour vers la
  nouvelle signature (1.6 + endDots + softGlow — changement délibéré)
```

SW `td-shell-v128` → `td-shell-v129` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v129)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées à l'utilisateur
```

## 4. MINI-BILAN tournée 116-120 (chiffres vérifiés dans les rapports)

```text
5 lots · 24 tests + 2 lots graphiques · suite 1960 → 1984 / 2 skipped
116 event_engine (8)     non confirmé jamais actionnable
117 factory (8)          un beau backtest ne suffit jamais
118 chart_read (8)       la méfiance prime sur l'enthousiasme
119 GRAPHIQUE Aujourd'hui  Catalyst Runway développé (zone ≤ 5 j,
                         impact dimensionné, anneau) · SW v128
120 GRAPHIQUE Marchés    lignes ultra propres (traits fins, halo,
                         points terminaux nommés, dégradé 4 arrêts) ·
                         SW v129
0 défaut moteur · 2 sondes corrigées au 118 (dites) · pivot de la
boucle vers l'esthétique sur directive utilisateur (lots 119+) ·
PR #149 → #153 · skyler_core 0.9.0 intact.
```

## 5. Suite

Lot 121 : amélioration graphique n°3 (Opportunités) — même directive
esthétique, chaque page au maximum.
