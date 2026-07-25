# CONTINUITY — LOT 1 · Audit de navigation & contrats de données

**Objectif du chantier** : faire de Vertex une **application continue unique** — navigation
instantanée, données conservées, prix live cohérents, snapshots analytiques persistants,
identité claire (live / snapshot / sauvegardé / stale / recalcul), bascule atomique de session.

**Périmètre du LOT 1** : audit only. **Aucun changement fonctionnel ni visuel.** Ce document
cartographie l'existant, propose l'architecture cible, liste routes/fichiers/risques, pose un
plan d'exécution par lots et des métriques de base mesurées.

Invariants non négociables (rappel) : **READONLY absolu** (aucun ordre), **données réelles
uniquement** (absent → `n/d`), **tests 100 %**, moteurs financiers inchangés.

---

## 0. Méthode & sources

- 4 cartographies parallèles (routes, shell/rendu, flux client, flux serveur), lecture seule.
- Mesures navigateur réelles (Playwright, Chromium 1440×900, mode DÉMO) : requêtes/page,
  poids, appels `/api` par page, test de rechargement à la navigation, temps de peinture.
- Fichiers pivots : `terminal.py`, `vertex/app/routes/*.py`, `vertex/ui/shell/__init__.py`,
  `vertex/ui/pages/*.py`, `vertex/static/vertex/js/{vx-core,vx-shell,live-updates,vx-entities}.js`,
  `vertex/app/state.py`, `vertex/engines/session_digest.py`.

---

## 1. MÉTRIQUES DE BASE (mesurées)

