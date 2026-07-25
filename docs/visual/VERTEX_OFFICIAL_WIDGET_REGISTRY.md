# VERTEX — REGISTRE OFFICIEL DES WIDGETS

> Source de vérité des composants **autorisés en page produit**. Un widget qui
> n'est pas OFFICIEL ici ne peut pas être utilisé dans une page Vertex sans
> repasser par le laboratoire `/widget-lab` et une validation humaine.
> Version du lab : **P04-curation**. Audit : `WIDGET-LAB-04-CURATION.md`.
> Données du lab = **échantillons fictifs** ; les contrats décrivent l'API
> réelle attendue en production (READONLY, aucune donnée inventée).

## Statuts

| Statut | Score | Sens |
|---|---|---|
| **OFFICIEL** | ≥ 90 | Prêt pour les pages produit, contrat gelé. |
| **RÉFÉRENCE** | 80–89 | Bon, réutilisable en second rideau ; pas encore gelé. |
| **À RETRAVAILLER** | 65–79 | Idée valable, forme à durcir avant usage. |
| **REJETÉ** | < 65 | Ne pas utiliser ; remplacé par un objet officiel. |

Répartition actuelle : **15 Officiels · 20 Références · 20 À retravailler ·
5 Rejetés** (60 widgets, aucun non classé).

---

## Les 15 objets OFFICIELS

Chaque officiel a un identifiant stable, un nom final, une question, un usage
canonique, trois variantes (officielle / compacte / mobile), des états, une
conclusion de décision, une API de données attendue et une liste de pages
autorisées.

### W01 — Regime Aura · Régime · score 92
- **Question** : Dans quel régime de marché suis-je, avec quelle confiance ?
- **Usage canonique** : bandeau de régime en tête d'Aujourd'hui / Marchés.
- **Variantes** : officielle = halo + grammaire (SPX>MM200 · breadth · VIX) ·
  compacte = halo + prix/% seuls · mobile = halo réduit + strip 3 métriques empilé.
- **États** : loading · empty · insufficient · stale · demo · live.
- **Conclusion** : « Régime porteur — risque neuf autorisé, invalidation SPX < MM50 ».
- **API attendue** : `regime.label`, `regime.confidence`, `spx.vs_ma200`,
  `breadth.pct`, `vix.level`, `regime.invalidation`.
- **Unité · période** : % confiance · séance.
- **Pages autorisées** : Aujourd'hui, Marchés.

### W-CAN — Candlestick Snapshot · Prix (Analyse) · score 94
- **Question** : Le prix confirme-t-il la cassure au-dessus de la résistance ?
- **Usage canonique** : graphe prix canonique d'une fiche Analyse.
- **Variantes** : officielle = chandeliers + volume + MM + niveaux + événement ·
  compacte = mini-chandeliers + prix/% (carte) · mobile = chandeliers pleine
  largeur, niveaux repliés au tap.
- **États** : loading · insufficient · stale · demo.
- **Conclusion** : « Cassure confirmée au-dessus de R — entrée valide, invalidation stop ».
- **API attendue** : `ohlc[]`, `plan.entry`, `plan.stop`, `plan.targets[]`,
  `levels.resistance`, `ma[]`, `events[]`.
- **Unité · période** : prix · 22 séances.
- **Pages autorisées** : Analyse, Marchés, Opportunités.

### W-RSP — Relative-Strength Path · Momentum · score 90
- **Question** : L'actif surperforme-t-il son indice ?
- **Usage** : force relative d'un titre vs indice (Analyse / Momentum).
- **Variantes** : officielle = chemin RS + ligne zéro · compacte = ligne RS +
  dernier point · mobile = ligne pleine largeur, ligne zéro conservée.
- **États** : loading · insufficient.
- **Conclusion** : « Surperforme — RS croissante au-dessus de 0 » / divergence baissière.
- **API** : `rs_series[]`, `benchmark.symbol`. **Unité·période** : écart % · 8 périodes.
- **Pages** : Analyse, Marchés.

