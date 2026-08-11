# SKYLER — LOT 598

## Ce que le lot établit

**Le vocabulaire de la boucle a changé de nature au lot 550, et le changement
est massif.**

| fenêtre | rapports | mots accusatoires | mots prudents | prudent / accusatoire |
| --- | --- | --- | --- | --- |
| **lots < 550** | 547 | **394** | **50** | **0,13** |
| **lots ≥ 550** | 48 | **49** | **179** | **3,65** |

**Le rapport s'inverse d'un facteur vingt-huit.** Avant, on écrivait « mort »,
« inutile », « silencieux » ; après, « candidate », « plancher », « sans lecture
observée », « indécidable ».

Et **à date égale**, les rapports qui citent `550-B` sont plus prudents que les
autres — **mais faiblement**, et la marge dépend du critère.

## Le choix (rrr)

Le 597 a trouvé `550-B` par accident, en cherchant autre chose : 14 citations,
13 lots, **zéro crédit**. Cette règle n'avait jamais été mesurée pour elle-même.

## La question du brief n'était pas mesurable telle quelle

Le brief demandait de « relever les libellés de tableaux de classification ».
**Le lot 553 — celui qui porte le mot « candidate » — n'a aucun tableau
markdown** : sa classification vit dans un bloc de texte.

> `ni lue ni nommée — CANDIDATE, rien de plus                20`

Un extracteur de tableaux aurait mesuré **la date d'apparition d'une forme
d'écriture**, exactement la faute que le second contrôle du 595 a caractérisée.
**J'ai donc renoncé à la formulation du brief** et mesuré ce qui traverse les
formes : les mots eux-mêmes.

## Le piège de rôle, nommé d'avance — et il a payé

`550-B` s'énonce dans des phrases qui **refusent** le mot accusatoire :

> « volontairement faible : **candidate**, jamais « morte » » *(553)*

Un comptage naïf y verrait une accusation **dans la phrase même qui la refuse**.
L'instrument devait voir ce cas ; **la calibration est passée du premier coup**
sur ce témoin, nommé avant la mesure.

## Le piège, verdict

| volet | verdict |
| --- | --- |
| **(a)** « le prudent domine après 550, rare avant » | **CONFIRMÉ** — 0,13 → **3,65**, un facteur 28 |
| **(b)** « les rapports citant `550-B` sont plus prudents » | **CONFIRMÉ, faiblement** — voir ci-dessous |
| **global** | **CONFIRMÉ** |

Le volet (a) était **suspect par construction et je l'avais écrit avant de
mesurer** : les rapports antérieurs au 550 **ne peuvent pas** citer `550-B`.
La comparaison avant/après mesure donc **la date autant que la discipline**.
C'est pourquoi le volet (b) existe : il compare **à date égale**.

## Le volet (b) sous deux critères (597-C)

| groupe | lots | prudents | accus. NET | ratio | accus. BRUT | ratio |
| --- | --- | --- | --- | --- | --- | --- |
| **citant `550-B`** | 15 | 61 | 14 | **4,36** | 19 | **3,21** |
| ne citant pas | 33 | 118 | 35 | **3,37** | 39 | **3,03** |

**Le sens tient sous les deux critères** — mais la marge passe de **1,29×** à
**1,06×**. Le signe est robuste ; **l'ampleur ne l'est pas**. Et les effectifs
accusatoires sont de **14 et 35** : aucune loi n'en sort (590-C).

## Les arrêts du lot — trois, dont deux sur mon correcteur

**1. L'instrument que je n'ai pas construit.** Un extracteur de libellés de
tableaux aurait mesuré une forme d'écriture. Ouvert avant d'être bâti (545).

**2. Mon correcteur de rôle a lui-même un problème de rôle.** Il retire du
compte accusatoire les mots en position de refus. Sur ses **9** détections,
**3 seulement sont de vrais refus** (553, 557, 568) ; les **6 autres** viennent
du motif « et non », qui attrape :

> « `VX.states.stale`, **morte et NON supprimée** » *(579, 580, 581, 582, 583)*

où « morte » est une accusation parfaitement réelle. **Le compte NET
sous-compte de 6.** C'est pourquoi le tableau ci-dessus donne aussi le BRUT.

