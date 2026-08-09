# SKYLER LOT 449 — La veine `reason` refermée : 7 phrases sur 7 tranchées, le rang 2 du 448 passe d'une route à trois, et une phrase n'est jamais produite

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-449` (base : lot 448 fusionné,
05c1eef)

Trente et unième lot de la veine, **dernier lot de mesure de la tranche 440-449**.
Le 448 avait laissé **quatre phrases `reason` sur sept NON ÉTABLIES**, faute
d'avoir identifié leur consommateur. Ce lot solde la dette : **il ferme, il
n'ouvre pas.**

**Aucun code, aucun gardien, aucun test.**

## Étape A — remonter la route, puis le lecteur

Payload identifié par sa forme, route retrouvée, citation cherchée dans les
octets servis, lecture de champ vérifiée (`.reason`, jamais un jeton nu).

```text
phrase                          route servante                     cité par              lecteur .reason
options_lab_api.py:57           /api/options/strategies/<sym>      options-structure.js  :101  (ligne exacte)
                                                                   options-intel.js      :468  (niveau fichier)
options_lab_api.py:72           /api/options/analyze               options-structure.js  :101
horizon_scanners.py:47          /api/options/scanner/<universe>    options-scanner.js    :32
tradingview_signal_store.py:52  — aucune route —                   —                     —
```

Le couple le plus net est **line-exact** : `options-structure.js:97` va chercher
`/api/options/strategies/<sym>`, et **quatre lignes plus bas**, `:101` rend
`(d && d.reason)` dans `insufficientCard`. Pour `options-intel.js`, les appels
passent par un helper (`:96`) : j'établis le couple **au niveau du fichier**, pas
de la ligne, **et je le dis**.

### La quatrième n'est pas « non affichée » : elle n'est jamais produite

`tradingview_signal_store.py:52` est le retour de `SIGNAL_STORE.record(...)`.
Cherché en jeton nu dans tout `vertex/` : **`record()` de ce store n'a aucun
appelant**. Le `SIGNAL_STORE` n'est passé qu'à `system_diagnostics(...)`
(`strategy_os_api.py:153`), qui n'appelle pas `record`. La phrase « signal
inconnu : … » **n'est donc jamais construite**. Chemin mort — famille 436.

## Étape B — ce que les trois routes affichées rendent vraiment

Banc sur les **moteurs réels**, entrées mal formées :

```text
A. /api/options/strategies/<sym>   (multileg_lab.strategies_for_symbol)
   board None        → pas d'exception
   spot None         → pas d'exception
   board mal typé    → « AttributeError: 'str' object has no attribute 'get' »

B. /api/options/analyze            (multileg_lab.analyze_strategy)
   legs None         → pas d'exception
   legs vides        → pas d'exception
   leg mal typé      → « AttributeError: 'str' object has no attribute 'get' »

C. /api/options/scanner/<universe> (horizon_scanners.scan)
   univers 'SWING'   → « aucun contrat SWING dans la fenêtre [60, 180] pour ce filtre »
   univers 'inconnu' → « univers inconnu : 'INCONNU' (attendu ['LEAPS', 'SWING', 'TACTICAL']) »
   univers ''        → « univers inconnu : '' (attendu ['LEAPS', 'SWING', 'TACTICAL']) »
```

**A et B rendent une `AttributeError` Python dans une carte d'état vide de
`/options`.** C'est exactement le défaut du 448 — **et il n'était pas isolé** :

```text
routes qui affichent un vidage d'exception       448 : 1        449 : 3
   /api/options-for/…            options-intel.js:413    « simulation impossible: 'NoneType' object has no attribute 'spot' »
   /api/options/strategies/<sym> options-structure.js:101 / options-intel.js:468
   /api/options/analyze          options-structure.js:101
