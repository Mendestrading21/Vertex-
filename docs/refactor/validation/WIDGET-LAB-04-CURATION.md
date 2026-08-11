# WIDGET LAB — CURATION & SIGNATURE PASS 04

> Finance Native P03 validée. Cette passe ne fait **plus grossir** la
> bibliothèque : elle la **trie**. Audit qualitatif des 60 widgets sur 10
> critères, **15 objets officiels** (un par domaine structurant), 20 références,
> 20 à retravailler, 5 rejetés — **aucun widget non classé**. Trois widgets
> faibles refondés, contrats normalisés, registre officiel, export enrichi.
> **Aucune page produit touchée. Aucun moteur modifié. Uniquement /widget-lab.**
> Préférence assumée : **15 widgets exceptionnels > 60 corrects.**

## 1. Méthode d'audit

Chaque widget noté /100 sur 10 critères (10 pts chacun) : reconnaissable sans
titre · immédiatement financier · lisible < 3 s · répond à une vraie question
d'investissement · plus utile qu'un graphe classique · forme mémorable ·
hiérarchie claire · mobile viable · états honnêtes élégants · candidat officiel.
Seuils : **OFFICIEL ≥ 90 · RÉFÉRENCE 80-89 · À RETRAVAILLER 65-79 · REJETÉ < 65**.
Scores non gonflés — la classification vit dans le code (`CURATION` de
`widget_lab.py`), rendue en badge sur chaque bench + bandeau récapitulatif, et
gardée par test (`test_curation_every_widget_classified`, `_caps_and_distribution`).

## 2. Résultat global

| Statut | Nombre | Plafond |
|---|---|---|
| ◎ OFFICIEL | **15** | ≤ 15 |
| ★ RÉFÉRENCE | **20** | ≤ 20 |
| ◐ À RETRAVAILLER | **20** | — |
| ✕ REJETÉ | **5** | — |
| **Total classé** | **60 / 60** | aucun non classé |

## 3. Les 15 OFFICIELS (couverture des 15 domaines)

| Domaine | Widget | ID | Score |
|---|---|---|---|
| Régime | Regime Aura | W01 | 92 |
| Prix | Candlestick Snapshot | W-CAN | 94 |
| Momentum | Relative-Strength Path | W-RSP | 90 |
| Breadth | Market Breadth Field | W-BF | 90 |
| Rotation sectorielle | Sector Rotation Orbit | W12 | 91 |
| Opportunité | Opportunity Dominant Slab | W33 | 92 |
| Analyse | Verdict Slab | W44 | 93 |
| Risque | Risk / Reward Terrain | W-RRT | 91 |
| Catalyseur | Catalyst Runway | W-CR | 90 |
| Portefeuille | Position Health Strip | W-PHS | 91 |
| Drawdown | Drawdown Canyon | W-DC | 90 |
| Options | Payoff Terrain | W50 | 91 |
| Volatilité | Volatility Cone | W-VC | 90 |
| Liquidité | Liquidity Depth | W-LD | 90 |
| Système | Data Integrity Reactor | W68 | 90 |

Contrats complets (usage, API, variantes officielle/compacte/mobile, pages
autorisées, états) : **`docs/visual/VERTEX_OFFICIAL_WIDGET_REGISTRY.md`**, et
rendus en direct dans le lab via le panneau dépliant « Contrat officiel ».

## 4. Audit complet des 60 widgets

