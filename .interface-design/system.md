# Vertex — Design System (interface-design)

> Source de vérité des décisions de craft pour VERTEX. Tenir ces valeurs :
> espacements sur la grille, stratégie de profondeur unique, couleurs de la
> palette, patterns documentés réutilisés (pas réinventés).

## Direction & feel

**VERTEX BLACK GLASS INSTITUTIONAL** — terminal d'analyse de trading, lecture
seule. Persona : trader qui scanne vite, veut la densité d'un cockpit sans bruit.
Feel : noir profond, cartes en verre gris translucide, structure blanc/gris/argent,
précis, premium sobre (pas gaming, pas néon). Le motion est *felt, not watched*.
Une couleur = une signification. **Le bleu n'est jamais une identité ; le vert est
réservé au positif.** Donnée absente = état vide honnête (jamais un chiffre inventé).

Signature : le « V » argent sur obsidienne ; les surfaces en verre (translucide +
blur + bordure argent fine + reflet) ; les états vides structurés avec mini-viz
fantôme ; les badges de statut honnêtes (LIVE/DELAYED/STALE/DEMO).

## Architecture

- Coque unique `vertex/ui/shell/` (8 espaces) ; pages `vertex/ui/pages/*.py`
  → `render_shell(...)`.
- CSS = `vertex/static/vertex/css/` : `tokens.css` (source des hex canoniques),
  base, layout, components, buttons, states, forms, tables, charts, utilities,
  animations, responsive, puis **`glass.css` chargé en dernier** (couche verre +
  neutralisation argent — c'est la vérité d'exécution).
- JS graphiques = `vertex/static/vertex/js/charts/` + thème `chart-theme-obsidian-copper.js`
  (nom de fichier historique ; ses séries sont argent/gris, jamais bleu).
- **Toujours** consommer les tokens (`var(--vx-*)`), jamais de hex en dur.

## Couleurs (tokens réels)

- Fonds : `--vx-obsidian-950 … -800` (noir profond) · graphites `--vx-graphite-900 → -700`. Halo diffus neutre dans la sidebar.
- Surfaces verre : `--vx-glass-1` (carte) · `--vx-glass-2` (élevée/secondaire) · `--vx-glass-3` (critique/sélectionnée) + `--vx-glass-border[-faint/-strong]`, `--vx-glass-sheen`, `--vx-blur-sm/md/lg`. Classes utilitaires `.vx-glass-*`.
- Bordures : faint .055 · default .10 · strong .18 (rgba argent `222,227,237`).
- Texte (4 niveaux) : primary `#f3f1ed` · secondary `#b7b3ad` · muted `#817d77` · faint `#5c626b`.
- **Marque = argent** : `--vx-brand` = `--vx-silver #c9cdd4` · strong/hover `#e6e9ee` · `--vx-brand-gradient` = graphite `linear-gradient(135deg,#3a3f47,#23262c)`. (Les hex canoniques verts restent figés dans `tokens.css` mais sont overridés en argent par `glass.css`.)
- Sémantiques STRICTES : positive `#36c889` · negative `#ed655c` · warning/amber `#dda23b` · option/violet `#9c79d0` (réservé options) · neutral-chart gris. Le vert = positif uniquement ; l'orange = prudence/incertitude.
- Info = argent (jamais bleu). `--vx-cyan`/`--vx-blue` mappés sur des neutres.
- Distribution ~60/30/10 : obsidienne domine, verre gris secondaire, argent = structure ; sémantique = accent rare et signifiant.

## Profondeur (UNE stratégie)

Dark mode : **verre (translucidité + blur) + bordures argent + décalages de surface**
en premier ; ombres douces en appoint + reflet interne haut. `--shadow-card`,
`--shadow-float`, `--vx-glow-brand` (ring argent). Élévation = surface `--vx-glass-1 → -2 → -3`.

## Typographie

