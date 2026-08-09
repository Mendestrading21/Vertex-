# SKYLER LOT 420 — BILAN n°11, tranche 410 → 419

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-420` (base : lot 419 fusionné,
0676d78)

Dix lots. Bilan **sur pièces** : les dix rapports relus, les chiffres re-mesurés
dans le dépôt. Serveur DEMO non lancé.

## La tranche a deux moitiés nettes

```text
410        bilan n°10
411 → 415  LES OCTETS SERVIS   provenances · contrat de cache SW · chemins client
                               · boutons · identifiants dupliqués
416 → 419  LES MOTEURS         RSI · track_record · multiplicateur · bornage
```

**Première moitié — le produit est sain, le filet est court.** Cinq contrôles,
zéro défaut produit : 59 provenances dont 25 littéraux exacts (411) · 156 chemins
client, aucun mort (413) · 167 boutons servis, aucun sans écouteur (414) ·
288 identifiants, aucun doublon (415). Mais **trois fois sur cinq, le gardien
censé protéger l'invariant s'arrête avant la fin** :

```text
412   le gardien détecte le changement d'asset, il n'IMPOSE pas le bump
414   le gardien couvre 149 boutons servis sur 167
415   le gardien visite 3 pages sur 8
```

**Seconde moitié — quatre lots, quatre trouvailles.**

```text
416   RSI = 100 sur une série plate — indéfini rendu comme l'extrême, affiché
417   track_record : le N affiché n'est pas le N du calcul (jusqu'à 1 observation)
418   multiplicateur d'option assumé à 100 + `MULTIPLIER_INVALID` mort deux fois
419   bornage de la forme du 418 : 4 sites sur 22 — et un RSI de 0 EFFACÉ
```

## Le fait le plus important : le changement de famille a payé immédiatement

Trois bornages consécutifs (413, 414, 415) rendaient le même diagnostic de forme
avec un rendement décroissant. La note de cadence du 416 disait : *si le lot rend
une quatrième fois « produit sain, gardien à périmètre court », déclarer la veine
épuisée et changer de famille.* Elle a été appliquée.

```text
veine « octets servis »   5 lots   0 défaut produit, 3 filets courts
veine « moteurs »         4 lots   4 défauts produit
```

**C'était le bon appel, et la décision est reproductible : quand trois lots
d'affilée rendent le même diagnostic de forme, changer de famille.** C'est
l'acquis de méthode le plus utile de la tranche.

## Le motif technique, vérifié quatre fois

Dans les quatre lots de la veine des moteurs, **la bonne pratique est écrite à
quelques lignes du défaut** :

```text
416   `pos = 50.0` quand `hi == lo`            trois lignes plus bas
417   `tp1_resolved` exposé pour TP1           dans le même dictionnaire
418   le `is None` explicite de `quantity`     deux lignes plus haut
419   le `is not None` du coût moyen           quatre lignes plus haut
```

Le défaut n'est jamais l'ignorance de la règle : c'est son **application
incomplète**. *Chercher la règle que le fichier respecte ailleurs, puis l'endroit
où il l'oublie* — c'est la méthode la plus rentable depuis le lot 398, et elle se
formule maintenant comme une procédure, pas comme une anecdote.

## Le résultat le plus parlant : deux fautes opposées sur le même indicateur

```text
416   RSI FABRIQUÉ à 100   série plate → 0/0 indéfini, rendu comme l'extrême haussier
419   RSI EFFACÉ à 0       `float(d.get('rsi') or 50)` → 0.0 est falsy, devient neutre 50
```

Une seule cause : **traiter une valeur extrême légitime comme une donnée
manquante**. Dans un cas on invente, dans l'autre on gomme — et les deux se
lisent comme des mesures.

## Les gravités, distinguées et non gonflées

```text
un NOMBRE FAUX                            407 (hors tranche)  HHI ×170, alerte fabriquée
un ÉCHANTILLON MAL PRÉSENTÉ               417                 moyenne réelle, dénominateur caché
une HYPOTHÈSE DOCUMENTÉE NON VÉRIFIÉE     418                 multiplicateur = 100, jamais lu
un TEXTE D'EXPLICATION INCOMPLET          419                 raison absente sur RSI = 0
```

Ce ne sont pas quatre fois le même défaut, et les présenter ainsi serait
malhonnête. **Trois lots ont resserré leur propre diagnostic quand la mesure les
contredisait** : le 416 (la phrase « RSI 100 suracheté » est atteignable **mais**
légitime au sens de Wilder), le 418 (le vrai défaut est en amont, et la valeur
vaut toujours 100 en pratique), le 419 (18 des 22 replis sont sains). C'est à
porter au crédit de la méthode.

## L'instrument pris en défaut — compté honnêtement

```text
413   deux fois   les 26 fichiers /static hors corpus (chemin disque faux)
                  `fetch(` sans ses enveloppes → `get('/api/…')` manqué
