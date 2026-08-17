# SIGNAL OS · LOT 35 — LE CHIFFRE FAUX QUI NE SE DIT PAS

Branche : `agent/vertex-signal-os-v1` · SW **v233 inchangé** · Suite
**3178 → 3187 passed**

Le lot 29 avait éprouvé les pannes **globales** et conclu par une réserve. Le
lot 30 avait construit l'outil, mesuré 0 fuite et 0 erreur, puis **refusé de
conclure** sur la question centrale — trois méthodes essayées, trois familles de
faux positifs — et l'avait écrite dans l'en-tête de son propre outil :

> « Conclure "propre" sur cette question serait affirmer plus que ce que la
> mesure permet. Elle reste ouverte. »

Ce lot la ferme. La question : **sous panne partielle, un chiffre calculé sans
la source manquante peut-il s'afficher entre des chiffres justes, sans qu'aucun
état d'erreur n'apparaisse ?**

---

## 1. Le résultat mesuré

Course complète, méthode encadrée, serveur de démonstration à SW v233 :

| | |
| --- | --- |
| vues | **33** |
| cellules chiffrées / stables | **546 / 546** |
| sources éprouvées en panne isolée | **10** |
| fuites techniques (`NaN`, `undefined`…) | **0** |
| erreurs de page | **0** |
| **chiffres faux silencieux** | **0** |
| libellés de **durée** modifiés (comptés à part) | **4**, sur une seule vue |
| témoin | **concluant** |

**Ce que « 0 » veut dire ici :** aucune cellule portant une **valeur** — un
pourcentage, un prix, un compte, un score — ne change en silence quand une
source tombe. Ce qui reste tient en quatre libellés d'**âge** sur
`/system?view=automations` (« Il y a 51 min » → « 52 min », « dans ~1 min » →
« ~0 min »). Ils sont identiques dans les trois relevés sains et différents sous
panne : la panne change donc bien la durée affichée — vraisemblablement
l'horodatage de repli employé. Une durée plus ancienne n'est pas un chiffre
inventé, mais **la cause reste à expliquer**, et l'outil l'affiche à chaque
exécution au lieu de la ranger dans un total rassurant.

---

## 2. Ce qui a débloqué une mesure restée ouverte deux lots

### 2.1 La clé — chemin DOM, pas classe

`e.className` vaut `[object SVGAnimatedString]` pour **tout** texte SVG : la clé
du lot 30 versait des valeurs sans rapport dans le même seau, et glissait dès
qu'un élément apparaissait. Le chemin DOM désigne une cellule et une seule.

| clé | cellules stables |
| --- | --- |
| `className` + longueur (lot 30) | 637 / 1768 |
| chemin DOM (ce lot) | **546 / 546** |

Passer de 36 % à 100 % de cellules exploitables, c'est ce qui rend la
comparaison possible : toute variation devient du signal.

### 2.2 La référence — la mesure doit être **encadrée**, pas seulement précédée

C'est le point qui compte, et il m'a fallu **deux** erreurs pour l'atteindre.

**Première erreur.** Une référence globale unique, puis dix sources éprouvées.
Vingt minutes plus tard, « Il y a 5 min » était devenu « Il y a 8 min » et
l'outil accusait **quinze chiffres** sur `/api/desk`. C'était l'horloge.
Correction : deux relevés de référence, séparés du **même délai** que celui qui
précède la mesure — une cellule qui suit le temps se démasque entre les deux.

**Seconde erreur — et j'avais déjà écrit « 0 » dans ce rapport.** La course
complète, avec cette correction, a rendu **4** cellules sur
`/system?view=automations` : « Il y a 25 min » → « 26 min », « Il y a 26 s » →
« 32 s », « dans ~1 min » → « ~0 min ». Encore l'horloge. Deux relevés espacés
de 2,4 s ne voient pas bouger un libellé à la minute : il ne tique qu'une fois
par minute, et il peut tomber pile pendant la mesure.

**Troisième forme : encadrer.** Deux références AVANT, un contrôle APRÈS, tous
sans panne ; une cellule n'est jugée que si elle est identique dans les **trois**.
On demande à la cellule si elle bouge **aussi quand rien n'est cassé** — aucune
liste de formats de durée, et le lot 33 a montré ce que valent les listes de noms.

**Et il reste quatre cas.** Ils passent l'encadrement : identiques dans les trois
relevés sains, différents sous panne. Ce ne sont donc **pas** des faux positifs
d'horloge — la panne change réellement la durée affichée. Mais ce sont des
**durées**, et une durée plus ancienne n'est pas un chiffre inventé.

À ce stade j'ai arrêté d'itérer sur l'instrument, et je lui ai fait **dire** la
distinction au lieu de la masquer : les durées sont comptées à part **et
affichées à chaque exécution**. Un total qui les aurait absorbées aurait fait
dire à l'outil autre chose que ce qu'il mesure ; un filtre qui les aurait tues
aurait caché un comportement réel que je n'explique pas encore.

