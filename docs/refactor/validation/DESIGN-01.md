# Validation — PR Design n°1 : Design System & Chart System

> Branche `agent/vertex-total-rebuild`. Périmètre STRICT : fondations design.
> **Pas de refonte de contenu de page, pas de fusion de graphiques doublons,
> aucun moteur financier modifié pour une raison esthétique, IBKR READONLY intact.**
> Fondée sur `docs/refactor/PRODUCT_EXPERIENCE_REVIEW.md`.

## 1. Fichiers modifiés

**Tokens & shell**
- `vertex/static/vertex/css/tokens.css` — typo officielle (Inter + JetBrains Mono).
- `vertex/ui/shell/__init__.py` — font-link Google Fonts → JetBrains Mono.
- `vertex/app/routes/system.py` — bump service worker `td-shell-v43 → v44`.

**Chart Shell & composants**
- `vertex/static/vertex/js/charts/chart-core.js` — Chart Shell canonique étendu
  (`C.card` + `C.freshnessBadge` + `C.cardState`/`C._stateBody`).
- `vertex/static/vertex/css/components.css` — composants canoniques (Verdict Card,
  Scenario Card, Freshness Badge, badge Unité, état Insufficient).
- `vertex/static/vertex/css/responsive.css` — anti-débordement étendu à la tablette.

**Présentation honnête & purge couleurs**
- `vertex/ui/pages/intelligence_page.py` — état DATA_INSUFFICIENT calme et explicite.
- `vertex/ui/pages/analysis_page.py` — doc de l'échelle de repli chandeliers.
- `vertex/ui/pages/{briefing,portfolio,performance,system,design_system}_page.py`,
  `opportunities_page.py`, `static/vertex/js/pages/{options-intel,tracking}.js` —
  purge des fallbacks couleur inline périmés (`#8f8a83`, `#48631b`).

**Tests**
- `tests/test_design_system_v1.py` (nouveau, 9 gardiens).
- `tests/test_production_guards_canonical.py`, `tests/test_ui_v3.py`,
  `tests/test_redesign_ui.py` — SW `v44`.

## 2. Composants créés / consolidés

| Composant | Statut | Emplacement |
|---|---|---|
| Chart Shell (titre·question·conclusion·période·**unité**·source·**fraîcheur**·légende·aide·**résumé accessible**·**skeleton/vide/périmé/erreur**) | **étendu** | `chart-core.js` `C.card` |
| Freshness Badge (live/delayed/stale/demo/offline/missing) | **créé** | `C.freshnessBadge` + `.vx-freshness` |
| Verdict Card (hero verdict + score/40 + confiance + entrée + invalidation) | **créé** | `.vx-verdict-card` |
| Scenario Card (pessimiste/probable/exceptionnel) | **créé** | `.vx-scenario` / `.vx-scenario-grid` |
| État Insufficient (DATA_INSUFFICIENT honnête) | **créé** | `.vx-insufficient` |
| Card, KPI, Alert, Table, Tabs, Segmented, Chip, Button, Tooltip, Drawer, Modal, Skeleton, Empty, Stale, Error, Demo badge, Live-dot | **confirmés canoniques** (déjà présents) | `components.css`, `states.css`, `buttons.css`, `control-surface.css` |

## 3. Moteur de chandeliers retenu + justification

**Retenu : TradingView Lightweight Charts (`VXCharts.lwCandlestickCard`).**
- Contrôle navigateur `/analysis/ACN` (symbole scanné, données réelles démo) :
  `#an-chart` contient **un unique `.vx-lwc`** → LWC est bien le moteur qui rend.
  Aucun double rendu (les autres `canvas` de la page sont d'autres graphiques :
  radar de scorecard, etc.).
- Justification : rendu pro (chandeliers nets, zoom/pan natif, overlays MM + plan
  d'entrée/stop), lib vendorée (`vendor/lightweight-charts…`, pur frontend, aucun
  ordre).
- `candlestick-chart.js` (Canvas) et `price-chart.js` (ligne) sont **conservés
  comme échelle de repli honnête** (LWC → Canvas → ligne), documentée dans
  `analysis_page.py`. Aucun retrait : cela casserait un fallback nécessaire (la
  consigne l'interdit). Le « chargement concurrent » n'était pas un double rendu
  mais une échelle de dégradation — clarifiée en commentaire.

## 4. Résultats exacts des tests

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **908 passed, 2 skipped** (baseline PR n°1 : 899
  → +9 gardiens design, aucun désactivé).

## 5. Contrôle navigateur 390 / 768 / 1440

Overflow réel (contenu hors conteneur de scroll intentionnel) :

| Viewport | Résultat |
|---|---|
| **768 (tablette)** | **7/7 pages OK** (briefing corrigé : 844 → OK) |
| **390 (mobile)** | OK (briefing/markets vérifiés ; règles ≤768 renforcent ≤640) |
| **1440 (desktop)** | 7/7 OK |

Assets servis confirmés : `tokens.css` = JetBrains Mono ; font-link = `JetBrains+Mono` ;
`components.css` = `vx-verdict-card`/`vx-freshness`/`vx-insufficient` ;
`chart-core.js` = `freshnessBadge`/`_stateBody`/`opts.summary` ; `/sw.js` = `td-shell-v44`.

## 6. Captures avant / après

- « Après » (scratchpad `after/`) : `after-analysis-ACN-desktop.png` (chandeliers
  LWC + overlays), `after-briefing-tablet.png` (768, sans débordement).
- « Avant » : captures de baseline en scratchpad `shots3/` (PR n°1).
- Note honnête : rendu Chromium **headless** dans le conteneur ; la police
  JetBrains Mono/Inter provient de Google Fonts (repli système si le proxy
  bloque le réseau — le nom de famille officiel reste correct).

## 7. Erreurs console

- `GET /api/client-log` → `{"count":0,"errors":[]}` — **0 erreur applicative**.
- Une entrée navigateur `ERR_CONNECTION_RESET` observée = ressource externe
  (Google Fonts via proxy sandbox), **pas** une erreur JS de l'app.

## 8. Preuve du bump service worker

`vertex/app/routes/system.py` : `const CACHE='td-shell-v44'` ; `/sw.js` sert
`td-shell-v44` (vérifié live). Gardiens mis à jour :
`test_production_guards_canonical.py:304`, `test_ui_v3.py:229-230`,
`test_redesign_ui.py:305-306` (v44 présent, v43 absent).

## 9. Risques & reste à faire

**Risques maîtrisés**
- Extension du Chart Shell **rétrocompatible** (nouveaux champs optionnels ;
  les ~55 appels existants ne passent ni `unit`/`freshness`/`summary`/`state`).
- Aucun moteur financier touché ; READONLY intact ; `test_no_orders` vert.

**Reste à faire (PR suivantes)**
- **Adopter** les nouveaux composants dans les pages (Verdict/Scenario/Freshness
  Badge, états du Chart Shell) — c'est la refonte page par page, hors périmètre ici.
- Réduire les **1 682 `style=` inline** de `terminal.py` (sweep mécanique, PR nettoyage).
- Fusionner les graphiques doublons (jauges ×3, secteurs ×4) — PR pages.
- Convertir certaines tables larges en cartes mobiles (scroll résiduel toléré).

## Verdict

**GO.** Les 6 items du périmètre sont livrés, testés et vérifiés au navigateur ;
908 tests verts ; 0 erreur console applicative ; SW bumpé. La couche design est
prête à porter la refonte page par page.