| ID | Widget | Famille | Score | Statut |
|---|---|---|---|---|
| W-CAN | Candlestick Snapshot | Analyse | 94 | OFFICIEL |
| W44 | Verdict Slab | Analyse | 93 | OFFICIEL |
| W01 | Regime Aura | Régime | 92 | OFFICIEL |
| W33 | Opportunity Dominant Slab | Opportunité | 92 | OFFICIEL |
| W12 | Sector Rotation Orbit | Rotation | 91 | OFFICIEL |
| W-RRT | Risk / Reward Terrain | Opportunité | 91 | OFFICIEL |
| W-PHS | Position Health Strip | Portefeuille | 91 | OFFICIEL |
| W50 | Payoff Terrain | Options | 91 | OFFICIEL |
| W-RSP | Relative-Strength Path | Momentum | 90 | OFFICIEL |
| W-BF | Market Breadth Field | Breadth | 90 | OFFICIEL |
| W-CR | Catalyst Runway | Catalyseurs | 90 | OFFICIEL |
| W-DC | Drawdown Canyon | Portefeuille | 90 | OFFICIEL |
| W-VC | Volatility Cone | Volatilité | 90 | OFFICIEL |
| W-LD | Liquidity Depth | Options | 90 | OFFICIEL |
| W68 | Data Integrity Reactor | Système | 90 | OFFICIEL |
| W29 | Premium Index Card | Marchés | 88 | RÉFÉRENCE |
| W-PLD | Price Ladder | Analyse | 88 | RÉFÉRENCE |
| W45 | Scenario Triad | Analyse | 87 | RÉFÉRENCE |
| W-TP | Thesis Pulse | Analyse | 86 | RÉFÉRENCE |
| W-OFR | Order-Flow Ribbon | Opportunité | 86 | RÉFÉRENCE |
| W37 | Comparison Matrix | Opportunité | 86 | RÉFÉRENCE |
| W-SRS | Support / Resistance Spine | Analyse | 85 | RÉFÉRENCE |
| W-PC | Allocation Constellation | Portefeuille | 85 | RÉFÉRENCE |
| W-CANM | Candlestick — Indice | Marchés | 85 | RÉFÉRENCE |
| W36 | Investment Pipeline (refondé) | Opportunité | 85 | RÉFÉRENCE |
| W-SD | Score Decomposition | Analyse | 84 | RÉFÉRENCE |
| W51 | Greek Vector Field | Options | 84 | RÉFÉRENCE |
| W-TAPE | Market Tape | Marchés | 84 | RÉFÉRENCE |
| W-BH | Bias Cost Ledger (refondé) | Journal | 84 | RÉFÉRENCE |
| W-EGM | Earnings Gap Map | Catalyseurs | 83 | RÉFÉRENCE |
| W-CT | Concentration Tower | Portefeuille | 83 | RÉFÉRENCE |
| W-CL | Confidence Lens | Analyse | 82 | RÉFÉRENCE |
| W-CW | Market Correlation Web | Marchés | 82 | RÉFÉRENCE |
| W-CANC | Candlestick — Carte compacte | Opportunité | 82 | RÉFÉRENCE |
| W-CC | Committee Consensus | Analyse | 81 | RÉFÉRENCE |
| W-PL | Discipline Curve (refondé) | Journal | 79 | À RETRAVAILLER |
| W35 | Asymmetry Ledge (Scatter) | Opportunité | 78 | À RETRAVAILLER |
| W41 | Catalyst Countdown Ring | Catalyseurs | 77 | À RETRAVAILLER |
| W21 | Health Reactor | Breadth | 76 | À RETRAVAILLER |
| W-FM | Source Freshness Matrix | Système | 76 | À RETRAVAILLER |
| W-WG | Winner / Loser Guardrails | Portefeuille | 75 | À RETRAVAILLER |
| W23 | Stress Thermocline | Volatilité | 75 | À RETRAVAILLER |
| W04 | Risk-of-Day Verdict (Slab) | Régime | 74 | À RETRAVAILLER |
| W07b | Momentum Ribs | Momentum | 74 | À RETRAVAILLER |
| W-ES | Engine Status Spine | Système | 74 | À RETRAVAILLER |
| W17 | Breadth Tide | Breadth | 73 | À RETRAVAILLER |
| W-OB | Opportunity Beacon (Signal Bloom) | Opportunité | 73 | À RETRAVAILLER |
| W07 | Momentum Comb | Momentum | 72 | À RETRAVAILLER |
| W23b | Volatility Rift | Volatilité | 72 | À RETRAVAILLER |
| W38b | Conviction Pillar | Opportunité | 72 | À RETRAVAILLER |
| O-1 | Primitives — KPI/Grade/Live | Primitives | 72 | À RETRAVAILLER |
| W08 | Trend Ribbon (Sparkline+) | Momentum | 70 | À RETRAVAILLER |
| W38 | Conviction Spine | Opportunité | 70 | À RETRAVAILLER |
| W-DR | Discipline Ring | Journal | 70 | À RETRAVAILLER |
| W-RC | Risk Crater | Volatilité | 68 | À RETRAVAILLER |
| W-RS | READONLY Seal | Système | 64 | REJETÉ |
| W24 | Dial (VIX / borné) | Volatilité | 62 | REJETÉ |
| W-TB | Theta Burn Track | Options | 60 | REJETÉ |
| W05 | Rail (axe borné) | Régime | 60 | REJETÉ |
| W-LL | Liquidity Lens | Options | 58 | REJETÉ |

## 5. Widgets refondés (3)

- **Selection Funnel → Investment Pipeline** (W36) : n'est plus un entonnoir
  marketing. Devient un pipeline de sélection à barres — univers → éligibles
  (liquidité) → qualité → radar → prioritaires → actionnables — avec **cause
  d'exclusion** à chaque étage, **coût de filtration** (% écartés) et **variante
  honnête « zéro actionnable »** (« Aucun dossier actionnable — patience, pas de
  forçage »).
