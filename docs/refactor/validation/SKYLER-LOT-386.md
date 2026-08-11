# SKYLER LOT 386 — Les 38 `except: pass` de `terminal.py`, lus un par un

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-386` (base : lot 385 fusionné,
3128135)

## Piste

Le lot 379 avait ouvert un par un les 46 `except: pass` de `vertex/`. Le lot 385
a montré que le recensement s'arrêtait à cette frontière : `terminal.py` en porte
38 que personne n'avait jamais lus. Ce lot les lit.

## Classement par ce que le `try` ENTOURE

```text
nettoyage / fermeture        6   ← cancelMktData ×3, disconnect ×2, reqMarketDataType
journal / persistance       10   ← beats du scheduler, caches, track_record
import / config optionnel    2   ← dotenv, provider JSON
infra thread                 2   ← boucle asyncio, événement de re-scan
absence honnête             16   ← donnée externe manquante → clé/élément OMIS
examinés de près             2   ← L621 et L1342
```

**Trente-six sont sans danger** pour l'invariant n°4 : un échec y produit une
absence, jamais une valeur inventée. Deux méritaient mieux qu'un coup d'œil.

## L621 — l'overlay IBKR : honnête au moteur, muet au produit

`_apply_ibkr_indices()` écrase les indices différés yfinance par les valeurs IBKR
temps réel et marque chaque entrée touchée `src = 'ibkr'` — le commentaire dit
même « provenance temps réel (honnêteté §4) ». Si l'overlay échoue, les entrées
restent **non marquées**. Le mécanisme est complet et correct côté moteur.

**Mais le marqueur n'atteint aucune surface servie.** Mesuré :

- `markets_page.py` et `briefing.py` lisent `.price`, `.change`, `.spark` —
  **jamais `.src`** ;
- le seul rendu de « TEMPS RÉEL IBKR » vs « yfinance différé » du dépôt est dans
  `PAGE_ME` (L4741-5189), **l'une des 7 constantes `PAGE_*` mortes du lot 374**,
  jamais renvoyée par une route ;
- `indices_live` part bien au client (`/scan` sérialise `{**scan_state}`) mais
  **aucun code client ne le lit** — zéro occurrence en Python comme en JS.

Ce n'est **pas** une malhonnêteté : un cours différé reste un cours réel. C'est
la catégorie du lot 382 — **un énoncé du code plus large que ce que le produit
délivre**. Rien à corriger sans décision produit (afficher un badge de provenance
changerait des octets servis).

En revanche la pièce fragile est identifiée : **la fenêtre de fraîcheur de 75 s**.
Si elle grandissait, des valeurs IBKR périmées seraient servies comme du temps
réel — *ça*, ce serait la vraie faute. Le gardien la verrouille, avec le marqueur
lui-même, pour qu'un affichage futur ait quelque chose de vrai à lire.

## L1342 — `bret = 0.0` : mesuré, pas excusé

Dans `edge_backtest`, l'échec du calcul du rendement de référence laisse
`bret = 0.0`, qui part dans `analyse(sub, bret)`. J'allais l'excuser en disant
que 0 est le neutre. **La mesure dit le contraire** — `analysis.py:54` :
`rs = clip(50 + (sym_ret − bench_ret) × 200, 0, 100)`.

```text
sym +0.10   bench réel +0.15 → rs 40    |   bench 0.0 → rs 70
sym −0.05   bench réel +0.12 → rs 16    |   bench 0.0 → rs 40
sym +0.20   bench réel +0.20 → rs 50    |   bench 0.0 → rs 90
```

La force **relative** devient une performance **absolue**. Ce n'est donc pas un
neutre — exactement le piège du lot 378 avec `entry_quality`, où « 50 » n'était
pas le milieu de l'échelle.

Trois faits l'empêchent d'être une faute : `0.0` est le défaut **déclaré** de la
fonction (atteint aussi sans exception quand `bi <= 63`) · le chemin de scan
**vivant** (L395) passe un `bench_ret` réel, donc le repli est confiné au
backtest · `scan_state['edge']` part au client mais **aucune page servie ne le
lit**.

**Caractérisation, pas correction** — jumelle du dossier `context()` du lot 379.
Le gardien fige la sensibilité mesurée pour qu'on ne puisse plus l'innocenter par
un raisonnement élégant.

## Gardien

`tests/test_pass_terminal_lot386.py` (11 tests) : dénominateur (les 38 exacts,
classement complet) · le marqueur de provenance doit survivre · **une valeur IBKR
périmée ne doit pas être présentée comme du temps réel** · anti-dérive de la
fenêtre · l'overlay ne réassigne pas `scan_state` · la sensibilité de `bret`
figée + anti-péremption de la formule · le chemin de scan vivant passe un
rendement réel.

### Preuve ROUGE

```text
marqueur de provenance supprimé                      ROUGE OK  | restauration identique
fenêtre de fraîcheur élargie 75 s → 1 h              ROUGE OK  | restauration identique  (2 tests)
formule de force relative changée                    ROUGE OK  | restauration identique
39ᵉ `except: pass` ajouté                            ROUGE OK  | restauration identique
scan_state réassigné dans l'overlay                  ROUGE OK  | restauration identique  (2 tests)
après restauration : 11 passed
```

## Un test creux, démasqué par sa propre preuve ROUGE

Ma première version de l'anti-dérive testait `'< 75' in src`. La preuve ROUGE l'a
prise en défaut : **la chaîne apparaît 4 fois dans `terminal.py`** (deux autres
fraîcheurs `_live_meta`, plus la docstring), donc élargir la fenêtre de l'overlay
à une heure laissait le test **vert**. Réécrit pour lire la constante **dans le
corps de la fonction, par AST** — il mord désormais. Une mutation qui ne mord pas
accuse d'abord la mutation ; ici, après vérification, elle accusait le test.

## Trouvaille adjacente — la suite de tests écrit dans les données du desk

En vérifiant l'invariant « ne muter aucun fichier runtime », j'ai mesuré :

```text
desk_data.json   avant suite   md5 f30f5d7da49a
desk_data.json   après  suite  md5 c6beebcf97f0     ← RÉÉCRIT
```

**Aucune donnée perdue** : 6 clés avant, 6 après, `data` **byte-identique** — seul
le champ `ts` change. Le risque n'est donc pas réalisé aujourd'hui. Mais il est
réel demain, et le lot 362 l'a déjà caractérisé : un push **partiel** remplace le
blob entier et un push `data: {}` est **accepté** (la validation porte sur le
type, pas le contenu). Un futur test qui pousserait des données partielles
effacerait des clés en silence, et le filet ne rendrait que l'état d'**avant la
première écriture du jour**.

Ce n'est pas la piste de ce lot et je ne l'ai pas engagée. **Elle devient le
16ᵉ dossier**, et c'est la piste que je recommande pour le lot 387 : identifier
quels tests écrivent, et rediriger l'écriture vers un dossier temporaire — c'est
exactement la règle que la boucle s'applique à ses propres sondes.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`.
- `integration/vertex-skyler-v2` à jour (tête = lot 385, 3128135) ; arbre propre,
  **toutes les mutations restaurées** (vérifié à l'octet).
- **Aucun fichier de production touché** — pas de preuve MD5 requise, pas de bump.
- `fund_cache.json` inchangé (`mtime` vérifié). `desk_data.json` réécrit par la
  suite **sans perte** (voir ci-dessus), copie de sûreté prise avant analyse.
- Suite : **2806 → 2817 passed / 2 skipped** (+11). SW : `td-shell-v187`.

## Portée

Les 36 handlers classés « sans danger » l'ont été par lecture de ce que leur
`try` entoure, pas par exécution de chaque chemin d'échec. Le classement est
gelé et sa dérive est gardée ; il n'est pas une preuve que chaque chemin est
inoffensif. Et le verdict sur L621 porte sur les **surfaces servies mesurées
aujourd'hui** — il changerait si une page se mettait à lire `.src`.

## Suite

La piste des 38 est **close** : la dernière question d'honnêteté non tranchée des
pistes fines est répondue. Reste, par ordre d'intérêt : **les écritures de la
suite dans `desk_data.json` (nouveau, recommandé pour le 387)** · refus construits
en variable (377) · formes imbriquées des promesses de retour (375) · trois sites
de concaténation à constantes (374).

Les quinze dossiers en attente de décision humaine n'ont pas bougé — le 16ᵉ les
rejoint. Prochaine échéance périodique : **~lot 390**.
