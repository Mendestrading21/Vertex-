# Registre page → widget, et contrat des graphiques

Contrôles **060** (registre page → widget) et **061** (contrat des graphiques).

Le registre n’est pas déclaré : il est **mesuré** en lisant les sites d’appel
des primitives de `VXCharts`, et en cherchant dans chaque expression les cinq
champs que le contrat exige.

## Pourquoi la mesure est statique, et non runtime

Un premier relevé a été fait dans le navigateur, sur l’application réellement
exécutée. Il n’a trouvé **une seule** carte sur les 24 sous-vues : sans accès
aux fournisseurs de marché, presque tous les graphiques tombent en état vide
**avant** d’être construits. Un registre bâti là-dessus aurait affirmé que le
produit contient un graphique.

Le registre est donc lu dans le code. C’est une limite déclarée, pas un choix
de confort : le relevé runtime reste dans `tools/vertex_2_0_graphiques.py` et
redeviendra la mesure de référence sur une machine connectée.

## Conformité mesurée

| Champ du contrat | Cartes qui le portent | Sur |
|---|---:|---:|
| Question | **69** | 72 |
| Conclusion | **51** | 72 |
| Source | **72** | 72 |
| Unité | **72** | 72 |
| Période | **9** | 72 |

**72 cartes** dans 12 fichiers.

### Ce que « unité » et « source » valaient avant ce lot

| Champ | Avant | Après |
|---|---:|---:|
| Unité | 20 / 72 | **72 / 72** |
| Question | 64 / 72 | **69 / 72** au site d’appel, **72 / 72** à l’écran |
| Source | 66 / 72 | **72 / 72** |

Les trois cartes dont le site d’appel ne porte pas de question sont les trois
treemaps du Portefeuille : leur **carte hôte** la pose déjà, juste au-dessus.
La passer aussi à la primitive l’affichait deux fois à trois centimètres
d’écart. Le contrat est tenu à l’écran ; il l’est par la carte, pas par la
primitive — et le registre le dit plutôt que d’afficher un 72/72 flatteur.

L’unité a d’abord été comptée à 15/72, puis à 20/72 : la première mesure ne
cherchait qu’un badge `unit:`, alors qu’une unité peut légitimement vivre dans
un **titre d’axe**, un **suffixe de graduation** ou une **infobulle**. Mesurer
mal et « corriger » ensuite 52 cartes déjà conformes aurait été pire que de ne
rien faire. Le détecteur regarde les quatre emplacements.

### Deux primitives ne portaient RIEN, et l’ignoraient en silence

`treemap` et `waterfall` rendent un SVG nu : contrairement à `VXCharts.card`,
elles n’ont jamais eu de coquille de carte. Les options `unit`, `source` et
`question` qu’on leur passait étaient **silencieusement ignorées** — le
contrat ne pouvait donc pas être tenu là où elles servent, et personne ne
pouvait le voir. Elles portent désormais leur question au-dessus et leur
unité, source, horodatage et limites en dessous.

### Conclusion et période : ce qui n’est PAS un manque

**Conclusion — 51/72.** Une conclusion est une *lecture* de la donnée. Un
treemap de poids ne conclut rien au-delà de ce qu’il montre ; lui coller une
phrase reviendrait à fabriquer une interprétation. Les 21 cartes sans
conclusion sont des cartes descriptives, pas des cartes bâclées.

**Période — 9/72.** Une période n’a de sens que pour une **série temporelle**.
La majorité de ces cartes sont des instantanés : open interest par strike,
répartition sectorielle, allocation. Leur « période » est l’instant de la
mesure — que le pied de carte porte déjà, horodaté. Ajouter un badge de
période à un instantané inventerait une fenêtre qui n’existe pas.

## Registre par page

### Analyse

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `card` | Croissance × rentabilité vs pairs | % | ● | ● | ● | `analysis_page.py:509` |
| `card` | Croissance trimestrielle | % | ● | ● | ● | `analysis_page.py:566` |
| `card` | Dispersion des rendements — Monte-Carlo & bootstrap | % horizon | ● | ● | ● | `analysis_page.py:678` |
| `card` | (titre dynamique) | RSI | ● | ● | ● | `analysis_page.py:1046` |
| `card` | (titre dynamique) | titres | ● | ○ | ● | `analysis_page.py:1061` |

