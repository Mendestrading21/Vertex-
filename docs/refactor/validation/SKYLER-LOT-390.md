# SKYLER LOT 390 — BILAN DE TRANCHE 380-389

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-390` (base : lot 389 fusionné,
0b3eae7)

Dix lots de veille autonome. Ce document n'ajoute aucun gardien : il mesure ce
que la tranche a réellement produit, et sert de point d'appui à la décision.

## Vérification de tranche — refaite, pas rappelée

**MD5 des 8 pages servies** (serveur DEMO après `/scan`) :

```text
/                fc15688d1af6   IDENTIQUE   (40 057 o)
/markets         c0bb91c6971a   IDENTIQUE   (71 089 o)
/opportunities   6a22a6abbd03   IDENTIQUE   (67 278 o)
/analysis        113827718e99   IDENTIQUE   (22 359 o)
/portfolio       f1b41b665d4a   IDENTIQUE   (85 672 o)
/options         6387210de785   IDENTIQUE   (24 696 o)
/journal         243699ace2d5   IDENTIQUE   (56 093 o)
/system          73e917c0f2d0   IDENTIQUE   (82 837 o)
```

**8/8 identiques aux références.** Dix lots n'ont pas déplacé un octet servi.

**Navigateur réel** (Chromium, `load` + détachement du squelette — `networkidle`
ne se stabilise jamais avec le SSE live) :

```text
/ 460 · /markets 613 · /opportunities 983 · /analysis 256 · /portfolio 318
/options 409 · /journal 401 · /system 486        (nœuds DOM après hydratation)
TOTAL erreurs console sur les 8 pages : 0
```

**Les gardiens de la tranche, rejoués avec une faute réelle** — un gardien au
vert ne prouve rien tant qu'on ne l'a pas vu tomber :

```text
381   clé retirée du repli SERVI de /system          MORD
382   bleu NON-MARQUE injecté dans un octet SERVI    MORD
383   recul de version du cœur                       MORD
385   repli numérique neuf dans terminal.py          MORD
386   marqueur de provenance IBKR supprimé           MORD
387   `finally` retiré de l'écrivain desk autorisé   MORD
389   redirection retirée du test journalisant GEX   MORD
[témoin] commentaire ajouté, borne inchangée         ne mord pas — correct
```

**7 sur 7.** Aucun gardien de la tranche n'a pourri.

## Les chiffres

| | |
|---|---|
| Lots | 10 (380 → 389) |
| Suite | **2 754 → 2 835 passed / 2 skipped** (+81) |
| Gardiens ajoutés | 7 fichiers, **81 tests** — exactement le delta |
| PR | #412 → #421, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, **inchangé sur les 10 lots** |
| `main` | jamais touchée |
| Fichiers de production modifiés | **0** |

Zéro fichier de production sur dix lots : c'est cohérent avec le MD5 8/8, et
c'est aussi la limite de la tranche — voir « ce qui n'a pas été prouvé ».

## Les trouvailles réelles — cinq

1. **381 — un repli SERVI que rien ne gardait.** Le repli de `deskKeys()` dans
   `/system` (utilisé quand `VXEntities` n'est pas chargé) n'était couvert par
   aucun test : y retirer une clé passait les 2 754 tests. Constat joint :
   `vx_kit.JS` (21 727 o) n'atteint **aucune** des 8 pages.
2. **382 — un énoncé plus large que la règle tenue.** « Aucun littéral couleur »
   était faux : **265 littéraux `#RRGGBB` distincts dans `vertex/ui/**`, dont 53
   atteignent une page servie**. La règle réellement imposée — *aucun bleu
   non-marque* — est la bonne ; c'est la documentation qui mentait.
3. **385 — le recensement des replis s'arrêtait à `vertex/`.** 254 handlers
   couverts, **113 hors filet dont 101 dans `terminal.py`** : **31 % des
   handlers de production**. Prouvé : un `except: return 50` neuf dans le
   monolithe passait, le même défaut dans `vertex/` faisait tomber la suite.
