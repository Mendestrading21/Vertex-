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

## 1. Le résultat, tel qu'il est établi

| | |
| --- | --- |
| vues | **33** |
| cellules chiffrées / stables | **546 / 546** |
| sources éprouvées en panne isolée | **10** |
| 9 sources sur 10 — chiffres faux silencieux | **0** |
| `/api/desk` (33 vues) | **4 candidats, tous identifiés comme des horloges** |
| témoin | **concluant** |

Les quatre candidats de `/api/desk` sont des libellés d'âge — « Il y a 25 min »
devenu « 26 min », « dans ~1 min » devenu « ~0 min ». Ils ont été **réfutés par
mesure** : en reprenant `/api/desk` seul avec une référence prise juste avant, il
n'en restait qu'un, « Il y a 36 s » → « Il y a 41 s », l'âge qui avait avancé
pendant la mesure elle-même.

L'instrument ne pouvait pas les distinguer tout seul — c'est ce que la §2.2
corrige, et la course de confirmation avec la méthode encadrée est ce qui
autorisera à écrire « 0 » sans réserve. Tant qu'elle n'a pas rendu son verdict,
ce document écrit **ce qui est mesuré**, pas ce qui est attendu.

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

**La correction juste : encadrer.** Deux références AVANT, un contrôle APRÈS,
tous sans panne. Une cellule n'est jugée que si elle est identique dans les
**trois**. Ce qui change alors sous panne ne peut venir que de la panne.

Aucune liste de formats de durée là-dedans — ce serait encore une liste de noms,
et le lot 33 a montré ce qu'elles valent. On demande simplement à la cellule si
elle bouge **aussi quand rien n'est cassé**.

> Le résultat de ce lot n'est donc pas « le produit est propre » obtenu du
> premier coup : c'est un chiffre que mon instrument a d'abord annoncé faux,
> deux fois, avant que la méthode ne soit juste.

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
