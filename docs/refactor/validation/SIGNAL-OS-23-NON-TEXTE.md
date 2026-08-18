# SIGNAL OS · LOT 23 — LE CONTRASTE NON TEXTUEL

Branche : `agent/vertex-signal-os-v1` · SW v228 → **v229** · Suite **3122 passed**

Suite du lot 22, côté **non textuel**. WCAG 1.4.11 demande 3:1 pour ce qui
permet d'identifier un composant **et son état**.

---

## 1. Deux résultats, dont un vide

### Rien côté graphiques

| série | ratio sur le fond de graphique |
| --- | --- |
| `#9B7BFF` (marque) | 5,76 |
| `#45D6E8` (technique) | 10,39 |
| `#c8bfae` (sable) | 9,94 |
| `#D9BE3C` (ambre) | 9,82 |
| `#8A8284` (acier) | 4,84 |

Les couleurs sémantiques passent aussi (positif 7,66 · négatif 5,12 · neutre
9,34), et **zéro trait SVG** sous le seuil sur les 35 vues.

Un résultat vide ne vaut que si l'instrument pouvait échouer. Celui-ci a échoué
ailleurs sur la même exécution — donc il mesurait bien.

### Un défaut systémique côté contrôles

**56 boutons, chips, champs et selects sur 14 familles : 1,15 à 1,24:1.**

---

## 2. Le constat honnête sur la cause

Ce n'est **pas** « quelqu'un a cassé une valeur ». **Aucun** jeton de bordure du
produit n'atteint 3:1 :

| jeton | sur le canevas |
| --- | --- |
| `--vx-border-soft` (Signal OS) | 1,15 |
| `--vx-border-soft` (tokens) | 1,46 |
| `--vx-border-default` | 1,68 |
| `--vx-border-strong` | **2,51** |

C'est un parti pris cohérent des deux couches. La correction est donc **scopée
aux contrôles** : les bordures décoratives gardent leur discrétion, parce que la
règle porte sur ce qui **identifie un composant**, pas sur tout trait.

`primary`, `ghost` et `link` restent **exclus** — ils n'ont pas de bordure par
choix et sont identifiés par leur fond (dégradé plein) ou par leur nature de
lien. Leur en donner une aurait inventé un défaut en corrigeant l'autre.

Deux jetons, deux valeurs, réversibles d'une ligne :
`--vx-border-control` (blanc .35) et `--vx-border-control-brand` (violet .75).

> Précédent interne qui rend la valeur défendable : `.vx-input:focus` employait
> déjà `rgba(255,255,255,.42)`. Ce poids était donc déjà admis sur un contrôle.

---

## 3. Trois fois le même piège, et je ne l'ai vu qu'à la troisième

L'instrument ne regardait **qu'un seul canal** à la fois.

| # | ce qu'il ignorait | conséquence |
| --- | --- | --- |
| 1 | le fond, dès qu'une bordure existait | accusait des composants dont le fond portait la limite |
| 2 | la cascade réelle | ma correction n'agissait pas |
| 3 | l'anneau `box-shadow` | déclarait en échec un contrôle **déjà corrigé** |

Le deuxième mérite d'être détaillé : ma première correction empilait un override
de spécificité **inférieure**. Elle n'a rien changé pour les champs ni les
chips ; seuls les boutons passaient, parce que leur chaîne de `:not()` les
faisait gagner. J'ai fini par **demander au moteur** la liste des règles qui
s'appliquent, au lieu de raisonner sur l'ordre des feuilles — et la gagnante
était une règle scopée que je n'avais pas lue.

Le troisième est le plus dangereux : sans ce canal, l'instrument m'aurait poussé
à **sur-corriger un défaut déjà résolu**.

---

## 4. L'état sélectionné, mesuré plutôt que supposé

Le segment pressé ne se distinguait que par un fond violet à `.12` — **1,17:1**.

Son libellé change bien de couleur (`#F5F3F0` contre `#989092`), mais cet écart
vaut **2,81:1** : il porte *presque* l'état, pas tout à fait. Et l'assombrir
davantage aurait cassé sa propre lisibilité, mesurée au lot 22.

D'où un **anneau interne** plutôt qu'un fond saturé : il franchit le seuil des
deux côtés (**3,72** contre le fond du groupe, **3,17** contre le fond du
segment) sans décaler la mise en page.

---

## 5. Trouvé en chemin, et c'est moi qui l'avais causé

Deux `C.colors.series[i % 6]` sur un tableau de **cinq** entrées, hérités du
retrait d'`OPTION` de la série que j'ai fait moi-même plus tôt dans cette
refonte.

**Latents** : aucun graphique n'atteint six séries, et les trois overlays du
graphique principal portent tous une couleur explicite. Mais `series[5]` vaut
`undefined` — donc le jour où une sixième série apparaît, la couleur sort de la
palette **sans erreur**. Corrigés en `C.colors.series.length`.

---

## 6. Mesures — serveur `td-shell-v229` vérifié avant lecture

| relevé | avant | après |
| --- | --- | --- |
| objets non textuels sous 3:1 | **56** | **0** |
| familles distinctes | **14** | **0** |
| texte sous AA (non-régression lot 22) | 0 | **0** |

---

## 7. Gardien — `tests/test_signal_os_non_texte_lot23.py` (6 tests, 8 mutations sur 8 tuées)

| mutation | résultat |
| --- | --- |
| limite des contrôles remise à l'origine | 1 échec |
| limite de marque affaiblie | 1 échec |
| champs revenus à `--vx-border-soft` | 1 échec |
| chips revenus à `--vx-border-soft` | 1 échec |
| anneau du segment retiré | 1 échec |
| longueur figée revenue (chart-core) | 1 échec |
| longueur figée revenue (price-chart) | 1 échec |
| une série assombrie sous 3:1 | 1 échec |

La huitième a d'abord **survécu** : ma mutation visait `'#8A8284'`, dont la
première occurrence du fichier est le jeton `copper`, pas la série. Rejouée sur
le tableau `series`, elle tombe. Une mutation qui ne touche pas sa cible ne
prouve rien — et ressemble exactement à un gardien qui marche.

---

## 8. Ce que ce lot change à l'œil

À dire franchement : les contours des boutons, chips et champs deviennent
**nettement plus visibles** qu'avant (facteur ~4,6 sur l'alpha), et le segment
sélectionné porte désormais un anneau violet. C'est un changement esthétique
assumé, pas seulement un correctif invisible — et il se défait en remettant deux
valeurs de jeton.
