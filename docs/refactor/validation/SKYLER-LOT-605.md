# SKYLER — LOT 605 · LES SEPT DÉPÔTS, LUS — ET CE QU'ILS ONT VRAIMENT DONNÉ

L'humain a cité sept dépôts GitHub et écrit « prend tout ce quil ya a prendre
pour le devloper au max ». Aucun n'avait été ouvert. Ce lot les lit tous.

## La réponse courte : il n'y a rien à *prendre*, et ça valait quand même le voyage

**Cinq des sept dépôts n'ont AUCUNE licence.** Sans licence, le droit d'auteur
par défaut s'applique : tous droits réservés. **Ils ne sont pas copiables**,
quelle que soit leur qualité.

| dépôt | pile | licence | taille |
| --- | --- | --- | --- |
| `khushi2706/finhub-…-mern-nextjs` | Next.js / MERN | **aucune** | 4,1 Mo |
| `rohitgulam/Finhub-HTML-CSS-JS` | HTML / CSS / Vue | **aucune** | 576 ko |
| `mechanic-power/finance_ts` | **Elixir** | MIT | 548 ko |
| `VVVleng/TD-Rotman-FinHub-…` | Python / notebooks | **aucune** | 45 Mo |
| `SharipovSherzodbek/FinHubService` | **C# / .NET** | MIT | 464 ko |
| `lumoraesf/Finhub` | Python (3 fichiers) | **aucune** | 208 ko |
| `medeupazylov/StockApp` | **iOS** Obj-C / Swift | **aucune** | 4,4 Mo |

Les **deux seuls dépôts licenciés** (MIT, donc copiables) sont en **C#/.NET** et
en **Elixir** — deux piles sans rapport avec un monolithe Flask. **L'intersection
« légalement copiable » ∩ « techniquement transposable » est vide.**

## Ce qu'ils ont donné quand même : une question

`lumoraesf/Finhub` — **le plus petit des sept, 3 fichiers** — branche deux
sources de news et **déduplique par titre exact** avant de scorer. En lisant ces
quinze lignes, une question s'est posée : *et Vertex, il déduplique comment ?*

**Vertex faisait pire.**

## Le défaut trouvé chez nous, corrigé

`terminal.py::_news_loop` alimente `/news-feed`, les 45 dépêches du produit :

```python
k = (it.get('title') or '')[:60]
if k and k not in seen:
```

**Une clé sur les 60 premiers caractères du titre brut.** Deux erreurs opposées,
toutes deux réelles :

| erreur | mécanisme | conséquence |
| --- | --- | --- |
| **faux positif** | deux dépêches **différentes** partageant leur ouverture — cas courant en finance, où les titres commencent par une formule figée | **la seconde est JETÉE : de l'information réelle disparaît du fil** |
| **faux négatif** | le même article, même lien, titre en casse ou ponctuation différente selon le fournisseur | **il passe deux fois** |

Et le plus dur à admettre : **`news_plus.dedupe_news()` existe dans le dépôt
depuis le lot 4**, est testé, et clé sur le **titre normalisé complet + le lien**.
**Le fil de news ne l'appelait simplement pas.**

### La preuve du mécanisme

| cas | dédup d'avant | `dedupe_news()` | attendu |
| --- | --- | --- | --- |
| « La Réserve fédérale maintient ses taux directeurs inchangés et **signale une baisse en juin** » / « …et **écarte toute baisse cette année** » | **1** — une dépêche perdue | **2** | 2 |
| « Nvidia beats on revenue, raises outlook » / « NVIDIA BEATS ON REVENUE - RAISES OUTLOOK » (même lien) | **2** — doublon servi | **1** | 1 |

**Un faux positif, un faux négatif, zéro erreur du dédupeur canonique.**

Ce banc prouve le **mécanisme**, pas une fréquence : **aucun corpus de news réel
n'est disponible hors ligne**, et je ne prétends donc rien sur le nombre de
dépêches perdues en production.

