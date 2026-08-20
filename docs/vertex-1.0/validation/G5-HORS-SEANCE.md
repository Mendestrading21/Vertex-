# « Comme si sur IBKR on n'avait rien trouvé »

Signalé en conditions réelles, TWS branché : beaucoup de graphiques vides.
Gardien : `tests/test_vertex_1_0_hors_seance.py` (15 tests, 6 mutations)

---

## La première chose mesurée : l'heure

**02:50 à New York. Le marché est fermé.**

Ce n'est pas une excuse, c'est le point de départ : un terminal d'analyse doit
rester utile hors séance. Ce qu'il ne doit pas faire, c'est se vider en silence.

## Défaut 1 — `reqMarketDataType(1)` ne bascule pas tout seul

Deux commentaires du produit l'affirmaient :

```python
ib.reqMarketDataType(1)   # 1 = temps réel (bascule auto en différé si pas d'abonnement)
ib.reqMarketDataType(1)   # temps réel (repli auto différé si besoin)
```

**C'est faux.** Le type 1 demande du temps réel et ne rend rien d'autre. Marché
fermé ou abonnement absent → aucun tick, donc aucun cours, donc des écrans
vides. Un commentaire faux est pire qu'aucun : il dissuade d'aller vérifier.

Et le produit *savait déjà* : le chemin options retente les cotations manquantes
en **type 2** (clôture figée) puis restaure le type 1. Les deux autres flux — les
cotations de la watchlist et les indices — ne le savaient pas.

C'est la même famille que les cinq ordres de ports corrigés la veille : **trois
chemins font la même chose de trois façons, et celui qui a raison n'a pas
contaminé les autres.**

## Défaut 2 — un prix RÉEL était jeté parce qu'un champ dérivé manquait

```python
if last and close:      # <- sinon RIEN n'est rangé
```

Hors séance, IBKR ne livre pas toujours la clôture. Un prix parfaitement réel
était alors **jeté** parce que la *variation* n'était pas calculable. C'est
l'inverse exact de la règle du produit : une donnée absente devient un `—`
honnête, elle ne fait pas disparaître ce qu'on sait par ailleurs.

Le worker des indices, lui, était tolérant (prix conservé, variation `None`). Un
troisième désaccord entre trois chemins.

## Défaut 3 — le repli vers la clôture figée ne suffisait pas

Mon premier correctif repliait de 1 vers 2. **Le type 2 exige toujours un
abonnement.** Il ne règle donc QUE le cas « marché fermé alors qu'on est
abonné » — et laisse entier le cas « pas d'abonnement », qui produit exactement
le même écran vide.

Les quatre situations réelles, et le seul type qui répond dans chacune :

| abonné | marché | type |
| --- | --- | --- |
| oui | ouvert | **1** temps réel |
| oui | fermé | **2** clôture figée |
| non | ouvert | **3** différé (~15 min) |
| non | fermé | **4** clôture différée |

D'où une **échelle unique** — `ibkr_link.type_suivant` — partagée par les trois
flux : rien reçu → on descend d'un cran ; arrivé en bas → on **remonte au temps
réel**, sans quoi un flux resterait coincé en différé après la réouverture.

Écrire trois fois la même escalade produit trois escalades différentes : c'est
déjà arrivé deux fois dans ce produit (les cinq ordres de ports, puis ce repli).
La règle est donc écrite une fois, et un gardien vérifie que **chaque flux y est
câblé** — pas qu'il contient telle constante.

Le rattrapage des options, lui, ne tentait que le type 2 : sans abonnement, la
chaîne restait vide **malgré** le rattrapage. Il parcourt désormais l'échelle
entière.

## Le correctif

- **`_store_ticker`** conserve le prix dès qu'il existe (`last`, sinon
  `marketPrice()`, sinon `close`), avec `change: None` quand la clôture manque —
  inconnue avouée, jamais inventée. Il rend désormais `(stocke, temps_reel)` :
  c'est ce `stocke` qui déclenche le repli.
- **Cotations** : deux cycles entiers sans un seul cours → descente d'un cran
  sur l'échelle, et **retour au temps réel toutes les 15 minutes** pour ne pas
  mentir à l'ouverture.
- **Indices** : même règle, même échelle, réversible.
- **Options** : rattrapage sur l'échelle entière au lieu du seul type 2.
- Les deux commentaires mensongers sont supprimés.

**Rien n'est inventé.** La clôture figée est une donnée vraie, simplement datée
d'hier — et le système de fraîcheur le dit déjà (`marketDataType != 1` ⇒ la puce
ne peut plus afficher « Live »).

## Une faute à moi, refusée par deux gardiens

Mon premier correctif ajoutait **deux `except: pass`** autour de la bascule des
indices. `test_pass_terminal_lot386` et `test_replis_racine_lot385` l'ont refusé
(« 40 recensés, borne 38 — examiner les nouveaux cas avant de relever la
borne »). Ils avaient raison, et pas seulement formellement : avaler l'échec
d'une bascule rendait muette **la seule explication d'un bandeau vide** — le
défaut même que ce chantier corrige. L'échec est désormais écrit dans
`_IDX_META['err_mdt']`.

## Et une faute de gardien, à moi aussi

Ma première version du gardien cherchait le littéral `reqMarketDataType(2)`.
Elle a échoué **quand le code s'est amélioré** (`cible = 2 if recus == 0 else
1`), en signalant un défaut qui n'existait pas. Un gardien qui n'accepte qu'une
écriture interdit de réécrire, et pousse à contourner plutôt qu'à corriger.
Réécrit en contrôle de **comportement**… puis réécrit **une seconde fois**,
pour la même raison : quand l'escalade est passée d'un `if` bricolé à la règle
partagée, le contrôle « peut-il demander le type 2 » a de nouveau signalé un
défaut inexistant. Il vérifie désormais le **câblage** — le worker passe-t-il à
`reqMarketDataType` un résultat de `type_suivant` — en suivant les alias
**jusqu'au point fixe**, parce que le code écrit `suivant = type_suivant(...)`
puis `mdt = suivant`. Ne suivre qu'un saut manquait la cible : exactement le
piège que `self._ib = ib` avait déjà tendu à l'outil de surface IBKR.

## Vérification

- `compileall` → 0 · suite complète → **3 506 passed**
- 11 mutations, 11 détectées : exiger `last` ET `close` à nouveau · inventer
  `change = 0` · retirer le repli · réintroduire le commentaire mensonger ·
  repositionner le compteur de bascule à chaque cycle · rendre un `nan`
  exploitable · arrêter l'échelle à la clôture figée (différé inatteignable) ·
  empêcher la remontée au temps réel · faire descendre malgré une donnée reçue ·
  redonner au worker sa propre règle · ramener le rattrapage options au seul
  type 2.

## Ce que cela ne prouve pas

Que c'était **la** cause de tes écrans vides. C'est une cause réelle, mesurée
dans le code, et cohérente avec l'heure. Il peut y en avoir d'autres —
abonnements de données manquants, symboles non qualifiés, collisions de session.
Seul `tools/vertex_1_0/mesurer_g5_live.py`, lancé **sur ta machine avec TWS
ouvert**, tranchera : il sépare « pas d'abonnement » de « marché fermé » de
« ma sonde est en faute ».
