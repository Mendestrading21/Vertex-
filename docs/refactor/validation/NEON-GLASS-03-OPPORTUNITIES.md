# Validation — NEON GLASS 03 : Opportunités (refonte premium)

> Issue #14, 3ᵉ espace. **Marchés (02B) est validé comme patron de qualité.**
> Opportunités adopte le même système : composition asymétrique ordonnée, widgets
> à identité, glass premium, densité maîtrisée, orange réservé à l'identité/action,
> couleurs sémantiques intactes, graphiques réellement redessinés, zéro grand vide.
> Branche `agent/vertex-neon-glass-graphs`.
> **ANALYSIS ONLY — aucun ordre, IBKR READONLY. Aucun moteur/donnée/route modifiés.
> Analyse non démarrée.**

Mission de la page (Constitution §2/§15) : **« Qu'est-ce qui mérite réellement mon
attention et mon capital ? »** — réduire le bruit, faire ressortir les rares
asymétries fortes.

## 1. Fichiers modifiés

| Fichier | Nature |
|---|---|
| `vertex/ui/pages/opportunities_page.py` | Vue **radar** entièrement recomposée : hero éditorial compact, carte opportunité dominante, shortlist premium, op-scatter redessiné, entonnoir compact, matrice de comparaison. Champs moteur réels uniquement. |
| `vertex/static/vertex/css/neon-glass.css` | **Scope glass étendu** à `[data-space="opportunities"]` (base partagée) + bloc de widgets premium `vx-op-*` (hero-chips, dominant, ticker cards, matrice, scatter). |
| `vertex/app/routes/system.py` | Service worker `v53 → v54`. |
| `tests/test_neon_glass_01.py` | Gardiens : Opportunités **migré** (scope), Portefeuille toujours hors scope, widgets `vx-op-*` présents. |
| `tests/test_*` (SW) | Bump v54. |

**Aucun token global, aucun fichier de shell, aucun moteur touché.** Tout le style
Opportunités est scopé `.vx-content[data-space="opportunities"]`.

## 2. Structure avant / après (vue Radar)

| Avant | Après |
|---|---|
| Hero + KPI plats | **Hero éditorial compact** (tag À ÉTUDIER/Patience + phrase honnête + chips S+/S/A/Meilleure/Données + CTA) |
| 6 cartes « top » identiques (effet copier-coller) + bug `[object Object]` | **1 carte dominante** distincte + **3 cartes shortlist** à densité variable |
| Entonnoir **géant** (~40 % écran) | **Entonnoir compact** (col-4) + conclusion « plus forte déperdition » |
| Scatter générique dans une boîte | **Op-scatter signature** : quadrants nommés, labels directs sur les meilleurs, orange = sélection, tooltip |
| Classement « décomposition » en barres arc-en-ciel (long) | **Matrice de comparaison** premium (rails, meilleur du critère en orange) |

Widgets visibles (respecte le budget : 1 hero · 1 dominante · 3 secondaires · 2 graphes majeurs · 1 matrice).

## 3. Widgets reconstruits (identité forte, classes stables `vx-op-*`)

- **Hero** `vx-op-hero-*` : compte S+/S/A, meilleure, qualité des données, message
  éditorial, conclusion — jamais 40 % de vide, jamais inventé.
- **Opportunité dominante** `vx-op-dominant` : bandeau signature pleine largeur —
  ticker + **grade** (moteur `r.grade`), score /100, momentum 1S/1M/1T/1A, grille
  métriques (**Asymétrie** `vx_asym`, **Prob. gain** `vx_pwin`, **R:R visé** `vx_rr`,
  **Edge** `vx_edge`), **catalyseur** (résultats datés du calendrier — réels),
  **invalidation** (prob. stop-first `vx_stopfirst` + renvoi dossier), profil, CTA
  « Ouvrir le dossier ». Distincte des cartes secondaires.
- **Shortlist** `vx-op-tk` (×3) : monogramme, ticker, secteur, score, grade,
  asym/R:R/prob, catalyseur court, **barres de momentum multi-horizon**, action.
- **Matrice de comparaison** `vx-op-cmp` (2-4 candidats) : critères Score /
  Asymétrie / Prob. gain / R:R / Edge / Momentum / Qualité données ; **rails
  d'intensité**, meilleur du critère en **orange**, colonne tête de shortlist
  surlignée. Pas de radar (conforme à la consigne).

## 4. Graphes redessinés

- **Op-scatter** (pièce signature) : axes nommés (qualité → / timing ↑), quadrants
  interprétés (À ÉTUDIER / TIMING SEUL / QUALITÉ SEULE / À ÉVITER), points séparés,
  taille = intensité du signal, couleur = verdict (émeraude/corail/acier), **point
  actif = orange** (meilleure opportunité), **étiquettes directes** sur les 4
  meilleurs candidats (haut-droit), tooltip enrichi (qualité/timing/asym), conclusion,
  panneau « point sélectionné » cliquable, lisible mobile.
