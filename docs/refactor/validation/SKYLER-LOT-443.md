# SKYLER LOT 443 — Trois R:R différents sur la même page, et le seul honnête n'apparaît que pour se plaindre : le test du 442 généralisé aux douze champs du plan

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-443` (base : lot 442 fusionné,
3254557)

Vingt-cinquième lot de la veine. Le 442 avait trouvé que `plan.rr` est un
littéral constant et que `rr_res` n'est jamais servi. Question de ce lot :
**combien d'autres champs du plan sont dans ce cas ?** Le balayage a répondu — et
il a corrigé une de mes propres affirmations au passage.

**Aucun code, aucun gardien, aucun test.**

## L'instrument, et ses deux témoins intégrés

Pour chacun des **douze champs** du `plan` : nombre de valeurs distinctes sur six
marchés très différents (banc sur le moteur réel), occurrences dans les octets
servis, nombre de moteurs consommateurs.

**Témoins positifs intégrés** — l'instrument doit retrouver seul les deux
trouvailles du 442 :

```text
rr       1 valeur distincte sur 6   → CONSTANT      ✓ retrouvé
rr_res   5 valeurs distinctes       → jamais servi  ✓ retrouvé
```

Il les retrouve. Contrôles d'échappement (leçon 436) : **0 déstructuration de
`plan`, 0 accès par crochet `plan[…]`** dans les octets servis.

## Le tableau, après trois corrections

```text
champ           distinctes/6   atteint un écran ?              moteurs
entry                      6   OUI  (5 rendus)                      11
stop                       6   OUI  (8 rendus)                      14
tp1 / tp2 / tp3            6   OUI  (cône, price-chart, lwc)   9/13/11
resistance                 6   OUI  — via un BUILDER                 6
rr                         1   OUI  (4 rendus)  ← CONSTANT           4
atr                        6   non observé                           2
rr_res                     5   seulement en MESSAGE DE BLOCAGE       9
setup_quality              5   non observé                     1 (+5 sur un homonyme)
stop_type                  2   OUI — dans une PHRASE SERVEUR         3
stop_dist_atr              2   NON — aucun consommateur, nulle part  0
```

**Sept champs sur douze atteignent un écran. Un seul est totalement mort.**

### Trois verdicts faux, arrêtés avant publication

Mon premier tableau annonçait **six** champs « jamais servis ». Trois étaient
faux, et chacun pour une raison différente :

**`resistance`** — `plan.resistance` compte 0 dans les octets de la page, mais
`price-chart.js:16` lit `plan.resistance` et en fait un niveau étiqueté
« Résistance », et `candlestick-lwc.js:133` le rend aussi. Le champ est consommé
**dans un builder servi depuis `/static`**, qui reçoit `plan` en option.
*Compter sans les enveloppes rate l'usage* — **sixième récidive** (409, 413, 414,
439, 442, ici).

**`setup_quality`** — mon compteur annonçait **zéro consommateur**. Faux : il
existe **deux** `setup_quality`, l'un dans `plan` (`analysis.py:264`), l'autre au
**premier niveau** du payload (`:316`). Les cinq moteurs que je cherchais lisent
le second (`quant_engine:67`, `decide:23`, `skyler_core:161`, `track_record:58`,
`context:17`) ; celui du plan n'a qu'un lecteur, `weekly.py:79`, qui se replie
justement sur le premier. *Un nom peut désigner plusieurs payloads* — leçon 438,
appliquée à deux **niveaux** du même objet.

**`stop_type`** — annoncé « n'atteint aucun écran », et c'est faux d'une manière
que la boucle n'avait encore jamais rencontrée. `committee.py:133` :

```python
invalidation = f"clôture sous ${plan.get('stop')} ({plan.get('stop_type', 'structure')})"
```

Le champ n'est pas lu par le client : il est **fondu dans une phrase composée au
serveur**. Et `invalidation` est lu par **cinq écrans** — `/`, `/opportunities`,
`/portfolio`, `/journal`, et **12 fois** sur la route `/analysis` à paramètre.

**Règle nouvelle** : *un champ peut atteindre l'écran à l'intérieur d'une phrase
composée au serveur — une recherche par NOM DE CHAMP sur les octets servis ne le
verra jamais.* Mon instrument mesure ce que le **client** lit par nom ; il est
aveugle à ce que le **serveur** rédige.

### Le seul champ vraiment mort

**`stop_dist_atr`** : calculé à chaque analyse (`analysis.py:263`), recherché en
jeton nu dans tout `vertex/` et `terminal.py` — **aucun lecteur**, et **0
occurrence** dans les 8 pages, la route à paramètre et les 43 fichiers `/static`.
Un champ sur douze, du poids mort (famille 436). **Rang 4** : rien à l'écran,
donc aucun mensonge.

## La correction que je dois à mon propre lot 442

Le 442 affirme : « `rr_res` n'est affiché nulle part ». **Trop fort.** Mesuré ici,
en exécutant `build_ticket()` :

```text
rr_res = 0.4  → blocked=True   « R:R 0.4 < 2.0 (minimum stratégie) »   AFFICHÉ
rr_res = 1.1  → blocked=True   « R:R 1.1 < 2.0 (minimum stratégie) »   AFFICHÉ
rr_res = 3.5  → blocked=False  —                                       jamais montré
rr_res = 4.7  → blocked=False  —                                       jamais montré
rr_res = None → blocked=False  —                                       jamais montré
```

Le ticket est atteignable depuis la page (`an-order-ticket`, `__prepOrder`,
`/api/planning/ticket` — tous présents dans les octets servis).

**Formulation exacte substituée** : le R:R honnête **n'apparaît que lorsqu'il est
mauvais**, et sous la forme d'un **message de blocage**. Un bon R:R (4,7) n'est
montré nulle part. La trouvaille du 442 tient ; sa phrase était trop absolue.

## Ce que le balayage a trouvé de neuf : trois R:R, même page, même instant

En remontant les consommateurs de `rr_res`, un troisième R:R apparaît.
`pretrade.py:130` **le recalcule**, à partir du prix **live** :

```python
rr = (tp1 - px_now) / (px_now - stop)          # ni plan.rr, ni plan.rr_res
```

Et `/api/pretrade/check` est l'une des **douze routes** que la page appelle.
Mesuré, pour le même titre au même instant :

```text
cas                 carte plan   rr_res (décide)   pré-trade au prix d'entrée   pré-trade à +3 %
haussier calme           3.0:1               0.4                        1.0:1              0.2:1
haussier violent         3.0:1               0.7                        1.0:1              0.5:1
baissier                 3.0:1               1.1                        1.0:1              0.3:1
plat                     3.0:1               3.5                        1.0:1                  —
très volatil             3.0:1               1.1                        1.0:1              0.6:1
court (120 barres)       3.0:1               4.7                        1.0:1                  —
```

Deux faits :

**Le pré-trade rend 1,0:1 au prix d'entrée, pour tous les titres.** C'est
structurel : `tp1 = entrée + risque`, donc `(tp1 − entrée)/(entrée − stop) = 1`
exactement. **Un second constant par construction**, découvert par le même test
que le premier.

**Et il est étiqueté comme une faute.** `pretrade.py:134` ajoute
« (< 2:1 — Constitution) » dès que le R:R passe sous 2. Donc la même page peut
afficher, au même instant, pour le même titre :

```text
carte plan       « R:R structurel 3 »
contrôle pré-trade  « Invalidation … · TP1 … · R:R 1.0:1 (< 2:1 — Constitution) »
```

**L'un dit que le plan est bon, l'autre qu'il viole le minimum de la stratégie.**
Ni l'un ni l'autre ne dit contre quel objectif il compte — 3 est vs TP3, 1,0 est
vs TP1 — et aucun des deux n'est le R:R que les neuf moteurs utilisent pour
décider.

## Classement

- **Trois R:R contradictoires sur la même page, aucun n'annonçant sa
  référence** → **rang 1**, et il **aggrave** le 442 : ce n'est plus une
  tautologie isolée, c'est une contradiction visible à l'écran.
- **`rr_res` visible seulement en message de blocage** → nuance du 442, la
  trouvaille tient, la phrase est corrigée.
- **`stop_dist_atr` mort** → **rang 4**.

Correction pressentie, inchangée dans son esprit : nommer la référence de chaque
R:R (« vs TP3 », « vs TP1 »), et afficher `rr_res` — déjà calculé, déjà servi.
**Aucun GO, rien n'est engagé.**

Aucun test du dépôt ne compare ces trois valeurs : **aucun gardien.**

## Portée

Le R:R du pré-trade est obtenu en **reproduisant la formule** de
`pretrade.py:130`, pas en appelant la route : `/api/pretrade/check` est un
**POST** qui exige un `scan_state` peuplé, et le scan est vide au démarrage. La
formule est recopiée à l'identique, mais **ce n'est pas une exécution de la
route** — je le dis plutôt que de le laisser croire.

Le banc utilise le **moteur réel** sur des séries **synthétiques** : il établit le
comportement du code, **pas la fréquence des cas réels**.

Mon instrument mesure ce que le **client** lit **par nom de champ**. Il est
aveugle aux valeurs **fondues dans une phrase composée au serveur** — c'est
exactement ce qui a produit le faux verdict sur `stop_type`, et je n'ai **pas**
quantifié combien d'autres champs passent par ce chemin.

`atr` et `setup_quality` sont classés « non observé », pas « absent » : leur nom
n'apparaît nulle part dans les octets servis, mais la limite ci-dessus s'applique
aussi à eux.

Aucun navigateur ouvert.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Routes appelées en **GET** ; `persist` redirigé vers un
  répertoire temporaire ; `analyse()` et `build_ticket()` appelées en mémoire,
  sans écriture.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Quarante-sixième lot court. Séquence : **441 ✗ · 442 ✓ · 443 ✓ (généralisation
qui aggrave)**.

Le 442 avait ouvert une affirmation et trouvé un défaut. Ce lot applique le même
test aux douze champs voisins : il **retrouve seul** les deux trouvailles du 442,
en **corrige la formulation**, en **écarte trois faux verdicts** — dont un par un
mécanisme neuf, la phrase composée au serveur — et en **remonte un plus gros** :
trois R:R contradictoires sur le même écran.

Le compte des résultats faux arrêtés avant publication passe à **dix-huit**,
convention du 440.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
