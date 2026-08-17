# SIGNAL OS · LOT 27 — LES LIGNES CLIQUABLES ÉTAIENT FOCUSABLES ET INERTES

Branche : `agent/vertex-signal-os-v1` · SW v231 → **v232** · Suite **3145 passed**

Un angle fonctionnel jamais testé. Le lot 22 avait vérifié que les contrôles
sont **visibles** au focus ; personne n'avait vérifié qu'ils sont
**activables**.

---

## 1. Le défaut

Un contrôle **non natif** — `role="button"` sur un `<span>`, une ligne de
tableau cliquable — n'est activé au clavier que si quelqu'un l'a câblé. Le
navigateur ne le fait que pour `button`, `a[href]`, `input`, `select`.

Sonde : focus, `Entrée`, et on regarde si un clic part.

| relevé | résultat |
| --- | --- |
| contrôles non natifs testés | 18 |
| **muets au clavier** | **3 familles** |

- scanner LEAPS (`/options?view=leaps`)
- positions options (`/options?view=positions`)
- comparateur d'options (`/opportunities?view=options`)

On pouvait les atteindre au clavier, et il ne se passait **rien**. WCAG 2.1.1.

---

## 2. La cause, et c'est la même qu'au lot 25

```js
closest('[data-open-analysis],[data-entity-menu],[data-position-menu]')
```

Le gestionnaire clavier délégué n'énumérait que **trois attributs**. Toute ligne
qui n'en portait aucun était hors de sa portée.

> Une règle qui énumère des noms ne protège que ce qu'on a pensé à nommer. Au
> lot 25 c'était la taille tactile définie par **classe** ; ici l'activation
> clavier définie par **attribut**. Même forme, deux endroits, deux lots
> consécutifs.

Le correctif vise `[data-clickable]`, l'attribut que **toutes** les lignes
cliquables du produit portent — plutôt que d'ajouter `data-candidate`,
`data-ct` et `data-option-position` à la liste, ce qui aurait recommencé la même
erreur un cran plus loin.

---

## 3. Un second défaut, trouvé en chemin

Deux de ces familles n'ont **ni rôle ni nom accessible** : focusables et
cliquables — donc des contrôles — mais un lecteur d'écran annonce « ligne ».

L'audit de sémantique du lot 24 ne les avait pas vues **parce qu'il
sélectionnait `[role="button"]`**, que justement elles n'avaient pas.

> Un audit ne trouve que ce que son sélecteur admet. Le lot 24 concluait
> « 0 contrôle sans nom accessible » — c'était vrai *de ce qu'il regardait*, et
> il regardait à côté de ces trois familles.

Corrigé : `role="button"` et un `aria-label` qui dit l'action (« Ouvrir la
position NVDA CALL 120 », « Simuler GOOGL PUT 175 »).

---

## 4. Le faux positif écarté

`.vx-heatmap-scroll` reste « muet » à la mesure, et **c'est correct** : il porte
`role="region"` et un libellé qui annonce le défilement horizontal. Un conteneur
défilable focusable est un motif légitime, où `Entrée` ne doit rien faire.

C'est mon sélecteur `[tabindex="0"]` qui l'avait ramassé. Lui donner
`role="button"` pour faire taire la sonde aurait transformé une région lisible
au clavier en un contrôle qui ne fait rien — le gardien fige ce refus.

---

## 5. Mesures — serveur `td-shell-v232` vérifié avant lecture

| relevé | avant | après |
| --- | --- | --- |
| familles muettes au clavier | **3** (+ 1 faux positif) | **0** (+ 1 faux positif conservé) |
| défauts de sémantique (lot 24) | 0 | **0** |
| suite | 3141 | **3145** |

---

## 6. Gardien — `tests/test_signal_os_clavier_lot27.py` (4 tests, 6 mutations sur 6 tuées)

| mutation | résultat |
| --- | --- |
| lignes cliquables retirées du gestionnaire | 1 échec |
| tickers et menus retirés | 1 échec |
| garde des contrôles natifs retirée | 1 échec |
| positions sans rôle ni nom | 1 échec |
| scanner sans rôle ni nom | 1 échec |
| région défilable transformée en bouton | 1 échec |

Le troisième test est un **contre-exemple** : intercepter `Entrée` sur un
`<button>` déclencherait son action **deux fois**, le navigateur le faisant
déjà. La garde qui exclut les contrôles natifs est aussi importante que la liste
qui inclut les autres.

---

## 7. Réserve honnête

La sonde teste `Entrée`, pas `Espace`. Le gestionnaire traite les deux, et le
code est le même chemin — mais ce n'est pas mesuré. Elle teste aussi au plus six
contrôles par vue, pour tenir dans un temps raisonnable : une quatrième famille
muette dans la queue d'une vue longue passerait inaperçue.