### Aujourd’hui

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `card` | (titre dynamique) | points d’indice | ● | ● | ● | `briefing.py:1069` |
| `card` | Qui mène ? | % | ● | ● | ● | `briefing.py:1127` |
| `card` | Courbe des taux US | % | ● | ● | ● | `briefing.py:1161` |
| `card` | Rotation — force relative × momentum | axe/infobulle | ● | ● | ● | `briefing.py:1209` |
| `sectorCard` | Rotation sectorielle | % | ● | ● | ● | `briefing.py:1242` |
| `heatmapCard` | Performance et momentum par secteur | % | ● | ● | ● | `briefing.py:1253` |
| `treemap` | (titre dynamique) | titres par secteur | ● | ○ | ● | `briefing.py:1272` |
| `card` | Tendance de participation | % de titres | ● | ● | ● | `briefing.py:1406` |
| `waterfall` | (titre dynamique) | points de santé (0-100) | ● | ○ | ● | `briefing.py:1444` |
| `timelineCard` | Calendrier & catalyseurs | événements | ● | ○ | ● | `briefing.py:1783` |

### Marchés

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `card` | Indices — performance comparée | % | ● | ● | ● | `markets_page.py:542` |
| `areaCard` | (titre dynamique) | points d’indice | ● | ● | ● | `markets_page.py:568` |
| `card` | Courbe des taux US | % | ● | ● | ● | `markets_page.py:628` |
| `timelineCard` | Calendrier macro | événements | ● | ○ | ● | `markets_page.py:673` |
| `heatmapCard` | Performance et momentum par secteur | % | ● | ● | ● | `markets_page.py:685` |
| `heatmapCard` | Performance et momentum par secteur | % | ● | ● | ● | `markets_page.py:701` |
| `card` | Rotation sectorielle — force relative × momentum | axe/infobulle | ● | ● | ● | `markets_page.py:730` |
| `card` | Tendance de participation | % de titres | ● | ○ | ● | `markets_page.py:811` |
| `donutCard` | Répartition des verdicts du scan | titres | ● | ● | ● | `markets_page.py:823` |
| `waterfall` | (titre dynamique) | points de santé (0-100) | ● | ○ | ● | `markets_page.py:855` |

### Opportunités

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `card` | Le POURQUOI en un regard — avantage × proba de gain | axe/infobulle | ● | ● | ● | `opportunities_page.py:440` |
| `card` | Dispersion Monte-Carlo | % | ● | ● | ● | `opportunities_page.py:515` |
| `sectorCard` | Secteurs des résultats | titres | ● | ● | ● | `opportunities_page.py:552` |
| `heatmapCard` | Carte secteur × statut | titres | ● | ● | ● | `opportunities_page.py:684` |
| `donutCard` | Verdicts des résultats | titres | ● | ○ | ● | `opportunities_page.py:709` |
| `card` | Qualité × proba de profit — où sont les bons contrat | axe/infobulle | ● | ● | ● | `opportunities_page.py:899` |
| `card` | IV selon l’échéance | axe/infobulle | ● | ● | ● | `opportunities_page.py:961` |
| `payoffCard` | ${c.sym} ${c.strike} ${c.type} ${c.exp} | $ par contrat | ● | ● | ● | `opportunities_page.py:1052` |
| `thetaCard` | Décomposition temps | $ par jour | ● | ● | ● | `opportunities_page.py:1071` |
| `ivSensitivityCard` | Sensibilité IV | $ | ● | ● | ● | `opportunities_page.py:1075` |
| `donutCard` | Secteurs du portefeuille | % du portefeuille | ● | ○ | ● | `opportunities_page.py:1196` |
| `timelineCard` | Calendrier des catalyseurs | événements | ● | ○ | ● | `opportunities_page.py:1322` |

