# SKYLER LOT 208 — Inventaire mesuré de cohérence : divergences toutes justifiées, 0 retouche

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-208` (base : lot 207 fusionné)

## Livré

### Inventaire mesuré (script d'analyse des builders charts + pages)

Balayage de `vertex/static/vertex/js/charts/*.js` +
`vertex/static/vertex/js/pages/*.js` sur 4 axes.

| Axe | Constat | Verdict |
|---|---|---|
| **Police des chips** | `tvEdgeChip` : fontSize **9 partout** (cône, runway, radar, treemap). Chips canvas : **700 9px uniformes** (tvExtremes, levelLines, barres dominantes). Libellés de zones payoff/GEX : 8.5 (viewBox denses 520-560). Le « 11 » de candlestick-lwc est la config d'AXES de Lightweight Charts, pas un chip (faux positif de grep). | JUSTIFIÉ |
| **Densités de hachures** | SVG `tvHatch` : tuile 6, fill .08, stroke .38 w1.6 · canvas `hatchPattern` : tuile 8, fill .08, stroke .38 w1.4. Alphas IDENTIQUES ; tuile/épaisseur légèrement différentes = équivalence visuelle voulue entre coordonnées userSpace SVG et pixels canvas. | JUSTIFIÉ |
| **Rayons/hauteurs de chips** | rx 3 (tvEdgeChip h~17), rx 6 (GEX h12), r 7 (canvas h14), r 8 (pilule h16) — tous ≈ h/2, coins pleinement arrondis cohérents. Les rx 128/92 de regime-aura sont les ellipses du halo, le rx 4 du runway la zone ≤5 j (faux positifs). | JUSTIFIÉ |
| **Pieds de cartes** | Trois classes, trois RÔLES distincts : `vx-chart-foot` = pied de carte graphique (porte updateIndicator/fraîcheur), `vx-meta` = note contextuelle, `vx-muted` = texte secondaire. L'unique `vx-card-footer` (options-structure) est le pied standard du design system. Pas une divergence — une sémantique. | JUSTIFIÉ |

### Verdict : AUCUNE retouche

Toutes les divergences relevées sont soit justifiées par le support
(SVG vs canvas, densité du viewBox), soit des faux positifs du grep
(config d'axes, titres, halos). Une « harmonisation » serait un
changement gratuit — risque sans gain, contraire à la discipline des
lots. L'option 2 de la proposition du lot 205 est SOLDÉE par constat.

## Accros

Aucun. AUCUN code touché, AUCUN bump SW.

## Preuves

- Sortie du script d'inventaire (tableau ci-dessus) ; vérification
  ciblée du seul point suspect (fontSize 11 → config LWC L92).
- Suite complète : **2461 passed / 2 skipped** (inchangée).

## Suite

LOT 209 : lot d'entretien (gardiens/honnêteté/petites dettes — ex.
aria-hidden du drawer noté au lot 206) sauf directive utilisateur.
MINI-BILAN 206-210 au lot 210.
