# SKYLER LOT 484 — Les 7 fractions que le 456 avait nommées sans les tracer : deux sont saines, et la carte de décision de `/analysis` affiche un score sur 40 dont 5 points sont inatteignables — les deux plus hauts niveaux de conviction ne peuvent JAMAIS être atteints

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-484` (base : lot 483 fusionné,
`bae6e6ac`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

## Pourquoi cette direction plutôt que l'autre

Le réveil proposait (a) chiffrer la dette 456+459 ou (b) tracer les 7 gabarits de
fraction que le 456 avait **nommés mais explicitement laissés « ni comptés, ni
conclus »**. J'ai pris **(b)**, et pas seulement parce qu'un devis de plus dans
une pile que personne n'a engagée n'apprend rien : parce que **le 456 avait
pré-classé trois des sept en « barèmes » — par LECTURE, sans les tracer**. Or la
leçon 481 dit qu'une restriction qui écarte des faux positifs fabrique des faux
négatifs. **Je trace donc les sept, y compris les trois écartés.** C'est
exactement là que la trouvaille se trouvait.

## Les deux contrôles

**Contrôle 1 — réponses connues, écrites dans le code du détecteur** : un site
que je sais SAIN (`options/environment.py`, `dimensions_known/dimensions_total`)
et un que je sais PLAFONNÉ (`strategy_os_api.py`, `list(detail)[:200]`). Les deux
retrouvés → instrument calibré, sortie programmée en cas d'échec.

**Contrôle 2 — un cas que l'instrument EXCLUT.** Mon instrument part des
**7 gabarits littéraux** ; le 456 avait lui-même nommé son angle mort : « une
fraction construite par un helper (`pct(a,b)`) ou par une déstructuration
échapperait — non quantifié ». Balayage des helpers (`pct(`, `frac`, `ratio`,
`return … + '/' + …`) sur les surfaces servies : les `pct()` trouvés rendent des
**pourcentages**, pas des fractions `A/B` ; le seul producteur de la forme `a/b`
est le gabarit G3, **déjà dans le périmètre**. **L'exclusion est justifiée cette
fois-ci**, et je borne : j'ai cherché quatre formes de helper, pas toutes.

## Les sept, tracés

| # | gabarit | site servi | producteur | verdict |
|---|---|---|---|---|
| G1 | `battu ${sm.beats}/${sm.total} trim.` | `analysis_page.py:705` | `analyst_deep.py:96-111` | fraction défendable, **moyenne fausse** |
| G2 | `${diag.ai.ok}/${diag.ai.total} analyses OK` | `vx-shell.js:209` | `ai/audit.py:29-34` | population saine, **dénominateur plafonné à 200** |
| G3 | `b.points/b.max` | `analysis_page.py:879` | `skyler_core.py:233-237` | **LA TROUVAILLE** |
| G4 | `p.v/p.max` | `options-structure.js:367-368` | `leapsScore()` même fichier | **SAIN — témoin positif** |
| G5 | `rating_mean/5` | `analysis_page.py:486` | `company.py:236` | échelle **sans sens déclaré** |
| G6 | `favorable points sur pts.length` | `options-structure.js:224` | même fonction | **SAIN — témoin positif** |
| G7 | `CALLS n · PUTS m / 1 max` | `portfolio_page.py:270` | même ligne | portée du « max » ambiguë |

### Les deux témoins positifs — sans eux, rien ne vaut

**G4** : `leapsScore` pousse cinq dimensions de maxima 30, 25, 20, 15, 10 —
**somme exactement 100**, conforme à sa propre docstring « score 0-100 » — et
**chaque maximum est atteint par la branche haute de son ternaire** (delta 0,70-0,90
→ 30 ; 6-18 mois → 25 ; OI ≥ 8 000 → 20 ; spread ≤ 3 % → 15 ; IV ≤ 45 → 10).
Barème dont le plafond est réellement atteignable.

**G6** : `favorable = pts.filter(p => p.pnl >= 0).length` sur `pts.length` — le
numérateur est **une compréhension filtrée du dénominateur lui-même**. Même forme
que les trois fractions saines du 456.

Un instrument qui rendrait « tout est plafonné » serait indistinguable d'un
instrument juste. Ces deux-là le distinguent.

## G3 — la carte de décision de `/analysis`

C'est l'un des trois « barèmes » que le 456 avait écartés sans tracer.

### Le bloc qui ne peut jamais marquer — établi par AST, pas par `grep`

Mon premier détecteur cherchait `block('nom', 0,` et rendait **huit** blocs figés
à zéro. **Faux** : sept d'entre eux ont un `block(nom, 0, …)` dans une *branche*
et un `block(nom, pts, …)` dans une autre. Refait par AST, en comptant les sites
d'appel par nom et en testant si **au moins un** porte une expression non nulle,
avec témoin de calibration (`technical_timing` DOIT ressortir « peut marquer ») :

```text
fundamentals_quality           1 site   peut_marquer=False   L237  ZERO LITTERAL
catalysts                      3 sites  peut_marquer=True
technical_timing               2 sites  peut_marquer=True    ← calibration OK
institutions_flow_anomalies    2 sites  peut_marquer=True
market_regime_sector           2 sites  peut_marquer=True
asymmetry_scenarios            2 sites  peut_marquer=True
options_quality                3 sites  peut_marquer=True
data_quality                   1 site   peut_marquer=True
```

**Un seul bloc, `fundamentals_quality`, appelé une fois, avec le littéral `0`,
hors de toute condition** — et son statut est `'INSUFFICIENT'`, également en dur.

### Ce que cela fait au dénominateur

```text
poids du profil V2 (vertex_strategy_v2.json:281 sq.)
  fundamentals_quality 5 · catalysts 5 · technical_timing 6
  institutions_flow_anomalies 4 · market_regime_sector 4
  asymmetry_scenarios 6 · options_quality 6 · data_quality 4
  SOMME = 40      dénominateur écrit en dur (skyler_core.py:339) = 40
  points INATTEIGNABLES = 5      →  score maximal réel = 35 / 40
```

### Ce que cela fait aux niveaux de conviction — le vrai préjudice

```text
conviction_levels (profil V2)      S_PLUS score_min 36 · S 32 · A 28 · B 24
plafond réel du score                                     35
  → S_PLUS exige 36 : INATTEIGNABLE par arithmétique
skyler_core.py:333-334
  if insufficient and level in ('S_PLUS','S'): level = 'A'
  fundamentals_quality est TOUJOURS 'INSUFFICIENT'
  → `insufficient` n'est JAMAIS vide → S ET S_PLUS sont inatteignables,
    quel que soit le score, pour TOUS les symboles
```

**Deux des quatre niveaux de conviction de la Constitution — ceux qui portent les
plafonds d'allocation 7-10 % et 10-15 % — ne peuvent être atteints par aucun
titre.**

### Et rien ne le dit à l'écran — vérifié dans les octets servis

`GET /analysis/AAPL` = **75 216 octets**, et dedans :

```text
titre « Score /40 par blocs de la Constitution V2 »   PRESENT   (analysis_page.py:127)
total  (sc.total ?? '—') + '/40'                      PRESENT   (:888)
puce   b.points + '/' + b.max                         PRESENT   (:879)
libellé « Fondamentaux »                              PRESENT   (:873)
insufficient_blocks lu par la page                    ABSENT
mention d'un plafond de NIVEAU                        ABSENT
```

**Un faux positif arrêté ici même** : ma première sonde cherchait le mot
`plafonn` et le trouvait — mais l'unique occurrence des octets servis est
`d.capped_by_gate ? ' · plafonnée par ' + …`, **le plafond de HARD GATE, pas
celui des blocs insuffisants**. Matcher un mot n'est pas matcher la chose
(leçon 466). **Arrêté avant publication 48 → 49.**

Et `insufficient_blocks` — le champ qui expliquerait tout — **est bien produit**
(`skyler_core.py:340`) et **lu par trois moteurs** (`red_team.py:126`,
`skyler_sweep.py:62`, `decision_memory.py:124`) : **par aucune surface servie.**
La donnée existe, le chemin vers l'écran n'existe pas.

### Ce qui atténue, et que je dis

La puce **« Fondamentaux 0/5 » est bel et bien affichée**, en `vx-muted`, avec
`title` = « contexte fondamental non branché — 0 point, jamais estimé ». C'est
une information **co-visible et honnête** sur le bloc. Elle ne dit rien du
dénominateur global, et **rien du tout** du plafonnement des niveaux.

### Classement — deux défauts distincts, critères absolus (règle 480)

**(A) Les niveaux S et S+ sont inatteignables en silence → rang 1.**
(a) servi — `niveau ' + esc(d.level)` est dans les 75 216 octets ; (b) la
conséquence porte sur une **décision** — deux niveaux sur quatre, avec leurs
bandes d'allocation, sont hors d'atteinte pour tout titre ; (c) **aucune
information co-visible** — le seul « plafonné » de la page désigne autre chose,
et le champ explicatif n'atteint pas l'écran. Aucune comparaison à un autre
dossier n'entre dans ce rang.

**(B) « Score /40 » dont le plafond est 35 → rang 2.**
Mêmes critères (a) et (b), mais **(c) tombe** : la puce « Fondamentaux 0/5 » est
co-visible. C'est exactement la mécanique qui a maintenu le 456 (i) au rang 2 —
une note honnête à côté, muette sur le plafond.

## Les trois autres, tracés et non gonflés

**G1 — la moyenne, pas la fraction.** `analyst_deep.py` incrémente `total` pour
**tout** trimestre publié, mais n'ajoute à `acc` que si `surp is not None`, puis
rend `avg = round(acc / total, 1)`. **Une somme de surprises CONNUES divisée par
TOUS les trimestres** : dès qu'une surprise manque, la moyenne servie
(`· moy. +X %`, `analysis_page.py:705`) est **diluée vers zéro**. La fraction
`beats/total`, elle, est défendable — un trimestre sans surprise connue n'est pas
un « battu ». **Accessibilité NON établie** : il faut un trimestre avec BPA réalisé
et `Surprise(%)` absent, et je ne peux pas l'établir sans réseau sortant. → **rang 3**,
et c'est ce troisième critère qui l'y maintient.

**G2 — un dénominateur qui cesse de croître.** `AIAudit` est un
`deque(maxlen=200)` ; `total = len(entries)` est donc **une fenêtre glissante de
200**, pas un compte de vie. « 45/200 analyses OK » se lit comme un cumul.
Coïncidence notable : **le même 200 que le plafond du 456**, sans lien de cause.
Numérateur et dénominateur viennent de la **même liste** — la fraction est juste,
c'est son **référent** qui est implicite. → **observation**, pas de rang posé.

**G5 — une échelle sans sens déclaré.** `rating_mean` est
`info.get('recommendationMean')` (`company.py:236`), affiché `(3,2/5)`. **Le dépôt
n'encode NULLE PART le sens de cette échelle** — trois occurrences en tout, aucune
comparaison, aucun seuil, aucun commentaire. Je **ne** conclus **pas** « l'échelle
est inversée » : je n'ai aucune source dans le dépôt pour l'affirmer, et
l'affirmer sans preuve serait exactement ce que la boucle s'interdit. Ce que
j'établis : **une fraction « x/5 » se lit spontanément « plus haut, mieux », et
rien dans le produit ne confirme ni n'infirme ce sens.** Le libellé traduit
juste à côté (« Achat », « Conserver ») porte la direction ; le nombre, non.
→ **observation**, à trancher par qui connaît la source.

**G7 — la portée du « max ».** `CALLS ${…} · PUTS ${…} / 1 max` est **une seule
chaîne**. La garde qui l'accompagne est `opts.filter(t => t.type === 'PUT').length > 1` :
le « 1 max » ne concerne **que les PUTS**. Affiché « CALLS 2 · PUTS 0 / 1 max », il
se lit comme s'appliquant à l'ensemble. → **observation** d'ambiguïté de portée.

## Mutualisation — cherchée, partiellement trouvée

Deux des trois plafonds (G2 `maxlen=200`, G3 `fundamentals_quality`) sont des
**bornes de construction jamais énoncées à l'écran** — même genre que le
`[:200]` du 456. Mais **aucun site commun, aucun correctif commun** :
`ai/audit.py`, `skyler_core.py`, `strategy_os_api.py`. Trois fichiers, trois
décisions indépendantes. **La famille est réelle, la mutualisation ne l'est pas** —
et je le dis plutôt que de proposer un correctif unique qui n'existe pas
(leçon 483 : la parenté de famille n'est pas une parenté de site).

## Portée

- **Aucun banc sur `skyler_core`** : le blocage de S/S+ est établi par **lecture
  de deux lignes** (`:237` le bloc figé, `:333-334` la règle de rabattement) et
  par **AST** pour l'unicité du site d'appel. Je n'ai pas exécuté `decide()` sur
  un paquet fabriqué — ce serait le banc qui manque, et il monterait la preuve
  d'un cran.
- Le calcul « 5 points inatteignables » vaut pour le **profil V2** ; je n'ai
  trouvé **qu'un seul fichier de profil** portant `skyler_score.blocks`.
- **Accessibilité non établie pour G1** (il faut une surprise manquante), et je
  n'ai **pas** vérifié la fréquence réelle des trimestres sans `Surprise(%)`.
- **Je n'affirme rien sur le sens de `recommendationMean`** — le dépôt est muet.
- Le balayage des helpers du contrôle 2 couvre **quatre formes**, pas toutes.
- **Aucun navigateur ouvert** : la présence à l'écran est établie sur les octets
  servis de `/analysis/AAPL`, pas sur un rendu peint — et la leçon 482 rappelle
  qu'un littéral servi peut n'être jamais peint. Ici la carte est le cœur de la
  page, mais **je ne l'ai pas vue**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié**. Pages en **GET**. **`/api/skyler/`,
  `/api/analyst/`, `/api/correlations/`, `/options/` et `/desc/` NON appelées.**
  Aucun écrivain appelé.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Le 483 avait clos la liste d'attente en montrant qu'elle ne contenait presque
rien. Ce lot rouvre le produit et **y trouve un défaut de rang 1 en une seule
séance** — dans un endroit que le 456 avait balayé soixante-douze lots plus tôt
et écarté d'une ligne : « barèmes : x sur un maximum, pas une population ».

**Le fait de méthode est là, et il est le prolongement direct de la leçon 481 :**
*un lot qui écarte une catégorie « par nature » sans la tracer ne l'a pas
mesurée — il l'a supposée.* Le 456 a eu raison sur deux des trois barèmes
(G4 et G5 ne cachent pas de plafond faux) et **tort sur le troisième**, qui
portait le défaut le plus grave trouvé depuis longtemps. Un tiers d'erreur sur
une catégorie écartée d'une phrase.

Comptes séparés : résultats faux **arrêtés avant publication 49 (+1)** ; publiés
puis corrigés **8** ; interprétations retirées **3**.

**Huit bilans — n°9 à n°16 — attendent une réponse.**
