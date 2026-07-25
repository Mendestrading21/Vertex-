# RECONSTRUCTION 01 — AUJOURD'HUI (widgets validés, en live)

> Le Widget Lab est **figé** : source de vérité design. Première page reconstruite
> avec **uniquement des widgets validés**, câblés aux **vraies données**, moteurs
> et calculs **intacts**, IBKR **READONLY**. Architecture retenue (validée) :
> **recomposer en live** — on garde le système produit (shell serveur + squelette
> + hydratation client `VXCharts` / Neon Glass Orange), on n'y met que des objets
> validés, alignés sur leurs designs. Aucun SVG serveur figé, aucun CSS `.wl`
> importé. Aujourd'hui **RÉSUME**, Marchés **explique**.

## 1. Objets validés réalisés en live

Deux objets décisionnels du jour (contrats `CONTRACTS`, domicile « Aujourd'hui ») :

- **Regime Aura (W01)** — `VXCharts.regimeAura` (`charts/regime-aura.js`). Halo
  atmosphérique coloré par l'état, arc de confiance (orange Ember), grammaire
  boursière (Marché RISK-ON/OFF · Breadth >MM200 · VIX) et verdict
  « Risque neuf autorisé / BLOQUÉ » + invalidation. Remplace la jauge générique.
- **Catalyst Runway (W-CR)** — `VXCharts.catalystRunway` (`charts/catalyst-runway.js`).
  Piste de décollage : chaque catalyseur posé selon son **DTE**, coloré par
  impact, prochain événement priorisé + conclusion. Remplace la timeline générique.

Les deux builders suivent le style des builders SVG existants de `chart-core.js`
(`gauge`/`rings`/`radar`) : injection `innerHTML`, couleurs via tokens `--vx-*`
(aucun littéral), états honnêtes (`VX.states.empty/error`), pied de source
(`VX.updateIndicator`). Glow réservé au point actif.

## 2. Câblage aux vraies données (aucun calcul ajouté)

| Objet | Champ UI | Source réelle (moteur, inchangé) |
|---|---|---|
| Regime Aura | régime + confiance | `/api/market/regime` → `regime`, `confidence` |
| | risque neuf | `/api/market/regime` → `adjustments.new_risk_allowed` |
| | invalidation | `/api/briefing/editorial` → `main_risk` |
| | grammaire | `/api/market/summary` → `roro`, `breadth.above200`, `vix` |
| | confirmations | `/api/market/regime` → `adjustments.confirmation_required` |
| Catalyst Runway | events (label/DTE/impact) | `/cal-feed` → `macro[]` + `items[]` (earnings) |
| KPI résumé | Régime/Breadth/VIX/best opp | summary + `/api/command` `top_stocks[0]` |

Donnée absente → **état honnête** (`Régime indéterminé — Vertex ne tranche pas.`,
`Aucun catalyseur imminent identifié.`). Aucun chiffre inventé.

## 3. Invariants préservés (gardiens verts)

Conservés dans `briefing.py` : `vx-hero`, `loadSummary`, `vx-diff`, `kpiTile`,
`kpiTile('VIX',vixHtml,''` (VIX sans couleur directionnelle), `Aucun historique
de comparaison disponible`, `vx-demo-banner`, `states.empty/error`, `source:` sur
tout builder. `build_editorial()` inchangée (deterministic, ≤12 lignes dont
« Discipline »). **Jamais réintroduit** : `VXCharts.gauge`/`timelineCard`/
`vx-regime-gauge`/`loadPulse`/`vx-market-chart`/`VXCharts.breadthCard`/
`loadRotation`/`#8f8a83`/verbe d'ordre. Style neon-glass **scopé
`[data-space="briefing"]`**.

## 4. Validation

- `python -m compileall -q terminal.py vertex` → exit 0.
- `python -m pytest tests/ -q` → **991 passed, 2 skipped** (985 baseline + 6
  gardiens `test_reconstruction_today.py` ; cockpit/ui_v3/neon_glass/redesign verts ;
  SW `td-shell-v54` → **v55** répercuté dans les 3 tests qui l'épinglent).
- Navigateur (`DEMO=1 NO_IBKR=1`) **1440 & 390** : page sans débordement réel
  (`scrollWidth == viewport`), Regime Aura + Catalyst Runway rendus et câblés,
  états honnêtes (portefeuille vide assumé), bannière démo étiquetée. *(Les seuls
  signaux résiduels sont environnementaux et pré-existants sur toutes les pages :
  le drawer `position:fixed` hors-écran, et le CDN Google Fonts bloqué par le
  proxy du bac à sable — non liés à cette reconstruction.)*
- Captures : `today-desktop.png`, `today-mobile.png`.
- Diff limité à : `briefing.py`, `charts/regime-aura.js`, `charts/catalyst-runway.js`,
  `neon-glass.css`, `system.py` (SW v55), 4 fichiers de tests, ce rapport. **Aucun
  moteur / calcul / route API / contrat de données touché. READONLY intact.**

## 5. Limites / suite

- W01 expose « SPX vs MM200 » au contrat ; aucun champ réel propre ne le fournit
  → remplacé honnêtement par la chip **Marché (RORO)**, donnée réelle disponible.
- Breadth / VIX gardent leur **domicile** sur Marchés (Aujourd'hui = tuiles-résumé
  + liens) — invariant « une donnée = un seul domicile ».
- **Data Integrity Reactor (W68)** reste sur Système (son domicile) ; la confiance
  données sur Aujourd'hui passe par les badges de fraîcheur existants.
- Prochaine page de la roadmap : **Marchés** (déjà premium — alignement sur les
  objets validés Regime Aura / Breadth Field / Volatility Cone / Rotation), après
  validation humaine.

## Verdict

Aujourd'hui est reconstruit avec **uniquement des widgets validés**, réalisés en
**live** sur les **vrais moteurs**, sans toucher un seul calcul. Regime Aura et
Catalyst Runway remplacent les composants génériques ; le résumé (hero, KPI, diff,
opportunités, alertes, portefeuille) est préservé et aligné. **991 tests verts ·
0 débordement réel · états honnêtes · READONLY · aucune donnée inventée.**
**Arrêt pour validation humaine.**
