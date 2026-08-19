# Audit des moteurs — ce qu'ils calculent sort-il ?

Instrument : `tools/vertex_1_0/mesurer_moteurs.py`
Gardien : `tests/test_vertex_1_0_moteurs.py` (7 tests, 3 mutations)
Mesure figée : `docs/vertex-1.0/inventory/moteurs.json`

---

## La question posée

La mission demande un audit des moteurs de décision **avant** d'en créer un
nouveau. La question naturelle — « que calcule chaque moteur ? » — n'est pas la
plus utile. Celle qui l'est :

> **ce que ce moteur calcule sort-il quelque part ?**

Le lot précédent a montré pourquoi. `track_record.evaluate()` tournait, ne
plantait pas, et rendait `resolved: 0` sur toutes les entrées : un moteur
parfaitement vivant dont le résultat était vide, **sous un test vert**. Un moteur
qu'aucune surface n'atteint est le cas dégénéré du même problème.

## Le résultat

```text
59 moteurs
54  SERVI      — importés directement par une surface servie
 4  INDIRECT   — atteints via un autre module servi
 1  INATTEINT  — aucun chemin d'import depuis une surface
 0  atteints mais sans aucun appel mesuré
```

**58 des 59 moteurs sont atteints ET appelés.** Le tableau est sain, et il faut
le dire aussi clairement que l'inverse : il n'y a pas de forêt de code mort dans
`vertex/engines/`.

## Le seul isolé : `performance_ledger`

124 lignes. Il implémente la séparation stricte
`SIGNAL → ALERT → RECOMMENDATION → USER_DECISION → SIMULATED_POSITION →
REAL_POSITION` — exactement la discipline que `PRODUCT_CONTRACT.md` demande pour
ne jamais confondre la performance théorique d'un signal avec la performance
réelle d'un portefeuille.

**Aucun chemin de production ne le lit.** Trois fichiers de tests l'importent, ce
qui suffit à lui donner l'air vivant dans une recherche naïve.

Il n'est **pas supprimé** ici. La mission interdit tout nettoyage destructif sans
preuve de non-usage : la preuve existe désormais, mais la suppression relève de
`CLEANUP_POLICY.md` (#782) **et d'une décision humaine**. Deux lectures sont
défendables, et ce n'est pas à moi de trancher :

- c'est une **intention non branchée** — la brancher servirait G3 (« la mémoire
  des résultats est exploitable ») mieux que `track_record` seul, qui mélange
  encore signal et résultat ;
- c'est un **doublon abandonné** — auquel cas il coûte de la lecture et de la
  maintenance pour rien.

Le gardien fige la liste : un second moteur isolé qui apparaîtrait ferait échouer
la suite, et une entrée qui cesserait d'être isolée devrait être retirée.

## Trois fois où l'instrument était faux avant le produit

Cet audit a demandé trois corrections **de la mesure**, aucune du code mesuré.

**1. Les surfaces étaient trop étroites.** La première version ne partait que de
`routes/` et `pages/`. Elle rendait `analysis` — 336 lignes, producteur des
séries de prix de tout le produit — « INATTEINT », avec huit autres. L'hypothèse
« surface servie = déclare une route » avait été invalidée par le chantier #779
**lui-même** : il a fait passer `terminal.py` de 14 routes à 0, et le monolithe a
cessé de déclarer des routes **sans cesser d'être servi** — il héberge les
boucles qui remplissent `scan_state`, l'état que toutes les routes servent.

Un instrument qui encode une hypothèse périmée mesure le passé.

**2. Les liaisons d'attribut étaient ignorées.** Le compteur d'appels ne voyait
que `X.f(...)`, pas `f = X.f` suivi de `f(...)` ailleurs. Cinq faux positifs,
dont `analysis` à nouveau (`analyse = _analysis.analyse`, `terminal.py:201`). Et
l'idiome en cause est précisément celui que j'ai généralisé en #779 pour les
façades (`_sync_ibkr_state = _ibkr_state.sync`).

**3. Le témoin négatif n'éprouvait rien.** Il vérifiait qu'un fichier fabriqué
n'existe pas sur disque — ce qui est vrai par construction. Il **injecte**
désormais un moteur que personne n'importe dans le graphe et vérifie qu'il
ressort isolé.

## Ce que cette mesure ne dit pas

Un chemin d'import prouve la **portée**, pas la **sortie**. Le compteur d'appels
s'en approche mais reste **borné par le bas** : un appel indirect (`getattr`,
fonction passée en argument, méthode stockée) n'est pas vu.

- `INATTEINT` est un fait **solide** : aucun chemin n'existe.
- `SERVI` est un fait **faible** : le module est atteint et appelé, ce qui ne
  garantit pas que son résultat arrive à l'écran.

Aller plus loin — suivre chaque valeur jusqu'à une réponse HTTP — demanderait
une analyse de flux que l'`import *` de `terminal.py` rend structurellement
incomplète. C'est une limite assumée, pas un oubli.

## Preuves

```text
compileall                     exit 0
pytest tests/ -q               3 347 passed        (3 340 avant le lot)
pytest tests/test_no_orders.py 3 passed
mutations                      3/3 mordent, contrôle vert
```

Les trois : surfaces réduites aux routes (l'erreur d'origine, qui isolait
`analysis`) · liaisons d'attribut de nouveau ignorées · graphe qui relie tout
(le témoin négatif doit alors rompre).

## Décision humaine en attente

**`performance_ledger` : brancher, ou retirer ?** La preuve de non-usage est
faite ; le choix ne l'est pas. À traiter en #782 avec `CLEANUP_POLICY.md`.
