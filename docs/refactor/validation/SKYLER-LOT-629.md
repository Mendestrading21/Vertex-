# SKYLER LOT 629 — Regime Aura : le refus portait sur le dessin, les défauts étaient réels

Date : 2026-08-14 · Branche : `agent/regime-aura-629` (base : `origin/main`)
Service worker : v205 → **v206**

Point de départ : une capture d'écran et une phrase — « je n'aime pas ce
graphique ». La carte RÉGIME de l'accueil montrait une jauge complète, repère à
zéro, arc corail, « 0 % confiance », et la ligne
« ▸ Risque neuf BLOQUÉ · Régime UNKNOWN — risque neuf bloqué ».

Le refus était esthétique. En le regardant de près, trois choses qui n'ont rien
d'esthétique sont sorties.

---

## 1. Ce qui n'allait pas

### (a) Un garde d'honnêteté qui ne s'est jamais déclenché

`regime-aura.js` portait depuis sa création :

```js
if (o.state === 'empty' || !o.regime) { …état vide honnête… }
```

Le moteur ne rend pas une valeur vide quand il ne tranche pas. Il rend la
**chaîne `'UNKNOWN'`** — vérifié sur le serveur de ce lot :

```json
{"regime":"UNKNOWN","confidence":0.0,
 "notes":["moins de 3 dimensions disponibles — régime inconnu (honnête)"]}
```

`'UNKNOWN'` est *truthy*. Le garde était décoratif. Le moteur, lui, était
parfaitement honnête — il le dit même dans ses `notes`. **C'est l'affichage qui
transformait son aveu en lecture.**

### (b) Un chiffre inventé, produit par un `||`

Site d'appel, `briefing.py` :

```js
confidence: Math.round(((r && r.confidence) || 0) * 100)
```

Une confiance **absente** devenait `0`, affichée « 0 % confiance ». Rien ne la
distinguait d'un zéro mesuré. La règle « données réelles uniquement » prise à
revers par une commodité d'écriture.

### (c) La couleur du risque réel pour une indétermination

`new_risk_allowed: false` → tonalité `risk` → `--vx-negative`, que la charte
réserve à « perte / risque **RÉEL** ». Vertex peignait en rouge le fait de ne
pas savoir.

### (d) Et le dessin, qui méritait bien le refus

L'arc de confiance était **peint sur toute la course** en dégradé continu
(.18 → .95), quelle que soit la confiance. Aucune échelle n'était visible :
rien ne disait où s'arrêtait la mesure. Derrière, deux ellipses floutées **plus**
un dégradé radial plein cadre se superposaient sous le texte.

---

## 2. Ce qui a été fait

| | avant | après |
| --- | --- | --- |
| régime `UNKNOWN` | jauge complète, arc corail | **état vide honnête**, aucun tracé |
| confiance absente | « 0 % confiance » | `null` → couronne éteinte, « confiance n/d » |
| échelle | arc plein, course invisible | **30 crans**, les éteints se voient |
| fond | 2 ellipses floutées + dégradé plein cadre | **1 halo borné** + disque de lisibilité |
| verdict | « BLOQUÉ · Régime UNKNOWN — risque neuf bloqué » | fragments redondants retirés |

Règle d'allumage : **un cran est allumé quand son MILIEU est atteint** — 62 %
donnent 19 crans sur 30. Arrondi honnête, jamais un demi-cran qui suggérerait le
centième.

### Le contre-exemple qui borne le correctif

Première version du garde : `|| confidence <= 0`. **Retirée.** Un régime
`CHOP` **mesuré** avec 0 % de confiance est une lecture, pas une absence — le
faire disparaître serait exactement le même défaut, dans l'autre sens. C'est la
couronne éteinte qui le dit. Un gardien tient ce cas
(`test_une_confiance_nulle_mesuree_ne_fait_pas_disparaitre_le_regime`).

### Un piège mesuré en cours de route

Première couronne en `stroke-linecap:round`. Un bout rond ajoute la moitié de
l'épaisseur à chaque extrémité : 3,25 unités sur un rayon de 64, soit 2,9° de
chaque côté pour un intervalle de 7,87° et un cran dessiné de 4,88°. **Les crans
allumés (épais) se rejoignaient donc et redonnaient l'arc plein que ce lot venait
de retirer**, pendant que les crans éteints (fins) restaient séparés. Le défaut
n'existait que sur la partie allumée — la seule qu'on lit. Vu sur la capture à
1440 px, corrigé en bouts droits.

---

## 3. Preuves

**Instrument.** Les gardiens n'inspectent pas la source à la recherche d'une
chaîne (leçon du lot 615 : compter un littéral dans les octets servis n'est pas
mesurer un rendu). Ils **exécutent** `regime-aura.js` dans Node avec un DOM
minimal et lisent le HTML produit. Sans Node, deux gardiens de source subsistent.

| cas | vide | crans | éteints | repère | texte |
| --- | --- | --- | --- | --- | --- |
| `UNKNOWN`, conf 0 | **oui** | 0 | — | non | « Régime indéterminé — Vertex ne tranche pas. » |
| `TREND`, conf 62 | non | 30 | **11** | oui | « 62 % confiance » |
| `RISK-OFF`, conf `null` | non | 30 | **30** | **non** | « confiance n/d » |
| `CHOP`, conf 0 *(mesurée)* | **non** | 30 | 30 | oui | « 0 % confiance » |

**Mutation du gardien** — les cinq mutations mordent :

| mutation | résultat |
| --- | --- |
| garde revenu à `!o.regime` seul | 1 échec |
| garde élargi à `confidence <= 0` | 1 échec |
| dédoublonnage du verdict retiré | 1 échec |
| tous les crans allumés | 1 échec |
| `\|\|0` revenu au site d'appel | 1 échec |

**Navigateur** (serveur dont le code servi a été vérifié — `/sw.js` répond
`td-shell-v206`), 1440 px et 390 px, vrai CSS, vrai builder :
**0 erreur console**, aucun débordement.
La carte RÉGIME de `/` affiche désormais « Aucune donnée · Régime indéterminé —
Vertex ne tranche pas. » là où elle dessinait une jauge.

**Suite** : `3017 passed` (3009 avant, +8 gardiens du 629).

---

## 4. Ce que ce lot ne prétend pas

- Le dessin reste un choix de forme. Ce qui est **mesuré**, c'est que l'échelle
  est visible, que l'état indéterminé ne dessine plus rien, et qu'aucune
  confiance n'est fabriquée.
- Les autres objets graphiques du produit **n'ont pas été passés au même
  crible**. Le défaut trouvé ici — un garde d'honnêteté écrit contre l'absence
  de valeur, alors que le moteur rend une chaîne sentinelle — n'a aucune raison
  d'être unique. Il mérite un balayage à part entière.

---

## 5. Fichiers

- `vertex/static/vertex/js/charts/regime-aura.js` — garde, couronne, halo,
  dédoublonnage, échappement.
- `vertex/ui/pages/briefing.py` — confiance absente → `null`.
- `vertex/app/routes/system.py` — SW v206.
- `tests/test_regime_aura_lot629.py` — **nouveau**, 8 gardiens.
- `tests/test_sw_cache_scope_lot361.py` — empreinte des assets servis.
- `tests/test_replis_racine_lot385.py` — `lancer_ipad.py` déclaré hors
  production (lanceur autonome, jamais importé ; son unique `except` rend `None`
  et l'adresse manquante est **dite**, jamais remplacée).