### Options

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `card` | Structure par terme de l’IV | axe/infobulle | ● | ● | ● | `options-intel.js:419` |
| `card` | Cône de mouvement attendu | axe/infobulle | ● | ● | ● | `options-intel.js:467` |
| `card` | Open interest par strike | axe/infobulle | ● | ● | ● | `options-intel.js:497` |
| `card` | Smile d’IV | axe/infobulle | ● | ● | ● | `options-intel.js:559` |
| `thetaCard` | Décote temps (theta) | $ par jour | ● | ○ | ● | `options-intel.js:647` |
| `ivSensitivityCard` | Sensibilité à l\ | $ de prime | ● | ○ | ● | `options-intel.js:648` |
| `card` | Payoff à l\ | P&L $ (1 structure) | ● | ● | ● | `options-structure.js:219` |

### Options · dossier

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `card` | Structure par terme de l’IV | axe/infobulle | ● | ● | ● | `options-symbol.js:133` |
| `card` | Cône de mouvement attendu | cours | ● | ● | ● | `options-symbol.js:144` |
| `card` | Open interest par strike | contrats | ● | ● | ● | `options-symbol.js:153` |
| `card` | Smile d’IV ·  | axe/infobulle | ● | ● | ● | `options-symbol.js:164` |
| `heatmapCard` | Scénarios spot × temps | $ de prime | ● | ○ | ● | `options-symbol.js:196` |
| `card` | Décote temps (theta) | $ par jour | ● | ○ | ● | `options-symbol.js:205` |
| `card` | Sensibilité à l’IV | axe/infobulle | ● | ○ | ● | `options-symbol.js:212` |
| `volSurfaceCard` | Surface de volatilité — strike × échéance | % d’IV | ● | ○ | ● | `options-symbol.js:387` |
| `card` | Skew par échéance | pts IV | ● | ● | ● | `options-symbol.js:400` |

### Performance

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `equityCard` | Courbe d’équité (déclarée) | $ | ● | ● | ● | `performance_page.py:433` |
| `drawdownCard` | Drawdown depuis les pics | % | ● | ● | ● | `performance_page.py:443` |
| `card` | Distribution des rendements par trade | trades | ● | ● | ● | `performance_page.py:545` |
| `card` | Erreurs déclarées par mois | erreurs | ● | ● | ● | `performance_page.py:685` |
| `card` | Rendement moyen +20 séances par verdict | % | ● | ○ | ● | `performance_page.py:740` |

### Portefeuille

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `heatmapCard` | Corrélations du portefeuille | coefficient | ● | ● | ● | `portfolio_page.py:313` |
| `treemap` | (titre dynamique) | $ investi | ○ | ○ | ● | `portfolio_page.py:519` |
| `equityCard` | Courbe d’équité (cumulée) | $ | ● | ● | ● | `portfolio_page.py:687` |
| `drawdownCard` | Drawdown depuis les pics | % | ● | ● | ● | `portfolio_page.py:694` |
| `heatmapCard` | P&L moyen par mois (clôtures) | % | ● | ● | ● | `portfolio_page.py:716` |
| `card` | Contribution au P&L (positions ouvertes) | $ | ● | ● | ● | `portfolio_page.py:730` |
| `treemap` | (titre dynamique) | $ investi | ○ | ○ | ● | `portfolio_page.py:819` |
| `donutCard` | CALL vs PUT | contrats | ● | ● | ● | `portfolio_page.py:846` |
| `treemap` | (titre dynamique) | % du portefeuille | ○ | ○ | ● | `portfolio_page.py:1481` |

### Suivi

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `card` | Performance hypothétique depuis le suivi | axe/infobulle | ● | ● | ● | `tracking.js:68` |

### Système

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `barCard` | Plus forts mouvements du jour | % | ● | ○ | ● | `system_page.py:393` |
| `donutCard` | Qualit&eacute; des donn&eacute;es ( | titres | ● | ● | ● | `system_page.py:786` |

### Vertex IA

| Widget | Carte | Unité | Q | C | S | Fichier |
|---|---|---|:-:|:-:|:-:|---|
| `card` | Carte du comité — conviction × accord | axe/infobulle | ● | ● | ● | `intelligence_page.py:478` |
| `barCard` | Sharpe par fen&ecirc;tre (walk-forward) | ratio | ● | ● | ● | `intelligence_page.py:687` |

---

`●` porté · `○` absent · l’unité « axe/infobulle » est portée par le titre
d’axe, le suffixe de graduation ou l’infobulle plutôt que par un badge.

