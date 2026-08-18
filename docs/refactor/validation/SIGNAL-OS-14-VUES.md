# SIGNAL OS · LOT 14 — TROIS DE MES INSTRUMENTS VISITAIENT DES URL INVENTÉES

Branche : `agent/vertex-signal-os-v1` · SW v220 → **v221** · Suite **3106 passed**

Ce lot devait auditer Opportunités rang par rang. Il a commencé par découvrir
que **je mesurais depuis cinq lots des pages qui n'existent pas**.

---

## 1. Les URL fabriquées

En lisant les vues **déclarées dans la source** et en les comparant à celles que
mes relevés visitaient :

| relevé | URL utilisée | existe ? |
| --- | --- | --- |
| Opportunités | `?view=shortlist`, `?view=compare` | **non** |
| Options | `?view=gex`, `?view=vol` | **non** |

Le mécanisme qui rendait l'erreur invisible :

```python
view = view if view in dict(_VIEWS) else 'radar'
```

Une vue inconnue **ne produit ni 404 ni erreur** — juste une autre page. Mes
relevés mesuraient donc la **même page plusieurs fois** en croyant en couvrir
plusieurs, et ne visitaient **jamais** `stocks`, `anomalies`, `calendar`,
`positioning`, ni les trois vues héritées d'Options.

**Troisième fois** qu'une URL fabriquée me trompe : au lot 08 j'avais inventé
l'onglet `engines` de Système, puis pris son repli pour un doublon.

### Vues réelles — lues dans la source

| espace | vues déclarées |
| --- | --- |
| `/markets` | overview · macro · sectors · breadth · volatility |
| `/opportunities` | radar · **stocks** · options · **anomalies** · **calendar** |
| `/portfolio` | team · positions · performance · risk · options · watchlist |
| `/options` | structure · **positioning** · leaps · positions · volatility · events *(+3 héritées hors barre d'onglets)* |
| `/journal` | overview · journal · learnings · progression · track-record |
| `/system` | connections · data · automations · settings · archive |

---

## 2. Ce que ça change au lot 12

« **12 graphiques rendus** » était faux. Sur les vues réellement déclarées il y
en a **quatorze**, et deux de mes douze étaient le **même graphique compté trois
fois**.

La **conclusion tient** — 0 graphique sans question ni conclusion — et elle tient
désormais sur un échantillon correct et plus grand. C'est le décompte publié qui
était erroné, pas le verdict.

---

## 3. Un angle mort systématique dans le même relevé

Mon relevé de structure cherchait `.vx-card-title` et `h2`. Or le Chart Shell
émet `<h3 class="vx-chart-title">`.

**Il a donc manqué tous les titres de graphiques**, dans *tous* mes audits de
structure — Marchés, Journal, Opportunités. Corrigé.

---

## 4. Quatrième fausse accusation, évitée

Avec le relevé corrigé, les vues `anomalies` et `calendar` semblaient **ne rien
rendre du tout**. Mesure directe avant d'écrire quoi que ce soit : **879 px** et
**1627 px** de contenu. Ce n'étaient pas deux vues vides, c'était mon sélecteur.

---

## 5. Mais le vrai défaut était dessous

La vue **Anomalies** — rang 5 de `PAGES.md` §3 — sert 879 px de contenu et
**aucun titre**. Son seul intitulé était un `<b>` nu, là où les **25 autres
vues** du produit ouvrent sur un titre.

C'est précisément pour ça que mon relevé n'y trouvait rien : il n'y avait
effectivement rien à trouver de la grammaire d'en-tête commune. Corrigé —
`<h2>` + `.vx-sub`, comme partout ailleurs.

---

## 6. Opportunités — rangs de `PAGES.md` §3

| rang | état |
| --- | --- |
| 1. Filtres principaux | couvert — barre de filtres (`radar`, `stocks`) |
| 2. Top S+/S | couvert — « Priorités » + badges de rang |
| 3. Tableau / scanner complet | couvert — `stocks` « Dossiers à étudier » |
| 4. Catalyseurs | couvert — `calendar` « Calendrier des catalyseurs » |
| 5. Anomalies / nouveaux signaux | couvert — `anomalies`, **titre ajouté ici** |

Les cinq rangs sont matérialisés, un par vue. Aucun n'était absent ; l'un
n'était pas *présentable*.

---

## 7. L'instrument livré au lot 13 portait la même liste fabriquée

`tools/mesurer_rognage_silencieux.py` **dérive désormais ses vues de la
source**. Une liste écrite à la main dans un outil ne peut pas savoir qu'elle est
périmée — c'est exactement la nature du défaut qu'elle cause.

---

## 8. Le gardien m'a repris une fois de plus

Ma première version de `test_une_vue_inconnue_retombe_sur_un_defaut_silencieux`
exigeait **une seule forme d'écriture** du repli (`view = view if …`) et
accusait Marchés à tort, qui l'écrit `if view not in dict(…)` sur deux lignes.

> Un gardien qui impose une forme d'écriture n'a rien mesuré : il a exigé un
> style.

Gardien `tests/test_signal_os_vues_declarees_lot14.py` — 4 tests, **7 mutations
sur 7 tuées** (vue ajoutée, vue retirée, repli supprimé, titre reperdu,
orientation reperdue, liste redevenue littérale, nom fabriqué réintroduit).

---

## 9. Dette

- Portefeuille (6 vues) et Options (6+3 vues) : rangs non audités — et cette
  fois avec les **bonnes** URL.
- Rang 3 du Journal (grade / setup / horizon), win/loss par bucket.
- 5 modules UI morts : mesure faite au lot 13, suppression à instruire.
- `chart-theme-obsidian-copper.js` : nom qui ment.
- Étiquetage démo : figé en caractérisation (lot 08).
