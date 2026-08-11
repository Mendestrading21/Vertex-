# SKYLER LOT 444 — 235 phrases écrites par le serveur, jamais recensées depuis le 427 — et la première fois qu'un résultat faux m'a échappé jusqu'au rapport publié

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-444` (base : lot 443 fusionné,
dc449df)

Vingt-sixième lot de la veine. Le 443 avait découvert qu'une valeur peut
atteindre l'écran **fondue dans une phrase composée au serveur**, et avait dit
n'avoir pas quantifié la classe. Ce lot la quantifie — et **retire l'exemple sur
lequel le 443 fondait sa règle**.

**Aucun code, aucun gardien, aucun test.**

## L'instrument : recensement par AST, pas par motif

Les 299 fichiers Python de `vertex/` parcourus par `ast` ; toute f-string ou
`%`-format **qui interpole au moins une valeur** et qui est rangée sous un nom de
champ (valeur de dict littéral, affectation à un nom, mot-clé d'appel) est
retenue.

```text
fichiers analysés                                       299
noms de champs recevant une phrase composée              74
phrases composées au total                              235
```

**Témoin positif** : `invalidation` (`committee.py:133`) — la phrase du 443 —
ressort bien du recensement.

### Ce que je ne compte pas, et pourquoi

Trente-six des 74 noms sont **trop génériques pour être distingués dans du JS** :
`note` (31 phrases), `error` (16), `src` (7), `label` (6), `key` (6), `lbl` (5),
`when` (5), `content`, `title`, `body`… Chercher `.note` dans 3,8 Mo de code
servi rend du bruit — c'est la leçon du 437 (« un receveur d'une ou deux lettres
est indistinguable du Chart.js minifié »), généralisée aux **noms communs**.

**125 phrases sur 235 sont donc non concluantes. Je les nomme et je ne les
compte pas** — pas de total contaminé (règle 437).

## Sur le périmètre concluant : 38 champs, 110 phrases, 13 atteignent un écran

```text
champ            phrases   écrans   où
reason                 7        4   /opportunities, /portfolio, /journal, /analysis param.
detail                 7        4   /markets, /portfolio, /system, /analysis param.
source                 4        4   /markets, /opportunities, /portfolio, /system
narrative              1        4   /, /portfolio, /journal, /analysis param.
basis                 28        3   /portfolio, /journal, /analysis param.
action                 6        3   /portfolio, /system, /analysis param.
impact                 1        3   /portfolio, /system, /analysis param.
close                  1        2   /markets, /analysis param.
invalidation           1        2   /opportunities, /analysis param.        ← voir plus bas
summary                6        1   /analysis param.
question               3        1   /portfolio
volume                 1        1   /analysis param.
spread_pct             1        1   /opportunities

à nom distinctif mais lus par AUCUN écran : 25 champs
  logic(5) · reading(4) · page_label(4) · prompt(3) · age_seconds(3) · pm_html(2)
  verdict_global(2) · main_reason(2) · alert(2) · exec_summary · objection · synth …
