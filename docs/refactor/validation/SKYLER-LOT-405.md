# SKYLER LOT 405 — Aucun octet mort dans `/static` : 54 sur 54 réellement référencés

Date : 2026-08-09 · Branche : `agent/skyler-v2-lot-405` (base : lot 404 fusionné,
36f4120)

Balayage AST/textuel, quelques secondes. **Aucun code, aucun gardien, aucun test
ajouté.**

## Pourquoi cette question, et pourquoi elle compte

Le service worker met en cache **tout `/static`** (règle n°3 de `CLAUDE.md`). Un
fichier statique mort n'est donc pas seulement du poids dans le dépôt : ce sont
des octets **téléchargés et conservés sur l'appareil de l'utilisateur**, et une
entrée de plus dans l'empreinte que le gardien du lot 361 doit suivre.

```text
vertex/static/  →  54 fichiers · 824 Ko
                   34 .js · 17 .css · 2 .woff2 · 1 .md
```

## L'instrument, validé avant emploi

Recherche du **nom de base** de chaque fichier dans tout le texte du dépôt
(1 218 fichiers). Volontairement **large** — `<script src>`, `url()` CSS,
`@import`, chaîne Python composant le chemin : chercher un chemin exact aurait
fabriqué de faux morts.

**Témoin positif** : un fichier `zz-temoin-mort-405.css` déposé dans
`vertex/static/vertex/css/`, référencé nulle part.

```text
JAMAIS cité, nulle part            1
   vertex/static/vertex/css/zz-temoin-mort-405.css      29 o
```

Seul le témoin est signalé ; **aucun des 54 fichiers réels**. Témoin supprimé
immédiatement, arbre vérifié propre.

## Le résultat — et ce qui le rend substantiel plutôt que décoratif

Un « 0 mort » obtenu par une recherche large serait faible : un fichier peut être
« cité » dans une note de documentation sans être servi. Trois raffinements ont
donc été appliqués.

```text
fichiers statiques                                        54
   cités depuis la PRODUCTION (vertex/**, terminal.py)    54
   cités seulement depuis un AUTRE fichier static          0
   cités seulement dans docs/ ou tests/                    0
   cités NULLE PART                                        0
```

Puis le contrôle de **second ordre**, celui qui distingue vraiment : un fichier
référencé uniquement par un module lui-même mort est mort par transitivité.
`CLAUDE.md` et les lots 327/381 nomment six modules de `vertex/ui/` sans aucun
consommateur en production (`options_lab`, `journal`, `vault`, `signals`,
`strategy_os`, `vx_kit`).

```text
302 modules de production examinés (dont 6 connus morts)
fichiers statiques cités UNIQUEMENT par un module mort :  0
```

**Les 54 fichiers sont donc tous atteints depuis du code vivant.** Le zéro tient
après trois filtres successifs — c'est un zéro substantiel.

## Ce que ce lot dit du dossier « code mort »

Le poids mort identifié par les lots précédents est **dans le monolithe Python**,
pas dans les octets servis : 604 Ko de `PAGE_*` jamais servis (374), `vx_kit.JS`
qui n'atteint aucune page (381), cinq modules reliques (327). Le répertoire
`/static`, lui, est **propre**.

C'est une information utile pour arbitrer les dossiers de rang 3 : inutile d'y
chercher un gain de poids côté assets — il n'y en a pas.

## Vérifications du cycle

- Anti-doublon : `total 100 · actifs 0`. `pwd` vérifié avant toute mesure.
- **Aucun fichier touché** — le témoin créé par la sonde a été supprimé par la
  sonde, `git status` vide de bout en bout. Pas de preuve MD5 requise, pas de
  bump, empreinte SW inchangée. SW : `td-shell-v187`.
- Snapshot des 22 fichiers runtime avec contrôle d'apparition ; la suite a
  ré-horodaté les trois fichiers habituels, restaurés. Écart final **aucun**,
  aucun fichier apparu.
- Suite : **2864 passed / 0 skipped**, inchangée.

## Portée

La recherche est **textuelle par nom de base**. Elle prouve qu'un nom apparaît
dans du code vivant ; elle ne prouve pas que la ligne qui le contient soit
**exécutée** — une balise `<script src>` construite dans une branche jamais
empruntée compterait comme vivante. Pour aller plus loin il faudrait relever les
requêtes réelles d'un navigateur sur les 8 pages, ce qui suppose de lancer le
serveur DEMO — donc de fabriquer un point dans `breadth_history.json`. Le coût
n'en vaut pas la peine pour confirmer un zéro déjà filtré trois fois.

## Où en est la boucle

Dixième lot court, dixième point de contrôle distinct. Trois lots d'affilée
(403, 404, 405) sont revenus négatifs — mais chacun avec un dénominateur mesuré
et un instrument prouvé, et chacun a fermé une question qui, jusque-là, n'avait
jamais été posée.

La question du **bilan n°9 (lot 400) attend toujours une réponse** : aucun GO
depuis le lot 388, tous les dossiers de rang 1 à l'arrêt.
