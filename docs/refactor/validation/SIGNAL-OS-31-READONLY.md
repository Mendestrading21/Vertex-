# SIGNAL OS · LOT 31 — LE GARDE-FOU LE PLUS IMPORTANT AVAIT DEUX TROUS

Branche : `agent/vertex-signal-os-v1` · SW **inchangé (v233)** · Suite **3159 passed**

`READONLY` est l'invariant produit absolu de Vertex : *aucun ordre ne peut
jamais être passé*. La CI en fait un **job bloquant séparé**
(`tests/test_no_orders.py`). Personne n'avait jamais vérifié que ce gardien-là
**tient**.

Je l'ai muté. **Deux mutations ont survécu** — c'est-à-dire deux façons de
retirer la protection sans qu'aucun test ne bronche.

Aucun octet servi n'a changé : **pas de bump de service worker**.

---

## 1. Trou n°1 — retirer le verrou était invisible

L'ancienne logique :

```python
if 'readonly' in seg.lower():
    assert re.search(r'readonly\s*=\s*True', seg)
```

Le contrôle ne se déclenchait **que si le mot « readonly » était encore là**.

| mutation | avant |
| --- | --- |
| `readonly=False` | **tuée** |
| `readonly=True` **supprimé** | **survivait** |

> Un garde-fou qui ne se déclenche que si la protection est encore présente ne
> protège rien. Et « supprimer l'argument » est précisément le geste qu'un
> correctif distrait produit — bien plus probable que « le passer à False ».

**Corrigé** : une connexion IBKR est reconnue par `clientId=` — ce qui la
distingue de la façade sans argument (`gateway.connect()`) et de tout autre
`.connect(` du dépôt — et `readonly=True` y est exigé **inconditionnellement**.
Les quatre sites réels du produit le portent : `ibkr_gateway.py` et trois dans
`terminal.py`.

---

## 2. Trou n°2 — le gardien ignorait la moitié du produit

Le balayage ne globait que `*.py`. Or Vertex est **massivement écrit en
JavaScript** : 36 fichiers rien que sous `vertex/static`.

Un `placeOrder(` déposé dans un `.js` passait **tous** les tests.

**Corrigé** : le balayage couvre `.py` **et** `.js`, en excluant les fichiers de
test (qui citent volontairement les motifs) et les bibliothèques minifiées.
Vérifié avant d'étendre : **zéro** motif interdit déjà présent dans le JS du
produit — l'extension n'introduit donc aucun faux positif.

---

## 3. Un troisième point, ajouté par précaution

`connects` était collecté et **jamais vérifié**. Un commentaire disait même :
« si aucun connect n'existe, le test est vacuously vrai — pas de risque ».

C'est vrai pour la sûreté, faux pour la **confiance** : un gardien qui devient
vide et vert ne dit plus rien. `assert connects` est ajouté.

---

## 4. Le tableau des mutations — 6 tuées sur 7

| mutation | avant | après |
| --- | --- | --- |
| `readonly=True` **retiré** de la passerelle | **survivait** | tuée |
| `readonly=False` | tuée | tuée |
| `placeOrder(` dans un `.js` | **survivait** | tuée |
| `placeOrder(` dans un `.py` | tuée | tuée |
| `readonly` retiré d'un site de `terminal.py` | — | tuée |
| `config.READONLY = False` | tuée | tuée |
| **passerelle IBKR supprimée** | survit | **survit — légitimement** |

### Pourquoi la dernière survit, et pourquoi je ne la « corrige » pas

Supprimer `ibkr_gateway.py` casserait l'application — mais **l'invariant de
sûreté tient toujours** : les trois connexions restantes de `terminal.py` sont
verrouillées. Le rôle de ce fichier est de garder l'invariant, pas l'existence
d'un fichier ; la casse serait attrapée par les autres tests.

> Contorsionner un garde-fou de sûreté pour qu'il attrape aussi une panne
> fonctionnelle brouille ce qu'il affirme. Une mutation qui survit doit être
> expliquée, pas forcément tuée.

---

## 5. Ce que ce lot n'a pas fait

Les motifs interdits restent une **liste de noms** (`placeOrder`, `submitOrder`,
`MarketOrder`…). Un chemin d'exécution écrit sous un autre nom — appel
dynamique, chaîne construite, bibliothèque tierce — passerait. C'est la limite
structurelle d'un gardien par motif, et elle est réelle.

Ce qui la compense : le verrou `readonly=True` côté connexion, désormais exigé
sans échappatoire, et `config.READONLY`. La défense ne tient pas à un seul
niveau.
