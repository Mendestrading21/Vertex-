# SIGNAL OS · LOT 38 — ÉTAT DES LIEUX : CE QUE VERTEX GARDE, MESURÉ

Branche : `agent/vertex-signal-os-v1` · SW **v233** · Suite **3194 passed**
(conditions de la CI : Playwright rendu inimportable)

Sept lots (31→37) ont posé la même question à sept endroits : *un garde-fou
garde-t-il vraiment ce qu'il prétend garder ?* Ce document ne rajoute pas un
huitième instrument — il les fait tous parler d'une voix, avec leurs verdicts du
jour et leurs réserves.

---

## 1. Le tableau de bord

| invariant | instrument | verdict mesuré | témoin |
| --- | --- | --- | --- |
| **READONLY** — surface IBKR | `mesurer_surface_ibkr.py` | **22 capacités, toutes en lecture**, aucun nom calculé | témoin d'ordre (3 formes) |
| **Sorties de texte externe** | `mesurer_sorties_news.py` | **154 routes servies, 0 sert la charge** | témoin `/news-feed` neutralisé |
| **Dégradation honnête** (panne globale) | `mesurer_degradation.py` | 33 vues × 3 pannes : **0 fuite, 0 vue muette, 0 erreur** | — |
| **Panne partielle** | `mesurer_panne_partielle.py` | 10 sources : **0 chiffre, 0 tracé** en silence | 2 témoins (cellule + tracé) |
| **Intégrité des pages** | `mesurer_integrite_pages.py` | **0 id dupliqué, 0 débordement, 65 liens, 0 cassé** | — |

Tous ces chiffres viennent d'une exécution de ce jour, serveur de démonstration
à v233, et non d'une mémoire de lot précédent.

---

## 2. La règle que cette série a coûté cher à apprendre

**Un instrument doit reproduire l'état que le produit peut réellement
atteindre.** Sinon il mesure son propre montage — et il le fait avec autorité,
puisqu'il accuse.

Cinq fois, la même faute, sous cinq déguisements :

| lot | l'état fabriqué | ce que fait la production | ce que l'outil accusait |
| --- | --- | --- | --- |
| 35 | une référence prise 20 min plus tôt | — | 15 chiffres (horloges) |
| 35 | deux références à 2,4 s d'écart | — | 4 chiffres (horloges à la minute) |
| 36 | un bras avec cache, l'autre sans | les deux à conditions égales | 4 durées « non expliquées » |
| 37 | un témoin qui ne touche pas l'entrée des courbes | — | 0 tracé (détecteur aveugle) |
| 38 | `detail` empoisonné **brut** | `detail` rempli **assaini** (écrivain unique) | `/scan` |

Et son corollaire, payé deux fois : **un détecteur sans témoin rend un zéro qui
ne prouve rien.** Les deux outils qui concluent portent désormais leur témoin et
**refusent de conclure** s'il reste muet, avec un code de sortie distinct.

---

## 3. Le motif technique sous-jacent

Quatre des cinq erreurs sont la même : **comparer par le texte ce qu'il faut
comparer par la structure.**

| comparaison faite | ce qu'il fallait | conséquence |
| --- | --- | --- |
| `e.className` | chemin DOM | tout texte SVG dans un seul seau |
| découpe de source avant `def main(` | `ast.parse().body` | un import paresseux accusé |
| liste de noms interdits | énumération des capacités employées | angle mort sur tout nom non prévu |
| deux contextes de navigateur différents | mêmes conditions de cache | toute valeur vivante faussée |

---

## 4. Les réserves, toutes ouvertes et nommées

1. **Points hors limites non mesurés** — `/api/ticker/<sym>`, `/desc/…`,
   `/api/analyst/…` : exclus par consigne, leur cas est raisonné à la lecture du
   code, pas mesuré.
2. **Routes à plusieurs paramètres** écartées du balayage : on ne sait pas les
   remplir honnêtement.
3. **GET seul.** Une sortie POST qui renverrait du texte externe ne serait pas
   vue — écarté délibérément, l'invariant READONLY interdit de balayer des POST
   à l'aveugle.
4. **Une seule source en panne à la fois.** Deux sources simultanées sont un
   régime non mesuré.
5. **Contenu non visible** — tableau replié, infobulle — hors de portée de la
   sonde.
6. **Signature géométrique** = longueur de `d` + nombre de sommets. Une courbe
   dont les valeurs changeraient sans toucher ni l'une ni l'autre passerait.
7. **Analyse statique pour IBKR.** Un ordre par un chemin que l'AST ne relie pas
   à un objet `IB` n'est pas vu ; la défense de fond reste `readonly=True` côté
   serveur IBKR.
8. **`strip_markup` ne retire que les balises fermées.** Une balise jamais
   fermée traverse — assumé pour la famille échappée au rendu.
9. **Jeu de démonstration.** Certaines sources n'alimentent qu'une ou deux vues :
   leur panne a peu de surface pour mentir.

---

## 5. Ce que ce document n'est pas

Ce n'est pas un certificat. Chaque ligne du §1 est vraie **pour ce que
l'instrument sait voir**, et le §4 dit exactement où il ne voit pas. La valeur
de l'ensemble tient à ce que les deux soient écrits côte à côte.
