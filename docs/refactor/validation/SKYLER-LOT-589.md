# SKYLER — LOT 589

## Ce que le lot établit

**L'angle mort annoncé n'existait pas à cette taille.** Le 588 avait déclaré
« 226 comparaisons à gauche non nommable, écartées par les deux relevés » et le
brief en avait fait « le plus gros angle mort de la série, plus que les 192
seuils nus, plus que les 108 à droite variable ».

**Mesuré : 28 sites de produit. Le plus PETIT des trois.**

Et **deux d'entre eux avaient déjà été lus et publiés** par les lots 583 et 584.

## Le nombre 226, décomposé — mesuré, pas deviné

Le compteur du 588 était un `res.sansNom++` **sans position**. Un nombre sans
position ne peut être ni dédupliqué (580-C) ni filtré des tiers (587-C). J'ai
donc relevé chaque site avec sa position et reproduit exactement ce que « 226 »
comptait :

| ce qui est compté | sites |
| --- | --- |
| bruts, gauche non nommable, **toute** droite | **318** |
| bruts, gauche non nommable, **droite non littérale** | **226** ← le chiffre du 588 |
| après déduplication (580-C), toute droite | **71** |
| **après retrait des tiers (587-C) — de PRODUIT** | **28** |
| de produit, droite non littérale | **16** |

**Le « 226 » du 588 était un nombre brut** : un fichier statique y comptait huit
fois, bibliothèques tierces incluses, et il était restreint aux droites non
littérales sans que le rapport le dise.

**Publiés puis corrigés : 39 → 40.**

**La part tierce de ces comparaisons est de 43 sur 71, soit 61 %** — la
proportion la plus élevée de toute la série. C'est logique : une expression
composée à gauche est la signature d'un code minifié.

## Les pièges, écrits avant la mesure (564), vérifiés comme le reste (568-B)

| piège | verdict |
| --- | --- |
| **Attente principale** — la plupart sont de l'arithmétique de dessin | **RÉFUTÉE** : géométrie **5 sur 28 (18 %)** |
| **Contre-piège 1 (588-C)** — « ce dépôt juge plus qu'il ne dessine » | **CONFIRMÉ une troisième fois** |
| **Contre-piège 2 (588-A)** — publier l'histogramme avant de classer | **respecté** : formes de gauche publiées d'abord, **0 non tranché** au final |
| **Contre-piège 3 (587-A)** — recalculer le 226 | **A PAYÉ** : le nombre était brut, le vrai est 28 |

## Les 28, lues par famille

| famille | sites | part |
| --- | --- | --- |
| **DURÉE / ÂGE** | **10** | 36 % |
| **COMPARAISON DE DOMAINE** | **8** | 29 % |
| **COMPTE / SIGNE** | **5** | 18 % |
| **GÉOMÉTRIE** | **5** | 18 % |
| non tranché | **0** | — |

Les 28 ont été **affichées en entier** avant tout classement. Elles tiennent sur
une page : il n'y avait aucune raison d'en résumer une seule.

### Les 10 « durée / âge »

```javascript
(Date.now()/1000-(s.received_ts||0))<=6*3600        // /analysis — déjà publié (583/584)
((new Date(t.exp)-Date.now())/86400000)<=7          // /portfolio — échéance ≤ 7 j (×2)
(now-(base.ts||0))>43200000                         // /portfolio — déjà publié (584)
Date.now() - hit.ts <  ttl                          // vx-core — cache (×2)
Date.now() - hit.ts >= ttl                          // vx-core — la borne inverse
Date.now() - e.ts < PF_TTL                          // vx-router (×2)
now - _lastSessionNotify >= SESSION_NOTIFY_THROTTLE // vx-shell → « Analyse mise à jour »
```

### Les 8 « comparaison de domaine »

```javascript
byMonth[months[months.length-1]] <= byMonth[months[0]]   // /journal : dernier mois vs premier
m[i-1]*m[i] <= 0                                          // /markets : changement de signe
values[values.length-1] >= values[0]                      // /portfolio : fin vs début
cl[n - 1] >= cl[0]                                        // anomaly-scan
values[values.length - 1] >= values[0]                    // chart-core
(s.value - next.value) > worstDrop                        // chart-core : recherche du pire recul
rank[st.key] < rank[worst.key]                            // options-structure : classement
capital / (spot * 100) > 0.12                             // options : taille de position 12 %
```

**`m[i-1]*m[i] <= 0` est la plus fine du relevé** : un produit de deux termes
consécutifs négatif ou nul **détecte un croisement de zéro** — une décision de
marché écrite en une multiplication, qu'aucun instrument cherchant un nom ne
pouvait voir.

