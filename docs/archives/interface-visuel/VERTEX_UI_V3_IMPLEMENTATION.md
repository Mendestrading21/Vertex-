# VERTEX EXPERIENCE OS — Implémentation (UI V3)

Refonte visuelle/UX complète (2026-07-11), phases 1-24 avec commit stable
après chaque groupe. Chaque affirmation est adossée à un test, un run
Chromium ou une capture.

## 1. Architecture visuelle

- **Design system V3** « Dark Financial Luxury » : `tokens.css` (palette
  canonique orange/ambre, alias legacy sans casse), `base.css` (ambiance
  halos + vignettage, typo tabulaire), `layout.css` (shell, grille 12),
  `components.css` (cartes 3 niveaux, badges, drawers/modales/palette),
  `buttons.css`, `states.css`, `animations.css`, `forms.css`, `tables.css`,
  `charts.css`, `responsive.css`, `utilities.css` — 13 feuilles, zéro
  couleur arbitraire dans les pages.
- **Thème graphique unique** : `charts/chart-theme.js` → `chart-core.js`
  (24 modules, contrat titre/question/conclusion/source/timestamp/
  « Comprendre ce graphique »).
- **Shell** : sidebar 240/72 (7 espaces + état système + Système en bas +
  Réduire), topbar (retour contextuel, breadcrumb, ⌘K, état marché avec
  point de vie + horloge NY, connexions, notifications, refresh, bouton
  Ajouter brand), barre mobile 5+Plus.

## 2. Pages refondues (8/8)

Voir `VERTEX_WIDGET_CATALOG.md` (widgets par page) et
`VERTEX_UI_V3_BEFORE_AFTER.md` (captures et changements détaillés) :
Briefing hero + cross-asset compacté · Marchés (fix bandeau indices,
multi-indices rebasés, heatmap secteurs) · Opportunités (dossier radar +
actions rapides) · Portefeuille (synthèse, options tactiques hors équipe,
contributeurs) · Analyse (workspace + rail décisionnel sticky) ·
Performance (heatmap mensuelle, distribution) · Intelligence (suggestions,
récents) · Système (états moteurs différenciés, endpoints en drawer).

## 3. Bugs réels corrigés pendant la refonte

1. `[object Object]` sur Marchés (leader sectoriel = objet rendu tel quel).
2. Bandeau indices de Marchés à « n/d » alors que les données existaient
   (mapping objet `SPX` vs liste par noms).
3. Bouton « Réduire » au style navigateur par défaut (reset manquant).
4. **Unités de coût des positions** : le modal stockait un prix unitaire
   là où le schéma desk historique attend un TOTAL investi ; `enrich()`
   multipliait coût×qté×100 (poids d'option affiché à 98 % du
   portefeuille) ; la clôture journalisait un investi ×100 (un gain
   pouvait être classé LOSS). Les quatre points alignés sur le schéma
   historique (`cost` = total ; action cotée au spot, option au
   mark×100×qté).
5. `heatmapCard`/`bars` non chargés sur Marchés-Secteurs et Performance.
6. Mauvaise signature `VX.recentTickers` (attrapée par la télémétrie
   `/api/client-log` — la boucle 0-erreur fonctionne).

## 4. Preuves (reproduites)

- **Tests** : `python -m pytest tests/ -q` → **543 passed** (dont 27
  canoniques §39 dans `tests/test_ui_v3.py`).
- **Console** : 0 erreur sur les 8 espaces + vues avec données seedées ;
  `GET /api/client-log` → 0.
- **Parcours A-I** : 9/9 PASS en Chromium (favori, options→scénarios→
  alerte→notifications, watchlist aller-retour, position→clôture→journal,
  secteurs→opportunités, ⌘K, replis Claude/TV/IBKR).
- **Responsive** : 7 viewports × 8 pages — 0 débordement, 0 erreur page.
- **Captures** : 8 pages × 5 tailles (`docs/redesign/v3-after/`).
- **READONLY** : `readonly=True` intact ; gardien V3
  `test_no_order_execution_path` (appels/définitions) vert.

## 5. Performance front

Chart.js mutualisé + registre anti-canvas-orphelins ; `VX.fetch` avec TTL
et retry (pas de double-fetch entre widgets d'une même page) ; refresh
manager avec garde `document.hidden` ; debounce sync 1.2 s + sendBeacon ;
animations courtes uniquement (reduced-motion coupé) ; halos en un seul
`body::before` fixe (aucun repaint).

## 6. Accessibilité

Navigation clavier complète (palette, menus, drawers avec focus trap +
Échap), `aria-current/selected/pressed/sort`, focus visible brand,
`vx-sr-only`, tailles tactiles ≥ 34 px, sémantique jamais portée par la
couleur seule (signe/badge/texte systématiques), reduced-motion.

## 7. Documentation liée

`VERTEX_DESIGN_TOKENS.md` · `VERTEX_UI_COMPONENT_LIBRARY.md` ·
`VERTEX_CHART_LIBRARY.md` · `VERTEX_WIDGET_CATALOG.md` ·
`VERTEX_UI_V3_BEFORE_AFTER.md` · `VERTEX_UI_V3_AUDIT.md` ·
`VERTEX_UI_KNOWN_LIMITATIONS.md`.
