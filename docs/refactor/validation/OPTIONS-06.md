# Validation — PR n°6 : Refonte Options

> Branche `agent/vertex-total-rebuild`. Options cesse d'être un catalogue de
> Greeks pour répondre à **une seule question** : « Cette structure offre-t-elle
> une asymétrie suffisamment bonne pour mériter du capital ? »
> Conforme à `VERTEX_CONSTITUTION.md` (§6, §17-22), `VERTEX_PRODUCT_BIBLE.md`,
> `PRODUCT_EXPERIENCE_REVIEW.md`. **IBKR READONLY absolu** : aucun bouton ni chemin
> d'exécution d'ordre. Un seul moteur de payoff : `multileg_lab`.

## 1. Fichiers modifiés

- `vertex/engines/multileg_lab.py` — **correction de calcul prouvée** : conversion
  IV pourcentage → décimale au point de jonction `strategies_for_symbol` (cœur
  `analyze_strategy` intact).
- `vertex/ui/pages/options_intel_page.py` — 3 vues canoniques (structure défaut ·
  LEAPS · Mes positions) ; overview/radar/scenarios restent servies (routes 200).
- `vertex/static/vertex/js/pages/options-structure.js` (**nouveau**) — Carte-Verdict,
  Carte-Scénario, payoff canonique, Greeks interprétés, liquidité, LEAPS, positions.
- `vertex/ui/pages/portfolio_page.py` — vue Options réduite à un **résumé + lien**
  (réconciliation LOT J) ; drawer/payoff combiné par position retirés.
- `vertex/app/routes/system.py` — bump service worker `td-shell-v48 → v49`.
- Tests : `tests/test_multileg_iv_units_06.py` (**4 gardiens, correction prouvée**),
  `tests/test_options_structure_06.py` (**19 gardiens**) + gardiens SW v49.

## 2. Correction de calcul (protocole preuve → rouge → correction → vert → doc)

**Preuve** : le board porte `iv` en pourcentage (ex. 40,4 = 40,4 %) ; `analyze_strategy`
attend une **décimale**. Sans conversion, la volatilité valait ~4040 %, produisant :
- **PoP = 100 %** (impossible pour un call long à débit),
- **delta de call ATM saturé à 100** (soit 1,0/action au lieu de ~0,5),
- theta ≈ −0,0 (érosion nulle).

**Test rouge** puis **vert** : `tests/test_multileg_iv_units_06.py` (PoP < 95 %,
delta ATM ∈ ]20,90[, theta < 0, IV renvoyée < 1,5). **Correction** localisée :
`iv = raw/100 si raw > 1,5` dans `strategies_for_symbol`. Vérifié en live après
correction : `iv 0.404 · PoP 22,1 % · delta 54,2 · theta −28,3`. **166 tests
options/portefeuille verts** (aucune régression).

## 3. Structure avant / après (sous-vues Options)

| Avant | Après |
|---|---|
| Vue d'ensemble (défaut) · Volatilité · Radar contrats · Scénarios · Événements | **Structure** (défaut : Carte-Verdict) · **LEAPS** · **Mes positions** · Volatilité · Événements · (overview/radar/scenarios encore servies, hors barre) |

## 4. Carte-Verdict Options (LOT A)

`section.vx-verdict-card` depuis la structure recommandée : sous-jacent + spot ·
stratégie · biais · échéance/DTE · strikes · débit/crédit · **capital à risque** ·
**perte max** · **gain probable (+1σ, échéance)** · **gain exceptionnel** ·
**breakeven(s)** · **ratio d'asymétrie** (gain exc. / perte max) · delta · theta ·
IV · **liquidité** · fraîcheur · qualité des données · **verdict analytique**.
Verdicts : *Asymétrie excellente · Structure intéressante mais chère · Risque/temps
médiocre · Liquidité insuffisante · Données insuffisantes · Attendre une meilleure
entrée · Structure rejetée*. Aucune probabilité inventée (la PoP vient du moteur,
étiquetée « estimation »). Le mouvement favorable est **orienté par le biais**
(baissier → vers le bas) pour un « gain probable » cohérent avec les scénarios.

## 5. Carte-Scénario (LOT C)

`div.vx-scenario-grid` : **pessimiste / probable / exceptionnel** — prix du
sous-jacent (±1σ/±2σ via IV·√t), **P&L à l'échéance**, P&L %, horizon (DTE).
Distinction explicite **payoff à l'échéance vs valeur avant échéance** (valeur-temps
non modélisée pour ne pas inventer un prix). Perte probable / gain probable / gain
exceptionnel jamais confondus.

