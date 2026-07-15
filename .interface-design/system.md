# Vertex — Design System (interface-design)

> Source de vérité des décisions de craft pour VERTEX. Tenir ces valeurs :
> espacements sur la grille, stratégie de profondeur unique, couleurs de la
> palette, patterns documentés réutilisés (pas réinventés).

## Direction & feel

**VERTEX OBSIDIAN COPPER INSTITUTIONAL** — terminal d'analyse de trading, lecture
seule. Persona : trader qui scanne vite, veut la densité d'un cockpit sans bruit.
Feel : sombre, dense, précis, premium sobre (pas gaming, pas néon). Le motion est
*felt, not watched*. Une couleur = une signification. **Le bleu n'est jamais une
identité.** Donnée absente = état vide honnête (jamais un chiffre inventé).

Signature : le « V » cuivre sur obsidienne ; les états vides structurés avec
mini-viz fantôme ; les badges de statut honnêtes (LIVE/DELAYED/STALE/DEMO).

## Architecture

- Coque unique `vertex/ui/shell/` (8 espaces) ; pages `vertex/ui/pages/*.py`
  → `render_shell(...)`.
- CSS = `vertex/static/vertex/css/` : `tokens.css` (source unique), base, layout,
  components, buttons, states, forms, tables, charts, utilities, animations, responsive.
- JS graphiques = `vertex/static/vertex/js/charts/` + thème `chart-theme-obsidian-copper.js`.
- **Toujours** consommer les tokens (`var(--vx-*)`), jamais de hex en dur.

## Couleurs (tokens réels)

- Fonds : `--vx-obsidian-950 #050505 → -800 #0f1011` · graphites `--vx-graphite-900 #121315 → -700 #25282d`.
- Surfaces : base/raised/elevated/hover (rgba 15..34). Sidebar = même fond que canvas.
- Bordures : faint .035 · soft .065 · default .095 · strong .15 (rgba blanc).
- Texte (4 niveaux) : primary `#f3f1ed` · secondary `#b7b3ad` · muted `#817d77` · faint `#5e5b56`.
- **Marque** : `--vx-brand` = orange-500 `#cf6128` · hover 700 `#9f4117` · strong 400 `#df7739`. Cuivre `#914b2b`, copper-light `#b9683d`.
- Sémantiques : positive `#38b879` · negative `#dc5f52` · warning `#ce8a29` · option/violet `#85609f` · amber `#ce8a29` · beige `#c8ad8d` · neutral-chart `#8f8a83`.
- Info = `var(--vx-copper-light)` (jamais bleu). `--vx-cyan` mappé sur beige.
- Distribution ~60/30/10 : obsidienne domine, graphite secondaire, cuivre = accent rare.

## Profondeur (UNE stratégie)

Dark mode : **bordures + décalages de surface** en premier ; ombres discrètes en
appoint (les ombres portent peu sur fond noir). `--vx-shadow-1` (1px) · `-2` (4/16px)
· `-modal` (16/48px) · `--vx-glow-brand` (ring cuivre). Élévation = surface +7/+9/+12 %.

## Typographie

Font `Inter`, mono `SFMono/JetBrains`. Échelle : page 32 · section 19 · card 13 ·
body 13 · meta 11 · KPI 28 / KPI-sm 20. **La hiérarchie vient du poids + couleur**,
pas de la taille seule (ex. KPI : label 11/500/muted-tracked · value 28/800/mono-tabular
· delta 12). `text-wrap: balance` sur titres, `pretty` sur paragraphes.
`font-variant-numeric: tabular-nums` sur toute valeur dynamique.

## Espacement & formes

- Base 4px : `--vx-s1 4 … s4 16 s5 20 s6 24 s8 32 s16 64`. Padding symétrique.
- Rayons (échelle) : sm 8 (inputs/boutons) · r 12 · lg 14 (cartes) · modal 16 · pill 999.
- Densité : cartes padding s4 (16) ; compact s3 (12). Grille 12 col, max 1600px, sidebar 240px.

## Motion (craft)

- Courbe **ease-out marquée** : `--vx-ease-out: cubic-bezier(.23,1,.32,1)` (jamais ease-in).
  `--vx-t-fast 140ms · --vx-t 200ms · --vx-t-slow 260ms` (tous en ease-out).
- **Press feedback** `scale(.97)` sur boutons/onglets/chips/tickers.
- **Cartes** : lift `translateY(-1px)` au survol (+ bordure/ombre). Transform/opacity only.
- **Entrée de page** : cascade `vx-rise` échelonnée (.04/.08/.12/.15s) sur `.vx-content > *`.
- Durées < 300ms. `prefers-reduced-motion` : mouvement coupé, opacité gardée.

## Patterns de composants (mesures)

- `.vx-btn` — 34px h · 7/14 pad · r-sm 8 · 13/600 · variantes primary(gradient cuivre)/secondary/soft/ghost/danger/success/link · `:active scale(.97)`.
- `.vx-card` — surface-1 · bordure soft · r-lg 14 · pad 16 · hover lift. Variantes `--hero` (halo ambré, pad 20), `--compact` (pad 12), `.vx-elevated`, `.vx-active` (glow cuivre).
- `.vx-kpi` — label 11/muted/upper · value 28/800/mono/tabular · delta 12/mono.
- `.vx-badge` — pill 11/600 · variantes decision/risk/status/entity/demo (couleur = sens).
- `.vx-tab` — 13/600 · underline cuivre actif · count pill.
- **États** (`VX.states` dans vx-core.js) : loading (skeletons) · empty (mini-viz fantôme bars/line/ring + titre « Aucune donnée » + action) · stale/error bannières. Jamais de rectangle vide.
- **A11y** : `.vx-skip-link` (Tab → « Aller au contenu ») · `:focus-visible` ring cuivre 2px · cibles mobiles ≥ 40px · `.vx-sr-only`.

## Garde-fous (ne pas régresser)

- 0 hex bleu identité · cuivre = accent · READONLY intact · moteurs/données/décisions non touchés.
- 862 tests, 0 débordement horizontal (desktop/tablette/mobile), 0 erreur console.
- Toute nouvelle valeur : sur la grille 4px, tokens de la palette, une seule stratégie de profondeur.

## Références visuelles

Linear / Vercel / Stripe (densité, hover discrets, hiérarchie par poids) ·
terminal Bloomberg (densité de données, honnêteté). Rejeter : SaaS générique
multicolore, néons, glow permanent, donuts décoratifs.
