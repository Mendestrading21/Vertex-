# SIGNAL OS · LOT 24 — MOBILE ET SÉMANTIQUE

Branche : `agent/vertex-signal-os-v1` · SW v229 → **v230** · Suite **3133 passed**

Deux angles que les audits précédents ne couvraient pas.

---

## 1. Ce qui manquait aux lots 22-23 : ils ne mesuraient qu'à 1440

| relevé à 390 px | résultat |
| --- | --- |
| texte sous AA | **0** sur 2 274 éléments |
| non textuel sous 3:1 | **1 famille** |

La famille : les **lignes de tableau cliquables en mode cartes**
(`role="button"`, `tabindex`, `aria-label`), dont la carte **est** la limite, à
**1,20:1**.

> Un défaut ne se voit que dans la forme où il existe. À 1440, ces lignes sont
> des lignes de tableau et non des cartes : il n'y avait rien à trouver.

Les lignes **non** cliquables gardent leur bordure discrète — elles
n'identifient aucun contrôle.

---

## 2. L'audit de sémantique, jamais fait, et le produit est propre

Sur les 35 vues :

| contrôle | résultat |
| --- | --- |
| contrôles sans nom accessible | **0** |
| tableaux sans `<th>` | **0** |
| images sans `alt` | **0** |
| sauts de niveau de titre | **1 famille** (5 vues) |
| SVG sans nom ni masquage | **1** |

Deux défauts réels sur cinq contrôles. C'est un bon résultat, et il vaut d'être
dit comme tel plutôt que noyé.

### Défaut 1 — l'ossature de titres de Marchés sautait de h1 à h3

Sur les **cinq** vues. Cause exacte, mesurée : les titres de cartes de tête sont
des `<span>` — donc **aucun** titre de niveau 2 n'existait — et le `h3` venait du
Chart Shell.

Ma première correction (promouvoir les titres de cartes en `h2`) n'a réparé que
**deux** vues sur cinq. Mesure au navigateur ensuite : sur `macro`, `sectors` et
`breadth`, c'est un **graphique** qui ouvre la vue, donc son `h3` précède tout
`h2` situé plus bas.

D'où `titleLevel` sur le Chart Shell : quand un graphique **ouvre** une vue, son
titre **est** le titre de section. Le défaut reste `h3` — un graphique est le
plus souvent une sous-section, et tout passer en `h2` n'aurait fait que déplacer
le saut. L'option **ne change rien au rendu** : le style vient de la classe.

Un cinquième cas est apparu une fois Marchés réparé : `/opportunities?radar`,
même mécanisme, même correctif.

### Défaut 2 — la racine du treemap d'allocation était muette

Chaque tuile porte déjà `role="img"` et son libellé, mais on entrait dans un
graphique **anonyme** avant de les rencontrer.

Nommée en **`role="group"`** — et non `img`, qui aurait rendu le sous-arbre
opaque et fait **perdre le détail par tuile**. Le résumé est dérivé des données
tracées : nombre de postes, dominant et sa part.

---

## 3. Quatrième fois qu'une portée d'instrument me fait crier au loup

L'instrument accusait la jauge de Système. Or `chart-core.js` la nomme déjà sur
son conteneur avec `role="img"` — ce qui rend le sous-arbre **opaque** pour un
lecteur d'écran : le graphique est annoncé comme une image nommée, ses entrailles
ne sont pas exposées.

L'instrument ne regardait que l'élément lui-même. Corrigé, le relevé est passé de
3 familles à 2 — et le troisième « défaut » n'en était pas un.

---

## 4. Mesures — serveur `td-shell-v230` vérifié avant lecture

| relevé | avant | après |
| --- | --- | --- |
| défauts de sémantique (35 vues) | 6 occurrences / 2 familles | **0** |
| non textuel à 390 px | 3 occurrences / 1 famille | **0** |
| non textuel à 1440 px (non-régression lot 23) | 0 | **0** |
| texte à 390 px | 0 | **0** |

Ossature de titres après correction :

| vue | avant | après |
| --- | --- | --- |
| markets/overview | h1 → h3 | h1 → h2 → h3 |
| markets/macro | h1 → h3 | h1 → h2 |
| markets/sectors | h1 → h3 | h1 → h2 → h2 → h3 |
| markets/breadth | h1 → h3 | h1 → h2 → h2 |
| markets/volatility | h1 → h3 | h1 → h2 |
| opportunities/radar | h1 → h3 | h1 → h2 |

---

## 5. Gardien — `tests/test_signal_os_semantique_lot24.py` (6 tests, 8 mutations sur 8 tuées)

| mutation | résultat |
| --- | --- |
| `titleLevel` retiré du Chart Shell | 1 échec |
| graphique macro sans niveau 2 | 1 échec |
| radar sans niveau 2 | 1 échec |
| titre de tête redevenu `<span>` | 1 échec |
| racine du treemap redevenue anonyme | 1 échec |
| résumé du treemap non dérivé | 1 échec |
| ligne cliquable sans contour | 1 échec |
| jauge sans nom sur son conteneur | 1 échec |

Le quatrième test est un **contre-exemple** : il aurait suffi de poser
`titleLevel` partout et de laisser les cartes en `<span>`. Or sur `overview` et
`volatility`, c'est une **carte** qui ouvre la vue — son titre doit donc être un
vrai titre. Les deux corrections sont nécessaires, aucune ne remplace l'autre.

---

## 6. Réserve honnête

L'audit de sémantique couvre cinq contrôles automatisables (nom accessible,
en-têtes de tableau, ossature des titres, `alt`, nommage des graphiques). Il ne
dit rien de la **qualité** des libellés, de l'ordre de lecture réel, ni du
comportement d'un vrai lecteur d'écran — ces trois-là demandent un test humain
que cet environnement ne permet pas.
