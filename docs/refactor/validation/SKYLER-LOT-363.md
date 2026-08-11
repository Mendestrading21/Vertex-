# SKYLER LOT 363 — Règle n°4 : la seule règle qui tient déjà, et le gardien qui l'empêche de se reperdre

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-363` (base : lot 362 fusionné,
f9ebd3f)

## Piste calibrée

Cinquième et dernier passage de la question qui a donné les lots 358, 359, 361
et 362 — « la règle écrite décrit-elle vraiment le code servi ? » — sur la
**règle n°4** : « données RÉELLES uniquement ; jamais de chiffre inventé
affiché comme réel ; donnée absente → `—`/`n/d` honnête ; le mot « démo » ne
s'affiche que si le serveur le confirme ».

## Verdict : SAINE — et c'est prouvé, pas supposé

### 1. Les données DEMO sont bien synthétiques, et le serveur le dit

`terminal.py` : en DÉMO, `data = _demo_universe(_syms)` puis
`scan_state['source'] = 'demo'`. Mesuré sur le serveur DEMO :

```text
source du scan : demo | lignes: 20
macro : [{"id": "^IRX", "name": "Taux 3 mois", "value": 35.6, …}]
```

Un taux 3 mois à **35,6 %** : la donnée est manifestement fabriquée. La
question n'est donc pas « est-ce inventé » (ça l'est, c'est la vitrine) mais
**« l'utilisateur est-il prévenu partout »**.

### 2. Les 8 pages préviennent, en navigateur, après hydratation

| page | mentions visibles | extrait |
|---|---|---|
| `/` | 6 | « **DÉMO** Données synthétiques clairement identifiées — jamais présentées comme réelles. » |
| `/markets` | 13 | idem |
| `/opportunities` | 8 | « Mode **DÉMO** — données synthétiques, clairement identifiées. » |
| `/portfolio` | 2 | « DELAYED **DÉMO** 2 300 de valeur nette · P&L latent indisponible » |
| `/options` | 4 | « Payoff & greeks : moteur multileg_lab (**board démo**) » |
| `/journal` | 3 | badge **DÉMO** sur les décisions |
| `/system` | 5 | « Données marché **demo** · Mode global **demo** » |
| `/analysis` | 1 | chip « Mode démo » de la nav |

`/analysis` (index) n'a qu'une mention parce que c'est une page de **recherche**
— elle n'affiche aucune donnée de marché. Cohérent, pas une lacune.

Le « board démo » de `/options` est le correctif du lot 296 ; il tient toujours.

### 3. Les étiquettes de provenance sont dérivées du serveur

Chaque carte porte un couple `source:` / `mode:` — le seul endroit où une
chaîne peut mentir sur la réalité d'un chiffre. Recensement sur les sources
servies (hors Widget Lab, référence de design) :

```text
couples source:/mode: servis — DÉRIVÉS : 31 · CONSTANTS : 59
CONSTANTS qui AFFIRMENT réel/live : 0
```

Les 59 constants sont tous prudents : `mode` vaut `delayed` ou `index`,
`source` nomme un moteur ou un journal (`board options`, `scenario_pricer`,
`moteur track-record`, `journal local`…). **Aucun** n'affirme `réel`, `live`,
`broker` ni `IBKR`. Les cartes de marché tirent leur source de la charge
serveur : `source:(scan&&scan.source)||'scan'` — donc « demo » quand le serveur
le dit.

## Ce que le lot livre

La règle tient, mais elle s'est **déjà perdue deux fois** :
lot 296 (« board réel » codé en dur, affiché en DÉMO) et lot 297 (chip « Live »
codé en dur, affiché sur des cotes de repli). Rien n'empêchait une troisième
fois.

**Gardien neuf** `tests/test_honnetete_provenance_lot363.py` (4 tests) :

1. anti-vide (≥60 couples analysés, dérivés **et** constants présents) ;
2. aucun `mode:` constant hors des valeurs prudentes — seul un mode **calculé**
   peut annoncer du live ;
3. aucune `source:` constante n'affirme réel/live/broker/IBKR ;
4. contre-preuve : `markets_page` et `opportunities_page` dérivent bien au moins
   une source du serveur.

### Preuve ROUGE — les deux fautes historiques rejouées

```text
ROUGE OK     faute du lot 297 rejouée : chip « Live » codé en dur | restauration identique
ROUGE OK     faute du lot 296 rejouée : « board réel » codé en dur | restauration identique
VERDICT : les deux fautes historiques sont désormais attrapées
```

## Une observation, pas un défaut

Sur `/markets`, la carte de la courbe des taux porte les textes
« 4 maturités réelles (3M/5A/10A/30A) » et « points réels du scan, non
interpolés ». Ces « réels » parlent de **méthode** (maturités effectives, pas de
points interpolés), pas de provenance — et la carte affiche par ailleurs
`source: demo` en mode démo, la page portant le badge DÉMO. Ce n'est donc pas
une fausse affirmation, mais le mot est ambigu à côté d'un badge « démo ».
**Rien changé** : reformuler (« 4 maturités du scan », « points non
interpolés ») serait un octet servi modifié pour une question de style — à vous
de trancher.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 362, f9ebd3f) ; arbre propre.
- Serveur DEMO + navigateur réel (Chromium 1440×900, après hydratation) sur les
  8 pages.
- Suite complète : **2516 → 2520 passed / 2 skipped** — verte.

## Décision SW

**Pas de bump** (`td-shell-v187`) : le lot ne touche que `tests/` et `docs/` —
aucun octet servi, `/static` inchangé.

## Bilan des 5 règles passées à la question

| Règle | Verdict |
|---|---|
| n°2 — JS valide (lot 359) | **trou** : `/analysis` hors des gardiens |
| n°3 — service worker (lot 361) | **trou** : périmètre réel = tout `/static` |
| n°4 — données réelles (lot 363) | **saine**, prouvée en navigateur ; gardée désormais |
| n°5 — news (lot 358) | **trou** : deuxième famille de sorties non gardée |
| n°6 — desk (lot 362) | **saine** mais promesse plus étroite que la règle écrite |

Quatre trouvailles sur cinq règles. La n°1 (clés de sync desk) reste, mais elle
a déjà été auditée aux lots 323/327 et porte deux gardiens.

## Suite

LOT 364 : veille active — la veine « règle écrite vs code servi » est épuisée
sur les règles de `CLAUDE.md`. Piste suivante possible : appliquer la même
question aux **docstrings de modules** (le lot 71 avait trouvé un gardien
inexistant cité dans une docstring). Prochaine échéance périodique : ~lot 370.
