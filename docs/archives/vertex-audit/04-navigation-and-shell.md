# 04 — Navigation & shell

## Shell canonique (`vertex/ui/shell/__init__.py`)
- `PRIMARY_NAV` (ligne 14) = **8 items** : Dashboard `/` · Opportunités `/opportunities` · Portefeuille
  `/portfolio` · Analyse `/analysis` · Options `/options` · Performance `/performance` · Intelligence
  `/intelligence` · Système `/system`. Icônes = SVG inline sobres (`_ICONS`), pas d'emojis comme langage principal.
- Sidebar avec `aria-current` (gardien `test_redesign_ui.py::test_active_nav_item_marked`).
- Breadcrumbs `Vertex / espace / sous-vue` + bouton retour (`vxNavigationContext`).
- Recherche globale `#vx-global-search` + **command palette** `#vx-palette` (backend `/api/command`).
- Topbar : Ajouter · horloge/compte à rebours de séance · Connexions · Notifications · Refresh.
- **Pas de sélecteur de compte** (mono-utilisateur) — correct.

## Finding structurant
- **IA-01 (P1) — Double navigation.** `vertex/ui/nav.py` définit une **2ᵉ** navigation de **10 items** pointant
  vers des routes **legacy** distinctes : `/` (Market Overview), `/stocks`, `/strategie` (Trading Desk),
  `/journal`, `/options` (Options Lab), `/sectors`, `/catalysts`, `/anomalies`, `/settings`, `/vault`.
  C'est le vestige du monolithe pré-strangler. `PRIMARY_NAV` (8, moderne) **fait autorité** ; `nav.py` crée un
  risque de liens divergents/morts et de confusion mentale.
  **Action (Phase 3)** : confirmer qu'aucune page servie n'utilise encore `nav.py` pour son rendu de sidebar ;
  rediriger les routes legacy utiles vers les espaces canoniques (`/stocks`→`/analysis`, `/strategie`→prep/sim,
  `/journal`→`/performance?view=journal`, `/sectors`/`/catalysts`/`/anomalies`→`/opportunities`, `/vault`→
  `/system?view=archive`) ; retirer `nav.py` de la sidebar. Ne pas casser les URL entrantes (301 internes).

## Règle service worker (à ne jamais oublier)
Tout changement de **shell visible** → bump `td-shell-vN` (`vertex/app/routes/system.py`) **+** les 3 tests qui
l'épinglent (`test_ui_v3.py`, `test_production_guards_canonical.py`, `test_redesign_ui.py`). Version actuelle
constatée : `td-shell-v89`.

## Cible shell (Phase 3)
Une seule nav (PRIMARY_NAV), statut IBKR honnête dans la topbar (voir `09`), recherche + palette unifiées,
raccourcis clavier, focus visible. DoD shell : `references/page-definition-of-done.md`.
