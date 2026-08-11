# SKYLER LOT 507 — `/options`, desk jamais audité : `iv_units` promet une détection d'unité « JAMAIS MUETTE » et le moteur tient parole — il rend `iv_unit`, `iv_detected_from` et un avertissement en clair. **L'interface n'en lit AUCUN.** Zéro consommateur de `warnings` dans les trois scripts servis, alors que la clé voisine `limitations` est rendue deux fois

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-507` (base : lot 506 fusionné,
`dfb18b88`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)** et `/options`, comme recommandé : desk autonome, jamais mesuré, plein de
chiffres où une erreur d'unité se voit. La piste des unités était la bonne, mais
**pas là où je la cherchais** — et le second contrôle a démoli deux tiers de mon
brouillon avant de laisser un dossier plus petit et plus net.

## D'abord : je corrige un chiffre que j'ai publié il y a un lot

Le 506 a publié « **30 vues servies, 8 empreintées** ». **C'est faux.** J'avais lu
`_VIEWS` sur chaque module ; or `/options` sert ses vues via `_ALL_VIEWS`
(6 visibles **+ 3 legacy** : `overview`, `radar`, `scenarios`), et
`/opportunities` a **cinq** vues que j'avais comptées pour une seule.

```text
page              vues réellement servies (ce que render() accepte)
/journal                     5
/portfolio                   6
/markets                     5
/options                     9   ← 6 + 3 legacy hors barre d'onglets
/system                      5
/opportunities               5   ← comptée « 1 » par le 506
/ · /analysis                2
──────────────────────────────
TOTAL                       37   (le 506 disait 30)   ·   8 empreintées
```

**Vingt-neuf vues servies hors de toute empreinte, pas vingt-deux.** Empreintes
nouvelles : `/options?view=overview` `7524912d285a` · `radar` `0e0addc7515e` ·
`scenarios` `bc4f76a90c3b` · `/opportunities?view=stocks` `96c7c4f531a5` ·
`options` `c79a0f86fcee` · `anomalies` `1ba9b087876f` · `calendar` `b2292037cb33`.

**Publiés puis corrigés : 12 → 13.** C'est la deuxième fois en deux lots que
`_VIEWS` me piège ; le 506 s'était déjà trompé sur `VIEWS` pour `/system`.

## La question posée, et ce que le contrat déclare

`vertex/options/iv_units.py` énonce son contrat **trois fois** :

```text
« plus JAMAIS d'heuristique silencieuse "si IV > 1,5, diviser par 100" dans le
  cœur métier »
« from_legacy_board — UNIQUE frontière tolérée pour le board historique »
« La détection y est EXPLICITE, ÉTIQUETÉE (unité détectée + avertissement) et
  testée — jamais muette. L'appelant DOIT propager l'unité détectée et
  l'avertissement. »
