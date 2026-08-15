# SIGNAL OS · LOT 05 — PORTEFEUILLE

Branche : `agent/vertex-signal-os-v1` · SW v211 → **v212** · Suite **3064 passed**

---

## 1. La règle propre à cette page

`PAGES.md` §5 donne au Portefeuille une contrainte qu'aucun autre espace n'a :

> Le portefeuille doit mettre les risques **avant** les statistiques décoratives.

**Mesuré à 1440 px** avant ce lot :

| bloc | position |
| --- | --- |
| tuiles valeur / P&L / cash | 603 px |
| **journal « depuis ta dernière visite »** | **746 px** |
| concentration du capital | 852 px |
| positions exigeant une décision | 1292 px |

Un delta depuis la dernière visite est une lecture intéressante. **Ce n'est pas
ce qui menace le capital.** Il passait pourtant avant la concentration *et*
avant les positions à revoir.

### Après

| bloc | position | déplacement |
| --- | --- | --- |
| tuiles valeur / P&L / cash | 603 px | — |
| **concentration du capital** | **746 px** | **−106** |
| **positions exigeant une décision** | **1186 px** | **−106** |
| journal « ce qui a changé » | 1436 px | **+690** |

---

## 2. Le contre-exemple

Le journal n'est pas **supprimé** — il descend.

Le retirer aurait fait passer la même règle, en retirant une lecture réelle
(« la valeur nette a bougé de X depuis ma dernière visite »).
`test_le_journal_est_deplace_et_non_supprime` refuse cette sortie : il exige
que l'hôte **et** la référence de comparaison soient toujours là.

---

## 3. Une incohérence que j'ai moi-même introduite

Au lot précédent, j'ai renommé l'onglet `Watchlist` → `Surveillance` en fermant
la table de micro-copy. **Le bouton d'ajout, à quarante pixels de là, disait
toujours `+ Watchlist`.**

Deux noms pour la même chose sur le même écran, créés par mon propre renommage.
C'est le risque exact d'une migration partielle, et c'est pourquoi le nom est
maintenant gardé **des deux côtés** — l'onglet et le bouton, dans le même test.

Mesuré après correction, à 1440 et 390 px :
`boutons: ["+ Position", "+ Surveillance"]`,
`onglets: [Synthèse, Positions, Performance, Risque, Options, Surveillance]`.

---

## 4. Deux libellés alignés

| avant | après | motif |
| --- | --- | --- |
| `Depuis ta dernière visite` | **`Ce qui a changé`** | même objet que sur Aujourd'hui, qui l'appelait déjà ainsi — `VALIDATION.md` : labels cohérents |
| `Allocation & concentration du capital` | **`Allocation & concentration`** | « du capital » est vrai de toute la page |

---

## 5. Une case du DoD jamais vérifiée, vérifiée

`VALIDATION.md` → Interactions → « Tous les boutons ont un handler ».

Je l'annonçais non mesurée depuis le lot Shell. **Mesuré au navigateur sur les
huit espaces** :

| route | boutons | sans handler |
| --- | --- | --- |
| `/` | 8 | 0 |
| `/markets` | 45 | 0 |
| `/opportunities` | 28 | 0 |
| `/analysis` | 0 | 0 |
| `/portfolio` | 2 | 0 |
| `/options` | 10 | 0 |
| `/journal` | 0 | 0 |
| `/system` | 3 | 0 |
| **total** | **96** | **0** |

La case est **verte**, et elle l'est par mesure et non par supposition.

*Portée* : le détecteur considère qu'un bouton a un gestionnaire s'il porte
`onclick`, un `data-*` connu de la délégation, ou un `type`. Un bouton câblé par
un `addEventListener` posé ailleurs serait compté comme sans handler — donc le
zéro est **conservateur**, jamais optimiste.

---

## 6. Gardiens

`tests/test_signal_os_portfolio.py` — **5 tests**, commentaires retirés avant
analyse.

| mutation | résultat |
| --- | --- |
| journal remonté avant le risque | 1 échec |
| journal **supprimé** au lieu d'être déplacé | 2 échecs |
| bouton `+ Watchlist` revenu | 1 échec |
| ancien nom du journal revenu | 1 échec |
| titre répétant le nom de la page | 1 échec |

---

## 7. Ce que ce lot ne fait pas

Seule la vue **Synthèse** a été mesurée et retouchée. Les cinq autres
(`positions`, `performance`, `risk`, `options`, `watchlist`) **n'ont pas été
ouvertes** — les rangs 5, 6 et 7 de `PAGES.md` (table des positions, watchlist,
alertes/catalyseurs) y vivent et restent à auditer.

---

## 8. Dette

- Portefeuille : **5 vues sur 6** non auditées.
- Marchés : 6 vues non reconstruites · Opportunités : structure jugée conforme,
  pas mesurée rang par rang.
- Analyse : la fiche `/analysis/<ticker>` reste inaccessible ici
  (`/api/ticker/<sym>` interdit).
- Aucun instrument ne détecte le **rognage silencieux**.
- La palette violette n'est pas dans `palette.py` : **les graphiques restent
  cuivre** pendant que l'interface est violette. Décision utilisateur en attente.
- Blocs du DoD encore non vérifiés : Escape ferme drawer/modal, focus trap,
  palette de commandes, et l'inventaire loading/empty/error/stale zone par zone.

---

## 9. Suite

Lot **06 — Options**.
