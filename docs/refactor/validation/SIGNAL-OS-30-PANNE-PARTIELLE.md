# SIGNAL OS · LOT 30 — LA PANNE PARTIELLE, ET CE QUE JE N'AI PAS PU DÉCIDER

Branche : `agent/vertex-signal-os-v1` · SW **inchangé (v233)** · Suite **3159 passed**

Le lot 29 s'était fermé sur une réserve écrite : « une panne **partielle** est
un régime différent, où un chiffre faux peut se glisser entre des chiffres
justes sans qu'aucun état d'erreur ne s'affiche ». Ce lot l'éprouve.

Aucun octet servi n'a changé : **pas de bump de service worker**.

---

## 1. Ce qui est mesuré, et sûr

D'abord la carte de **qui appelle quoi** — mesurée, pas supposée :

| source | vues qui l'appellent |
| --- | --- |
| `/scan` | 10 |
| `/api/pos-quotes` | 7 |
| `/api/options/overview` | 2 |
| `/api/market/summary` | 1 |
| `/api/command` | 1 |
| `/api/portfolio/team` | 1 |

Puis chaque source coupée seule, en ne jugeant **que les vues concernées** :

**0 fuite technique, 0 erreur de page**, sur les six.

Sans cette carte, on jugerait des vues qui n'ont rien à voir avec la source
coupée — et c'est exactement ce que faisait ma première version.

---

## 2. Ce que je n'ai PAS pu décider

La question du « chiffre faux silencieux » **n'est pas décidable** sur le jeu de
démonstration. Trois méthodes, trois familles de faux positifs, réfutées une par
une.

### Tentative 1 — comparer toutes les cellules avant/après

`e.className` vaut `[object SVGAnimatedString]` pour **tout** texte SVG : la clé
regroupait des valeurs sans aucun rapport. Résultat : « 25 zéros inventés » pour
**chaque** source, y compris celles sans lien avec les vues incriminées. Une
signature d'artefact, pas de défaut.

### Tentative 2 — clé par classe + rang de fratrie, plus un témoin de stabilité

Deux relevés identiques d'affilée, en ne gardant que les cellules stables :
**637 cellules stables sur 1 768**. Le bruit tombe, un seul candidat subsiste —
une KPI de Système passant de « 8/8 » à « 0 ».

**Réfuté en regardant l'écran** : la valeur est *identique* avec et sans panne.
La clé positionnelle glisse dès que l'ordre de rendu change et désigne une autre
cellule.

### Tentative 3 — exiger qu'une vue « signale » son manque

Plusieurs sources n'apportent **rien** en démonstration : `/api/pos-quotes` est
en POST et n'a aucune position à valoriser — ce que le lot 15 avait déjà établi.
Leur panne ne peut donc rien changer, et l'absence de signal n'y prouve rien.

---

## 3. Pourquoi je ne conclus pas « propre »

> Conclure « propre » aurait affirmé plus que ce que la mesure permet.

Le verdict de l'outil est formulé exactement comme ce qui a été mesuré —
« aucune fuite ni erreur sous panne partielle » — et pas « le produit est
propre ». Un gardien fige cette formulation.

La réserve du lot 29 est donc **partiellement** levée :

| question | statut |
| --- | --- |
| fuites techniques en régime partiel | **mesuré : aucune** |
| erreurs de page en régime partiel | **mesuré : aucune** |
| chiffre faux silencieux | **ouvert** — demande un jeu de données où chaque source apporte une valeur observable |

---

## 4. Ce que le lot livre

**`tools/mesurer_panne_partielle.py`** — la carte des dépendances et les six
pannes isolées, rejouables. Son en-tête documente **les trois faux positifs**
plutôt que de les taire : sans cela, le prochain lecteur rouvrirait la même
impasse et croirait avoir trouvé un défaut.

---

## 5. Gardien — 4 tests

| test | ce qu'il tient |
| --- | --- |
| l'instrument est conservé | l'invariant reste rejouable |
| la carte est **mesurée**, pas supposée | sans elle le verdict porte sur des vues sans rapport |
| les limites sont **écrites dans l'instrument** | le verdict ne se lira pas comme une preuve d'absence de défaut |
| le verdict ne prétend pas à l'absence de défaut | la formulation exacte est figée |

Le troisième est le plus important du lot : il garde une **honnêteté**, pas un
comportement.
