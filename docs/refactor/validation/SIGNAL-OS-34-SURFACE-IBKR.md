# SIGNAL OS · LOT 34 — READONLY TENU PAR CE QUE LE CODE FAIT, PAS PAR UNE LISTE DE NOMS

Branche : `agent/vertex-signal-os-v1` · SW **v233 inchangé** · Suite
**3171 → 3177 passed**

Réserve ouverte du lot 31, écrite en toutes lettres : le garde-fou READONLY
« reste une liste de NOMS ; un chemin d'exécution nommé dynamiquement
passerait ». Le lot 33 a montré ce que valent les listes tenues à la main — une
quatrième sortie de news est passée exactement par là.

On inverse l'instrument.

| | liste noire (lot 31) | liste blanche mesurée (ce lot) |
| --- | --- | --- |
| principe | interdire `placeOrder`, `transmit`… | énumérer ce que le code emploie |
| angle mort | tout nom non prévu | aucun : une capacité inconnue **sort** |
| verdict sur `placeOrder` | « interdit » | **absent** de la surface |

---

## 1. La surface réellement employée — 22 capacités

Mesurée à l'AST sur 310 fichiers, objets `IB` **dérivés du code** :

| famille | capacités |
| --- | --- |
| connexion / cycle de vie | `connect` · `disconnect` · `isConnected` · `sleep` · `run` · `client` · `RequestTimeout` · `managedAccounts` |
| référentiel | `qualifyContracts` · `reqSecDefOptParams` · `reqNewsProviders` |
| marché (lecture) | `reqTickers` · `reqTickersAsync` · `reqMktData` · `cancelMktData` · `reqMarketDataType` · `reqHistoricalData` · `reqHistoricalNews` · `reqScannerData` |
| compte (lecture) | `positions` · `accountSummary` |
| second niveau | `client.marketDataType` |

Aucun accès à **nom calculé**. Aucune capacité d'exécution. `cancelMktData`
annule un *abonnement de données*, pas un ordre — c'est la seule entrée dont le
nom peut tromper, et c'est pour ça qu'elle est classée explicitement.

---

## 2. Deux erreurs de mesure, corrigées avant de conclure

**L'alias.** Ma première dérivation ne retenait que `X = IB()`. Or la passerelle
fait `self._ib = ib` puis n'appelle `isConnected` et `disconnect` **que** par
`self._ib` : trois accès m'échappaient. Un instrument qui ne voit pas une
capacité ne peut pas la garder. La dérivation itère maintenant jusqu'au point
fixe.

**Le second niveau.** Ma première passe ne regardait que `ib.X` et annonçait
« aucun accès dynamique ». Faux : il y en a un, `getattr(ib.client,
'marketDataType', 3)`, au niveau d'en dessous. Le nom y est une **constante**,
donc la liste blanche peut le classer — mais je ne l'aurais jamais su sans
suivre les chemins pointés.

---

## 3. Ce qui empêche ce gardien d'être creux

Un test qui passe ne prouve rien s'il ne peut pas échouer. Deux témoins et un
plancher, tous mesurés :

1. **Témoin d'ordre** — le scanner tourne sur un fichier contenant
   `ib.placeOrder`, `self._ib.cancelOrder` et `ib.client.placeOrderAsync` ; les
   trois doivent ressortir. Les deux dernières formes sont précisément celles que
   ma première version ratait.
2. **Témoin de nom calculé** — `getattr(ib, verbe)()` doit être relevé, tandis
   que `getattr(ib, 'reqTickers')()` doit rejoindre la surface. Sans les deux, on
   perdrait le cas des deux côtés.
3. **Plancher** — ≥ 250 fichiers lus, ≥ 20 capacités, et les porteurs doivent
   inclure `_ib`.

Et la liste blanche est elle-même gardée : un test vérifie qu'**aucun verbe
d'exécution ne peut y être glissé**. Sinon il suffirait d'y écrire `placeOrder`
pour faire taire le gardien.

---

## 4. Mutations — 6 sur 6 tuées

| mutation | résultat |
| --- | --- |
| `placeOrder` glissé dans la liste blanche | mord |
| alias non suivi (retour à l'avant-lot) | mord |
| second niveau perdu | mord |
| `getattr` non relevé | mord |
| le scanner ne lit plus les `.py` | mord |
| **un vrai `ib.placeOrder` dans la passerelle** | mord |

La dernière est la seule qui compte vraiment : le gardien voit une violation
réelle, introduite là où elle serait le plus naturelle.

---

## 5. Ce que la liste noire a appris de la liste blanche

En livrant l'outil, le gardien du lot 31 a mordu — **sur l'outil lui-même**,
ligne 3 : une docstring qui nomme le verbe qu'elle sert justement à tenir hors du
code. Le balayage signale une **mention**, pas un **appel**.

Deux façons d'en sortir. Contourner (réécrire la prose en vague) aurait rendu
flou le document de sûreté à l'endroit exact où il faut être exact. J'ai donc
rendu l'instrument plus précis : commentaires et docstrings Python sont blanchis
avant le balayage. Ce n'est pas un affaiblissement — un commentaire ne s'exécute
pas — et les **chaînes restent scannées**, parce que `getattr(ib, 'placeOrder')`
est précisément la forme qu'aucune liste ne rattrape ailleurs.

Vérifié par mutation, 4 sur 4 :

| mutation | résultat |
| --- | --- |
| vrai appel d'ordre dans la passerelle | mord |
| ordre nommé par une **chaîne** (`getattr`) | mord |
| blanchiment étendu à toutes les chaînes | mord |
| blanchiment des commentaires devenu total | mord |

Les deux dernières sont gardées par un témoin qui vérifie que le blanchiment
ignore les mentions **sans** manger un appel réel.

---

## 6. Ce que le lot ne prouve pas

1. **C'est de l'analyse statique.** Un ordre passé par un chemin que l'AST ne
   relie pas à un objet `IB` (objet reçu en paramètre, stocké dans une
   structure, importé d'un module tiers) n'est pas vu. La défense de fond reste
   `readonly=True` **côté serveur IBKR**, qui refuse l'ordre quoi qu'il arrive —
   ce lot garde la couche au-dessus, pas à sa place.
2. La liste blanche est un **jugement humain** figé : chaque entrée a été
   classée à la main. Le gardien garantit qu'on ne l'élargit pas sans le voir,
   pas que la classification initiale est juste.
3. Rien n'est mesuré du côté `ib_insync` lui-même : si la bibliothèque exécutait
   un ordre depuis une méthode de lecture, aucun de ces tests ne le verrait.
