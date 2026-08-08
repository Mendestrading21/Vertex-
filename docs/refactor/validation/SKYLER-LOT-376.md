# SKYLER LOT 376 — La piste se referme, mais elle exhibe le contrat de refus honnête

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-376` (base : lot 375 fusionné,
81922b7)

## Piste calibrée, et la consigne : mesurer d'abord

Angle mort déclaré au lot 375 : son détecteur ne reconnaissait que la forme
`Retourne {…}`. Combien de docstrings décrivent leur retour **en prose**, et
tiennent-elles ? La consigne était explicite — **mesurer le volume avant de
promettre un verdict**, précisément parce que le lot 375 s'était fait piéger par
un « 0 » dont personne n'avait compté le dénominateur.

## Mesure

```text
fonctions                                   1321
avec docstring                               674
dont la docstring parle de RETOUR             51
  · forme structurée `Retourne {…}` (lot 375)   6
  · EN PROSE (l'angle mort)                    45
    dont mécaniquement vérifiables              2
```

Deux candidats sur 45. Et les **deux sont de faux positifs** :

```text
multileg_lab.analyze_strategy      « manque » premium, model, refusals
multileg_lab.strategies_for_symbol « manque » cost
```

Lecture faite : `premium`, `model`, `iv` sont des **paramètres d'entrée** et un
bloc de la sortie, `cost` est un champ **du board** (l'entrée). Mon heuristique
prenait tout mot cité entre backticks pour une clé de retour.

**11ᵉ fois de la boucle que l'outil est le premier suspect, et 4ᵉ d'affilée où
mon détecteur accuse du code sain.** Une docstring en prose ne marque pas ce
qu'elle décrit ; la question n'est pas décidable ainsi. **Piste close par la
mesure**, comme le volet 2 du lot 375 — et non par un vert de complaisance.

## Ce que la lecture a exhibé, en revanche

`analyze_strategy` porte un contrat que le lot 375 ne savait pas lire, et qui est
**parfaitement décidable** :

```text
entrée insuffisante ou invalide => {'available': False, 'reason',
                                    'refusals': [{field, value, why}]}
```

C'est l'**invariant produit n°4 de Vertex sous sa forme code** : donnée absente →
motif honnête, jamais un blanc. Un `available: False` sans motif est un refus
**muet** — l'interface affiche un vide que l'utilisateur risque de lire comme
« rien à signaler » plutôt que « je ne sais pas ». C'est exactement le genre de
silence que le produit interdit.

Cette forme précise (`=> {…}`) n'existe qu'**une fois** dans le paquet : ce n'est
pas une famille de docstrings. Mais le **comportement**, lui, est partout.

### Mesure du contrat de refus

```text
`return {available: False, …}` dans le paquet : 13
avec un motif non vide                        : 13
REFUS MUETS                                   :  0
```

Vérifié aussi sur **valeurs réelles** (leçon du lot 374 : la propriété se prouve
sur ce que la fonction renvoie, pas sur la forme du littéral) :

```text
jambes vides   available=False  reason='jambes ou cours sous-jacent manquants.'
cours nul      available=False  reason='jambes ou cours sous-jacent manquants.'
prime absente  available=False  reason='prime manquante sur une jambe — pas de P&L inventé.'
board vide     available=False  reason='aucun contrat pour ce titre dans le board.'
```

Des motifs en français, explicites, adressés à l'utilisateur.

**Verdict : sain, rien touché.** Ce que le lot ajoute, c'est l'invariant : aucun
refus futur ne pourra être muet.

## Gardien

`tests/test_refus_honnete_lot376.py` (9 tests) :

- **périmètre** (leçon du lot 373) : ≥ 100 fichiers, moteurs inclus ;
- **anti-vide** : ≥ 8 refus trouvés — sans dénominateur, un « 0 muet » ne
  prouverait rien (leçon du lot 375) ;
- **la propriété** : aucun refus n'est muet, avec un message d'échec qui dit
  *pourquoi* c'est grave, pas seulement *que* ça échoue ;
- **sur valeurs réelles** : 4 refus provoqués, motif d'au moins 12 caractères et
  non purement numérique ;
- **anti-dérive** : la docstring doit continuer d'annoncer le contrat — c'est
  elle qui fait de ce comportement une promesse ;
- **pas trop strict** : `refusals`, `issues`, `note` sont des motifs légitimes, et
  un test exige qu'il en reste au moins un — sinon la tolérance est sans objet et
  doit être resserrée plutôt que gardée à vide.

### Preuve ROUGE

```text
ROUGE OK  refus rendu MUET (motif retiré)      | restauration identique
          1 failed, 8 passed
ROUGE OK  motif vidé en chaîne vide            | restauration identique
          2 failed, 7 passed
ROUGE OK  contrat retiré de la docstring       | restauration identique
          1 failed, 8 passed
ROUGE OK  motif remplacé par un code numérique | restauration identique
          2 failed, 7 passed
après restauration : 9 passed
VERDICT : gardien mordant sur les 4 cas
```

Le deuxième cas est celui qui compte : un motif vidé en `''` **passe** un contrôle
de présence de clé. C'est l'absence déguisée en présence — et c'est le test sur
valeurs réelles qui l'attrape, pas le test statique.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 375, 81922b7) ; arbre propre.
- **Aucun fichier de production touché** — le lot n'ajoute qu'un test. Pas de
  preuve MD5 requise.
- Suite complète : **2703 → 2712 passed / 2 skipped** — verte (+9).

## Décision SW

**Pas de bump** (`td-shell-v187`) : `tests/` et `docs/` seulement.

## Portée — ce que ce lot ne prétend pas

Le contrat de refus n'est vérifié que sur la forme `return {…'available': False…}`
**littérale**. Un refus construit dans une variable puis renvoyé, ou signalé par
une autre convention (`None`, `{}`, une exception), échappe au détecteur — je n'ai
pas mesuré combien il en existe, et c'est une piste en soi. Les 45 docstrings en
prose restent **non vérifiées** : la mesure dit qu'elles ne sont pas
mécaniquement décidables, pas qu'elles sont justes. Enfin, un motif présent et
long n'est pas un motif **exact** : ce lot vérifie qu'on parle, pas qu'on dit
vrai.

## Suite

LOT 377 : veille active. Pistes ouvertes — (b) les trois sites de concaténation à
constantes du lot 374, sondés pour eux-mêmes ; (c) les formes **imbriquées** des
promesses de retour (lot 375) ; (d) **les autres conventions de refus** (`None`,
`{}`, exception) — angle mort déclaré ci-dessus, et prolongement direct de ce lot.
Prochaine échéance périodique : **~lot 380**.
