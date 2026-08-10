# SKYLER LOT 509 — Le cas dégradé intermédiaire, en transversal : **AUCUN NOUVEAU DOSSIER**, trois candidats retirés sur atteignabilité, et un résultat qui vaut mieux — le **508-A est DEUX FOIS plus large que publié** (`_strat_tilt` est une copie quasi mot pour mot de `climate`), pendant que **le dépôt sait déjà dégrader honnêtement dans deux autres modules**

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-509` (base : lot 508 fusionné,
`bfdc6bad`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(b)**, la veine neuve née de la règle du 508 : *un gardien teste souvent le cas
qui marche*. La question, posée avant de toucher quoi que ce soit :

> combien de fonctions de synthèse rendent un verdict sur une entrée
> **PARTIELLE** (ni pleine, ni vide), et combien s'abstiennent honnêtement ?

## La réponse

```text
producteur                          PLEIN                PARTIEL             VIDE      marqueur
market_lens.climate (témoin 508)    score 93 FAVORABLE   score 46 NEUTRE     None      AUCUN
strategy_fit._strat_tilt            score 93             score 46            None      AUCUN
scorecard.verdict                   décision ACCEPTÉ     décision REFUSÉ     None      « insuffisant »
context.context_for                 dict 8 clés          dict 8 clés         None      « dimensions »
decide.decide                       SURVEILLER           TypeError           None      —
quant.scoring.compose               global 54 · grade C  TypeError           global 40 · grade D
```

**Ce lot ne produit aucun nouveau dossier.** Il produit deux choses qui valent
mieux, et trois retraits.

## 1. Le dossier 508-A est DEUX FOIS plus large que ce que j'ai publié

`strategy_fit._strat_tilt` est une **copie quasi mot pour mot** de
`market_lens.climate` :

```python
# market_lens.py:21              # strategy_fit.py:130
if not market: return None       if not mctx: return None
s = 35 if reg=='TREND' else 18 if reg=='NEUTRAL' else 6 if reg=='CHOP' else 14
s += 25 if roro=='RISK-ON' else 2 if roro=='RISK-OFF' else 12
a50 = br.get('above50')
s += round((a50 if a50 is not None else 50) / 100 * 25)
```

Mêmes poids, **même substitution `else 50`**, même garde limitée à l'absence
totale, **même 46 sur une entrée partielle, sans marqueur**. Le 508 n'en nommait
qu'une seule.

**Le rang du 508-A ne change pas** — ce qui le plafonnait à rang 3 est
l'atteignabilité non démontrée, et la duplication n'y change rien. **Sa portée,
elle, double.** Une correction qui ne toucherait que `market_lens` laisserait le
second exemplaire intact.

## 2. Le dépôt SAIT dégrader honnêtement — dans deux modules sur quatre

C'est le résultat que je n'attendais pas, et il est plus utile que le grief :

```text
scorecard.verdict   entrée partielle → décision « REFUSÉ », et la sortie porte
                    le mot « insuffisant » : elle refuse ET elle dit pourquoi.
context.context_for entrée partielle → sortie portant une clé « dimensions »,
                    qui expose ce sur quoi le classement a pu être établi.
