# Validation — PR n°5 : Refonte Portefeuille

> Branche `agent/vertex-total-rebuild`. Le Portefeuille cesse d'être un inventaire
> pour répondre à **une seule question** : « Où mon capital est-il réellement
> exposé, et quelle position exige une décision ? »
> Conforme à `VERTEX_CONSTITUTION.md` (§17-22), `VERTEX_PRODUCT_BIBLE.md`,
> `PRODUCT_EXPERIENCE_REVIEW.md`. **IBKR READONLY absolu** : aucun bouton ni chemin
> d'exécution d'ordre. Aucun moteur financier modifié pour l'esthétique.

## 1. Fichiers modifiés

- `vertex/ui/pages/portfolio_page.py` — refonte complète (635 → ~760 lignes) :
  Synthèse premier écran + tableau canonique + moteur analytique de thèse +
  garde-fou perdants + vue Performance migrée + risque priorisé.
- `vertex/ui/pages/performance_page.py` (Journal) — retrait des courbes de
  **performance de portefeuille** (équité/drawdown/saisonnalité) migrées ;
  conserve méthode/discipline (KPI + distribution) + pointeur vers le domicile.
- `vertex/app/routes/system.py` — bump service worker `td-shell-v47 → v48`.
- `tests/test_portfolio_thesis_guardrail_05.py` (**nouveau, 10 gardiens**) dont le
  test gardien exigé du garde-fou perdants + gardiens SW (v48).

## 2. Structure avant / après

### Sous-vues Portefeuille
| Avant | Après |
|---|---|
| Équipe · Positions · Options · Risque · Watchlist | **Synthèse** · **Positions** · **Performance** (nouvelle) · Risque · Options · Watchlist |

### Synthèse (`/portfolio` — premier écran, LOT A)
| Avant (Équipe) | Après (Synthèse) |
|---|---|
| Allocation treemap + donut rôles + barres contributeurs + colonnes équipe (attaquants/milieux/défenseurs) | **Hero éditorial** (valeur nette + P&L latent + concentration Top1/Top3 + Freshness LIVE/DELAYED/OFFLINE) · **1 risque dominant** · **1 action prioritaire** · **4 KPI canoniques** (valeur nette · P&L total · concentration · exposition options/cash) · **Diff honnête** « depuis ta dernière visite » · **1 graphique** allocation/concentration · aperçu « positions exigeant une décision » |

### Positions (`/portfolio?view=positions` — LOT B/C/D)
| Avant | Après |
|---|---|
| Tableau Titre/Source/Contrat/Qté/Coût/Marque/P&L/Statut | **Tableau canonique** : ticker · instrument · qté · **prix moyen** · **prix actuel** · **valeur marché** · **P&L abs** · **P&L %** · **poids** (avec borne S+/S/A/B) · **conviction** · **état de thèse** · **invalidation** · **catalyseur** · **prochaine action** · bannière **garde-fou perdants** · graphique **contribution au P&L** |

## 3. Premier écran (LOT A)

Hero honnête (données réelles uniquement) : `« 22 610 de valeur nette · +710,00
de P&L latent »`, concentration `Top 3 = 85 %`, badge **LIVE/DELAYED/OFFLINE**.
**1 message max**, **4 KPI**, **1 risque dominant**, **1 action prioritaire**
(`analyse — aucune exécution d'ordre`). Chaque donnée porte unité, source et
fraîcheur ; un P&L indisponible affiche `n/d` (jamais un zéro inventé).

## 4. État de thèse (LOT B) — six états honnêtes

`intacte · renforcée par les faits · à surveiller · fragilisée · cassée · données
insuffisantes`. **« Cassée » vient EXCLUSIVEMENT du franchissement de
l'invalidation** (niveau pré-défini avant l'entrée : `mark <= stop`) — **jamais
d'une simple baisse de prix** (Constitution §18). `« Renforcée par les faits »`
exige un fait de validation explicite du snapshot (`validated/breakout/confirmed`)
— jamais fabriqué. Sans marque : `« données insuffisantes »`, jamais un verdict.

## 5. Gestion des gagnants (LOT C)

Règles **indicatives**, jamais une sortie automatique (§19) : +20 % (validé,
laisser courir), +30 % (verrouiller le risque), +50 % (relever le stop, réévaluer),
+75 %, **≥ +100 % : « sécuriser 25-50 % et laisser courir le reste »**.

