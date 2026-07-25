# WIDGET LAB — FINANCE NATIVE PASS 03

> La base Art Direction Pass 02 est validée. Cette passe rend chaque widget
> **immédiatement lisible comme un objet de marché financier** : grammaire
> boursière native (prix, %, plage, entrée/stop/objectif, volume, volatilité,
> percentile, RS, OI, spread, DTE, drawdown), **formes propriétaires Vertex**
> (chandeliers, price ladder, market tape, order-flow ribbon, volatility cone,
> relative-strength path, risk/reward terrain, breadth field, liquidity depth,
> correlation web, earnings gap map, S/R spine, catalyst runway), une **question
> de trading** et une **conclusion de décision** par widget, et une densité
> **institutionnelle en 3 couches** (réponse / preuve / détail au survol).
> **Aucune page produit touchée. Aucun moteur modifié. Uniquement /widget-lab.**
> Route autonome, aucune donnée réelle, READONLY.

## 1. Objectif atteint — reconnaissable comme objet financier sans titre ni logo

Retirez le titre, l'id, l'orange : un **chandelier + volume + MM + niveaux
entrée/stop/objectif**, un **cône de volatilité**, une **échelle de prix avec
distances en %**, un **bandeau de tickers**, une **toile de corrélations** se
reconnaissent **immédiatement** comme des objets de bourse. Chaque widget porte
désormais la grammaire du marché, pas une abstraction jolie.

**Test de reconnaissance** (sans titre/id/orange) : Candlestick Snapshot,
Volatility Cone, Price Ladder, Market Tape, Order-Flow Ribbon, Relative-Strength
Path, Risk/Reward Terrain, Liquidity Depth, Earnings Gap Map, Market Breadth
Field, Correlation Web → **tous identifiés comme financiers**. ✔

**Test de décision** : chaque widget répond à une **question de trading** et
délivre une **conclusion actionnable** (`▸` entrer / attendre / éviter /
surveiller / conserver / réévaluer / risque élevé / données insuffisantes).

## 2. Grammaire boursière native (briques financières)

Trois primitives partagées, appliquées à tous les nouveaux objets :

- `_hdr(nom, prix, %)` — en-tête : **ticker + prix + variation** en tabular-nums.
- `_concl(texte, ton)` — **conclusion de décision** colorée (go/risk/wait/opt).
- `_foot(source, fraîcheur, mode)` — **source · fraîcheur · mode** (live/delayed/
  demo) avec pastille — honnêteté §7 (donnée absente → `n/d`, jamais inventée).

Vocabulaire natif injecté : **prix, %, plage, entrée, stop, objectif, résistance,
volume, MM5/10/20/50/200, volatilité implicite, percentile, benchmark, RS,
spread, bid/ask, OI, A/D, nouveaux hauts/bas, DTE (J-n), drawdown, R:R,
invalidation**.

## 3. Formes financières signature implémentées (SVG/CSS réels) — 16

| Widget | Objet de marché | Réponse |
|---|---|---|
| **Candlestick Snapshot** | chandeliers + volume + MM + niveaux + gap + événement + bougie active | cassure confirmée ? |
| **Candlestick — Indice** | même moteur, sans plan (indice) | l'indice tient sa plage ? |
| **Candlestick — Carte compacte** | mini-chandeliers format carte | aperçu prix instantané |
| **Price Ladder** | échelle de prix : niveaux + distances % | où sont entrée/stop/objectifs ? |
| **Market Tape** | bandeau de flux : tickers · % · volume (défilant) | que fait le marché maintenant ? |
| **Order-Flow Ribbon** | pression acheteurs/vendeurs + déséquilibre | qui domine ? |
| **Volatility Cone** | vol actuelle vs enveloppe historique + percentile | la vol est-elle chère ? |
| **Relative-Strength Path** | actif vs benchmark : accélération/divergence | surperforme-t-il ? |
| **Risk/Reward Terrain** | perte max / gain probable / exceptionnel + BE | asymétrie favorable ? |
| **Position Health Strip** | P&L · thèse · catalyseur · invalidation · action | position en bonne santé ? |
| **Market Breadth Field** | champ de participation + A/D + hauts/bas | hausse partagée ? |
| **Liquidity Depth** | bid/ask · spread · volume · OI · exécution | puis-je exécuter proprement ? |
| **Market Correlation Web** | corrélations entre actifs (hub SPX) | mes actifs bougent ensemble ? |
| **Earnings Gap Map** | historique des gaps post-résultats | réaction violente aux résultats ? |
| **Support/Resistance Spine** | colonne de niveaux techniques | quels niveaux encadrent le prix ? |
| **Catalyst Runway** | piste de décollage : DTE + impact | quel catalyseur, quand ? |