*Détail honnête* : mon **premier** cas de faux positif ne collisionnait pas —
« relève » et « abaisse » divergent avant le 60ᵉ caractère. Le banc me l'a dit,
le cas est conservé tel quel dans le rapport comme témoin d'un piège trop
optimiste.

### Le gardien, vérifié par mutation

`tests/test_fil_news_dedupe_lot605.py` — **6 tests**. Sur le code d'avant,
**3 échouent** (le fil n'appelle pas le dédupeur, il clé sur une troncature, et
l'ordre dédup/tri n'existe pas). Un gardien qui passerait sur les deux versions
ne vérifierait rien (**591-C**).

## Les deux arrêts du lot

**1. Mon anti-doublon a compté à vide.** J'ai lu la clé `triggers` d'une charge
qui expose `data`, obtenu `total 0 · actifs 0`, et failli le publier. Le vrai
compte : **5 réveils, tous `run_once_fired`, 0 actif**. Un compteur qui répond
zéro parce qu'il regarde au mauvais endroit est **600-A** dans sa forme la plus
simple. *(Au passage : le « total 100 » que mon propre brief annonçait comme
attendu était un artefact de `limit`, pas une mesure. Le brief est une source
comme une autre.)*

**2. Mon périmètre de recherche excluait `terminal.py`.** J'ai cherché les
appelants de `sentiment()` dans `vertex/` seulement, n'en ai trouvé aucun, et
**conclu que `/news-feed` publiait un agrégat structurellement nul**. Faux :
l'appel est à `terminal.py:1172`. **Le monolithe est le plus gros fichier de
production du projet et mon instrument l'ignorait.** Interprétation retirée
avant publication.

*(Et la mesure qui devait trancher — appeler `/news-feed` — a d'abord répondu
sur **0 item**, donc `sentiment: {}`. Un contrôle qui « confirme » sur un
ensemble vide ne confirme rien.)*

## Le piège, écrit avant d'ouvrir un dépôt — réfuté quatre fois sur quatre

| volet | énoncé | verdict |
| --- | --- | --- |
| **(a)** | « au moins un des 7 contient du code directement prenable » | **RÉFUTÉ** — et pour une raison non prévue : **la licence**, pas la technique |
| **(b)** | « les dépôts nommés Finhub partagent une base commune » | **RÉFUTÉ** — 7 piles différentes, et **seuls 4 sur 7 mentionnent Finnhub** ; trois « Finhub » ne le citent jamais |
| **(c)** | « le plus gros dépôt est le plus utile » | **RÉFUTÉ** — 45 Mo dont **14 Mo de présentation et 4,2 Mo de PDF** ; le plus utile fut **le plus petit** |
| **(d)** | « la valeur sera dans le CODE » | **RÉFUTÉ** — la valeur fut **une question**, qui a mené à un défaut de Vertex |
| **global** | | **RÉFUTÉ 4 / 4** |

**Un piège entièrement réfuté et un lot qui livre quand même un correctif
prouvé** : les deux ne sont pas liés, et c'est bien ainsi.

## Second contrôle (481) — le cas que l'instrument exclut

L'instrument mesurait **le contenu des 7 dépôts**. Le cas exclu : **ce que
Vertex a déjà**.

`lumoraesf` déduplique par **titre exact dans un `set`** ;
`news_plus.dedupe_news()` déduplique par **titre normalisé (casse, ponctuation,
espaces) + lien**. **Le dépôt de référence est moins bon que notre propre code.**
Sans ce contrôle j'aurais pu importer une régression en croyant emprunter une
amélioration.

## Ce que le lot n'établit pas

- **Combien de dépêches sont réellement perdues en production.** Le mécanisme
  est prouvé, la fréquence non — pas de corpus hors ligne.
