# SIGNAL OS · LOT 18 — L'ÉTIQUETAGE DÉMO, INSTRUIT

Branche : `agent/vertex-signal-os-v1` · SW v223 → **v224** · Suite **3104 passed**

Le lot 08 avait **figé un constat plutôt que de corriger au jugé**. Il refusait
d'étiqueter avant d'avoir établi quelle donnée est réellement synthétique, et
notait une pièce qui ne collait pas : `/api/market/summary` répondait
`source: "cloud"` alors que `DEMO=1`.

**Cette pièce cachait un défaut d'honnêteté, pas une bizarrerie.**

---

## 1. Deux endpoints, deux vérités sur la même donnée

| endpoint | disait | sert |
| --- | --- | --- |
| `/scan` | `source: 'demo'` | données synthétiques |
| `/api/market/summary` | **`source: 'cloud'`** | **les mêmes**, dérivées du scan |

### La cause

```python
'source': 'ibkr' if IBKR_ENABLED else 'cloud'     # feeds.py:43
```

Un **binaire** — alors qu'il y a **trois** états. Sans `DEMO_MODE` dans
l'expression, la donnée synthétique tombe forcément dans l'une des deux cases
**réelles**. En démo, l'endpoint annonçait « cloud », c'est-à-dire de la donnée
de marché réelle, pour des chiffres fabriqués.

C'est l'**invariant produit n°4 pris à revers** : « jamais de chiffre inventé
affiché comme réel ».

### Ce qui rend l'erreur instructive

Le bon calcul **existait déjà, à côté** : `status_service.py` fait le trois-états
depuis toujours. Ce site-ci ne l'avait pas suivi. Un gardien vérifie désormais
que les deux restent d'accord — deux réponses divergentes sur le mode réel,
c'est le défaut du lot 08 réinstallé ailleurs.

---

## 2. Le trou d'Options, comblé

`options_intel_page.py` déclare `<div id="vx-demo-banner">` et **rien** ne le
remplissait — « le signe le plus net » du constat, disait le lot 08.

Chaque carte de l'espace savait pourtant qu'elle était en démo : `d.demo`
traverse le hero, les compteurs, le scanner, le payoff. **Seul l'espace se
taisait.** Il porte désormais le même libellé que Marchés et Opportunités — un
seul fait, un seul libellé.

---

## 3. Ce qui reste muet, et c'est voulu

`/analysis` (accueil) et `/journal` n'affichent **aucune donnée de moteur** :
ils lisent le bureau du navigateur, données **personnelles**. Un bandeau
« démo » y serait un mensonge d'un autre genre.

### Une précision que la mesure a apportée

Le Journal affiche bien « DÉMO » — mais dans **deux badges de carte**, pas dans
un bandeau de page, et sur la moitié **moteur** de l'historique (« Moteur ·
verdicts théoriques »), jamais sur la moitié déclarée.

**C'est plus juste qu'un bandeau de page** : l'étiquette est posée là où la
donnée est synthétique, et absente là où elle est personnelle. La règle « une
donnée = une provenance » appliquée à l'intérieur d'une même vue.

---

## 4. Mesures — serveur `td-shell-v224` vérifié avant lecture

`/api/market/summary` → **`"source":"demo"`**.

| espace | étiquette démo visible | nature |
| --- | --- | --- |
| `/` · `/markets` · `/opportunities` | **oui** | bandeau de page |
| `/portfolio` · `/system` | **oui** | badge posé à l'exécution |
| `/options` | **oui** | **corrigé ici** |
| `/journal` | **oui, au niveau carte** | moitié moteur seulement |
| `/analysis` | **non** | données personnelles — voulu |

**0 erreur de page.**

---

## 5. Le gardien remplace la caractérisation

`tests/test_signal_os_demo_visible_lot08.py` — qui ne validait rien et portait
sa propre date de péremption — est **supprimé**, remplacé par
`tests/test_signal_os_demo_lot18.py` : 5 tests, **8 mutations sur 8 tuées**.

Son test le plus important est le **contre-exemple** : il vérifie que la
correction **ne s'étend pas** à `/analysis` et `/journal`. Poser un hôte démo
sur des données personnelles est exactement l'erreur symétrique de celle qu'on
vient de corriger.

### Une portée trop large, la neuvième

`'remplirBandeauDemo' in js` restait vert après un renommage en
`remplirBandeauDemoX` — la chaîne cherchée en est un **préfixe**. Même piège
qu'au lot 13 avec `td.vx-truncate`. Resserré sur `function remplirBandeauDemo(`
**et** sur ses deux sites d'appel.

---

## 6. Dette restante

- Rang 3 du Journal (grade / setup / horizon) et win/loss par bucket — à
  instruire avant de construire, comme celui-ci l'a été.
- Fiche `/analysis/<ticker>` inaccessible dans cet environnement.
