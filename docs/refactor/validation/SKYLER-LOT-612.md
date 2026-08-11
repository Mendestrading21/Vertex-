# SKYLER — LOT 612 · L'EN-TÊTE PROMETTAIT 40 PX, DEUX LIGNES AU-DESSUS D'UN 32

Le brief soupçonnait un **oubli** sur les boutons des bandeaux. La lecture du CSS
a montré une **exemption écrite**, et la mesure a montré qu'elle est **générale**.
Le défaut n'est donc pas le seuil : **c'est ce que le code dit de lui-même**.

## Ce que le CSS annonçait

```css
/* responsive.css, ≤ 768 px */
/* Cibles tactiles ≥ 40px */
.vx-btn,.vx-tab,.vx-chip{min-height:40px}
.vx-btn-sm{min-height:32px}          ← deux lignes plus bas
```

Un en-tête qui promet « ≥ 40px » **immédiatement suivi d'un 32**. Il décrivait
une **intention**, pas le bloc.

## La mesure, à 390 px, cinq écrans en état d'échec

| famille | boutons | hauteurs | sous 40 px |
| --- | --- | --- | --- |
| **dans les bandeaux d'état** | **20** | **32 px** *(toutes)* | **20 / 20** |
| **hors bandeaux** *(témoin, même page, même largeur)* | **42** | 32 px et 40 px | **20 / 42** |

**Vingt boutons hors bandeaux sont au même 32 px.** Les bandeaux ne sont donc
**pas un angle mort** : `.vx-btn-sm` est une règle générale des actions
**secondaires**, appliquée uniformément à **40 boutons** du produit.

Largeurs mesurées : **82 à 130 px** — aucune difficulté horizontale.

Témoin à 1440 px : les mêmes boutons font **26–28 px**, et les 42 témoins sont
tous sous 40 — normal, la règle mobile ne s'y applique pas. **Le passage 26 → 32
prouve que la règle mobile s'applique bien** aux bandeaux : ils ne sont pas
hors de sa portée, ils sont dans son exemption.

## Ce que le lot corrige — et ce qu'il refuse de corriger

**Corrigé** : l'en-tête décrit désormais **deux seuils**, dit que le second est
une exemption **assumée** pour les actions secondaires, donne le chiffre mesuré
(40 boutons, dont 20 hors bandeaux), et note que 32 px reste sous les
recommandations d'accessibilité usuelles.

**Refusé** : porter `.vx-btn-sm` à 40 px. Cela toucherait **40 boutons** et
changerait la mise en page mobile de tout le produit. **C'est une décision de
design, pas un correctif** — et rien dans la mesure ne prouve que 32 px nuit.
La décision revient à l'humain ; le lot lui donne le chiffre pour la prendre.

C'est **609-C** : refuser d'ajouter est un résultat. Et c'est la limite que la
boucle se donne — corriger ce que le code **dit**, pas ce que le design **choisit**.

## Le piège, écrit avant de mesurer

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « les boutons des bandeaux mesurent 32 px » | **CONFIRMÉ** — exactement, sur les 20 |
| **(b)** | « 32 px est sous le standard du dépôt, donc c'est un défaut à corriger » | **RÉFUTÉ DANS SA PRÉMISSE** — ce n'est pas un angle mort mais une règle générale ; le défaut est la **description**, pas le seuil |
| **(c)** | « la largeur n'est pas un problème » | **CONFIRMÉ** — 82 à 130 px |
| **(d)** | « ces boutons existent bien à 390 px » | **CONFIRMÉ** — 20 boutons ; sans quoi le lot aurait été sans objet |
| **global** | | **le brief cherchait un oubli ; il y avait une décision mal décrite** |

**(d) méritait d'être posé** — le brief lui-même demandait de le vérifier
d'abord. S'il avait été faux, mesurer des hauteurs n'aurait rien signifié
(600-A).

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesure **les boutons des bandeaux**. Le cas exclu : **les autres
`vx-btn-sm` du produit** — s'ils sont rares, l'exemption vise un cas précis ;
s'ils sont nombreux, c'est une règle de design.

