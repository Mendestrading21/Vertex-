# VERTEX — Registre des contradictions (Phase 2)

> Branche `agent/vertex-total-rebuild` @ `362c7d4`. Chaque contradiction cite ses
> **deux sources**, propose une **source canonique**, une **décision** et la
> **validation** nécessaire. **Aucune correction appliquée dans ce lot d'audit.**

Sévérité : 🔴 critique (honnêteté données / décision) · 🟠 majeure (cohérence /
maintenabilité) · 🟡 mineure (doc / nommage).

---

## C-01 🟠 Navigation : « 8 espaces » vs « 9 espaces »

- **Source A** : `vertex/ui/shell/__init__.py:12` — docstring « Navigation
  principale — EXACTEMENT huit espaces (§10) » ; `redesign.py:122-124` — « Options…
  PAS un 9e espace ».
- **Source B** : `vertex/ui/shell/__init__.py:13-23` — `PRIMARY_NAV` liste **9**
  entrées (briefing…system) ; `tests/test_redesign_ui.py:30`
  `test_primary_navigation_has_nine_items` fige **9**.
- **Canonique** : le **code + test (9 espaces)**. La cible SKILL parle de 8
  espaces (avec « Journal » au lieu de Performance+Intelligence) — c'est un
  objectif de refonte, pas l'état courant.
- **Décision** : corriger les commentaires (9), puis, lors de la refonte IA,
  décider explicitement de l'architecture cible (8 vs 9) et migrer le test.
- **Validation** : `test_redesign_ui.py` + revue nav shell.

## C-02 🟠 Palette graphique : séries divergentes Python ↔ JS

- **Source A** : `vertex/visualization/palette.py` — série neutre `#9d978e`,
  copper `#747d75`, copper_light `#a3ca42`.
- **Source B** : `js/charts/chart-theme-obsidian-copper.js` — `series[2]=#8f8a83`,
  `series[5]=#48631b`, `copperLight #84aa31`.
- **Problème** : 2 des 6 couleurs de série (indices 2 et 5) diffèrent ; le gardien
  `tests/test_visual_intelligence.py::test_js_theme_matches_python_palette:37` ne
  vérifie QUE brand/beige/option + absence de bleu → **divergence non détectée**.
- **Canonique** : à trancher (proposer **`palette.py` Python** comme source, JS et
  CSS dérivés). 
- **Décision** : aligner les 3 sources, **renforcer le test** pour comparer
  `SERIES` entière.
- **Validation** : test durci + rendu graphiques inchangé visuellement.

## C-03 🟡 Identité graphique : commentaires « cuivre/orange » vs rendu vert

- **Source A** : `palette.py:16` (« ex-cuivre, purgé ») et
  `chart-theme-obsidian-copper.js:2-5` décrivent « cuivre / orange ».
- **Source B** : la valeur réelle `BRAND=#84aa31` est un **vert olive** ; le nom
  de fichier `chart-theme-obsidian-copper.js` évoque le cuivre.
- **Décision** : purger les commentaires, envisager de renommer le fichier de
  thème pour refléter l'identité réelle (à coordonner avec C-04).
- **Validation** : grep « cuivre/copper/orange » nul dans les commentaires actifs.

## C-04 ✅ RÉSOLU — Identité produit : Obsidian Copper / Inter (décision utilisateur)

- **Origine du signalement** : le `CLAUDE.md` de la branche d'intégration
  (`integration/vertex-v4-clean`, injecté au démarrage de session) parlait de
  « Vertex V4 — Obsidian Prism » et « General Sans ».
- **État réel sur `agent/vertex-total-rebuild`** : ces termes **n'existent pas**
  (le `CLAUDE.md` de cette branche — 37 lignes — ne mentionne aucune identité
  design ; « Obsidian Prism »/« General Sans » n'apparaissent que dans les
  présents documents d'audit). L'identité est **déjà cohérente** dans le code et
  les specs : « **VERTEX OBSIDIAN COPPER** » (39 fichiers), polices **Inter**
  (UI, `tokens.css:120`) + **IBM Plex Mono** (chiffres, `tokens.css:121`).
- **Décision utilisateur (2026-07-23)** : conserver **Obsidian Copper / Inter**
  (le code actuel fait foi). **Aucun changement runtime nécessaire.**
- **Reste mineur** : certaines specs (`docs/VERTEX_DESIGN_TOKENS.md`) citent
  « JetBrains Mono » alors que `tokens.css` utilise **IBM Plex Mono** — écart de
  nommage typographique à réconcilier dans la PR design (n°2), sans urgence.
- **Validation** : grep « Obsidian Prism »/« General Sans » nul hors docs
  d'audit ✔ ; `tokens.css` = Inter + IBM Plex Mono ✔.

## C-05 🟠 Deux moteurs de chandeliers chargés simultanément

- **Source A** : `vertex/ui/pages/analysis_page.py:204` charge
  `charts/candlestick-chart.js` (Canvas OHLC).
- **Source B** : `analysis_page.py:206` charge `charts/candlestick-lwc.js`
  (TradingView LWC) — plus `price-chart.js`.
- **Problème** : deux (voire trois) implémentations du même graphique prix chargées
  ensemble ; une seule s'affiche (`lwCandlestickCard` avec repli).
- **Décision** : identifier par test navigateur le rendu réel, retirer le
  redondant.
- **Validation** : test navigateur sur `/analysis/<sym>` ; poids JS réduit.

## C-06 🟠 Deux registres de navigation

- **Source A** : `vertex/ui/nav.py:10` `ITEMS` (10 libellés anglais), consommé par
  `terminal.py:6517-6518`.
- **Source B** : `vertex/ui/shell/__init__.py:13` `PRIMARY_NAV` (9 espaces),
  rendu par le redesign.
- **Canonique** : `PRIMARY_NAV`. `nav.py` = vestige du monolithe.
- **Décision** : confirmer que `nav.py` ne sert plus aucune page vivante puis le
  retirer (avec `tests/test_nav.py`).
- **Validation** : aucune régression sur les pages, `test_nav.py` mis à jour.

## C-07 🔴 Qualité des données en démo : tout « MISSING » alors que les pages affichent des scores

- **Source A** : `GET /api/data-quality` (démo) → `by_quality = {MISSING: 20}` —
  les 20 titres notés `MISSING`.
- **Source B** : `GET /healthz` → `scanned:20, vertex_ready:20` et les pages
  Opportunités/Analyse affichent scores, verdicts, R:R pour ces mêmes titres.
- **Problème** : le graphique « Qualité des données » (`vx-data-quality-chart`)
  afficherait 100 % `MISSING` pendant que le reste de l'app montre une analyse
  complète → message contradictoire sur la fiabilité.
- **Canonique** : la fraîcheur/qualité doit refléter l'état **démo** (données
  synthétiques étiquetées), pas `MISSING`.
