# Vertex — Audit complet de production (Full Production OS)

Audit indépendant du 2026-07-11 (agent dédié, lecture seule) sur `vertex/`
(moteurs, routes, UI redesign, design system) + routes actives de
`terminal.py`. Chaque constat est suivi de la **décision prise** et, le cas
échéant, du correctif livré dans cette passe.

## 1. Hygiène de code

- **TODO/FIXME/XXX** : aucun dans `vertex/`. **`console.log`** : aucun dans
  `vertex/static/vertex/js/` (seul `console.error` légitime du refresh
  manager). → RAS.
- **`except Exception` silencieux** : 99 occurrences / 37 fichiers, la
  grande majorité étant des helpers de parsing (`_f()`, `_num()`) ou des
  dégradations volontaires commentées (`_backup_desk`, webhook TV,
  `market/context.py`). → Acceptés tels quels.

## 2. « Faux zéros » (donnée absente traitée comme 0) — DOCUMENTÉ

Constats les plus risqués (le score/prix qui plante devient un vrai 0) :

| Emplacement | Comportement |
|---|---|
| `vertex/engines/quant_engine.py:58,109,190` | `except → return 0` sur des sous-scores |
| `vertex/engines/quant_engine.py:135` | R:R à 0 sur exception |
| `vertex/engines/track_record.py:63` | fiabilité → 0 sur erreur |
| `vertex/options/legacy_engine.py:26,33` | greeks/prix → 0 silencieux |
| `vertex/engines/decide.py:20` | `d.get('score', 0)` : titre non scoré = score 0 |
| `vertex/engines/options_lab.py:638,645` | prime absente → coût 0 |
| `vertex/options/vol_surface.py:84` | `c.get('strike', 0)` fausse le bucket ATM |
| `vertex/options/legacy_engine.py:349-376` | pénalités danger/theta neutralisées si champ absent |

**Décision** : ces moteurs sont le **chemin legacy** (verdicts historiques du
scan). Le chemin canonique (scenario_pricer, ExecutiveEngine, provenance)
refuse la donnée absente (`None`/refus de simulation — testé par
`test_missing_data_becomes_none`, `test_no_invented_data_anywhere`).
Réécrire le scoring legacy changerait les verdicts historiques du track
record ; on documente ici plutôt que de modifier des sorties calibrées.
Limitation déclarée (`VERTEX_KNOWN_LIMITATIONS.md`).

## 3. Unités options — CORRIGÉ/DOCUMENTÉ

- Conversions **existantes et tracées** : `/api/options/simulate`
  (`redesign.py`) normalise IV %→décimal (`iv>3 → ÷100`) et prime
  par contrat→par action (`mid>spot → ÷100`) avec note de limitation ;
  `scenario_pricer.py` (`cost_per_contract = mid×100`) attend l'IV
  **décimale** ; `legacy_engine.py` manipule l'IV **en %** (÷100 interne,
  ré-export en %).
- **Incohérence inter-moteurs** : le champ `iv` d'un contrat n'a pas la
  même convention selon le moteur lecteur ; la normalisation vit à la
  frontière API. **Décision** : convention canonique = décimal
  (`VERTEX_CALCULATION_REFERENCE.md §3`), gardiens
  `test_percentage_conventions` + `test_iv_scenarios_are_relative` ; tout
  nouvel appel moteur→moteur doit passer par la frontière normalisée.
- **Delta signé vs absolu** : `abs(delta)` appliqué aux bandes de
  catégories (PUT arrive signé négatif) — volontaire, désormais documenté
  (référence des calculs §3) et testé (`test_delta_bands_by_category`).

## 4. Timezones — CORRIGÉ (chemin décisionnel)

- Constat : `datetime.now()` naïf partout sauf `status_service.py` ; sur un
  serveur UTC, le **DTE** d'une option pouvait être surestimé d'un jour en
  soirée (minuit UTC ≠ minuit New York).
- **Correctif livré** : les deux calculs de DTE/échéances passent à
  l'horloge **America/New_York** (`vertex/engines/options_lab.py`
  `_timeline`, `vertex/options/legacy_engine.py` `_ny_now()`).
- Usages naïfs restants **assumés** (granularité jour, non décisionnels) :
  bornes de semaine (`scanner/weekly.py`), clé de backup quotidien
  (`desk.py`), dates démo (`data/demo.py`), `as_of` du track record.

## 5. XSS / innerHTML — RAS (vérifié)

Chaque page redesign définit et applique `esc()` sur les champs texte issus
d'API ; les news sont assainies **côté serveur** (`news_plus.sanitize_news`).
Titres de drawer/modal/toast via `textContent`. Aucune injection API brute
dans `innerHTML` trouvée dans `vertex/ui/pages/*` ni
`vertex/static/vertex/js/*`.

## 6. Timers — RAS actifs, code mort identifié

Nouvelle UI : 3 timers uniques et disciplinés (horloge 30 s, refresh
manager avec garde `document.hidden`, pull desk 120 s). Les `setInterval`
des modules legacy `vertex/ui/*.py` ne sont plus chargés par le shell
redesign (code mort conservé pour référence, non actif).

## 7. Bogues fonctionnels trouvés par l'audit — TOUS CORRIGÉS

1. **Contrat `/api/pos-quotes` cassé** (le client envoyait `{items:…}` et
   indexait par id ; le serveur attend `{positions:…}` et renvoie des clés
   composites `SYM|exp|strike|RIGHT`) → **corrigé** dans
   `portfolio_page.py` et `briefing.py` ; P&L live des positions vérifié en
   navigateur.
2. **Télémétrie orpheline** (`/api/client-log` sans émetteur dans la
   nouvelle UI) → **corrigé** : `vx-core.js` remonte `window error` +
   `unhandledrejection` ; auto-testé de bout en bout (erreur injectée →
   visible dans `GET /api/client-log`).
3. **États dégradés bruyants** (`/api/ibkr/positions` 503,
   `/api/strategy/decision/<sym>` 404 → erreurs console à chaque visite) →
   **corrigé** : HTTP 200 avec `ok:false`/`available:false`, le corps porte
   l'état honnête, la console reste à zéro.
4. **Vue `?view=compare` d'`/analysis`** : paramètre accepté mais ignoré
   (redirection legacy `/compare`) → **assumé**, limitation déclarée n° 11
   (comparateur redirigé vers la recherche Analyse).

## 8. Routes orphelines — DOCUMENTÉ

30 routes API restent servies sans consommateur dans la nouvelle UI
(liste exhaustive : `VERTEX_ROUTE_MATRIX.md §4`). **Décision** : conservées
comme API publiques internes (tests, usage externe, iPhone raccourcis) —
aucune suppression sans redirection ; les deux plus notables (`/news-feed`
assaini mais non affiché, `/api/options-lab` research center sans point
d'entrée) sont déclarées comme limitations produit à trancher par
l'utilisateur.
