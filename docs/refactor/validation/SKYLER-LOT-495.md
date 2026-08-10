# SKYLER LOT 495 — La veine des barèmes close : les « cinq » n'étaient que DEUX — et en la fermant, la mesure trouve un DOSSIER RANG 1, le moteur exécutif décide en aveugle sur QUATRE de ses entrées, dont le score fondamental

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-495` (base : lot 494 fusionné,
`ea749665`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

**Premier dossier neuf depuis cinq lots**, et il n'était pas la cible : il sort de
la fermeture d'une veine qu'on croyait vide.

## Le choix

J'ai pris **(a)**, comme recommandé : la veine des barèmes est une dette de
**mesure** nommée depuis le 491 et jamais payée, alors que (b) — l'audit
`PAGE_*` — ouvrait une famille neuve après quatre lots stériles. **(b) reste une
dette nommée.**

## La liste des « cinq barèmes » était sale — pour la deuxième fois

Le 491 avait déjà montré que la liste du 486 confondait trois échelles. Rebelote,
tracé sur pièces :

```text
best.score /100   opportunities_page.py:111  ─┐  MÊME producteur : row.score
r.score    /100   opportunities_page.py:149  ─┘  (deux sites de rendu, un barème)
edge       /100   opportunities_page.py:119     quant_engine.edge — NON mesuré ici
rating_mean /5    analysis_page.py:486          consensus analystes yfinance
                                                → échelle EXTERNE, pas un barème Vertex
count / 10 max    analysis_page.py:673          « Positions déclarées 3 / 10 max »
                                                → un COMPTE contre un plafond de
                                                  portefeuille, pas un score
```

**Cinq entrées → deux barèmes réels.** Et sur les deux, un seul est mesuré ici.

## Ce que le barème « score Vertex /100 » donne, mesuré

Banc sur `vertex/quant/scoring.py`, **691 200 combinaisons d'indicateurs × 3 jeux
de fondamentaux**. **Calibration écrite dans le banc**, calculée à la main sur le
code, sortie programmée : `technical_score` tout allumé = **100** (22+16+10+18+12+12+10),
tout éteint = **0**. Les deux OK.

```text
technical                    [   0 , 100 ]
momentum                     [   0 , 100 ]
risk                         [   6 ,  72 ]   ← PLAFOND À 72 sur une échelle « 0-100 »
fundamental (proxy)          [  15 ,  90 ]   ← plafond à 90
fundamental (fond. réels)    [ 100 , 100 ]

compose()['global'], chemin /scan (poids 30/20/20/15, somme 85)
  fund proxy   [ 6 , 93 ]      fund TOP   [ 26 , 95 ]      fund PIRE  [ 5 , 74 ]
borne analytique si risk ≤ 72 : (30·100 + 20·100 + 20·100 + 15·72)/85 = 95,06 → 95
```

**La borne mesurée (95) et la borne analytique (95) coïncident : la composition
du score plafonne à 95/100, et la cause est unique — `risk_score` ne peut jamais
dépasser 72.**

**Mais le chiffre AFFICHÉ n'est pas plafonné**, et je le dis plutôt que de
publier un titre plus flatteur : `analysis.py:228` ajoute un correctif structurel
`struct_adj ∈ [−12, +10]` (physique + multi-horizons), donc `score = clamp(0, 100,
95 + 10) = 100`. **Le 100 est atteignable — jamais par la composition, seulement
par le bonus.** → **observation, pas dossier** (règle 492 : ne pas gonfler).

Deux gardes internes au passage, de la famille du 492 : dans
`regime_features.score_adjust`, le plafond `min(8, …)` **ne mord jamais** — la
composition maximale des termes positifs vaut **+7** (`+4` structure fractale,
`+3` efficience). Un garde mort de plus. **Nommé, non classé.**

## Le vrai résultat du lot — DOSSIER 495-A, RANG 1

En traçant `st_fund` (le sous-score fondamental) pour savoir s'il est peint, j'ai
trouvé qu'il **est lu sur le mauvais objet**.

```text
terminal.py:440     'st_fund': _sub.get('fundamental')   ← posé sur la ROW
vertex/engines/analysis.py                                ← le DÉTAIL ne le porte PAS
                                                            (il porte `sub.fundamental`)

