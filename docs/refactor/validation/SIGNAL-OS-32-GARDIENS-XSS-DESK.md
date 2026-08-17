# SIGNAL OS · LOT 32 — LES DEUX GARDIENS LES PLUS COÛTEUX, ÉPROUVÉS PAR MUTATION

Branche : `agent/vertex-signal-os-v1` · SW **v233 inchangé** (aucun octet servi
modifié) · Suite **3159 → 3168 passed**

Le lot 31 a prouvé qu'un gardien critique peut avoir des trous : celui de
READONLY en avait deux. Même discipline ici, sur les deux invariants les plus
coûteux qui restaient — la **sortie XSS** (sécurité) et les **clés de sync desk**
(perte de données).

---

## 1. Les clés de sync desk : 6 mutations, 6 morsures

| mutation | verdict |
| --- | --- |
| `vxAlerts` retirée du repli servi de `/system` | mord |
| `vxJournal` retirée du repli servi de `/system` | mord |
| clé fantôme ajoutée au repli | mord |
| `vxAlerts` retirée de `vx-entities.js` | mord |
| clé renommée dans `vx-entities.js` (`myFavs` → `myFavsX`) | mord |
| clé fantôme ajoutée à `vx-entities.js` | mord |

Le gardien du lot 381 tient. Rien à corriger — c'est un résultat, pas une
absence de résultat.

---

## 2. La sortie XSS : 18 mutations, 12 morsures

Six mutations passent le gardien **nommé** (`test_xss_exits_lot177.py`) :

| mutation | gardien nommé | suite complète |
| --- | --- | --- |
| `&` non échappé | survit | mord (lot 102) |
| `<` non échappé | survit | mord (lot 102) |
| `'` non échappée | survit | mord (lot 102) |
| champ `sym` non assaini | survit | mord (lot 102) |
| **champ `time` non assaini** | survit | **SURVIT** |
| **champ `why` non assaini** | survit | **SURVIT** |

Les quatre premières sont une **division du travail légitime** : le lot 177 garde
les *routes*, le lot 102 garde la *fonction*. Les deux dernières ne sont gardées
nulle part — elles passent les 3 159 tests.

`time` compte : `/news-feed` le sert et le fil live l'injecte en innerHTML
(`terminal.py::renderFeed`). Il n'est pas moins externe que le titre. `why`, lui,
n'existe sur **aucun** item de news du dépôt — c'est une défense pour un champ
qui n'arrive jamais. Les deux sont désormais tenus par le contrat de la
fonction (`test_news_plus_lot102.py`), et `time` en plus par la route.

---

## 3. Ce que la question « pourquoi ça ne mord pas ? » a trouvé de plus grave

`news_state['items']` est **brut** — la boucle d'actualités y dépose les titres
yfinance/RSS tels quels, chaque sortie neutralisant pour son compte. Le gardien
du lot 177 en nomme trois. Il y en a **quatre**.

```
/api/briefing/editorial
  → daily_brief.build_daily_brief  (via news_pipeline.collect)
  → editorial.build_narrative      (lit news_state directement)
```

Mesuré, charge injectée dans `news_state` :

```
.editorial.narrative      À la une : <script>alert(1)</script>Résultats…
.daily.what_changed[0]    <img src=x onerror=alert(2)> (<b>Pub</b>)
.daily.compact[3]         Actualité dominante : <img src=x onerror=…
.daily.sections[3].text   <img src=x onerror=alert(2)> (<b>Pub</b>, …)
.what_changed_today[0]    <img src=x onerror=alert(2)> (<b>Pub</b>)
```

**Il n'y avait pas de XSS exploitable** — et il faut le dire ainsi. Aucun de ces
champs n'est rendu ; les deux seuls consommés (`sources` et `main_risk`, dans
`briefing.py`) passent par `esc()`. Ce qu'il y avait : une charge vivante à un
pas d'un rendu, et rien — ni test, ni documentation — pour dire que ce pas était
interdit.

