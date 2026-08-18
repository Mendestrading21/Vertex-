# SIGNAL OS · LOT 61 — CHAQUE CHIFFRE PEINT VIENT-IL D'UNE SOURCE ?

Branche : `agent/vertex-signal-os-v1` · SW **v242, inchangé** (aucun octet servi
touché) · Suite **3 492 passed** (3 486 → +6)

Réserve SIGNAL-OS-60 §3 et §5.3, de ma main :

> Il ne sait pas reconnaître un hôte qui aboutit avec une valeur **inventée** ou
> **périmée**. […] C'est de loin le plus utile qui manque encore.

C'est le seul défaut qui, dans un terminal d'analyse, peut coûter **de l'argent**
plutôt que de la confiance : un chiffre plausible, affiché sans source.

---

## 1. Le principe, et ce qu'il garantit exactement

`tools/mesurer_chiffres_tracables.py` capture **tout ce que la page reçoit** (le
corps de chaque réponse d'API), extrait **tout ce qu'elle affiche** (les nombres
de `innerText`), et demande pour chacun : *est-il dans ce qui est arrivé ?* —
exactement, ou à l'arrondi près.

Un nombre peint absent de toute réponse est **inexpliqué**. Cela ne prouve pas
qu'il soit inventé : il peut être **dérivé** (une somme, un écart, un
pourcentage). Mais l'implication qui compte tient dans l'autre sens et elle est
solide :

> **Tout chiffre inventé est nécessairement inexpliqué.**

Donc la liste des inexpliqués **contient** tous les défauts de cette famille.
L'outil réduit l'espace à fouiller ; il ne rend pas un verdict moral. C'est le
lecteur qui tranche — et je l'ai fait, un par un.

---

## 2. Le résultat : aucun chiffre inventé

Huit espaces, nominal, puis sous panne de `market` et de `skyler`.

| espace | tracés | inexpliqués |
| --- | --- | --- |
| Aujourd'hui | 25 | 0 |
| Marchés | 68 | 0 |
| Opportunités | 46 | 0 |
| Analyse | 40 | 0 |
| Portefeuille | 4 | 3 |
| Options | 26 | 4 |
| Journal | 16 | 0 |
| Système | 5 | 0 |

Les sept inexpliqués, lus **avec leur contexte**, sont tous des dérivations que
la page **nomme elle-même** :

```text
150,42   … mouvement attendu ~1σ (IV·√t) / Sous-jacent / 150,42 …
209,58   … mouvement contraire ~1σ / Sous-jacent / 209,58 …
280,86   … Gain probable (+1σ, échéance) / +280,86 …
3 239    … P&L (échéance) / +3 239 / P&L % / +142 % …
65       … Concentration élevée : ACN = 65 % du portefeuille …
100      … Top 1 ACN · Top 3 100 % · repère ~15 % …
35       … Exposition / options 35 % …
```

Le point qui rassure n'est pas qu'ils soient absents des réponses — c'est que
**leur libellé énonce le calcul**. « Mouvement attendu ~1σ (IV·√t) » dit d'où
vient le chiffre. C'est la règle produit tenue à l'endroit exact où elle compte.

Sous panne, aucun inexpliqué **nouveau** n'apparaît : les mêmes agrégats
subsistent, et ils viennent de familles restées vivantes. Un cas mérite d'être
cité pour sa franchise — « Valeur nette / 2 300 / **cash non renseigné** » : la
page calcule ce qu'elle peut et **nomme ce qui manque**.

---

## 3. Le témoin qui compte le plus de toute la série

« Zéro inexpliqué » et « je ne sais pas voir » rendent **le même chiffre**.

Le mode `--temoin` injecte dans la page un nombre qui n'est dans aucune réponse
(`987654,321`) et exige que l'outil le dénonce :

```text
TEMOIN : chiffre fabrique DENONCE — le detecteur mord
traces : 68 · inexpliques : 1
inexpliques : 987654,321
```

Sans cela, tout ce rapport ne vaudrait rien. Deux autres refus de conclure
complètent le dispositif : aucune réponse capturée, ou aucun nombre expliqué.

---

## 4. Deux artefacts que j'ai failli publier comme trouvailles

Le premier passage accusait `2026 12` (Aujourd'hui) et `127.0` (Système).

**Ni l'un ni l'autre n'existe.** C'était **mon propre découpage** qui les
fabriquait : l'espace pris pour séparateur de milliers sur un groupe de deux
chiffres — donc une date collée à son mois — et une adresse `127.0.0.1` coupée
en morceaux. Corrigé : le séparateur de milliers exige des groupes de **trois**
chiffres, et un nombre suivi de `.chiffre` est ignoré.

Publier ces deux-là aurait été **accuser le produit de mes fautes**. C'est la
raison d'être de la relecture du §2 : un inexpliqué sans son contexte n'est pas
une trouvaille, c'est une alarme.

---

## 5. Le gardien, et ses quatre mutations

| mutation | test qui tombe |
| --- | --- |
| le chiffre fabriqué du témoin retiré | le témoin |
| la garde contre les adresses IP retirée | les artefacts |
| la tolérance à l'arrondi supprimée | l'appariement |
| une limite effacée de l'en-tête | les limites déclarées |

La troisième mérite un mot : sans tolérance, `198,00` peint contre `198.0031`
reçu serait « inexpliqué », et la liste noierait tout vrai défaut sous les prix.
Un détecteur trop strict est aussi inutile qu'un détecteur aveugle.

---

## 6. Réserves — et elles bornent ce que le §2 autorise à conclure

1. **« Dérivé » n'est pas distingué de « inventé ».** Le tri est humain. Sept cas
   ici, tous lus. À cent, la méthode ne tiendrait pas telle quelle.
2. **La fraîcheur n'est pas jugée.** Un nombre présent dans une réponse
   **périmée** paraît tracé. La moitié « périmée » de la réserve du lot 60
   reste donc ouverte — seule la moitié « inventée » est traitée.
3. **Seul `innerText` est lu.** Un chiffre peint dans un attribut, un `title`,
   ou dessiné dans un SVG échappe à la mesure.
4. **Deux familles coupées** (`market`, `skyler`) sur les seize relevées.
5. **Mode démonstration, une seule largeur, un seul titre** (`ACN`).
