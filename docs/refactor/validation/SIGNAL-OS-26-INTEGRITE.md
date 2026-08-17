# SIGNAL OS · LOT 26 — UN LOT QUI NE TROUVE RIEN

Branche : `agent/vertex-signal-os-v1` · SW **inchangé (v231)** · Suite **3141 passed**

Quatre invariants qu'aucun test de la suite ne peut tenir, parce qu'ils
n'existent qu'une fois la page rendue et hydratée. Le produit est propre.

**Aucun octet servi n'a changé — donc pas de bump de service worker.** Le
bumper par réflexe aurait purgé le cache hors-ligne de tous les visiteurs pour
un lot qui n'a touché que `tools/`, `tests/` et `docs/`.

---

## 1. Le relevé

| invariant | 1440 px | 320 px |
| --- | --- | --- |
| identifiants dupliqués | **0** | **0** |
| erreurs de page | **0** | **0** |
| liens internes cassés (65 distincts) | **0** | **0** |
| débordement horizontal (WCAG 1.4.10) | **0** | **0** |

Sur les **35 vues**, aux deux largeurs. Il n'y a rien à corriger, et l'écrire
est le résultat du lot — pas son échec.

Le 320 px compte : c'est la largeur qu'impose WCAG 1.4.10, plus étroite que le
390 des lots précédents. Le produit y tient sans défilement horizontal.

---

## 2. Le poids, mesuré pour la première fois

| page | requêtes | total | CSS | JS | nœuds DOM | DOM ready |
| --- | --- | --- | --- | --- | --- | --- |
| `/` | 57 | 922 Ko | 193 Ko | 390 Ko | 430 | 174 ms |
| `/markets` | 41 | 1 310 Ko | 193 Ko | 381 Ko | 701 | 133 ms |
| `/opportunities` | 45 | 1 326 Ko | 193 Ko | 386 Ko | 1 011 | 148 ms |
| `/portfolio` | 44 | 764 Ko | 193 Ko | 385 Ko | 320 | 229 ms |
| `/options` | 46 | 829 Ko | 193 Ko | 494 Ko | 422 | 159 ms |
| `/journal` | 37 | 900 Ko | 193 Ko | 373 Ko | 540 | 122 ms |
| `/system` | 42 | 736 Ko | 193 Ko | 373 Ko | 485 | 158 ms |

**19 feuilles de style** et **11 scripts** externes sur chaque page. C'est
beaucoup de requêtes bloquantes — mais les réduire demanderait une étape de
build que le produit n'a pas, et qui est une décision d'architecture, pas un
correctif. Constat posé, pas d'action prise.

---

## 3. Deux pièges d'instrument, dont un qui aurait supprimé du code vivant

En cherchant du poids mort par couverture CSS, deux fichiers sont ressortis à
**0 %**.

### `responsive.css` — 0 % à 1440, **35 %** à 390

Tout son contenu vit dans des `@media` qui ne matchent pas à 1440 px. Mesuré aux
deux largeurs, il remonte immédiatement.

> Agir sur le premier relevé aurait **supprimé la feuille mobile du produit** —
> celle-là même que les lots 24 et 25 venaient de corriger.

### `fonts.css` — 0 % partout, et c'est normal

Il ne contient que des `@font-face`, que la couverture CSS n'attribue **jamais**
à une utilisation. Les deux polices sont auto-hébergées, précisément pour ne
dépendre d'aucun CDN.

### Et une mesure JS carrément fausse

Ma première version calculait la couverture avec `Math.max(endOffset)` —
l'offset le plus lointain atteint, pas la somme des plages exécutées. D'où des
**« 100 % » partout**, qui ne mesuraient rien. Corrigée, la granularité de V8
reste trop grossière pour distinguer le mort du vivant sur ces fichiers : je
n'en tire donc **aucune conclusion**, plutôt qu'une conclusion confortable.

> Trois fichiers auraient pu être « nettoyés » sur la foi de ces relevés. Le
> seul garde-fou a été de trouver le résultat trop beau et de refaire la mesure.

---

## 4. Ce que le lot livre

- **`tools/mesurer_integrite_pages.py`** — un invariant qu'on ne peut plus
  re-mesurer se dégrade en silence ; c'est exactement ce qui était arrivé au
  rognage silencieux avant le lot 13. L'outil rejoue le relevé ci-dessus et
  conclut par `TOUT PROPRE` ou la liste des défauts.
- Il hérite des leçons des lots précédents : vues **dérivées de la source**
  (lot 14), points d'entrée interdits **avortés au navigateur** (lot 20), et ses
  propres avortements **exclus** du décompte d'erreurs (lot 13).

---

## 5. Gardien — `tests/test_signal_os_integrite_lot26.py` (4 tests, 7 mutations sur 7 tuées)

| mutation | résultat |
| --- | --- |
| balayage 320 px retiré | 1 échec |
| avortement des interdits retiré | 1 échec |
| liens interdits suivis par l'outil | 1 échec |
| avortements recomptés en erreurs | 1 échec |
| vues plus dérivées de la source | 1 échec |
| **feuille mobile vidée** | 1 échec |
| **polices vidées** | 1 échec |

Les deux dernières sont le cœur du lot : elles simulent exactement la
« suppression de code mort » que mes relevés fautifs auraient justifiée.
