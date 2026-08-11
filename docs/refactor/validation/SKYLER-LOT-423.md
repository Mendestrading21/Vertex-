# SKYLER LOT 423 — « clôture sous $None (structure) » : le comité sait dire « — », sauf sur son invalidation — et la chaîne referme le dossier

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-423` (base : lot 422 fusionné,
50a32dc)

Septième lot dans la veine des moteurs. Cible : `vertex/engines/committee.py` —
le comité qui rend **ACHETER / RENFORCER / ATTENDRE / ÉVITER** avec thèse, plan
et **invalidation**, affichés sur « Aujourd'hui ».

**Aucun code, aucun gardien, aucun test.** Et **aucun défaut produit** — c'est le
résultat, pour la seconde fois dans cette veine.

## La règle que le fichier respecte

Le comité affiche des textes destinés au trader, et il sait déjà remplacer une
donnée absente par un tiret :

```python
note = f"Qualité insuffisante (score {score}, {grade or '—'}) — hors critères."
bits.append(f"momentum {d.get('mom', '—')}/100, force rel. {d.get('rs', '—')}")
```

Mesuré, `grade=None` → *« score 70, **—** »*, et `rs` absent → *« force rel.
**—** »*. La règle est là, et elle marche.

## L'endroit où il ne la tient pas

Une ligne plus bas, l'**invalidation** — la phrase qui dit au trader à quel prix
sa thèse est morte :

```python
invalidation = f"clôture sous ${plan.get('stop')} ({plan.get('stop_type', 'structure')})"
```

Mesuré, en faisant varier le seul plan :

```text
plan complet (stop 92, type ATR)     « clôture sous $92.0 (ATR) »
stop_type ABSENT                     « clôture sous $92.0 (structure) »   ← type INVENTÉ
stop ABSENT                          « clôture sous $None (structure) »
plan VIDE                            « clôture sous $None (structure) »
plan absent (clé manquante)          « clôture sous $None (structure) »
```

Deux choses distinctes : le prix devient le mot **`None`** à l'écran, et le
**type de stop est affirmé** — « structure » — alors qu'il n'a jamais été
calculé. Le second est plus grave que le premier : `$None` se voit, « structure »
se croit.

## Le détail le plus fin — dans une seule ligne

Mon témoin a révélé mieux que ce que je cherchais :

```text
d.get('mom', '—')  avec mom = None   →  « momentum None/100 »
d.get('rs',  '—')  avec rs  ABSENT   →  « force rel. — »
```

**Même f-string, même forme, deux comportements** : `d.get(clé, '—')` ne protège
que de la **clé absente**, jamais d'une **valeur présente valant `None`**. C'est
l'instance la plus resserrée du motif de la veine — la bonne pratique et sa
faille tiennent sur la même ligne.

## La chaîne referme le dossier

Le seul producteur du `detail` consommé par le comité est
`vertex/engines/analysis.py`, et il remplit tout, inconditionnellement :

```text
analysis.py:260-263   plan = {'entry': …, 'stop': round(stop, 2), …, 'stop_type': stop_type, …}
analysis.py:304       'mom': round(mom), 'rs': round(rs), 'rsi': round(r)
terminal.py:608       committee.evaluate(rows, detail, …)     ← unique appelant
```

`stop`, `stop_type` et `mom` sont **toujours présents et jamais `None`**. Les cas
mesurés ci-dessus sont donc **inatteignables aujourd'hui**.

## Verdict du lot

**Négatif sur le produit.** Ce qui reste :

- une phrase d'invalidation qui **affirmerait un type de stop non calculé** et
  afficherait `$None`, si un jour un second producteur de `detail` apparaissait ;
- un `d.get(clé, '—')` qui ne couvre pas la valeur `None`, sur la même ligne
  qu'un usage correct.

**Rang 4** — pièges latents, aucune conséquence actuelle, exactement la même
nature qu'au lot 421. **Aucun GO, rien n'est engagé.**

## Ce qu'il faut dire sur la cadence

Séquence de la veine : **416 ✓ · 417 ✓ · 418 ✓ · 419 ✓ · 421 ✗ · 422 ✓ · 423 ✗**.
Ce n'est **pas** deux négatifs d'affilée — le compteur repart de 1, et je le dis
plutôt que d'arrondir dans un sens ou dans l'autre.

Mais il y a un signal plus utile que le compteur : **les deux lots négatifs ont
la même forme** — un défaut réel dans le code, rendu inoffensif par un producteur
unique qui remplit tout. Les moteurs sont honnêtes **sur leurs entrées réelles** ;
ce qui reste se trouve dans des branches que rien n'atteint. **Si le 424 rend une
troisième fois ce même verdict, la veine devra être déclarée épuisée** — non
parce qu'elle ne trouve rien, mais parce qu'elle ne trouve plus que de
l'inatteignable.

## Portée

Un seul moteur, une seule fonction (`_evaluate_one`), et son unique chaîne
d'alimentation. Je n'ai pas vérifié les branches de verdict une par une — le lot
416 avait déjà ouvert celle du RSI, et le reste n'a pas été rejoué ici.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout ; la sonde importe
  une fonction pure et l'appelle avec des dicts fabriqués. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-sixième lot court. Cinq trouvailles et deux négatifs sur sept lots dans
cette veine. Le motif tient toujours — *la règle que le fichier respecte
ailleurs* — mais il désigne de plus en plus souvent du code que la production
n'emprunte pas.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
