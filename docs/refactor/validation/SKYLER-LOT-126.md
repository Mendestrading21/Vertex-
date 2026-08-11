# SKYLER V2 — LOT 126 : amélioration graphique n°8 — Système (jauge verre + lisibilité)

Date : 2026-08-06 · Branche : `agent/skyler-v2-lot-126`
(base : `integration/vertex-skyler-v2` @ `406b514`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE — 8e et dernière page de la 1re tournée.**
Moteurs INTACTS — diff = chart-core.js + utilities.css + system_page.py
+ SW + gardiens + docs.

## 1. Diagnostic (capture AVANT, /system)

Trois défauts : (a) la jauge « Santé — Moteurs » (`C.gauge`) : arc plat
uniforme, aucun matière ; (b) libellés clé/valeur ÉCRASÉS par les
valeurs longues (« Ét at », « Rô le », « Éta t » — le libellé se cassait
au milieu d'un mot) ; (c) badge `CONFIGURATION_MISSING` qui débordait
de sa colonne fixe 130px sur le texte voisin.

## 2. Améliorations

```text
C.gauge matière VERRE (chart-core.js — toutes les jauges héritent :
  Santé moteurs, Participation Marchés…) : l'arc de valeur est un
  dégradé de sa propre couleur (doux au départ → dense à l'extrémité,
  même grammaire que les barres du lot 125), posé sur un halo large
  et léger ; le point de lecture gagne son halo ; id de dégradé
  unique par hôte
.vx-kv .k (utilities.css) : le libellé garde sa largeur NATURELLE
  (≤ 55 %) — c'est la valeur qui replie, plus jamais « Ét at » ;
  le gardien lot 57 (jamais d'ellipse, jamais nowrap) est respecté
canaux (system_page.py) : colonne du badge en minmax(110px,
  max-content) — CONFIGURATION_MISSING s'affiche entier
uniquement des tokens — AUCUN littéral couleur nouveau
```

SW `td-shell-v134` → `td-shell-v135` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v135)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées
```

## 4. Suite

Première tournée graphique TERMINÉE (8 pages / 8). LOT 127 : nouvelles
passes — widgets Options avancés (scénarios, theta, IV sensitivity).
