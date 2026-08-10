# SKYLER LOT 502 — La dette du coût de démarrage payée : les 4 369 lignes mortes coûtent NEUF MILLISECONDES et 1,49 Mo. Le devis de purge gagne son dernier chiffre — et ce chiffre lui RETIRE un argument

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-502` (base : lot 501 fusionné,
`8fa7de14`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.
Rien supprimé.**

## Le choix

**(a)**, et sans hésiter. La dette était nommée au **498**, non payée au 499, au
500, au 501. **Trois reports, c'est le seuil où le 498 avait décidé d'arrêter de
reporter** — et il avait fini par payer. **(b)** l'espion au troisième niveau et
**(c)** les huit rangs relatifs **restent des dettes nommées**.

## La réponse

```text
composante                                        mesure
compilation des 4 369 lignes mortes           3,8 – 4,3 ms   deux mesures concordantes
allocation des littéraux à l'exécution             0,00 ms   constantes du code compilé
passes d'injection sur 1,43 Mo                    4,50 ms   BORNE INFÉRIEURE
──────────────────────────────────────────────────────────
TOTAL                                          ≈ 8 – 9 ms
mémoire résidente                                  1,49 Mo
part de l'exec de terminal.py (~1,17 s)             0,7 %
```

**Neuf millisecondes.** Le devis de purge du 498 — 4 369 lignes, 19 constantes,
12 pages, zéro consommateur — a désormais son dernier chiffre, et **ce chiffre
retire un argument** : **la performance n'est pas une raison de purger.**

## Le détail, et pourquoi chaque nombre tient

### A. Compilation — 4,3 ms, et elle est payée à CHAQUE démarrage

Source réel **796 882 o** contre source neutralisé en mémoire **148 162 o** —
81 % des octets retirés. `compile()`, 9 répétitions :

```text
compile RÉEL        min 21,7 · médiane 22,7 · max 25,0 ms
compile NEUTRALISÉ  min 17,3 · médiane 18,3 · max 19,5 ms
ÉCART médian 4,3 ms   ·   BRUIT max 3,3 ms   →  significatif, mais DE PEU
```

Mesure indépendante : `compile()` du **seul** sous-ensemble mort (653 412 o,
4 369 lignes) → **3,77 ms**. **Les deux chemins concordent** (règle 495 — quand
la borne mesurée coïncide avec la seconde mesure, la cause est identifiée).

**Et cette compilation est payée à chaque lancement.** `CLAUDE.md` documente le
démarrage comme `python terminal.py` : le module **principal** n'est jamais mis
en cache bytecode. **Vérifié par exécution**, pas supposé :

```text
script exécuté 2 fois comme __main__  →  AUCUN __pycache__
le même fichier importé 1 fois        →  gros.cpython-311.pyc apparaît
```

### B. Injections — 4,50 ms, et c'est une borne inférieure

Rejouées sur les **12** constantes `PAGE_*` (1 431 362 octets) :

```text
_inject_single_nav × 12    1,94 ms
replace </body>    × 12    2,30 ms
_inject_vx         × 12    0,13 ms
_extract           × 12    0,13 ms
                   TOTAL   4,50 ms
```

**Borne inférieure assumée** : je rejoue **une** passe de chaque helper, alors
que `PAGE_DAILY` subit **six** réaffectations successives dans le fichier.

### C. Allocation à l'exécution — zéro, et j'ai vérifié que c'est un vrai zéro

```text
exec des 19 affectations seules, 9 répétitions : min 0,00 · médiane 0,00 · max 0,00 ms
TÉMOIN : copier une chaîne de 650 000 o                            0,3 µs
```

Un zéro se lit mal (leçon 501 : *un zéro de couverture et un zéro de propreté
sont indiscernables*). **Vérifié plutôt que publié tel quel** : les littéraux
sont des **constantes du code compilé**, leur « allocation » n'est qu'un
`STORE_NAME` sur un objet déjà construit par le compilateur. Le témoin montre que
le chronomètre voit bien la microseconde. **Le zéro est physique, pas cassé.**

**Arrêtés avant publication : 79 → 80.**

## Ce que la mesure a fait échouer — et c'est un ajout au devis

Ma première approche exécutait `terminal.py` **neutralisé en mémoire** pour
comparer directement les deux temps d'exécution. **Elle échoue** :

```text
terminal.py:5884  assert _opp_i > 0 and 'scHome' in _OPP_BRIEF_JS
                         and 'top5Sec' in _OPP_BRIEF_JS, 'extraction Opportunity Brief KO'
