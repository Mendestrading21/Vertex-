# SKYLER LOT 492 — Les deux barèmes réellement peints, tracés jusqu'au producteur : « accord /100 » est SAIN, « confiance /100 » plafonne à 95 — et les DEUX bornes du garde-fou du comité sont MORTES

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-492` (base : lot 491 fusionné,
`28e1eb65`)

**Aucun code, aucun gardien, aucun test. Aucun fichier de production touché.**

Le 491 avait nommé sa dette : « la prochaine mesure partira des **deux barèmes
réellement peints** ». Septième dette nommée payée d'affilée.

## D'abord : vérifier que je mesure bien ce qui s'affiche (leçon 491)

Chaîne établie **avant** toute mesure : `analysis_page.py:735`
`VX.fetch('/api/decision/'+SYM)` → `decision_api.py:58-59` qui renvoie
`'confidence': r['confidence']` et `'agreement': com.get('agreement')` →
`decision_stack`. **Les deux chiffres affichés viennent bien de là.** Cette fois,
la vérification est faite **au début**, pas après un lot perdu.

`decision_stack` **ne contient aucune écriture** (vérifié : ni `save_json`, ni
`open(`, ni `.record(`, ni `persist`). Banc sûr ; `persist` redirigé quand même.

## Le brief était incomplet — deux fois

Contrôlé sur pièces (leçon 490) :

- il donnait la formule `int(max(0, min(100, round((base_conf + committee)/2))))`
  en **omettant le terme `- dq.get('confidence_penalty', 0)`** ;
- il ne mentionnait **pas** que le comité a **son propre garde-fou**,
  `int(max(20, min(95, round(45 + agreement*45 - 15*contradiction))))` (`:247`) ;
- il situait `agreement` en `:251` — c'est **`:252`**.

C'est justement ce garde-fou omis qui porte la trouvaille.

## Calibration, écrite dans le code

Sur la formule relue, deux réponses déductibles à la main :

```text
agreement = 1, sans contradiction  → 45 + 45      = 90   OK
agreement = 0, avec contradiction  → 45 − 15      = 30   OK
```

Et sur le banc `evaluate()` : **la porte de qualité ne doit pas bloquer**
(`blocks_decision = False`), sinon le banc mesure autre chose — voir plus bas.

## Trouvaille — les deux bornes du garde-fou du comité sont inatteignables

`agreement = abs(lean − 0.5) × 2` est borné dans **[0, 1]** par construction.
L'expression `45 + agreement×45 − 15×contradiction` parcourt donc **[30, 90]**.
Énumération complète de l'espace d'entrée (agreement au centième × contradiction) :

```text
61 valeurs distinctes · MIN 30 · MAX 90
borne basse  max(20, …)  →  NE MORD JAMAIS  (plancher réel 30)
borne haute  min(95, …)  →  NE MORD JAMAIS  (plafond réel 90)
```

**Les deux gardes sont morts.** Et le plus parlant est le haut : l'auteur a écrit
un plafond à **95** que la formule ne peut pas approcher — elle s'arrête à **90**.
Le code exprime une échelle 20-95 qui **n'existe pas**.

## Le chiffre affiché « confiance X/100 » ne peut jamais atteindre 100

```text
confiance = clamp(0, 100, (base_conf + comité)/2 − pénalité_qualité)
            comité ≤ 90  (mesuré ci-dessus)
            base_conf = scoring.compose(...)['confidence'], défaut 55 si absent

→ MAXIMUM ABSOLU = (100 + 90) / 2 = 95.   Jamais 100.
```

Banc réel sur `evaluate()`, porte de qualité franchie :

```text
d.confidence absent → « confiance 72/100 »   (défaut 55, comité 90)
d.confidence = 90   → « confiance 90/100 »
d.confidence = 100  → « confiance 95/100 »   ← le maximum
« accord 100/100 » dans les trois cas · comité 90 · lean 100
```

**« accord X/100 » atteint bien 100 : c'est le témoin POSITIF du lot.** Sans lui,
un instrument qui rendrait « tout est plafonné » serait indistinguable d'un
instrument juste.

### Le producteur réel de `base_conf` — et une hypothèse à moi, réfutée

Je pensais que `d['confidence']` était presque toujours absent, donc que la
moitié du chiffre était la constante **55**. **Faux.** `vertex/quant/scoring.py:139` :

```python
out['confidence'] = round(_clip(100 - min(float(np.std(core)) * 2.5, 60)))
```

Il **est** produit, et vaut **50** sur mon entrée d'essai. Formule bornée dans
**[40, 100]** ; **balayage de 2 700 combinaisons d'indicateurs : [40, 73]**.
La borne haute de 100 exige un écart-type **nul** entre les quatre sous-scores —
que ma grille n'a pas produit. **C'est une propriété de ma grille, pas du
produit** (règle 459), et je le dis.

Sur cette grille, le chiffre affiché plafonne donc à **(73 + 90)/2 = 82**.

## Ce que je refuse de faire : gonfler

**Aucun rang posé, et je dis pourquoi.**

Un plafond à 95 sur une échelle annoncée /100, c'est **cinq points inatteignables
sur cent**, sur une grandeur explicitement heuristique. Comparé au 484-B — un
« /40 » qui plafonne à 29, soit **27,5 %** hors d'atteinte, sur la carte de
décision — l'écart n'est pas du même ordre. **Un utilisateur qui lit
« confiance 82/100 » n'est pas trompé par le fait que 96-100 soit hors
d'atteinte.** → **observation, pas dossier.**

Les deux bornes mortes du comité sont **internes** : `min(95, …)` n'atteint
aucune surface servie. Règle 486/491 — **un défaut non affiché se nomme, il ne se
classe pas.** → **observation.**

## Le second contrôle — un cas que le banc EXCLUAIT

Mon banc fabriquait un `detail` **sans pénalité de qualité**. Cas exclu : le scan
rassis.

```text
age=None  → pénalité  0 · grade A · « confiance 72/100 »
age=1200  → pénalité 15 · grade B · « confiance 38/100 »
demo=True → pénalité  0 · grade A · inchangé
```

Deux enseignements. **(1)** Une pénalité de 15 fait chuter le chiffre de **34
points**, pas de 15 : le drapeau `stale` modifie aussi les preuves, donc le lean,
donc le comité. **L'effet d'une pénalité n'est pas additif, et rien ne le dit.**
**(2)** Symétrie utile : la borne **basse** `max(0, …)` du chiffre affiché, elle,
**est atteignable** — pénalité maximale 60 contre un plancher de (40+30)/2 = 35,
donc −25, clampé à 0. **Un garde-fou mort en haut, un garde-fou vivant en bas,
dans la même expression.**

## Deux faux résultats arrêtés avant publication

1. **Mon premier banc `evaluate()` mesurait la branche `DATA_INSUFFICIENT`** — le
   `detail` fabriqué n'avait pas de `plan`, donc `blocks_decision` était vrai et
   la fonction renvoyait `confidence = 0` **trois fois de suite**. J'aurais pu
   publier « le chiffre affiché vaut toujours 0 ». **Diagnostiqué, pas conclu**,
   et une calibration explicite (`blocks_decision` doit être faux) a été ajoutée
   au banc.
2. **Mon scan AST affirmait que `compose()` ne renvoie pas `confidence`** — il
   cherchait un `return {...}` littéral, or la fonction remplit un `out` puis le
   renvoie. **L'exécution a répondu l'inverse.** J'allais bâtir tout le lot sur
   « base_conf est toujours la constante 55 ».

**Arrêtés avant publication : 57 → 59.**

## Portée

- Les bornes du **comité** sont établies par **énumération complète** d'une
  formule déterministe : c'est une preuve, pas un échantillon.
- Les bornes de **`compose()['confidence']`** viennent d'un **balayage de grille**
  — **[40, 73] mesuré, [40, 100] par formule**. La différence est nommée.
- Le banc **fabrique un `detail`** : il établit ce que le moteur **peut** rendre,
  pas la distribution en usage.
- **Aucun navigateur ouvert** ce lot : la chaîne d'affichage est établie par
  lecture du code client et de la route, et elle avait été vérifiée au 491.
- **Trois barèmes restent non tracés** : `best.score /100`, `edge /100`,
  `r.score /100` (`/opportunities`), plus `count / 10 max` et `rating_mean/5`.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié ; sorties en chemin
  **absolu** (incident 487).
- **Aucun fichier de production touché.** Pas de bump. SW : `td-shell-v187`.
- `persist` redirigé **et vérifié** ; `decision_stack` **sans écriture**, vérifié ;
  aucune route réseau sortante.
- **MD5 des 8 pages remesurés : 8 / 8 identiques.**
- Snapshot runtime : 21 fichiers, aucun apparu, aucun disparu, écart **AUCUN**.
- Suite : **2864 passed / 0 skipped**, lancée **après** les trois documents.

## Où en est la boucle

**Deuxième lot consécutif sans nouveau dossier classé**, et ce n'est pas une
panne : c'est ce que donne une veine correctement mesurée quand elle se vide. Le
491 avait nettoyé la liste de cibles ; le 492 en trace deux jusqu'au bout et
trouve **un témoin sain, un plafond mineur et deux gardes morts**.

Le fait le plus utile est de méthode, et il est déjà connu : **l'exécution
décide**. Deux fois dans le même lot, une lecture — mon AST, mon premier banc —
donnait une réponse nette et fausse. La règle tient parce qu'on la paie.

Comptes séparés : résultats faux **arrêtés avant publication 59 (+2)** ; publiés
puis corrigés **10** ; interprétations retirées **3**.

**Neuf bilans — n°9 à n°17 — attendent une réponse.**