**3. Le second contrôle aurait conclu l'inverse de la vérité.** Le comptage naïf
trouve **63 occurrences dans `vertex/`, 28 dans `tests/`, 1 dans `terminal.py`**
— de quoi annoncer « le vocabulaire prudent a franchi la frontière vers le
produit ». **Faux.** La lecture donne :

```python
def evaluate_candidate(candidate: dict) -> dict:      # vertex/scanner/candidate_pipeline.py
def fundamental_stage(candidate: dict) -> dict:       # vertex/scanner/stages.py
```

**« candidate » y est un mot de MÉTIER** — une valeur candidate du scanner — et
il précède `550-B` de plusieurs centaines de lots. **Mon attente disait « non,
le code nomme pour trancher » : elle est confirmée par la lecture et réfutée par
le comptage.**

**C'est la quatrième fois d'affilée que 596-B mord** — et cette fois **dans le
correcteur censé traiter le rôle**.

**Arrêtés avant publication : 225 → 228 (+3).**

## Ce que le lot n'établit pas

- **Que `550-B` ait CAUSÉ la prudence.** La corrélation entre citation et
  vocabulaire n'est pas une causalité — c'est la limite que le 597 a posée sur
  les crédits, et elle vaut ici mot pour mot. **Le renversement de vocabulaire
  au 550 coïncide avec la règle ; rien ne prouve qu'il en découle.**
- **Qu'un libellé prudent soit meilleur.** Nommer « candidate » ce qui est
  réellement mort est aussi une erreur. Le lot mesure un vocabulaire, il ne le
  juge pas.
- Que les quatre mots prudents et les quatre accusatoires épuisent le
  vocabulaire : **ce sont huit mots choisis, pas un lexique**.
- Que la marge du volet (b) soit significative : **1,06× sous le critère brut**.

## Limites déclarées

- Le comptage accusatoire **NET sous-compte de 6 sites**, mesuré et déclaré ;
  le BRUT est donné à côté partout où il change quelque chose.
- Les huit mots sont cherchés **avec bornes de mot et accents** (« morte »,
  « indécidable ») — `a·mort·i` et `ter·rien` ne sont jamais comptés.
- La fenêtre « avant 550 » compte **547 rapports** contre **48** après : les
  totaux ne se comparent pas, seuls les **ratios** le font.
- Le second contrôle porte sur `vertex/`, `tests/` et `terminal.py` ; les
  fichiers non lisibles en UTF-8 sont sautés en silence.

## Règles neuves

- **598-A — UN CORRECTEUR DE RÔLE A LUI AUSSI UN RÔLE À VÉRIFIER.** Mon filtre
  anti-faux-positifs a produit **6 faux positifs sur 9**. Corriger un critère ne
  le met pas au-dessus du critère.
- **598-B — UN MOT DE MÉTIER N'EST PAS UN MOT DE MÉTHODE.** « candidate » dans
  un pipeline de scanner et « candidate » dans une classification prudente sont
  homonymes ; les compter ensemble inverse la conclusion.
- **598-C — QUAND UN VOLET COMPARE DEUX ÉPOQUES, IL MESURE LA DATE ; SEUL UN
  VOLET À DATE ÉGALE MESURE LA DISCIPLINE.** Le volet (a) valait 28×, le volet
  (b) 1,06× à 1,29× : **c'est le second qui répond à la question posée**.

## Ce que le dépôt fait bien

- **Le renversement de vocabulaire est réel, daté et visible** : 0,13 avant,
  3,65 après. Quelle qu'en soit la cause, la prudence lexicale s'est installée.
- **Les phrases qui posent la prudence nomment le mot qu'elles refusent** —
  « candidate, jamais morte », « pas servie pour rien », « ne s'appelle pas
  échecs silencieux ». **La règle se transmet avec son contre-exemple.**
- **Le code ne s'est pas contaminé de prose** : les mots prudents qu'on y trouve
  sont du métier, pas de la méthode. La frontière tient.
- **`550-B` est citée dans 15 rapports sur 48** sans jamais avoir été créditée.
  Une règle peut vivre longtemps sans compteur.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché, aucun test modifié, aucun libellé
  renommé** — mesure de vocabulaire, pas ménage. Pas de bump, SW
  `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped** · `git status tests/` et `docs/**` (hors 598) **vides**

## Comptes

- Arrêtés avant publication : **228 (+3)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **14**
