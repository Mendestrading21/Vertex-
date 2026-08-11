# Validation — NEON GLASS 02 : Marchés (refonte premium, 2ᵉ passe)

> Issue #14, 2ᵉ espace. **La 1ʳᵉ proposition Marchés (recolorisation CSS scopée) a
> été REFUSÉE** par l'humain : rendu pas assez premium, graphiques génériques dans
> des boîtes, et surtout **le shell restait Signal Green** (sidebar/topbar/nav hors
> `.vx-content`). Cette 2ᵉ passe corrige la cause racine puis refond Marchés.
>
> Branche `agent/vertex-neon-glass-graphs`. **Aucun moteur, aucune donnée, aucun
> calcul modifié. IBKR READONLY intact. Les 6 autres espaces non touchés.**

## 0. Ce qui a changé depuis le refus

Le refus visait deux causes ; les deux sont corrigées **à la racine**, pas par une
surcouche :

1. **Le vert de marque survivait dans le shell.** Corrigé dans `tokens.css` (source
   unique) : Signal Green `#84aa31` n'est plus la marque. Identité = **Orange Ember
   `#FF6D29`** partout, y compris sidebar/topbar/nav mobile (hors `.vx-content`).
2. **Graphiques génériques.** Les 3 miroirs graphiques ont été synchronisés sur
   l'orange Ember ; Marchés a été **restructuré** (hero régime, états honnêtes,
   widgets glass à classes stables), pas seulement recoloré.

## 1. Fichiers modifiés

| Fichier | Nature du changement |
|---|---|
| `vertex/static/vertex/css/tokens.css` | **Réécriture NEUE EMBER** : Signal Green → Orange Ember à la source. Noms de tokens conservés (rien ne casse), valeurs changées. Compat `--vx-signal-*`/`--vx-orange-*`/`--vx-copper-*` repointée sur Ember. |
| `vertex/visualization/palette.py` | `BRAND #84aa31→#FF6D29` + couleurs fonctionnelles (émeraude/corail/ambre/violet/gris chaud) + séries. |
| `vertex/static/vertex/js/charts/chart-theme-obsidian-copper.js` | Miroir JS strict de `palette.py`. |
| `vertex/static/vertex/js/charts/chart-core.js` | Repli codé en dur mis en parité (3ᵉ copie). |
| `vertex/static/vertex/css/neon-glass.css` | **Recentré sur les tokens** (plus de littéral orange), `overflow:hidden→visible` (bug tooltips), `::before` `pointer-events:none`, **sélecteurs fragiles supprimés** (`[class*="heat"]`, `[class*="rail"]`, `[id$="-gauge"]` → classes stables `vx-mk-*`), fond bleu décoratif retiré, widgets premium `vx-mk-hero-grid`/`vx-mk-chip`. |
| `vertex/ui/pages/markets_page.py` | **Restructuration Vue d'ensemble** (bandeau hero régime + risque), **hero régime premium** avec **état honnête** (plus de « UNKNOWN / 0 % » géant), étiquettes FR des régimes, contexte volatilité honnête. Aucune donnée/route/endpoint changés. |
| `vertex/app/routes/system.py` | Service worker `v52 → v53` (shell visible modifié à la racine). |
| `tests/…` | Gardiens durcis (voir §7). |
| `docs/visual/VERTEX_NEUE_EMBER_SYSTEM.md` | **Créé** : système visuel canonique. |

## 2. Structure avant / après (Vue d'ensemble)

| Avant | Après |
|---|---|
| 3 cartes égales `col-4` (Régime / Leadership / Risque), toutes identiques | **Bandeau HERO** : Régime (`col-8`, `vx-card--hero`, question « Le vent est-il dans le dos ou de face ? ») + Risque du jour (`col-4`) |
| Régime = petite carte, jauge + KV | **Hero régime** : nom de régime large (ton sémantique), jauge de confiance, **chips de modulation** (nouveau risque / priorité setups / confirmations) |
| Régime absent → **« UNKNOWN » + jauge à 0 %** (géant) | **État honnête** : « Régime indéterminé — moins de 3 dimensions (0 évaluée). Nouveau risque bloqué. » + action Système/Données |
| SPY seul sur `col-12`, Leadership en tête | SPY `col-8` **+ Leadership `col-4`** côte à côte (hiérarchie) |

Les vues **Macro · Secteurs · Breadth · Volatilité** conservent leur structure
décisionnelle (RRG, heatmap, jauge VIX, rails) et gagnent l'identité Ember + le
verre premium + les états honnêtes. Le contexte régime de **Volatilité** affiche
désormais « indéterminé » explicité au lieu du code brut `UNKNOWN`.

## 3. Graphiques avant / après

| Élément | Avant | Après |
|---|---|---|
| Séries de courbes/barres | vert Signal `#84aa31` en tête | **Orange Ember `#FF6D29`** en série 0 (identité) |
| RRG rotation sectorielle | quadrants, dots | quadrants **interprétés** (LEADING/IMPROVING/WEAKENING/LAGGING), axes nommés, dots sémantiques, tickers orange, tooltip verre, help |
| Jauge VIX / régime / breadth | bandes | bandes sémantiques (émeraude/ambre/corail), valeur centrale dominante, lecture sous la valeur |
| Heatmap secteurs | table-heat | texte renforcé (classe stable `vx-heat-cell`), échelle explicite, conclusion |
| KPI cross-asset | tuiles | tuiles **glass** + sparkline sémantique (émeraude/corail) |

