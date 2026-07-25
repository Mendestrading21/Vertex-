# CONTINUITY — LOT 2 · Shell persistant + store global (validation)

**But** : transformer le MPA (shell détruit/reconstruit à chaque navigation) en
**application continue** — le shell reste, seul le contenu change — en
**progressive-enhancement** (URL, deep links, retour, refresh, sans-JS intacts).

**Invariants** : READONLY, données réelles, moteurs inchangés, tests 100 %.

---

## Livré

1. **Rendu de fragment serveur** (`vertex/ui/shell/__init__.py`)
   - `render_shell()` détecte une requête fragment (en-tête `X-Vertex-Fragment: 1`
     ou `?__frag=1`) et renvoie alors UNIQUEMENT : métadonnées (`data-title`,
     `data-active`, `data-space-label`, `data-sub-label`, `data-page-label`) +
     `<template class="vx-frag-content">` + `<template class="vx-frag-mobile">` +
     `page_js`. Sinon → document complet inchangé.
   - Zéro changement dans les 14 pages : la bascule est centralisée dans le shell.

2. **Routeur client** (`vertex/static/vertex/js/vx-router.js`, nouveau)
   - Intercepte les clics de liens internes (délégation globale), `history.pushState`,
     récupère le fragment, remplace `#vx-content`, met à jour fil d'Ariane / nav active /
     titre, ré-exécute `page_js`. `popstate` géré (retour/avance).
   - **Sécurité de ré-exécution** : scripts inline de page = IIFE (idempotents en portée
     globale, vérifié sur les 7 pages) ; scripts externes = chargés une seule fois (dédup).
   - **Repli navigation dure** (progressive-enhancement) : page « external-only »
     (aucun inline, ex. Options), fragment absent, ou **toute** erreur → `location.href`.
   - Modificateurs clavier / `target=_blank` / `download` / `/static` / `/api` /
     `/widget-lab` → comportement natif (jamais intercepté).

3. **Cycle de vie de page** (`vertex/static/vertex/js/vx-core.js`)
   - `VX.page._teardown()` (appelé avant chaque swap) : arrête les tâches `VX.refresh`
     de page, retire les abonnements `VX.bus` de page, exécute les `onLeave`.
   - `VX.refresh.register(..., {persistent})` et `VX.bus.on(..., {persistent})` :
     le SHELL (statut global) est persistant ; les loaders de PAGE sont purgés à la
     navigation → **aucun timer fantôme, aucun doublon de loader**.
   - `VX.store` (fondation) : `active_session_id`, `active_ticker`, `nav_history`,
     `live_prices`, `freshness_map` (SWR/dédup complets au LOT 3).

4. **Police non bloquante** (`shell/__init__.py`)
   - Google Fonts passe de `<link rel=stylesheet>` (bloquant le rendu, ~1,8 s repayé
     à chaque page) à `<link rel=preload as=style onload=…swap>` + `<noscript>` de repli.

5. **Statut shell persistant** (`vx-shell.js`) + **SW** `td-shell-v64 → v65`.

---

## Validation (navigateur réel, Chromium 1440×900, DÉMO)

**Navigation client (persistance du shell)** — sentinelle de contexte JS + identité
du nœud sidebar (survivent au SPA, réinitialisés par un vrai reload) :

| Navigation | Espace | Shell conservé (SPA) |
|---|---|---|
| → Marchés | markets | **OUI** |
| → Opportunités | opportunities | **OUI** |
| → Analyse | analysis | **OUI** |
| → Portefeuille | portfolio | **OUI** |
| → Aujourd'hui | briefing | **OUI** |
| Bouton **Retour** | portfolio | **OUI** (popstate) |
| → Options (external-only) | options | Repli **dur** (attendu) |
| `/analysis/MSFT` (fiche) | analysis | **OUI** · `store.active_ticker=MSFT` · 6 graphiques rendus |

**Aucune fuite mémoire / timer** : après **6 navigations SPA** en boucle, `VX.refresh._tasks`
reste à **4** (`status` persistant + 3 tâches de page ré-enregistrées) — jamais d'accumulation.

**Élimination de la redondance réseau** (tour SPA de 7 navigations) :

| Endpoint (niveau shell) | MPA (avant) | SPA (après) |
|---|---|---|
| `/api/desk` | ~8× (1×/page) | **1×** |
| `/api/live/status` | ~8× | **1×** |
| `/api/live/events` | ~8× | **1×** |
| `/api/market/summary` | ~8× | **1×** |

> `/api/session/digest` reste ré-appelé (loader `no-store` de la page Aujourd'hui à
> chaque revisite) → cible du LOT 3 (stale-while-revalidate + dédup dans le store).

**Console** : **0 erreur** sur l'ensemble du parcours. **Repli sans-JS** : le document
complet est toujours servi sans l'en-tête (deep link / refresh / nouvel onglet intacts).

---

## Tests

- `tests/test_continuity_shell.py` (11 gardiens) : document complet toujours servi,
  fragment vs document, métadonnées de fragment, 7 espaces navigables, routeur inclus,
  police non bloquante, cycle de vie + store dans le core, tâche shell persistante,
  repli dur.
- **Suite complète : 1008 passed / 2 skipped.** compileall OK. READONLY intact.

---

## Limites connues (traitées plus tard)

- **Options** (et toute future page « external-only ») : navigation dure — sera
  rendue SPA au LOT 5 en exposant un point d'init idempotent.
- **Barre d'actions mobile** de la fiche Analyse : la nav active mobile est mise à jour,
  mais les actions spécifiques (Favori/Alerte/Options) ne sont pas re-injectées en SPA
  (LOT 5, intégration pages).
- **`/api/session/digest`** ré-appelé sans dédup (loader `no-store`) → LOT 3.

Prochaine étape : **LOT 3 — Cache & stale-while-revalidate** (dédup, SWR, persistance
légère, annulation, anti-hors-ordre, invalidation ciblée).
