# SKYLER — LOT 599

## Ce que le lot établit

**Une garde de bornes ne garde pas le rôle — et c'est démontré sur les deux
fautes du même lot.** Le lot 596 a produit deux faux retraits ; leurs motifs
sont **différents**, dans **deux bancs différents** :

| banc | motif | classe | ce qu'il a laissé passer |
| --- | --- | --- | --- |
| `l596_inventaire.py` | `retir\|RETIRÉE\|est fausse` | **NU** | « tiers re**tir**és » |
| `l596_elargi.py` | `\bretirée?\b\|\bretiré\b\|\bretire\b\|est fausse` | **GARDÉ** | « **retiré** à la main » |

**Le second portait des bornes de mot et a échoué quand même.** C'est la preuve
directe de 596-B : le problème n'est pas la frontière du mot, c'est son rôle
dans la phrase.

## L'inventaire — 1 941 motifs sur 415 bancs

| forme | sites |
| --- | --- |
| `.startswith` | 463 |
| `'x' in y` | 461 |
| `re.split` | 316 |
| `re.compile` | 157 |
| `re.findall` | 153 |
| `re.search` | 103 |
| `.endswith` / `re.sub` / `re.match` / `.find` / `.count` / `re.fullmatch` | 288 |

Relevé **par AST, pas par regex** — chercher des motifs avec un motif aurait été
exactement la faute mesurée (598-B).

## Les « nus » ne sont pas tous accusables

Un comptage brut donne **1 632 motifs nus (84 %)**. **Ce chiffre accuse à tort.**
La moitié n'a aucun mot de langue naturelle — `'|'`, `'#'`, `'—'`, `'N/D'`,
`'/'` — et n'a donc **aucun homonyme possible** : la question du rôle ne se pose
pas pour eux.

| classe | sites | part des nus |
| --- | --- | --- |
| **NU JUSTIFIÉ** — aucun mot de langue | **766** | 47 % |
| **NU À RISQUE** — contient un mot de langue | **866** | 53 % |

Sur la seule population où la question a un sens :

| classe | sites | part |
| --- | --- | --- |
| **NU À RISQUE** | **866** | **74 %** |
| **GARDÉ** | 302 | 26 % |
| **GARDÉ MAIS INSUFFISANT** | 7 | 1 % |
| **total pertinent** | **1 175** | |

## Le piège, classe MIXTE prévue d'avance (590-A)

| volet | verdict |
| --- | --- |
| **(a)** « la majorité de mes motifs est nue » | **CONFIRMÉ** — **74 %** de la population pertinente |
| **(b)** « les quatre incidents viennent tous de motifs nus » | **RÉFUTÉ** — **4 sur 5, pas 5 sur 5** |
| **global** | **MIXTE** |

Les cinq motifs fautifs, ouverts un par un :

| lot | banc | motif | classe |
| --- | --- | --- | --- |
| 595 | `l595_corps.py` | `'volet'` *(in)* | NU |
| 596 | `l596_inventaire.py` | `retir\|…` | NU |
| **596** | **`l596_elargi.py`** | **`\bretiré\b\|…`** | **GARDÉ** |
| 597 | `l597_lecture.py` | `'arrêt'` *(in)* | NU |
| 598 | `l598_vocab.py` | `…\|et non\|…` | NU |

**Le volet (b) tombe sur un seul cas — mais c'est le cas décisif** : celui qui
prouve qu'ajouter des bornes ne suffit pas.

## L'arrêt du lot — j'avais nommé le mauvais banc

Ma calibration exigeait que le motif `\bretirée?\b…` ressorte en **GARDÉ MAIS
INSUFFISANT**. Elle a **échoué** : le banc que j'avais nommé,
`l596_inventaire.py`, porte un motif **NU**.

**L'instrument avait raison ; mon témoin était mal attribué.** Les deux fautes
du 596 viennent de deux bancs distincts, et je les avais confondues en une.

C'est la troisième fois qu'une calibration écrite d'avance m'arrête — et la
première fois qu'elle m'arrête sur **l'énoncé du témoin** plutôt que sur
l'instrument. **Le banc fautif `l599_motifs.py` est conservé tel quel**, avec sa
calibration en échec : son échec *est* le résultat.

**Arrêtés avant publication : 228 → 229 (+1).**

