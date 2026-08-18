# SIGNAL OS · LOT 07 — JOURNAL (et la règle généralisée aux huit espaces)

Branche : `agent/vertex-signal-os-v1` · SW v213 → **v214** · Suite **3081 passed**

---

## 1. Le gardien du lot précédent a servi deux fois

Le lot Options avait trouvé cinq `.vx-card-title` formulés en question — et le
gardien, écrit comme une **propriété** (« un titre ne se termine pas par ? »),
en avait trouvé **un cinquième que je n'avais pas vu**.

La même propriété, appliquée cette fois aux **huit** pages, en trouve quatre de
plus :

| page | sous-titre | titre |
| --- | --- | --- |
| `analysis_page.py` (fiche) | `Cette entreprise et cette opportunité méritent-elles du capital maintenant ?` | — |
| `performance_page.py` | `Suis-je en train de devenir un meilleur investisseur ?` | `Post-mortem — que disent mes sorties ?` |
| `system_page.py` | `Le système est-il en bonne santé et branché sur du réel ?` | — |
| les cinq autres | conformes | conformes |

**Cinq espaces sur huit le faisaient déjà correctement.** Trois posaient la
question à l'utilisateur au lieu de lui dire où il se trouve.

`COPY.md` § Sous-titres : « Maximum une ligne. **Expliquer ce que la zone aide à
décider.** » Ses trois exemples sont des orientations : « Régime, risque et
leadership. », « Exposition, risque et prochaine décision. », « Convexité,
volatilité et risque événementiel. »

| avant | après |
| --- | --- |
| `Suis-je en train de devenir un meilleur investisseur ?` | **`Ce qui renforce ou dégrade la qualité des décisions.`** |
| `Le système est-il en bonne santé et branché sur du réel ?` | **`Connexions, fraîcheur des données et confiance du terminal.`** |
| `Cette entreprise et cette opportunité méritent-elles du capital maintenant ?` | **`La thèse mérite-t-elle du capital, et à quel risque.`** |
| `Post-mortem — que disent mes sorties ?` | **`Post-mortem`** + question dans son élément |

### La question n'est pas perdue

La question **de la page** vit dans `PAGES.md` et dans le docstring du module :
c'est une boussole de conception. Le sous-titre, lui, est relu à chaque visite —
il doit orienter. Pour un **graphique**, `CHARTS.md` exige au contraire la
question, et elle a son élément.

---

## 2. Le dernier possessif du produit

`Ma progression` → **`Progression`**. « Mes positions » était devenu
« Positions » au lot 04 ; celui-ci avait survécu. Un gardien refuse désormais
tout titre commençant par `Ma` / `Mon` / `Mes` sur les huit pages.

---

## 3. Le gardien des noms personnels m'a arrêté

Mon premier sous-titre était :

> « Ce qui **améliore** ou dégrade la qualité des décisions. »

`test_no_personal_name_in_current_tree` a mordu. Accents retirés,
**am‑élio‑re** contient le motif interdit. Le mot est banal, la règle est
absolue, et je ne l'aurais pas vu.

Reformulé en « Ce qui **renforce** ou dégrade… ». C'est exactement le genre de
piège pour lequel ce gardien existe : il ne cherche pas une faute d'inattention,
il cherche un motif **caché dans un mot ordinaire**.

---

## 4. Un trou dans mon propre contre-exemple, trouvé par la mutation

`test_les_huit_espaces_ont_bien_un_sous_titre` vérifiait que le fichier contient
`class="vx-sub"` **quelque part**. Trois pages en ont plusieurs (en-têtes de
sous-vues) : la mutation qui **supprimait** le sous-titre de la page restait au
vert.

Il exige maintenant un `vx-sub` dans les 400 caractères qui suivent le premier
`<h1>`. **Cinquième fois** qu'une assertion de portée trop large me trompe dans
cette refonte — le motif ne varie pas : *chercher une chaîne dans un fichier
n'est pas lire un bloc.*

---

## 5. Mesures — version servie vérifiée avant de mesurer

`/sw.js` → `td-shell-v214`.

| route | sous-titre servi | réécrits | erreurs |
| --- | --- | --- | --- |
| `/journal` | `Ce qui renforce ou dégrade la qualité des décisions.` | 0 | 0 |
| `/system` | `Connexions, fraîcheur des données et confiance du terminal.` | 0 | 0 |

---

## 6. Gardiens

`tests/test_signal_os_copy_grammaire.py` — **5 tests**, portant sur les **huit**
pages et non sur une seule. Portée dite : ils lisent les **sources de page**ﾠ; un
titre construit à l'exécution en JavaScript leur échappe.

| mutation | résultat |
| --- | --- |
| sous-titre Journal redevient une question | 1 échec |
| sous-titre Système redevient une question | 1 échec |
| sous-titre **supprimé** au lieu d'être reformulé | 1 échec |
| titre post-mortem redevient une question | 2 échecs |
| possessif revenu | 1 échec |

---

## 7. Ce que ce lot ne fait pas

La structure du Journal n'a **pas** été reconstruite. `PAGES.md` §7 demande six
rangs (track record séparant signaux et positions réelles, décisions récentes,
résultats par grade/setup/horizon, erreurs répétées, learnings, notes) et cinq
visualisations (equity, drawdown, win/loss par bucket, distribution, calibration
score→résultat) : **rien de tout cela n'a été vérifié**.

Les cinq vues existent et portent des noms cohérents ; leur contenu n'a pas été
audité rang par rang.

---

## 8. Dette

- Journal : 6 rangs et 5 visualisations non vérifiés.
- Options : profil de lecture non vérifié · Portefeuille : 5 vues sur 6 ·
  Marchés : 6 vues · Opportunités : structure jugée, pas mesurée.
- Analyse : fiche `/analysis/<ticker>` inaccessible ici.
- Aucun instrument ne détecte le **rognage silencieux**.
- **Palette : interface violette, graphiques cuivre.** En attente de décision.
- DoD non vérifié : Escape, focus trap, palette de commandes, inventaire
  loading/empty/error/stale.

---

## 9. Suite

Lot **08 — Système**, puis la passe finale.
