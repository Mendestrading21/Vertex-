# SIGNAL OS · LOT 28 — LE CONTRAT DE FOCUS, ET UNE RÉSERVE LEVÉE

Branche : `agent/vertex-signal-os-v1` · SW **inchangé (v232)** · Suite **3150 passed**

Deux mesures, deux résultats vides — et un trou trouvé dans **mon propre
gardien**, pas dans le produit.

Aucun octet servi n'a changé : **pas de bump de service worker**.

---

## 1. Les surcouches tiennent le focus

Six critères, deux surcouches, tous verts :

| critère | modale | tiroir |
| --- | --- | --- |
| ouverture | oui | oui |
| focus déplacé dedans | oui | oui |
| focus **piégé** (25 `Tab`) | oui | oui |
| `Échap` ferme | oui | oui |
| `inert` reposé | oui | oui |
| focus **rendu au déclencheur** | oui | oui |

Le dernier point mérite d'être raconté. Je ne l'avais **pas vu** en lisant le
code, et la mesure l'a montré vrai. Plutôt que de me contenter du « oui », j'ai
cherché **pourquoi** — `lastFocus` est capturé à l'ouverture (deux sites) et
restauré à la fermeture (deux sites).

> Un résultat vert qu'on n'explique pas est un résultat qu'on n'a pas compris.
> Ici il aurait aussi bien pu venir du navigateur déplaçant le focus quand un
> élément devient `inert` — auquel cas la « conformité » aurait été un accident,
> et le gardien aurait verrouillé du vide.

---

## 2. La réserve du lot 27 est levée

Le lot 27 concluait avec cette réserve : *« la sonde teste `Entrée`, pas
`Espace` […] et au plus six contrôles par vue »*.

Refait sans plafond et sur les deux touches :

| relevé | lot 27 | lot 28 |
| --- | --- | --- |
| contrôles non natifs testés | 18 | **45** |
| touches | `Entrée` | `Entrée` **et** `Espace` |
| familles muettes | 3 (corrigées) | **0** |

Le plafond ne cachait rien, et `Espace` se comporte comme `Entrée`. Une réserve
qu'on lève par la mesure vaut mieux qu'une réserve qu'on répète.

---

## 3. Le trou était dans mon gardien

J'avais laissé `mobileNav` **hors** du test de `closeAll`, comme témoin de
mutation. Il a **survécu** — ce qui était le comportement attendu d'un témoin.

Sauf qu'en regardant ce qu'il protégeait, ce n'était pas une limite assumée mais
un trou : la navigation mobile **est** une surcouche, et si `Échap` cesse de la
fermer, un utilisateur au téléphone reste bloqué dedans.

> Un témoin qui survit est soit une limite assumée, soit un trou. Le distinguer
> demande de regarder ce qu'il couvre — pas de se féliciter qu'il ait survécu.

Ajouté au gardien ; la mutation le tue désormais.

---

## 4. Ce que le lot livre

- **`tools/mesurer_clavier.py`** — les deux mesures, rejouables. Il conclut
  `TOUT PROPRE` en écartant explicitement le faux positif attendu.
- **`tests/test_signal_os_focus_lot28.py`** — le contrat de focus n'était
  protégé par **rien**. `lastFocus?.focus?.()` pouvait disparaître sans qu'un
  seul test bronche, et le focus serait retombé sur `<body>` à chaque fermeture :
  une régression qu'aucune relecture ne remarque.

---

## 5. Le faux positif, conservé et expliqué

`.vx-heatmap-scroll` ressort « muet » aux deux touches, et **c'est correct** :
`role="region"` plus un libellé qui annonce le défilement horizontal. L'outil
l'écarte de son verdict et le gardien fige ce refus — sinon quelqu'un finira par
« corriger » une région lisible au clavier en un bouton qui ne fait rien.

---

## 6. Gardien — 5 tests, 8 mutations sur 8 tuées

| mutation | résultat |
| --- | --- |
| focus non rendu (1 des 2 sites) | 1 échec |
| mémoire du déclencheur retirée | 1 échec |
| `inert` retiré à la fermeture | 1 échec |
| cycle **arrière** du piège retiré | 1 échec |
| menu contextuel hors de `closeAll` | 1 échec |
| **nav mobile hors de `closeAll`** | 1 échec *(après fermeture du trou)* |
| `Espace` plus testé par l'outil | 1 échec |
| ré-échantillonnage à 6 contrôles | 1 échec |

Le cycle **arrière** mérite sa ligne : un essai qui ne tabule que vers l'avant
ne verrait jamais sa disparition, alors que `Maj+Tab` sortirait de la modale.

---

## 7. Réserve honnête

Les surcouches sont ouvertes par l'**API publique** du produit
(`VX.shell.openModal` / `openDrawer`), pas par un clic sur un déclencheur réel —
les vues en démo en offrent peu. C'est le même chemin de code, mais un
déclencheur qui oublierait de passer par cette API ne serait pas couvert.
