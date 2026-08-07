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
- ✔ lot 200 : série de référence 120 séances — chips Max/Min sur les
  extrêmes RÉELS (passthrough `extremes` de areaCard) + pilule
  dernière valeur (déjà héritée)
- ✔ lot 194 : heatmap (builder partagé) — texte des cellules coloré
  par intensité + cellule dominante en évidence (hérite : secteurs
  Marchés, P&L mensuel Portefeuille, scénarios/IV Options)
- ✔ lot 199 : barres (C.bars partagé) — dominante en évidence :
  liseré appuyé + valeur en chip pleine couleur (héritent : leadership,
  S+/S/A/B, discipline, movers, recherche, sensibilité IV)
- ✔ lot 198 : bandes CALME↔STRESS / DÉFENSE↔ATTAQUE — chip de valeur
  RÉELLE sur le pointeur (.vx-rail-chip réutilisable ; VIX réel,
  confiance % — « n/d » honnête sur régime indéterminé)

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
- ✔ lot 195 : equity curve + drawdown — chips Max/Min sur les
  extrêmes RÉELS (C.tvExtremesPlugin, opt-in `extremes` de C.area ;
  drawdown = chip Min seul, le pire creux)
- ☐ barres S+/S/A/B (concentration)

### Options (options_intel_page.py)
- ✔ lot 192 : payoff (option-payoff) — zones GAIN/PERTE hachurées
  (équivalent canvas du tvHatch) + libellés de zones au breakeven
- ✔ lot 197 : théta (option-theta) — aire HACHURÉE (hatch de C.area,
  la projection modèle assume sa texture) + chip Min
- ✔ lot 197 : scénarios (option-scenarios) — par HÉRITAGE de la
  heatmap TV lot 194 (constaté en navigateur)
- ✔ lot 199 : sensibilité IV — par HÉRITAGE du C.bars TV (barre
  dominante : liseré appuyé + valeur en chip, constaté en navigateur)
- ☐ GEX (barres par strike) · double probabilité

### Journal (journal pages)
- ✔ lot 200 : barres de discipline/stats — par HÉRITAGE structurel du
  C.bars TV lot 199 (appels directs VXCharts.bars, chemin unique)

### Intelligence (intelligence_page.py)
- ☐ jauge comité (vx-committee-gauge — hérite déjà du ✔ C.gauge)
- ✔ lot 191 : barres de consensus du comité (consensus-bars.js —
  verdicts RÉELS en FR via __VXVOCAB désormais injecté par le shell)

### Système (system_page.py)
- ✔ jauge santé (vx-sys-gauge — hérite du C.gauge)
- ✔ lot 196 : fraîcheur par domaine — le plus rassis en DOMINANTE
  (tuile liserée + âge en chip pleine couleur), les autres adoucis

## Prochains lots proposés
1. Lot 190 : cône de projection du plan (Analyse) + zones hachurées
   sur les aires de prévision — les deux signatures TV les plus
   fortes. + MINI-BILAN 186-190.
2. Lot 191 : barres de consensus comité (Intelligence) + regimeAura
   aligné (Aujourd'hui).
3. Lot 192+ : payoff hachuré, treemap, equity/drawdown, heatmap,
   GEX, sparklines, discipline.
