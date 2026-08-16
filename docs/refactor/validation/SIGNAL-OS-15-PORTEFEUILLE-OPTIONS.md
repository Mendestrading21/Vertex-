# SIGNAL OS · LOT 15 — PORTEFEUILLE ET OPTIONS, LES DEUX DERNIERS AUDITS DE RANGS

Branche : `agent/vertex-signal-os-v1` · SW v221 → **v222** · Suite **3110 passed**

---

## 1. Portefeuille — `PAGES.md` §5

| rang | vue |
| --- | --- |
| 1. Valeur / P&L / cash / drawdown | `team` (bande KPI) · `performance` |
| 2. Risque global et concentration | `risk` · « Allocation & concentration » |
| 3. Positions prioritaires à revoir | `team` « Positions exigeant une décision » |
| 4. Allocation / exposition secteurs | `risk` · donut « Secteurs » |
| 5. Table positions | `positions` |
| 6. Watchlist / candidats | `watchlist` (3 blocs) |
| 7. Alertes et prochains catalyseurs | `team` « Ce qui a changé » · `watchlist` |

**Les sept rangs sont couverts par les six vues**, et la règle propre à la page
— « le risque avant les statistiques décoratives » — tient depuis le lot 06.

### Le défaut

La vue **`performance` n'avait aucun titre**. Hors le `<h1>` de la page, son
seul intitulé était le `<b>` d'une note.

C'est la **deuxième** vue du produit dans ce cas après `anomalies` (lot 14) :
deux occurrences font une famille, pas un accident.

Et c'est la plus gênante des deux : c'est le **domicile de la courbe d'équité**,
donc la destination du relais que j'ai posé sur le Journal au lot 11. **On y
arrive en cherchant explicitement sa progression** — et on tombait sur quatre
états vides sans en-tête.

La note « domicile unique » est **conservée** : c'est elle qui explique pourquoi
l'équité n'est pas dans le Journal, donc ce qui rend ce relais honnête plutôt
qu'arbitraire. Un gardien la tient séparément du titre.

---

## 2. Options — `PAGES.md` §6

Les six vues d'onglet sont **toutes titrées** et portent **toutes leur
question**. Les sept rangs sont couverts (environnement IV/term/liquidité,
LEAPS, filtres, payoff, thêta/sensibilités, risque événementiel, relais
watchlist).

### Le profil de lecture, dette annoncée depuis le lot 06

`PAGES.md` §6 exige huit champs : *delta, DTE, spread, OI, break-even, coût,
perte max., scénario probable/exceptionnel*. Mesuré sur la vue qui porte des
données : **6 sur 8**. Manquaient **`spread`** et **`OI`**.

### Et ils étaient calculés

`liqState()` produit un champ `note` valant exactement
« OI 12 340 · spread 2,1 % » — les deux chiffres demandés — et **aucun des deux
sites de rendu ne l'affichait**. L'écran montrait « Liquidité : Excellente »,
sans qu'on puisse distinguer OI 5 000 / spread 3 % de OI 50 000 / spread 0,2 %.

> Une donnée calculée puis jetée coûte plus cher qu'une donnée absente : le
> produit sait, et se tait.

Affichée aux **deux** sites — carte-verdict et ligne de tableau — y compris son
état honnête « bid/ask ou OI absent — non évaluable », qui devient visible
maintenant qu'elle est rendue.

---

## 3. Ce que je n'ai PAS accusé, et c'est délibéré

Les vues `positions` et `leaps` d'Options rendent 1/8 et 5/8 champs du profil.
**Elles sont vides en démo** — aucune position options déclarée, aucun LEAPS
retenu par le scanner. Mesurer un profil de lecture sur une table vide n'accuse
pas le produit, ça accuse le jeu de données.

---

## 4. Un faux manquant, arrêté au dernier moment

Ma mesure finale annonçait **7/8**, `OI` manquant. Vérification avant
publication : `\bOI\b` échoue sur `MédiocreOI 6169` — le `textContent`
concatène les nœuds sans espace, donc il n'y a pas de frontière de mot. Le champ
**est** rendu.

**8/8.** C'est le cinquième artefact d'instrument arrêté dans cette refonte, et
celui-ci aurait fait publier un manque qui n'existe pas juste après l'avoir
corrigé.

---

## 5. Mesures — serveur `td-shell-v222` vérifié avant lecture

| relevé | résultat |
| --- | --- |
| profil de lecture Options (`structure`) | **8/8** |
| liquidité rendue | `Liquidité : Médiocre · OI 6169 · spread 7,1 %` |
| titre de la vue Performance | « Performance de portefeuille » |
| erreurs de page | **0** |

Gardien `tests/test_signal_os_rangs_pf_options_lot15.py` — 4 tests, **6
mutations sur 6 tuées**. Les deux sites de rendu de la liquidité sont vérifiés
**nommément** : une assertion « au moins deux occurrences » restait verte quand
on en retirait un — et mon propre commentaire dans le produit contenait la
chaîne, ce qui suffisait à la satisfaire. Même piège qu'au lot 13.

---

## 6. Dette restante

- Rang 3 du Journal (grade / setup / horizon) et win/loss par bucket.
- 5 modules UI morts : mesure faite au lot 13, suppression à instruire.
- `chart-theme-obsidian-copper.js` : nom qui ment.
- Étiquetage démo : figé en caractérisation (lot 08).
- Fiche `/analysis/<ticker>` inaccessible dans cet environnement.