**Vingt boutons hors bandeaux, à 32 px, sur les mêmes cinq écrans.** C'est ce
contrôle, et lui seul, qui a réfuté (b) : sans lui j'aurais corrigé le seuil des
bandeaux en croyant réparer un oubli, et j'aurais **cassé l'uniformité** — une
famille de boutons à 40, une autre à 32, sans raison lisible.

## Ce que le lot n'établit pas

- **Que 32 px suffise au doigt.** Aucun test d'usage. Les recommandations
  usuelles (44 pt, 48 dp) sont **plus hautes** que le seuil primaire du dépôt
  lui-même. Le chiffre est posé ; le jugement appartient à l'humain.
- **Le contraste et la lisibilité du texte** — toujours non mesurés, après trois
  lots (610, 611, 612) qui n'ont jugé que la **géométrie**.
- **La hauteur des bandeaux eux-mêmes** ni le débordement vertical.
- Que les 62 boutons mesurés soient tous ceux du produit : ce sont ceux que
  **cinq écrans en échec** exposent.

## Règles neuves

- **612-A — UNE EXEMPTION ÉCRITE N'EST PAS UN OUBLI.** `.vx-btn-sm{32px}` figure
  deux lignes sous la règle qu'elle contredit : quelqu'un l'a voulue. Avant de
  corriger un écart à une règle affichée, chercher si l'écart **est lui-même une
  règle**.
- **612-B — QUAND LE CODE ET SON COMMENTAIRE DIVERGENT, C'EST LE COMMENTAIRE
  QU'IL FAUT D'ABORD RÉPARER.** Changer le code aligne le produit sur une phrase
  que personne n'a validée ; changer la phrase rend la décision visible et laisse
  le choix ouvert.
- **612-C — LE SECOND CONTRÔLE (481) EST CE QUI DISTINGUE UN ANGLE MORT D'UNE
  RÈGLE.** Sans les 20 boutons témoins hors bandeaux, ce lot aurait « corrigé »
  une décision de design en croyant réparer un oubli.

## Ce que le dépôt fait bien

- **L'exemption est explicite et unique** : un seul endroit fixe la hauteur des
  actions secondaires, appliqué uniformément aux 40 boutons.
- **La règle mobile atteint bien les bandeaux** : 26 px au bureau, 32 px au
  tactile. Ils sont dans le périmètre de la règle, pas en dehors.
- **Les commentaires du bloc datent leurs décisions** — « lot 294 : les contrôles
  segmentés mesuraient 26px ». L'habitude d'écrire *pourquoi* était déjà là ;
  seul l'en-tête général avait vieilli.
- **Aucun bouton n'est étroit** : 82 à 130 px de large, très au-dessus du besoin.

## Cycle

- Anti-doublon : réveils tous `run_once_fired`, **0 actif**.
- **2 fichiers de production** : `vertex/static/vertex/css/responsive.css`
  (commentaire seul — **aucune règle CSS modifiée**), `vertex/app/routes/system.py`
  (bump).
- **1 gardien neuf** (4 tests, rouge dans les deux sens) + **5 épingles**
  `td-shell-v194` → **`td-shell-v195`** + empreinte des assets et `_SW_VERSION`
  du gardien 361.
- MD5 des 8 pages : **8 / 8 identiques**.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2905 passed / 0 skipped** *(2901 + les 4 du gardien neuf)*.
- Navigateur : **10 chargements** (5 écrans × 2 largeurs), **62 boutons mesurés
  par largeur**, dont **42 en témoin hors bandeau**.
- **READONLY intact.**

## Comptes

- Arrêtés avant publication : **245**
- Publiés puis corrigés : **41**
- Interprétations retirées : **15**
- **Dossiers produit corrigés : 9** *(l'en-tête qui décrivait une intention et
  non son bloc)*