## Second contrôle (481) — les gardiens du dépôt, et il réfute mon attente

La restriction est « mes bancs du scratchpad ». Le cas exclu : les **1 782
motifs** des **257 fichiers** de `tests/`.

| corpus | population pertinente | nus à risque | part |
| --- | --- | --- | --- |
| **mes bancs** | 1 175 | 866 | **74 %** |
| **gardiens du dépôt** | 1 472 | 1 395 | **95 %** |

**Mon attente disait « le dépôt garde mieux que mes bancs jetables ». Elle est
réfutée** : les gardiens sont **moins** gardés, et largement.

**Et ce n'est pas un défaut.** Un gardien assert sur une chaîne littérale d'un
fichier qu'il contrôle — `'vx-hero' in src`, `'td-shell-v187' in sw` — où
l'homonyme est improbable. Mes bancs, eux, cherchent des mots de langue dans de
la prose française. **Deux profils de risque, pas deux niveaux de soin.**

## Ce que le lot n'établit pas

- **Qu'un motif nu soit une faute.** La très grande majorité des 866 n'a jamais
  produit d'incident. **L'absence de garde n'est pas une erreur réalisée.**
- **Combien d'incidents dorment encore.** Je connais cinq motifs fautifs parce
  que je les ai trouvés. **Le dénominateur des fautes est inconnu**, et aucun
  comptage de motifs ne le donnera.
- Que les 95 % du dépôt soient sans risque : **ils sont expliqués, pas
  vérifiés** — je n'ai lu qu'une poignée de leurs motifs.
- Que ma séparation justifié/à-risque soit juste : **« contient un mot de langue
  de trois lettres » est un critère grossier**, et ce lot montre cinq fois ce
  que valent les critères grossiers.

## Limites déclarées

- L'extraction ne voit que les motifs **littéraux**. Un motif construit par
  concaténation ou passé en variable échappe entièrement.
- `re.split` (316 sites) est compté comme un motif alors qu'il découpe plus
  souvent qu'il ne cherche : **il gonfle le total sans peser sur la question du
  rôle**.
- Les deux corpus sont mesurés au **même critère** mais **ne sont pas
  additionnés** (546-A) : le tableau compare des **parts**, jamais des totaux.
- Les bancs sont **lus, jamais réparés** — pas un motif corrigé (591-B).

## Règles neuves

- **599-A — UNE BORNE DE MOT GARDE LA FRONTIÈRE, PAS LE RÔLE.** Démontré sur
  deux motifs du même lot : le nu et le gardé ont échoué tous les deux, sur des
  phrases différentes. **Ajouter `\b` déplace la faute, il ne la supprime pas.**
- **599-B — UN MOTIF SANS MOT DE LANGUE N'A PAS DE PROBLÈME DE RÔLE.** 766 des
  1 632 « nus » sont de la ponctuation ou des identifiants : les compter comme
  un manque de garde accuse à tort (550-B appliquée à mes propres instruments).
- **599-C — UNE CALIBRATION PEUT ÉCHOUER PARCE QUE LE TÉMOIN EST MAL ATTRIBUÉ,
  PAS PARCE QUE L'INSTRUMENT EST FAUX.** Vérifier d'abord l'énoncé du témoin ;
  l'instrument n'est coupable qu'après.

## Ce que le dépôt fait bien

- **Les gardiens cherchent des chaînes qu'ils contrôlent** : `'vx-hero'`,
  `'td-shell-v187'`, des noms de clés. Leur faible taux de garde est **le
  symptôme d'un corpus sans ambiguïté**, pas d'un relâchement.
- **766 motifs nus sont nus à bon droit** — ponctuation, séparateurs, `'N/D'`,
  `'—'`. Le dépôt n'a pas ajouté de gardes décoratives.
- **Les cinq motifs fautifs sont tous documentés dans un rapport**, avec leur
  phrase piégeuse citée. Aucun n'a été effacé.
- **Les 302 motifs gardés existent** : la garde n'est pas absente du corpus, elle
  est appliquée là où l'auteur a vu le risque — 26 % des cas pertinents.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché, aucun test modifié, aucun motif
  réparé** — inventaire, pas ménage. Pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped** · `git status tests/` et `docs/**` (hors 599) **vides**

## Comptes

- Arrêtés avant publication : **229 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **14**
