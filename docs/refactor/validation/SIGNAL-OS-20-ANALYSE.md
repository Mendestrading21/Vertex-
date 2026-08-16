# SIGNAL OS · LOT 20 — ANALYSE, LE HUITIÈME ESPACE

Branche : `agent/vertex-signal-os-v1` · SW v225 → **v226** · Suite **3112 passed**

Depuis le lot 12 je répétais la même phrase : « `/analysis/<ticker>` est
**non mesurable** dans cet environnement — l'ouvrir déclenche
`/api/ticker/<sym>`, appel sortant interdit. » Elle était fausse **deux fois**.

---

## 1. Ce que le constat cachait

### `/analysis` — l'index — n'a jamais rien eu d'interdit

Il ne consulte que `/api/names`. Il était mesurable depuis le premier lot.
Personne ne l'avait ouvert parce qu'il porte le même nom que la fiche : j'ai
étendu l'interdiction de l'une à l'autre **sans le vérifier**.

### La fiche est mesurable en avortant les appels interdits

`page.route(motif, r => r.abort())` intercepte **dans le navigateur** : la
requête ne part jamais, donc le serveur n'exécute jamais la route, donc **aucun
appel sortant n'a lieu**. La consigne est respectée à la lettre.

La mesure obtenue est **partielle**, et je la donne comme telle : elle prouve la
structure, la mise en page, les identifiants dupliqués et les erreurs de page ;
elle ne prouve rien du rendu des données bloquées.

> « Non mesurable » était un raccourci confortable : il transformait une mesure
> **plus difficile** en mesure **impossible**, et personne n'allait vérifier.

---

## 2. Les onze rangs de `PAGES.md` §4 — mesurés, 11 sur 11

| rang | hôte | présent |
| --- | --- | --- |
| 1. Identity strip | `.an-identity` | oui |
| 2. Verdict en une phrase | `#an-verdict` | oui |
| 3. Asymétrie | `#an-scenarios` | oui |
| 4. Price chart | `#an-chart` | oui |
| 5. Catalyseurs | `#an-catalysts` | oui |
| 6. Fondamentaux | `#an-fundamental` | oui |
| 7. Technique | `#an-technical` | oui |
| 8. Positionnement | `#an-sentiment` | oui |
| 9. Risques / invalidation | `#an-rail-risks` | oui |
| 10. Options adaptées | `#an-options` | oui |
| 11. Notes / suivi | `#an-history` | oui |

