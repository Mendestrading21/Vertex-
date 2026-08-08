# SKYLER LOT 326 — Trois pistes instruites : deux saines, une laissée à l'humain

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-326` (base : lot 325 fusionné,
7f18796) · **Aucun code modifié**

Après les imports (lots 324-325), trois pistes de code mort restaient ouvertes.
Elles sont mesurées ici **avant** toute intervention. Deux sont closes saines ;
la troisième est un dossier que je n'ai pas le droit de trancher seul.

## (a) Fichiers statiques CSS/JS non référencés — SAIN

51 fichiers dans `vertex/static/vertex/**` (`.css` + `.js`), chacun cherché par
nom de base dans tout le dépôt (`*.py`, `*.js`, `*.html`, `*.css`, `*.json`,
en excluant le fichier lui-même).

**0 fichier non référencé.** Rien à retirer.

## (b) Routes définies mais jamais appelées — SAIN

**186 routes** dans `app.url_map` (hors `/static`). Pour chacune, le préfixe
statique (avant le premier `<param>`) est cherché dans le code qui construit
l'interface : JS statique, `vertex/ui/**`, `vertex/app/**`, `terminal.py`.

**0 route orpheline.** Toute route servie a un appelant dans le produit.

## (c) Fonctions top-level jamais citées — DOSSIER OUVERT, rien touché

L'analyse trouve **24 fonctions / 258 lignes** définies dans `vertex/` et
citées nulle part ailleurs dans le dépôt (tests inclus), décorateurs exclus
(une fonction décorée est appelée par le framework) :

| famille | fonctions | lignes |
|---|---|---|
| `data_sources` | 9 | 110 |
| `research` | 5 | 53 |
| `scanner` | 1 | 31 |
| `anomalies` | 2 | 25 |
| `observability` | 3 | 22 |
| `strategy` | 4 | 17 |

**Je ne retire rien, et c'est la bonne décision.** Le gros du lot
(`data_sources`, 9 fonctions) est constitué de **façades d'intégration IBKR** :
`fetch_positions`, `fetch_snapshot`, `fetch_daily_bars`, `fetch_expirations`,
`fetch_contract_details`, `qualify_stock`, `validate_option_contract`… Ces
fonctions sont le **chemin de lecture du compte réel via TWS**. « Jamais citée
dans le dépôt » ne veut pas dire « morte » : cela peut vouloir dire « point
d'entrée d'une intégration qui n'est pas encore recâblée », et les supprimer
serait détruire le travail d'intégration, pas nettoyer.

C'est la leçon du lot 325 (`BROKER` dans `services/startup.py`) appliquée à
plus grande échelle : **un compteur ne distingue pas le mort de l'endormi.**

Trancher ce dossier demande une décision produit, pas une analyse statique :
pour chaque famille, la question est « cette porte sert-elle encore ? ». Elle
appartient à l'utilisateur, comme É2 et É3 de la purge.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 325, 7f18796) ; arbre propre.
- Suite complète : **2501 passed / 2 skipped** — verte.

## Décision SW

**Pas de bump** (`td-shell-v186`) : aucun code touché, docs seulement. Les MD5
des 8 pages n'ont pas besoin d'être re-mesurés — rien n'a changé.

## Suite

LOT 327 : veille active. Trois dossiers attendent une décision humaine — purge
É2, purge É3, et les 24 fonctions ci-dessus. Prochaine échéance périodique :
~lot 330.