Le code affirmait même l'inverse de la mesure. `editorial.py` étiquetait sa
source « actualités (**fil assaini**) » et l'en-tête de `news_pipeline` parlait
du fil « déjà collecté et **assaini** ». Deux commentaires devenus vrais avec ce
lot, et faux depuis leur écriture.

---

## 4. Pourquoi retirer le BALISAGE et non appeler `sanitize_news`

Le réflexe — « c'est une sortie de news, donc `sanitize_news` » — aurait été un
défaut visible à l'écran. Cette sortie appartient à la **seconde famille** de la
règle n°5 : son rendu échappe déjà. Un assainissement serveur en plus donnerait,
sur des titres parfaitement légitimes :

| titre réel | avec `sanitize_news` + `esc()` | avec `strip_markup` + `esc()` |
| --- | --- | --- |
| `AT&T` | `AT&amp;T` | `AT&T` |
| `Barron's` | `Barron&#39;s` | `Barron's` |
| `P/E < 10` | `P/E &lt; 10` | `P/E < 10` |

D'où `news_plus.strip_markup()` : retire le balisage, ne touche pas aux
méta-caractères. Le balisage, lui, ne survit à **aucun** rendu — échappé ou non —
il n'a donc aucune raison de traverser le serveur.

Le test `…n_echappe_pas_le_texte_legitime` **interdit** la « correction » par
`sanitize_news` : la mutation C8 l'applique et le gardien mord.

---

## 5. Ce que le lot change dans le code

| fichier | changement |
| --- | --- |
| `vertex/services/news_plus.py` | `strip_markup()` + `safe_link()` (extraite de `sanitize_news`, comportement identique) |
| `vertex/market/news_pipeline.py` | titre / traduction / éditeur / heure démarqués ; lien filtré http(s) ; titre entièrement fait de balisage **rejeté et compté** |
| `vertex/market/editorial.py` | le titre « À la une » est démarqué avant composition |
| `CLAUDE.md` | règle n°5 : le fil est **brut**, et la quatrième sortie est nommée |

Aucun moteur, aucune règle métier, aucun octet servi (`/static`, shell HTML)
touché — **donc pas de bump SW**, et le gardien d'empreinte du lot 361 le
confirme.

---

## 6. Gardiens — 12 mutations sur 12 tuées

`tests/test_signal_os_sortie_editoriale_lot32.py` (7 tests) :

| mutation | résultat |
| --- | --- |
| narratif : balisage non retiré | mord |
| pipeline : titre non nettoyé | mord |
| pipeline : traduction non nettoyée | mord |
| pipeline : éditeur non nettoyé | mord |
| pipeline : lien non filtré | mord |
| pipeline : titre vide non rejeté | mord |
| `strip_markup` devient l'identité | mord |
| **`strip_markup` échappe AUSSI (double échappement)** | mord |
| rendu : `sources` non échappées | mord |
| rendu : `decision` non échappée | mord |

Plus, sur la **suite complète**, les deux trous du lot 177 :

| mutation | avant le lot | après |
| --- | --- | --- |
| champ `time` non assaini | survit (3 159 tests) | mord |
| champ `why` non assaini | survit (3 159 tests) | mord |

---

## 7. Réserves honnêtes

1. Le gardien statique du lot 177 compte les appels à `sanitize_news`
   (`n >= 6`). Il détecte qu'on en **retire** un ; il ne peut pas détecter une
   **nouvelle** sortie qui oublierait d'en appeler un. C'est exactement le défaut
   par lequel `/api/briefing/editorial` est passée — et l'énumération reste
   manuelle après ce lot.
2. `strip_markup` retire les balises **fermées** (`<[^>]*>`). Une balise jamais
   fermée (`<img src=x onerror=…` sans `>`) traverse — c'est assumé pour cette
   famille : son rendu échappe, et échapper au serveur coûterait les titres
   légitimes du tableau §4. La propriété qui protège cette famille reste le
   `esc()` au rendu ; le lot l'ancre par un test.
3. La mesure est faite au client de test Flask, pas au navigateur : ce lot ne
   touche à aucun octet servi, il n'y avait pas de rendu à observer.