```

**Deux sur quatre.** Ce n'est donc pas une limite d'architecture ni un arbitrage
assumé à l'échelle du produit : c'est une **incohérence entre modules**. La
« correction pressentie » que j'ai écrite au 508 n'est pas une invention — c'est
le comportement que `scorecard` applique déjà, deux répertoires plus loin.

## 3. Trois candidats retirés sur atteignabilité

### `decide()` plante sur `clé: None` — mais la forme n'arrive jamais

Le piège est réel et mesuré :

```text
{'score': None}.get('score', 0)  →  None, PAS 0
   (le défaut de .get ne s'applique QUE si la clé est ABSENTE)

decide({})                       →  None            ← s'abstient proprement
decide({'score': None, …})       →  TypeError       ← plante
```

`decide()` gère donc la forme que le système **n'utilise pas** et échoue sur
celle qu'il **pourrait** utiliser. Mais sur les vingt détails d'un scan DEMO
réel :

```text
score · trend · regime · setup_quality · confidence  →  20/20 présentes AVEC valeur
seule clé présente-à-None : `sector` (5 titres) — et decide() ne la lit pas
decide() sur les 20 détails réels : 20 verdicts · 0 abstention · 0 PLANTAGE
```

**Non atteint. Pas de dossier** (règle 507-A). Je note tout de même que les deux
sites d'appel relevés n'ont **aucun `try/except` en amont** : le jour où la forme
apparaîtrait, la TypeError remonterait.

### `compose({})` rend `global 40 · grade D · confidence 58` — sans aucune garde

Un grade **et un indice de confiance** calculés sur une entrée vide. Mais
`compose` n'a **qu'un seul appelant** :

```text
analysis.py:203   sc = scoring.compose(ind, fund=fund)
analysis.py:200   ind = {'above20': …, 'above50': …, … }   ← littéral, 12 clés TOUJOURS présentes
```

L'unique appelant construit un dictionnaire complet par construction.
**Non atteint. Pas de dossier.**

### Ma thèse « les synthèses fabriquent » était trop large

Le banc la contredit : deux producteurs sur quatre portent un marqueur.
**Retirée telle quelle**, remplacée par le constat d'incohérence ci-dessus.

**Arrêtés avant publication : 92 → 95.**

## Le contrôle négatif a ÉCHOUÉ, et je le dis

J'avais posé : *il faut au moins un producteur qui S'ABSTIENNE sur le partiel,
sinon mon instrument ne distingue pas « s'abstient » de « fabrique »*.

```text
producteurs qui s'abstiennent (rendent None) sur le PARTIEL : 0 / 4
```

**Aucun.** Mon banc n'a donc **aucun contre-exemple** sur cet axe-là : je ne peux
pas affirmer, mesure à l'appui, qu'une synthèse *pourrait* s'abstenir. Ce que je
peux affirmer, parce que le banc le montre sur un **autre** axe (CALIB 4 :
trois comportements distincts), c'est que **deux d'entre elles marquent leur
incomplétude**. C'est une honnêteté différente de l'abstention, et c'est celle
que le dépôt pratique.

Je publie l'échec plutôt que de le maquiller : la conclusion est plus faible que
celle que je visais.

## Portée — ce que ce lot NE dit PAS

- **Les entrées partielles sont fabriquées.** Le scan DEMO, lui, est réel — et
  c'est lui qui montre que la forme `clé: None` n'atteint pas `decide()`.
- **Six producteurs, pas tous.** Ils ont été recensés par la FORME (garde sur
  l'absence totale puis notation dimension par dimension), par regex sur
  `vertex/engines`, `vertex/portfolio`, `vertex/quant`, `vertex/options`. **Un
  producteur d'une autre forme m'échappe.**
- Deux des six n'ont pas pu être appelés sur les trois formes (TypeError) : le
  tableau porte 4 lignes complètes sur 6, et je le dis plutôt que de compter 6.
- **Aucun navigateur, aucun POST, aucune route réseau.** Tout est appel de
  moteurs en processus, plus un scan DEMO.
- Je n'ai **pas** vérifié si `_strat_tilt` atteint un écran. Sa duplication du
  508-A est établie sur le CODE ; sa visibilité ne l'est pas.

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

**Premier lot sans nouveau dossier depuis le 503.** Ce n'est pas un accident de
parcours : c'est la troisième fois d'affilée que l'atteignabilité tue mon
meilleur candidat — au 507 la bande d'IV, au 508 la jauge MM50, ici la TypeError
de `decide()`. **La règle 507-A, que j'ai écrite il y a deux lots, a maintenant
coûté trois dossiers.** Elle est chère, et elle a raison : chacun de ces trois
aurait été un rang 2 ou 3 fondé sur un état que le producteur n'atteint jamais.

Ce que ce lot rapporte à la place tient en une phrase : **le grief du 508 est
deux fois plus large, et sa correction existe déjà ailleurs dans le dépôt.** Un
lot qui élargit un dossier existant et lui fournit son précédent vaut mieux qu'un
lot qui en invente un faible.

Je note aussi, franchement, que **la veine se referme**. Cinq lots produit ont
donné 1, 2, 2, 3, 3 ; le sixième donne zéro. Continuer à chercher des défauts
d'affichage a maintenant un rendement mesurablement décroissant, et je le dis
plutôt que d'attendre le lot 512 pour l'admettre.

Feuille **inchangée : 31 dossiers · seize rang 1 · onze rang 2 · cinq rang 3** —
mais **508-A voit sa portée doubler** (deux modules au lieu d'un).

Dettes nommées restantes : **les 29 vues servies hors empreinte** ; **l'espion au
troisième niveau** (toujours déconseillé) ; **le compte des rangs relatifs
postérieurs au 480**. Et une dette **neuve** : *un producteur de synthèse d'une
autre forme que celle recensée ici m'échappe peut-être.*

Comptes séparés : résultats faux **arrêtés avant publication 95 (+3)** ; publiés
puis corrigés **13** ; interprétations retirées **3 → 4** (la thèse « les
synthèses fabriquent », trop large, remplacée par un constat d'incohérence).

**Dix bilans — n°9 à n°18 — attendent une réponse.**