lecteurs, tous sur un objet DÉTAIL :
  vertex/app/routes/strategy_os_api.py:56   detail.get('st_fund') or detail.get('fund_score')
  vertex/positions/recalculator.py:99       idem
  vertex/positions/thesis_health.py:37      idem
  vertex/ui/pages/analysis_page.py:432      d.st_fund ?? f.score   (d = t.detail)
```

**Vérifié à l'exécution** (scan DEMO en mémoire, `persist` redirigé) :

```text
detail.st_fund            = None        ← ce que le code lit
detail.sub.fundamental    = 83          ← la valeur, dans le MÊME objet
detail.st_timing          = None        ← n'est écrit NULLE PART dans le dépôt
detail.earnings_dte       = None        ← jamais posé sur le détail (seulement sur
                                          `out` d'options_pack, un autre objet)
detail.fund_score         = None        ← le repli du `or` n'existe nulle part
```

**Quatre entrées du paquet exécutif sont nulles en permanence** — score
fondamental, repli du score fondamental, échéance de catalyseur, score de timing.

### Ce que ça change à l'écran, mesuré par A/B

`/api/strategy/decision/<sym>` alimente le **badge de décision en tête
d'`/analysis`** (`analysis_page.py:327` : `const decision=(exec&&exec.final_decision)`).
J'ai rejoué les 20 titres du scan DEMO, une fois tels quels, une fois en
remplissant **la seule clé `st_fund`** :

```text
fundamental.score   null → 83 / 45 / 72 …        sur les 20 titres
unknowns            « fundamental » disparaît    20 / 20
DÉCISION AFFICHÉE   change                        4 / 20   (20 %)
    ACN  fund 75   REFUSER → ATTENDRE
    ALL  fund 78   REFUSER → ATTENDRE
    AOS  fund 64   REFUSER → ATTENDRE
    LNT  fund 65   REFUSER → ATTENDRE
```

**Le moteur exécutif refuse des titres parce qu'il croit ne pas connaître leur
score fondamental, alors que celui-ci est dans l'objet qu'il tient en main.**

**Aucune atténuation** : le champ `unknowns` du paquet exécutif — qui contient
littéralement « fundamental » sur 20 titres sur 20 — **n'est affiché nulle part**
sur `/analysis` (vérifié : aucun `exec.unknowns` dans le code servi). L'utilisateur
voit « REFUSER » et n'a **aucun moyen** de savoir que le moteur a décidé en
aveugle.

**Rang 1**, au critère du 486-A : un défaut **affiché**, **permanent**, qui
modifie une sortie d'aide à la décision, **sans rien qui l'atténue**.

**Ce que je ne dis pas** : les 20 % sont mesurés sur les **20 titres synthétiques
du scan DEMO**, pas sur l'univers réel — **c'est un taux de démonstration, pas
une fréquence de production**. Le **mécanisme**, lui, est certain et permanent :
la clé n'est écrite nulle part sur cet objet. Et la direction observée est
**restrictive** (REFUSER → ATTENDRE) : le défaut prive d'information, il ne rend
pas le terminal plus permissif.

## Le second contrôle — ce que mon instrument EXCLUAIT

J'ai trouvé `st_fund` en lisant **une ligne d'interface**. Cette méthode exclut
par construction tout autre champ lu sur le mauvais objet. Généralisation :
comparer les jeux de clés **réels** de la ROW et du DÉTAIL (mesurés à
l'exécution) et confronter chaque `detail.get('X')` du code serveur.
**Calibration** : positif `st_fund` (doit sortir), négatif `score` (présent des
deux côtés, ne doit pas sortir). Les deux OK.

Le détecteur rend **33 lectures** dont la clé est absente du détail réel. **Je
n'en publie pas 33** : ma regex accepte tout objet nommé `d`/`det`/`_d`/`detail`,
or dans `decision_memory`, `skyler_journal` et `skyler_sweep` ce `d` est un
**dict de décision**, pas le détail du scan. **Tri à la lecture** (règle 488) —
il reste **quatre** lectures certaines, toutes dans le paquet exécutif et ses
jumeaux `recalculator` / `thesis_health`, celles listées ci-dessus.

Le contrôle a donc fait son travail : il a **élargi le défaut de un champ à
quatre**, et il a **failli me faire publier vingt-neuf faux**.

## Trois faux résultats arrêtés avant publication

1. **Les 33 lectures mortes.** Publier la liste brute revenait à annoncer 33
   défauts là où il y en a quatre. Arrêté par la lecture.
2. **`dec.unknowns` à `analysis_page.py:798`.** J'allais écrire que le champ
   `unknowns` du paquet exécutif est affiché. **Il vient de `/api/decision/`,
   c'est-à-dire du `decision_stack`** — pas du moteur exécutif. **Vingt-troisième
   homonyme**, et exactement le piège qui a coûté le lot 491 en entier.
3. **J'allais ouvrir le navigateur sur `/analysis`.** La page fetche
   `/api/ticker/<sym>`, dont le serveur appelle `options_pack`, qui fait
   `yf.Ticker(sym)` **sans aucune garde DEMO** (`terminal.py:1526`). C'est une
   route **réseau sortant**, au même titre que `/options/<sym>`. Sonde annulée.

**Arrêtés avant publication : 65 → 68.**

## Le brief était incomplet — troisième fois

Sa liste « NE JAMAIS APPELER » cite `/api/analyst`, `/api/correlations`,
`/options/<sym>`, `/desc/<sym>` — **et omet `/api/ticker/<sym>`**, qui appelle
exactement le même `options_pack`. Après 490 et 492, **le brief se trompe ou
s'incomplète pour la troisième fois** : la règle « le brief est une source comme
une autre » se paie encore.

## Portée

- Le taux de **4/20** est mesuré sur le **scan DEMO** (20 titres synthétiques).
  **Non extrapolable.** Le mécanisme, lui, est établi par AST **et** par
  exécution.
- Les jeux de clés ROW / DÉTAIL sont mesurés **sur le détail DEMO**. Pour
  `st_fund`, `fund_score`, `st_timing` et `earnings_dte`, la conclusion ne dépend
  pas de la démo : elle est confirmée par l'AST de `analysis.py` et par
  l'absence de tout écrivain dans le dépôt.
- **`edge /100` n'est PAS mesuré** : il exige une série de prix et le moteur
  `quant_engine` complet. **Dette nommée** — la veine des barèmes est close **à
  un barème près**, et je le dis plutôt que d'annoncer une fermeture complète.
- Le plafond 95 de `compose()['global']` est **atteint** par la grille : la borne
  est exacte (règle 494), pas seulement une borne inférieure.
- `risk_score ≤ 72` et le garde mort `min(8, …)` sont **internes, non affichés** :
  nommés, non classés.
- **Aucun navigateur ouvert**, et la raison est mesurée, pas invoquée (voir le
  faux résultat n°3).

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties de script en
  chemin **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** à chaque banc ; scans DEMO **en mémoire** ;
  **aucune route réseau sortante appelée**.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, **aucun apparu, aucun
  disparu**. Quatre fichiers re-datés — `ai_enrichment`, `desk_data`,
  `weekly_snapshot` (passage de suite) et **`daily_prev`**, écrit par mes scans
  DEMO **en processus** : c'est le comportement attendu d'un scan, déclaré ici
  parce que la liste des SONDES ne l'attribuait qu'à un serveur DEMO. **Écart
  final AUCUN** après restauration.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

**Cinq lots sans nouveau dossier, puis celui-ci.** Et la leçon est celle que la
tranche répète depuis le 485 : **payer une dette nommée trouve autre chose**.
J'allais mesurer un barème ; le barème est sain (95 par composition, 100 à
l'écran) et c'est **le chemin pour y arriver** qui était cassé.

La feuille passe de **24 à 25 dossiers**, dont **quinze rang 1**.

Comptes séparés : résultats faux **arrêtés avant publication 68 (+3)** ; publiés
puis corrigés **11** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**
