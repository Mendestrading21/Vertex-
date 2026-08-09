# SKYLER LOT 429 — Trois vocabulaires de décision coexistent légitimement : 13 porteurs sur 14 prennent le bon, un seul se trompe

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-429` (base : lot 428 fusionné,
3538f34)

Treizième lot de la veine. Le 428 avait trouvé un calcul rendu **constant** par
un décalage de vocabulaire. La règle de la boucle dit : *quand un lot TROUVE, le
suivant peut utilement BORNER.* C'est ce lot.

**Aucun code, aucun gardien, aucun test.** Et **aucun défaut nouveau** — c'est un
bornage, et il tranche.

## L'instrument

Sur le corpus **servi** (95 objets, 3 829 722 octets) : toute comparaison d'un
porteur à un **jeton de vocabulaire** (littéral en MAJUSCULES), groupée par
porteur.

Le premier passage ne connaissait qu'une forme — `.champ === 'JETON'` — et
manquait `u !== 'ÉVITER'`, la moitié même du défaut du 428, portée par une
`const` locale. **Un détecteur qui ne connaît qu'une forme fabrique de faux
zéros** (leçon 414) : un second passage a été ajouté pour les **identifiants
nus**.

```text
passage 1 · `.champ` comparé à un jeton      27 couples
passage 2 · identifiant NU comparé à un jeton 17 couples
                                     TOTAL   44 couples · 18 porteurs
```

**Témoin positif** : les deux moitiés du défaut du 428 apparaissent bien —
`isBuy` au passage 1, `isAct` (`u`) au passage 2. L'instrument mord là où l'on
sait qu'il doit mordre.

## Ce que la confrontation a révélé de structurel

Le dépôt n'a pas « un vocabulaire de décision ». Il en a **trois**, tous
légitimes, produits par trois moteurs différents :

```text
lignes du scan       BUY · WATCH · WAIT · AVOID          vertex/strategy/config.py:51
comité               ACHETER · RENFORCER · ATTENDRE · ÉVITER   vertex/engines/committee.py
Skyler canonique     ACHETER · ATTENDRE · REFUSER        vertex/engines/skyler_core.py
```

**Le défaut du 428 se re-décrit alors plus précisément** : ce n'est pas « du
français contre de l'anglais », c'est **le vocabulaire du COMITÉ appliqué aux
lignes du SCAN**. Deux vocabulaires réels du même dépôt, appliqués au mauvais
producteur.

## La confrontation, porteur par porteur

Chaque porteur remonté à son producteur dans la source de vérité :

```text
porteur (page)                 jetons comparés                producteur                              verdict
name (/markets)                VIX, WTI                       terminal.py:450 / :240                  EXACT
verdict, v (/opportunities)    BUY, AVOID, ACHETER, ÉVITER    config.py:51 (+ comité)                 EXACT — accepte les DEUX
u, (v||'') (/markets)          ACHETER, RENFORCER, ÉVITER     config.py:51 → BUY/WATCH/WAIT/AVOID     ✗ DÉFAUT (lot 428)
x = r.decision (/opportunities) ACHETER, RENFORCER,           skyler_core → ACHETER/ATTENDRE/REFUSER  EXACT — 2 jetons morts
                                REFUSER, REDUIRE