- **Que `VVVleng` soit sans valeur.** Son dictionnaire **Loughran–McDonald**
  (lexique de sentiment financier académique, ~2 300 termes négatifs) est
  autrement plus riche que nos **22 mots positifs / 22 négatifs**. Il est
  **nommé, non pris** : redistribué dans un dépôt sans licence, et sa propre
  licence d'origine mérite une décision humaine avant tout usage produit.
  *Ce n'est pas un oubli, c'est un refus motivé.*
- Que les autres consommateurs de news (`events.build`, `skyler_sweep`)
  n'aient pas leur propre déduplication faible : `events.py` importe bien
  `dedupe_news`, les autres n'ont pas été audités.
- Que le sentiment lexical de Vertex soit bon. Il est **ternaire** (`+1/-1/0`
  sur un simple `pos > neg`) : trois mots positifs valent un seul. Nommé,
  non traité.

## Règles neuves

- **605-A — UN DÉPÔT SANS LICENCE N'EST PAS UNE RESSOURCE, QUELLE QUE SOIT SA
  QUALITÉ.** Cinq des sept sont dans ce cas. La première question à poser d'un
  code qu'on envisage de reprendre n'est pas « est-il bon ? » mais « ai-je le
  droit ? ».
- **605-B — LA VALEUR D'UNE LECTURE EXTÉRIEURE EST SOUVENT LA QUESTION, PAS LE
  CODE.** Quinze lignes d'un dépôt de trois fichiers ont fait trouver un défaut
  dans le nôtre. Aucune ligne copiée, un correctif livré.
- **605-C — UN PÉRIMÈTRE DE RECHERCHE QUI EXCLUT LE MONOLITHE CONCLUT FAUX.**
  `terminal.py` porte du code de production ; chercher un appelant dans
  `vertex/` seulement produit des « jamais appelé » qui n'existent pas.

## Le troisième arrêt — un accent manquant a réintroduit un nom interdit

`tests/test_namespace_guards.py` a **refusé le commit**. Le motif interdit
Le motif dormait dans le mot **« amélioration »** — mais **privé de son accent**,
comme l'exige le style non accentué des lignes d'INDEX. Accentué, le mot ne
contient pas le motif ; désaccentué, si.

Le gardien a raison sur le fond — il ne peut pas savoir que c'est un mot commun —
et **le coût du faux positif est nul comparé au risque qu'il couvre**. Ligne
reformulée.

**Arrêtés avant publication : 236 → 237.**

## Ce que le dépôt fait bien

- **`dedupe_news()` était déjà écrit, déjà testé, déjà correct** depuis le
  lot 4. Le défaut n'était pas une absence de solution mais un câblage manquant —
  et le correctif tient en une ligne parce que le bon outil existait.
- **`news_plus.dedupe_news` bat le dépôt de référence** sur les trois cas.
- **Le pipeline de sentiment est intact** : `senti` posé sur chaque item,
  `aggregate()` le lit. Mon accusation de « zéro structurel » était fausse.

## Cycle

- Anti-doublon : **5 réveils, tous `run_once_fired`, 0 actif** *(page 1 ; le
  jeton `has_more` n'a pas été suivi — seul le compte des actifs est établi)*.
- **1 fichier de production** : `terminal.py` (`_news_loop`).
- **1 gardien neuf** : `tests/test_fil_news_dedupe_lot605.py`, **6 tests**,
  **vérifié par mutation** (3 rouges sur le code d'avant).
- MD5 des 8 pages : **8 / 8 identiques** — le correctif est côté serveur, aucun
  octet servi ne change, **donc aucun bump** : SW inchangé à `td-shell-v190`.
- Sondes : snapshot **pris avant, restauré après — écart final AUCUN**.
- Suite : **2870 passed / 0 skipped** *(2864 + les 6 du gardien neuf)*.
- **READONLY intact** · aucun octet copié d'un dépôt tiers.

## Comptes

- Arrêtés avant publication : **238 (+3)**
- Publiés puis corrigés : **40**
- Interprétations retirées : **15 (+1)**
- **Dossiers produit corrigés : 4**