AssertionError: extraction Opportunity Brief KO
```

`terminal.py` **s'auto-vérifie sur le CONTENU de `PAGE_ENTREPRISES`** : il en
extrait le Morning Opportunity Brief (`:5882-5884`) et **refuse de démarrer** si
l'extraction rate.

**Conséquence concrète pour le devis du 498 : une purge des constantes mortes
ferait échouer le module au démarrage tant que cette assertion — et l'extraction
qu'elle protège — ne sont pas traitées.** `PAGE_ENTREPRISES` est morte comme
page, mais **vivante comme réservoir** : `_OPP_BRIEF_JS` en est extrait et
réinjecté dans `PAGE_DAILY`… qui est morte aussi. La chaîne reste interne à la
famille morte — le 498 l'avait déjà montré pour `_NAV_CSS_CANON` — mais **elle
est protégée par une assertion**, ce que le 498 n'avait pas vu.

## Le second contrôle — ce que le banc EXCLUT

Mon instrument mesure du **temps au démarrage** et de la **mémoire**. Il exclut
trois choses, et je les nomme plutôt que de les laisser entendre :

1. **Le coût par requête : nul, et c'est structurel.** Les constantes sont
   construites une fois à l'import ; aucune route ne les touche (498). Le
   démarrage est le **seul** moment où elles coûtent quelque chose.
2. **Le démarrage de PROCESSUS complet** est plus long que l'exec de
   `terminal.py` : **1,44 à 2,20 s** mesurés en sous-processus, dominés par
   numpy, pandas, flask et les moteurs. Rapportée à ce total, la part morte
   tombe vers **0,4 – 0,6 %**. Mon 0,7 % est donc la **borne haute** du ratio.
3. **Si 1,49 Mo résident comptent sur la machine cible**, je ne peux pas le
   savoir d'ici. Le chiffre est donné, son importance est un arbitrage humain.

## Portée

- Les temps sont mesurés **sur cette machine**, dans ce conteneur. Un autre
  matériel donnerait d'autres millisecondes ; **les ordres de grandeur et les
  ratios, eux, sont robustes**.
- L'écart de compilation (4,3 ms) est **significatif mais du même ordre que le
  bruit** (3,3 ms). C'est la mesure indépendante à 3,77 ms qui le solidifie, pas
  la première seule.
- Les 4,50 ms d'injection sont une **borne inférieure** explicite.
- La neutralisation en mémoire **n'a jamais touché le disque**.
- **Aucun navigateur ouvert** — la question est un temps d'import, pas un rendu.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties en chemin
  **absolu** (incident 487).
- **Aucun fichier de production touché. Rien supprimé.** Pas de bump.
  SW : `td-shell-v187`.
- `persist` redirigé **et vérifié dans chaque sous-processus chronométré**
  (avertissement du réveil, appliqué) ; aucune route réseau sortante.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La dette est payée au quatrième tour, et **la réponse est décevante dans le bon
sens** : le code mort ne coûte presque rien à l'exécution. Neuf millisecondes et
un mégaoctet et demi. **Un lot qui retire un argument vaut un lot qui en
ajoute** — le devis du 498 est maintenant complet et honnête : la purge se
justifierait par la **lisibilité** de `terminal.py` (61,1 % de sa masse), **pas**
par la performance.

Et la tentative ratée a rapporté plus que la mesure réussie : **le fichier
contient une assertion qui dépend du contenu d'une page morte.** Le devis a une
ligne de plus, et elle n'était pas dans le 498.

Feuille **inchangée : 26 dossiers · quinze rang 1 · neuf rang 2 · trois rang 3**.
Dettes nommées restantes : **l'espion au troisième niveau** et les **huit rangs
relatifs jamais re-vérifiés**.

Comptes séparés : résultats faux **arrêtés avant publication 80 (+1)** ; publiés
puis corrigés **11** ; interprétations retirées **3**.

**Dix bilans — n°9 à n°18 — attendent une réponse.**