> Le résultat de ce lot n'est donc pas « le produit est propre » obtenu du
> premier coup : c'est un chiffre que mon instrument a annoncé faux **deux fois**
> avant que la méthode ne soit juste, et dont la dernière part n'est pas classée
> comme propre mais comme **non expliquée**.

### 2.3 Le détecteur — tout chiffre qui change, pas seulement les zéros

Le lot 30 ne cherchait qu'un « 0 » substitué. Une moyenne sur cinq sources au
lieu de six est plausible **et** fausse — c'est même la forme la plus
dangereuse, celle qui ne se remarque pas.

---

## 3. Le témoin, sans lequel un « 0 » ne prouve rien

Un balayage qui ne trouve rien peut vouloir dire deux choses : le produit est
honnête, ou l'instrument est aveugle. On tranche en **fabriquant** le défaut —
la source répond `200` avec un corps **valide mais altéré**, si bien que la vue
n'a aucune raison d'afficher une erreur.

Mesuré sur `/` avec `/api/market/summary` altérée :

```
« 45 % »  ->  « 3 % »        (breadth)
« 12.7 »  ->  « 20.47 »      (VIX)
la vue signale quelque chose : false
```

L'instrument voit les deux. Son « 0 » sur les pannes réelles n'est donc pas un
aveuglement. L'outil porte ce témoin lui-même et **rend un code distinct s'il ne
voit rien** : il refuse de conclure plutôt que de rassurer à tort.

Ce que le témoin dit aussi, et qu'il faut énoncer : si une source **ment** —
répond bien, avec de mauvais chiffres — Vertex les affiche comme réels. Ce n'est
pas un défaut du produit, c'est la limite de tout terminal : il ne peut pas
détecter une source amont qui ment. La revendication de ce lot est étroite et
exacte : **sous panne, aucun chiffre inventé**.

---

## 4. Ce que le lot livre

| fichier | rôle |
| --- | --- |
| `tools/mesurer_panne_partielle.py` | réécrit : clé DOM, double référence immédiate, détecteur généralisé, témoin intégré |
| `tests/test_signal_os_chiffre_silencieux_lot35.py` | garde la **logique** de détection (9 tests, sans navigateur) |

Le balayage complet (33 vues × 10 sources, ~10 min) reste un outil : sa place
n'est pas dans une suite de 40 secondes. Le gardien tient ce qui peut l'être
sans navigateur — la logique de `_silencieux`, et les trois propriétés de
méthode payées par un faux positif.

Aucun moteur, aucune règle métier, aucun octet servi touché — **pas de bump SW**.

---

## 5. Réserves honnêtes

1. **Jeu de démonstration.** Certaines sources n'apportent qu'une ou deux vues
   (`/api/command`, `/cal-feed`) : leur panne a peu de surface pour mentir. La
   couverture est solide sur `/scan` (10 vues), `/api/pos-quotes` (7) et
   `/api/desk` (33), plus faible ailleurs.
2. **Une source à la fois.** Deux sources tombant ensemble sont un troisième
   régime, non mesuré.
3. **Cellules visibles seulement.** Un chiffre faux dans un graphique SVG sans
   texte, ou derrière un `<details>` fermé, n'est pas vu.
4. Le témoin altère **une** source (`/api/market/summary`). Il prouve que
   l'instrument peut voir ; il ne prouve pas qu'il verrait toute forme de
   fausseté sur toute source.
5. **Les quatre durées de `/system?view=automations` ne sont pas expliquées.**
   Elles ne sont pas un artefact de mesure — l'encadrement les laisse passer.
   La panne de `/api/desk` change la durée affichée ; je n'ai pas identifié
   quel horodatage de repli le fait, et je ne l'ai pas cherché plus loin dans ce
   lot. C'est la réserve la plus concrète qu'il laisse ouverte.

---

## 7. Deux fautes de validation, corrigées ici

Elles n'ont rien à voir avec le sujet du lot, et elles ont coûté deux CI rouges.

1. **Le gardien `test_strategy_os_final_guards` scanne `git ls-files`** — donc
   les fichiers **suivis**. J'avais lancé la suite avant de stager : mon outil du
   lot 34 était invisible, la suite passait, et le gardien s'est déclenché au
   commit. Désormais : stager, puis valider.
2. **L'outil importait Playwright au chargement.** La CI n'a pas de navigateur :
   la **collecte de toute la suite** échouait, et mon poste — qui a Playwright —
   ne pouvait pas le montrer. L'import est passé dans `main()`, un gardien tient
   la règle pour les trois outils que les tests importent, et **je rejoue
   désormais la suite avec Playwright rendu inimportable** pour éprouver le
   même environnement que la CI, pas un plus riche.
