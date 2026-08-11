# SKYLER LOT 516 — Recensement : **457 phrases calculées, 75 atteignent l'écran, 8 portent un nombre construit.** Et une correction du 514 : la liste est **coupée à cinq**, si bien que la phrase « top X % » que j'avais montrée est **évincée dans 2 cas sur 2** sur données réelles

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-516` (base : lot 515 fusionné,
`fb43ea7c`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(a)** — recommandée deux fois, jamais prise. Le 514 a rendu le seul dossier
**visible** des cinq derniers lots productifs, par un chemin précis : une phrase
de moteur portant un **nombre construit**, transportée par la charge utile d'une
route, peinte par la page. La question transversale n'avait jamais été posée :
**combien de phrases calculées atteignent l'écran ?**

Crible par **AST**, pas par motif textuel — la leçon 515-A, apprise à mes dépens.

## Le recensement

```text
phrases françaises interpolées dans les sources Python      457
   ATTEIGNENT l'écran                                        75   (16 %)
      via les OCTETS SERVIS                                   7
      via la CHARGE d'une route appelée                      68
   dont porteuses d'un NOMBRE CONSTRUIT                       8
```

**Le chemin dominant n'est pas la page, c'est la charge utile** : 68 des 75 y
transitent. C'est exactement la voie par laquelle le 514-A est devenu visible, et
elle est **dix fois plus large** que le rendu serveur direct.

Les 8 phrases à nombre construit qui atteignent l'écran :

```text
decide.py:45            « Setup de qualité — marge vers la résistance ({round(sq)}/100) »
decide.py:51            « Momentum sain (RSI {round(rsi)}) »
evidence.py:86          « Sous-performe le marché (force relative {int(rs)}) »
evidence.py:127         « Fondamentaux solides vs secteur (note {int(fs)}) »
evidence.py:129         « Fondamentaux fragiles vs secteur (note {int(fs)}) »
regime_features.py:164  « désordre élevé (entropie %.0f%%) … »
dealer_synthesis.py:94  « résultats dans %d j »
weekly.py:113           « force relative %d (bat le SPY) »
```

**Aucune n'est un dossier**, et je le dis plutôt que d'en fabriquer un. Trois
utilisent `int()` — une **troncature**, pas un arrondi : une note de 74,9
s'affiche « note 74 ». L'écart est **borné à un point sur cent** et va toujours
dans le même sens. C'est du même genre que le libellé de durée du 515 :
**une convention d'affichage, pas une destruction d'information** (règle 515-C).
Les cinq autres arrondissent correctement.

## La correction du 514 — la coupe à cinq

`decision_stack._result` fait :

```python
pros = [e['text'] for e in committee.get('positive', [])][:5]
cons = [e['text'] for e in committee.get('negative', [])][:5]
```

**La liste est coupée à cinq.** Le 514 a mesuré sur une carte de 517 titres
**fabriquée en mémoire**, dont les titres n'avaient que quelques facteurs
concurrents : la phrase transversale y passait. Sur le **scan réel** :

```text
titres scannés                                20
titres où la phrase transversale est PRODUITE  5
titres où elle SURVIT à la coupe               2      → 40 %

ABT    retardataire   SURVIT    « Parmi les plus faibles de l'univers (bas 5%) »
AKAM   retardataire   SURVIT    « … (bas 12%) »
ALGN   retardataire   ÉVINCÉE
ACN    leader         ÉVINCÉE   « Parmi les meilleurs de l'univers (top 2%) »
AFL    leader         ÉVINCÉE   « … (top 8%) »
```

**Les deux cas « leader » sont évincés — deux sur deux.** La forme qui atteint
réellement l'écran est **« bas X % », dans les facteurs NÉGATIFS**, pas
« top X % » dans les facteurs positifs.

**Ce que cela change au 514-A** : le dossier **tient** — la phrase atteint bien
l'écran, et à l'échelle de production elle y écrira **« bas 0 % »**. Mais
**l'illustration que j'ai publiée était la mauvaise** : j'ai montré « top 0 % »
sous « Facteurs positifs », alors que c'est précisément la forme que les données
réelles évincent. Le rang 2 reste justifié ; la vitrine était fausse.

**Publiés puis corrigés : 14 → 15.**

## Le second contrôle — mon recensement rate son propre cas de référence

Le crible retient une phrase quand son **plus long fragment littéral** ressemble
à de la prose. Or `context._headline` assemble sa sortie par
`' · '.join(parts)`, chaque morceau valant `'Top %d%% de l'univers'`. Le plus long
fragment y est **« de l'univers » — 13 caractères**, sous le seuil.

> **Mon propre dossier 513-A échappe à mon propre recensement.**

