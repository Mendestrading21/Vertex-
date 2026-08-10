# SKYLER LOT 493 — La famille « producteur constant » balayée sur tout le code serveur : elle ne rend RIEN de neuf — mais le balayage découvre un SECOND score /40, importé en production sous l'alias `ibkr`

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-493` (base : lot 492 fusionné,
`778ce801`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

## Le choix, et pourquoi

Le réveil offrait **(a)** clore proprement la veine des barèmes ou **(b)** rouvrir
la famille « valeur affichée dont le producteur est une constante » — celle qui a
donné **deux rangs 1 sur trois**.

**J'ai pris (b)**, et je dis pourquoi j'écarte (a) : le 492 a montré que les deux
barèmes les plus servis sont **sains ou mineurs**. Finir la veine serait du
rangement à rendement nul annoncé. **(a) reste une dette nommée**, chiffrée à
**un seul traçage pour trois cibles** (les trois `/100` d'`/opportunities`
partagent vraisemblablement l'échelle `opGrade` — hypothèse, non mesurée).

## L'instrument, et sa calibration qui a ÉCHOUÉ du premier coup

Détecteur AST sur tout le code serveur (`vertex/**` hors `ui/`, plus
`terminal.py`) : pour chaque clé de dict littéral, relever **tous** ses sites ;
une clé est **constante** si tous ses sites portent une constante **et** qu'elles
sont **égales**.

**Calibration écrite dans le code**, deux réponses connues :

```text
POSITIF  'rr'    → doit sortir constant  (dossier 442, rang 1, « rr constant à 3 »)
NÉGATIF  'score' → ne doit PAS sortir
```

**Premier passage : ÉCHEC.** `'rr'` est ressorti **non constant**, et le détecteur
s'est arrêté comme prévu. Diagnostic avant réécriture :

```text
'rr' a 12 sites dans 8 modules
  command.py · committee.py ×2 · quant_engine.py ×2 · options_lab.py ×3
  pivots.py · ml_calibration.py ×2       ← tous CALCULÉS
  analysis.py:262                        ← seul littéral 3.0
```

**J'agrégeais par NOM DE CLÉ sur tout le dépôt : c'est le piège de l'homonyme au
niveau du CHAMP.** Corrigé en groupant par **(fichier, clé)** — calibration
repassée : `('analysis.py','rr') → (3.0, 1 site)`, `('analysis.py','score') → None`.

## Le résultat : la veine ne rend rien de neuf

Après restriction — **valeurs numériques** seulement (une étiquette constante
comme `'à ÉVITER'` est un **libellé**, pas un défaut) et **hors des modules dont
le métier est de déclarer des constantes** (`strategy/config.py`,
`scanner/scan_budget.py`, profils) — il reste **onze** champs :

```text
long                   3        terminal.py:577            horizon de scan
fundamentals       86400        app/routes/system.py:168   TTL de cache
news                3600        app/routes/system.py:168   TTL de cache
SPY / AAPL / NVDA  600/230/140  data/demo.py               prix de DÉMO, par nature
Portefeuille        1.15        engines/evidence.py:189    poids de pondération
Risque               1.2        engines/evidence.py:189    poids de pondération
VOLATILITY_COMPRESSION 3        engines/skyler_core.py:273 table de points
max                   40        engines/scorecard.py:178   ← voir ci-dessous
rr                   3.0        engines/analysis.py:262    ← DOSSIER 442 CONNU, rang 1
```

**Dix sur onze sont légitimes** : des TTL, des prix de démo dans le module de
démo, des poids, une table de points. **Le onzième est le dossier déjà classé.**

**La famille est balayée sur l'intégralité du code serveur et ne produit AUCUN
défaut neuf.** C'est un résultat de bornage, et je le publie tel quel : la
question « combien d'autres `fundamentals_quality` ? » a une réponse mesurée —
**aucun, sous cette forme**.

## Ce que le balayage trouve et qu'il ne cherchait pas

`engines/scorecard.py:178` déclare `'total': total, 'max': 40`. **Un SECOND score
sur 40**, distinct de celui de `skyler_core` mesuré au 485.

Et il est bien vivant : `terminal.py:45` fait
`from vertex.engines import scorecard as **ibkr**`, puis l'appelle en production
à `:591` et `:1597` (`out['ibkr'] = ibkr.verdict(...)`, commenté
« VERDICT IBKR (/40 + niveau + timing) »).

**Vingtième récurrence du piège de l'homonyme, et d'un genre déjà connu (473,
l'alias d'import)** : un moteur nommé `scorecard` vit en production sous le nom
`ibkr`. **En 493 lots, la boucle n'avait jamais remarqué qu'il existe deux scores
/40 dans Vertex.**

Ses six composantes sont déclarées `Fondamentaux /8 · Technique /8 · Catalyseur /6
· Institutions /6 · Option Fit /6 · Asymétrie /6` — somme **40**, cohérente.

### Et je n'ai PAS réussi à établir son plafond

Mon banc a rendu « maximum 25/40 sur 288 combinaisons ». **Je ne le publie pas
comme un plafond**, parce que les composantes trahissent le banc :

```text
Fondamentaux 5/8   ← la branche « inconnu → neutre » (f8 = 5)
Option Fit   4/6   ← la branche « neutre » (of6 = 4)
```

**Mon `detail` fabriqué n'est pas lu là où je le crois** : le moteur retombe sur
ses neutres, donc le banc mesure **ce que rend une entrée non reconnue**, pas le
maximum. Exactement la leçon du 492 — *calibrer le banc sur sa propre validité*.
**Dette nommée : le plafond du second /40 reste à établir.**

## Le second contrôle — ce que l'instrument EXCLUT, et c'est grave

Mon détecteur ne voit que les **dicts littéraux** `{'clé': constante}`. Il ne voit
donc **ni** `out['clé'] = 5`, **ni** un `return 5`, **ni** un **argument par
défaut**.

Or le 492 a trouvé exactement cela : `base_conf = _num(d.get('confidence'), **55**)`.
**Mon recensement d'aujourd'hui aurait manqué la trouvaille du lot précédent.**

Le contrôle ne dit donc pas « la famille est vide » : il dit **« la famille, sous
la forme dict littéral, est vide »**. La restriction est nommée, et son coût en
faux négatifs est **réel et démontré par un cas**.

## Trois faux résultats arrêtés avant publication

1. **Le premier détecteur agrégeait par nom de clé** sur tout le dépôt — la
   calibration l'a arrêté avant toute lecture de résultats.
2. **Mon extraction cherchait la clé `score`** dans le verdict, qui expose
   `score40` : le balayage rendait « −1 », un non-résultat que j'aurais pu lire
   comme « rien trouvé ».
3. **Le banc du second /40 tombait dans les branches neutres** — « 25/40 »
   n'aurait pas été un plafond mais un artefact d'entrée non reconnue.

**Arrêtés avant publication : 59 → 62.**

## Portée

- Le balayage couvre **les dicts littéraux du code serveur**. Les autres formes
  d'affectation constante **échappent**, et le second contrôle en donne un cas.
- Le filtre « le nom de la clé apparaît dans les octets servis » est **large** :
  il retient une clé nommée `type` ou `note` pour de mauvaises raisons. Je ne
  l'ai pas resserré ; **j'ai trié à la lecture**, sur onze lignes, ce qui est
  possible à cette taille et ne le serait pas à mille.
- L'exclusion des modules de configuration est **mon jugement**, pas une mesure.
- Le second `/40` est **découvert**, pas mesuré : ni son plafond, ni s'il atteint
  une surface servie (`out['ibkr']` part dans `scan_state` — **non vérifié côté
  page**).
- **Aucun navigateur ouvert.**

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties en chemin
  **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** ; `scorecard` **sans écriture**, vérifié ;
  aucune route réseau sortante.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime : **un fichier est APPARU** — `desk_backup_20260810.json`,
  créé par le passage de suite au moment où la date a basculé. **Ce n'est pas une
  pollution de sonde : c'est le comportement caractérisé au lot 388** (« lancer
  la suite consomme le créneau de sauvegarde du jour »), et la conséquence
  mesurée au 362 (un restore rendrait l'état d'avant la première écriture du
  jour). **Je ne le supprime PAS** : effacer une sauvegarde du desk serait
  destructeur, l'invariant interdit d'y toucher à la main, et le fichier est
  **gitignoré** (`.gitignore:37`, vérifié) donc jamais commité. Vérifié aussi :
  son contenu est une **copie fidèle** du desk courant (`data` identique), et
  `desk_data.json` lui-même est **restauré à l'octet**. Compte runtime : **21 → 22**.
  Chaîne de sauvegarde : 07, 08, 09, 10 — cohérente avec `BACKUP_KEEP = 7`.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

**Troisième lot consécutif sans nouveau dossier classé.** Le 491 a nettoyé une
liste, le 492 a mesuré deux barèmes, le 493 balaie une famille entière — et les
trois concluent la même chose : **les veines ouvertes sont mesurées, et elles ne
rendent plus.**

Ce lot ajoute pourtant quelque chose que le bilan n°17 n'avait pas : la preuve
qu'**une famille peut être close par la mesure**. « Combien d'autres champs
constants ? » — **aucun sous cette forme**, sur tout le code serveur, calibration
à l'appui.

Et il laisse un objet neuf sur la table : **un second score /40 que 493 lots
n'avaient pas vu**, caché derrière un alias d'import.

Comptes séparés : résultats faux **arrêtés avant publication 62 (+3)** ; publiés
puis corrigés **10** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**
