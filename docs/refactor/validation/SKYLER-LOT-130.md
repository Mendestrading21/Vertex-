# SKYLER V2 — LOT 130 : passe n°5 — fiche Analyse (performance multi-horizons en verre) + mini-bilan

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-130`
(base : `integration/vertex-skyler-v2` @ `5ec562e`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
analysis_page.py + SW + gardiens + docs.

## 1. Diagnostic (capture AVANT, /analysis/ACN)

Tour de la fiche Analyse (la page où l'utilisateur passe le plus de
temps) : radar (verre 122), chandeliers + plan (lot 54), runway (119),
timeline HTML et price-chart déjà au niveau. Le bloc encore PLAT :
« Performance multi-horizons » (1 sem./1 mois/1 trim./1 an) — barres
pleines uniformes depuis le centre.

## 2. Amélioration (perfBars, analysis_page.py)

```text
matière VERRE : chaque barre est un dégradé de sa propre couleur,
  doux au CENTRE (zéro) → dense à l'extrémité de la valeur — même
  grammaire que C.bars (lot 125)
dégradé construit par color-mix(in srgb, token 35 %, transparent)
  sur var(--vx-positive/negative) — AUCUN littéral couleur nouveau
coins arrondis 2px sur le remplissage · axe zéro et étiquettes
  tabulaires inchangés · aria-label par barre inchangé
```

SW `td-shell-v138` → `td-shell-v139` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v139)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (fiche ACN)
```

## 4. Mini-bilan 126-130 (chiffres vérifiés dans les rapports)

5 lots, suite constante 1984/2, PR #159 → #163, SW v134 → v139 :
jauge verre + kv protégés + badge adaptatif (126) · heatmaps verre
sur tokens (127) · donut à chiffre central (128) · rails sémantiques
rétablis + taux cyan + anti-collision (129) · multi-horizons verre
(130). Deux BUGS visuels réels tués au passage : les stats collées
« Trades3 » (125-126) et les rails invisibles (129).

## 5. Suite

LOT 131 : passe n°6 (candidats : Portefeuille vues secondaires,
Options desk, vues Opportunités restantes).
