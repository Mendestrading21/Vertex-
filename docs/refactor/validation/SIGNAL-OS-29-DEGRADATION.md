# SIGNAL OS · LOT 29 — LA DÉGRADATION HONNÊTE, ÉPROUVÉE

Branche : `agent/vertex-signal-os-v1` · SW v232 → **v233** · Suite **3155 passed**

`CLAUDE.md` pose l'invariant le plus important du produit — « donnée absente →
mention honnête, jamais un chiffre inventé ». Personne ne l'avait **éprouvé** :
on l'avait lu dans le code, jamais **provoqué**.

---

## 1. La méthode, et sa limite volontaire

Trois pannes simulées sur les points de **données uniquement** :

| panne | forme |
| --- | --- |
| erreur serveur | HTTP 500 |
| réponse vide | HTTP 200, corps `{}` |
| JSON malformé | HTTP 200, corps non analysable |

Jamais le HTML, le CSS ni le JS. Les casser ferait mesurer **un navigateur en
panne**, pas un produit qui dégrade — et rendrait un verdict catastrophique qui
ne dirait rien.

Ce qu'un utilisateur ne doit jamais lire : `NaN`, `undefined`, `null`,
`Infinity`, `[object Object]`. Ce ne sont pas des données absentes, ce sont des
fuites de plomberie — et elles ressemblent assez à du texte pour passer
inaperçues.

---

## 2. Le relevé — 33 vues × 3 pannes

| panne | fuites | vues sans état honnête | erreurs de page |
| --- | --- | --- | --- |
| erreur 500 | **0** | 0 | **0** |
| réponse vide | **1 → 0** | 0 | **0** |
| JSON malformé | **0** | 0 | **0** |

Le produit tient remarquablement : aucune page ne casse, et sur deux pannes sur
trois, rien de technique ne fuit à l'écran.

---

## 3. Le défaut

Sur une réponse vide, le scanner LEAPS rendait :

> `· fenêtre  DTE · undefined contrat(s)`

Trois champs, trois problèmes : l'univers disparu sans le dire, la fenêtre
réduite à « fenêtre  DTE » — deux mots sans nombre entre eux — et le compte de
contrats affiché comme `undefined`.

Les cellules voisines gardaient **déjà** (`c.iv != null ? … : '—'`). C'est cette
ligne-ci qui avait oublié : le défaut n'est pas une absence de convention, c'est
un endroit où la convention n'a pas été appliquée.

Corrigé : chaque champ est gardé et **se nomme quand il manque** — `—`,
« fenêtre n/d », « nombre de contrats n/d ».

---

## 4. Deux faux positifs, écartés après vérification

Mon heuristique « du contenu mais aucun état honnête » signalait
`/journal?view=progression` et `/system?view=settings`.

Vérifié avant d'accuser, en mesurant les chiffres **réellement affichés** :

| vue | chiffres à l'écran | nature |
| --- | --- | --- |
| `/journal?view=progression` | `5`, `10`, `20`, `30` — des valeurs de filtre | relais posé au lot 11 |
| `/system?view=settings` | **aucun** | formulaire de réglages |

Ce sont des vues **statiques**, dont le contenu ne vient d'aucune source.

> Une vue qui n'affiche pas de donnée n'a pas d'état de donnée à montrer.

Elles sont écartées **par leur nom** dans l'instrument, et non en relevant le
seuil jusqu'à ce qu'elles se taisent — ce qui aurait masqué du même coup de
vraies vues muettes.

---

## 5. Ce que le lot livre

**`tools/mesurer_degradation.py`** — un invariant qu'on ne peut plus provoquer
redevient une croyance. L'outil conclut `TOUT PROPRE` ou liste les fuites.

Un défaut de mon côté, corrigé en chemin : Playwright passe `request` en
**second argument positionnel** au gestionnaire de route, ce qui écrasait mon
paramètre par défaut `p=panne` et rendait
`'Request' object is not subscriptable`. La closure ne prend plus qu'un
paramètre.

---

## 6. Gardien — `tests/test_signal_os_degradation_lot29.py` (5 tests, 7 mutations sur 7 tuées)

| mutation | résultat |
| --- | --- |
| nombre de contrats dégardé | 1 échec |
| univers dégardé | 1 échec |
| fenêtre dégardée | 1 échec |
| panne « JSON malformé » retirée | 1 échec |
| pannes étendues à **tout** (HTML/CSS/JS) | 1 échec |
| vues statiques non écartées | 1 échec |
| liste des fuites réduite | 1 échec |

Les trois premières comptent séparément : corriger deux champs sur trois
laisserait la ligne mentir sur le troisième.

---

## 7. Réserve honnête

Les trois pannes sont **globales** : toutes les sources tombent en même temps.
Une panne **partielle** — une source sur six qui répond mal pendant que les
autres vont bien — est un régime différent, où un chiffre faux peut se glisser
entre des chiffres justes sans qu'aucun état d'erreur ne s'affiche. Non mesuré.
