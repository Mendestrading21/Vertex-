# SKYLER LOT 422 — Le R:R affiché repose sur un mouvement attendu que le moteur s'invente, et c'est le seul repli qu'il n'étiquette pas

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-422` (base : lot 421 fusionné,
f939d56)

Sixième lot dans la veine des moteurs. Cible :
`vertex/options/scenario_pricer.py` — le simulateur qui produit le **R:R du
plan** et le **gain attendu** affichés sur `/options`, `/analysis` et
`/opportunities`.

**Aucun code, aucun gardien, aucun test.**

## La règle, et elle est écrite partout dans ce fichier

Le docstring l'annonce : *« honnêteté §6.8 : le modèle européen est une
ESTIMATION … étiquetée MODEL_ESTIMATE, jamais présentée comme vérité broker »*.
Et le corps la tient, trois fois :

```python
if not mid or mid <= 0 or dte <= 0 or spot <= 0:
    result['limitations'].append('données de contrat insuffisantes — simulation refusée '
                                 '(pas de chiffre inventé)')          # ← refus honnête
if iv is None or iv <= 0:
    iv = _implied_vol(...)
    result['limitations'].append('IV recalculée depuis le mid (FALLBACK_ESTIMATE)')
    result['model_source'] = 'FALLBACK_ESTIMATE'                      # ← repli ÉTIQUETÉ
if stop:
    result['worst_planned_loss_pct'] = min(stop_pnls)                 # ← calculé SEULEMENT sur un vrai stop
```

Trois lignes au-dessus du repli IV étiqueté, un quatrième repli — **muet** :

```python
em_pct = setup.expected_move_pct
if em_pct is None:
    em_pct = iv * math.sqrt(holding_days / 365.0) * 100     # aucune limitation ajoutée
```

## Ce repli n'est pas un cas de bord : c'est le seul chemin

Les **deux** constructeurs d'`UnderlyingSetup` du dépôt omettent le champ :

```text
vertex/app/routes/options_intel_api.py:107   UnderlyingSetup(symbol, spot, invalidation, tp1, tp2, tp3)
vertex/app/routes/redesign.py:226            UnderlyingSetup(symbol, spot, invalidation, tp1, tp2, tp3)
```

`expected_move_pct` vaut donc **`None` à chaque simulation**, et le mouvement
attendu est **toujours fabriqué par le moteur lui-même**.

## Ce que ça change — mesuré

Contrat identique (strike 150, spot 155, DTE 45, mid 6.00, IV 30 %, stop 145,
TP1-3 170/180/190) ; seul le mouvement attendu varie :

```text
                                    gain BASE    pire perte    R:R      model_source
expected_move_pct = None (PROD)       145.7 %      -40.8 %     3.57     MODEL_ESTIMATE
expected_move_pct =  3.0 %            104.7 %      -40.8 %     2.57     MODEL_ESTIMATE
expected_move_pct =  5.0 %            146.4 %      -40.8 %     3.59     MODEL_ESTIMATE
expected_move_pct =  8.0 %            213.7 %      -40.8 %     5.24     MODEL_ESTIMATE
expected_move_pct = 12.0 %            309.6 %      -40.8 %     7.59     MODEL_ESTIMATE
```

Le moteur fabrique ici **4,97 %** — d'où le R:R de **3,57**. Le même contrat
afficherait **2,57** ou **7,59** selon l'hypothèse. **Le R:R du plan est
entièrement déterminé par une hypothèse que le moteur prend pour lui-même.**

Et les limitations déclarées, dans le cas production, sont exactement les trois
constantes du fichier :

```text
- pricing Black-Scholes européen : ESTIMATION pour des options américaines…
- dividendes intégrés via un rendement continu…
- IV supposée constante par strike (pas de déformation de smile)
```

**Aucune ne mentionne le mouvement attendu.** Vérifié par recherche sur la liste
servie : `False`.

## Où ça s'affiche

```text
vertex/ui/pages/analysis_page.py:631              « R:R »  →  t.reward_risk
vertex/ui/pages/opportunities_page.py:553         « R:R simulé … · perte planifiée … »
vertex/static/vertex/js/pages/options-intel.js:439 « R:R du plan : … »
vertex/static/vertex/js/pages/options-intel.js:431 « Limites méthodologiques » ← la liste EST rendue
```

Le point est là : **la carte affiche la liste des limites, et cette limite-là n'y
figure pas.** Le trader lit une méthodologie qui se présente comme complète.

## Classement — famille du 417, pas du 407

Ce n'est **pas un chiffre faux** : un mouvement attendu déduit de l'IV est
l'estimation standard, et probablement la meilleure disponible. Ce qui manque,
c'est **l'étiquette** — dans un fichier dont c'est le sujet, à trois lignes d'un
repli qui, lui, est étiqueté et dégrade `model_source`.

**Rang 1**, même famille que le 417 (échantillon/hypothèse mal présentés, pas
arithmétique fausse). Correction pressentie, minuscule et déjà écrite juste
au-dessus : ajouter une ligne de limitation — *« mouvement attendu non fourni :
déduit de l'IV (…) »* — et, au choix, dégrader `model_source` comme le fait le
repli IV. **Aucun GO, rien n'est engagé.**

## Portée

Un seul moteur, une seule fonction (`simulate`). Je n'ai pas vérifié que le
mouvement déduit de l'IV soit **numériquement** le bon estimateur — la question
de ce lot est l'étiquetage, pas la formule. `capital_free_analysis` n'a pas été
ouvert au-delà d'un constat : il applique lui aussi un multiplicateur **100 en
dur** (`mid * 100`), même hypothèse qu'au lot 418, dans un autre fichier —
**signalé, non mesuré ici**.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; la sonde importe
  des fonctions pures et un dataclass, et les appelle avec des valeurs
  fabriquées. Pas de preuve MD5 requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-cinquième lot court, sixième dans la veine des moteurs — **cinq trouvailles
sur six lots**, le 421 restant le seul négatif. La veine n'est pas épuisée, et le
compteur annoncé au 421 (deux négatifs d'affilée → le dire ; trois → changer de
famille) **repart à zéro**.

Le motif se vérifie une **cinquième** fois, et c'est ici sa forme la plus nette :
le fichier étiquette un repli, refuse une simulation faute de données, garde un
calcul derrière un vrai stop — **et laisse passer le seul repli qui s'exécute à
chaque appel**.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
