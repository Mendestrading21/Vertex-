# Validation — NEON GLASS 02B : Marchés, passe de COMPOSITION visuelle

> Issue #14. La palette **Orange Ember** et le socle technique sont **validés**.
> Cette passe ne retouche NI les tokens globaux, NI le shell, NI les moteurs :
> elle corrige la **composition** de Marchés (hiérarchie, taille des cartes,
> profondeur du glass, identité de chaque widget, design des graphiques, zones
> vides, rendu générique). Branche `agent/vertex-neon-glass-graphs`.
> **ANALYSIS ONLY — aucun ordre, IBKR READONLY intact. Opportunités non démarré.**

## 0. Périmètre strict respecté

| Consigne | Respect |
|---|---|
| Ne plus changer les tokens globaux | ✅ `tokens.css` **non modifié** |
| Ne plus toucher au shell | ✅ aucun fichier shell touché ; tout est scopé `.vx-content[data-space="markets"]` |
| Ne modifier aucun moteur | ✅ aucune route/endpoint/calcul modifié ; mêmes données, mêmes valeurs |
| Ne pas démarrer Opportunités | ✅ |

Fichiers modifiés : `vertex/ui/pages/markets_page.py` (widgets + composition) et
`vertex/static/vertex/css/neon-glass.css` (règles **markets-scopées** uniquement).

## 1. Grandes zones vides supprimées

- **Hero « Régime de marché »** — avant : quand le régime est indéterminé (moteur
  < 3 dimensions), un **immense rectangle vide** occupait ~40 % de l'écran (« Aucune
  donnée » + jauge à 0 %). Après : **hero compact éditorial** — tag `INDÉTERMINÉ`,
  phrase honnête (« le moteur reste honnête et bloque le nouveau risque »), puis les
  **signaux de marché réellement disponibles** (VIX à rail, participation, régime
  S&P, risk-on/off) et l'action suivante. Hauteur réduite, zéro vide, 100 % de
  données réelles.
- **Cartes macro 10Y / DXY** (sans série) — avant : demi-carte droite vide (« série
  n/d »). Après : **variante flat plein-largeur** (valeur + variation + relation),
  aucune colonne vide.
- **Leadership sectoriel** — avant : un seul secteur + grand vide. Après :
  **classement visuel top-5** avec barres d'intensité (meneur en orange) + tickers
  leaders — remplit la carte à côté du graphe de référence.

## 2. Cartes reconstruites (widgets à identité)

| Widget | Avant | Après |
|---|---|---|
| **Index cards** (S&P/Nasdaq/Dow/Russell) | KPI + sparkline générique, identiques | **Widget premium** : monogramme (S&P/NDQ/DJIA/RUT), valeur forte, variation, **mini-area à dégradé + point actif**, **plage de série**, **état relatif** (« près du haut/bas · milieu de plage »), accent latéral sémantique. |
| **Macro cross-asset** (10Y/DXY/WTI/Or/BTC) | KPI uniformes | **Cartes identitaires** : monogramme, valeur, variation (·niveau pour taux/dollar), **relation clé** (« Dollar fort = vent de face… »), area à dégradé si série ; variante flat sinon. |
| **Hero régime** | carte plate | **bandeau hero** avec question, nom de régime à ton sémantique + jauge + chips de modulation, OU état compact éditorial honnête. |
| **Leadership** | 1 ligne | **classement à barres d'intensité** (hiérarchie par intensité, pas arc-en-ciel). |

Toutes les classes sont **stables** (`vx-mk-idx`, `vx-mk-macro`, `vx-mk-sig`,
`vx-mk-lead-*`, `vx-mk-hero-grid`) — aucun sélecteur fragile.

## 3. Composition asymétrique mais ordonnée (Vue d'ensemble)

Grille non uniforme, hiérarchisée :

1. **Bandeau hero** : Régime (`col-8`, compact) + Risque du jour (`col-4`, vertical).
2. **Bloc indices** horizontal, précédé d'un **titre de section** (« INDICES ACTIONS »).
3. **Graphe de référence** (`col-8`) + **Leadership** visuel (`col-4`).
4. **Comparaison multi-indices** pleine largeur.
5. **Top / Flop** en deux colonnes.

Macro : titre de section + rangée dense d'actifs identitaires (aires ou stats
compactes), puis appétit pour le risque + KPIs.

## 4. Profondeur du glass par priorité

- Reflet supérieur (`inset 0 1px 0`) + bord intérieur fin sur toutes les cartes.
- **Hero** = profondeur maximale (`--ng-shadow-raised`) ; cartes standard =
  médium ; `--compact` = allégée.
- Accent orange réservé à l'**actif / la sélection / la donnée importante**
  (monogrammes, meneur, onglet actif) — jamais toutes les cartes en orange.