« le cœur métier n'a pas le droit de deviner. »          _LEGACY_THRESHOLD = 1.5
```

## La réponse — le moteur tient parole, l'interface la rompt

Mesuré en appelant `multileg_lab.strategies_for_symbol` en processus sur le board
DEMO (GOOGL) :

```text
iv                = 0.468
iv_detected_from  = 'PERCENT'
iv_unit           = 'DECIMAL'
warnings          = ['IV du board détectée en POURCENTAGE (46.8) — convertie en
                     décimal à la frontière legacy (iv_units.from_legacy_board).']
```

**Le moteur propage exactement ce que le module exige.** Puis :

```text
octets servis inspectés : 6 vues de /options + options-intel.js + options-structure.js
                          = 223 890 caractères
  « iv_warning »        ABSENT
  « iv_unit »           ABSENT
  « POURCENTAGE »       ABSENT
  « from_legacy_board » ABSENT
  « frontière legacy »  ABSENT
```

Et — c'est la mesure qui tranche, parce qu'un littéral absent des octets ne
prouverait rien si le JS rendait le tableau à l'exécution :

```text
occurrences de `.warnings` dans options-intel.js, options-structure.js,
options-gex.js :                                                     ZÉRO
occurrences de `limitations`, rendues à l'écran :   DEUX
    options-intel.js:67   '<h4>Limites méthodologiques</h4><ul>' + li(interp.limitations)
    options-intel.js:431  var lims = (sim.limitations || []).map(…)
```

**La page a une place pour les réserves méthodologiques, et elle l'utilise. Le
canal `warnings` — celui où atterrit la détection d'unité — n'a aucun
consommateur.** Une conversion d'unité a lieu à chaque analyse d'options, et
aucun octet servi ne le dit.

## Le second contrôle — il a retiré DEUX tiers de mon brouillon

J'étais parti sur une thèse plus large : « sept politiques d'unité concurrentes,
donc des affichages faux d'un facteur 100 ». Trois contrôles l'ont réduite.

### I. La bande de divergence existe, mais elle n'est PAS atteinte

Sept sites de conversion vivent hors de la frontière « unique » — re-comptés sur
disque, pas de mémoire :

```text
options_intel_api.py:64    c.get('iv') / 100.0                   INCONDITIONNEL
options_intel_api.py:105   iv/100 if isinstance(iv,…) and iv > 3  seuil 3, muet
redesign.py:220-221        if contract['iv'] > 3: … / 100.0       seuil 3, muet
swing.py:23                / (100.0 if (iv or 0) > 3 else 1.0)    seuil 3, muet
red_team.py:66             iv * 100 if iv < 3 else iv             seuil 3, muet
vol_charts.py:56 et :115   round(iv / 100.0, 4)                   INCONDITIONNEL ×2
```

Le seuil documenté est **1,5** ; quatre heuristiques inline utilisent **3**. Sur
la bande `]1.5, 3]` les deux politiques divergent **d'un facteur 100** :

```text
board   frontière 1.5   seuil 3    verdict
 1.49        1.490000   1.490000   accord
 1.60        0.016000   1.600000   ** DIVERGENT **
 2.00        0.020000   2.000000   ** DIVERGENT **
 2.99        0.029900   2.990000   ** DIVERGENT **
 3.50        0.035000   0.035000   accord
