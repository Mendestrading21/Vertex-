# SIGNAL OS · LOT 04 — LA TABLE DE MICRO-COPY EST FERMÉE

Branche : `agent/vertex-signal-os-v1` · SW v210 → **v211** · Suite **3064 passed**

---

## 1. Pourquoi ce lot n'est pas « Analyse »

L'ordre du skill dit Analyse. En mesurant ce qui restait à migrer sur cette page,
j'ai trouvé **sept réécritures vivantes** en tout, réparties sur trois pages :

| page | libellés encore réécrits dans le DOM |
| --- | --- |
| `/analysis` | `Récents` · `Recherche` · `Portefeuille` |
| `/portfolio` | sous-titre · onglet `Surveillance` |
| `/options` | onglets `Positions` · `Catalyseurs` |
| `/journal`, `/system` | **aucune** |

Sept. `WORKFLOW.md` : « Modifier d'abord les primitives si la correction doit
bénéficier à plusieurs pages. » Faire Analyse seule aurait laissé la table
ouverte pour deux libellés — et la dette que j'ai signalée **trois lots de suite
sans la mesurer** serait restée.

**Ce lot ferme la table.**

---

## 2. Le mécanisme, une dernière fois

La couche portait une `Map` de **45 libellés** réécrits dans le DOM **après** le
rendu : le serveur envoyait « VIX — volatilité implicite du marché », l'écran
affichait « VIX ».

Deux vérités pour un même libellé. Tout gardien qui lit les octets servis gardait
**l'ancienne**, pendant que la nouvelle n'était gardée par **rien**.

Vidée page par page : shell + Aujourd'hui (7), Marchés (15), Opportunités (5),
et les 7 derniers ici.

---

## 3. Huit entrées ne pouvaient déjà plus rien réécrire

| entrée | pourquoi elle était morte |
| --- | --- |
| `Rechercher un titre pour ouvrir sa fiche canonique.` | produite par aucune page |
| `Ce que révèle une fiche` | produite par aucune page |
| `Que s'est-il passé après ? — évidence historique` | produite par aucune page |
| `Cette structure offre-t-elle une asymétrie suffisante ?` | produite par aucune page — et présente **deux fois** dans la table |
| `Skyler — décision canonique` | n'existe que dans un **commentaire** de code |
| `Où est la meilleure convexité…` | n'existe que dans une **docstring** |
| `Ajouter` | déjà écrit à la source au lot Shell |

**Une table de réécriture ne peut pas savoir qu'elle est périmée.** Elle cherche
une chaîne, ne la trouve pas, et ne fait rien. Aucune erreur, aucun signal.
C'est exactement sa nature, et c'est pourquoi elle ne pouvait pas rester.

---

## 4. Ce qui disparaît avec la table

`replaceStaticCopy` — la passe que le `MutationObserver` relançait sur **sept
sélecteurs et tout le sous-arbre de `#vx-content`** à **chaque mutation du DOM**,
donc à chaque mise à jour live.

C'est la dette que j'ai signalée aux lots Shell, Aujourd'hui, Marchés et
Opportunités en écrivant chaque fois « coût non mesuré ». Je ne l'ai toujours pas
mesurée — **je l'ai supprimée.**

L'observateur **reste**, et il est nécessaire : les grades arrivent avec les
données, donc après le premier rendu, et la navigation persistante remplace le
contenu sans recharger la page. Mais il ne relance plus que deux passes qui
**lisent** des attributs (`normalizeGrades`, `normalizeDecisionCards`) sans
toucher au texte.

---

## 5. Un dernier libellé, aligné sur sa destination

Le raccourci d'Analyse affichait `Scanner d'opportunités` alors que l'espace
s'appelle **Opportunités** dans la navigation, le fil d'Ariane et le titre de la
page. Un raccourci nomme sa destination.

---

## 6. Mesures — version servie vérifiée avant de mesurer

`/sw.js` → `td-shell-v211`, contrôlé **avant** la première mesure (leçon du lot
Opportunités, où une instance en v209 m'avait rendu quatre lignes fausses).

| page | libellés réécrits dans le DOM |
| --- | --- |
| `/` · `/markets` · `/opportunities` · `/analysis` | **0** · **0** · **0** · **0** |
| `/portfolio` · `/options` · `/journal` · `/system` | **0** · **0** · **0** · **0** |

**Le serveur et l'écran disent maintenant la même chose sur les huit espaces.**

8 espaces × 4 largeurs : **0 erreur console**, 0 débordement réel, sidebar
224 px / rail 72 px / rail 72 px / hors-champ.

---

## 7. Gardiens

Le test qui énumérait les entrées mortes **s'est pris les pieds dedans** : le
commentaire qui explique la fermeture cite les libellés retirés, et une
énumération de chaînes interdites interdit aussi qu'on écrive **pourquoi** on les
a retirées. Troisième occurrence de cette famille dans la refonte (616-B).

Remplacé par une propriété **structurelle**, plus forte :

```
'const COPY' not in js
'replaceStaticCopy' not in js
'.textContent =' not in js
```

Plus `test_les_libelles_migres_sont_bien_a_la_source` : la table est fermée
**parce que** chaque libellé a été écrit à sa source — pas parce qu'on a renoncé
aux libellés. Les deux tests se tiennent l'un l'autre.

Deux gardiens existants mis à jour **avec leur raison** :
`test_options_new_views_registered` (garde la vue `positions`, pas son libellé)
et `test_signal_os_copy_layer_is_local_and_read_only`.

---

## 8. Dette

- **Analyse n'est pas faite.** Ce lot a pris ses trois libellés, pas sa
  structure. La fiche `/analysis/<ticker>` — les onze rangs de `PAGES.md` — n'a
  **pas été ouverte** : la charger déclenche `/api/ticker/<sym>`, interdit dans
  cet environnement. Elle demandera une session où ce chemin est autorisé.
- Aucun instrument produit ne détecte le **rognage silencieux** (`overflow:hidden`
  sur un enfant trop large) — ouvert au lot Marchés, toujours ouvert.
- La vue `anomalies` d'Opportunités n'a toujours aucun titre de carte.
- La palette violette n'est toujours pas dans `palette.py` : `signal-os.css`
  redirige `--vx-brand` vers `--vx-option`, donc **les graphiques restent
  cuivre**. Décision à prendre explicitement.

---

## 9. Suite

Lot **05 — Analyse (structure)**, puis Portefeuille, Options, Journal, Système.