- Surfaces translucides chaudes (jamais bleues), blur contrôlé (10–14 px).

## 5. Graphiques redessinés

- **Mini-areas** (index & macro) : ligne + **remplissage dégradé** + point actif
  final, couleur **sémantique** (émeraude/corail/cyan/gris) — fluides, lumineux.
- **Graphe de référence** (SPY/proxy) : area remplie, conclusion textuelle,
  « Comprendre ce graphique ».
- **Comparaison multi-indices** : lignes propres (comparaison = lignes, pas aires),
  série S&P en tête orange, légende + rebasage 0 % expliqué.
- **RRG secteurs** : quadrants interprétés (LEADING/IMPROVING/WEAKENING/LAGGING),
  axes nommés, dots sémantiques, tickers orange.
- **Jauges** (participation/VIX/régime) : bandes sémantiques, valeur centrale
  dominante, lecture sous la valeur. **Funnel / donut / histogramme / waterfall**
  (Breadth) en palette Ember, hiérarchie par intensité.

Aucun graphe recréé côté moteur : habillage + options d'affichage via les
callbacks du Chart Shell (aucune modification des fabriques globales → les autres
espaces ne bougent pas).

## 6. Contrôle visuel vs intention moodboard

> Aucune image de moodboard n'est versionnée (cf. `VISUAL_REFERENCE_MAP.md`) : la
> direction est portée par les références nommées (Linear/Vercel/Stripe/Bloomberg/
> TradingView) — densité maîtrisée, hiérarchie par poids, profondeur par surfaces,
> **zéro remplissage cosmétique**.

| Question | Réponse |
|---|---|
| Chaque widget a-t-il une identité ? | ✅ monogramme, forme, visualisation, relation propres |
| Une capture seule paraît-elle premium ? | ✅ (voir §8) |
| Voit-on autre chose qu'une grille ? | ✅ composition asymétrique + titres de section |
| Les graphes sont-ils réellement redessinés ? | ✅ aires dégradées, quadrants interprétés, jauges sémantiques |
| Les états vides restent-ils élégants ? | ✅ hero compact éditorial, jamais de grand vide |
| Marchés ressemble-t-il à une app de référence ? | ✅ densité Bloomberg + finition Linear/Stripe |

## 7. Composants canoniques réutilisés

Chart Shell `C.card` (title/question/conclusion/source/légende/aide/états), jauge,
RRG scatter, heatmap, donut, funnel, waterfall, timeline, rails, `VX.states.*`.
**Aucun nouveau moteur graphique** ; les nouveaux widgets (`indexCard`,
`macroCard`, hero compact, leadership) sont du HTML/CSS scopé + SVG inline (aires),
sans dépendance réseau nouvelle.

## 8. Captures (évidence de session)

`afterB-{overview,macro,sectors,breadth,volatility}-{1440,1920}.png` +
tablette `-768` + mobile `-390` (overview, macro, sectors). Vérifié : hero compact
à signaux réels, index cards premium (monogramme/plage/état relatif/area dégradée),
macro identitaire sans demi-carte vide, leadership à barres, RRG interprété, jauges
sémantiques, composition asymétrique, **shell orange Ember**, DÉMO étiqueté.

## 9. Tests · Console · Responsive

- `python -m compileall -q vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **961 passed, 2 skipped** (aucune régression ;
  changements visuels only).
- Sweep Chromium **5 vues × 5 viewports (390/768/1280/1440/1920) = 25/25** :
  **débordement réel 0 px**, **0 erreur console applicative** (hors
  `ERR_CONNECTION_RESET` Google Fonts du bac à sable, non applicatif).
- Service worker inchangé (`td-shell-v53` déjà émis à la passe précédente ; le shell
  n'a pas rechangé). Neon-glass.css et markets_page.py sont hors périmètre du cache
  shell versionné mais servis frais.

## 10. Risques & éléments différés

- **Risque faible** : composition HTML/CSS + SVG inline, **aucune donnée/moteur/route
  touchés**, réversible. En démo, `/api/market/regime` reste honnêtement `UNKNOWN`
  (< 3 dimensions) — géré par le hero compact.
- **Différé** (après validation) : cadran macro « relations clés » interactif ;
  term structure IV si données réelles ; consolidation structurelle du nombre de
  graphes (hors périmètre de cette passe visuelle).

## Verdict

**Marchés n'est plus une grille administrative** : hero compact éditorial (zones
vides supprimées), index & macro reconstruits en widgets à identité, leadership
visuel, glass à profondeur hiérarchisée, graphiques à aires dégradées et jauges
sémantiques, composition asymétrique ordonnée. **961 tests verts · 25/25
combinaisons propres · READONLY intact · tokens globaux & shell non touchés ·
aucune donnée modifiée.** **Arrêt pour validation humaine avant Opportunités.**
