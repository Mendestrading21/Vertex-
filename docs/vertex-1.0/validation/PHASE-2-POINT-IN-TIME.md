# Phase 2 — fondation point-in-time : le socle, et ce qu'il ne fait pas encore

Lot `agent/vertex-1-0-point-in-time`, empilé sur le lot 2 (`4f55faeb`).

## Le défaut que ce lot rend impossible

L'audit du 24 août le nomme sans détour : *« un score historique peut
bénéficier d'informations futures »*. Les fondamentaux venaient de
`yfinance.Ticker.info`, qui rend la valeur **actuelle** — révisions comprises —
sans jamais dire à quelle date elle est devenue connaissable.

Rétrotester là-dessus ne mesure pas une méthode : cela mesure une clairvoyance.

## Trois instants, jamais confondus

| champ | ce qu'il désigne |
|---|---|
| `observed_at` | l'instant que la donnée **décrit** (fin de trimestre) |
| `available_at` | l'instant où elle est devenue **connaissable** (publication) |
| `received_at` | l'instant où Vertex l'a **reçue** |

`savoir_a()` filtre sur `available_at`. Un trimestre clos le 30 septembre et
publié le 25 octobre **n'existe pas** pour Vertex le 1er octobre.

Filtrer sur `observed_at` — l'erreur naturelle, celle qu'on écrit sans y
penser — le rendrait visible. C'est pourquoi le registre le refuse par
construction plutôt que de le déconseiller en commentaire.

## L'identité : un ticker n'en est pas une

`FB` est devenu `META` sans changer de société ; et un ticker rendu à la
corbeille peut être réattribué à une autre entreprise des années plus tard.
Bâtir une série sur le ticker mélange deux sociétés dans la même courbe —
silencieusement, et d'autant plus dangereusement que le graphique reste joli.

Ordre d'autorité : **conId IBKR** (stable chez le courtier qui calcule le P&L)
→ **CIK SEC** (stable chez l'émetteur) → **ticker + place + devise**, utilisable
mais `fragile`, et l'objet le **dit**. Un appelant peut refuser une clé fragile
pour une preuve historique ; il ne peut pas le décider s'il l'ignore.

La devise entre dans la clé : la même société cotée en USD et en EUR n'a pas la
même série de prix, et les confondre produirait des rendements qui ne sont que
du change.

## Quatre refus, et pourquoi chacun protège

| Refus | Ce qu'il empêche |
|---|---|
| instant **sans fuseau** | « 20:05 » désigne vingt-six instants ; supposer UTC décale les publications d'une demi-journée et inverse l'ordre de deux dépêches |
| `available_at` **avant** `observed_at` | connaître un résultat avant la fin de la période qu'il décrit n'est pas une donnée, c'est une erreur d'ingestion qui contaminerait tous les backtests en aval |
| `remplacer()` | append-only n'est pas une convention de nommage ; une correction s'écrit en **révision**, qui laisse l'original interrogeable |
| version de schéma **future** | lire un format non compris ne produit pas une erreur mais une donnée *fausse présentée comme sûre* |

## Ce qui est enregistré, jamais recalculé

Un **split** est une observation portant son facteur, à sa date de
disponibilité. L'ajustement se calcule à la lecture et reste explicable.
Réécrire les prix passés effacerait ce que Vertex a réellement vu — et un
registre qui réécrit son passé ne sert plus à expliquer une décision.

Un **changement de ticker** ne coupe pas la série : la clé repose sur le conId.

## Mesures

```
tests du lot          29 passed, 1 skipped
couverture            instruments 97 % · point_in_time 95 % · schemas 100 %
suite complète        3 651 passed, 7 skipped, 0 failed
tests/test_no_orders  3 passed
compileall            PASS
```

Le skip est honnête et documenté : aucune migration n'existe à la version 1,
parce qu'il n'existe aucun format antérieur. Le test le dit plutôt que de
prétendre avoir vérifié un aller-retour inexistant.

## Ce que ce lot ne fait PAS

- **aucun producteur n'écrit encore dans le registre.** C'est un socle, pas une
  ingestion : SEC, FRED, BLS et CFTC sont les lots suivants, et les brancher
  ici aurait mélangé deux phases ;
- **aucun moteur ne le lit encore.** Le remplacement de `yfinance.Ticker.info`
  dans le domaine fondamental est un chantier à part, avec son propre
  adaptateur et son propre rollback ;
- **`contracts.py` et `entitlements.py`** — les deux autres composants de la
  phase 2 — restent à faire. Ce sont des protocoles de provider ; ils ont leur
  sens quand un premier provider écrit vraiment ;
- **le format est JSON Lines sur disque.** Suffisant pour la volumétrie
  actuelle et lisible à l'œil, ce qui compte plus qu'on ne croit : un registre
  qu'on ne peut pas inspecter devient un registre qu'on croit sur parole. Une
  bascule vers un stockage colonne se fera derrière la même interface, et la
  migration de schéma existe pour cela.

## Rollback

Entièrement additif : deux paquets neufs (`vertex/domain`, `vertex/storage`),
un banc neuf, aucun fichier existant modifié. `git revert` du commit suffit, et
rien du produit actuel n'en dépend encore — c'est précisément ce qui rend ce
socle sûr à poser avant ses consommateurs.
