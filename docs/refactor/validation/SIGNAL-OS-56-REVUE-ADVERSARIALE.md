# SIGNAL OS · LOT 56 — DIX QUESTIONS HOSTILES, ENFIN AFFICHÉES

Branche : `agent/vertex-signal-os-v1` · SW **v239 → v240** · Suite **3 459 passed**
(3 454 → +5)

Le premier lot construit **sur** l'instrument du lot 55, et il valide l'instrument
autant que le produit : `red_team_review` est la sortie la plus riche du dossier
Skyler, et rien ne la lisait. Aucun des inventaires précédents ne pouvait la
voir — c'est une clé de **premier niveau** de la réponse, sans le moindre rapport
de nom avec son module `red_team`.

---

## 1. Ce qui était calculé, envoyé, et jamais montré

`/api/skyler/<sym>` sert, à côté de `decision` et `packet`, un troisième objet :

```json
"red_team_review": {
  "questions": [
    {"id": "Q01", "status": "ANSWERED", "evidence_level": "F2",
     "question": "Qu’est-ce qui est déjà dans le prix ?",
     "answer": "Le prix intègre déjà : RSI 65 — plus la lecture est tendue, plus l’avantage restant est faible."},
    {"id": "Q02", "status": "ANSWERED", "evidence_level": "F1",
     "question": "Quel chiffre peut être trompeur ?",
     "answer": "Blocs insuffisants : data_quality, fundamentals_quality ; MODE DÉMO étiqueté — tout chiffre issu de ces blocs vaut 0, jamais une estimation."}
  ],
  "answered": 10, "complete": true
}
```

**Dix questions hostiles au dossier**, répondues avec les seules données
présentes, chacune portant son niveau de preuve. La décision n'en retenait que
deux champs (`complete`, `basis`) ; les dix questions elles-mêmes voyageaient
jusqu'au navigateur pour n'y rien produire.

C'est le motif du dossier 454 à son degré le plus coûteux : non pas une valeur
perdue, mais **le raisonnement adverse** — précisément ce qu'un opérateur veut
lire avant d'engager du capital.

---

## 2. Le point qui décide de l'honnêteté du bloc

Le moteur émet deux états, et le second compte davantage :

| état | ce que porte la question |
| --- | --- |
| `ANSWERED` | `answer` + `evidence_level` |
| `UNANSWERED` | une `reason`, et **rien d'autre** |

Le moteur le dit lui-même : *« les objections sans preuve restent ouvertes et ne
valident jamais le dossier »*. Une revue qui afficherait les réponses en taisant
les questions ouvertes transformerait une revue **incomplète** en satisfecit.
C'est le mensonge exact que cette série traque depuis le lot 35, et il aurait été
facile à commettre ici : le jeu de démonstration répond aux dix.

Le rendu montre donc les questions ouvertes **en premier**, les compte à part
dans le résumé (« N ouverte(s), jamais comblée(s) ») et affiche leur raison à la
place d'une réponse absente.

Deux tests ne servent qu'à cela, et ils **fabriquent** une question ouverte —
appel du moteur sur un packet vide — au lieu d'attendre qu'il en existe une.
Attendre, c'était ne jamais éprouver la branche qui empêche le satisfecit.

---

## 3. Vérifié au pixel — et la sonde a d'abord dit « absent »

Premier passage de `tools/mesurer_blocs_peints.py` :

```text
revue adversariale (lot 56)   ABSENT  ancre=oui · lignes 0/2 dans le bloc
```

Ancre visible, lignes introuvables. Le chiffre qui explique tout :
`#an-skyler` portait **5 258 caractères écrits pour 3 183 montrés**. L'écart est
exactement le contenu du nouveau `<details>`, replié. La sonde n'ouvrait que deux
disclosures ; il y en a désormais **trois**. Ce n'est pas un défaut produit — le
repli est voulu, comme pour les contextes — mais un rappel utile : *chaque bloc
replié ajoute une porte au chemin du produit, et une sonde qui ne la franchit pas
rend « jamais peint » sur un produit correct.*

Après ouverture au clic — le geste du produit, jamais un `open=true` :

```text
contextes (lot 49)             PEINT  3/3      préparation (lot 54)         PEINT  2/2
fiabilité (lot 50)             PEINT  3/3      revue adversariale (lot 56)  PEINT  2/2
contextes du dossier (lot 51)  PEINT  3/3
#an-skyler : 5 216 caracteres ecrits · 5 327 montres
```

Les quinze hôtes de la fiche aboutissent toujours (`mesurer_hotes_resolus.py`).

---

## 4. Le gardien, et ses quatre mutations

| mutation | test qui tombe |
| --- | --- |
| `+revueAdversariale(r)` retiré du rendu | le site d'appel (leçon du lot 49) |
| le tri des questions ouvertes neutralisé | la distinction des deux états |
| le compte des ouvertes retiré du résumé | la même |
| **le moteur comble une question ouverte** avec une réponse | l'état ouvert lui-même |

La quatrième est la plus importante : elle ne garde pas la mise en page mais **la
règle du moteur** — une objection sans preuve ne doit jamais être présentée comme
traitée. Elle tomberait même si l'interface était parfaite.

---

## 5. Réserves

1. **L'état ouvert n'est pas observé à l'écran.** Le jeu de démonstration répond
   aux dix questions ; la branche « ouverte » est prouvée au niveau du moteur et
   par l'expression de rendu, pas par un pixel. Pour la voir il faudrait un
   dossier réellement incomplet.
2. **Dix moteurs muets restent** (inventaire du lot 55), dont sept servent le
   corps entier d'une route sur cinq pages différentes.
3. **La fiche Analyse compte maintenant trois disclosures imbriquées.** Cinq
   blocs descriptifs vivent derrière deux à trois clics. C'est cohérent avec le
   principe « l'expertise à la demande ne concurrence pas le verdict », mais
   c'est une question de conception qui mérite d'être posée à un humain : la
   revue adversariale mérite-t-elle d'être si profonde ?
4. **Un seul titre, une seule largeur** pour la vérification au pixel (`ACN`,
   1440 px, mode démonstration).