```

**Mais le board DEMO ne l'atteint jamais** : 51 contrats, `iv` min **28,1**,
médiane **46,8**, max **61,9** — tous en pourcentage, tous au-dessus de 3.
**Zéro contrat dans la bande.** La divergence est donc **théorique sur ce
board**, et je n'ai aucun moyen d'ici de mesurer le board réel. Je ne fais pas de
dossier avec ça.

### II. Le couple `vol_charts` ↔ JS se COMPENSE

`vol_charts.py` divise par 100 ; `options-intel.js:310` et `:388` multiplient par
100. **Aller-retour = identité.**

```text
board en POURCENTAGE  45.0  → serveur 0.45   → affiché 45.0 %  (vérité 45 %)  JUSTE
board en DÉCIMAL      0.45  → serveur 0.0045 → affiché  0.4 %  (vérité 45 %)  FAUX
```

Sur le board mesuré (pourcentage), **l'affichage est juste**. Mon grief ne tient
que pour un board décimal, qui n'existe pas ici. **Retiré.**

### III. Et les deux conventions du JS ne sont pas une incohérence

J'avais relevé que le JS traite `iv` tantôt en pourcentage (`:230`, `:436`,
`options-structure.js:345`) tantôt en décimale (`:310`, `:388`, `:473`,
`options-structure.js:105`). **Ce ne sont pas les mêmes objets** : `overview` et
`scenarios` renvoient l'`iv` brute du board (pourcentage), `strategies` et
`vol-charts` renvoient du décimal normalisé. **Chaque site respecte le contrat de
SON endpoint.** Règle 495 appliquée : une clé lue sur le mauvais objet — sauf
qu'ici elle est lue sur le bon. **Retiré.**

**Arrêtés avant publication : 86 → 89.**

## Aucun gardien sur la propagation

```text
tests/test_iv_units_lot114.py          la FRONTIÈRE elle-même
tests/test_options_correctness_lot1.py normalize_iv(40.4, PERCENT) == 0.404
tests/test_multileg_iv_units_06.py     la conversion dans le moteur
occurrences de « warnings » dans ces quatre fichiers :        ZÉRO
```

La frontière est bien gardée. **Ce que le module appelle l'obligation de
l'appelant — propager — n'est vérifié par rien.**

## DOSSIER 507-A — Classement

**Rang 3, et je dis par rapport à quoi.**

L'étalon est le **454** : *une conséquence CALCULÉE, SÉRIALISÉE et ENVOYÉE n'est
toujours pas AFFICHÉE*, classé **rang 4** avec ce motif — « Rien de faux n'est
montré, et c'est pour cela que ce n'est pas plus haut ».

**Ici non plus rien de faux n'est montré** : sur le board mesuré, l'IV affichée
(46,8 %) est juste. Mais je le place **un cran au-dessus du 454**, sur deux
critères absolus :

1. **Un contrat explicite est rompu au dernier mètre.** Le module ne dit pas
   « il serait bien de propager » : il écrit « l'appelant **DOIT** propager » et
   « jamais muette ». Le moteur obéit ; l'interface jette. La promesse est donc
   **fausse du point de vue de l'utilisateur**, qui est le seul point de vue qui
   compte (critère du 464 — le consommateur).
2. **La place existe et sert déjà.** `limitations` est rendue à deux endroits sur
   la même page. Ce n'est pas « il n'y avait pas où le mettre » : c'est un canal
   rempli sans lecteur, à côté d'un canal identique qui est lu.

**Ce qui l'empêche d'être rang 2** : aucun chiffre faux, aucune phrase fausse,
et la valeur manquante est une **provenance**, pas une mesure. Sur le board
mesuré, l'utilisateur ne perd rien d'exploitable — il perd le droit de savoir
qu'une conversion a eu lieu.

Correction pressentie, non engagée : rendre `warnings` là où `limitations` est
déjà rendue (deux lignes de JS), **ou** fusionner les deux canaux ; et, pour la
fragilité structurelle, ramener les quatre heuristiques `> 3` sur
`iv_units.from_legacy_board` afin qu'il n'existe qu'un seul seuil. **Aucun GO,
rien n'est engagé.**

## Fait ancré sans être classé

**Sept sites de conversion contredisent la mention « UNIQUE frontière »**, avec
deux seuils incompatibles (1,5 contre 3) et trois divisions sans aucune
détection. Sur le board mesuré, rien n'en sort de faux. **C'est une fragilité
structurelle, pas un défaut observable — et un jour où un producteur émettra du
décimal, les trois divisions inconditionnelles rendront des IV cent fois trop
petites, en silence.** Je l'ancre ; je ne le classe pas.

## Portée — ce que ce lot NE dit PAS

- **Le board mesuré est le board DEMO.** Il est en pourcentage. Je n'ai **aucun
  moyen d'ici** de savoir si le board réel (IBKR/yfinance) l'est toujours. Toute
  la partie « la divergence n'est pas atteinte » vaut **pour la démo seulement**.
- **Aucune route `/api/options/*` n'a été appelée** — ni `/options/<sym>`, ni
  aucun POST. J'ai appelé `multileg_lab.strategies_for_symbol` en processus, et
  lu les octets servis par les pages et les fichiers statiques.
- **Aucun navigateur ouvert.** L'absence des littéraux dans les octets servis est
  corroborée par l'absence de `.warnings` dans le JS — c'est cette seconde mesure
  qui fait la preuve, pas la première.
- `terminal.scan()` a été exécuté en DEMO pour peupler le board (51 contrats) ;
  le snapshot runtime a tout restauré.
- Les **trois vues legacy** de `/options` (`overview`, `radar`, `scenarios`) sont
  servies mais **hors barre d'onglets** — atteignables par URL seulement. Fait
  ancré, non jugé.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les deux scripts.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Quatrième lot d'affilée dans le produit, quatrième dossier — mais **le plus petit
des quatre**, et c'est le résultat honnête. J'ai commencé avec une thèse à
facteur 100 sur sept sites ; le second contrôle en a retiré la bande (non
atteinte), le couple `vol_charts` (il se compense) et la prétendue incohérence du
JS (chaque site respecte son endpoint). Ce qui reste tient en une phrase : **un
avertissement écrit noir sur blanc par le moteur, que personne ne lit.**

La règle que je retiens : **une thèse qui rétrécit sous ses propres contrôles
n'est pas un lot raté.** Trois retraits et un dossier rang 3 valent mieux qu'un
dossier rang 1 fondé sur une bande que le board n'atteint jamais.

Feuille : **30 dossiers · seize rang 1 · onze rang 2 · quatre rang 3**.
Dettes nommées restantes : **`/markets`** (jamais auditée, cinq vues) ; **les
vingt-neuf vues servies hors empreinte** ; **les trois sous-vues de `/journal`** ;
**l'espion au troisième niveau** (toujours déconseillé) ; **le compte des rangs
relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 89 (+3)** ; publiés
puis corrigés **12 → 13** (les « 30 vues servies » du 506) ; interprétations
retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
