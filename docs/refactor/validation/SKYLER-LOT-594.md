# SKYLER — LOT 594

## Ce que le lot établit

**La force d'une assertion de sous-chaîne ne tient pas à la nature de son
corpus, mais à la question de savoir si ce corpus CROÎT.**

`assert 'GO' in idx` est satisfait **609 fois**. Il survit au retrait des **587
verdicts `GO` délibérés** : il resterait **22 occurrences** cachées dans
`GOOGL`, `CATÉGORIE`, `GONFLÉ`, `GOALKEEPER`, `GOUVERNÉE`. **Ce gardien ne garde
même pas la colonne qu'il a l'air de garder.**

En face, les trois assertions du gardien 228 portent sur `head` — les **600
premiers caractères**, une meule **bornée par construction** — et sont
satisfaites **une seule fois chacune**. Elles tombent au premier retrait.

## Le choix (nnn)

Le 593 a laissé une question explicitement non tranchée : `assert 'GO' in idx`
est-il intentionnel ou accidentel ? **La question d'intention n'est pas
mesurable ; la force de garde l'est.**

## Dix-neuf sites, pas quatre (581-A)

Le brief en nommait quatre. L'AST, passé sur les quatre gardiens, en relève
**19** — dont **15 que le brief ne nommait pas**.

| meule | sites | traitement |
| --- | --- | --- |
| **document sur disque** — `idx`, `head`, documents vivants | **5** | mesurés |
| **corps rendu** — un `body` HTML produit par un GET | **14** | **nommés, pas ouverts** |

Les 14 exigent d'appeler la vue post-mortem et `/memory/…`, **hors de ma liste
sûre**. Ils sont comptés et laissés fermés. C'est la restriction de
l'instrument, déclarée avant la mesure.

## La force de garde, mesurée

| assertion | meule | croît ? | occurrences | force |
| --- | --- | --- | --- | --- |
| `'GO' in idx` | tout l'index — **1 184 525 car.** | **OUI** | **609** | **INERTE** |
| `'lots' in head` | `idx[:600]` | non | **1** | **maximale** |
| `'10' in head` | `idx[:600]` | non | **1** | **maximale** |
| `'STATUS.md' in head` | `idx[:600]` | non | **1** | **maximale** |
| `'RETIRÉ' in ligne` *(lot 364)* | chaque ligne des 4 documents vivants | oui | **17 lignes** | moyenne |

`RETIRÉ` se répartit ainsi : `CLAUDE.md` **0** · `ANNEXE-E1-RETRAITS.md` **3** ·
`SKYLER-INDEX.md` **9** · `STATUS.md` **5**.

## Le retrait poussé à bout

| état de l'index | occurrences de `GO` | l'assertion tient ? |
| --- | --- | --- |
| tel quel | 609 | oui |
| **privé de ses 587 verdicts `GO`** | **22** | **oui encore** |
| privé aussi des 22 fragments | 0 | non |

**Pour faire tomber ce gardien il faudrait vider l'index de tout mot contenant
les deux lettres `GO`** — y compris le ticker `GOOGL` et le mot « catégorie ».

## Deux des trois aiguilles sont dans la même phrase

L'en-tête, ouvert et non deviné (545) :

> « Périmètre : lots **10 et suivants**. »

`'lots'` est en position **81**, `'10'` en position **88** : **sept caractères
d'écart, dans le même groupe de mots**. `'STATUS.md'` est en position **259**,
dans la phrase suivante.

**La conjonction à trois termes n'a donc que DEUX points de rupture
indépendants.** Supprimer sept mots en tue deux d'un coup.

En revanche — et c'est à porter au crédit du dépôt — **les trois aiguilles
désignent réellement ce que la docstring promet** : « lots 10 et suivants » *est*
le périmètre, et `STATUS.md` *est* l'endroit où vivent les rapports pré-index.
**Aucune ne passe par accident.** Je m'attendais à trouver un `'10'` parasite
venu d'un « 100 » ; il n'y en a pas.

## Le piège, classe MIXTE prévue d'avance (590-A) — quatrième d'affilée

| volet | verdict |
| --- | --- |
| **(a)** « `GO` apparaît des centaines de fois, l'assertion est inerte » | **CONFIRMÉ** — 609, et elle survit au retrait des 587 |
| **(b)** « `'10'` est la plus fragile des quatre » | **RÉFUTÉ** — trois sont **à égalité stricte à 1** |
| **global** | **MIXTE** |

**Quatre MIXTE consécutifs : je l'avais noté d'avance comme suspect, je le
tiens.** L'explication n'est pas le hasard, c'est la forme de mes pièges : le
volet (a) est une affirmation **large et qualitative** (« des centaines »), le
volet (b) une **prédiction de classement précise**. Les premières passent
presque toujours, les secondes échouent presque toujours. **Le MIXTE est
fabriqué par la structure de mes attentes, pas découvert dans le dépôt.**

## L'arrêt du lot — ma propre prose a dépassé mes propres tableaux

Deux fois dans ce lot, la phrase de conclusion d'un banc a dit plus que le
tableau imprimé juste au-dessus :

| banc | son tableau | sa phrase |
| --- | --- | --- |
| `l594_second.py` | « **4 sur 15** à une seule occurrence » | « **chaque** occurrence est la seule de son fichier » |
| `l594_croissance.py` | « **502** lignes sur 584 portent un `GO` (86 %) » | « **chaque** lot ajoute une ligne qui porte son verdict » |

**C'est exactement l'écart que je mesurais chez les gardiens du dépôt** — la
prose plus large que le code (592-B, 593-A) — **reproduit par moi, dans le lot
même qui l'étudie.** Les deux phrases sont arrêtées avant publication ; **les
deux bancs sont conservés tels quels**, fautes comprises.