### W-BF — Market Breadth Field · Breadth · score 90
- **Question** : La hausse est-elle partagée ?
- **Usage** : participation du marché (Marchés / Aujourd'hui).
- **Variantes** : officielle = champ 40 points + A/D · compacte = champ + %>MM50 ·
  mobile = grille points + A/D empilés.
- **États** : loading · insufficient · stale.
- **Conclusion** : « Hausse partagée — participation saine > 55 % ».
- **API** : `breadth.above_ma50`, `breadth.above_ma200`, `adv`, `dec`,
  `new_highs`, `new_lows`. **Unité** : % · séance. **Pages** : Aujourd'hui, Marchés.

### W12 — Sector Rotation Orbit · Rotation · score 91
- **Question** : Qui entre en leadership ?
- **Usage** : rotation sectorielle (Marchés).
- **Variantes** : officielle = orbite à comètes · compacte = orbite réduite,
  4 leaders · mobile = liste secteurs triés par force.
- **États** : loading · insufficient.
- **Conclusion** : leadership vs retard sectoriel.
- **API** : `sectors[].symbol`, `sectors[].strength`, `sectors[].momentum`,
  `sectors[].state`. **Unité** : force · 20 séances. **Pages** : Marchés.

### W33 — Opportunity Dominant Slab · Opportunité · score 92
- **Question** : Quelle est la meilleure asymétrie, et pourquoi ?
- **Usage** : meilleure opportunité mise en avant (Opportunités).
- **Variantes** : officielle = slab dominant score + preuves · compacte =
  ticker + grade + score · mobile = colonne unique, métriques 2×2.
- **États** : loading · empty · demo.
- **API** : `top.symbol`, `top.grade`, `top.score`, `top.metrics[]`.
  **Unité** : /100 · scan. **Pages** : Opportunités.

### W44 — Verdict Slab · Analyse · score 93
- **Question** : J'entre, j'attends ou j'évite ?
- **Usage** : verdict de décision d'une fiche (Analyse).
- **Variantes** : officielle = verdict + preuves chiffrées · compacte = verdict +
  score seuls · mobile = verdict pleine largeur, preuves empilées.
- **États** : loading · insufficient · demo.
- **Conclusion** : ENTRER / ATTENDRE / ÉVITER.
- **API** : `verdict`, `score`, `grade`, `confidence`, `entry`, `invalidation`.
  **Unité** : /40 · scan. **Pages** : Analyse, Opportunités.

### W-RRT — Risk / Reward Terrain · Risque · score 91
- **Question** : L'asymétrie penche-t-elle en ma faveur ?
- **Usage** : asymétrie d'un plan (Analyse / Opportunités).
- **Variantes** : officielle = terrain relief + break-even · compacte = barre
  R:R + ratio · mobile = terrain pleine largeur, légendes sous le graphe.
- **États** : loading · insufficient.
- **API** : `plan.max_loss`, `plan.prob_gain`, `plan.exceptional`,
  `plan.break_even`. **Unité** : % · horizon plan. **Pages** : Analyse, Opportunités.

### W-CR — Catalyst Runway · Catalyseur · score 90
- **Question** : Quel catalyseur arrive, et quand ?
- **Usage** : prochains catalyseurs d'un titre (Analyse / Opportunités).
- **Variantes** : officielle = piste DTE + impact · compacte = prochain
  catalyseur + J-n · mobile = piste horizontale scrollable.
- **États** : loading · empty · stale.
- **API** : `catalysts[].label`, `catalysts[].dte`, `catalysts[].impact`.
  **Unité** : jours (DTE) · 30 j. **Pages** : Analyse, Opportunités, Aujourd'hui.

### W-PHS — Position Health Strip · Portefeuille · score 91
- **Question** : Cette position va-t-elle bien ?
- **Usage** : santé d'une position détenue (Portefeuille).
- **Variantes** : officielle = P&L + thèse + catalyseur + invalidation + action ·
  compacte = ticker + P&L + thèse · mobile = bande pleine largeur, action en bas.
- **États** : loading · empty · insufficient.
- **API** : `pos.symbol`, `pos.pl_pct`, `pos.thesis`, `pos.next_catalyst`,
  `pos.invalidation`. **Unité** : % P&L · temps réel. **Pages** : Portefeuille.

### W-DC — Drawdown Canyon · Drawdown · score 90
- **Question** : À quel point suis-je descendu ?
- **Usage** : repli d'un portefeuille / titre (Portefeuille).
- **Variantes** : officielle = canyon complet · compacte = canyon + creux max ·
  mobile = canyon pleine largeur.
- **États** : loading · insufficient.
- **API** : `drawdown_series[]`. **Unité** : % · glissant. **Pages** : Portefeuille, Journal.

### W50 — Payoff Terrain · Options · score 91
- **Question** : Que rapporte / coûte ce contrat ?
- **Usage** : payoff d'un contrat option (Options).
- **Variantes** : officielle = relief + zones · compacte = relief + break-even ·
  mobile = relief pleine largeur, zones colorées.
- **États** : loading · insufficient · demo.
- **API** : `contract.strike`, `contract.premium`, `contract.right`, `spot`,
  `break_even`. **Unité** : $/contrat · échéance. **Pages** : Options.

### W-VC — Volatility Cone · Volatilité · score 90
- **Question** : La vol implicite est-elle chère ?
- **Usage** : cherté de la volatilité implicite (Options / Volatilité).
- **Variantes** : officielle = cône + point actuel + percentile · compacte =
  cône + point · mobile = cône pleine largeur, percentile sous le graphe.
- **États** : loading · insufficient.
- **API** : `iv.current`, `iv.percentile`, `iv.cone[]`. **Unité** : % IV ·
  3M/6M/1A. **Pages** : Options, Marchés.

### W-LD — Liquidity Depth · Liquidité · score 90
- **Question** : Puis-je exécuter proprement ?
- **Usage** : liquidité / exécution d'un contrat (Options).
- **Variantes** : officielle = profondeur bid/ask + spread + OI · compacte =
  spread + volume · mobile = barres bid/ask empilées.
- **États** : loading · insufficient.
- **API** : `bid`, `ask`, `volume`, `open_interest`. **Unité** : prix · temps
  réel. **Pages** : Options.

### W68 — Data Integrity Reactor · Système · score 90
- **Question** : Puis-je faire confiance aux données ?
- **Usage** : confiance dans les données (Système).
- **Variantes** : officielle = cœur + barres qualité · compacte = cœur + score ·
  mobile = cœur + barres qualité empilées.
- **États** : loading · demo · offline.
- **API** : `integrity.score`, `sources[].name`, `sources[].quality`.
  **Unité** : /100 · temps réel. **Pages** : Système, Aujourd'hui.

---

## Contrat commun (schéma normalisé)

Tout widget officiel expose : `title` · `question` · `conclusion` · `value` ·
`unit` · `period` · `source` · `freshness` · `state` · `semantic tone` ·
`compact mode` · `mobile mode` · `accessible summary` · `interaction contract`.
Dépendances communes : tokens `tokens.css` (NEUE EMBER), aucune lib externe,
SVG/CSS inline, `prefers-reduced-motion` respecté. Aucune dépendance moteur au
niveau du widget : il consomme une **API de données déjà calculée** par les
moteurs Vertex (decision_stack, recommendation, options, evidence…), jamais un
appel direct — READONLY.

## Règle d'usage

Aucun widget **non enregistré comme OFFICIEL** ne peut apparaître dans une page
produit. Les Références sont utilisables en second rideau après validation ; les
« À retravailler » et « Rejetés » sont exclus des pages jusqu'à repassage par le
laboratoire. Toute nouvelle page se compose **exclusivement** à partir de ce
registre.