```

## La correction : mon lot 443 s'est trompé, deux fois, sur la même ligne

Le 443 publie : *« `invalidation` est lu par **cinq écrans**, **12 fois** sur la
route `/analysis` à paramètre »*, et s'en sert pour établir que `stop_type`
atteint l'écran à travers la phrase du comité.

**Les deux moitiés sont fausses.**

**(1) Le « cinq » comptait des mots français, pas des lectures de champ.**

```text
page                jeton nu   LECTURE de champ (.invalidation / ['invalidation'])
/                          1                  0     « invalidation:inval » — une ÉCRITURE
/opportunities             2                  2
/portfolio                 9                  0     « Cassée — invalidation atteinte », etc.
/journal                   3                  0     « raison + invalidation = plan »
/analysis param.          12                  4     dont « Stop (invalidation sous-jacent) »
```

Les neuf occurrences de `/portfolio` sont des **libellés d'interface** ; celles de
`/journal`, des phrases de discipline. **Deux écrans lisent un champ, pas cinq.**

**(2) Et ces deux-là ne lisent pas la phrase du comité.**

```python
# skyler_core.py:433 et :627
'invalidation': stop,          # un NOMBRE
```

```javascript
// opportunities_page.py:669 — tableau « Classement Skyler »
<td data-label="Invalidation" class="vx-num">${r.invalidation!=null?VX.fmt.num(r.invalidation,2):'—'}</td>
```

Le champ lu est le **niveau numérique de Skyler**, formaté par `VX.fmt.num` ;
même chose pour `dec.invalidation` sur la page à symbole. La phrase
« clôture sous $95.0 (structure) » du comité **n'est lue par aucun écran sous ce
nom**.

**Troisième occurrence du piège « un nom de champ, plusieurs payloads »** — après
`scan` (438) et `.decision` (441). Les deux premières ont été arrêtées avant
publication. **Celle-ci ne l'a pas été : c'est la première fois qu'un résultat
faux passe dans un rapport fusionné.**

Le compte des résultats faux **arrêtés avant publication** reste donc à **18** ;
celui des résultats faux **publiés puis corrigés** passe de 0 à **1**. Les deux
comptes doivent rester séparés — ils ne mesurent pas la même chose.

**Conséquence sur le 443** : son verdict « `stop_type` atteint un écran » est
**retiré**. `stop_type` retourne dans la colonne « non observé ». Le reste du 443
— les douze champs du plan, les trois R:R, la correction du 442 — n'est pas
touché : aucune de ces mesures ne dépendait de cette ligne.

## La règle du 443 survit, avec un vrai exemple à la place du faux

Une valeur **peut** bien atteindre l'écran fondue dans une phrase serveur. La
preuve n'est pas `invalidation`, c'est **`basis`** :

```text
28 phrases composées   decision_memory (16) · knowledge_graph (6) · skyler_core (5) · red_team (1)
lu par                 /portfolio · /journal · /analysis à paramètre  (+ performance_page)
```

Et ces phrases **portent des chiffres** :

```text
« corrélation des résidus de marché %s/%s = %.2f sur %d points … »   knowledge_graph:169
« %d contradiction(s) tracée(s) — −0,20 chacune »                    skyler_core:101
« bloc data_quality %d/4 du score »                                  skyler_core:99
« analyse de perturbation : %d/%d perturbation(s) laissent la … »    skyler_core:87
```

### Où elles s'affichent — et pourquoi rien ne les avait vues

```javascript
analysis_page.py:879    title="${esc(b.basis||'')}"     ← infobulle d'un badge de score
portfolio_page.py:847   … + esc(x.basis||'') …          ← texte
performance_page.py     title="${esc(p.basis||'')}"     ← ×3, infobulles
```

**L'essentiel de cette classe vit dans des attributs `title=`** — visible au
survol seulement. Ni un recensement du **texte visible**, ni celui des
**littéraux du client** (427→441) ne pouvait les atteindre : elles sont écrites en
Python, transportées en JSON, et rendues dans un attribut.

## Classement

**Aucun défaut de produit nouveau.** Le lot rend trois choses :

1. une **correction publiée** d'un chiffre et d'un verdict de mon propre lot 443 ;
2. la **quantification** de la classe que le 443 avait ouverte : 235 phrases
   composées au serveur, dont **110 mesurables** et **13 champs qui atteignent un
   écran** ;
3. l'observation que cette classe s'affiche surtout en **infobulles**, ce qui
   explique qu'aucun recensement de la boucle ne l'ait jamais croisée.

Les 110 phrases concluantes sont **recensées, non ouvertes** : je n'ai vérifié
**aucune** de leurs affirmations. C'est le vivier du lot suivant.

## Portée

Le recensement ne voit que ce qui est **rangé sous un nom** au point de
composition. Une phrase composée puis passée directement en argument
(`f(x, f"…{v}…")`) sans nom lui échappe — **non quantifié**.

Les **125 phrases à nom générique** sont hors mesure, pas hors existence : elles
peuvent parfaitement atteindre un écran, je ne sais pas le dire.

Le comptage des écrans porte sur les **octets servis** et sur les formes
`.champ` et `['champ']`. Une lecture par déstructuration ou par variable
intermédiaire lui échappe — même limite qu'au 436.

Je n'ai **ouvert aucune** des 110 phrases : leur véracité n'est pas mesurée.
**Aucun navigateur ouvert** ; les infobulles n'ont pas été observées au survol.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant chaque mesure ;
  scripts du scratchpad avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de bump.
  SW : `td-shell-v187`. Routes appelées en **GET** ; `persist` redirigé vers un
  répertoire temporaire ; analyse `ast` en lecture pure.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Quarante-septième lot court. Séquence : **441 ✗ · 442 ✓ · 443 ✓ · 444 ✗ (mais
il corrige le 443)**.

Trois lots d'affilée ont trouvé quelque chose ; celui-ci trouve surtout que
**j'avais tort la veille**. C'est le premier résultat faux de la boucle à être
passé dans un rapport fusionné, et la cause est un piège que j'avais moi-même
nommé deux fois — *un nom de champ peut désigner plusieurs payloads*. Le connaître
n'a pas suffi : il fallait l'appliquer, et j'avais compté un **jeton nu** là où il
fallait compter une **lecture de champ**.

La classe ouverte au 443 est réelle et large — 235 phrases, dont aucune n'a
jamais été vérifiée. Ce que ce lot livre, c'est la carte ; l'ouverture reste à
faire.

**Cinq bilans — n°9, n°10, n°11, n°12 et n°13 — attendent une réponse.**