type, typ, kind                CALL, PUT, STK                 ibkr_positions.py:26/:34 (secType)      EXACT
result (/journal, /portfolio)  WIN, LOSS                      <option value="WIN|LOSS"> servi         EXACT
status (/journal)              ANOMALIES                      decision_memory.py:850 → SAIN|ANOMALIES EXACT
status (/journal)              MESURE                         decision_memory.py:238                  EXACT
status (/system)               MISSING, OK                    ai/health.py:36                         EXACT
state (/system)                ACTIVE, DISABLED               tradingview_signal_store.py:109-110     EXACT
label (options-intel.js)       HOSTILE, PORTEUR               options/environment.py:91/:94           EXACT
level (vx-shell.js)            ACTIONABLE                     alerts/engine.py:15                     EXACT
regime (/markets)              UNKNOWN                        regime_engine.py:11                     EXACT
spy_regime (/markets)          TREND                          market/context.py:46                    EXACT
```

**14 porteurs confrontés · 13 exacts · 1 défectueux — celui du 428.**

*(Hors périmètre : `sym` sur `/portfolio` compare six tickers — BIL, GLD, SGOV,
SHV, XLP, XLU — ce n'est pas un vocabulaire moteur mais une liste de titres
défensifs.)*

## Deux résultats fins qui méritent d'être dits

**Une alerte levée par la chaîne** (motif du 426). `regime` et `spy_regime`
portent **deux vocabulaires différents** : `regime_engine.py` émet `TREND_UP`,
`TREND_DOWN`, `CHOP`, `RISK_ON`… et **jamais** `'TREND'` tout court. Or
`markets_page.py:545` compare `m.spy_regime === 'TREND'`. La remontée montre que
`spy_regime` a un **autre producteur** — `market/context.py:46`, qui émet
`TREND` / `CHOP` / `NEUTRAL`. **Deux champs distincts, deux vocabulaires, chaque
consommateur prend le bon.** L'alerte était légitime, la mesure l'a levée.

**Deux jetons morts, sans conséquence.** Sur `/opportunities`, la fonction de ton
du classement Skyler teste `RENFORCER` et `REDUIRE` ; `skyler_core.decide`
n'émet que `ACHETER`, `ATTENDRE`, `REFUSER`. Les deux branches sont
**inatteignables** — mais le comportement reste **juste** sur les trois jetons
réellement produits. C'est un rang 4, pas un défaut d'affichage.

**Un producteur plus riche que son consommateur, correctement traité.**
`tradingview_signal_store` émet **trois** états (`ACTIVE`, `WAITING`,
`DISABLED`) ; le détecteur n'en a vu que deux comparés. Vérification :
`system_page.py:538-540` les traite **tous les trois** par table, avec un repli
`['offline','n/d']`. Rien à signaler — et c'est justement le contre-exemple du
428.

## Ce qui échappe encore au détecteur, quantifié

```text
comparaisons à un jeton MINUSCULE ('live', 'demo'…)   44 couples · 27 porteurs
lecture par table `{…}[champ]` au lieu d'une comparaison   15 porteurs
```

Ces deux familles **n'ont pas été confrontées**. La seconde est celle qui, au
`/system`, se révèle *plus sûre* que la comparaison (elle porte un repli
explicite) — mais rien ne le garantit ailleurs. Un `switch`/`case` échapperait
aussi. **Le « 13 sur 14 » vaut pour les vocabulaires en MAJUSCULES comparés
explicitement, pas pour tout le dépôt.**

## Verdict du lot

**Négatif — et c'est le bon résultat.** Le défaut du 428 est une **exception**,
pas le symptôme d'un dépôt qui confondrait ses vocabulaires : sur les treize
autres porteurs, chacun interroge le vocabulaire de son propre producteur, y
compris là où deux champs voisins portent des vocabulaires différents.

Ce bornage **renforce** le 428 au lieu de l'affaiblir : un seul site se trompe,
et c'est celui qui affiche au trader comment interpréter son propre résultat.

## Portée

Un seul type de défaut cherché : la comparaison à un vocabulaire. Les 116
affirmations rendues non ouvertes du vivier restent **non vérifiées**. Aucune
exécution : ce lot lit des octets servis et remonte des chaînes de production —
**aucune valeur n'a été calculée ni observée sur des données réelles**.

Les producteurs ont été identifiés par recherche dans les sources ; pour chacun
j'ai lu l'énumération ou les affectations littérales, **pas exécuté le moteur**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; les trois fichiers ré-horodatés par la suite **restaurés à l'octet
  près et revérifiés par md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Trente-deuxième lot court, **dernier lot de mesure de la tranche 420-429**.
Séquence de la veine : **416 ✓ · 417 ✓ · 418 ✓ · 419 ✓ · 421 ✗ · 422 ✓ · 423 ✗ ·
424 ~ · 425 ✓ · 426 ✗ · 427 ✓ · 428 ✓ · 429 ✗ (bornage)**.

L'alternance trouvaille/bornage tient : le 426 avait borné le 425 et désigné une
vraie limite (le recensement) ; le 429 borne le 428 et tranche dans l'autre sens
— ici **rien à élargir**, la mesure dit simplement que le reste du dépôt sait
lequel de ses trois vocabulaires il interroge.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