Contexte DÉMO local. Chaque page ouverte **à froid** (cache mémoire vide — ce qui reflète
exactement l'état après chaque navigation, puisque le shell recharge, cf. §3).

| Page | Appels `/api` | Requêtes totales | HTML | Poids total |
|---|---|---|---|---|
| Aujourd'hui | 12 | 41 | 33 KB | 467 KB |
| Marchés | 6 | 38 | 63 KB | **1000 KB** |
| Opportunités | 6 | 41 | 55 KB | **999 KB** |
| Analyse MSFT | 12 | 43 | 56 KB | 651 KB |
| Portefeuille | 5 | 39 | 68 KB | 486 KB |
| Options | 7 | 40 | 20 KB | 541 KB |
| Journal | 5 | 32 | 37 KB | 450 KB |
| Système | 11 | 40 | 70 KB | 487 KB |

**Faits mesurés majeurs :**

- **Navigation = rechargement complet du document.** Un clic sur un lien de nav déclenche
  bien une navigation de frame principale (MPA classique, confirmé). Pas de routeur client.
- **5 appels API identiques repartent sur les 8 pages** (cache mémoire détruit à chaque
  reload) : `/api/desk`, `/api/live/status`, `/api/live/events`, `/api/market/summary`,
  `/api/session/digest` — soit **~40 requêtes API redondantes** pour un simple tour des 8 pages.
- **Police Google Fonts bloquante** : le `<link>` `css2?family=Inter` du `<head>` du shell
  met **~1,8 s** (mesuré sur /portfolio) et jusqu'à plusieurs secondes de timeout en cold
  start. Comme le shell recharge à **chaque** navigation, ce coût est **repayé à chaque page**.
- Pages Marchés/Opportunités ≈ **1 Mo** (chart.umd + modules de charts rechargés à chaque fois).

> Note environnement : les temps « load » bruts (~13 s uniformes) sont un artefact du bac à
> sable (CDN Google Fonts filtré par le proxy → timeout). Le signal fiable est ci-dessus :
> nombre de requêtes, redondance inter-pages, poids, et le blocage police réel.

---

## 2. PROBLÈMES ACTUELS (synthèse priorisée)

**P1 — Architecture MPA : le shell est détruit et reconstruit à chaque navigation.**
Aucun routeur client, liens `<a href>` nus, aucun `pushState`/`popstate`/fetch de fragment.
`render_shell()` ré-émet le document entier (17 feuilles CSS + police Google + 7 scripts +
sidebar + topbar + palette + overlays) à **chaque** route. → flashs, re-parse, re-exécution
des IIFE, perte de tout l'état mémoire. C'est la cause racine de presque tout le reste.

**P2 — Aucune conservation des données entre pages.** Le cache `VX.fetch` est une `Map`
mémoire (`vx-core.js:197`) anéantie à chaque reload. Toute donnée est re-fetchée « from
scratch » en arrivant sur une page ; les TTL (ex. `/api/names` ttl 10 min) sont inutiles
d'une page à l'autre. Seuls survivent `localStorage` (desk/favoris/sidebar/tickers) et
`sessionStorage` (contexte de nav : filtres + scroll, pas les données).

**P3 — Redondance des appels transverses.** `/api/market/summary`, `/api/market/regime`,
`/api/live/status`, `/api/session/digest`, `/api/desk`, `/api/pos-quotes` sont consommés par
plusieurs pages avec **des TTL divergents** (ex. `/scan` : 120 s côté Marchés vs 300 s côté
Portefeuille ; `/api/live/status` : 60 s / 0 / 30 s selon l'appelant). Pas de source unique.

**P4 — Pas de couche « prix live » centrale.** `/api/pos-quotes` (POST, jamais caché) est
rappelé indépendamment par Aujourd'hui, Portefeuille et Options. Rien ne garantit qu'un même
ticker affiche le même prix partout, ni ne distingue prix live vs prix de référence du snapshot.

**P5 — Pas de session analytique atomique.** `scan_state` est **un unique dict global muté en
place, en continu**, par 12 boucles à cadences différentes (scan 120 s, options 120 s, fund 6 h,
edge 6 h, weekly 5 min, cal 3 h, indices ~12 s…). Un lecteur peut observer un état composite
(rows du cycle N, committee du cycle N-1, options du cycle N-3). **Pas de `session_id`, pas de
snapshot figé, pas de manifest, pas de bascule atomique.** Le seul instantané est le digest
compact de `session_api.py`.

**P6 — Fraîcheur incohérente et partielle.** 3 surfaces de fraîcheur (`/scan` stale 900 s,
`/healthz` chip 420 s, `/api/live/status` 300/1800 s) avec des seuils différents. `scan_ts_h`
est lu (`session_digest.py:70`) mais **jamais écrit** → toujours `None`. Pas de système visuel
unifié live / snapshot / sauvegardé / stale / recalcul / erreur.

**P7 — `VX.fetch` : pas de robustesse concurrentielle.** Dédup in-flight ✔, mais : **pas de
stale-while-revalidate**, **pas de protection contre les réponses hors-ordre** (la dernière
réponse écrit le DOM même périmée), `AbortController` créé mais **jamais relié** aux navigations
ni au changement de vue/symbole (aucune annulation effective), éviction FIFO (pas LRU), aucune
persistance, aucune invalidation ciblée (seulement `cache.clear()` global au bouton refresh).

**P8 — Coût de rendu fixe repayé à chaque page.** Police bloquante (~1,8 s+), 17 CSS + 7 JS
re-parsés, chart.umd rechargé, placeholders → valeur (horloge `—`, statut « État… », skeletons)
à chaque navigation. Le Service Worker est **network-first** et **ne précache PAS** le shell/CSS
/JS à l'install (`system.py:212` ne met que manifest + 1 icône) → cold start = attente réseau.

**Bonne nouvelle confirmée : aucune navigation ne déclenche un scan des ~517 sociétés.**
`scan()` n'est appelé que par le worker `_loop` (`terminal.py:666`). Les re-scans sont
explicites (`/api/rescan`, `/api/live/refresh`) et asynchrones (Event → thread de fond), la
requête HTTP retourne immédiatement. **Le risque « une page relance un scan lourd » n'existe pas
aujourd'hui — il faudra le préserver dans la refonte.**

---

## 3. ARCHITECTURE ACTUELLE

### 3.1 Navigation & shell (MPA pur)
- `PRIMARY_NAV` : 8 espaces canoniques — `vertex/ui/shell/__init__.py:18-27`
  (briefing `/`, markets `/markets`, opportunities `/opportunities`, analysis `/analysis`,
  portfolio `/portfolio`, options `/options`, journal `/journal`, system `/system`).
- `render_shell()` `shell/__init__.py:151-204` : document complet à chaque route
  (`_sidebar` 58-79, `_topbar` 82-105, `_mobile_bar` 108-121, `_OVERLAYS` 124-148,
  17 `<link>` CSS 166-181, police Google 163-165, 7 `<script>` 196-202).
- Liens de nav = ancres nues `<a href>` (`:62-64`, `:117-118`) — **aucun** `preventDefault`.
- Navigations programmées = rechargements durs `location.href` (`vx-core.js:183`,
  `vx-shell.js:82,224`, `vx-entities.js:255-257`). Aucun `pushState` dans tout le code applicatif.
- `SHELL_VERSION='vx-shell-1'`, émis sur `<body data-shell>`.

### 3.2 Rendu des pages
- 14 routes HTML dans `vertex/app/routes/redesign.py` (make_blueprint) ; chaque page
  `vertex/ui/pages/*.render()` enveloppe son contenu dans `render_shell`. Sous-vues par `?view=`.
- Les anciennes routes HTML de `terminal.py` sont neutralisées (`# [redesign] migrée`).
- 41 redirections legacy 301 (`LEGACY_REDIRECTS`, `redesign.py:19-59`) + `/titre/<sym>`,
  `/company/<sym>` → `/analysis/<sym>`.

### 3.3 Données client
- Noyau `vx-core.js` : `VX.fetch` (cache `Map` TTL + dédup in-flight, éviction FIFO 80,
  `:199-225`), `VX.refresh` (setInterval, `:226-249`), `VX.bus` (événements), `VX.context`
  (sessionStorage : filtres+scroll, `:137-177`), préchauffage idle `/api/session/digest` +
  `/api/market/summary` (`:256`).
- Socle rechargé sur **chaque** page : `/api/live/status` (shell + live-updates),
  `/api/system/diagnostics`, `/api/alerts/active`, `/api/names`, `/api/desk`, `/api/live/events`.
- Par page : voir §7 (matrice endpoints).

### 3.4 Données serveur (3 couches mélangées dans un seul dict)
- `scan_state` (`vertex/app/state.py:15`) : muté en place par 12 boucles `while True`
  (`terminal.py`). LIVE (`_quotes_worker` ~s, `_indices_loop` ~12 s, `_news_loop` 60 s,
  `_radar_loop` 240 s), SNAPSHOT (`_loop`/`scan()` 120 s, `_fund_loop` 6 h, `_edge_loop` 6 h,
  `_weekly_loop` 5 min, `_opt_loop` 120 s, `_cal_loop` 3 h).
- Caches disque `*_cache.json` (persist.py) : fund, options, optall, macro, radar, edge, cal,
  breadth_history, daily_prev, alerts_fired, **session_digest_cache**, company (survivent au
  restart, gitignorés).
- Fraîcheur : `scan_ts` (epoch), `updated` (HH:MM:SS), `/api/live/status` (live_engine,
  domaines + seuils), `/healthz` `scan_age`. `session_digest.build()` = seule « photo » figée.

---

## 4. ARCHITECTURE CIBLE

Principe directeur : **un shell persistant + un store client unique + trois couches de données
explicitement séparées et versionnées**, sans jamais bloquer l'écran ni casser READONLY.

### 4.1 Trois couches (contrats)
Chaque donnée servie expose un **enveloppe de fraîcheur** homogène :
```
{ value, source, ts, freshness: live|snapshot|saved|stale|refreshing|error,
  session_id?, age_s }
```

- **A · LIVE** (prix, bid/ask, variation, indices, VIX, statut marché, P&L, IBKR, alertes,
  horloge) : polling borné (secondes→minutes), aucune analyse lourde. **Source de prix
  centrale unique** côté client (un ticker → un prix partout), distincte du prix de référence
  du snapshot et du prix moyen d'achat.
- **B · SNAPSHOT ANALYTIQUE** (régime, breadth, secteurs, fondamentaux, technique, momentum,
  scores, grades, asymétrie, scénarios, catalyseurs, news, risques, portefeuille, options,
  opportunités) : produit par une **session** identifiée (`session_id`), recalcul périodique,
  **remplacement ATOMIQUE** uniquement quand la session est complète et validée (manifest).
- **C · SAUVEGARDÉ** (dernières sessions, analyses titres, watchlists, préférences, navigation
  récente, état widgets, filtres, ticker sélectionné, historique sessions, dernière page) :
  persistance (localStorage + `/api/desk` + caches disque + snapshots serveur).

### 4.2 Shell persistant (MPA → app continue)
Convertir en navigation client **sans casser les URL** : le shell (`vx-app`, sidebar, topbar,
palette, overlays, barre mobile) **ne se détruit plus** ; seul `#vx-content` (zone principale)
est remplacé. Approche pragmatique **progressive-enhancement** :
1. Les liens `[data-nav-id]` et `<a href>` internes sont interceptés → `history.pushState` +
   fetch d'un **fragment de contenu** (nouvelle route serveur renvoyant le HTML de la page
   **sans** le chrome shell), injecté dans `#vx-content` ; `popstate` géré.
2. Repli **sans-JS** : les mêmes URL servent toujours le document complet (deep link, refresh,
   nouvel onglet, bouton retour intacts). Zéro régression MPA.
3. Le shell relit l'état depuis le store (pas de flash placeholder→valeur).

### 4.3 Store global client (`VX.store`)
Un store unique conscient de : `active_session_id`, `previous_session_id`, `session_status`,
`session_progress`, `live_prices`, `market_status`, `active_ticker`, `selected_timeframe`,
`cached_pages`, `portfolio_state`, `opportunities_state`, `news_state`, `connection_state`,
`freshness_map`, `errors`, `pending_requests`. Règles : **dédup** (une requête identique ne part
pas 2×), **stale-while-revalidate** (afficher le sauvegardé immédiatement, revalider en fond,
ne jamais vider), **annulation** des requêtes obsolètes (relier `AbortController` au
changement de page/vue/ticker), **jeton de génération** anti-réponse-hors-ordre, **isolation
par `session_id`** (jamais mélanger deux sessions). Persistance légère (sessionStorage /
IndexedDB) pour survivre au reload dur.

### 4.4 Session analytique atomique (serveur)
Introduire un **conteneur de session** immuable : quand un cycle de scan se termine, publier un
snapshot **complet et cohérent** sous un nouveau `session_id` + `manifest` (timestamps,
couverture, qualité, absence d'erreur critique) ; **basculer `active_session_id` d'un coup** ;
notifier les clients (toutes les pages lisent le même snapshot). Conserver l'ancienne session
tant que la nouvelle n'est pas validée (jamais remplacer du valide par du vide). Le live reste
un overlay séparé au-dessus du snapshot. *Contrainte : n'ajoute aucun recalcul — enrobe l'état
déjà produit ; READONLY intact.*

### 4.5 Identité visuelle unifiée
Un composant discret et cohérent (déjà amorcé par la « Session d'analyse » v64) : point vert
LIVE, label Analyse + heure + `session_id`, Sauvegardé + date, À actualiser + âge + raison,
Recalcul + progression (ancienne donnée visible), Erreur localisée + dernier résultat valide.
Seuils de stale **unifiés** (une seule table).

### 4.6 Navigation instantanée
Préchargement ciblé (idle/hover/focus/proximité viewport/historique), transitions courtes
(crossfade + skeleton local), rendu progressif (cache d'abord, frais injecté ensuite).
Cibles : réponse au clic < 100 ms, contenu cache < 150 ms, aucun scan lourd déclenché.

---

## 5. ROUTES CONCERNÉES

- **Pages (14)** : les 8 espaces (`/`, `/markets`, `/opportunities`, `/analysis[/<sym>]`,
  `/portfolio`, `/options`, `/journal`, `/system`) + hors-nav (`/intelligence`, `/tracking`,
  `/design-system`, `/system/design-system`, `/widget-lab`). → chacune devra exposer un
  **rendu de fragment** (contenu sans shell) en plus du rendu complet.
- **Nouvelle(s) route(s) à prévoir (LOT 2+)** : fragment de contenu par page (ex.
  `?fragment=1` ou en-tête `X-Vertex-Fragment`), `/api/session/manifest` +
  `/api/session/active` (id + statut + progression), `/api/prices` (source live centrale).
- **APIs transverses à unifier derrière le store** : `/api/market/summary`, `/api/market/regime`,
  `/api/live/status`, `/api/live/events`, `/api/session/digest`, `/api/desk`, `/api/pos-quotes`,
  `/api/names`, `/scan`.
- **APIs par-titre (navigation ticker)** : `/api/ticker/<sym>`, `/api/strategy/decision/<sym>`,
  `/api/decision/<sym>`, `/api/analyst/<sym>`, `/api/anomalies/<sym>`, `/api/options-for/<sym>`.
- **Redirections legacy (41)** : à préserver telles quelles (deep links).
- **Ne pas toucher** : routes lourdes de scan (`/api/rescan`, `/weekly-regen`), IBKR
  (readonly), webhooks TradingView.

---

## 6. FICHIERS CONCERNÉS

| Zone | Fichiers | Rôle dans la refonte |
|---|---|---|
| Shell | `vertex/ui/shell/__init__.py` | Rendu shell + hooks fragment ; police non bloquante |
| Routeur client | `vertex/static/vertex/js/vx-shell.js` (+ nouveau `vx-router.js`) | Interception liens, pushState/popstate, swap `#vx-content` |
| Store | `vertex/static/vertex/js/vx-core.js` (+ nouveau `vx-store.js`) | `VX.store`, SWR, dédup, annulation, anti-hors-ordre, freshness_map |
| Prix live | nouveau `vx-prices.js` + `live-updates.js` | Source de prix centrale, cohérence inter-pages |
| Pages | `vertex/ui/pages/*.py` (8 espaces + analysis/index) | Découpage contenu/shell, lecture depuis le store |
| Session serveur | `vertex/app/state.py`, `vertex/engines/session_digest.py`, nouveau `vertex/engines/session_snapshot.py`, `vertex/app/routes/session_api.py` | Conteneur session atomique + manifest + `active_session_id` |
| Fraîcheur | `vertex/app/routes/live_api.py`, `vertex/services/` | Table de seuils unifiée, enveloppe de fraîcheur |
| SW / PWA | `vertex/app/routes/system.py` (`_SW_JS`, `td-shell-vNN`) | Précache shell/CSS/JS, stratégie SWR, offline |
| Observabilité | `vertex/ui/pages/system_page.py` | Métriques nav/cache/session |
| Tests | `tests/test_*` (nouveau `test_continuity_*.py`) | Voir §19 du cahier des charges |

---

## 7. MATRICE ENDPOINTS × PAGES (duplications → cibles store)

| Endpoint | Pages consommatrices | TTL divergents ? |
|---|---|---|
| `/api/market/summary` | Aujourd'hui, Marchés (×3), + préchauffage core | 60 000 / 30 000 |
| `/api/market/regime` | Aujourd'hui (×2), Marchés (×2) | 120 000 |
| `/api/command` | Aujourd'hui (×3) | 60 000 / 30 000 |
| `/scan` | Marchés, Portefeuille | **120 000 vs 300 000** |
| `/api/pos-quotes` (POST, jamais caché) | Aujourd'hui, Portefeuille, Options | — |
| `/api/live/status` | shell, live-updates, Système | **60 000 / 0 / 30 000** |
| `/api/session/digest` | Aujourd'hui (`no-store`), préchauffage core (VX.fetch) | **2 chemins incohérents** |
| `/api/desk` | Journal, entités, Système | — |
| `/api/names` | shell, Analyse | 600 000 (inutile car cache mémoire vidé) |
| `/cal-feed` | Aujourd'hui, Marchés | 300 000 |
| `/api/data-quality` | Opportunités, Système | 60 000 / 30 000 |

Cible : chaque endpoint transverse = **une entrée du store**, une politique de fraîcheur, un
seul fetch partagé par toutes les pages, revalidé en fond.

---

## 8. RISQUES

| # | Risque | Gravité | Mitigation |
|---|---|---|---|
| R1 | Casser deep links / retour / nouvel onglet en passant en client-routing | Élevée | Progressive-enhancement : les URL servent toujours le doc complet ; router = surcouche, repli sans-JS testé |
| R2 | Régression des 991+ tests (gardiens SW, ids, littéraux, sync desk) | Élevée | Lots isolés, pytest complet après chaque lot, bump SW discipliné |
| R3 | Fuite/mélange entre `session_id` (snapshot A affiché avec live B) | Élevée | Isolation stricte dans le store, jeton de génération, bascule atomique validée par manifest |
| R4 | Réponses hors-ordre peignant des données périmées | Moyenne | Génération monotone + annulation au changement de page/ticker |
| R5 | Ajout involontaire d'un recalcul lourd sur navigation | Élevée | Interdit par contrat ; test « aucun scan déclenché par navigation » |
| R6 | Fuite mémoire du store (cache pages/prix qui grossit) | Moyenne | Bornes + éviction LRU + métriques taille dans Système |
| R7 | Violation READONLY par une nouvelle route session/prix | **Critique** | Toutes les nouvelles routes = lecture seule ; `/readyz` vérifie READONLY ; test dédié |
| R8 | Incohérence prix live vs prix de scénario si source centrale mal cloisonnée | Moyenne | Contrat explicite : live ≠ référence snapshot ≠ prix d'achat, jamais de substitution silencieuse |
| R9 | Offline / cold start Render (SW network-first + police bloquante) | Moyenne | Précache shell, police locale/non bloquante, mode dégradé affichant le dernier snapshot |
| R10 | Monolithe `terminal.py` (~10,5 k lignes) fragile aux éditions | Moyenne | Travailler dans les modules (`vertex/…`), éditions chirurgicales, apostrophes JS échappées |

---

## 9. PLAN D'EXÉCUTION (lots)

- **LOT 1 — Audit & contrats** *(ce document)* : cartographie + archi cible + métriques. ✅
- **LOT 2 — Shell persistant + store global** : `vx-router.js` (interception + pushState +
  swap `#vx-content` + repli sans-JS), rendu de fragment par page, `VX.store` (session, prix,
  navigation), police non bloquante. Tests : nav sans reload du shell, retour, deep link.
- **LOT 3 — Cache & stale-while-revalidate** : dédup, SWR, persistance légère, annulation,
  anti-hors-ordre, invalidation ciblée. Tests : cache page, SWR, dédup, réponse hors-ordre
  ignorée, requête annulée, changement de page pendant chargement.
- **LOT 4 — Navigation instantanée** : préchargement (idle/hover/proximité), transitions,
  historique tickers, navigation titre, deep links. Tests : cibles perf mesurées.
- **LOT 5 — Session atomique + intégration pages** : conteneur session serveur + manifest +
  `active_session_id` + bascule atomique + notification ; branchement des 8 pages + identité
  visuelle unifiée + prix live cohérent partout. Tests : bascule atomique, ancienne session
  conservée pendant calcul, prix live vs snapshot distinct.
- **LOT 6 — Polish** : responsive, a11y, offline/dégradé, erreurs isolées, observabilité
  (Système), documentation, captures, mesures réelles.

**Après chaque lot** : `compileall` + `pytest` complet + test READONLY + navigateur
desktop & mobile + console 0 erreur + mesure perf + commit isolé + rapport.

---

## 10. MÉTRIQUES CIBLES (à mesurer réellement lot par lot)

| Métrique | Base actuelle | Cible |
|---|---|---|
| Rechargement du shell à la navigation | Oui (complet) | **Non** (shell persistant) |
| Appels API redondants sur un tour des 8 pages | ~40 (5 endpoints ×8) | ≤ 8 (un par endpoint, revalidé en fond) |
| Réponse visuelle au clic de nav | reload complet | < 100 ms |
| Contenu (cache) affiché | après reload + refetch | < 150 ms |
| Police bloquante en tête | ~1,8 s+ (repayé/page) | non bloquante / précachée |
| Scan lourd déclenché par navigation | 0 (à préserver) | 0 |
| Cohérence prix d'un ticker inter-pages | non garantie | garantie (source centrale) |
| Bascule de session | inexistante (mutation continue) | atomique + notifiée |

---

## 11. DÉCISION DEMANDÉE (arrêt pour validation humaine)

Le LOT 1 est terminé (audit only, aucun changement fonctionnel). **Validation requise avant
LOT 2** sur :
1. l'approche **shell persistant en progressive-enhancement** (URL intactes, repli sans-JS) ;
2. l'introduction d'un **`session_id` + snapshot atomique serveur** enrobant l'état existant
   (sans nouveau calcul) ;
3. l'ordre des lots ci-dessus.
