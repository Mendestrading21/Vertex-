# TOURNÉE GRAPHIQUE TV — INVENTAIRE DES GRAPHIQUES VIVANTS (lot 189)

Directive utilisateur (lot 188) : refaire TOUS les graphiques de
Vertex au langage visuel TradingView — jauges dégradées à aiguille,
cône de projection, consensus, zones d'estimation hachurées, doubles
axes annotés. Un ou deux graphiques par lot, protocole UI complet.
Statuts : ☐ à faire · ◐ partiel · ✔ refait TV.

## Grammaire commune (chart-core.js) — ✔ lot 189

- `C.gauge` ✔ : arc DÉGRADÉ continu (couleurs des bandes fondues),
  pointeur blanc court sur l'arc, libellés de zones, état coloré.
- `C.tvHatch(id,color)` ✔ : pattern SVG hachuré = « estimation ».
- `C.tvEdgeChip(x,y,text,color)` ✔ : chip d'étiquette de bord
  (Max/Moy/Min/Actuel) pour le cône et les échelles.

## Par page (ordre de visibilité produit)

### Aujourd'hui (briefing.py)
- ✔ lot 192 : regimeAura aligné grammaire TV — arc de confiance en
  dégradé continu de tonalité + pointeur blanc court (langage C.gauge)
- ✔ lot 193 : catalystRunway — piste DTE en dégradé continu
  (rouge→jaune→éteint), zone ≤ 5 j hachurée (tvHatch), chip tvEdgeChip
  J-x sur le prochain catalyseur
- ☐ sparklines des tuiles KPI (chart-core sparkline)

### Marchés (markets_page.py)
- ✔ jauge régime/confiance · jauge breadth (>MM50) · jauge VIX
- ☐ aires indices (line-area) + série de référence 120 séances
- ✔ lot 194 : heatmap (builder partagé) — texte des cellules coloré
  par intensité + cellule dominante en évidence (hérite : secteurs
  Marchés, P&L mensuel Portefeuille, scénarios/IV Options)
- ☐ barres leadership
- ☐ bandes CALME↔STRESS / DÉFENSE↔ATTAQUE (linéaires — déjà
  dégradées, à aligner sur la grammaire chip/aiguille)

### Analyse (analysis_page.py + options-intel.js)
- ☐ price-chart (chandeliers lightweight-charts + niveaux)
- ✔ lot 190 : CÔNE DE PROJECTION du plan de trade (projection-cone.js, branché dans an-plan)
  (entrée/stop/TP1-3 du moteur → éventail min/moy/max avec
  tvEdgeChip, style prix cible TV — données RÉELLES du plan, jamais
  un consensus inventé)
- ☐ radar de scores · jauge environnement options (options-intel)
- ☐ vol cone / IV term structure (vol_charts)

### Portefeuille (portfolio_page.py)
- ✔ jauge risque (pf-risk-gauge)
- ✔ lot 194 : treemap — part du total en chip tvEdgeChip pleine
  couleur sur les grandes tuiles
- ☐ equity curve (equity-chart) · drawdown
- ☐ barres S+/S/A/B (concentration)

### Options (options_intel_page.py)
- ✔ lot 192 : payoff (option-payoff) — zones GAIN/PERTE hachurées
  (équivalent canvas du tvHatch) + libellés de zones au breakeven
- ☐ scénarios (option-scenarios) · théta (option-theta) ·
  sensibilité IV (option-iv-sensitivity)
- ☐ GEX (barres par strike) · double probabilité

### Journal (journal pages)
- ☐ barres de discipline · stats comportementales

### Intelligence (intelligence_page.py)
- ☐ jauge comité (vx-committee-gauge — hérite déjà du ✔ C.gauge)
- ✔ lot 191 : barres de consensus du comité (consensus-bars.js —
  verdicts RÉELS en FR via __VXVOCAB désormais injecté par le shell)

### Système (system_page.py)
- ✔ jauge santé (vx-sys-gauge — hérite du C.gauge)
- ☐ barres de fraîcheur par domaine (staleness)

## Prochains lots proposés
1. Lot 190 : cône de projection du plan (Analyse) + zones hachurées
   sur les aires de prévision — les deux signatures TV les plus
   fortes. + MINI-BILAN 186-190.
2. Lot 191 : barres de consensus comité (Intelligence) + regimeAura
   aligné (Aujourd'hui).
3. Lot 192+ : payoff hachuré, treemap, equity/drawdown, heatmap,
   GEX, sparklines, discipline.