## 6. Payoff canonique (LOT D) — moteur unique

`multileg_lab` via `/api/options/strategies/<sym>` (aucun autre moteur de payoff sur
la page ; `option-payoff.js` retiré du parcours). Chart Shell : titre · question ·
**conclusion** (« zone favorable au-delà de … · perte plafonnée à … ») · unité
(P&L $) · période (DTE) · source · fraîcheur · **résumé accessible**. Marqueurs
tracés : **spot** + **breakeven(s)**, ligne zéro, segments verts/rouges (zones
favorable/défavorable).

## 7. Greeks interprétés (LOT E)

Premier niveau (delta/theta/vega/gamma) — chacun avec valeur + unité +
**interprétation en langage clair** (« Delta : ≈ 54,6 $ de P&L par +1 $ du
sous-jacent », « Theta : ≈ −17 $/jour d'érosion »). Deuxième niveau dépliable
(vanna/vomma). **Jamais un Greek sans interprétation** ; greeks non fiables (IV
absente) → **Insufficient** honnête (aucune estimation inventée).

## 8. Liquidité (LOT G)

État explicite **Excellente / Acceptable / Médiocre / Insuffisante** depuis OI +
spread % du board (pire jambe pour une structure). Un bid/ask ou OI absent →
**Insuffisante** (jamais remplacé par zéro) ; une liquidité insuffisante interdit
tout verdict positif (avertissement dominant).

## 9. LEAPS explicable (LOT B)

Lecture dédiée des calls 6-18 mois. **Score de compatibilité explicable** (0-100)
= somme de composantes réelles affichées (Delta 0,70-0,90 · échéance · OI · spread ·
IV), **aucun score opaque**. Distingue **achat de tendance** (delta directionnel)
et **achat de temps** — avec le rappel « le temps seul n'est pas une thèse ; la
durée ne remplace pas la thèse ».

## 10. Comparaison de structures (LOT I)

**Matrice** (pas de radar) : coût/risque max · gain max · breakeven · delta ·
theta · vega · PoP · DTE · liquidité · asymétrie · adéquation. La structure la
mieux adaptée au biais est marquée ★. Répond « quelle structure exprime le mieux
la thèse avec le moins de risque inutile ? ».

## 11. Positions & garde-fou (LOT J/K)

- **Réconciliation** : Options → **Mes positions** devient le domicile canonique
  détaillé (contrat, qté, coût, marque, P&L %, DTE, invalidation, prochaine action,
  lien Structure). Le **Portefeuille** ne garde qu'un **résumé d'exposition + lien**
  (drawer et payoff combiné par position retirés — gardien
  `test_portfolio_options_is_summary_with_link`).
- **Règles gagnants** indicatives : +20 (aucune action) / +30 (réévaluer
  invalidation & temps) / +50 (conserver si thèse+catalyseur) / +75 (réévaluation
  complète) / +100 (« sécuriser 25-50 % et laisser courir »).
- **Garde-fou perdants** (test gardien exigé) : une option en perte ne reçoit
  **jamais** « renforcer » sans confirmation positive — **jamais parce que la prime
  a baissé** → message **« Renforcement interdit : aucune confirmation positive
  détectée »** (vérifié sur AMD PUT −33 %, capture).

## 12. DATA_INSUFFICIENT

Structure non évaluable → `vx-insufficient` : pas de verdict positif, pas de PoP
fabriquée, pas de Greek fiable, explication des données manquantes + prochaine
action. Greeks sans IV → « Insufficient ». Liquidité manquante → « Insuffisante ».

## 13. Graphiques avant / après

| Espace | Avant | Après | Note |
|---|---|---|---|
| **Options / parcours structure** | inexistant | **1 payoff canonique** | verdict/scénario/greeks/comparaison = composants, pas des graphiques |
| **Options / LEAPS** | — | **0** (barres de score explicables) | pas de chart décoratif |
| **Options / Volatilité, Événements** | inchangées | inchangées | domicile canonique volatilité/événement |
| **Portefeuille / Options** | treemap + N payoffs combinés + drawers | **0** (résumé KPI + liens) | détail migré vers Options |

Moteur de payoff : **un seul** (`multileg_lab`). Doublons retirés : payoffs combinés
par position et treemap options du Portefeuille (migrés vers le domicile Options).

## 14. Tests exacts

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **944 passed, 2 skipped** (+23 gardiens PR6 : 4 IV,
  19 structure/positions/garde-fou/READONLY/migration).
- Gardiens clés : `test_long_call_pop_is_not_impossible_100`,
  `test_atm_long_call_delta_not_saturated`, `test_verdict_card_present_and_honest`,
  `test_scenario_card_expiry_labeled`, `test_payoff_uses_canonical_engine`,
  `test_greeks_always_interpreted_or_insufficient`,
  `test_liquidity_states_explicit_no_zero_for_missing`,
  `test_leaps_score_is_explainable`, `test_comparison_matrix_not_radar`,
  `test_option_loser_reinforcement_forbidden`,
  `test_portfolio_options_is_summary_with_link`, `test_no_order_execution_in_options`.
  Routes 200 (structure/leaps/positions/volatility/events/overview/radar/scenarios) ;
  invariant READONLY (`_ORDER_WORDS`) vert.

## 15. Contrôle navigateur (390 / 768 / 1440)

Débordement réel et console applicative, sur 6 vues (structure/leaps/positions/
volatilité/événements + Portefeuille→Options) :

| Viewport | Débordement | Erreurs console |
|---|---|---|
| **390 mobile** | **0 px** (6/6) | **0** (6/6) |
| **768 tablet** | **0 px** (6/6) | **0** (6/6) |
| **1440 desktop** | **0 px** (6/6) | **0** (6/6) |

- Vérifié : Carte-Verdict (asymétrie, liquidité, verdict), Carte-Scénario
  (échéance), payoff canonique (spot+breakevens, zones), Greeks interprétés +
  Insufficient, matrice de comparaison, LEAPS explicable (delta 0,45 pénalisé),
  garde-fou perdants sur AMD PUT −33 %, réduction du Portefeuille→Options.
- Tableaux larges → scroll horizontal intentionnel (desktop) / cartes (mobile).
- Captures : scratchpad `pr6shots/` (desktop structure/leaps/positions, mobile
  structure).

## 16. Erreurs restantes

- Console applicative : **0**. (`ERR_CONNECTION_RESET` = Google Fonts via proxy
  sandbox, non applicatif.)

## 17. Risques techniques

- **Valeur avant échéance non modélisée** : les scénarios donnent le P&L à
  l'échéance (payoff). La valeur intraday (theta + IV) n'est pas estimée pour ne pas
  inventer un prix — clairement étiqueté. Une modélisation Black-Scholes avant
  échéance serait un ajout moteur futur (avec preuve/test).
- **Liquidité approchée depuis le board** (OI + spread %) ; sans profondeur réelle
  IBKR, l'état reste indicatif mais honnête (jamais un verdict positif si
  insuffisante).
