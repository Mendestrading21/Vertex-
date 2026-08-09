# SKYLER LOT 398 — Les 2 tests skippés : morts depuis leur naissance

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-398` (base : lot 397 fusionné,
f0e8cf9)

Quatrième lot court. Point de contrôle **jamais examiné en 26 lots** : la suite
affiche `2862 passed / 2 skipped` depuis des dizaines de rapports. **Personne n'a
jamais regardé lesquels.**

## Ce que les 2 skips étaient

```text
tests/test_cross_page_consistency.py:26  « aucun symbole scanné dans cet environnement de test »
tests/test_cross_page_consistency.py:73  « board options vide »
```

Le fichier a été créé le **2026-07-12** (`fa234ca`) et **jamais modifié depuis**.
Les deux skips sont **structurels, pas environnementaux** :

- `/scan` sérialise `scan_state` tel quel ; `scan_state['rows']` est vide sous
  pytest parce qu'**aucun test de la suite ne déclenche de scan** — mesure :
  `test_cross_page_consistency.py` est le **seul** fichier des 300 à appeler
  `/scan`, et ses deux appels sont dans le test skippé.
- même mécanique pour `options_board`, qui alimente `/api/options/overview`.

Autrement dit : ces deux tests n'ont **jamais tourné une seule fois**. Ils ont été
écrits, commités, comptés dans la suite — et n'ont rien protégé pendant un mois.

## Ce qu'ils protégeaient réellement — mesuré, pas supposé

Avant de les réveiller, il fallait savoir s'ils valaient d'être réveillés. J'ai
exécuté leurs corps sur un `scan_state` alimenté, puis fauté la **production** :

```text
mutation (production)                                          T1        T2
pulse.py : filtre CALL → CALLS (dérive de la duplication)      —         MORD
terminal.py /api/ticker : sert un prix autre que le detail     MORD (A)  —
terminal.py /scan : transforme rows sans transformer detail    MORD (B)  —
[témoin] docstring de pulse.py reformulée                      muet      muet
```

Les trois fautes sont réelles et distinctes :

1. Le filtre `type == 'CALL'` est écrit **deux fois** — `vertex/options/overview.py`
   L42 et `vertex/options/pulse.py` L34 — sur le même board. C'est exactement la
   dérive que T2 verrouille.
2. `/api/ticker` sert `scan_state['detail'][sym]` ; rien d'autre n'interdit qu'il
   aille chercher un prix ailleurs un jour.
3. `/scan` sérialise `rows` et `detail` ensemble ; rien d'autre n'interdit qu'une
   route en recalcule un sans l'autre.

Chaque mutation a été rejouée **dans l'environnement pytest réel**, sur le fichier
de test final, pas seulement dans la sonde — et la production a été restaurée à
l'octet (`git status` vide entre chaque).

## La réparation

`tests/test_cross_page_consistency.py` : une fixture `scanned` alimente
`scan_state` **en place** puis restaure dans un `finally` (convention de
`test_options_intelligence_lot6.py`, leçon du lot 387). Les `pytest.skip`
conditionnels deviennent des **assertions** : si l'entrée manque, c'est un échec,
plus un silence.

Deux effets de bord ont été neutralisés dans T1 par `monkeypatch` :
`options_pack` (chaîne d'options yfinance → **sortie réseau**) et `_company.get`
(→ **écriture de `company_cache.json` depuis la suite**). Ni l'un ni l'autre ne
participe à l'invariant testé ; les laisser aurait introduit un test lent,
flaky et écrivain — le défaut même que le lot 389 a fermé.

Le prix injecté n'est pas une donnée affichée : c'est l'**entrée** d'un test, et
`scan_state` est restauré. Les routes, elles, sont les vraies.

## Ce que ça change

```text
avant   2862 passed · 2 skipped   (2 tests morts depuis 2026-07-12)
après   2864 passed · 0 skipped
```

**La suite n'a plus un seul test skippé.** Deux assertions de cohérence
cross-page — le prix d'une entité, les compteurs d'options — sont désormais
réellement imposées.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — la seule modification est
  `tests/test_cross_page_consistency.py`. Pas de preuve MD5 requise, pas de bump.
- Snapshot des 22 fichiers runtime (21 `*.json` + `.vertex_secret`) avec contrôle
  d'apparition. La passe a horodaté `desk_data.json` / `ai_enrichment.json` /
  `weekly_snapshot.json` (**contenu identique, seul le `ts` bouge** — le `finally`
  du lot 387 fait son travail) ; restaurés depuis le snapshot. Écart final
  **aucun**, aucun fichier apparu.
- Suite : **2864 passed / 0 skipped**. SW : `td-shell-v187`.

## Portée

Ce lot ne dit rien des 300 fichiers de test au-delà de celui-ci : il traite les
**deux** cas que la suite signalait elle-même à chaque exécution. Et « MORD »
signifie « attrape CETTE faute-là ».

Une limite assumée : T1 tourne sur une entrée injectée. Il prouve que les
**routes** ne déforment pas ce que le scan a produit ; il ne prouve pas que le
scan produise des prix justes — ce n'est pas son objet.

## Où en est la boucle

Quatre lots courts, quatre points de contrôle distincts : pistes fines (395),
octets servis (396), registre (397), tests inertes (398). Celui-ci est le premier
des quatre à avoir trouvé **du code mort plutôt qu'une documentation périmée**.

La matière utile reste **décisionnelle** — purge des 7 points MSFT (388) et scan
de démo dans `breadth_history` (391).

Prochaine échéance : **bilan n°9 au lot 400**.
