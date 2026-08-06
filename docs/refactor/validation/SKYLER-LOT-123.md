# SKYLER V2 — LOT 123 : amélioration graphique n°5 — treemap matière verre (Portefeuille)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-123`
(base : `integration/vertex-skyler-v2` @ `9674332`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
chart-core.js + SW + gardiens + docs.

## 1. Diagnostic (capture AVANT, /portfolio)

Le treemap « Allocation & concentration du capital » : rectangles GRIS
PLATS uniformes (marques IBKR hors ligne → neutre honnête, mais un
aplat morne), gros trait noir de séparation, aucune profondeur, pas de
part du total lisible.

## 2. Améliorations (C.treemap, chart-core.js — tous les treemaps héritent)

```text
matière VERRE : chaque tuile est un dégradé DIAGONAL de sa propre
  couleur (dense en haut-gauche 90 % → doux en bas-droit 45 %) —
  même le neutre honnête gagne de la profondeur
liseré FIN de la couleur de la tuile (au lieu du trait noir épais),
  coins arrondis 5
part du TOTAL (%) affichée en haut-droit des grandes tuiles — LE
  chiffre éducatif du treemap (et il entre dans l'aria-label)
id de dégradé unique par hôte+tuile (aucune collision)
aucun littéral couleur nouveau — les couleurs viennent des données
  (émeraude gagnant / corail perdant / neutre sans marque, inchangé)
```

SW `td-shell-v131` → `td-shell-v132` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v132)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées à l'utilisateur
```

## 4. Suite

Lot 124 : amélioration graphique n°6 (Options) ; lot 125 = n°7
(Journal) + mini-bilan 121-125.