**Arrêtés avant publication : 219 → 220 (+1).**

## Calibration (574-A)

Contrôle choisi avant d'ouvrir quoi que ce soit : l'inventaire AST doit
retrouver les **quatre** assertions établies par lecture au lot 593. Il les
retrouve **toutes les quatre**, et en révèle 15 de plus. **Passée du premier
coup**, et je le dis comme une mesure, pas comme un mérite.

## Second contrôle (481) — hors du périmètre documentaire

La restriction « gardiens documentaires » exclut les gardiens de production.
Ils portent **1 437 sites** de sous-chaîne littérale sur **239 fichiers**.

Mesuré sur les clés de synchronisation du desk (lot 381), meule = fichier
réellement servi :

| meule | étendue des occurrences |
| --- | --- |
| `vertex/static/vertex/js/vx-entities.js` | 4 à 15 |
| `vertex/ui/pages/system_page.py` | 1 à 3 |
| `vertex/ui/vx_kit.py` | 1 à 7 |

**4 couples sur 15 sont à une seule occurrence.** Mon attente disait « une
assertion sur du code servi est plus forte » : **réfutée**. La fourchette de
production (**1 à 15**) tient tout entière **à l'intérieur** de la fourchette
documentaire (**1 à 609**). Ce n'est pas prose contre code — c'est **borné
contre croissant**.

## Ce que le gardien perd à chaque lot

L'index compte **584 lignes de lot**, dont **502 (86 %)** portent au moins un
`GO` ; **567** des 587 `GO`-mots vivent dans ces lignes, **20** ailleurs.

**Le gardien s'affaiblit du travail même qu'il accompagne** : chaque lot livré
ajoute une ligne, et le plus souvent une occurrence de plus. `head`, borné à 600
caractères, ne s'affaiblit jamais.

## Ce que le lot n'établit pas

- **Que `assert 'GO' in idx` soit intentionnel ou accidentel.** Le 593 l'avait
  déclaré non déterminé ; compter des occurrences ne répond pas à une question
  d'intention, et **je ne prétends pas y répondre**. La mesure ajoute un seul
  fait : l'assertion ne peut pas avoir été calibrée sur l'index d'aujourd'hui.
- **Qu'un gardien inerte soit un défaut.** Il passe, et il passait déjà quand
  l'index était mille fois plus petit. C'est un constat de portée.
- Que les 14 sites à meule rendue se comportent comme les 5 mesurés : **ils
  n'ont pas été ouverts**.
- Que la loi « borné contre croissant » vaille au-delà de ces 20 mesures :
  **c'est une tendance, sur un petit nombre** (590-C).

## Limites déclarées

- Le partage des 19 sites entre « document » et « corps rendu » repose sur le
  **fichier et la ligne**, lus ; il n'a pas été vérifié en exécutant les tests.
- Le comptage de `GO` est celui du **littéral**, comme le gardien : 609. Le
  comptage en **mot entier** donne 587. **Deux définitions, déclarées, jamais
  additionnées** (546-A).
- « 584 lignes de lot » vient d'un motif lu sur l'index (`| <numéro> |`), pas
  d'un décompte des rapports sur disque — **ce n'est pas le « 582 » du 593**,
  qui comptait des fichiers cités.
- Les retraits sont **simulés en mémoire**. Aucun octet du dépôt n'a bougé.

## Règles neuves

- **594-A — LA FORCE D'UNE ASSERTION DE SOUS-CHAÎNE SE MESURE À LA CROISSANCE
  DE SA MEULE, PAS À SA NATURE.** Borné → forte ; croissant → inerte. Prose ou
  code servi n'y change rien.
- **594-B — POUR UN GARDIEN, FRAGILE ET FORT SONT LE MÊME MOT.** Une assertion
  qui tombe au premier retrait fait son travail ; celle qui survit à 587
  retraits ne garde rien. Mon piège appelait « la plus fragile » ce qui était en
  fait la plus solide.
- **594-C — UN PIÈGE À DEUX VOLETS DONT L'UN EST QUALITATIF ET L'AUTRE UN
  CLASSEMENT PRÉCIS PRODUIT UN MIXTE PAR CONSTRUCTION.** Quatre d'affilée : le
  verdict venait de la forme de l'attente, pas du dépôt.

## Ce que le dépôt fait bien

- **Les trois aiguilles de l'en-tête désignent vraiment le périmètre.** Aucune
  ne passe par accident — je cherchais un faux positif, il n'y en a pas.
- **L'en-tête tient la promesse en 600 caractères** : périmètre, exclusion des
  lots 01→09, renvoi à `STATUS.md`, branche d'intégration, `main` jamais
  touchée. Un lecteur sait où il est avant la première ligne du tableau.
- **`ANNEXE-E1-RETRAITS.md` porte 3 lignes `RETIRÉ`** et l'index 9 : la trace
  des retraits est écrite là où le gardien 364 la cherche.
- **86 % des lignes de lot portent un verdict explicite.** La colonne `GO`
  affaiblit un gardien, mais c'est d'abord une discipline tenue sur 584 lignes.

## Cycle

- Anti-doublon : `total 100 · actifs 0`.
- **Aucun fichier de production touché, aucun test modifié, aucune docstring
  corrigée, aucun octet supprimé** — pas de bump, SW `td-shell-v187`.
- MD5 des 8 pages : **8 / 8 identiques** (SW `td-shell-v187`)
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN** (22 fichiers ; 3 modifiés par la suite, restaurés)
- Suite : suite **2864 passed / 0 skipped** · `git status tests/` et `docs/**` (hors 594) **vides**

## Comptes

- Arrêtés avant publication : **220 (+1)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **13**
