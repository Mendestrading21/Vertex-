# Arrêter de corriger un écran vide à la fois

Instrument : `tools/vertex_1_0/mesurer_surfaces_vides.py`
Gardien : `tests/test_vertex_1_0_surfaces_vides.py` (26 tests, 6 mutations)

---

## Pourquoi

Trois défauts de suite ont eu **exactement la même forme** — une donnée
existait, l'écran restait vide :

| chantier | ce qui était su | ce qui était montré |
| --- | --- | --- |
| hors séance | `last` sans `close` | rien (prix jeté) |
| échelle IBKR | le différé aurait répondu | rien (jamais demandé) |
| cotations | ACN à 198,0 dans le scan | `results: {}` |

Et les trois ont été trouvés **un par un, après signalement**. Corriger au
rythme des symptômes, c'est laisser le quatrième arriver.

## La mesure

Corpus dérivé de la **table de routage** (jamais d'une liste écrite à la main,
qui divergerait au premier ajout). Chaque surface est appelée, sa charge
classée. « Vide » ne veut pas dire HTTP 500 — ça se voit — mais **HTTP 200 avec
une charge sans aucune donnée exploitable**. La panne silencieuse : une carte
propre et creuse.

Un statut n'est pas un contenu : sans cette règle, `{'status': 'ok'}` passerait
pour une surface pleine et l'outil ne verrait plus jamais un écran creux. En
revanche un **zéro mesuré compte** — « zéro opportunité aujourd'hui » est une
réponse, pas un silence.

### Résultat sur la RC

```
surfaces servies : 92
PLEINE              85
VIDE_CACHE_RESEAU    5     (caches que le réseau remplit — bloqué ici)
ATTENDU_404          2     (échantillons délibérément inexistants)
VIDE_A_EXAMINER      0
ERREUR               0
```

**Aucun quatrième défaut.** Ce qui n'est pas une garantie : voir la limite.

## L'instrument s'est trompé trois fois en une heure

1. **Il appelait des routes à effet.** `/api/rescan`, `/api/live/refresh`,
   `/api/skyler/sweep` : il n'aurait pas mesuré, il aurait **agi** — relancé un
   scan, consommé du quota, faussé la mesure suivante. Le premier essai a
   expiré exactement pour ça.
2. **Il attendait la fin d'un flux SSE.** `/api/live/events` ne répond jamais
   « fini » : c'est sa nature. L'outil le classait « en erreur », accusant un
   endpoint qui fonctionne comme prévu.
3. **Il comptait ses propres échantillons comme des pannes.** Un 404 sur
   `decision_id=inexistant` est la bonne réponse. Trois lignes de bruit
   fabriqué, dans lesquelles une vraie anomalie se serait noyée.

Les trois corrections sont tenues par des mutations — dont une qui vérifie que
l'indulgence accordée aux échantillons **ne s'étend pas** à un vrai 404.

## La limite, et elle est décisive

Cinq surfaces dépendent d'un **cache que le réseau remplit** (noms
d'entreprises, fiches analystes, scan hebdomadaire). Le réseau de cet
environnement bloque tout hôte hors registres de paquets : ces caches **ne
peuvent pas** se remplir ici, et leur vide ne dit rien du produit.

Donc : ce balayage ne discrimine vraiment que **sur la machine de production**,
réseau ouvert et TWS branché.

```bash
python tools/vertex_1_0/mesurer_surfaces_vides.py
```

Toute ligne en `VIDE_A_EXAMINER` ou `ERREUR` y sera un vrai signal — et donnera
le chemin exact à remonter, au lieu d'un « il manque des graphiques ».
