# SKYLER LOT 395 — Rien à faire, vérifié

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-395` (base : lot 394 fusionné,
a295dce)

**Aucun code. Aucun gardien. Aucun test ajouté.** C'est le résultat, pas un
défaut d'exécution.

## Pourquoi ce lot est court

Le lot 393 a constaté l'épuisement des pistes fines ; le 394 l'a confirmé en
allant vérifier ailleurs. Toutes les veines sont closes **par la mesure** :

| veine | close au | ce qu'elle a donné |
|-------|----------|--------------------|
| audit des gardiens par mutation | 384 | 27 mutations, 2 trouvailles (381, 382) |
| écritures runtime par la suite | 389 | 2 trouvailles (387, 388) |
| refus API, dicts littéraux | 377 | 39 refus, 39 motivés |
| refus API, construits en variable | 392 | 30 routes, 12 refus, 0 muet |
| promesses de retour littérales | 375 | 6 fonctions, 0 promesse fausse |
| promesses de retour imbriquées | 393 | 2 fonctions, 0 promesse fausse |
| rejeu des gardiens anciens | 394 | 7/8 mordent ; l'écart était une docstring |

Un gardien de plus ici serait le changement gratuit que la boucle s'interdit
depuis le lot 384.

## Mais un constat se vérifie, il ne se répète pas

Reprendre la liste des pistes restantes sans la contrôler serait exactement la
faute que cette tranche a commise huit fois : **faire confiance à ce qu'on
transporte**. Les deux items restants ont donc été re-mesurés.

**Le commentaire périmé de `vx-entities.js` — toujours là, toujours faux.**

```text
vertex/static/vertex/js/vx-entities.js:18
  /* Clés synchronisées — MIROIR EXACT de __DESK_KEYS (terminal.py) + vxWatchlist. */
```

`__DESK_KEYS` n'existe plus dans `terminal.py` depuis la purge É1 (établi aux
lots 381 et 384). L'énoncé est faux, dans un fichier **servi**.

**Les sites de concaténation à constantes (374) — décompte conforme.** Quatre
appels `_extract(PAGE_DAILY, …)` dans `terminal.py`, ce qui correspond aux
« 4 points de concaténation » mesurés au lot 374, dont trois « à constantes ».
Aucune dérive entre ce que la boucle transporte et ce que le dépôt contient.

## Une asymétrie qu'il faut assumer, pas cacher

Le lot 394 vient de corriger une docstring fausse dans un fichier de test. Le
commentaire de `vx-entities.js` est **le même genre de défaut** — un énoncé faux
qu'un lecteur croira — et il reste différé. Est-ce cohérent ?

Oui, et la raison n'est pas le coût d'édition mais **l'invalidation de cache** :
`vx-entities.js` est servi, donc le corriger impose un bump de service worker
(règle n°3), la mise à jour de `_EMPREINTE`, et purge la copie hors-ligne de
l'utilisateur. Une docstring de test ne coûte rien ; un octet servi coûte le
cache de tout le monde. **Pour un commentaire, c'est disproportionné** — et
c'est une décision à prendre, pas un effet de bord de lot.

La règle qui en sort : *un énoncé faux se corrige immédiatement là où c'est
gratuit, et se verse aux dossiers là où cela coûte au produit.*

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- Arbre propre, **aucun fichier touché** — ni production, ni test.
- Snapshot des 21 fichiers runtime, contrôle d'apparition inclus ; écart final :
  **aucun**.
- Suite : **2862 passed / 2 skipped**, inchangée. SW : `td-shell-v187`.

## Où est la matière utile

Elle n'est pas technique, elle est **décisionnelle**. Les dossiers du rang 1
attendent, dont deux chiffrés et sans risque :

1. **Purge des 7 points MSFT fabriqués** dans `gex_history_cache.json` (388) —
   coût quasi nul, risque nul, et la seule ligne où un chiffre inventé est
   aujourd'hui servi comme une mesure.
2. **Le scan de démo écrivant dans `breadth_history.json`** (391) — 16 points
   identiques, servis sur `/markets` comme « historique breadth RÉEL » ; trois
   issues défendables, aucune que l'agent puisse trancher seul.

Puis `context()` sur univers vide (379) + « points réels du scan » (363), les
replis `0` (378), le badge de provenance IBKR (386), et le filet desk (362).

## Suite

Tant qu'aucun GO n'arrive, les lots suivants seront de cette nature : courts,
vérifiés, sans code. **Le dire est plus utile que de meubler.** Prochaine
échéance périodique : bilan n°9 **~lot 400**.