4. **387 — un test pouvait effacer les notes du trader.** `myNotes` est une clé
   **synchronisée** (`{"NVDA": "note"}`) ; le round-trip desk l'écrasait par un
   marqueur et restaurait **sans `finally`**. Assertion en échec →
   `{"guard": "lot84-guard-…"}` **définitivement**, le snapshot quotidien étant
   déjà consommé.
5. **388 — un point GEX fabriqué par jour, sur un vrai titre, dans un fichier
   servi.** 8 points MSFT strictement identiques accumulés par la suite, dans
   `gex_history_cache.json` que `/api/options/gex-radar` rend à l'utilisateur —
   pendant qu'ACN et ADBE portaient des valeurs variées et authentiques.

Les deux dernières sont d'une autre gravité que les trois premières : elles
touchent **les données réelles de l'utilisateur**, pas la documentation ni la
couverture.

## Deux veines ouvertes, deux veines fermées par la mesure

- **Audit des gardiens par mutation** (381-384) : 27 mutations utiles, **2
  trouvailles, toutes deux dans les 2 premiers lots**. Fermée au 384 malgré un
  protocole plus rigoureux à chaque passe — le rendement, pas la fatigue.
- **Écritures runtime par la suite** (386-389) : **2 trouvailles** (387, 388).
  Fermée au 389 : 5 fichiers encore touchés au départ, **4 à l'arrivée, tous sur
  un simple horodatage** (vérifié feuille à feuille, pas au premier niveau).

## Trois caractérisations gelées, non corrigées

Ce ne sont pas des fautes prouvées ; ce sont des comportements figés pour qu'on
ne puisse plus les innocenter par un raisonnement élégant.

- **`bret = 0.0`** (386) : `rs = clip(50 + (sym_ret − bench_ret) × 200)` fait
  passer 40 → 70, 16 → 40, 50 → 90. La force **relative** devient **absolue** —
  ce n'est pas un neutre. Confiné au backtest.
- **`context()` sur univers vide** (379) : affirme « NEUTRE » et « 0 % de
  participation » là où il faudrait dire « je ne sais pas ».
- **Les replis numériques de `terminal.py`** (385) : honnêtes *par leur site
  d'appel* (`if iv <= 0 or oi <= 0: continue`), pas dans l'absolu.

## Le fil rouge : la faute la plus fréquente était dans MES instruments

Sur dix lots, **huit fois** l'erreur n'était pas dans Vertex mais dans l'outil
avec lequel je le mesurais :

| lot | l'instrument mentait |
|-----|----------------------|
| 385 | périmètre `vertex/` seulement — 31 % des handlers invisibles |
| 386 | `'< 75' in src` : chaîne présente **4×**, le test restait vert |
| 387 | périmètre 4 → 15 → **17** fichiers ; et un gardien accusant **2 fichiers sains** |
| 387 | mutation `('msg' and False)` portant sur le **message**, pas la condition |
| 387 | exemption au **fichier** laissant passer un écrivain ajouté après coup |
| 388 | détecteur rendant « ? » : **8 sites comptés, 12 réels** |
| 389 | 8 candidats → **2 écrivains réels** ; et l'anti-vide creux **refait** |
| 390 | ce lot : mutation injectée dans une clé de nav **jamais rendue** |

Deux enseignements, tous deux coûteux :

**Avoir la règle écrite ne suffit pas à ne pas la re-violer.** Le lot 389 a
refait mot pour mot la faute du 386 — chercher une chaîne dans tout un fichier —
alors qu'elle figurait dans mes propres consignes. Ce qui l'a attrapée, ce n'est
pas la mémoire : **c'est la preuve ROUGE**.

**Le témoin négatif a une valeur symétrique.** Au 389 il a mordu : ma
« modification anodine » était une `AttributeError`, et le gardien avait raison.
Un témoin qui mord accuse d'abord le témoin.

## Ce que la tranche n'a PAS prouvé

- **Les 81 tests ajoutés sont STATIQUES.** Ils lisent le code — ils n'observent
  pas l'exécution. C'est précisément ainsi que le cas GEX a échappé au lot 387,
  dont le périmètre s'arrêtait au desk.
- **Les caractérisations sont datées.** « Les 4 fichiers ne changent qu'un
  horodatage » est vrai aujourd'hui ; rien dans le code ne l'impose.
