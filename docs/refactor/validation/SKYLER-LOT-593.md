# SKYLER — LOT 593

## Ce que le lot établit

**Trois gardiens sur quatre ont un écart entre leur prose et leur code — et
tous les écarts vont dans le même sens : le code est plus PERMISSIF que la
prose.** Sept promesses lues : **EXACT 3 · PLUS LARGE 3 · NON ÉCRIT 1**, aucun
« plus étroit ».

Un seul gardien tient exactement ce qu'il annonce : celui du lot **366**.

## Le choix (mmm)

Le 592 a trouvé un écart sur **un** gardien. Les trois autres n'avaient jamais
été confrontés à leur propre docstring.

## Le piège, MIXTE prévu d'avance (590-A) — troisième d'affilée

| volet | verdict |
| --- | --- |
| **(a)** « au moins un autre gardien a un écart » | **CONFIRMÉ** : deux autres (228, 23) |
| **(b)** « les nombres des docstrings sont TOUS périmés » | **RÉFUTÉ** : **deux des trois sont encore exacts** |
| **global** | **MIXTE** |

## Le tableau prose / code — sept promesses lues

| gardien | verdict | promesse écrite | ce que le code vérifie |
| --- | --- | --- | --- |
| 228 | **EXACT** | les références citées existent toutes | `morts == []` sur tout `SKYLER-LOT-*.md` cité |
| 228 | **PLUS LARGE** | « 13 rapports pré-index (lots **01-09**) » | `^SKYLER-LOT-0[1-9][A-E]?\.md$` — accepte **aussi les suffixes A-E** |
| 228 | **PLUS LARGE** | « le périmètre est **écrit dans l'en-tête** de l'index » | `'lots' in head and '10' in head and 'STATUS.md' in head`, sur 600 caractères |
| 364 | **PLUS LARGE** | « à condition de le dire **sur la même ligne** » | `any(nom in ligne and 'RETIRÉ' in ligne …)` — n'importe où *(témoin du 592)* |
| 366 | **EXACT** | tout `CAPS_SNAKE` d'une docstring de moteur existe dans le paquet | 6 racines pour les docstrings, **tout `vertex/`** pour la recherche |
| 23 | **EXACT** | l'index consolide les rapports 10 → 23 | `for n in range(10, 24): assert 'SKYLER-LOT-%d' % n in idx` |
| 23 | **NON ÉCRIT** | *(rien dans la docstring)* | `assert 'GO' in idx` — **une exigence que la prose ne mentionne pas** |

**Le sens des écarts est unanime.** Trois fois le code accepte davantage que la
prose ; **zéro fois il exige davantage**. Sauf sur un point : le gardien du
lot 23 vérifie **en plus** que l'index contient le mot `GO` — une exigence
réelle, invisible dans sa description.

## Les nombres datés, recalculés avec le critère du code (587-A)

| nombre cité | à sa date | aujourd'hui |
| --- | --- | --- |
| « 218 rapports cités » *(lot 228)* | 218 | **582** |
| « 13 rapports pré-index » *(lot 228)* | 13 | **13** — encore exact |
| « 110 modules de moteur » *(lot 366)* | 110 | **110** — encore exact |

**Les trois sont datés dans leur propre phrase** : « Calibré au lot 228 : … »,
« Audit du lot 364 : … », « Ce lot a passé les 110 modules ». **Un nombre daté
qui a bougé n'est pas un mensonge** (592-C). Et **deux des trois n'ont pas
bougé** — mon attente disait « tous périmés ».

## L'arrêt du lot — j'ai recalculé avec ma définition, pas la sienne

Mon premier banc annonçait **117 modules** contre les 110 de la docstring : un
nombre « périmé ». **Faux.** Le code du gardien exclut `__init__.py` :

```python
out += [os.path.join(racine, n) for n in noms
        if n.endswith('.py') and n != '__init__.py']
```

Recalculé **avec son critère** : **110 exactement**. Le nombre n'a pas bougé
d'une unité en 227 lots.

