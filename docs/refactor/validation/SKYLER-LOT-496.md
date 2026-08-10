# SKYLER LOT 496 — La veine des barèmes définitivement close : `edge /100` est SAIN, il atteint 100 et S+ — mais le second contrôle montre que le R:R du moteur est une TAUTOLOGIE, et que « R:R visé » affiche un score /100 sous une étiquette de ratio

Date : 2026-08-10 · Branche : `agent/skyler-v2-lot-496` (base : lot 495 fusionné,
`8664d8e4`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le 495 avait nommé sa dette : « la veine est close **à un barème près** ».
**Dixième dette nommée payée d'affilée** — et pour la dixième fois, ce n'est pas
la cible qui rend le résultat.

## Règle 491 d'abord — l'objet mesuré est-il l'objet affiché ?

Fait **avant** tout banc, et cette fois sans y perdre un lot :

```text
opportunities_page.py:119   metric('Edge composite', edge+'/100')   edge = best.vx_edge
terminal.py:429             'vx_edge': _vx.get('edge')              _vx = detail['vertex']
analysis.py:321             result['vertex'] = vertex.evaluate(result)   ← quant_engine

scan DEMO : vx_edge NON NUL sur 20 titres / 20        → l'objet est bien peint
```

## Le banc — et un dimensionnement que j'ai dû jeter

Ma première grille faisait **1 119 744 combinaisons**, chacune passant par un
Monte-Carlo à 1 200 chemins. **Des heures de calcul.** Je l'ai tuée et
restructurée en deux passes : les cinq termes seuls sur la grille complète
(arithmétique pure, **16,5 s**), puis `evaluate()` complet sur **1 604
configurations ciblées** (argmax de la passe 1 + échantillon, **3,7 s**). Rien de
faux n'a été publié — mais **j'ai dimensionné avant de mesurer le coût**, alors
que la ligne de chronométrage était déjà dans le script.

**Calibration écrite dans le banc**, deux réponses, sortie programmée :

```text
(A) RÉPONSE CONNUE, calculée à la main sur trend_quality :
    18 + 14 + 16 + 12 + 12 + 16 + 8 + 8 = 104 → clamp 100      MESURÉ 100   OK
(B) VALIDITÉ DE GRILLE (leçon 495) : chacun des CINQ termes doit atteindre son
    propre maximum, sinon toute borne est un artefact de grille.
```

## Le résultat : le barème est SAIN

```text
tq 100 · eq 100 · rr 100 · em 100 · inst 99

edge AVANT Monte-Carlo   MIN 23 · MAX 100
edge COMPLET (1 604 cfg) MIN 32 · MAX 100        verdict au max : VERTEX S+
verdicts atteints        S+ · BUY · WATCH · WAIT · AVOID   — les CINQ
```

`edge` atteint **100/100**, tous les paliers du verdict sont atteignables, **y
compris `VERTEX S+` (edge ≥ 82)**, la quatrième échelle S+ du dépôt. **Aucun
plafond, aucun bloc bridé, aucune borne morte.** La veine des barèmes est
**close**.

## Un faux résultat arrêté : `inst` ne plafonne PAS à 99

La calibration (B) a mordu : `institutionality` s'arrêtait à **99**, et j'allais
écrire « un cinquième terme plafonné ». Vérifié à la main sur le code —
`_clamp((volx − 0.8) × 12, 0, 15)` — puis par exécution :

```text
volx = 2.0  (ma grille)  → (1.2)×12 = 14,4  → inst 99
volx = 2.5               → 15               → inst 100     ← vérifié
```

**C'était ma grille, pas le moteur** (règle 459). Sans la calibration (B), je
publiais un cinquième plafond inexistant.

**Arrêtés avant publication : 68 → 69.**

## Le second contrôle — ce que le banc EXCLUAIT, et il trouve

Mon banc **fabrique** les champs du détail. Il exclut donc deux questions que
seule la production peut trancher : *ces champs sont-ils réellement remplis ?* et
*que valent les cinq termes sur de VRAIS détails ?*

**Premier volet — les entrées sont bien nourries.** Contrairement au 495, aucun
champ mort : les **16 champs** lus par les cinq termes (`price`, `ma20/50/200`,
`rs`, `roc`, `adx`, `chop`, `volx`, `rsi`, `ext_atr`, `setup_quality`, `regime`,
`pos52`, `score`, `plan`) sont présents **20/20**.

**Second volet — et c'est là que ça tombe.** Les cinq termes sur les 20 détails
réels :

```text
        min    max   valeurs distinctes
tq      7,0   70,0        15
eq     41,0   91,0        14
rr      3,0   64,0        11
em     72,0  100,0         4
inst   10,0   44,0        15
edge   45,0   65,0        14

rr1 / rr2 / rr3  →  UNE SEULE valeur distincte sur 20 titres : (1.0, 2.0, 3.0)
```

### Le R:R du moteur est une tautologie — dossier 442 ÉTENDU

`analysis.py:260-262` construit le plan ainsi :

```python
plan = {'entry': last, 'stop': stop,
        'tp1': last + risk, 'tp2': last + 2 * risk, 'tp3': last + 3 * risk,
        'rr': 3.0, …}
```

et `quant_engine.rr_score` recalcule `rr1 = (tp1 − entry) / risk`, etc.

**Il recalcule des cibles qu'il a lui-même définies comme entrée + k × risque.**
Le résultat est **(1, 2, 3) par construction, pour tout titre, toujours** —
mesuré 20/20, et structurel, pas un artefact de démo : la formule est dans le
moteur, pas dans les données.

Le dossier **442** (« `rr` constant à 3 », rang 1, reconfirmé au 493) disait :
*un littéral constant*. **Ce lot montre que c'est plus large** : ce n'est pas
seulement le champ `rr` qui est figé, c'est **toute l'échelle de cibles**. Le
moteur ne peut structurellement pas exprimer un autre rapport rendement/risque.
**442 n'est pas un nouveau dossier — il est requalifié, et il pèse plus lourd
qu'écrit.**

Conséquence mesurée sur `rr_score` : il **varie** (11 valeurs distinctes, 3 à
64), mais **uniquement par le plafonnement par la résistance**
(`if entry < res < tp2: real_target = res`). Autrement dit, **il mesure où se
trouve la résistance, pas le rendement/risque.**

## DOSSIER 496-A, RANG 2 — « R:R visé » affiche un score /100

Sur `/opportunities`, **quatre sites** affichent `vx_rr`, qui est `rr_score`,
**une note de 0 à 100** :

```text
:118  metric('R:R visé', VX.fmt.nd(rr))              carte dominante   rr = best.vx_rr
:150  « R:R ${r.vx_rr} »                             shortlist
:167  ['rr','R:R visé', r=>r.vx_rr, …]               colonne de tableau
:289  <span class="k">R:R visé</span>… d.rr          (:271 pose rr: r.vx_rr)
```

**« R:R » est, en langage de trader, un RAPPORT.** Le chiffre affiché est une
note. Sur la même carte, « Edge composite » porte bien **`/100`** — « R:R visé »
et « Asymétrie » ne portent **rien**.

Le vrai rapport existe : `rr_detail = {rr1, rr2, rr3}`. **Mesuré dans les octets
servis : `rr_detail`, `rr1`, `rr2`, `rr3` → 0 occurrence.** Il est calculé et
jeté.

**Pas d'atténuation utilisable.** `/analysis/AAPL` affiche bien
« R:R structurel 3 » (`plan.rr`) — mais c'est une **autre page**, et la règle 487
est explicite : une atténuation doit être sur la **même vue**. Elle ne compte
pas. Pire, elle aggrave : le même concept vaut **3** sur une page et **64** sur
l'autre.

**Rang 2, et je dis pourquoi pas rang 1** : le chiffre est ambigu, pas faux, et
« 64 » ne peut pas se lire comme un rapport plausible — un trader ne va pas
prendre 64:1 au sérieux. Il est privé d'une information, il n'est pas conduit à
une décision erronée. **Ne pas gonfler** (règle 492).

## Portée

- Le plafond 100 de `edge` est **atteint** par la passe 2 : la borne haute est
  **exacte** (règle 494), pas seulement une borne inférieure.
- La passe 2 tourne sur **1 604 configurations ciblées**, pas sur la grille
  complète : les **comptes** de verdicts (S+ 188, BUY 525, …) décrivent **mon
  échantillon**, pas une distribution. Je les donne comme preuve
  d'atteignabilité, **jamais comme fréquence**.
- Les cinq termes sur détails réels sont mesurés sur les **20 titres du scan
  DEMO** : c'est une distribution de démonstration (règle 495). **La tautologie
  du R:R, elle, ne dépend pas de la démo** — elle est lue dans le code du moteur.
- Le Monte-Carlo est stochastique ; graine fixée à 496 pour la reproductibilité.
- **Aucun navigateur ouvert** : `/opportunities` est peint par `/scan`, sûr, mais
  le lot n'avait rien à vérifier au rendu que les octets servis n'établissent
  déjà. Je le note plutôt que de le présenter comme une contrainte.
- Le dossier **442 est requalifié, pas dupliqué** : la feuille reste à 25 + 1.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties de script en
  chemin **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** à chaque banc ; scans DEMO **en mémoire** ;
  **aucune route réseau sortante** — `/api/ticker/<sym>` inclus (règle ajoutée
  au 495).
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime **avec copie du contenu** : 22 fichiers, écart final
  **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

La veine ouverte au 486, nettoyée au 491, tracée au 492, bornée au 495, est
**close au 496**. Sur les sept barèmes annoncés, **deux étaient des homonymes,
deux n'étaient pas des barèmes, un était un doublon, et les deux vrais sont
sains.** C'est un résultat de bornage complet, et il a coûté cinq lots.

Ce que la fermeture rapporte est ailleurs, et c'est la dixième fois : **le second
contrôle trouve ce que la cible ne contenait pas.** Ici, que le moteur calcule un
rapport rendement/risque qu'il a lui-même rendu constant, et qu'il affiche une
note là où il annonce un ratio.

Feuille : **26 dossiers** — 25 + le **496-A rang 2** — dont **quinze rang 1** et
**neuf rang 2**. Le **442 est requalifié** (plus large qu'écrit), pas dupliqué.

Comptes séparés : résultats faux **arrêtés avant publication 69 (+1)** ; publiés
puis corrigés **11** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**