## 6. Garde-fou perdants (LOT D) — **test gardien exigé**

Une position en perte **ne reçoit jamais** de suggestion « renforcer » sans
confirmation positive explicite. Sinon message affiché :
**« Renforcement interdit : aucune confirmation positive détectée »**
(vérifié en navigateur sur PLTR −10 % sans validation — capture mobile).
Test gardien : `test_loser_reinforcement_forbidden_message_present`,
`test_loser_reinforcement_gated_on_positive_confirmation`,
`test_no_naive_reinforce_suggestion_on_price_drop`.

## 7. Concentration & allocation (LOT E)

Poids par position, **Top 1 / Top 3**, exposition **options / cash / actions**.
Bornes indicatives **S+ 10-15 % · S 7-10 % · A 3-5 % · B 1-2 %** dérivées du score
du snapshot (`tierOf`), affichées `poids / borne` (surlignées si dépassement).
Repères analytiques, **jamais** un ordre de vente. Un seul graphique
allocation/concentration (treemap avec conclusion) — le donut rôles redondant a
été supprimé.

## 8. Risque priorisé (LOT F)

Hiérarchie **critiques → importants → secondaires** : garde-fous bloquants +
invalidations atteintes ; concentration/bêta/pire stress ; secteurs/Greeks.
« Manquant/insuffisant » n'est jamais présenté comme zéro (Greeks `non estimés
sans IBKR`). Moteur `risk_engine` inchangé (positions réelles).

## 9. Migration performance Journal → Portefeuille (LOT G, §6 « un seul domicile »)

- **Vers Portefeuille → Performance** : courbe d'équité **cumulée**, **drawdown**,
  **saisonnalité mensuelle**, **contribution au P&L par position**. 4 graphiques
  majeurs, chacun via Chart Shell (titre/question/conclusion/source/fraîcheur/aide).
- **Retiré du Journal** : `equityCard`, `drawdownCard`, `heatmapCard` (gardien
  `test_journal_no_longer_owns_portfolio_performance`). Le Journal conserve la
  **méthode/discipline** (P&L, taux de réussite, profit factor, espérance,
  **distribution des rendements**, erreurs, leçons) + un pointeur explicite vers
  `Portefeuille → Performance`. **Aucune courbe dupliquée.**

## 10. Diff « depuis ta dernière visite » (LOT H)

Référence localStorage `vxPortfolioBaseline` (posée avec marques réelles, fenêtre
12 h). Au premier passage : **« Aucun historique de comparaison disponible »**
(vérifié en capture). Ensuite : Δ valeur nette, Δ P&L latent, ≤3 positions ayant
le plus bougé. Jamais de delta fabriqué.

## 11. Mode sans IBKR (LOT I)

États honnêtes : `LIVE/DELAYED/OFFLINE` dans le Hero, `n/d` sur les marques
absentes, bannière « IBKR hors ligne — marques desk/EOD utilisées (aucune valeur
inventée) », Greeks « non estimés sans IBKR ». Mode démo : badge/bannière DÉMO.

## 12. Graphiques avant / après

| Espace | Avant | Après | Note |
|---|---|---|---|
| **Portef. Synthèse** | 3 (treemap + donut rôles + barres contrib) | **1** (treemap alloc/concentration) | donut rôles redondant supprimé ; contrib déplacé en Positions |
| **Portef. Positions** | 0 | **1** (contribution P&L) | |
| **Portef. Performance** | — | **4** (équité cumulée · drawdown · saisonnalité · contribution) | migrés depuis Journal |
| **Portef. Risque** | 3 | **3** (jauge HHI · secteurs · stress) | inchangé |
| **Journal Vue d'ensemble** | 4 (équité + drawdown + heatmap + distribution) | **1** (distribution) | 3 migrés vers Portefeuille |

Aucun graphique décoratif ajouté ; chaque graphique porte une **conclusion**.
Doublon supprimé : donut de rôles (redondant avec l'allocation treemap).

## 13. Tests exacts

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **926 passed, 2 skipped** (+10 gardiens PR5).
- Gardiens PR5 : `test_loser_reinforcement_forbidden_message_present`,
  `test_loser_reinforcement_gated_on_positive_confirmation`,
  `test_no_naive_reinforce_suggestion_on_price_drop`,
  `test_thesis_state_from_invalidation_not_price_drop`,
  `test_thesis_state_has_six_honest_states`,
  `test_winner_rules_indicative_never_auto_exit`,
  `test_canonical_positions_table_columns`, `test_no_order_execution_button`,
  `test_performance_migrated_to_portfolio`,
  `test_journal_no_longer_owns_portfolio_performance`.
- Routes 200 (`test_subviews_return_200`, `test_every_primary_route_returns_200`) ;
  `test_no_orders` (READONLY) vert. Gardiens SW v48 mis à jour (3 emplacements).

## 14. Contrôle navigateur (390 / 768 / 1440)

Débordement réel (hors conteneur de scroll intentionnel) et console applicative,
sur les 7 vues (Synthèse/Positions/Performance/Risque/Options/Watchlist/Journal) :

| Viewport | Débordement | Erreurs console |
|---|---|---|
| **390 mobile** | **0 px** (7/7) | **0** (7/7) |
| **768 tablet** | **0 px** (7/7) | **0** (7/7) |
| **1440 desktop** | **0 px** (7/7) | **0** (7/7) |

- Tableau canonique large → **scroll horizontal intentionnel** (desktop) et
  **cartes par position** (mobile, `vx-table-cards`) conservant ticker/P&L/poids/
  état de thèse/prochaine action.
- Vérifié : Hero + 4 KPI + risque dominant + action prioritaire, états de thèse
  (Intacte/Cassée/À surveiller/Renforcée par les faits), **garde-fou perdants**
  (« Renforcement interdit… » sur PLTR), migration Performance (4 graphiques),
  Diff honnête (« Aucun historique… »).
- Captures : scratchpad `pr5shots/` (desktop synthèse/positions/performance/risque,
  mobile synthèse/positions).

## 15. Erreurs restantes

- Console applicative : **0**. (`ERR_CONNECTION_RESET` = Google Fonts via proxy
  sandbox, non applicatif.)

## 16. Risques techniques

- **État de thèse dépend de la marque** : sans cote (IBKR hors ligne), l'état est
  honnêtement « données insuffisantes » — pas de faux verdict. Les états
  `renforcée`/`fragilisée`/`cassée` supposent un `entrySnap.stop` renseigné ; sinon
  seuls `intacte`/`surveiller`/`insuffisant` s'appliquent (jamais « cassée » sans
  invalidation définie).
- **Concentration Top1/Top3** calculée sur la valeur de marché (repli au coût) ;
  cohérente avec le moteur de risque HHI mais servie côté client (agrégation
  arithmétique simple, aucun calcul financier déplacé).
- **Vue Options** conservée telle quelle (refonte dédiée PR n°7) ; elle reste
  fonctionnelle mais son alignement au premier-écran viendra avec l'espace Options.
- **Diff** dépend de localStorage (fenêtre 12 h) — au premier passage, honnêtement
  vide.
- Validation Chromium **headless** (pas d'appareil physique).

## 17. Plan précis de la prochaine PR — Options

- **Premier écran Options** : stratégie · biais · coût · gain/perte max · breakevens
  · PoP · rendement/risque · échéance · **delta/theta** (gamma/vega/vanna/vomma en
  niveau expert). LEAPS : delta 0,70-0,90, échéance 6-18 mois, OI élevé, spread
  faible.
- **Payoff canonique** : spot, zéro, breakevens, gain/perte max, zones profit/perte,
  hypothèses (source unique `multileg_lab`).
- **Greeks agrégés** uniquement avec IBKR (jamais estimés) ; IV/PoP honnêtes.
- Réconcilier la vue Options du Portefeuille avec l'espace Options (un domicile) ;
  Chart Shell complet ; 0 débordement 390/768/1440 ; 0 console ; SW bump ; READONLY
  intact ; captures avant/après + comptes de graphiques.

## Verdict

**GO.** Le Portefeuille répond à sa question unique : Hero + risque dominant +
action prioritaire, tableau canonique avec **état de thèse honnête** (jamais
« cassée » sur une simple baisse), **garde-fou perdants testé**, concentration
S+/S/A/B, risque priorisé, **performance migrée en domicile unique**, Diff honnête,
mode sans IBKR digne. **926 tests verts** ; **0 débordement** et **0 erreur console**
sur 21 combinaisons vue×viewport ; **READONLY intact**. Fondations posées pour la
refonte de l'espace Options.
