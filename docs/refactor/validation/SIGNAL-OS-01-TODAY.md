# SIGNAL OS · LOT 01 — AUJOURD'HUI

Branche : `agent/vertex-signal-os-v1` · SW v207 → **v208** · Suite **3051 passed**

---

## 1. Le point de départ

Sur la capture du lot Shell, la première tuile KPI de l'accueil disait :

```
Régime
UNKNOWN  (0%)
voir →
```

Trois choses fausses en quatre lignes.

### (1) `(0%)` était fabriqué

`const conf = Math.round((reg.confidence || 0) * 100)`, et le libellé
concaténait `(conf + '%')` **sans condition**. Une confiance **absente** devenait
« 0% », indiscernable d'un zéro mesuré.

C'est **exactement** le défaut corrigé au lot 629 dans l'objet Regime Aura, à un
**second site d'appel**. Le 629 avait corrigé `loadRegime` et laissé
`loadSummary` : la même page portait le correctif **et** le défaut.

### (2) `UNKNOWN` était présenté comme un nom de régime

Le moteur ne rend pas une valeur vide quand il ne tranche pas : il rend la
**chaîne `'UNKNOWN'`**. La tuile l'affichait telle quelle, à la place où elle
affiche `TREND` ou `RISK-OFF`.

### (3) `voir →` occupait le troisième étage des quatre tuiles

`VISUAL_SYSTEM.md` donne la forme d'un KPI : `label → valeur → delta/contexte`.
Les quatre tuiles portaient la **même phrase**, qui ne disait rien que la tuile
ne dise déjà — elle est un lien en entier. `COPY.md` range `View more` dans les
libellés à éviter.

### Et un troisième site, côté serveur

`vertex/market/daily_brief.py:142` produisait
`'Régime UNKNOWN — risque neuf bloqué'` — la sentinelle interne en majuscules et
en anglais, dans **la phrase la plus lue de Vertex**, en tête de l'accueil.

**La condition était juste ; c'est le libellé qui fuyait.** Aucune règle n'a
changé : même test, même branche, même conclusion. Seul le mot change.

---

## 2. Audit — décisions

| Élément | Décision | Motif |
| --- | --- | --- |
| Tuile Régime | **REWRITE** | zéro fabriqué + sentinelle affichée |
| 3ᵉ étage des 4 tuiles | **REDESIGN** | `voir →` × 4 → contexte réel |
| `kpiTile` (styles en ligne) | **REWRITE** | 3 déclarations statiques → CSS |
| `<details>` catalyseurs + portefeuille | **DELETE** | rangs 4 et 5 de `PAGES.md` |
| Titres des cartes | **REWRITE** | libellés canoniques `COPY.md`, à la source |
| Message d'erreur du brief | **REWRITE** | `e.message` brut exposé |
| Hero, Régime, Ce qui a changé, Alertes | **KEEP** | conformes |

---

## 3. Le repli qui cachait un catalyseur à J-3

Catalyseurs et portefeuille étaient dans un `<details>` **fermé** (décision du
lot 621, « reléguer le contexte profond »). `PAGES.md` les classe **4ᵉ et 5ᵉ**
des six rangs de cette page.

**Mesuré sur le serveur** : le premier catalyseur est **MMM à J-3**, et la piste
conclut « ▸ MMM dans 3 j — risque événementiel imminent ». Un catalyseur à J-3
qu'il faut déplier pour voir ne remplit pas son office : il existe précisément
pour prévenir **avant**.

Ce qui est **conservé** du 621, et qui était sa vraie trouvaille : une seule
visualisation de régime sur la page, et l'ordre décision → régime →
opportunités → surveillance.

---

## 4. Micro-copy écrite à la source

Sept entrées retirées de la table de réécriture de `signal-os.js`. Les titres
suivent `COPY.md` : **Signal du jour**, **Top opportunités**, **Catalyseurs**.

**Mesuré au navigateur : `[data-signal-copy]` = 0.** Plus un seul libellé
d'Aujourd'hui n'est réécrit après coup — le serveur et l'écran disent la même
chose.

*Choix assumé* : « Alertes prioritaires » est **conservé** plutôt que réduit à
« Alertes » comme le proposait la table. Le mot « prioritaires » porte une
information (elles sont triées) ; le raccourcir n'aurait servi que la symétrie.

---

## 5. Mesures navigateur

Serveur dont le code servi est **vérifié** (`/sw.js` → `td-shell-v208`,
`/api/briefing/editorial` → `main_risk: "Régime indéterminé — risque neuf bloqué"`).

| tuile | valeur | contexte |
| --- | --- | --- |
| Régime | `Indéterminé` | `Vertex ne tranche pas` |
| Breadth >MM200 | `45 %` | `participation étroite` |
| VIX | `12.7` | `calme` |
| Meilleure opp. | `ACN` | `ACHETER` |

Les quatre contextes viennent de données réelles : la bande `calme` est le
`vix_band` du serveur, `ACHETER` le verdict du comité.

| | 1440 px | 390 px |
| --- | --- | --- |
| libellés réécrits en JS | **0** | **0** |
| `<details>` | **0** | **0** |
| défilement horizontal de page | non | non |
| débordements réels | **0** | **0** |
| erreurs console | **0** | **0** |
| lignes de contexte alignées | 4 à y=491 | 2 + 2 (512 / 628) |

Ordre vertical mesuré : hero 284 → régime 679 → opportunités/alertes 1016 →
catalyseurs 1202 → portefeuille 1261. Conforme à la hiérarchie cible.

### Un faux négatif de mon banc, vérifié avant conclusion

La sonde annonçait `calendrier rendu: False`. **Faux** : le sélecteur cherchait
`.vx-chart-card, .vx-card` alors que `catalystRunway` rend `.vx-chart-head` sans
carte enveloppante. Vérification directe : hôte de **281 px**, six événements
réels (MMM J-3, ACN J-5, ARE J-7, ALB J-7, NFP J-20, CPI J-29). Le widget
fonctionne ; c'est la sonde qui regardait à côté.

---

## 6. Gardiens

`tests/test_signal_os_today.py` — **7 tests**. Les commentaires sont retirés
avant analyse : l'explication d'un retrait citait le défaut retiré (même famille
que 616-B).

| mutation | résultat |
| --- | --- |
| repli `\|\|0` revenu | 1 échec |
| `UNKNOWN` affiché tel quel | 1 échec |
| `voir →` revenu | 1 échec |
| contexte VIX retiré | 1 échec |
| style en ligne revenu | 1 échec |
| règle CSS retirée | 1 échec |

`test_total_rebuild_today_markets_lot621` : renversement documenté, ordre des six
ancres vérifié. `test_audit_lot66` **a mordu pendant le lot** — j'avais déplacé
`>MM200` du label vers le contexte ; le label doit nommer la métrique, sinon
« 45 % » ne dit pas 45 % de quoi. Restauré.

---

## 7. Dette

- Table de réécriture : **35 entrées** restantes (7 pages).
- `MutationObserver` sur `#vx-content` : coût **toujours pas mesuré**.
- Le seuil de participation `>= 55` est dans l'UI (couleur **et** texte, une
  seule écriture désormais). Il duplique une règle serveur — à faire descendre
  côté moteur un jour, hors périmètre visuel.
- `/markets` à 390 px : 2 éléments coupés (~40 px), reporté depuis le lot Shell.

---

## 8. Suite

Lot **02 — Marchés**, avec le débordement 390 px à corriger en premier.