Les **chandeliers ne sont PAS réservés à Analyse** : présents en Analyse,
Marchés (indice) et Opportunité (carte compacte).

## 4. Densité institutionnelle en 3 couches

Chaque objet financier suit la lecture de bureau :

1. **Réponse** (< 1 s) : header prix/% + conclusion `▸`.
2. **Preuve** (2–3 s) : le graphe/relief + niveaux chiffrés.
3. **Détail au survol** (`.wl-more`, `.wl-tip`) : MM, volume, gap, A/D,
   percentile, spread, OI — révélé au hover, jamais dans le premier écran.

Exemple d'enrichissement d'un widget existant : **Regime Aura V1** porte
désormais la grammaire (SPX > MM200 · Breadth 63 % · VIX 14,6), une conclusion
(« Régime porteur — risque neuf autorisé, invalidation SPX < MM50 5 780 ») et un
détail RS/A-D au survol.

## 5. Palettes financières (sémantique, pas décoration)

Vert émeraude = haussier/gagnant ; rouge = baissier/perte ; ambre = attente/
résistance ; violet = volatilité/convexité (options) ; cyan = force relative/
information ; vert citron = momentum. **Orange Ember réservé** à identité,
sélection, prix actif, ligne d'entrée, bougie active. **Aucun bleu identitaire**
(gardien vérifié).

## 6. États honnêtes

Bande d'états par bench : loading · empty · **insufficient** (« Données
insuffisantes — Vertex ne tranche pas ») · stale · demo · live · offline · error.
Les widgets financiers portent des états cohérents (chandeliers → insufficient/
stale ; order-flow → live ; catalyseurs → stale).

## 7. Chiffres & tests

- **60 widgets** (benches), **14 familles**, **16 formes financières signature**
  nouvelles, **≥ 20 widgets clairement financiers** (test gardien
  `test_finance_grammar_present`).
- `python -m compileall -q terminal.py vertex` → exit 0.
- `python -m pytest tests/ -q` → **973 passed, 2 skipped** (baseline 971
  maintenue + 2 gardiens P03 : ≥ 60 widgets, formes financières présentes,
  grammaire de décision).
- Navigateur **1440 & 390** : **0 débordement de page, 0 débordement d'élément,
  0 erreur console** (`val.py`).
- Chandeliers, cône, échelle, bandeau, ribbon, terrain, strip, field, depth, web,
  gaps, spine, runway : tous rendus.

## 8. Captures (évidence de session)

`lab3-desktop.png` (page complète 1440), `lab3-mobile.png` (390),
`lab3-candles.png` (Candlestick Snapshot V1/V2 + états), `lab3-mobilepreview.png`
(toggle aperçu mobile).

## 9. Limites restantes / différé

- **Vraie version mobile dédiée par widget complexe** : aujourd'hui reflow +
  défilement contrôlé + header compact ; le repli container-query du détail
  secondaire par widget reste à approfondir sur les objets les plus denses
  (Correlation Web, Payoff Terrain).
- **Encore un peu génériques** (à re-spécifier P04) : Selection Funnel, Bias
  Heatmap, Progress Ladder (Journal) — corrects mais moins « marché » que les
  objets de prix.
- **Non encore rendus** (spécifiés) : Capital Flow Stream, Institutional
  Footprint, Volatility Term Rift 3D, LEAPS Compatibility, Sector Rotation Orbit
  V2.
- Le lab reste un **catalogue** : la sélection Officiel/Référence/Rejeté + export
  permet de graver les choix avant reconstruction des pages produit.

## Verdict

Le laboratoire passe de « premium abstrait » à **finance native** : chaque objet
se lit comme un instrument de bureau de marché, avec grammaire boursière,
question de trading et conclusion de décision. **60 widgets · 16 formes
financières signature · ≥ 20 clairement financières · 973 tests verts · 0
débordement · 0 erreur console · READONLY · aucune donnée inventée.** **Arrêt
pour validation humaine.** Dis-moi les widgets à graver (Officiel/Référence/
Rejeté via Exporter) et ceux encore trop génériques à repousser.
