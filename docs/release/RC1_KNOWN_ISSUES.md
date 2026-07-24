# Vertex — RC1 Known Issues

> Classement par sévérité. **Aucun bloquant / majeur** n'a survécu à la stabilisation.
> Les éléments listés sont acceptés pour RC1 (interne, non public, pas de merge `main`).

## Bloquant (empêche RC1)
**Aucun.** Critères GO tous satisfaits : compileall vert, pytest vert, 0 endpoint
d'ordre (prouvé), READONLY prouvé, 0 erreur console applicative, 0 débordement
critique, 0 faille critique connue, 0 donnée inventée, démo/sans-IBKR/stale/missing/
insufficient corrects, service worker cohérent, documentation complète, rollback
documenté.

## Majeur (à corriger avant une release publique — hors périmètre RC1)
**Aucun connu.**

## Mineur (accepté pour RC1)
1. **Vues Options legacy** (`overview` / `radar` / `scenarios`) encore servies hors barre
   d'onglets (routes 200, test-gardées `test_options_routes.py`). Le parcours canonique
   passe par **Structure** (désormais le défaut de `/options`). Retrait propre + mise à
   jour des tests = travail post-RC1.
2. **`terminal.py` monolithe** (~10 700 lignes) : cartographié (cf. RC1-STABILIZATION
   §terminal.py) mais **non extrait** en RC1 (règle « aucun déplacement non testé,
   pas de migration big-bang »). Extraction incrémentale post-RC1.
3. **Endpoints legacy non consommés** par le frontend : `/api/strategie`, `/api/comite`,
   `/api/weekly`, `/api/correlations/<sym>`, `/api/risk`, `/api/portefeuille`,
   `/api/company/twin/<sym>` (holdovers de l'ère monolithe). Non retirés en RC1 (leur
   suppression exige une revue de contrat + tests dédiés). Aucun n'expose d'ordre.
4. **`intelligence_page.py`** (espace hors-nav transitionnel `/intelligence`, absorbé
   par Analyse) conserve du **vouvoiement** et un `<h1>Intelligence</h1>`. Hors des 8
   espaces canoniques ; normalisation/retrait post-RC1.

## Cosmétique (accepté pour RC1)
5. **Styles inline** : 335 attributs `style=` répartis sur les pages (pics :
   `system_page.py` 49, `design_system_page.py` 49, `analysis_page.py` 48). Migration
   vers classes utilitaires = amélioration progressive, sans impact fonctionnel.
6. **Composants à consolider** : `.vx-stat*` dupliqué (options_intel + tracking) ;
   badges démo fragmentés (`.vx-badge-demo` / `.vx-demo-tag` / `.vx-hypo`) ; override
   local `.vx-verdict-card` dans `options_intel_page.py` ; `.vx-chip` réparti sur 3 CSS.
   Convergence canonique = travail de finition (aucun bug de rendu observé).
7. **Taxonomie d'états** partiellement scindée : `LIVE/DELAYED/OFFLINE` via tokens JS,
   `STALE/DEMO` via `data-state` CSS, insuffisance via `VX.states.empty()` FR. Cohérent
   à l'affichage ; unification de l'enum = amélioration.
8. **Label « Watchlist »** (anglais) comme titre de carte dans Portefeuille — terme
   financier standard, conservé.

## Limites environnementales (non applicatives)
- **Google Fonts** bloquées par le proxy sandbox → `ERR_CONNECTION_RESET` réseau (non
  applicatif ; la police système prend le relais). En production hors sandbox, non
  applicable.
- Validation navigateur en **Chromium headless** (pas d'appareil physique dans cet
  environnement) — contrôle sur appareil réel recommandé avant release publique.
- **Greeks/PoP options** = estimations modèle (lognormal) étiquetées « estimation » ;
  fiables uniquement avec IV réelle. Sans IBKR : « Insufficient » honnête.