- **Entonnoir** : trapèzes décroissants réels (univers → éligibles → radar →
  prioritaires → actionnables → suivis → positions), chips de rôles, **conclusion =
  plus forte déperdition entre étages** (calculée sur données réelles), aucune fausse
  progression (repli honnête si < 2 étages).
- **Mini-momentum** (dominante + shortlist) : barres 1S/1M/1T/1A réelles (perf_w/m/q/y),
  couleur sémantique.

## 5. Op-scatter — détail

Reconstruit sans changer les données : `x = strat_score`, `y = timing (st_tech/rs)`,
taille `= anomaly_score/sigcount`. Ajouts visuels : étiquettes directes top-4,
sélection orange, tooltip glass (thème), conclusion textuelle. **Aucune valeur
inventée.**

## 6. Entonnoir — détail

Source `/api/opportunities/funnel` (inchangée). Rendu compact (col-4, SVG borné à
330 px), conclusion « plus forte déperdition : X → Y (−N) ». Le message honnête
« Aucun dossier actionnable — c'est un résultat valide, pas un manque à remplir »
est conservé.

## 7. Comparaison — détail

Matrice 7 critères × 2-4 candidats (les mieux notés), rails d'intensité relative,
meilleur par critère en orange, colonne tête de shortlist surlignée. Champs moteur
réels ; `n/d` honnête si absent. Remplace l'ancien « classement décomposition »
(supprimé — code mort retiré : `renderTopCards`, `renderRanking`, `scoreBar`, `IDX`).

## 8. Responsive (mesuré : 390 / 768 / 1280 / 1440 / 1920)

Sweep Chromium (chargement naturel `load`) :

| Vue / viewport | Débordement réel | Erreurs console |
|---|---|---|
| radar 390/768/1280/1440/1920 | **0 px** (5/5) | **0** |
| stocks / options / anomalies / calendar (1440) | **0 px** (4/4) | **0** |

**9/9 combinaisons propres.** Mobile : hero compact, dominante pleine largeur
lisible, shortlist empilée, scatter simplifié lisible, comparaison en table à
défilement contrôlé — aucun débordement horizontal non maîtrisé.

> Note honnêteté : une erreur console fantôme (« Class constructor An… ») n'apparaît
> QUE sous instrumentation Playwright synthétique (nudge `dispatchEvent('load')`) ;
> au **chargement naturel de la page, la console est à 0** (vérifié sans
> instrumentation). Ce n'est pas une erreur réelle vue par l'utilisateur.

## 9. Tests

- `python -m compileall -q terminal.py vertex` → **exit 0**.
- `python -m pytest tests/ -q` → **962 passed, 2 skipped** (baseline 961 → **+1**
  gardien ; aucune régression).
- Gardiens durcis : Opportunités migré (scope), Portefeuille hors scope (anti
  big-bang), widgets `vx-op-*` présents, SW v54, identité orange sans bleu.

## 10. Captures (évidence de session)

`beforeOP-radar-1440.png` (avant : cartes plates, 6 top-cards clones, entonnoir géant,
`[object Object]`) · `afterOP-radar-{390,768,1440}.png` (après : hero compact,
dominante signature, shortlist, scatter à labels, entonnoir compact, matrice).

## 11. Risques

- **Risque faible** : composition HTML/CSS + SVG inline ; **aucune donnée/moteur/
  route touchés** ; réversible. En démo, `grade`/`vx_*` proviennent du board
  synthétique étiqueté.
- Pas de nom de société dans les lignes de scan (`sector`/`industry` affichés à la
  place — jamais inventé).

## 12. Éléments différés

- Logos réels dans les monogrammes (aucun asset embarqué — monogramme texte pour
  l'instant, conforme « aucune nouvelle dépendance réseau »).
- Vues **Actions / Options / Anomalies / Calendrier** : héritent du glass de base
  (scope) mais leur composition fine (tables premium, payoff) sera traitée si
  souhaité ; hors périmètre de cette passe centrée sur le Radar décisionnel.
- Catalyseur : couvre les résultats datés du calendrier ; d'autres catalyseurs
  (macro par titre) restent à câbler si données réelles disponibles.

## Verdict

**Opportunités atteint le niveau de référence Marchés** : hero éditorial compact,
carte dominante signature, shortlist à identité, op-scatter redessiné (pièce
signature), entonnoir compact à conclusion, matrice de comparaison premium. **Zéro
grand vide, zéro widget générique, densité maîtrisée, orange réservé à
l'identité/action, sémantiques intactes.** **962 tests verts · 9/9 combinaisons sans
débordement ni erreur console · READONLY intact · tokens globaux & shell non touchés
· aucune donnée inventée.** **Arrêt pour validation humaine avant Analyse.**
