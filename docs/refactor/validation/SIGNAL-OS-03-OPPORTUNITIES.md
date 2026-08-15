# SIGNAL OS · LOT 03 — OPPORTUNITÉS

Branche : `agent/vertex-signal-os-v1` · SW v209 → **v210** · Suite **3063 passed**

---

## 1. Ce que ce lot est, et ce qu'il n'est pas

**Un lot de micro-copy.** Il ne touche ni aux données, ni aux graphiques, ni à la
structure de la page.

La forme des cartes d'opportunité (`ticker → grade → score → verdict → asymétrie
→ catalyseur → invalidation`), l'entonnoir de sélection et l'ordre des cinq
sections étaient **déjà conformes** à `PAGES.md` — je l'ai vérifié avant de
chercher quoi refaire. Il n'y avait pas de dette structurelle à solder ici ; il y
en avait une de vocabulaire.

---

## 2. L'inventaire — titres réellement rendus, mesurés au navigateur

| avant | ce qui n'allait pas | après |
| --- | --- | --- |
| `Ce qui mérite ton attention` | une phrase d'accueil, pas un objet : le `Here is what you need to know` que `COPY.md` proscrit | **`Priorités`** |
| `Shortlist — méritent une analyse` | une shortlist **est** ce qui mérite une analyse | **`Shortlist`** |
| `Scatter d'asymétrie — qualité × timing` | « Scatter » nomme le TYPE de graphique ; on cherche un couple, pas un nuage de points | **`Qualité × timing`** |
| `Comparaison des meilleurs candidats` | trois mots pour un | **`Comparaison`** |
| `Entonnoir de sélection` | correct mais long pour un titre de carte | **`Sélection`** |
| `Les dossiers les plus utiles maintenant` | vague, et « maintenant » est vrai de toute la page | **`Dossiers à étudier`** |
| `Shortlist options — relais vers l'espace Options` | « relais vers l'espace » explique le LOGICIEL ; le lien juste dessous porte déjà l'action | **`Shortlist options`** |
| `Classement Skyler — score canonique /40` × 3 | « canonique » est du vocabulaire interne | **`Classement Skyler (/40)`** |
| sous-titre `Quelles opportunités méritent réellement une analyse ?` | question au lieu d'une orientation | **`Les dossiers qui méritent ton attention.`** |
| `Anomalies disponibles par source` | « disponibles » n'apporte rien | **`Anomalies par source`** |

`COPY.md` : « Préférer des noms d'objets ou de décisions. » Un titre **nomme** la
chose ; il n'annonce pas ce qu'elle va faire.

---

## 3. Deux messages d'erreur crachaient le jargon technique

```js
VX.states.error('Simulation moteur indisponible : ' + e.message)
VX.states.error('Chargement impossible : ' + e.message)
```

`COPY.md` : « Ne pas exposer stack trace ou jargon réseau brut. Traduire en
impact. » Remplacés par « Simulation indisponible. » et « Impossible de charger
les opportunités. »

---

## 4. Ce qui est conservé, et gardé

**Les `aria-label` longs.** « Sélection » à l'écran, `aria-label="Entonnoir de
sélection"` pour un lecteur d'écran : raccourcir un titre visible ne doit pas
appauvrir le nom accessible. C'est la simplification qu'on fait sans y penser,
donc un gardien la refuse.

**La question du graphique.** Raccourcir `Scatter d'asymétrie — qualité × timing`
en `Qualité × timing` ne doit pas emporter le `question:` qui justifie le
graphique (`CHARTS.md`). Un gardien lit le voisinage du titre pour l'exiger.

---

## 5. Mesures

**Serveur dont la version servie est vérifiée AVANT de mesurer** (`/sw.js` →
`td-shell-v210`).

| vue | titres rendus | libellés réécrits en JS | erreurs console |
| --- | --- | --- | --- |
| radar | `Priorités` · `Shortlist` · `Qualité × timing` · `Point sélectionné` · `Sélection` · `Comparaison` · `Classement Skyler (/40)` | **0** | 0 |
| stocks | `Dossiers à étudier` | **0** | 0 |
| options | `Shortlist options` | **0** | 0 |
| anomalies | — | **0** | 0 |

Balayage 8 espaces × 2 largeurs : **0 débordement réel**, 0 défilement horizontal
de page.

Tables à 390 px : les deux passent en **mode cartes** (`::before` = `"Titre"`),
défilement horizontal **0**. Le chiffre « 197 dépassements » du lot Shell
concernait des **cellules en mode cartes** dépassant le viewport — pas un
défaut, et pas une table qui force le zoom.

### Un serveur périmé, attrapé avant de conclure

Ma première série de mesures a rendu les **anciens** titres avec `réécrits: 0`.
Le nouveau serveur n'avait pas démarré (`Address already in use`) et une
instance en **v209** répondait encore. J'ai vérifié la version servie avant de
publier — c'est la seule raison pour laquelle ce rapport ne contient pas quatre
lignes fausses. La vérification de version est passée **avant** la mesure dans
la suite du lot.

---

## 6. Gardiens

`tests/test_signal_os_opportunities.py` — **6 tests**. Commentaires retirés avant
analyse.

| mutation | résultat |
| --- | --- |
| ancien titre radar revenu | 2 échecs |
| titre du scatter revenu au type de graphique | 3 échecs |
| question du scatter perdue | 1 échec |
| `aria-label` remplacé par le titre court | 1 échec |
| `e.message` revenu dans un état d'erreur | 1 échec |
| entrée revenue dans la table de réécriture | 1 échec |

Deux gardiens existants ont été **mis à jour avec leur raison**, pas contournés :
`test_opportunities_scatter_renamed` (garde désormais le titre **et** la
question, au lieu du mot « Scatter ») et
`test_options_is_a_three_contract_shortlist_and_canonical_relay` (garde la
propriété — trois contrats, relais canonique — pas la phrase).

---

## 7. Dette

- Table de réécriture : **15 entrées**, 5 pages (Analyse, Portefeuille, Options,
  Journal, Système).
- `MutationObserver` : coût **toujours pas mesuré**.
- Aucun instrument produit ne détecte le **rognage silencieux** (`overflow:hidden`
  sur un enfant trop large) — dette ouverte au lot Marchés, toujours ouverte.
- La vue `anomalies` n'a **aucun titre de carte** : sa section est introduite par
  un `<b>` dans un `.vx-page-lead`. Incohérent avec les trois autres vues, non
  corrigé ici pour ne pas mêler structure et copy dans le même lot.

---

## 8. Suite

Lot **04 — Analyse**.