### Les 6 branches qui produisent un libellé

`x[1]>=0 → var(--vx-positive)` · `xb-a.left>34 → PERTE/GAIN` ·
`a.right-xb>34 → GAIN/PERTE` · `now - _lastSessionNotify >= …` →
« Analyse mise à jour » · les compteurs d'entrées corrompues → `0`.

## Le recouvrement avec la série (546-A)

**2 des 28 avaient déjà été lus et publiés** : le `received_ts` de
`/analysis/AAPL` (les six sites « temps » du 583, le dossier du 584) et le
`base.ts` de `/portfolio` (584 — repli à effet **opposé**, réparateur).

**Un angle mort qui contient des sites déjà lus n'en est pas entièrement un.**
Personne dans la série n'avait mesuré ce recouvrement.

## Second contrôle (481) — les deux côtés non nommables

Le relevé « gauche non nommable » ne regardait jamais la droite. **6 des 28 ont
les deux côtés composés** :

```javascript
(Date.now()/1000-(s.received_ts||0)) <= 6*3600
byMonth[months[months.length-1]]     <= byMonth[months[0]]
values[values.length-1]              >= values[0]
cl[n - 1]                            >= cl[0]
values[values.length - 1]            >= values[0]
rank[st.key]                         <  rank[worst.key]
```

**Quatre des six comparent le dernier élément d'une série à son premier** —
c'est un idiome du dépôt, pas six écritures indépendantes.

## Ce que le lot n'établit pas

- Que ces 28 soient justes : elles sont lues et nommées, **aucune n'a été
  confrontée au serveur**.
- Que `m[i-1]*m[i] <= 0` détecte correctement tous les croisements : la forme
  est lue, **son comportement n'est pas évalué** (une valeur nulle y compte
  comme un croisement).
- Que les 43 sites tiers soient sans intérêt : **ils n'ont pas été lus**, ils
  ont été écartés par règle.
- Que le relevé couvre toutes les comparaisons : les opérateurs d'égalité
  restent hors champ, comme au 588.

## Limites déclarées

- Le corpus reste les 8 pages à leur URL de base + `/analysis/AAPL`.
- « Gauche non nommable » est **une propriété de mon instrument**, pas du code :
  elle recouvre `a-b`, `t[i]`, `f(x)+1` et rien d'autre. Un autre nommeur aurait
  découpé autrement — et c'est précisément ce qui a produit trois relevés
  différents (192 / 108 / 28) sur **le même corpus**.
- Le classement est **par motif de source lu**, avec les 28 affichées en entier
  au préalable : la couverture est vérifiée, la lecture reste une lecture.

## Règles neuves

- **589-A — UN COMPTEUR SANS POSITION N'EST PAS UNE MESURE.** `res.sansNom++`
  ne peut être ni dédupliqué ni filtré ; le nombre qu'il produit n'est
  comparable à rien. Enregistrer le site, pas l'incrément.
- **589-B — UN ANGLE MORT DOIT ÊTRE CONFRONTÉ À CE QUI A DÉJÀ ÉTÉ PUBLIÉ.**
  2 des 28 étaient déjà lus. Mesurer le recouvrement fait partie du relevé.
- **589-C — MON ATTENTE « SURTOUT TECHNIQUE » A ÉTÉ FAUSSE TROIS FOIS DE
  SUITE.** 587 (bornes techniques), 588 (géométrie), 589 (arithmétique de
  dessin). **Ce n'est plus une erreur, c'est un biais** : j'estime
  systématiquement trop bas la part du produit dans ce code.

## Ce que le dépôt fait bien

- **Les bornes de cache sont écrites dans les deux sens** (`< ttl` et `>= ttl`)
  plutôt qu'un `else` — le cas d'égalité est tranché explicitement.
- **`capital / (spot * 100) > 0.12`** exprime une règle de dimensionnement en
  une ligne lisible, sans constante magique cachée.
- **L'idiome « dernier vs premier »** est écrit de la même façon dans quatre
  fichiers différents : c'est une régularité, pas quatre inventions.
- **Vingt-huit sites seulement** échappent au nommage sur tout le corpus de
  produit : le code est très majoritairement écrit avec des noms.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped**

## Comptes

- Arrêtés avant publication : **215 (inchangé)**
- Publiés puis corrigés : **40 (+1 — les « 226 » du 588, ramenés à 28 de produit)**
- Interprétations retirées : **12**
