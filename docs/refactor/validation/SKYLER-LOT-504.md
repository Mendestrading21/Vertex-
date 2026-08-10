# SKYLER LOT 504 — Retour au PRODUIT après vingt lots de moteurs : sur `/journal`, page jamais auditée, le KPI « Respect des invalidations » affiche **100 % en vert** sur des entrées qui ne portent AUCUN stop — et **0 % en rouge** sur une petite position bien gérée. Et deux KPI voisins sont le MÊME nombre sous deux libellés

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-504` (base : lot 503 fusionné,
`682036ce`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé. Rien corrigé.**

## Le choix

**(b)**, la recommandation du 503 : **un retour au produit sur une surface jamais
auditée**. Vingt lots consécutifs sur les moteurs, les rapports et les constantes
mortes ; le 503 a montré qu'on trouve de vraies erreurs en se relisant, mais
quatre pages produit jamais regardées en promettaient davantage. J'ai pris
`/journal`. **La promesse était bonne.**

## La réponse

```text
KPI « Respect des invalidations » — /journal, vue PAR DÉFAUT, peint et colorié
forme du journal                            AFFICHÉ      VÉRITÉ    verdict
A · manuel LONG, prix bien renseignés        50 % neutre   50 %     CONFORME
B · manuel SHORT, les deux stops sautés     100 % VERT      0 %     ** FAUX **
C · auto, stop VIDE (la forme normale)      100 % VERT      n/d     ** FAUX **
D · auto, stop=prix / exit=total $          100 % VERT      n/d     ** FAUX **
E · auto, PETITE position bien gérée          0 % ROUGE     n/d     ** FAUX **
```

Et, du même défaut racine :

```text
« Respect de la méthode » vs « Qualité des entrées » — affichés CÔTE À CÔTE
sur les 5 formes de journal que le code peut réellement produire : ÉCART 0
ils ne divergent QUE sur des entrées qu'aucun producteur n'écrit
→ DEUX LIBELLÉS, DEUX SOUS-TITRES, UN SEUL NOMBRE
```

## L'instrument — je ne transcris rien, j'exécute les octets servis

`behavioral()` (1 258 caractères) et `loadDiscipline()` (3 113 caractères) sont
**extraites par regex des octets servis par `/journal`** puis exécutées telles
quelles sous node avec un `E()` bouchonné. Le page servie porte bien le md5 de
référence `243699ace2d5` — c'est la page de production, pas une copie.

Les journaux sont **fabriqués en mémoire** et passés à node sur stdin.
`desk_data.json` n'est ni lu ni écrit.

## Le code en cause — `performance_page.py:190-205`, servi sur `/journal`

```js
const num = (x)=>{const n=Number(x); return isFinite(n)?n:null;};
const withPlan     = j.filter(e=>e.reason && num(e.stop)!=null);
const lossWithStop = closed.filter(e=>e.result==='LOSS'
                     && num(e.stop)!=null && num(e.exit)!=null);
const respected    = lossWithStop.filter(e=>num(e.exit) >= num(e.stop)*0.97);
```

**Trois causes indépendantes, qui CO-OCCURRENT** (leçon 497) :

### A. `num('')` et `num(null)` valent ZÉRO, pas `null`

Témoin direct, sur le `num` du code servi :

```text
num("")        = 0      ← une chaîne vide devient zéro
num(null)      = 0      ← null aussi
num(undefined) = None   (null)
num("abc")     = None   (null)
```

Or **les deux seuls producteurs d'entrées écrivent toujours la clé** :
`vx-entities.js:177` écrit `stop: t.entrySnap?.stop ?? ''` — et `:145` crée les
positions avec `entrySnap: {}`, donc **le stop vide est la forme NORMALE de
l'entrée automatique**, pas un cas de bord ; `performance_page.py:353` écrit
`stop: n('j-stop')`, soit `null` quand l'utilisateur laisse le champ vide.

Conséquence : une entrée **sans stop** entre dans le dénominateur avec un stop
de 0, et `exit >= 0 × 0,97` est vrai pour tout montant positif → **comptée comme
« invalidation respectée »**.

### B. Aucune lecture de `e.dir` — le test est inversé pour les SHORT

Le modal propose explicitement SHORT (`performance_page.py:328`). Pour un short
le stop est **au-dessus** de l'entrée : respecter l'invalidation, c'est sortir
**en dessous**. La formule `exit >= stop × 0,97` compte donc comme « respecté »
un short sorti à 150 avec un stop à 100 — une débâcle.

### C. Les unités sont mêlées sur le chemin automatique

`vx-entities.js:177-179` écrit `entry: t.cost` et `exit: recovered`, des
**montants totaux en dollars** (le fichier le dit : « schéma desk : cost = TOTAL
investi »), tandis que `stop` est un **prix unitaire**. Le chemin manuel, lui,
écrit des **prix**. Le même champ porte deux sens selon qui l'a écrit, et la
comparaison `exit >= stop × 0,97` les confronte.

## Le second contrôle — et il m'a fait retirer mon propre adjectif

Mon premier banc exécutait `behavioral()` **seule**. Trois choses lui
échappaient, et je les ai attaquées (règle 481) :

**I. « servi mais jamais pris ».** J'avais vérifié le libellé dans les octets et
l'appel `loadDiscipline()` dans `boot()`. Ce n'est pas la même chose que d'être
peint. J'ai donc exécuté `loadDiscipline()` elle-même avec un DOM bouchonné et
**lu le HTML produit** : ~1 190 caractères dans `#vx-pf-kpis`, libellé présent,
valeur et classe extraites du HTML réel. **Le nombre atteint bien l'écran.**

**II. le pivot est-il un artefact de mon banc ?** (leçon 501) Témoin direct sur
`num`, ci-dessus. **Le pivot tient.**

