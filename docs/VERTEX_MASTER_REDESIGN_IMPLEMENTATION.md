# VERTEX MASTER REDESIGN — Rapport d'implémentation

Date : 2026-07-11 · Branche : `claude/vertex-strategy-os-h17dso`
Baseline : 414 tests → Final : **448 tests verts** · 0 erreur console sur
17 pages/vues (Chromium réel).

## 1. Audit initial

Voir `docs/VERTEX_MASTER_REDESIGN_AUDIT.md` : 56 routes, 3 générations de
pages incompatibles, 2 navigations concurrentes, 5 copies de sidebar,
4 copies de la logique de sync, 3 helpers KPI, 2 paradigmes graphiques.
Captures avant : `docs/redesign/before/` (20 captures).

## 2. Architecture avant / après

**Avant** : monolithe `terminal.py` servant ~25 pages HTML en chaînes Python,
navigation rail legacy + nav.py, styles par page.

**Après** :
```
vertex/ui/shell/            shell unique (sidebar 8 espaces, topbar, drawers,
                            palette ⌘K, toasts, mobile action bar)
vertex/ui/pages/            briefing, markets, opportunities, portfolio,
                            analysis (fiche canonique), performance,
                            intelligence, system
vertex/app/routes/redesign.py  routes + 43 redirections legacy + assets +
                            /api/briefing/editorial + /api/options/simulate
vertex/static/vertex/css/   design system 9 fichiers (tokens → utilities)
vertex/static/vertex/js/    vx-core (bus, contexte, refresh), vx-entities
                            (actions universelles), vx-shell (interactions)
vertex/static/vertex/js/charts/  22 modules (contrat §34)
```
Le monolithe conserve TOUTES ses APIs (strangler pattern) ; ses pages HTML
sont neutralisées (43 décorateurs commentés) et redirigées.

## 3. Navigation & mapping des routes

8 espaces : `/` Briefing · `/markets` · `/opportunities` · `/portfolio` ·
`/analysis(/<sym>)` · `/performance` · `/intelligence` · `/system`, chacun
avec ses sous-vues `?view=` (§10).

Redirections 301 (avec conservation ticker/vue/filtres) — extraits :
`/titre/<sym>`→`/analysis/<sym>` · `/strategie`→`/portfolio` ·
`/ma-page`,`/watchlist`,`/suivi`→`/portfolio?view=watchlist` ·
`/options*`→`/opportunities?view=options` · `/sectors`,`/heatmap`→
`/markets?view=sectors` · `/catalysts`→`/opportunities?view=calendar` ·
`/anomalies`→`/opportunities?view=anomalies` · `/journal`,`/decisions`→
`/performance?view=journal` · `/review`→`/intelligence?view=committee` ·
`/vault`,`/archive`→`/system?view=archive` · `/settings`,`/health`→`/system` ·
`/brief`→`/` · `/strategy-os`→`/intelligence` (liste complète :
`LEGACY_REDIRECTS`, testée route par route).

Pages fusionnées : 4 fiches concurrentes (titre/stocks/entreprises/compare)
→ 1 fiche canonique ; journal + décisions → Performance ; brief + review +
research + equipe + bordel + strategy-os → Intelligence ; settings + health +
vault → Système. Pages supprimées : aucune sans redirection.

## 4. Design system

`tokens.css` : palette canonique exacte §7 (fonds #050811→#16243B, bordures
bleutées, texte 4 niveaux, accents bleu/cyan/violet/vert/rouge/orange), Inter
+ mono tabulaire, hiérarchie 30/19/13/11, rayons 6-14 px, espacements 4-64,
grille 12 colonnes, max 1600 px. Règles §7 respectées : couleurs financières
sémantiques uniquement, pas de glow généralisé, ombres discrètes, aucune
animation continue (shimmer des skeletons uniquement, coupé en
reduced-motion).

## 5. Composants & interactions

Tous les composants §16 sont implémentés (shell, badges décision/risque/
statut/entités, tableaux premium avec tri/sticky/actions/cartes mobiles,
drawer, modal, palette de commandes clavier, toasts, menus contextuels
clavier, états LOADING/READY/EMPTY/STALE/ERROR, UpdateIndicator §38,
EmptyState avec action utile, ScenarioMatrix, Timeline, MobileActionBar).

**Actions universelles** (`vx-entities.js`) : un seul module pour favoris /
watchlist / suivis / positions / alertes / notes-thèses / journal — schémas
localStorage historiques préservés à l'identique (myFavs, myRecos, myTrades,
vxAlerts, vxJournal…), nouvelle clé `vxWatchlist` ajoutée aux 4 listes de
sync (gardiens de test mis à jour), protocole `/api/desk` inchangé
(last-writer-wins, jamais écraser du plus récent). Menu `data-entity-menu`
et ouverture d'analyse `data-open-analysis` disponibles partout. Formulaire
progressif « + Ajouter » (ticker → destination → détails → confirmer).

**Contexte de navigation** (`VXContext`) : page/vue/filtres/tri/scroll/
sélection sauvegardés (sessionStorage `vxNavigationContext`), bouton retour
étiqueté (« Retour aux opportunités »…) qui restaure la sous-vue, les filtres
et le scroll.

## 6. Graphiques