```text
interpolées retenues (fragment long, prose)      457
interpolées ÉCARTÉES pour fragment TROP COURT     98   ← dont le 513-A
interpolées écartées comme balisage              227
```

**Le « 8 phrases à nombre construit » est donc une BORNE BASSE**, et je publie la
borne plutôt que le chiffre seul.

Troisième angle mort, le français **assemblé en JavaScript** dans les octets
servis : mon motif en compte 336 (147 gabarits `` `…${x}…` `` + 189
concaténations). **Mais ce chiffre est mal discriminé** — les échantillons
montrent surtout du balisage à libellés français (`<span class="k">${k}</span>`),
pas des phrases calculées. Je le donne comme **majorant grossier**, pas comme
mesure. Le mesurer proprement demanderait un analyseur JS, que je n'ai pas
construit.

## Deux arrêts avant publication

1. **La calibration a échoué deux fois, et c'était mon banc.** Premier jet :
   j'interrogeais `/api/decision/AAPL` — or **AAPL n'est pas dans le scan DÉMO**
   (`UNIVERSE[:20]` donne A, ABBV, ABNB, ABT, ACN…). La route rendait
   `DATA_INSUFFICIENT` sans contexte. Famille 512-A, réapprise.
2. **Deuxième jet : je visais le seul meilleur titre (ACN).** Sa phrase est
   **évincée** — j'allais conclure « la phrase n'atteint jamais l'écran », c'est-
   à-dire réfuter le 514-A à tort. En interrogeant **les 20 titres**, deux cas
   survivent. **Viser un seul sujet, c'était mesurer un tirage, pas une règle.**

**Arrêtés avant publication : 110 → 112.**

## Ce que le dépôt fait bien, mesuré

- Sur les 8 phrases à nombre construit atteignant l'écran, **cinq arrondissent
  correctement** ; les trois `int()` restent à un point près.
- La coupe à cinq n'est pas un défaut : c'est une **hygiène d'affichage**
  délibérée (ne pas noyer l'utilisateur). Elle a simplement pour effet de
  hiérarchiser, et la phrase transversale a un poids (55) qui la place derrière
  d'autres.
- **382 phrases sur 457 n'atteignent jamais l'écran** — mais ce n'est pas un
  gâchis : beaucoup sont des messages d'erreur, de journal ou de diagnostic, qui
  n'ont pas vocation à être peints.

## Portée — ce que ce lot NE dit PAS

- **« Atteint l'écran » signifie ici : le fragment littéral est présent dans les
  octets servis OU dans la charge utile d'une route appelée.** Qu'un octet reçu
  soit peint est une question distincte — le 514 l'a tranchée pour un cas, pas
  pour les 75.
- Le crible est **Python** et **littéral**. Il rate les phrases assemblées
  (98 écartées, dont mon propre 513-A) et tout le JavaScript.
- **Mesuré sur le scan DÉMO (20 titres).** Les taux de survie à la coupe
  dépendent du nombre de facteurs concurrents, donc des données réelles.
- **Aucun navigateur, aucun POST, aucune route interdite appelée.** 61 routes
  sûres interrogées, dont `/api/decision/<sym>` pour les 20 titres scannés.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu**.
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** avant tout import, dans les trois bancs.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La série des rangs devient **1, 2, 2, 3, 3, 0, 0, 4, 4, 4, 2, 0, 0**.

Pas de dossier neuf — mais ce lot fait deux choses qu'un dossier neuf ne ferait
pas : il **cartographie** la voie par laquelle un défaut devient visible (la
charge utile, 68 cas sur 75, dix fois plus que le rendu serveur), et il
**corrige la vitrine du 514** sur données réelles.

L'enseignement de méthode est le même que celui du 515, appliqué à un autre
étage : **un instrument doit retrouver son propre cas de référence.** Le 514
avait échoué là-dessus et je l'avais réparé ; le 516 échoue à son tour — mon
recensement ne voit pas le 513-A — et cette fois je ne répare pas, je **publie la
borne**, parce que réparer demanderait de suivre les phrases assemblées, ce qui
est un autre instrument.

Feuille **inchangée : 35 dossiers · seize rang 1 · douze rang 2 · cinq rang 3 ·
trois rang 4**.

Dettes nommées restantes : **suivre les phrases ASSEMBLÉES** (dette neuve — 98
candidates, dont le 513-A) ; **le français construit en JavaScript** (dette
neuve, majorant grossier 336) ; **mesurer le contenu des 23 routes non
appelées** ; **les 29 vues servies hors empreinte** ; **la condition `k ≤ 5` sur
un scan réel** ; **recribler les chiffres publiés par motif textuel** ; **le
compte des rangs relatifs postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 112 (+2)** ;
**publiés puis corrigés 15 (+1)** ; interprétations retirées **4**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