- **Aucune couverture exhaustive n'est démontrée.** 27 mutations sur 2 835
  tests restent un sondage : « MORD » signifie « attrape CETTE faute-là ».
- **La pollution historique n'est pas nettoyée** : 7 points MSFT fabriqués et
  les points SKYX/TSTQ accumulés sont toujours là. Données runtime de
  l'utilisateur — leur purge est une décision, pas un effet de bord.

## Le vrai goulot — dix-huit dossiers, par ordre de priorité

L'agent a mesuré et documenté ; il ne peut pas trancher. Voici l'ordre que je
recommande, sur **impact utilisateur × coût × risque**.

### Rang 1 — l'utilisateur voit du faux (invariant n°4)

| dossier | pourquoi d'abord | coût |
|---------|------------------|------|
| **Purge des 7 points MSFT fabriqués** (388) | des chiffres de test servis comme un historique mesuré, sur un titre détenu | **minime** — supprimer une clé JSON |
| **Verdicts affirmés sur univers vide** dans `context()` (379) + **« points réels du scan »** sur `/markets` (363) | jumeaux : l'app affirme « NEUTRE / 0 % » au lieu de « je ne sais pas » | moyen — moteur + affichage |
| **Replis `0` de `_followed_count`/`_positions_count`** (378) | « desk illisible » et « desk vide » indiscernables | faible |
| **Badge de provenance temps réel IBKR** (386) | le marqueur `src='ibkr'` existe et n'est affiché nulle part ; temps réel et différé se ressemblent | faible côté moteur, **décision produit** côté UI |

### Rang 2 — risque sur les données de l'utilisateur

| dossier | pourquoi | coût |
|---------|----------|------|
| **Filet desk, option A** (362) | le restore rend l'état d'**avant la première sync du jour** : le travail de la journée est perdu | moyen — un instantané supplémentaire avant écrasement |

### Rang 3 — poids mort chiffré

| dossier | mesure | note |
|---------|--------|------|
| **7 constantes `PAGE_*`** (374) | **604 Ko de HTML assemblés à chaque import, jamais servis** | ⚠ contient le **seul** rendu « TEMPS RÉEL IBKR vs différé » du dépôt (386) — à trancher **avec** le badge, pas avant |
| **`vx_kit.JS`** (381) | 21 727 o servis **nulle part** | purger ou réintégrer, et déplacer l'ancre des clés de sync |
| **Purge É2** | 25 defs / 1 866 lignes | mécanique, gardée par la suite |
| **Purge É3**, **24 fonctions de tête** (326), **5 modules reliques** (327) | — | même famille |

### Rang 4 — cosmétique ou déconseillé

Empreinte dans les URL d'actifs (361) · PORTFOLIO_FIT dans `thesis_health` (365)
· échappement centralisé des étiquettes (368-369, coût mesuré : 1 page sur 8) ·
3 docstrings sous-déclarées (375) · points SKYX/TSTQ déjà accumulés (389 —
tickers synthétiques, bornés) · **durcissement de `vocab_js` (373) :
déconseillé en l'état**.

**Si un seul GO devait être donné**, ce serait la purge des points MSFT : coût
quasi nul, risque nul, et c'est la seule ligne de la liste où l'utilisateur voit
aujourd'hui un chiffre inventé présenté comme une mesure.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- Arbre propre ; **toutes les mutations du rejeu restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché.**
- Copies de sûreté des 21 fichiers runtime prises avant les sondes. Le serveur
  DEMO en a modifié 8 pendant la vérification — **arrêté, état restauré à
  l'identique**, écart final : aucun. *(Observation versée : un scan en mode
  DEMO écrit des valeurs de démo dans les caches runtime réels. Hors piste de ce
  bilan.)*
- Suite : **2 835 passed / 2 skipped**, inchangée. SW : `td-shell-v187`.

## Suite

Cadence normale au **lot 391**, sur les pistes fines restantes : refus construits
en variable (377) · formes imbriquées des promesses de retour (375) · trois sites
de concaténation à constantes (374) · le commentaire périmé de `vx-entities.js`.
Prochaine échéance périodique : **~lot 400**.
