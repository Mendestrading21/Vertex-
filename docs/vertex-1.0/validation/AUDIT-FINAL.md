# Audit final — tout a-t-il vraiment été fait ?

Date : 19/08/2026 · SHA audité : `16ec829` (`integration/vertex-1-0-rc`)

Cet audit **rejoue les instruments** au lieu de relire leurs rapports. La
distinction n'est pas rhétorique : une preuve peut devenir fausse sans que
personne ne touche au produit, et c'est exactement ce qui s'est produit ici.

---

## 1. État du dépôt

| contrôle | résultat |
| --- | --- |
| branche | `integration/vertex-1-0-rc` |
| arbre de travail | propre, rien de non commité |
| écart avec `origin` | 0 / 0 — tout est poussé |
| `origin/main` | `28343ec` |
| la RC contient-elle tout `main` ? | **oui** — fusion en avance rapide possible |
| avance de la RC | 110 commits |
| branches distantes | 700 |

## 2. Suite et compilation

```
python -m compileall -q terminal.py vertex   → 0
python -m pytest tests/ -q                   → 3 487 passed, 0 ignoré
```

## 3. Les treize instruments, rejoués

| instrument | sortie | verdict |
| --- | --- | --- |
| `inventaire_runtime` | 0 | — |
| `inventaire_domaines` | 0 | — |
| `mesurer_registre_jobs` | 0 | — |
| `mesurer_track_record` | 0 | — |
| `mesurer_moteurs` | 0 | — |
| `mesurer_branches` | 0 | — |
| `mesurer_exploitation` | 0 | **0 anomalie** |
| `mesurer_rollback` | 0 | 7 clés relues à l'identique — **après correction du banc** |
| `mesurer_qa_espaces` | 0 | débordements 0 · sans anneau 0 · contraste 0 · erreurs 0 |
| `mesurer_qa_degrade` | 0 | verbes d'ordre 0 · anomalies de fraîcheur 0 · symbole inconnu 0 |
| `mesurer_couche_visuelle` | 0 | mouvement malgré `reduce` : 0 |
| `mesurer_regles_mortes` | 0 | recensement gelé, aucune suppression |
| `mesurer_hors_ligne` | 0 | 15 chiffres datés · **0 daté faux** · **0 nu** |
| `mesurer_g5_live` | **3** | TWS injoignable — **rien n'a été mesuré**, et c'est le comportement voulu |

## 4. Ce que l'audit a trouvé

### Une preuve devenue fausse en silence

`mesurer_rollback` est sorti en **3** : « la version antérieure NE DÉMARRE
PAS ». Le produit n'y était pour rien. Deux causes empilées :

1. **`origin/main` a bougé** — la base commune de retour est passée de
   `d52a39d` à `28343ec`, soit 110 commits en arrière au lieu de quelques-uns ;
2. à cette distance, **`python -m vertex` n'existait pas encore**
   (`vertex/__main__.py` absent) : le lancement se fait par `python
   terminal.py`. Le banc supposait le mode de lancement au lieu de le lire.

C'est le mode de panne le plus vicieux d'un instrument : il ne se trompe pas
quand on l'écrit, il **devient faux plus tard**, quand la cible s'éloigne. Aucune
relecture de rapport ne l'aurait montré. Corrigé (mode de lancement dérivé de
l'arbre cible), remesuré : **rollback prouvé sans perte sur 110 commits**, les 7
clés du bureau relues à l'identique. Gardien ajouté, mutation vérifiée.

### Rien d'autre

Les douze autres instruments sortent en 0, et `mesurer_g5_live` sort en 3 pour
la bonne raison : il refuse de conclure sans broker.

## 5. Les gates, adossés à ces mesures

| gate | état | reste |
| --- | --- | --- |
| G0 Fondation | **PASS** | — |
| G1 Runtime | preuves complètes | acceptation humaine |
| G2 Données | preuves complètes | acceptation humaine |
| G3 Intelligence | **partiel** | spécimen de brief WMB réel |
| G4 Expérience | preuves complètes | résidu assumé : 2 fils tronqués (~12 px) |
| G5 Live read-only | **VIDE** | **TWS réel — seul blocage de `v1.0.0`** |
| G6 Exploitation | preuves complètes | CVE hors d'atteinte (politique réseau) |
| G7 Release | **NON** | G5, puis acceptation du SHA |

## 6. Ce qui reste, et à qui

**Toi seul peux :**

1. **Ouvrir TWS et lancer `python tools/vertex_1_0/mesurer_g5_live.py`.** C'est
   le seul blocage de la release. G5 n'attend pas une formalité : il est vide.
2. **Fournir un spécimen de brief WMB réel** (G3).
3. **Accepter le SHA `16ec829` et autoriser la fusion vers `main`** — techniquement
   une avance rapide, mais la mise à jour de `main` demande ton accord explicite.
4. **Fournir des identifiants autorisant la suppression de références** : les 32
   branches sont prouvées sans perte et le registre de restauration est écrit,
   mais la suppression a été refusée en **HTTP 403** (le jeton pousse, il ne
   supprime pas). Ce n'est pas un accord qui manque, c'est un droit.
5. **Trancher sur `performance_ledger`** : le brancher ou le retirer (D-015).
6. **Trancher la fusion des gardiens Signal OS absents de cette branche** — dont
   la liste blanche AST des capacités IBKR, qui a attrapé une régression réelle
   pendant ces travaux et qui n'existe pas ici.

**Rien n'attend de mon côté** : tout ce qui était mesurable sans TWS, sans
compte réel et sans droits supplémentaires est mesuré, corrigé et gardé.

## 7. La limite de cet audit

Il porte sur ce qui est **mesurable dans cet environnement** : sans broker, sans
marché ouvert, sans base de CVE, sans navigateur humain. Il ne dit rien de
l'esthétique, ni du confort d'usage, ni de la justesse *financière* des moteurs
— seulement que les invariants tenus par des gardiens le sont toujours, et que
les instruments qui les mesurent ne sont pas aveugles.