Aucun graphe supprimé ni ajouté : **~13 rendus VXCharts conservés**, habillés et
restructurés (pas de big-bang). Le contrat Chart Shell (`C.card`) reste intact
(titre/question/conclusion/période/unité/source/fraîcheur/légende/aide/résumé +
états loading/empty/stale/error/demo/insufficient/offline).

## 4. Widgets créés / composants réutilisés

- **Créés (classes stables `vx-mk-*`)** : `vx-mk-hero-grid` (bandeau hero régime),
  `vx-mk-regime-name` (nom + ton sémantique), `vx-mk-chips` / `vx-mk-chip`
  (modulations glass à état on/off).
- **Réutilisés** : Chart Shell `C.card`, jauge, RRG scatter, heatmap, donut,
  timeline, funnel, waterfall, rails, KPI glass — tous existants, non recréés.

## 5. Responsive (mesuré : 390 / 768 / 1280 / 1440 / 1920)

Sweep Playwright (Chromium) sur **5 vues × 5 viewports = 25 combinaisons**, métrique
de débordement réel (bord droit max des `.vx-content *` hors conteneurs à
`overflow-x` propre / fixed) :

| Viewport | Débordement réel | Erreurs console applicatives |
|---|---|---|
| 390 | **0 px** | 0 |
| 768 | **0 px** | 0 |
| 1280 | **0 px** | 0 |
| 1440 | **0 px** | 0 |
| 1920 | **0 px** | 0 |

**25/25 propres.** Le hero régime passe en pile à ≤ 768 px (`grid-template-columns:1fr`).
Tableaux larges = défilement intentionnel.

## 6. Console

**0 erreur applicative** sur les 25 combinaisons (hors `ERR_CONNECTION_RESET` Google
Fonts, non applicatif dans le bac à sable).

## 7. Tests

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **961 passed, 2 skipped** (baseline 958 → **+3**
  gardiens, aucune régression).
- Gardiens **durcis** :
  - `test_ui_v3.py::test_v3_tokens_are_canonical` → tokens **Ember** canoniques ;
    anti-régression : `--vx-brand` ne pointe plus sur le vert Signal, **aucun
    `#84aa31`** résiduel.
  - `test_design_system_v1.py::test_official_typography_tokens` → fallback **Inter**
    (Neue Montreal en direction, non embarquée).
  - `test_neon_glass_01.py` → identité **sourcée tokens** (`--ng-neon:var(--vx-ember-500)`),
    **overflow visible** (anti-clip tooltip), **`::before` `pointer-events:none`**,
    **classes `vx-mk-*` stables** (zéro sélecteur fragile), zéro-bleu, glow live-only,
    reduced-motion, scope briefing+markets, READONLY, SW v53.
  - `test_visual_intelligence.py` → **parité des 3 miroirs** + zéro-bleu (série 0 =
    Ember, `is_bluish(BRAND) is False`).

## 8. Captures

Générées (Chromium, `full_page`) — évidence de session :
`mk-overview-{390,1440,1920}.png`, `mk-sectors-{1440,1920}.png`,
`mk-volatility-{1440,1920}.png`. Vérifié visuellement : **shell orange Ember**
(sidebar active, CTA « + Ajouter », logo — plus aucun vert), hero régime premium
avec **état honnête** (« Régime indéterminé »), DÉMO clairement étiqueté, RRG
interprété, VIX jauge sémantique, tuiles glass, sémantiques respectées
(émeraude/corail/ambre), **aucun bleu identitaire, aucun glow permanent**.

## 9. Service worker

`td-shell-v53` (le shell visible a changé à la racine). Gardiens SW mis à jour
(v53 présent, v52 absent) dans `test_production_guards_canonical.py`,
`test_redesign_ui.py`, `test_ui_v3.py`.

## 10. Risques & éléments différés

- **Risque faible** : changement visuel + restructuration HTML/CSS **sans toucher
  données/moteurs/endpoints** ; réversible. En mode démo, `/api/market/regime`
  renvoie honnêtement `UNKNOWN` (< 3 dimensions) — le nouvel **état honnête** le rend
  lisible (comportement produit correct, pas un bug).
- **Différé** (structurel, avec tests, après validation) : consolidation du nombre
  de graphes vers primitives canoniques ; vue **Cross-asset** dédiée ; term
  structure / skew IV seulement si données réellement disponibles.
- Validation Chromium **headless** (pas d'appareil physique). Neue Montreal non
  embarquée (Inter rendu) : conforme — aucune dépendance réseau nouvelle.

## Verdict

**Marchés refondu premium en Neon Glass Orange**, cause du refus corrigée à la
racine (vert de marque tué dans `tokens.css` → shell orange partout ; 3 miroirs
synchronisés). Hero régime, états honnêtes (fini le « UNKNOWN / 0 % » géant),
widgets glass à classes stables, tooltips non rognés. **961 tests verts · 25/25
combinaisons sans débordement ni erreur console · READONLY intact · aucun bleu
identitaire · aucune donnée modifiée.** **Arrêt pour validation humaine avant
Opportunités.**