**C'est la faute du 592 répétée** (594 rapports contre 587 — deux définitions).
Cette fois elle est arrêtée avant publication, pas déclarée après.

**Arrêtés avant publication : 218 → 219 (+1).**

## Second contrôle (481) — hors du périmètre des quatre

La restriction « les quatre gardiens documentaires » exclut les gardiens de
production. Deux d'entre eux, cités par `CLAUDE.md`, portent pourtant des
nombres mesurables dans leur docstring :

- `test_sw_cache_scope_lot361` : « **Mesure de l'historique au lot 361** :
  27 commits sur 144 touchant… » — **daté**.
- `test_desk_keys_servies_lot381` : « Retirer `vxAlerts` du repli servi passe
  **les 2 754 tests** » — **daté**, et la suite en compte **2 864** aujourd'hui.

**Le même phénomène existe hors du périmètre, et de la même nature** : des
mesures datées, pas des promesses. La restriction n'isolait pas un cas
particulier.

## Ce que le lot n'établit pas

- **Que ces écarts soient des défauts.** Un gardien plus permissif que sa prose
  **passe quand même** ; il garde moins que ce qu'on croit en le lisant. C'est
  un constat de lisibilité, pas une accusation.
- Que les sept promesses soient toutes celles des quatre gardiens : **je les ai
  lues, je ne prouve pas qu'il n'y en a pas d'autres**.
- Que le sens unanime des écarts soit une loi : **trois cas**, c'est une
  tendance mesurée sur un très petit nombre (leçon du 590-C).
- Que `assert 'GO' in idx` soit intentionnel ou accidentel : **non déterminé**.

## Limites déclarées

- La classification EXACT / PLUS LARGE / PLUS ÉTROIT / NON ÉCRIT est une
  **lecture**, portée par le tableau, pas un programme.
- Le classeur automatique [DATÉ]/[ACTUEL] du premier banc s'est trompé : il a
  marqué « Ce lot a passé les 110 modules » comme *actuel* alors que « Ce lot »
  le date. **La lecture a corrigé le classeur, pas l'inverse** (583-A).
- Les quatre gardiens **passent** : rien ici ne contredit un test vert (592-A).

## Règles neuves

- **593-A — LES ÉCARTS PROSE/CODE VONT TOUS DANS LE MÊME SENS : LE CODE EST
  PLUS PERMISSIF QUE LA PROSE.** Trois « plus large », zéro « plus étroit ».
  En lisant une docstring de gardien, on surestime ce qu'il garde.
- **593-B — UN NOMBRE DATÉ SE RECALCULE AVEC LE CRITÈRE DU CODE QUI L'A
  PRODUIT.** 117 contre 110 : la différence tenait à `__init__.py`.
- **593-C — UN TEST PEUT VÉRIFIER PLUS QUE SA PROSE N'ANNONCE.** Une promesse
  **non écrite** est un écart au même titre qu'une promesse excédée.

## Ce que le dépôt fait bien

- **Tous les nombres des docstrings sont datés.** Aucun n'est présenté comme
  une vérité d'aujourd'hui : « Calibré au lot 228 », « Audit du lot 364 »,
  « Ce lot a passé… ». C'est ce qui les rend inoffensifs en vieillissant.
- **Deux nombres sur trois n'ont pas bougé en plus de deux cents lots** — le
  périmètre pré-index (13) et le parc de moteurs (110) sont stables.
- **Le gardien du lot 366 tient exactement sa prose**, et sa docstring explique
  même *pourquoi* sa portée est celle-là (« la recherche doit couvrir le
  paquet », leçon payée pendant son propre audit).
- **Le gardien du lot 23 en fait plus que promis**, pas moins.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché, aucun test modifié, aucune docstring
  corrigée** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped** · `git status tests/` et `docs/**` (hors 593) **vides**

## Comptes

- Arrêtés avant publication : **219 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **13**
