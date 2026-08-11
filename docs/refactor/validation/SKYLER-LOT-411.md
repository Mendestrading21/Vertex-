# SKYLER LOT 411 — Les 59 provenances déclarées : 2 nomment une origine sans producteur, et elles ne s'affichent jamais

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-411` (base : lot 410 fusionné,
1e66a29)

Chaque carte de Vertex déclare sa provenance (`source:`). C'est le contrat
d'honnêteté visible par le trader : *d'où vient ce que je regarde ?* Personne
n'avait vérifié que l'étiquette corresponde à la donnée réellement tracée.

**Aucun code, aucun gardien, aucun test.**

## Le recensement

Périmètre servi (`vertex/**` `.py` + `.js`, `terminal.py`, six modules reliques
exclus) :

```text
champs `source:`                          59   (dans 26 fichiers)
   EXPRESSION (variable, ternaire)        32   ← propage la provenance réelle
   LITTÉRAL (chaîne fixe)                 27   ← peut dériver
```

Les 32 expressions (`source: d.source`, `source: prov`) sont **honnêtes par
construction** : elles transportent ce que le serveur a déclaré. Seuls les 27
littéraux peuvent mentir, parce qu'ils sont écrits à la main une fois et ne
suivent pas la donnée.

**Témoin de l'instrument** : les deux étiquettes connues du lot 407
(`portfolio_page.py` L610/L617, « clôtures déclarées (myTradesEquity) ») sont
bien retrouvées parmi les littéraux.

## Les 27 littéraux, confrontés à leur origine

Chaque origine nommée a été cherchée dans le dépôt — existence **et** producteur :

```text
origine nommée                    vérification                          verdict
scenario_pricer  (×6)             vertex/options/scenario_pricer.py     EXISTE
SCAN             (×5)             options_board + le serveur déclare
                                  lui-même source='SCAN' (3 sites)      EXACTE
board options                     scan_state['options_board']           EXISTE
calendrier moteur (×3)            /cal-feed (7 réf. terminal.py)        EXISTE
moteur track-record               vertex/engines/track_record.py        EXISTE
Moteur de régimes                 /api/market/regime                    EXISTE
journal local    (×2)             set('vxJournal') ×2                   PRODUIT
clôtures déclarées (L642)         set('myTradesClosed') ×1              PRODUIT
clôtures déclarées (myTradesEquity) ×2   set('myTradesEquity') → 0      ★ SANS PRODUCTEUR
```

**25 sur 27 sont exactes.** Les deux seules qui nomment une origine sans
producteur sont celles du dossier 406/407.

Le sondage sur « SCAN » mérite d'être noté : l'étiquette du client **duplique la
déclaration du serveur** (`source='SCAN'` dans `options_intel_api.py`) au lieu
d'en inventer une. C'est la bonne façon de faire, et elle est majoritaire.

## Le détail qui change la description du dossier

Trois cartes de `/portfolio` portent « clôtures déclarées ». Elles ne se valent
pas :

```text
L610  equityCard    ← eq = E().equity()  → myTradesEquity  → 0 écrivain → JAMAIS rendue
L617  drawdownCard  ← même série                            → JAMAIS rendue
L642  heatmapCard   ← withPl (myTradesClosed)               → 1 écrivain → RENDUE, étiquette exacte
```

Conséquence pour le dossier de rang 1 : **ces deux étiquettes ne sont jamais
affichées**, puisque les cartes qui les portent sont sur une branche
inatteignable. Le préjudice du 406/407 est donc bien **le graphique absent et la
consigne impossible** — *pas* une provenance mensongère à l'écran.

C'est une précision, pas une atténuation : le HHI faux du 407, lui, **est**
affiché. Mais la description doit être juste.

## Ce que ce lot établit

Quatrième bornage consécutif (402, 408, 409, 411). Le contrat de provenance tient :
**59 déclarations, 32 honnêtes par construction, 25 littéraux exacts, 2 pointant
une origine morte et jamais affichées.**

Le zéro est **substantiel** : les 27 littéraux ont été confrontés un par un à
l'existence **et** au producteur de l'origine nommée, pas comptés.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de preuve
  MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; la suite a
  ré-horodaté les trois fichiers habituels, restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

Le contrôle porte sur la **correspondance entre l'étiquette et l'origine
nommée** : l'origine existe-t-elle, produit-elle. Il ne vérifie pas que la
**valeur** tracée soit juste — un `scenario_pricer` qui se tromperait dans ses
calculs porterait quand même une étiquette exacte. Et les 32 expressions n'ont
pas été suivies jusqu'à leur source : elles sont réputées honnêtes parce
qu'elles propagent, ce qui est un raisonnement de conception, pas une mesure.

## Où en est la boucle

Quinzième lot court. Les quatre derniers ont **borné** plutôt que trouvé — c'est
cohérent avec un dossier qu'on cherche à rendre décidable, pas avec une
exploration qui s'épuise.

**Deux questions — bilans n°9 et n°10 — attendent toujours une réponse.**