414   deux fois   55 faux « boutons morts » dont `vx-collapse-btn`
                  231 boutons annoncés au lieu de 167 (inline comptés deux fois)
415   deux fois   heuristique de proximité : 9 candidats → 1 par appariement
                  test d'englobement rendant des lignes propres, alignées, FAUSSES
417   une fois    jeu d'indices ne résolvant pas les horizons attendus
```

**Sept fois sur dix lots**, et toujours attrapé **avant publication** par un
témoin ou un contrôle de cohérence. Le point à retenir est plus dur que le
compte : **la leçon des enveloppes a été refaite trois fois — 409 (`emptyCard`),
413 (`get(…)`), 414 (`$(…)`).** Une règle écrite dans un document ne suffit pas ;
c'est le témoin qui l'attrape. La parade trouvée au 414 est structurelle : cesser
d'énumérer les accesseurs, exiger la **proximité** d'un accesseur quelconque.

## Ce qui n'a pas bougé — mesuré

```console
$ git diff --name-only bbd5f86..HEAD | grep -v '^docs/'
  (aucun)
$ git diff --shortstat bbd5f86..HEAD
  12 files changed, 2038 insertions(+)
```

| | |
|---|---|
| Lots | 10 (410 → 419) |
| Fichiers de production modifiés | **0** |
| Fichiers de test modifiés | **0** (la tranche précédente en avait 1) |
| Tests ajoutés | **0** — délibérément |
| Suite | **2 864 / 0 skipped**, identique aux dix lots |
| PR | **#442 → #451**, toutes fusionnées en squash |
| Service worker | `td-shell-v187`, servi et enregistré, inchangé |
| `main` | intacte |

Le MD5 des 8 pages servies a été prouvé identique aux lots **390** et **396** ;
il **n'a pas été re-mesuré depuis**. Comme aucun octet de production n'a bougé,
il est réputé inchangé — **c'est une inférence, pas une mesure fraîche**, et
c'est écrit comme telle.

## La question — plus pressante qu'au bilan n°10

Le rang 1 contient maintenant **six dossiers**, dont **deux chiffres faux
affichés comme réels** :

```text
407   HHI faux d'un facteur 170 + alerte de concentration fabriquée   /portfolio
416   RSI = 100 sur un titre qui n'a pas bougé                        /analysis
406   une consigne que le trader ne peut pas suivre (409 : unique)    /portfolio
417   un échantillon mal présenté sur la page qui parle de confiance  /portfolio
388   7 points MSFT fabriqués, servis comme des mesures               /options
378   replis `0` de `_followed_count` / `_positions_count`
```

**Aucun GO n'est arrivé depuis le lot 388 — trente-deux lots.**

- **(a)** continuer les lots courts. La veine des moteurs paie encore (4/4), donc
  ce n'est pas absurde — mais elle produit des **constats**, pas des corrections.
- **(b) GO groupé sur le rang 1, puis exécution. ← recommandé.** Commencer par la
  purge des 7 points MSFT (coût quasi nul, risque nul), puis `myCapital`, puis le
  RSI (deux lignes, deux moteurs).
- **(c)** arrêter la boucle et attendre. Défendable : rien ne se dégrade, la
  production n'a pas bougé depuis le lot 399.

Les bilans n°9 et n°10 posaient déjà cette question ; **ils ne sont pas
reformulés ici** — s'y reporter. La seule chose qui a changé depuis le n°10, et
qui compte : **il y a désormais deux chiffres faux affichés, pas un.**

## Portée

Ce bilan mesure ce que la tranche a **déposé dans le dépôt** et ce que les dix
rapports affirment. Il ne rejoue pas les trouvailles une à une — chaque rapport
porte ses propres preuves, et le 419 a re-mesuré la portée du 418. Aucun serveur
DEMO lancé, aucun moteur rouvert.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier de production touché** — bilan documentaire. Pas de preuve MD5
  requise, pas de bump. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; les trois
  fichiers habituels ré-horodatés par la passe de suite, restaurés. Écart final
  **aucun**.
- Suite : **2864 passed / 0 skipped**.
