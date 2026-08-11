# SKYLER LOT 426 — Les affirmations de méthode confrontées à leur code : 6 exactes sur 6, et une septième portée par une carte qui ne s'affiche jamais

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-426` (base : lot 425 fusionné,
32e2afa)

Dixième lot de la veine, deuxième mené **depuis l'écran**. Le lot 425 avait
recensé **17 affirmations littérales rendues** et n'en avait ouvert **qu'une**.
Celui-ci en ouvre **six de plus** — les plus testables : celles qui énoncent une
**formule** ou une **méthode**, donc confrontables ligne à ligne au code qui les
produit.

**Aucun code, aucun gardien, aucun test.** Et **aucun défaut** — c'est un
bornage.

## Les six confrontations

**1. « σ = spot · IV_ATM · √(DTE/365) — estimation lognormale »**
(`options-intel.js:336`, carte « Cône de mouvement attendu »)

```python
# vertex/options/vol_charts.py:73
em = spot * p['iv'] * math.sqrt(max(0, p['dte']) / DAYS_YEAR)
```

**Exacte, terme pour terme.** Les bandes tracées sont bien `spot ± em` et
`spot ± 2·em`, et l'infobulle nomme « 2σ+ / 1σ+ / médian / 1σ− / 2σ− » dans
l'ordre des jeux de données.

**2. « IV ATM approximée par le contrat le plus proche du spot »**

```python
# vertex/options/vol_charts.py:52-55
dist = abs(strike - spot)
if cur is None or dist < cur['dist']:
    by_dte[d] = {'dte': d, 'iv': round(iv / 100.0, 4), …}
```

**Exacte** : par échéance, le contrat retenu est celui de distance au spot
minimale. Le mot « approximée » est justifié — ce n'est pas une interpolation de
smile, et la carte le dit.

**Vérification annexe qui aurait pu mordre** : ce `iv / 100.0` est
**inconditionnel**, alors que `options_intel_api.py:105` normalise, lui,
**conditionnellement** (`iv / 100 if iv > 3 else iv`). Deux conventions dans le
même dépôt pour le même champ. J'ai remonté la chaîne : le producteur du board
écrit `round(float(mg.impliedVol) * 100, 1)` (`terminal.py:897`) — donc **en
pourcentage**, et la division inconditionnelle est **correcte** pour ce
producteur. Le second producteur (`options_lab.py:444`, `(iv or 35) * 1.4`) est
sur la même échelle. **Pas de défaut ; l'alerte était légitime, la mesure l'a
levée.**

**3. « moyenne des % par trade — pas une performance composée »**
(`portfolio_page.py:643`, saisonnalité mensuelle)

```javascript
arr.reduce((a, b) => a + b, 0) / arr.length
```

**Exacte** — moyenne arithmétique des `pnl_pct`, aucune capitalisation. La
précision « pas une performance composée » est **la bonne mise en garde**, et
elle est vraie.

**4. « P&L latent absolu (valeur − coût) »** (`portfolio_page.py:573` et `:655`)

```javascript
// portfolio_page.py:101-104
const value   = mark !== null ? (isOpt ? mark*100*t.qty : mark*t.qty) : null;
const invested = t.cost || 0;
const plAbs   = value !== null ? (value - invested) : null;
```

**Exacte** : littéralement valeur − coût. *(Le `mark*100` pour les options est le
multiplicateur assumé du dossier 418 — signalé là-bas, pas rouvert ici.)*

**5. « force = score moyen · momentum = variation moyenne du jour (univers
scanné) »** (`markets_page.py:697`, nuage des secteurs)

```python
# vertex/market/sectors.py:51 et :68
avg_score  = round(sum(i.get('score', 0) for i in items) / n)
avg_change = round(sum(i.get('change', 0) for i in items) / n, 2)
```

**Exacte pour les deux axes.**

**6. « historique breadth de l'univers scanné (partiel, pas tout le NYSE) »**
(`markets_page.py:764`)

**Exacte, et remarquable** : c'est une limite que rien n'obligeait à écrire.
L'aveu est volontaire.

## La septième — et c'est le seul point à signaler

**« Dérivé arithmétiquement de la courbe d'équité »** (`portfolio_page.py:616`,
conclusion de la carte drawdown), accompagnée de **« dérivé de la série déclarée
— pas un indicateur de marché »** (`:618`).

L'affirmation est **juste sur le fond** : le drawdown est bien dérivé de la série
d'équité. Mais le lot 406 a mesuré que `myTradesEquity` **n'a aucun écrivain**, et
le lot 411 en a tiré la conséquence : **cette carte n'est jamais rendue**. Deux
affirmations méthodologiquement correctes, portées par une carte que personne ne
voit.

**Ce n'est pas un défaut nouveau** — c'est le dossier 406/411, retrouvé par un
autre chemin. Je le note comme **recoupement**, pas comme trouvaille.

## Le bilan de la mesure

```text
affirmations littérales rendues (recensées au 425)        17
   ouvertes au 425                                         1   → FAUSSE (« 4 maturités réelles »)
   ouvertes ici                                            6   → 6 EXACTES
   portée par une carte inatteignable                      1   → recoupement 406/411
   non ouvertes                                            9
```

**Sur sept affirmations confrontées à leur code, six sont exactes et une est
fausse.** Le contrat d'honnêteté des cartes tient donc largement — et le défaut
du 425 en ressort mieux caractérisé : ce n'était pas un symptôme d'un texte
négligé, c'était **une exception dans un ensemble rigoureux**.

## Portée

Les **neuf** affirmations restantes ne sont **pas** vérifiées : elles décrivent
des conventions d'affichage (« Chaque indice rebasé à 0 % », « Vert = flux
entrant… »), un conseil (« Time stop conseillé : réévaluer après 5-8 séances »)
ou des périmètres déjà couverts. Le recensement lui-même reste borné aux
littéraux `limits:`/`conclusion:` de 15 à 150 caractères — les `question:`,
`explain.shows` et les phrases construites dynamiquement lui échappent, et n'ont
pas été comptés.

Pour la confrontation n°1, la mesure est **statique** : le board d'options est
vide au démarrage, je n'ai donc **pas** exécuté le cône sur des contrats réels.
La formule a été comparée au code, pas à une sortie.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — `git status` vide de bout en bout. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels restaurés. Écart final **aucun**.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Où en est la boucle

Vingt-neuvième lot court. Séquence de la veine : **416 ✓ · 417 ✓ · 418 ✓ · 419 ✓ ·
421 ✗ · 422 ✓ · 423 ✗ · 424 ~ · 425 ✓ · 426 ✗ (bornage)**.

Ce lot ne trouve rien, et c'est le bon résultat : après une trouvaille, **borner**
dit si le défaut était une exception ou un symptôme. Ici, **exception** — six
affirmations sur sept sont exactes, dont deux qui s'auto-limitent sans y être
obligées.

La méthode « partir de l'écran » reste la bonne : elle a produit une trouvaille
(425) puis un bornage propre (426) en deux lots, là où les trois lots partis du
moteur butaient sur l'inatteignable.

**Trois bilans — n°9, n°10, n°11 — attendent une réponse.**