22 modules sur un moteur unique (Chart.js déjà embarqué — aucune bibliothèque
concurrente ajoutée). Contrat §34 appliqué par `chart-core.card()` : titre,
question, conclusion, timeframe, contrôles, source, horodatage, mode
live/delayed/fallback, limites, bouton « Comprendre ce graphique » ouvrant le
drawer 4 sections (montre / pourquoi / confirmerait / invaliderait).
Annotations : niveaux entrée/stop/TP/support/résistance + marqueurs earnings ;
création d'alerte depuis un niveau réel (`alertFromLevel`). Options §35 :
payoff (arithmétique du contrat), matrice de scénarios, theta et sensibilité
IV alimentés par le moteur `scenario_pricer` via `/api/options/simulate` —
l'UI ne price jamais. Candlesticks : rendus uniquement si OHLC fourni, sinon
repli honnête en clôtures avec limitation affichée.

## 7. TradingView / IBKR / Claude dans l'expérience

- TradingView : signaux affichés sur la fiche (statut à confirmer/expiré),
  mention explicite « jamais un ACHETER direct », ouverture externe,
  création d'alerte, webhook §32 inchangé. Aucune donnée inventée si absent.
- IBKR : provenance et fraîcheur sur chaque donnée critique
  (UpdateIndicator), statuts Live/Différé/Hors ligne/Fallback dans le drawer
  Connexions et Système/Connexions, invariant READONLY affiché, marques de
  positions via `/api/pos-quotes` avec repli honnête.
- Claude : Intelligence/Analyste consomme le moteur exécutif ; encadré
  « Claude explique, ne décide jamais » ; brief éditorial §21 composé du
  paquet moteur avec générateur déterministe en repli (jamais de texte
  générique).

## 8. Responsive / accessibilité / performance

- 7 viewports testés (captures avant/après) ; mobile : bottom navigation,
  action bar contextuelle sur la fiche, tableaux → cartes, cibles ≥ 40 px,
  `overflow-x: clip` global.
- Accessibilité : focus-visible, aria-current/aria-selected/aria-label/roles,
  Échap ferme tout, navigation clavier palette et menus, reduced-motion,
  jamais d'information portée par la couleur seule (signes ± et libellés).
- Performance : Refresh Manager (dédup fetch, TTL, AbortController, retries
  bornés, suspension quand l'onglet est caché), registre de charts anti-
  canvas-orphelins, cache borné (80 entrées), aucun alert()/confirm().

## 9. Synchronisation

`/api/desk`, `deskTs` et le last-writer-wins sont intacts. Source canonique
des clés : `VXEntities.DESK_KEYS` (17 clés = 16 historiques + `vxWatchlist`),
alignée sur `__DESK_KEYS` (terminal), `vx_kit`, `journal`, `vault` — gardée
par `test_all_sync_keys_are_canonical` + test historique mis à jour.
Préférences locales non synchronisées volontairement device-specific :
`vxSidebarState`, `vxNavigationContext` (session), `vxRecentTickers`,
`vxDashboardLayout`, `vxNotificationPrefs`.

## 10. Service worker

`td-shell-v6` (bump — le shell a changé), anciens caches purgés par le SW
existant, version testée (`test_service_worker_bumped`).

## 11. Tests

448 verts au total, dont ~45 nouveaux (`tests/test_redesign_ui.py`) :
navigation 8 items, 200 sur toutes les routes et sous-vues, 43 redirections,
fiche unique, shell partagé, ids uniques, liens morts, brief (timestamp/
sources/fallback/longueur), contrat graphique, états de données, formats de
fraîcheur, clés de sync canoniques, schémas préservés, pull anti-écrasement,
actions universelles complètes, aucun dialogue bloquant, contexte/retour,
palette clavier, TV jamais un achat, IBKR visible, accessibilité,
reduced-motion, SW bumpé, zéro chemin d'ordre dans l'UI. Parcours navigateur
§50 exécutés en Chromium réel (voir rapport final). Tests historiques
adaptés aux redirections (journal, vault, smoke) — aucun invariant produit
affaibli.

## 12. Limitations restantes

- Candlesticks OHLC : le scan n'expose que les clôtures — le mode bougie
  attend des barres complètes des moteurs (repli honnête en ligne).
- Moyennes mobiles en série : le moteur expose ma20/50/200 ponctuels, pas
  les séries — non tracées (jamais recalculées côté UI).
- Le comparateur multi-titres historique (/compare) redirige vers Analyse ;
  la comparaison côte à côte reviendra comme sous-vue dédiée.
- Simulateur paper-trading legacy (simCash/simTrades) : données préservées
  et synchronisées, UI dédiée non recréée (consultable via export Système).
- Advance/decline et nouveaux hauts/bas : non fournis par les moteurs — non
  affichés (honnêteté), documenté sur Marchés/Breadth.
- Le brief éditorial est déterministe par défaut ; la reformulation Claude
  du même paquet pourra s'y brancher (validation stricte déjà en place).

## 13. Lancement

`python terminal.py` → http://127.0.0.1:5002 (verrou `VERTEX_CODE` inchangé).
Cloud/démo : `NO_IBKR=1 DEMO=1`. Tests : `python -m pytest tests/ -q`.
Captures : `docs/redesign/before/` et `docs/redesign/after/`.