- **Bias Heatmap → Bias Cost Ledger** (W-BH) : n'est plus une grille abstraite.
  Devient un registre trié par **coût P&L** : chaque biais avec fréquence, coût
  %, **récence** (pastille), barre d'impact, et une lecture décisionnelle qui
  désigne « le biais qui détruit le plus ».
- **Progress Ladder → Discipline Curve** (W-PL) : plus aucun ton de jeu / niveau.
  Devient une **courbe de respect de la méthode** dans le temps, seuil discipline
  80 %, **entorses marquées**, qualité moyenne des décisions, variantes progrès /
  recul.

## 6. Contrats normalisés

Schéma commun (P04 §5) : `title · question · conclusion · value · unit · period ·
source · freshness · state · semantic tone · compact · mobile · accessible
summary · interaction`. Les 15 officiels portent en plus usage canonique, API de
données attendue, variantes officielle/compacte/mobile et pages autorisées. Le
lab rend ces contrats en panneau dépliant sous chaque officiel ; le registre les
fige. Données du lab = échantillons fictifs, clairement étiquetés.

## 7. Export enrichi

Le bouton **Exporter mes choix** produit désormais un document structuré :
version du lab + date, sections **Officiels / Références / Rejetés** (nom +
statut/score de curation), **notes libres par widget** (bouton ✎ par tuile,
persistées `vxWidgetLabNotes`), et une section « Notes sans verdict ».
`Réinitialiser` efface choix **et** notes.

## 8. Test de cohérence des officiels

- **Diversité** : 15 formes distinctes (halo, chandeliers, chemin, champ, orbite,
  slab, terrain, piste, bande, canyon, relief, cône, profondeur, réacteur) — pas
  deux qui se ressemblent.
- **Grammaire commune** : tous via `_hdr` (prix/%), `_concl` (décision `▸`),
  `_foot` (source·fraîcheur·mode).
- **Couleurs sémantiques** : vert=haussier, rouge=baissier, ambre=attente,
  violet=vol, cyan=info ; **orange réservé** identité/interaction/point actif
  (gardien zéro-bleu vert).
- **Densité cohérente** : réponse < 1 s / preuve / détail au survol.
- **Lisibles ensemble** : vérifié en page complète 1440 et colonne 390.

## 9. Validation

- `python -m compileall -q terminal.py vertex` → exit 0.
- `python -m pytest tests/ -q` → **980 passed, 2 skipped** (dont 7 gardiens P04 :
  classification exhaustive, plafonds 15/20, contrats officiels complets,
  couverture des domaines, UI de curation, widgets refondés renommés, export enrichi).
- Navigateur **1440 & 390** : **0 débordement de page, 0 débordement d'élément,
  0 erreur console**.
- Captures : `lab4-top.png` (bandeau récap + statuts), `lab4-official-contract.png`
  (Verdict Slab officiel + contrat déplié), `lab4-pipeline.png` (Investment
  Pipeline), `lab4-journal.png` (Bias Cost Ledger + Discipline Curve),
  `lab4-mobile.png` (390 : header/récap/nav wrap, badges, Regime Aura enrichi).

## 10. Limites restantes / différé

- Les **20 « À retravailler »** ne sont pas supprimés : ils restent visibles,
  grisés/marqués, pour décision humaine (fusion, promotion ou retrait). Doublons
  identifiés à trancher : Momentum Comb/Ribs, Conviction Spine/Pillar, Volatility
  Rift vs Cone, Countdown Ring vs Catalyst Runway, Discipline Ring vs Curve.
- Les **variantes compacte/mobile** des officiels sont **spécifiées au contrat**
  mais pas toutes rendues en tuile dédiée — prochaine passe (rendu réel des 3
  variantes par officiel).
- Les 5 **rejetés** restent dans le lab (traçabilité de la décision) mais sont
  exclus du registre officiel.
- Aucune reconstruction de page produit : la curation **précède** la refonte des
  pages, qui devra se composer exclusivement à partir du registre officiel.

## Verdict

La bibliothèque devient un **système curé** : 15 objets officiels (un par
domaine) avec contrats gelés, 20 références, tout le reste explicitement classé,
**aucun widget médiocre conservé par défaut**, 3 widgets faibles refondés,
export de décision enrichi et registre officiel. **60 widgets classés · 15
officiels · 980 tests verts · 0 débordement · 0 erreur console · READONLY ·
aucune donnée inventée.** **Arrêt pour validation humaine.** Dis-moi les
promotions/retraits parmi les « À retravailler » et je grave le registre.