- **Décision** : en démo, étiqueter la qualité comme `DEMO/SIMULATED` (cohérent
  avec le badge démo), pas `MISSING`. À examiner côté producteur de `data-quality`.
- **Validation** : `/api/data-quality` en démo renvoie un état cohérent avec le
  badge démo ; test dédié.

## C-08 🔴 Décision « confiante » sur un ticker inexistant

- **Source A** : `GET /api/decision/ZZZZZ` (ticker bidon) → HTTP 200,
  `committee.confidence:56`, `lean:38`, verdict « Marché RISK-OFF ».
- **Source B** : `GET /api/ticker/ZZZZZ` → tous champs `null` (aucune donnée).
- **Problème** : viole le manifeste (« Vertex peut dire *je ne sais pas* ») et la
  règle d'intégrité 6 — une confiance chiffrée est produite sans aucune donnée
  titre.
- **Canonique** : absence de données → état « indisponible / données
  insuffisantes », pas un verdict chiffré.
- **Décision** : `decision_stack` doit renvoyer un état explicite « insuffisant »
  pour un symbole hors univers / sans données ; **exige un test rouge** avant
  correction (règle SKILL de modification moteur).
- **Validation** : test reproduisant le défaut + correction + non-régression.

## C-09 🟠 Graphiques doublons (même histoire, plusieurs vues)

- **Source A** : Marchés affiche 4 vues des mêmes `scan.sectors`
  (`vx-mk-sectors-chart` bar, `sectors-heat` heatmap, `rotation` RRG scatter,
  `sectors-tree` treemap) et **3 jauges régime + 3 jauges breadth**.
- **Source B** : `CHART_INVENTORY.md` §C — jauges VIX/Breadth/Régime répétées
  Briefing↔Marchés ; funnel dupliqué Marchés↔Opportunités ; radar scorecard
  dupliqué Analyse↔Intelligence.
- **Décision** : une instance par question et par page ; garder ≤2 vues secteurs.
- **Validation** : par page, lors de la refonte (test navigateur + revue produit).

## C-10 🟡 Surfaces d'API redondantes (options, comité, stratégie)

- **Source A** : `/api/comite` (snapshot `scan_state.committee`) et `/api/strategie`
  (snapshot `scan_state.strategy`) — feeds.
- **Source B** : `/api/committee-review` + `/api/brief` (moteur `committee`) ;
  `/api/strategy/profile` + `/api/strategy/decision` (moteurs). Options fragmentées
  sur 4 fichiers (feeds / options_lab_api / options_intel_api / redesign).
- **Décision** : documenter la source canonique par métrique ; consolider les
  surfaces options ; distinguer snapshot vs recalcul.
- **Validation** : carte endpoint→source unique par métrique (voir
  `ROUTE_ENDPOINT_MAP.md`).

## C-11 🟠 Trois sources de couleurs (rappel transverse de C-02)

- **Sources** : `vertex/visualization/palette.py` (Python) ·
  `chart-theme-obsidian-copper.js` (JS) · `tokens.css` (CSS).
- **Décision** : une source canonique unique, les deux autres dérivées et testées.
- **Validation** : test de cohérence tri-source.

---

## Tableau de synthèse

| # | Sévérité | Sujet | Source canonique proposée | Bloque la refonte ? |
|---|---|---|---|---|
| C-01 | 🟠 | 8 vs 9 espaces | code+test (9) | oui (IA) |
| C-02 | 🟠 | séries palette divergentes | palette.py | oui (design) |
| C-03 | 🟡 | commentaires cuivre/orange | — | non |
| C-04 | ✅ | identité (résolu : Obsidian Copper/Inter) | Obsidian Copper / Inter | non (réglé) |
| C-05 | 🟠 | 2 moteurs chandeliers | LWC probable | oui (analyse) |
| C-06 | 🟠 | 2 registres nav | PRIMARY_NAV | oui (nav) |
| C-07 | 🔴 | data-quality tout MISSING en démo | état démo | non (mais honnêteté) |
| C-08 | 🔴 | décision confiante sur ticker inexistant | état « insuffisant » | non (mais honnêteté) |
| C-09 | 🟠 | graphiques doublons | 1 par question/page | oui (par page) |
| C-10 | 🟡 | API redondantes | 1 source/métrique | non |
| C-11 | 🟠 | 3 sources de couleurs | 1 canonique | oui (design) |