Font `Inter`, mono `IBM Plex Mono / SFMono`. Échelle : page 30-32 · section 17-19 · card 12-14 ·
body 13 · meta 11 · KPI 24-30 / KPI-sm 20. **La hiérarchie vient du poids + couleur**,
pas de la taille seule (ex. KPI : label 11/500/muted-tracked · value 28/800/mono-tabular
· delta 12). `text-wrap: balance` sur titres, `pretty` sur paragraphes.
`font-variant-numeric: tabular-nums` sur toute valeur dynamique.

## Espacement & formes

- Base 4px : `--vx-s1 4 … s4 16 s5 20 s6 24 s8 32 s16 64`. Padding symétrique.
- Rayons (échelle) : sm 8-10 (inputs/boutons) · r 12 · lg 14-16 (cartes) · modal 16 · pill 999.
- Densité : cartes padding s4 (16) ; compact s3 (12). Grille 12 col, max ~1600px, sidebar 240px.

## Motion (craft)

- Courbe **ease-out marquée** : `--vx-ease-out: cubic-bezier(.23,1,.32,1)` (jamais ease-in).
  `--vx-t-fast 140ms · --vx-t 200ms · --vx-t-slow 260ms` (tous en ease-out).
- **Press feedback** `scale(.97-.98)` sur boutons/onglets/chips/tickers.
- **Cartes** : lift `translateY(-1px)` au survol (+ bordure argent/ombre). Transform/opacity only.
- **Entrée de page** : cascade `vx-rise` échelonnée (.04/.08/.12/.15s) sur `.vx-content > *`.
- Durées < 300ms. `prefers-reduced-motion` : mouvement coupé, opacité gardée.

## Patterns de composants (mesures)

- `.vx-btn` — 34px h · 7/14 pad · r-sm · 13/600 · variantes primary (verre graphite/argent)/secondary/soft/ghost/danger/success/link · `:active scale(.97)`.
- `.vx-card` — verre `--vx-glass-1` · bordure argent · r-lg · pad 16 · hover lift. Variantes `--hero` (verre élevé, pad 20), `--compact` (pad 12), `.vx-elevated`, `.vx-active`/`--selected` (verre `-3` + liseré argent). Classes utilitaires `.vx-glass-*`.
- `.vx-kpi` — label 11/muted/upper · value 28/800/mono/tabular · delta 12/mono · mini-graphe neutre (couleur seulement si directionnel).
- `.vx-badge` — pill 11/600 · variantes decision/risk/status/entity/demo (couleur = sens).
- `.vx-tab` — 13/600 · underline argent actif · count pill.
- `.vx-conviction` — barres segmentées (piste neutre, remplissage argent → sémantique selon force).
- **États** (`VX.states` dans vx-core.js) : loading (skeletons) · empty (mini-viz fantôme bars/line/ring + titre « Aucune donnée » + action) · stale/error/partial bannières. Jamais de rectangle vide.
- **A11y** : `.vx-skip-link` (Tab → « Aller au contenu ») · `:focus-visible` ring argent 2px · cibles mobiles ≥ 40px · `.vx-sr-only`.

## Garde-fous (ne pas régresser)

- 0 hex bleu identité · argent = structure, vert = positif, rouge = négatif/risque, orange = prudence · READONLY intact · moteurs/données/décisions non touchés.
- Suite complète verte, 0 débordement horizontal (desktop/tablette/mobile), 0 erreur console.
- Toute nouvelle valeur : sur la grille 4px, tokens de la palette, une seule stratégie de profondeur (verre + bordures argent).

## Références visuelles

Linear / Vercel / Stripe (densité, hover discrets, hiérarchie par poids) ·
terminal Bloomberg (densité de données, honnêteté) · référence Black Glass fournie
(cockpit sombre, cartes verre, sémantique stricte). Rejeter : SaaS générique
multicolore, néons, glow permanent, donuts décoratifs, bleu identité.