```

**Le rang 2 du 448 triple.** Trois routes de la page `/options`, trois cartes
d'état vide, trois messages d'implémentation présentés comme le motif.

### Et le témoin positif est sur la même page

**C ne présente aucun défaut.** `horizon_scanners` rend, dans le **même champ**,
sur la **même page**, par le **même chemin de rendu** :

- un refus de configuration qui **nomme la valeur reçue et l'ensemble attendu** ;
- un état vide qui **nomme le filtre et la fenêtre** — « aucun contrat SWING dans
  la fenêtre [60, 180] ».

C'est le contrôle qui manquait au 448 : l'instrument **distingue**, sur le même
écran, trois phrases fautives d'une phrase juste. Le défaut n'est donc pas une
propriété de la page ni du champ — **c'est une propriété des blocs `except`.**

## La veine `reason`, refermée

```text
phrase                            affichée ?        verdict
evidence_lab.py:59                OUI  (/analysis)  EXACTE      (448, banc 8/8)
anomaly.py:56                     OUI  (anomaly-scan.js) EXACTE (448)
horizon_scanners.py:47            OUI  (/options)   EXACTE      (449)
options_intel_api.py:113          OUI  (/options)   VIDAGE      rang 2 (448)
options_lab_api.py:57             OUI  (/options)   VIDAGE      rang 2 (449)
options_lab_api.py:72             OUI  (/options)   VIDAGE      rang 2 (449)
tradingview_signal_store.py:52    JAMAIS PRODUITE   chemin mort rang 4 (449)

                    7 sur 7 tranchées · 6 affichées · 3 exactes · 3 vidages · 1 morte
```

**Aucune ligne ne reste « non établie ».** C'est la clôture que le dernier lot
d'une tranche devait produire.

## Classement

- **Le vidage d'exception passe d'une route à trois** → le **rang 2** du 448 est
  **aggravé** en portée, pas en nature : toujours pas d'affirmation fausse,
  toujours affiché, désormais **trois fois** sur la même page.
- **`tradingview_signal_store.py:52` : phrase jamais produite** → **rang 4**,
  poids mort.
- **`horizon_scanners.py:47` : exacte** → aucun défaut, et **contre-exemple
  utile** — la correction pressentie pour les trois vidages est écrite dans ce
  fichier-là.

Correction pressentie, inchangée : journaliser l'exception côté serveur et rendre
un motif écrit, comme le fait `horizon_scanners` **sur la même page**. **Aucun
GO, rien n'est engagé.** Aucun test ne vérifie qu'un `reason` servi est une
phrase : **aucun gardien.**

## Portée

Les exceptions sont **réelles** (levées par `multileg_lab`), mais le formatage est
**la ligne de la route recopiée**, pas la route exécutée : `/api/options/…` exige
un board peuplé, vide au démarrage. **Une reproduction n'est pas une exécution**
(règles 443, 448).

Une seule famille d'entrées mal formées a été essayée (types incorrects). Je
n'ai **pas** cherché si d'autres chemins produisent des messages plus révélateurs
— chemins de fichiers, valeurs internes.

Le couple route ↔ lecteur est **line-exact** pour `options-structure.js`, et
**au niveau du fichier** pour `options-intel.js` : je ne prétends pas mieux.

`board None` et `spot None` **ne lèvent pas** : les moteurs encaissent l'absence
proprement. Le vidage n'apparaît que sur une entrée **mal typée** — je n'ai pas
mesuré la fréquence de ce cas en usage réel.

**Aucun navigateur ouvert.** Sur les 110 phrases concluantes du 444, **93 restent
fermées** : ce lot n'en ouvre aucune nouvelle, il termine les sept du 448.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. `multileg_lab` et `horizon_scanners` appelés en mémoire ;
  routes en **GET** ; `persist` redirigé.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Cinquante-deuxième lot court, **dernier de la tranche 440-449**.

Il fait ce qu'un dernier lot doit faire : il **solde une dette** au lieu d'ouvrir
un front. Les quatre lignes que le 448 avait laissées en suspens sont tranchées,
et la conclusion n'est pas neutre — **le défaut isolé du 448 était en fait
triple**, et le contre-exemple qui le condamne est sur la même page, dans le même
champ.

Le bilan n°14 trouvera donc la veine `reason` **close** : 7 sur 7.

Comptes séparés, inchangés : résultats faux **arrêtés avant publication** **20** ;
**publiés puis corrigés** **1**.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
