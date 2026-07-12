# VERTEX — Chart Intelligence & Options Intelligence

> Tranche verticale livrée et **prouvée** (tests + navigateur). Ce document
> décrit ce qui existe réellement dans le code, pas une intention. La règle de
> vérité s'applique : ce qui n'est pas prouvé n'est pas déclaré « fait » (voir
> la section « Périmètre livré vs reste à faire »).

## 1. Idée directrice

Un graphique Vertex n'est pas qu'un dessin : c'est une paire **(données,
interprétation)**. Chaque graphique répond à **une** question et rend un
verdict lisible — **FAVORABLE / NEUTRE / DÉFAVORABLE / BLOQUANT / INCONNU** —
accompagné de ses preuves, de ses incertitudes, de son impact stratégique et
de ses limites méthodologiques. Donnée absente → **INCONNU** honnête, jamais
un chiffre inventé. Lecture seule, aucun ordre.

## 2. Contrat canonique d'interprétation (§6)

`vertex/visualization/schemas.py` — `interpretation(...)` produit un dict au
format STRICT (validé par `is_valid_interpretation`) :

| champ | rôle |
|---|---|
| `chart_id` | identifiant stable (`options.volatility`, `options.overview_mix`…) |
| `question` | LA question à laquelle le graphique répond |
| `dominant_reading` | lecture dominante en une phrase |
| `status` | FAVORABLE / NEUTRE / DEFAVORABLE / BLOQUANT / INCONNU |
| `confidence` | 0..1 (clampé), `None` si non mesurable |
| `positive_evidence` / `negative_evidence` | faits pour / contre |
| `uncertainties` | zones d'ombre, données manquantes |
| `strategy_impact` | ce que ça change pour la décision |
| `source` / `as_of` | provenance + horodatage |
| `limitations` | limites méthodologiques honnêtes (§6.8) |

Garanties : lecture vide ⇒ statut forcé à `INCONNU` ; statut inconnu du
vocabulaire ⇒ `INCONNU` ; helper `unknown(...)` pour un verdict honnête
quand la donnée manque.

## 3. Moteurs options purs (testés)

Fonctions sans effet de bord, `None` si donnée absente (jamais de zéro inventé) :

- **`vertex/options/volatility.py`** — `iv_rank`, `iv_percentile`,
  `realized_vol` (close-to-close annualisée, écart-type d'échantillon),
  `iv_rv_premium`, `vol_regime`.
- **`vertex/options/expected_move.py`** — `expected_move` (1σ implicite
  `spot·IV·√(dte/365)`), `expected_move_pct`, `expected_range`,
  `move_covers_target`.
- **`vertex/options/event_risk.py`** — `earnings_risk`, `dividend_risk`
  (CALL pénalisé à l'approche de l'ex-dividende), `combined` (prend le pire).

Ces mesures alimentent **`vertex/options/interpretation.py`**
(`interpret_volatility`, `interpret_event_risk`) et
**`vertex/options/overview.py`** (`summarize` → compteurs, radar,
interprétation du biais) — tous rendent le contrat canonique du §2.

Point de vue assumé : le desk **achète** des options → une IV élevée est
**DÉFAVORABLE** (prime chère, risque de crush) ; une IV basse est
**FAVORABLE**.

## 4. API (lecture seule)

`vertex/app/routes/options_intel_api.py` :

| route | rend |
|---|---|
| `GET /api/options/overview` | compteurs + radar + interprétation du biais |
| `GET /api/options/volatility/<sym>` | interprétation volatilité du titre |
| `GET /api/options/event-risk/<sym>` | interprétation risque d'événement |
| `GET /api/charts/<chart_id>/interpretation` | route de contrat (délègue selon `chart_id`, `?sym=`) |

Les données proviennent du scan (`scan_state['options_board']`, réel ou démo).
Board vide → interprétation `INCONNU` (comportement vérifié).

## 5. Page `/options` — Options Intelligence

`vertex/ui/pages/options_intel_page.py` +
`vertex/static/vertex/js/pages/options-intel.js`.

- **Pas un 9e espace** : la barre reste à **huit** espaces. `/options` est un
  approfondissement d'**Opportunités** (le nav marque Opportunités actif) —
  invariant vérifié par test (`test_options_page_renders_and_stays_eight_spaces`).
- Points d'entrée : bouton « Options Intelligence → » dans Opportunités · vue
  Options ; URL directe `/options`.
- Sous-vues (`?view=`) : **overview · volatility · radar · events**.
- Chaque graphique porte un bouton **« Comprendre ce graphique »** qui ouvre un
  tiroir avec question, preuves pour/contre, incertitudes, impact, limites,
  source et horodatage — le contrat canonique rendu tel quel.
- Thème **Obsidian Copper** (zéro bleu) ; badges de statut colorés via
  `--vx-positive` / `--vx-negative` / dim.

## 6. Tests (prouvés)

- `tests/test_option_volatility.py` — 20 tests : IV rank/percentile bornés,
  vol réalisée (formule manuelle vérifiée, plat ⇒ 0, insuffisant ⇒ None),
  expected move 1σ, ratios cible, niveaux d'event risk, `combined` prend le pire.
- `tests/test_chart_interpretation.py` — 18 tests : contrat canonique (clés,
  clamp, lecture vide ⇒ INCONNU), verdicts volatilité/event, overview
  (compteurs, radar trié, board vide ⇒ INCONNU).
- `tests/test_options_routes.py` — 10 tests : routes rendent le contrat
  canonique, `/options` reste à 8 espaces, chart_id inconnu ⇒ INCONNU honnête,
  **aucun chemin d'ordre** dans les nouveaux modules.

Suite complète : **635 tests OK** (597 avant + 38 nouveaux). Navigateur
Chromium : `/options` et ses 4 sous-vues → **0 erreur console** ; verdict
interactif de volatilité vérifié (GOOGL ⇒ DÉFAVORABLE, IV médiane 46,8 %).

## 7. Invariants respectés

- **READONLY** : aucune route ne passe/modifie/clôture d'ordre ; test garde-fou
  sur les 14 verbes interdits pour chaque nouveau module.
- **Données réelles / honnêteté** : `None`/`—`/INCONNU quand la donnée manque ;
  le mot « démo » n'apparaît que si le serveur le confirme (`demo=DEMO_MODE`).
- **Zéro bleu** : styles ajoutés en tokens copper/beige uniquement.
- **Huit espaces** : `/options` n'ajoute pas d'item de navigation.
- **Zéro nom personnel** dans le code ajouté (garde-fou `test_namespace_guards` ⇒ vert).

## 8. Périmètre livré vs reste à faire (honnêteté §6)

**Livré et prouvé** : contrat d'interprétation canonique ; moteurs
volatilité / expected move / event risk / overview ; interprétations options ;
4 routes API ; page `/options` à 4 sous-vues avec tiroir « Comprendre ce
graphique » ; 48 tests ; 0 erreur navigateur.

**Non encore livré** (la spec « 11 sous-vues » est plus vaste) : sous-vues
Chain complète, Greeks agrégés de position, Scenarios (le moteur
`scenario_pricer` existe et est déjà exposé via `/api/options/simulate` mais
n'a pas encore d'onglet dédié dans `/options`), Events calendrier riche,
Positions options intégrées, Performance options, Journal options ;
enrichissement graphique des 8 pages avec le tiroir d'interprétation
généralisé. Ces éléments réutiliseront le même contrat canonique du §2 —
la fondation est posée et testée.
