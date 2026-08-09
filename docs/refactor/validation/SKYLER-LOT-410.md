# SKYLER LOT 410 — BILAN n°10, tranche 400 → 409

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-410` (base : lot 409 fusionné,
bbd5f86)

Dix lots. Bilan fait **sur pièces** : les dix rapports relus, les chiffres
re-mesurés dans le dépôt.

## Cette tranche n'est pas la précédente

Le bilan n°9 disait de la tranche 390-399 : *« elle n'a rien construit »*. Celle-ci
a **trouvé deux défauts visibles par l'utilisateur**, puis les a **bornés**.

```text
lots ayant TROUVÉ un défaut             3   (401, 406, 407)
lots ayant BORNÉ une trouvaille         3   (402, 408, 409)
lots revenus NÉGATIFS                   3   (403, 404, 405)
bilan                                   1   (400)
──────────────────────────────────────────
lots ayant modifié la PRODUCTION        0     ← mesuré
```

```console
$ git diff --name-only <lot 399>..HEAD | grep -vE '^(tests|docs)/'
  (aucun)
```

**Un seul fichier non documentaire modifié sur dix lots** :
`tests/test_skyler_sweep_x1.py`, le correctif du 401.

## Les chiffres

| | |
|---|---|
| Lots | 10 (400 → 409) |
| Suite | **2 864 / 0 skipped**, identique aux 10 lots |
| Tests ajoutés | **0** — délibérément (tranche précédente : +29) |
| PR | **#432 → #441**, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, inchangé |
| Fichiers de production modifiés | **0** |

Zéro test ajouté en dix lots : la boucle a **mesuré** et **réparé**, elle n'a pas
gonflé la suite. C'est un choix, pas un manque — la règle « jamais un gardien
pour faire un lot » tient depuis le 384.

## Les trois trouvailles

1. **401 — un gardien qui passait selon l'ordre d'exécution.**
   `test_sweep_route_and_no_journaling` restaurait avec `if v is None:
   scan_state.pop(k)`. Or `market_ctx` est initialisée à `None` : la clé
   **existe**, sa valeur légitime **est** `None`. La remise en état la
   **supprimait** du dict partagé pour toute la session, et
   `test_scan_state_has_expected_keys` — le gardien des 8 clés documentées —
   tombait selon l'ordre. Prouvé par une reproduction à **deux fichiers**.

2. **406 — deux clés lues, jamais écrites.** Sur les 17 clés du contrat
   `DESK_KEYS`, **7 n'ont aucun écrivain**. Deux d'entre elles sont **lues par
   `/portfolio`** : `myTradesEquity` et `myCapital`. Conséquence : la **courbe
   d'équité** et le **drawdown** ne peuvent **jamais** s'afficher — et l'état
   vide promet « *elle se construit au fil des clôtures de positions
   déclarées* », alors que clôturer n'écrit jamais cette clé. **Une consigne qui
   ne peut pas aboutir.** Piège évité au passage : élaguer `DESK_KEYS` serait une
   **perte de données**, pas un nettoyage (last-writer-wins total, mécanisme du
   362).

3. **407 — un `|| 0` qui fabrique une alerte.** `cash: E().capital() || 0` est
   envoyé au moteur de risque avec `simulated: false`, donc **déclaré réel**.
   Mesuré, mêmes positions : `hhi` **0.5003 avec cash=0 contre 0.0029 avec un
   cash réel — un facteur 170**. Et le seuil d'affichage est franchi : avec **une
   seule position**, HHI = **1.0** → le terminal affiche « **Concentration très
   élevée** » là où un portefeuille réel n'aurait aucune alerte. Trois lignes
   plus bas, le fichier écrit la règle qu'il enfreint : *« Manquant/insuffisant
   n'est jamais présenté comme zéro. »*

## Les trois bornages — aussi utiles que les trouvailles

Savoir si un défaut est isolé ou général **change la décision**. Trois lots l'ont
établi :

```text
402   dépendance d'ordre     300 / 300 fichiers verts en isolation   → 401 était la seule
408   `|| 0` fautif          1 sur 25 charges utiles POST            → 407 est isolé
409   consigne impossible    1 sur 12 promesses (sur 88 états vides) → 406 est unique
```

Sans eux, la correction aurait pu être présentée comme une campagne. **Elle ne
l'est pas : une cause, un site, une carte.**

## Les trois lots négatifs

```text
403   tests sans assertion ou toujours vrais    2 / 2 563, tous deux légitimes
404   assertions avalées par un `except`        0 / 91 candidates
405   fichiers statiques morts                  0 / 54
```

Ce sont des **résultats**, pas des échecs : chacun ferme une question avec un
dénominateur mesuré et un instrument prouvé. Mais il faut dire l'autre moitié :
ils **coûtent** du temps et leur rendement décroît. Trois d'affilée avaient
justifié, au 405, de le signaler franchement.

## Ce que cette tranche apprend, et c'est le point principal

**L'instrument — ou son interprétation — a été pris en défaut dans 6 lots sur
10**, dont **deux fois dans le même lot** (401). À chaque fois **avant
publication**, par un témoin ou un contrôle de cohérence :

```text
400   un `cd` oublié → j'ai cru pendant six commandes que CLAUDE.md avait disparu
401   hook pytest mesurant AVANT les finalizers → 84 « fuites » dont 42 fausses
401   témoin `monkeypatch` écrivant une valeur DÉJÀ présente → idempotent, donc muet à tort
402   `nohup … &` → deux passes concurrentes, 195 fichiers couverts sur 300 annoncés
406   fichier exclu pour ce qu'il DÉCLARE → « 13 clés sans écrivain », dont `myTrades`
408   vivier trié par la FORME (53) pris pour une liste de défauts → le 1ᵉʳ ouvert est sain
409   compter la DÉFINITION d'une aide au lieu de ses APPELS → le site du 406 introuvable
```

C'est la statistique la plus utile de la tranche. Elle ne dit pas que la méthode
est mauvaise : elle dit que **le contrôle de l'instrument est la partie du
travail qui rapporte le plus**. Chacune de ces erreurs aurait produit un rapport
faux — présenté avec les mêmes tableaux et la même assurance.

## L'état du produit n'a pas bougé

Aucun fichier de production modifié sur la tranche (mesuré ci-dessus). Le MD5 des
8 pages servies a été re-prouvé identique aux lots **390** et **396** — et **pas
re-mesuré depuis** : il n'y avait aucune raison de le refaire, mais c'est une
affirmation d'inférence, pas de mesure fraîche, et elle est écrite comme telle.

## La question, plus courte que celle du bilan n°9

Le rang 1 ne contient plus seulement des inexactitudes discrètes. Il contient
maintenant :

- **un chiffre FAUX affiché comme RÉEL** — HHI d'un facteur 170 sur `/portfolio`,
  avec une alerte de concentration fabriquée dès qu'une seule position est
  déclarée ;
- **une consigne que le trader ne peut pas suivre** ;
- et, depuis le 388, **7 points MSFT fabriqués** servis comme des mesures.

La correction est **bornée et petite** : une cause (`myCapital` jamais écrit), un
site (`portfolio_page.py:718`), une carte (l'état vide de la courbe d'équité).
Les lots 408 et 409 l'ont vérifié précisément pour que la décision soit facile.

**Aucun GO n'est arrivé depuis le lot 388 — vingt-deux lots.**

- **(a)** continuer les lots courts. Trois négatifs sur les dix derniers ; le
  rendement décroît et c'est mesuré.
- **(b) GO groupé sur le rang 1, puis exécution. ← recommandé.** Commencer par la
  purge des 7 points MSFT (coût quasi nul, risque nul), puis `myCapital`.
- **(c)** arrêter la boucle et attendre. Défendable : rien ne se dégrade.

Ce qui ne serait pas honnête, c'est de continuer en (a) en laissant croire que le
travail avance sur ce qui compte. Depuis le 406, **il ne s'agit plus d'hygiène :
un chiffre faux est affiché comme réel.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier de production touché** — bilan documentaire. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Serveur DEMO **non lancé** (il fabriquerait un point dans `breadth_history`).
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; écart final
  **aucun**.
- Suite : **2864 passed / 0 skipped**.

## Portée

Ce bilan mesure ce que la tranche a **déposé dans le dépôt** et ce que les dix
rapports affirment. Il ne rejoue pas les trouvailles une à une — 402, 408 et 409
l'ont fait pour leurs périmètres respectifs ; le reste repose sur les preuves
consignées dans chaque rapport.
