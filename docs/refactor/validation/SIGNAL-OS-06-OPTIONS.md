# SIGNAL OS · LOT 06 — OPTIONS

Branche : `agent/vertex-signal-os-v1` · SW v212 → **v213** · Suite **3076 passed**

---

## 1. Un en-tête différent des sept autres

Mesuré sur les **huit** fichiers de page :

| classe portant le sous-titre | pages |
| --- | --- |
| `<div class="vx-sub">` | **7** |
| `<p class="vx-page-lead__summary">` | **1** — Options |

Options portait en plus un `vx-page-lead__eyebrow` — « Intelligence de
convexité » — qu'**aucune autre page ne possède**, et qui ne disait rien de plus
que le `<h1>Options</h1>` situé une ligne plus bas.

Deux noms de classe pour un même rôle : un composant dupliqué pour changer le
look, ce que `VALIDATION.md` refuse, sous un `SKILL.md` §7 qui demande **un seul
shell**.

**Conservé** : le bouclier « Analyse uniquement · aucun ordre ». C'est le seul
élément du bloc qui porte une information, et c'est un invariant produit.

### Une entrée morte enfin expliquée

La table de micro-copy fermée au lot 04 contenait
`« Où est la meilleure convexité… » → « Convexité, volatilité et risque
événementiel. »`. Je l'avais classée « morte, produite par aucune page ». Elle
l'était pour une raison plus intéressante que je ne le pensais : la phrase cible
est **l'exemple de sous-titre donné par `COPY.md`**, et Options n'avait pas
l'élément qui aurait pu la recevoir. C'est elle qui est écrite ici, à la source.

---

## 2. Cinq titres qui posaient la question au lieu de nommer la chose

`COPY.md` : « Préférer des noms d'objets ou de décisions. »

| avant | forme du défaut | après |
| --- | --- | --- |
| `GEX quotidien — le gamma s'empile-t-il ?` | question **dans** le titre alors qu'un `.vx-chart-question` existait déjà dessous | `GEX quotidien` |
| `Scanner LEAPS — quels contrats longue échéance sont conformes ?` | idem | `Scanner LEAPS` |
| `Les options sont-elles chères ?` | le titre **était** la question — aucun nom d'objet | `Prix de la volatilité` |
| `Un événement menace-t-il l'échéance ?` | idem | `Risque événementiel` |
| `Que vaudra le contrat selon le spot, le temps et l'IV ?` | idem | `Scénarios de valeur` |

Les deux premiers disaient **deux fois la même chose** à deux lignes d'écart.
Les trois autres ne nommaient rien : impossible de savoir de quoi parle la carte
sans lire la réponse.

Les questions ne sont **pas supprimées** : elles descendent dans leur propre
élément. Un gardien tient ce point — `CHARTS.md` exige qu'un graphique dise à
quoi il répond.

### Le cinquième a été trouvé par le gardien, pas par moi

J'en avais corrigé quatre. Au premier lancement, le test qui refuse un
`.vx-card-title` finissant par `?` a signalé
« Que vaudra le contrat selon le spot, le temps et l'IV ? ». Un gardien écrit
comme une **propriété** trouve ce qu'une liste d'occurrences ne trouve pas.

---

## 3. Un doublon mesuré

Vue Structure, 1440 px :

| position | contenu |
| --- | --- |
| 1182 px | carte **« Payoff à l'échéance »** · *Où gagne / perd la structure selon le cours ?* |
| 1254 px | graphique **« Payoff à l'échéance — Put long »** · *Où gagne / perd la structure ?* |

Même titre, même question, **72 px** plus bas, dans une formulation à peine
différente. Le graphique ne garde que ce qu'il **ajoute** : quelle structure est
tracée.

Après : `1171 Payoff à l'échéance` · `1243 Put long`.

---

## 4. Mesures — version servie vérifiée avant de mesurer

`/sw.js` → `td-shell-v213`, contrôlé avant la première mesure.

| vue | sous-titre | titres | réécrits | erreurs |
| --- | --- | --- | --- | --- |
| structure | ✔ | `Payoff à l'échéance` · `Put long` · `Sensibilités (Greeks)` | 0 | 0 |
| positioning | ✔ | `Positionnement dealer` · `GEX par strike` · `GEX quotidien` | 0 | 0 |
| leaps | ✔ | `Scanner LEAPS` | 0 | 0 |
| volatility | ✔ | `Structure par terme de l'IV` · `Prix de la volatilité` | 0 | 0 |
| events | ✔ | `Risque événementiel` | 0 | 0 |

---

## 5. Gardiens

`tests/test_signal_os_options.py` — **7 tests**.

Le test d'en-tête **ne fige pas une classe** : il exige qu'il n'y en ait qu'**une**.
Si `vx-page-lead__summary` devenait un jour le standard, il échouerait sur les
sept autres — ce qui est la bonne conversation à avoir.

| mutation | résultat |
| --- | --- |
| en-tête Options redevient différent | 1 échec |
| eyebrow solitaire revenu | 1 échec |
| bouclier « lecture seule » retiré | 1 échec |
| titre redevient une question | 2 échecs |
| question supprimée au lieu d'être déplacée | 1 échec |
| graphique répète son cadre | 1 échec |

### Un trou dans mon propre gardien, trouvé par la mutation

`test_le_bouclier_lecture_seule_reste` cherchait `vx-readonly-shield` **dans tout
le fichier**. Les deux chaînes existent ailleurs (docstring, autres vues) : la
mutation qui retirait le bouclier de l'en-tête **passait au vert**. Le test lit
désormais le bloc `_HEADER` seul.

Quatrième fois qu'une assertion de sous-chaîne trop large me trompe dans cette
refonte. Le motif est constant : **chercher une chaîne dans un fichier n'est pas
lire un bloc.**

---

## 6. Ce que ce lot ne fait pas

Ni la structure des six vues, ni les graphiques, ni les données. Le profil de
lecture demandé par `PAGES.md` §6 (delta, DTE, spread, OI, break-even, coût,
perte max., scénarios) **n'a pas été vérifié champ par champ** — c'est un lot de
titres et d'en-tête.

---

## 7. Dette

- Options : 6 vues, profil de lecture non vérifié.
- Portefeuille : 5 vues sur 6 non auditées.
- Marchés : 6 vues non reconstruites.
- Analyse : la fiche `/analysis/<ticker>` reste inaccessible (`/api/ticker/<sym>`).
- Aucun instrument ne détecte le **rognage silencieux**.
- **Palette : l'interface est violette, les graphiques restent cuivre.** Décision
  utilisateur en attente.
- DoD non vérifié : Escape ferme drawer/modal, focus trap, palette de commandes,
  inventaire loading/empty/error/stale zone par zone.

---

## 8. Suite

Lot **07 — Journal**.
