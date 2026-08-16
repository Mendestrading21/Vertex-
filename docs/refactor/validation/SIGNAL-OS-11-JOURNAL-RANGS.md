# SIGNAL OS · LOT 11 — JOURNAL : LES SIX RANGS, MESURÉS

Branche : `agent/vertex-signal-os-v1` · SW v217 → **v218** · Suite **3093 passed**

Le lot 07 avait écrit, en toutes lettres : « la structure du Journal n'a **pas**
été reconstruite … rien de tout cela n'a été vérifié ». Voici la vérification.

---

## 1. Quatre rangs sur six sont couverts, et proprement

| rang `PAGES.md` §7 | état |
| --- | --- |
| 1. Track record séparant signaux et positions réelles | **couvert** |
| 2. Décisions récentes | **couvert** |
| 3. Résultats par grade / setup / horizon | **partiel** |
| 4. Erreurs répétées | **couvert** |
| 5. Learnings | **couvert** |
| 6. Notes et historique | **couvert** |

Le rang 1 est mieux tenu que la spécification ne l'exige : `track-record` oppose
« Moteur · verdicts théoriques » et « Journal · trades déclarés », marque chacun
par `data-source-kind`, et **écrit** la règle — « Aucun chiffre ne passe de
l'une à l'autre ». C'est l'invariant le plus fort de cette page, et il est
visible pour l'utilisateur, pas seulement vrai dans le code.

### Le rang 3, dit comme partiel

« Rendement moyen +20 séances **par verdict** » n'est ni par grade, ni par
setup, ni par horizon. Je **ne fabrique pas** un découpage dont je n'ai pas
vérifié que les données le portent : la dette est écrite, pas comblée au jugé.

---

## 2. Le conflit des visualisations, tranché plutôt que contourné

`PAGES.md` §7 demande cinq visualisations, dont **equity curve** et
**drawdown**. Elles ne sont pas dans le Journal.

Ce n'est pas un oubli : `equityCard` et `drawdownCard` existent au registre et
sont appelées par **Portefeuille**, où elles ont été migrées.

**Les ramener créerait deux courbes d'équité**, donc deux vérités possibles sur
un même capital. La règle « une donnée = un seul domicile » prime sur la liste
des visualisations — et c'est elle que le gardien tient, avec un contre-exemple :
si le domicile disparaissait de Portefeuille, le test mord aussi, parce que le
relais pointerait alors vers le vide.

| visualisation | état |
| --- | --- |
| equity curve | domiciliée **Portefeuille** · relais depuis `progression` |
| drawdown | domiciliée **Portefeuille** · relais depuis `progression` |
| distribution de résultats | **présente** |
| win/loss par bucket | **partiel** — une moyenne par verdict n'est pas un win/loss |
| calibration score→résultat | carte présente, **aucun tracé** |

Le Brier reste **déclaré indisponible** tant qu'il n'est pas mesurable. C'est
« donnée absente → mention honnête » appliqué à une métrique, et c'est plus
difficile à tenir qu'un tiret : il est tentant d'afficher un chiffre approché.

---

## 3. Ce que j'allais publier, et qui était faux

J'avais rédigé : « le Journal ne dit **nulle part** où sont l'équité et le
drawdown ». En comptant les occurrences avant d'écrire le gardien : **il le dit
deux fois** — dans la vue `overview` et dans un état vide.

Le trou réel est plus étroit, et c'est celui-là qui compte : **rien dans
`progression`**, c'est-à-dire pas dans la vue qui *pose* la question « est-ce que
je progresse ». Une adresse écrite ailleurs que là où l'on cherche ne sert
personne.

Un relais nommé y est posé : « Équité & drawdown → ». Il **nomme** sa
destination — un lien sans objet serait le « View more » que `COPY.md` proscrit.

---

## 4. Trois assertions de mon propre gardien étaient trop larges

Trouvées par mutation, avant publication :

| assertion | pourquoi elle restait verte |
| --- | --- |
| « `Erreurs récurrentes` est présent » | la chaîne figure **2 fois** — titre **et** texte d'état vide ; renommer le titre ne la faisait pas disparaître |
| « le relais existe » | `/portfolio?view=performance` figure **3 fois** dans le fichier ; deux mentions préexistantes hors de la vue |
| « `equityCard` est dans Portefeuille » | le nom figure **2 fois** — garde de disponibilité **et** appel ; remplacer l'appel laissait la garde |

**Septième fois** que ce motif me trompe dans cette refonte. Resserré : les rangs
sont lus dans les **titres** (`.vx-card-title` et `<h2>`), le relais dans le
**bloc de la vue** et sur un **élément d'action**, le domicile sur l'**appel**.

Une correction m'a aussi été imposée dans l'autre sens : ma première version ne
lisait que `.vx-card-title` et accusait à tort le rang 2, dont le titre est un
`<h2>` de vue. **Un gardien trop étroit accuse aussi faussement qu'un gardien
trop large.**

---

## 5. Mesures

`/sw.js` → `td-shell-v218` (vérifié avant lecture).

Relais rendu sur `/journal?view=progression` : texte « Équité & drawdown → »,
`href="/portfolio?view=performance"`, hauteur 30 px, visible. **0 erreur de
page.**

Gardien `tests/test_signal_os_journal_rangs_lot11.py` — 5 tests, **8 mutations
sur 8 tuées** :

| mutation | résultat |
| --- | --- |
| titre du rang 4 renommé | 1 échec |
| relais retiré de `progression` | 1 échec |
| relais devenu « Voir plus » | 1 échec |
| appel `equityCard` retiré de Portefeuille | 1 échec |
| appel `drawdownCard` retiré | 1 échec |
| équité dupliquée dans le Journal | 1 échec |
| les deux sources d'historique fusionnées | 1 échec |
| Brier fabriqué au lieu d'être déclaré indisponible | 1 échec |

---

## 6. Dette

- **Rang 3** : résultats par grade / setup / horizon — à instruire avant de
  construire (les données portent-elles ces axes ?).
- **Win/loss par bucket** : une moyenne par verdict n'est pas un win/loss.
- Contenus non audités : Marchés (6 vues), Opportunités (rangs), Portefeuille
  (5 vues sur 6), Options (profil de lecture).
- `chart-theme-obsidian-copper.js` : nom qui ment, renommage à solder seul.
- Étiquetage démo : figé en caractérisation (lot 08).
- Aucun instrument ne détecte le rognage silencieux.
- 5 modules UI morts (146 Ko, 0 consommateur) non supprimés.
