# SIGNAL OS · LOT 21 — LES NOMS DE COULEUR CESSENT DE MENTIR

Branche : `agent/vertex-signal-os-v1` · SW v226 → **v227** · Suite **3116 passed**

L'identité est violette (`#9B7BFF`) depuis le début de cette refonte. Le produit
la nommait encore sous **quatre générations d'alias périmés**.

---

## 1. Le constat

| famille | ce que le nom promet | ce que la valeur rend |
| --- | --- | --- |
| `--vx-ember-*` | braise | violet |
| `--vx-signal-*` | vert (« Signal Green ») | violet |
| `--vx-orange-*` | orange | violet |
| `--vx-copper-*` | cuivre | violet |

Un commentaire de `tokens.css` décrivait la chaîne comme « rampe **orange**
legacy → **cuivre** Ember ». Trois couleurs citées, **aucune exacte**.

C'est le même défaut que le fichier `chart-theme-obsidian-copper.js` renommé
plus tôt dans cette refonte : **un nom qui ment coûte à chaque lecture**, et il
ne se voit jamais à l'écran — donc rien ne le corrige jamais.

---

## 2. Ce qui a été fait

**126 sites** renommés vers la rampe canonique `--vx-violet-*` (ou
`--vx-brand-*`), dans **11 fichiers** :

| fichier | sites |
| --- | --- |
| `vertex/ui/pages/widget_lab.py` | 83 |
| `vertex/static/vertex/css/neon-glass.css` | 19 |
| `vertex/ui/pages/design_system_page.py` | 7 |
| `vertex/static/vertex/css/cockpit.css` | 5 |
| `vertex/static/vertex/js/pages/options-intel.js` | 3 |
| `vertex/static/vertex/js/vx-core.js` | 3 |
| `vertex/ui/pages/markets_page.py` | 2 |
| `vertex/ui/pages/design_system_demo.py` | 2 |
| `vertex/ui/pages/analysis_page.py` | 1 |
| `vertex/static/vertex/js/pages/options-gex.js` | 1 |

Le bloc d'alias **survit** dans `tokens.css`, marqué **DÉPRÉCIÉ** : le supprimer
casserait toute référence extérieure au dépôt, sans filet. Mais plus aucun
consommateur du produit ne le nomme.

Le nuancier de `/design-system` — la page qui existe pour **donner** la
référence — listait `--vx-orange-*` et `--vx-copper-*`. Il montre désormais la
rampe canonique, sous le nom `_MARQUE`.

---

## 3. Le piège évité, et il était exactement le défaut visé

Ma première version domiciliait le doux de marque sur `--vx-violet-soft` à
`.12`. Or **ce nom existe déjà** plus bas dans le même `:root`, à `.16`, pour le
violet **sémantique** des options (`--vx-violet-dim` en dérive).

La seconde déclaration l'aurait emporté : `--vx-brand-soft` serait passé de
`.12` à `.16`, et **le fond des actions primaires aurait changé de teinte sans
qu'aucun test ne le dise**.

> Un lot qui prétend supprimer les noms trompeurs a failli introduire un
> changement de couleur silencieux, par collision de noms.

La valeur vit désormais sur `--vx-brand-soft` (le nom que le produit emploie), et
l'alias `--vx-ember-soft` s'y réfère — la source de vérité ne porte plus un nom
périmé.

---

## 4. Le gardien a rattrapé mon travail incomplet

Ma première passe ne cherchait que `ember` et `copper`. Le gardien, lui, couvre
les **quatre** familles — et il a immédiatement échoué en désignant quatre
fichiers que j'avais manqués : `cockpit.css`, `options-gex.js`,
`options-intel.js`, `design_system_demo.py`.

C'est la valeur d'un gardien écrit à partir de la **règle** plutôt qu'à partir
de ce qu'on vient de corriger : il mesure l'intention, pas le geste.

Portée : le gardien ne retient que les emplois **réels** (`var(--vx-…)`), pas la
prose. Interdire la simple mention aurait rendu impossible d'expliquer, en
commentaire, pourquoi ces noms sont périmés.

---

## 5. La preuve qu'un renommage pur n'a rien changé

Un renommage se **prouve**, il ne se suppose pas. Relevé au navigateur, serveur
vérifié en `td-shell-v227` avant lecture :

- **10 pages** : `/`, `/markets`, `/opportunities`, `/analysis`,
  `/analysis/ACN`, `/portfolio`, `/options`, `/journal`, `/system`,
  `/widget-lab` ;
- pour chacune : **13 jetons résolus** (`--vx-brand*`, `--vx-violet-*`, et les
  alias `ember` / `copper` / `orange` / `signal`) **et** les couleurs
  réellement peintes (`color`, `background-color`, `border-color`, `fill`) sur
  un échantillon d'éléments ;
- comparaison avant / après : **0 écart**.

Mesuré deux fois : après la première passe (113 sites) et après la passe
complète (126 sites). Les deux fois, zéro.

---

## 6. Gardien — `tests/test_signal_os_noms_couleur_lot21.py` (4 tests)

| test | ce qu'il tient |
| --- | --- |
| aucun consommateur ne nomme un alias déprécié | la règle, sur les 4 familles |
| les alias survivent dans leur domicile | **contre-exemple** : ne pas « finir le travail » en cassant l'extérieur |
| le jeton doux de marque garde sa valeur | le piège de collision, figé |
| le nuancier officiel montre la rampe canonique | la page de référence ne documente plus des noms faux |

Le deuxième test est le plus important des quatre : sans lui, la lecture
naturelle du premier serait « supprimer les alias », ce qui est précisément ce
qu'il ne faut pas faire.
