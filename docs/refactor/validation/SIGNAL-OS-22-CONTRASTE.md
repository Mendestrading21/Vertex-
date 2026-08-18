# SIGNAL OS · LOT 22 — LE CONTRASTE RÉEL, ET LE FOCUS CLAVIER

Branche : `agent/vertex-signal-os-v1` · SW v227 → **v228** · Suite **3116 passed**

Deux audits que la refonte n'avait jamais faits. Le premier a trouvé trois
défauts ; le second n'a rien trouvé — et ça se dit aussi.

---

## 1. L'instrument, d'abord — parce que c'est lui qui rend le défaut visible

Le ratio se calcule contre le fond **effectif**, obtenu en remontant les
ancêtres et en composant les couches semi-transparentes.

Lire le `backgroundColor` de l'élément lui-même rend `rgba(0,0,0,0)` sur la
quasi-totalité du produit — donc un ratio calculé contre du vide. C'est
exactement ce qui rend ce défaut invisible à l'inspection ordinaire : l'outil
naïf ne le voit pas, et l'œil ne mesure pas.

Les vues sont **dérivées de la source** (leçon du lot 14), et les points
d'entrée interdits sont avortés au navigateur (leçon du lot 20).

**2 309 éléments de texte, 35 vues, 3 familles en échec.**

---

## 2. Un seul mécanisme derrière les trois défauts

> Une teinte sémantique **éclaircit** le fond ; le texte qui la traverse perd le
> contraste qu'il avait sur le fond nominal.

### Le négatif comme texte sur sa propre teinte

| fond | `--vx-negative` (#E9555F) |
| --- | --- |
| canevas | 5,69 |
| carte (`--vx-surface`) | 5,30 |
| carte élevée | 5,12 |
| **`--vx-negative-soft`** | **4,39 / 4,20** |

Vérification faite sur **toute la famille** plutôt que sur le seul cas qui a
échoué : l'avertissement rend **7,28** et le positif **6,02** sur leur propre
teinte. Le négatif est **le seul** des trois dans ce cas.

**La correction évidente aurait été fausse.** Éclaircir `--vx-negative` fait
passer le test — et repeint chaque chiffre de perte du produit, là où ce jeton
rend déjà 5,12 à 5,69:1. Le défaut n'existe que sur une surface teintée : c'est
donc un jeton dédié, `--vx-negative-text` (#EF737B), qui le corrige là où il se
produit.

### Le texte assourdi dans un insight

| teinte | `--vx-text-muted` | avec `--vx-text-secondary` |
| --- | --- | --- |
| cyan (insight par défaut) | **4,26** | 7,53 |
| avertissement (`data-tone="risk"`) | **4,11** | 7,26 |
| violet (`data-tone="ai"`) | 4,66 | 8,23 |

L'audit n'avait signalé que la teinte **avertissement** — non pas parce que les
autres tenaient, mais parce qu'aucune vue visitée ne rendait de texte assourdi
dessus. Le calcul les a toutes examinées : deux sur trois échouent, la troisième
a moins de 0,2 de marge. La règle couvre donc les trois.

Elle reste **scopée aux insights** : sur les surfaces nominales,
`--vx-text-muted` passe. Relever le jeton global aurait aplati la hiérarchie
typographique de tout le produit pour un défaut qui n'apparaît que sur une
teinte.

---

## 3. Le focus clavier — mesuré, rien trouvé

**109 familles** d'éléments atteintes au `Tab` sur les 8 espaces : **toutes**
portent un indicateur de focus visible.

Le point de méthode : l'état focalisé est comparé au **même sélecteur non
focalisé**. Sans cette référence, une carte portant déjà une ombre passerait
pour « focus visible » alors que rien ne change à l'écran — l'instrument aurait
validé un défaut au lieu de le trouver.

Un résultat vide n'est utile que si l'instrument pouvait échouer.

---

## 4. Mesures — serveur `td-shell-v228` vérifié avant lecture

| relevé | avant | après |
| --- | --- | --- |
| éléments de texte mesurés | 2 309 | 2 309 |
| familles sous le seuil AA | **3** | **0** |
| familles focusables sans indicateur | 0 | 0 |

---

## 5. Gardien — `tests/test_signal_os_contraste_lot22.py` (5 tests, 7 mutations sur 7 tuées)

Il **recalcule** le ratio depuis `tokens.css` — composition de la teinte sur les
deux surfaces réelles, elles-mêmes dérivées des jetons. Épingler
`color:var(--vx-negative-text)` n'aurait rien prouvé : le jeton pourrait valoir
n'importe quoi.

| mutation | résultat |
| --- | --- |
| jeton de texte redirigé vers la base | 1 échec |
| jeton de texte remis à la valeur d'origine | 1 échec |
| `--vx-negative` éclairci (la « correction évidente ») | 1 échec |
| bannière revenue au jeton de base | 1 échec |
| règle d'insight retirée | 1 échec |
| insight remis au texte assourdi | 1 échec |
| `--vx-text-muted` assombri globalement | 1 échec |

Le troisième test est le plus utile : il documente **pourquoi** la correction
intuitive est mauvaise, au moment précis où quelqu'un sera tenté de l'appliquer.

---

## 6. Réserve honnête

La règle du texte discret sur teinte est scopée aux `.vx-insight` et à la
bannière d'erreur — les deux surfaces teintées que l'audit a rencontrées. Une
future surface teintée portant du texte assourdi ne serait couverte ni par la
règle ni par le gardien ; c'est l'audit au navigateur qui la trouverait, pas la
suite.