- **PoP = modèle lognormal risque-neutre** — estimation étiquetée, jamais une
  promesse.
- Vues `overview/radar/scenarios` conservées (routes testées) mais hors barre
  d'onglets : à retirer proprement (avec mise à jour des tests) dans une passe de
  nettoyage ultérieure (PR n°9).
- Validation Chromium **headless**.

## 18. Plan précis de la prochaine PR — Journal + Système

- **Journal** (mission : « la méthode fonctionne-t-elle et est-elle correctement
  exécutée ? ») : décisions, hypothèses, erreurs, statistiques, apprentissage.
  Discipline seule (la performance de portefeuille vit déjà dans Portefeuille depuis
  la PR n°5). Boucle décision → résultat → leçon ; règles proposées.
- **Système** : IBKR/fraîcheur/moteurs/diagnostics/paramètres/design system ; états
  honnêtes (live/demo/offline), READONLY, service worker, versions.
- Chart Shell complet ; 0 débordement 390/768/1440 ; 0 console ; SW bump ; READONLY
  intact ; captures avant/après + comptes de graphiques.

## Verdict

**GO.** Options répond à sa question unique : **Carte-Verdict d'asymétrie** +
**Carte-Scénario** (échéance) + **payoff canonique** (`multileg_lab`, moteur unique)
+ **Greeks interprétés** (ou Insufficient) + **liquidité explicite** + **LEAPS
explicable** + **matrice de comparaison** ; positions options réconciliées en
domicile unique avec **garde-fou perdants testé** ; **bug d'unité d'IV corrigé
avec preuve** (PoP 100 %→22 %, delta saturé→54). **944 tests verts** ; **0
débordement** et **0 erreur console** sur 18 combinaisons vue×viewport ; **READONLY
intact**. Fondations posées pour Journal + Système.
