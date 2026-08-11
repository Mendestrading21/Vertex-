# SKYLER LOT 485 — La dette du 484 soldée par exécution : le rang 1 est CONFIRMÉ (0 niveau S ou S+ sur 3 072 combinaisons) et mon propre chiffre est FAUX — le plafond n'est pas 35/40, il est 29/40

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-485` (base : lot 484 fusionné,
`68d4c27e`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le 484 avait nommé sa dette : « **aucun banc sur `skyler_core`** — le blocage de
S/S+ est établi par LECTURE de deux lignes et par AST ; je n'ai pas exécuté
`decide()`, et ce banc monterait la preuve d'un cran ». Un lot qui nomme sa dette
et passe à autre chose la laisse pourrir. Ce lot la solde — **et elle me corrige.**

## Sûreté avant le banc

`skyler_core` ne contient **aucune écriture** : zéro `save_json`, zéro `open(`,
zéro `.record(`, zéro appel à `persist`. Les écrivains cités par le 484
(`decision_memory.freeze`, `skyler_journal.record`, `session_log.record_close`)
sont appelés par `analysis_api.py:170-201`, **pas par le moteur**. `persist`
néanmoins redirigé **et vérifié** (`cache_path()` suit la redirection).

## Calibration, écrite dans le code du banc

Deux réponses connues d'avance, avec sortie programmée en cas d'échec :

```text
paquet vide          total= 0  level=REFUS_WATCH   attendu 0/REFUS_WATCH   OK
score technique 100→0  29 → 23  = −6               attendu −6 (poids du bloc)  OK
```

## Le paquet PARFAIT — tout au maximum sur les sept autres blocs

```text
fundamentals_quality           0 /  5   INSUFFICIENT
catalysts                      2 /  5   PARTIAL
technical_timing               6 /  6   AVAILABLE
institutions_flow_anomalies    1 /  4   PARTIAL
market_regime_sector           4 /  4   AVAILABLE
asymmetry_scenarios            6 /  6   AVAILABLE
options_quality                6 /  6   AVAILABLE
data_quality                   4 /  4   AVAILABLE
─────────────────────────────────────────────────
TOTAL 29 / 40    level = A    insufficient = ['fundamentals_quality']
```

**Balayage de 648 combinaisons** (score technique, R:R, régime, confiance, nombre
de catalyseurs, nombre d'anomalies, qualité d'option) — la borne **ne bouge
pas** : maximum atteint **29**, toujours. La règle du 459 est respectée : j'ai
fait varier la grille jusqu'à ce que la réponse cesse de bouger, et elle a cessé.

## Ce que le banc CONFIRME — le rang 1

**3 072 combinaisons**, en faisant varier en plus la red-team et le mandat :

```text
REFUS_WATCH  2952       S       0
B             112       S_PLUS  0
A               8
```

**Jamais, pas une seule fois, un niveau S ou S+.** Le rang 1 du 484-A passe de
« établi par lecture » à **établi par exécution**. Le rang ne change pas ; sa
preuve monte d'un cran, ce qui était exactement l'objet du lot.

**Et le banc trouve pire que ce que le 484 annonçait** : le plafond réel étant
29 et le niveau A exigeant 28, **A n'apparaît que 8 fois sur 3 072 — 0,26 %**.
Ce n'est pas seulement S/S+ qui est hors d'atteinte : **A tient sur deux points
de marge**, et exige un paquet quasi parfait sur les cinq blocs qui marquent.

## Ce que le banc RÉFUTE — mon propre chiffre publié hier

Le 484 écrivait : « **5 points inatteignables → score maximal réel 35/40** ».
**C'est faux.** Mesuré : **11 points inatteignables → plafond 29/40**.

**Trois blocs sont plafonnés sous leur poids, pas un :**

```text
fundamentals_quality   0 / 5    toujours 0            −5   ← le seul que le 484 avait vu
catalysts              2 / 5    branche unique → 2    −3
institutions_flow…     1 / 4    branche unique → 1    −3
                                                     ───
                                                      −11   plafond 29 / 40
```

Les deux blocs manqués **ne sont pas figés à zéro** — c'est précisément pourquoi
le détecteur AST du 484 les a laissés passer : il testait « ce bloc peut-il
marquer **quelque chose** ? » et ils marquent, respectivement, 2 et 1. Il ne
testait pas « ce bloc peut-il atteindre **son propre maximum** ? »

### Pourquoi je me suis trompé, et c'est le fait de méthode du lot

**J'avais posé la bonne question la veille, et à un autre objet.** Dans le même
lot 484, sur le barème LEAPS (G4), j'ai vérifié que **chaque dimension atteint
son maximum par la branche haute de son ternaire** — 30, 25, 20, 15, 10, somme
100 — et j'ai conclu « sain » sur cette base. **Puis j'ai découvert le barème du
score /40 et je ne lui ai PAS appliqué le test que je venais d'appliquer au
précédent.** J'ai cherché les blocs morts, pas les blocs bridés.

**UN TEST APPLIQUÉ À UN OBJET DE L'ENQUÊTE DOIT ÊTRE APPLIQUÉ À TOUS LES OBJETS
DE MÊME GENRE, Y COMPRIS À CELUI QU'ON VIENT DE TROUVER.** La trouvaille fait
oublier la méthode qui l'a produite.

**Publiés puis corrigés : 8 → 9.**

## Le second contrôle — trois cas que le banc EXCLUT

**(a) Un profil autre que V2.** Mon banc n'exerce que le profil actif.

```text
vertex_strategy_v1.json    skyler_score.blocks = NON
vertex_strategy_v2.json    skyler_score.blocks = OUI, somme 40
profil ACTIF chargé : version 2
```

`cfg = (prof.raw.get('skyler_score') or {}).get('blocks') or {}` → sous V1,
**tous les `mx` valent 0** et le score entier serait 0/40. **V2 est le profil
actif**, donc la mesure porte là où ça compte — mais **la conclusion est bornée
au profil V2, et je le dis** plutôt que de la présenter comme universelle.

**(b) Un chemin qui contournerait `block()`.** `decide()` pourrait retoucher
`total` ou `level` après coup. Vérifié ligne à ligne (`:551-637`) : il ne fait
que **lire** — `main_reason`, `'level': score['level']`, `'score': score`.
**Aucune réécriture.** Le verdict du banc est donc bien celui du produit.

**(c) Les blocs plafonnés le disent-ils eux-mêmes ?** Oui, et cela **atténue** —
je le dis parce que cela joue contre l'aggravation que je viens de publier :

```text
catalysts             basis = « … (plafonné 2/5) »
institutions_flow…    basis = « … (plafonné 1/4) »
fundamentals_quality  basis = « contexte fondamental non branché — 0 point, jamais estimé »
```

Ce `basis` est rendu dans l'attribut `title` de la puce (`analysis_page.py:879`) :
**disponible au survol, pas affiché**. La puce affichée, elle, montre
« Catalyseurs **2/5** » — un chiffre qui **invite à croire que 3 points restent
à gagner**.

## Conséquence sur les rangs

**484-A — S et S+ inatteignables en silence : rang 1 CONFIRMÉ**, désormais par
exécution (0 sur 3 072). Critères absolus inchangés : servi, conséquence sur une
décision, aucune information co-visible sur le plafonnement des niveaux.

**484-B — le « /40 » : reste rang 2, avec ses chiffres corrigés** (plafond 29, pas
35 ; 11 points, pas 5). Le défaut est **plus grave** que publié, mais
l'atténuation est **plus forte** aussi que ce que le 484 avait créditée : deux
des trois blocs déclarent leur propre plafond. **Je ne le monte pas au rang 1** —
une aggravation est aussi fragile qu'une atténuation (leçon 478), et il existe
bien une information par bloc, fût-elle au survol.

**Observation neuve, non classée** : `decide()` renvoie
`red_team: {'required': score['level'] in ('S_PLUS','S')}` (`:621`) — or `level`
a **déjà** été rabattu par `apply_red_team_rule` **à l'intérieur** de `score40`.
**`required` est donc toujours `False`.** Drapeau mort. Il n'atteint de toute
façon aucune surface servie (`red_team` : 0 occurrence dans `vertex/ui/` et
`vertex/static/`).

## Portée

- Le banc **fabrique le paquet à la main**. Il n'exerce **pas** `build_packet()`
  sur des données réelles : il établit ce que **`score40` peut rendre**, pas la
  distribution des scores en usage. C'est exactement la limite que le 459 avait
  posée pour `gex_scan`.
- **Conclusion bornée au profil V2** (le seul portant `skyler_score.blocks`, et
  le profil actif).
- Les 3 072 combinaisons couvrent **neuf axes discrétisés**, pas l'espace continu.
  La borne a cessé de bouger sur cette grille ; je n'affirme pas qu'aucune grille
  plus large ne la bougerait.
- **Aucun navigateur ouvert.** Rien de neuf n'est affirmé sur le rendu au-delà de
  ce que le 484 avait établi sur les octets servis.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; scripts du scratchpad
  avec `sys.path.insert` **et** `os.chdir`.
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié**. `score40()` et `load_profile()` appelés en
  mémoire — **le module ne contient aucune écriture, vérifié**. **`/api/skyler/`,
  `/api/analyst/`, `/api/correlations/`, `/options/` et `/desc/` NON appelées.**
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 21 fichiers, aucun apparu, aucun
  disparu ; restauration vérifiée par **md5** — écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

Le lot fait ce qu'un lot de solde doit faire, et il le fait **dans les deux
sens** : il **confirme** la trouvaille de la veille par exécution, et il
**corrige son chiffre** — de 35 à 29, de 5 points à 11, d'un bloc à trois.

Le plus utile n'est pas le chiffre. C'est que **la dette avait été nommée par le
lot qui la créait**, et que la solder vingt-quatre heures plus tard a suffi à
attraper une erreur qui, sans banc, serait restée dans l'index et dans le
STATUS comme un fait établi. **Nommer sa dette n'est pas la payer ; ce lot est
la preuve que la payer trouve autre chose.**

Comptes séparés : résultats faux **arrêtés avant publication 49** ; **publiés
puis corrigés 9 (+1)** ; interprétations retirées **3**.

**Huit bilans — n°9 à n°16 — attendent une réponse.**