La règle de la page — « ne pas demander de lire 20 cartes avant de connaître le
verdict et le risque » — est tenue par la composition : verdict et scénarios
occupent le premier niveau, l'expertise est repliée dans deux `<details>`
(« Analyse approfondie », « Outils d'analyse »).

---

## 3. Le défaut trouvé — et sa cause était déjà connue

Le **radar de scorecard** était tracé **sans question ni conclusion**.

C'est la **troisième** occurrence de la même cause structurelle, après le donut
« Secteurs » du Portefeuille (lot 12) : ce ne sont pas les graphiques qui
oublient la règle de `CHARTS.md`, ce sont **ceux qui n'entrent pas par le
gabarit `VXCharts.card`**. Trois fois le même mécanisme, ce n'est plus un
accident :

> Un graphique monté dans une carte bâtie à la main n'a personne pour lui
> imposer sa question.

### Le correctif

- Question : « Quel axe de la décision est le plus faible ? »
- Conclusion **dérivée des axes tracés** — elle nomme l'axe le plus faible et
  **sa valeur**. Une phrase générique aurait été pire qu'une absence : elle
  aurait eu l'air d'une mesure.
- L'état honnête existant est conservé : axes manquants → radar **non tracé**,
  et les axes absents sont nommés.

Idiome retenu : question **et** conclusion visibles, comme le donut du lot 12.
Le repli en `.vx-sr-only` appartient au gabarit `VXCharts.card` ; les cartes
bâties à la main du produit affichent les deux.

---

## 4. Mesures — serveur `td-shell-v226` vérifié avant lecture

### `/analysis` (index) — mesure complète

| viewport | erreurs de page | débordement | ids dupliqués |
| --- | --- | --- | --- |
| 1440×900 | **0** | non | 0 |
| 768×1024 | **0** | non | 0 |
| 390×844 | **0** | non | 0 |

### `/analysis/ACN` (fiche) — mesure partielle

Points d'entrée avortés au navigateur : `/api/ticker/ACN`, `/api/options-for/ACN`.
Les seules erreurs console sont les `net::ERR_FAILED` de ces avortements — ce
sont **mes** blocages, pas des défauts du produit.

| relevé | 1440 | 390 |
| --- | --- | --- |
| débordement de page | non | non |
| ids dupliqués | 0 | 0 |
| radar tracé | oui | oui |
| conclusion rendue | « Axe le plus faible : Timing (50/100). » | idem |

La conclusion est **vérifiée contre le moteur** : `/api/strategy/decision/ACN`
rend `timing: 50.0`, `data_quality: 50`, `conviction: 52.5`, `asymmetry: 80.0`,
`risk: 100.0`. Le minimum est bien 50, et le tri stable retient `Timing`.

Sur `/analysis/NVDA` — absent du scan courant, donc **sans scores** — le radar
n'est pas tracé et affiche « Radar non tracé — axes n/d : … ». L'état honnête
fonctionne sur une vraie absence de données, pas sur une absence simulée.

---

## 5. L'instrument couvre enfin la fiche

`tools/mesurer_rognage_silencieux.py` balayait `/analysis` (l'index) mais jamais
la fiche — le seul écran du produit qu'aucun instrument ne visitait. Il la
balaie maintenant, avec la liste `INTERDITS` avortée au navigateur.

Relevé après extension : **0 élément rogné en silence à 1440 px, 0 à 390 px.**

### Ce que je n'ai PAS accusé

Le fil d'Ariane est coupé à 390 px (« Analyse » : 28 px, « ACN » : 16 px). Ce
n'est **pas** un défaut : `text-overflow:ellipsis` **signale** la coupure.
L'instrument du lot 13 l'exclut explicitement — ma sonde ad-hoc, elle, ne le
faisait pas et l'accusait. **Onzième** fois qu'une portée d'instrument me
trompe, cette fois par excès : j'ai failli signaler un défaut de shell qui
n'existe pas.

---

## 6. Gardien — `tests/test_signal_os_analyse_lot20.py` (5 tests, 8 mutations sur 8 tuées)

| mutation | résultat |
| --- | --- |
| question du radar retirée | 1 échec |
| hôte de la conclusion retiré | 1 échec |
| conclusion non dérivée (axe figé) | 1 échec |
| conclusion générique | 1 échec |
| état honnête « axes n/d » retiré | 1 échec |
| hôte du rang 3 renommé | 1 échec |
| fiche retirée de l'instrument | 1 échec |
| avortement des interdits retiré | 1 échec |

### Deux portées trop larges, attrapées par la mutation et non par la relecture

1. **Ma borne de bloc** s'arrêtait à la première occurrence de
   `missingAxes.length){` — qui est le `if(…!missingAxes.length){` **ouvrant**
   la branche. Le bloc était tronqué **avant** la dérivation, et le test
   échouait sur du code présent.
2. **`'an-scorecard-ccl' in bloc`** restait **vert** après suppression du `<p>` :
   la ligne qui l'interroge, `$('an-scorecard-ccl')`, contient le même
   identifiant. Le test était satisfait par le code qui **lit** l'élément, pas
   par l'élément. **Douzième** occurrence du même motif dans cette refonte.

Les deux corrections sont dans le fichier, avec leur raison.

---

## 7. État après ce lot

Les **huit** espaces sont audités rang par rang, et **tous les huit** sont
désormais mesurés au navigateur. Il ne reste aucune zone du produit déclarée
hors de portée.

Réserve honnête : sur la fiche, la mesure reste **partielle** — le rendu des
données servies par les points d'entrée interdits (cours, profil entreprise,
chaîne d'options) n'est pas observé dans cet environnement, seulement leur
dégradation, qui est propre : hôtes présents, états de chargement, pas d'erreur
de page.
