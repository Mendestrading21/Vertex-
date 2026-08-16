# SIGNAL OS · LOT 08 — SYSTÈME : un instrument faux, et un constat qui vaut mieux qu'un correctif

Branche : `agent/vertex-signal-os-v1` · SW **v214 inchangé** · Suite **3083 passed**

**Ce lot ne change aucun octet de production.** Il corrige un instrument, annule
deux accusations que j'allais porter, et fige un constat que je refuse de
corriger sans l'avoir fondé.

---

## 1. Deux fausses accusations, arrêtées avant publication

### (a) « Les connexions sont affichées deux fois »

Mon relevé de structure plaçait « Matrice consolidée des connexions » à 400 px
**et** trois cartes IBKR / TradingView / Claude à 1142 px, hautes de 382 px.
J'allais écrire : doublon, `VALIDATION.md` demande de fusionner.

**Faux.** Les trois cartes sont dans un `<details>` **fermé**. Mesuré
directement : `ouvert: false`, hauteur du bloc **50 px**. C'est de la
divulgation progressive — exactement ce que le skill demande.

### (b) « L'onglet `engines` sert la même page que `connections` »

Mon relevé donnait deux vues au contenu rigoureusement identique.

**Faux.** `engines` **n'est pas une vue déclarée** : `VIEWS` liste
`connections · data · automations · settings · archive`, et une valeur inconnue
retombe sur `_DEFAULT_VIEW`. J'avais fabriqué l'URL moi-même, puis pris le repli
correct pour un défaut.

---

## 2. L'instrument était faux, et il l'était depuis quatre lots

Mon relevé de structure appelait `getBoundingClientRect()` sur tout `.vx-card`.
Pour un enfant de `<details>` fermé, Chromium rend ici une **hauteur non nulle** :
le relevé plaçait donc du contenu **invisible** parmi le contenu visible.

La seule vérification fiable est de remonter la chaîne des parents et de chercher
un `<details>` sans `open`.

### Ce que le bon instrument montre

| espace | titres **visibles** | titres **repliés** |
| --- | --- | --- |
| `/` | 7 | 0 |
| `/markets` | 4 | 3 |
| `/opportunities` | 4 | 2 |
| `/analysis` | 3 | 0 |
| `/portfolio` | 3 | 0 |
| `/options` | 5 | 0 |
| `/journal` | **1** | 3 |
| `/system` | **2** | 8 |

### Est-ce qu'un rapport déjà publié en dépendait ?

Vérifié, un par un :

- **Portefeuille** — la page ne contient **aucun** `<details>` ; l'ordre publié
  (603 / 746 / 1186 / 1436) est intact.
- **Options** — le doublon « Payoff à l'échéance » est hors de tout repli ;
  intact.
- **Opportunités** — j'ai publié une liste de titres « rendus » sans dire que
  **deux d'entre eux** (« Comparaison », « Classement Skyler (/40) ») sont
  derrière un repli. Ce n'est pas faux, c'est **imprécis** — et c'est corrigé
  ici.

---

## 3. Système est conforme, et je le dis sans le retoucher

`PAGES.md` §8 demande six rangs. Les cinq vues déclarées les couvrent :

| rang | vue |
| --- | --- |
| 1. Connexions IBKR / sources | `connections` |
| 2. Santé des données | `data` |
| 3. Fraîcheur / dernières mises à jour | `data` — « Fraîcheur par domaine » |
| 4. Paramètres UI | `settings` — Affichage, Application, Référence visuelle |
| 5. Archive / logs | `archive` |
| 6. Mode démo / offline | *voir §4* |

Le sous-titre a été corrigé au lot 07. **Rien d'autre ne méritait d'être
touché**, et forcer un changement pour que le lot « produise » aurait été le
contraire du travail.

---

## 4. Le constat que je refuse de corriger tout de suite

Serveur en `DEMO=1`, recherche d'une étiquette démo **visible** :

| espace | étiquette visible | mécanisme |
| --- | --- | --- |
| `/` · `/markets` | **oui** | hôte serveur rempli en JS |
| `/portfolio` · `/system` | **oui** | badge posé à l'exécution |
| `/options` | **non** | **l'hôte existe et reste vide** |
| `/opportunities` · `/analysis` · `/journal` | **non** | rien |

**Trois mécanismes coexistent**, et `/options` porte un hôte que rien ne remplit.

### Pourquoi je m'arrête là

Je n'ai **pas établi** que les quatre espaces silencieux servent des données
synthétiques. `/analysis` (accueil) et `/journal` affichent des données
**personnelles** venant du navigateur : y coller « démo » serait un mensonge
d'un autre genre. `/opportunities` affiche bien des données de scan et mérite
l'examen ; `/options` porte un hôte vide, ce qui est un signe.

Et une pièce ne colle pas : `/api/market/summary` répond `source: "cloud"`, pas
`"demo"`, alors que `DEMO=1`. **Le mode réellement actif n'est pas uniforme entre
les points d'entrée.** Toucher aux étiquettes avant d'avoir démêlé ça, c'est
étiqueter au jugé la chose même qui doit être exacte.

Le constat est donc **figé dans un test de caractérisation**
(`tests/test_signal_os_demo_visible_lot08.py`), sur le modèle de
`test_desk_perte_lot362.py` : il ne valide rien, il empêche la dérive silencieuse
et il porte sa propre date de péremption.

### Une confusion de plus, dans ce fichier même

Ma première table mélangeait deux comptes : occurrences dans la **source** (qui
contient l'hôte *et* le JS qui l'écrit) et dans le **HTML servi**. 3 vs 2, 4 vs 3.
Le test partait avec les mauvais nombres et échouait sur son premier lancement.
Corrigé, et la distinction est écrite dans le fichier.

---

## 5. Dette

- **Étiquetage démo** : à instruire avant correction (voir §4).
- Contenus non audités : Marchés (6 vues), Opportunités (rangs), Portefeuille
  (5 vues sur 6), Options (profil de lecture), Journal (6 rangs, 5
  visualisations).
- Analyse : fiche `/analysis/<ticker>` inaccessible ici.
- Aucun instrument ne détecte le **rognage silencieux**.
- **Palette : interface violette, graphiques cuivre.**
- DoD non vérifié : Escape, focus trap, palette de commandes, inventaire
  loading/empty/error/stale.

---

## 6. Suite

**Passe finale** — et d'abord la décision palette, qui conditionne la cohérence
des graphiques sur les huit espaces.