**III. le défaut flatte-t-il TOUJOURS ?** J'allais écrire « le défaut rassure ».
**Le contrôle dit non.** Sur une petite position (stop 92 en prix, sortie 50 $ en
total), la formule rend **0 %, en ROUGE** — elle accuse un trader qui n'a rien
fait de mal.

> **Le défaut n'est pas « rassurant », il est ARBITRAIRE : le chiffre suit la
> TAILLE de la position, pas la discipline.** C'est plus grave que ce que
> j'allais publier, et moins simple à raconter.

**Arrêtés avant publication : 81 → 82.**

## Aucun gardien — et une VINGT-SIXIÈME récurrence du piège des homonymes

```text
tests/test_journal_system_07.py:39
    assert 'respectMethod' in src and 'invalRespect' in src
```

Le seul test qui nomme ces KPI vérifie que **les identifiants existent dans la
source**. Il passerait à l'identique si les quatre pourcentages étaient tirés au
hasard. C'est la règle de la veine : **matcher un MOT n'est pas matcher la
CHOSE.**

Et `tests/test_postmortem.py:29::test_behavioral_flags_derived_from_numbers`
**ne couvre pas cette fonction** : il teste `postmortem.build()`, le moteur
serveur. **« behavioral » désigne deux objets différents dans ce dépôt** —
vingt-sixième récurrence du piège des homonymes.

## DOSSIER 504-A — Classement

**Rang 1**, et je dis pourquoi ce n'est pas moins. Le chiffre est **affiché,
colorié et sur la vue par défaut** d'une page servie ; il est faux **dans les
deux sens** ; il n'a **aucun gardien** ; et surtout **la phrase d'en-tête porte
le même nombre** — `loadDiscipline()` construit « Tu as documenté un plan (raison
+ invalidation) sur X % de tes décisions » à partir de `respectMethod`, et la
tonalité de tout le hero en dérive. C'est le motif du 433 : *les phrases de tête
disent la même chose en chœur*. Enfin, le critère du 464 — **le consommateur** —
s'applique en plein : la page pose la question « Suis-je en train de devenir un
meilleur investisseur ? » et y répond par un nombre qui ne mesure pas ce qu'il
annonce.

**Ce qui l'empêche d'être plus haut** : aucun ordre n'est passé, READONLY est
intact, et il s'agit d'une auto-évaluation, pas d'une consigne d'entrée en
position — à la différence du 457.

Correction pressentie, et je ne l'engage pas : un `num` qui rende `null` sur
`''` et `null` ; un dénominateur restreint aux entrées portant réellement un
stop, avec `n/d` honnête sinon ; la lecture de `e.dir` ; et **un champ
d'unité explicite** sur `entry`/`exit`, puisque deux producteurs y écrivent deux
grandeurs différentes. **Aucun GO, rien n'est engagé.**

## Portée — ce que ce lot NE dit PAS

- Je n'ai **pas** ouvert le vrai `desk_data.json` : je ne sais pas combien
  d'entrées réelles sont dans chaque forme. Je montre que **le code produit ces
  formes**, pas leur fréquence chez l'utilisateur.
- Les formes de journal sont **fabriquées**. Elles suivent exactement les deux
  producteurs lus dans le code, mais ce sont mes fabrications.
- **Aucun navigateur ouvert.** Le rendu est mesuré par exécution de la fonction
  servie sur un DOM bouchonné, pas par capture d'écran. Un contrôle en navigateur
  reste à faire — et il est sans risque réseau sur `/journal`.
- Les **quatre autres sous-vues** de `/journal` (`journal`, `learnings`,
  `progression`, `track-record`) **ne sont pas auditées** ici. À noter : la
  référence MD5 de `/journal` ne couvre que la vue par défaut — **quatre vues
  servies ne sont dans aucune empreinte de la boucle.**
- « Qualité des sorties » (`closedWithLesson / closed`) **n'est pas mise en
  cause** : elle ne dépend d'aucun champ numérique.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` = `/home/user/Vertex-` ; sorties
  en chemin **absolu** (incident 487).
- **Aucun fichier de production touché** (`git diff --stat` : AUCUN). Pas de
  bump. SW : `td-shell-v187`.
- `persist` redirigé et **vérifié** (`cache_path` suit la redirection) avant tout
  import de `terminal`, dans les trois scripts. Aucune route réseau sortante :
  seul `GET /journal` a été appelé, une lecture.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Le 503 recommandait de quitter l'auto-audit pour le produit. **Un seul lot sur
une seule page en a rapporté un dossier rang 1**, avec trois causes racines, une
tautologie d'affichage en prime, et zéro gardien. Le contraste mérite d'être dit
franchement : vingt lots de moteurs avaient donné vingt-six dossiers ; une
après-midi sur une page jamais regardée en donne un de plus, du premier coup.

Ce que je retiens pour la méthode : **le troisième contrôle a changé la
conclusion, pas seulement sa confiance.** J'allais écrire « le défaut rassure » —
c'était faux, et ç'aurait été une interprétation à retirer plus tard. Le défaut
est arbitraire, ce qui est pire et plus difficile à formuler.

Feuille : **27 dossiers · seize rang 1 · neuf rang 2 · trois rang 3**.
Dettes nommées restantes : **l'espion au troisième niveau** (toujours
déconseillé) ; **les trois autres surfaces jamais auditées** (`/markets`,
`/options`, `/system`) ; **les quatre sous-vues non auditées de `/journal`** ; et
**le compte des rangs relatifs sur les lots postérieurs au 480**.

Comptes séparés : résultats faux **arrêtés avant publication 82 (+1)** ; publiés
puis corrigés **12** ; interprétations retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
