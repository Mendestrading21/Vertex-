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
| **tracés modifiés en silence** (géométrie SVG) | **0** |
| libellés de **durée** modifiés (comptés à part) | **0** |
| témoins (cellule **et** tracé) | **concluants** |
| code de sortie de l'outil | **0** |

**Ce que « 0 » veut dire ici :** aucune cellule portant une valeur — pourcentage,
prix, compte, score — ni même un libellé de durée ne change en silence quand une
source tombe. `/api/desk`, la source la plus exposée (33 vues), est à zéro comme
les neuf autres.

Ce verdict est le **quatrième** que l'instrument a rendu sur la même question.
Les trois premiers étaient faux, et le §2.2 dit pourquoi — c'est la partie de ce
document qui a le plus de valeur.

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

**Il restait quatre cas, et j'en ai tiré une conclusion fausse.** J'ai écrit :
« ils passent l'encadrement, donc ce ne sont pas des horloges — la panne change
réellement la durée affichée ». Deux faits l'ont démentie :

1. **La vue en cause ne lit même pas `/api/desk`** — elle lit
   `/api/system/automations`. Une panne de `/api/desk` n'a aucun chemin pour
   changer ses âges. Ce détail se trouve en lisant le code, pas le relevé.
2. **Mes deux bras n'avaient pas le même cache.** Le bras de contrôle réutilisait
   *un* contexte pour ses trois relevés : le cache client (`VX.fetch`, 15 s) lui
   rendait la **même** valeur, tandis que le bras sous panne — contexte neuf —
   refetchait. Toute valeur vivante différait donc systématiquement entre les
   bras, et l'outil l'imputait à la panne.

**Quatrième forme : le même cache des deux côtés.** Un contexte neuf par relevé,
témoin compris. La course rend alors **0 partout, durées incluses**.

> Ce n'est pas « le produit est propre » obtenu du premier coup : c'est un verdict
> que mon instrument a rendu **faux trois fois** — horloge globale, horloge à la
> minute, cache asymétrique — avant d'être juste. Les trois erreurs ont la même
> forme : **comparer deux choses qui ne sont pas comparables.**

La classification `est_duree` reste dans l'outil comme **précaution** — elle
mesure zéro aujourd'hui, et son rôle est de ne jamais laisser un total absorber
un cas de durée si la situation revenait.

### 2.3 Le détecteur — tout chiffre qui change, pas seulement les zéros

Le lot 30 ne cherchait qu'un « 0 » substitué. Une moyenne sur cinq sources au
lieu de six est plausible **et** fausse — c'est même la forme la plus
dangereuse, celle qui ne se remarque pas.

---

## 2bis. Les graphiques — l'angle mort le plus coûteux

Ce document a longtemps porté une réserve : « un chiffre faux dans un graphique
SVG sans texte n'est pas vu ». Pour un produit de graphiques, c'était l'angle
mort principal : une courbe qui perd la moitié de ses sommets ne porte **aucun
texte** qu'une cellule pourrait trahir.

La sonde relève désormais la **signature géométrique** de chaque SVG — nombre de
tracés, longueur de chaque `d`, nombre de sommets — avec la même discipline que
les cellules. Relevé : **0 tracé modifié en silence** sur les dix sources.

**Deux pièges avant d'y arriver, et c'est encore le même motif.**

1. **Détecteur sans témoin.** La première version rendait « 0 tracé » — un zéro
   sans valeur. Le témoin des *cellules* ne suffit pas : mesuré, altérer le VIX
   change deux cellules et **aucun** tracé.
2. **Témoin mal ciblé, puis altération mal ciblée.** `/opportunities?view=radar`
   ne bougeait pas ; puis une troncature limitée à `rows` ne touchait l'entrée
   d'aucune courbe. Rendue **récursive** — toute liste du corps réduite de
   moitié — elle fait passer deux aires de Marchés de **144 à 72 sommets**.

Avant de conclure, j'ai vérifié que la sonde relève réellement des graphiques :
6 sur `/`, 4 sur Marchés, 1 sur le radar. Elle n'était pas aveugle — ma cible
l'était.

**Ce que la signature ne voit pas**, et il faut le dire : elle compare une
longueur de `d` et un nombre de sommets. Une courbe dont les **valeurs**
changeraient sans changer ni sa longueur de chaîne ni son nombre de points
passerait. Le choix est délibéré — comparer les `d` au caractère près ferait
remonter des écarts sous-pixel entre deux rendus identiques, et l'instrument
crierait sans arrêt.

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
5. **Une réserve fermée, et il faut dire comment.** J'avais écrit ici que les
   quatre durées de `/system?view=automations` « ne sont pas un artefact de
   mesure ». C'était faux : c'était mon montage (§2.2, quatrième forme). Avec le
   même cache des deux côtés, elles disparaissent. La réserve est fermée par
   correction de l'instrument, **pas** par explication du produit — il n'y avait
   rien à expliquer dans le produit.
6. **Ce que le résultat ne couvre pas.** Une seule source à la fois ; jeu de
   démonstration ; témoins qui altèrent une source chacun. La réserve
   « cellules visibles seulement » est **levée pour les graphiques** (§2bis)
   mais pas au-delà : un contenu qui n'est ni texte visible ni géométrie SVG —
   un tableau replié, une valeur dans une infobulle — n'est toujours pas vu.
7. **La signature géométrique compare une longueur et un nombre de sommets.**
   Une courbe dont les valeurs changeraient sans toucher ni l'une ni l'autre
   passerait. Délibéré : comparer les `d` au caractère près ferait remonter des
   écarts sous-pixel entre deux rendus identiques.

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
