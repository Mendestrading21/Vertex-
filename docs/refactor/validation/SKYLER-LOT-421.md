# SKYLER LOT 421 — Le scoring note un dict vide « D, confiance 58 » — mais la mesure a réfuté mon hypothèse, et la chaîne a fermé le dossier

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-421` (base : lot 420 fusionné,
63cb9f5)

Cinquième lot dans la veine des moteurs. Cible : `vertex/quant/scoring.py`, qui
produit le **score global, la note et la confiance** de chaque titre.

**Aucun code, aucun gardien, aucun test.** Et, cette fois, **aucun défaut
produit** — c'est le résultat.

## La règle que le fichier respecte — et l'endroit où il ne la tient qu'à moitié

Le fichier porte son propre contrat d'honnêteté, ligne 136 :

```python
out['fundamental_is_proxy'] = not fund_real   # honnêteté : signale si le fondamental est un proxy
```

Il **sait** qu'un sous-score peut être une hypothèse plutôt qu'une mesure, et il
le **déclare**. La question devient : le fait-il pour les quatre ?

Non. Les trois autres sous-scores prennent des valeurs par défaut silencieuses —
`ind.get('rsi', 50)`, `ind.get('volx', 1.0)`, `ind.get('atr_pct', 2.0)` — et
**rien ne signale qu'ils ont servi**.

## Ce que rend le moteur sur un dict vide — mesuré

```text
compose({})   global=40  grade=D  confidence=58
              technical=18  momentum=50  fundamental=45  risk=64
              fundamental_is_proxy=True     ← le seul drapeau, et il est correct
```

**Un verdict complet, noté et chiffré, sur rien du tout.** Le détail des points
gagnés par les seules valeurs par défaut :

```text
technical_score({})   = 18.0     rsi=50 → +12 (bande 45-70) · volx=1.0 → +6
   les mêmes clés fournies au pire réel (rsi=10, volx=0.0)   = 0.0
momentum_score({})    = 50.0     neutre par construction
risk_score({})        = 64.0     atr_pct=2.0 → 72 − 8
fundamental_score({}) = 45.0     proxy — et c'est SIGNALÉ
```

Comparaison directe, tous les booléens à `False` dans les deux cas :

```text
mesures RÉELLES au pire (rsi 10, roc −25, rs 0, atr 10 %)   global=11  tech=0   mom=0   risk=42
mesures ABSENTES (clés retirées)                            global=40  tech=18  mom=50  risk=64
```

**L'absence de mesure vaut 29 points de plus que la pire mesure réelle.**

## Mon hypothèse était que la confiance s'inversait. La mesure l'a réfutée.

J'ai supposé que `confidence = 100 − min(std(sous-scores) × 2.5, 60)` rendrait sa
**valeur maximale** sur un dict vide — puisque des valeurs par défaut sont peu
dispersées. C'était une explication séduisante. Elle est **fausse** :

```text
aucune donnée                       confidence = 58
cas réel cohérent (haussier net)    confidence = 66      ← PLUS confiant
cas réel contradictoire             confidence = 40      ← MOINS confiant
```

La confiance se comporte correctement : elle est plus haute quand les
sous-scores concordent réellement, plus basse quand ils se contredisent, et
intermédiaire sur des valeurs neutres. **Je ne publie donc pas ce défaut, parce
qu'il n'existe pas.**

*Une hypothèse d'explication doit être testée, pas narrée* — la règle a servi
exactement à cela ici, et elle a coûté une trouvaille annoncée.

## La chaîne ferme le dossier

Reste à savoir si un dict incomplet peut atteindre `compose()`. **Un seul
appelant** dans tout le dépôt :

```text
vertex/engines/analysis.py:203    sc = scoring.compose(ind, fund=fund)
```

et le `ind` construit deux lignes plus haut porte **les douze clés, toujours** —
elles sont calculées inconditionnellement à partir de la série de prix.

**Les valeurs par défaut de `scoring.py` ne sont donc jamais utilisées en
production.** Le comportement mesuré ci-dessus est **inatteignable aujourd'hui**.

## Verdict du lot

**Lot négatif sur le produit, et c'est un résultat.** Ce qui reste est une
caractérisation utile, pas un défaut :

- `compose()` **note volontiers le vide** — verdict D, confiance 58, sur zéro
  mesure ;
- le contrat d'honnêteté du fichier couvre **un sous-score sur quatre** ;
- mais **le seul appelant fournit toujours tout**, donc rien n'est faux à
  l'écran.

Le module se présente comme **pur et réutilisable** (« Pures = testables », liste
des clés attendues en tête de fichier) : c'est une invitation à un second
appelant, qui recevrait alors une note sans savoir qu'elle repose sur des
valeurs par défaut. **Classé rang 4** — piège latent dans un module conçu pour
être réutilisé, aucune conséquence actuelle. **Aucun GO, rien n'est engagé.**

## Portée

Un seul moteur, une seule fonction d'entrée (`compose`). La vérification de la
chaîne s'arrête au constructeur d'`ind` : je n'ai pas vérifié que les douze
valeurs soient toujours **numériquement saines**, seulement qu'elles sont
**toujours présentes**. Et `options_score` n'a pas été ouvert — il reçoit `None`
sur ce chemin.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; la sonde importe
  des fonctions pures et les appelle avec des dicts fabriqués. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-quatrième lot court, cinquième dans la veine des moteurs. Après quatre
trouvailles (416-419), **celui-ci n'en produit pas** — et il faut le dire ainsi
plutôt que de gonfler une caractérisation en défaut.

La veine n'est pas épuisée pour autant : un seul lot négatif, et il a **réfuté
une hypothèse fausse avant publication**. C'est la troisième fois d'affilée dans
cette veine que la mesure **réduit** ce que j'allais écrire (416, 418, 419) — et
la première où elle l'annule.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
