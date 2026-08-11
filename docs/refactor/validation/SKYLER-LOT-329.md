# SKYLER LOT 329 — Le lot 328 était-il un cas isolé ? Oui : SAIN, rien touché

Date : 2026-08-08 · Branche : `agent/skyler-v2-lot-329` (base : lot 328 fusionné,
2d67474) · **Aucun code modifié**

## La question

Le lot 328 a corrigé un texte affiché qui nommait `__DESK_KEYS`, symbole disparu
avec la purge É1. Question honnête : **est-ce le seul ?** Après avoir retiré
82 définitions, d'autres libellés pourraient citer des noms qui n'existent plus.

## La méthode — le texte RENDU, pas la source

Un scan du HTML brut ne suffit pas : une bonne part des libellés est écrite par
le JS après hydratation (les cartes du desk, les états, les compteurs). La
mesure est donc faite **dans le navigateur**, sur `document.body.innerText`, sur
**16 vues** : les 8 pages racines, la fiche `/analysis/NVDA`, les 3 sous-vues
Système (données, réglages, archive), Marchés → ampleur, Opportunités →
anomalies, Portefeuille → risque, Journal → track-record.

Sur ce texte, extraction des jetons qui ressemblent à un identifiant technique
(`snake_case` avec underscore, ou nom de fichier `.py`/`.js`/`.json`), puis
confrontation de chacun au code réel du dépôt.

## Le résultat

- **30 identifiants techniques** apparaissent dans le texte rendu des 16 vues.
- **0 introuvable dans le code.** Tous désignent quelque chose qui existe.

Le même scan sur le HTML statique (avant hydratation) donne également 0.

**`__DESK_KEYS` était donc un cas isolé**, et il est corrigé. Rien à toucher
ici — c'est le résultat que j'espérais, pas un pis-aller.

## Vérifications du cycle

- Anti-doublon : 0 trigger actif hors boucle.
- `integration/vertex-skyler-v2` à jour (tête = lot 328, 2d67474) ; arbre propre.
- Suite complète : **2501 passed / 2 skipped** — verte.
- MD5 des 8 pages **identiques aux références** (dont `/system` 73e917c0f2d0,
  la nouvelle du lot 328) ; `/sw.js` sert bien `td-shell-v187`.

## Décision SW

**Pas de bump** (`td-shell-v187`) : aucun octet servi modifié.

## Suite

**LOT 330 = échéance périodique** (8e mesure) : smoke complet + MD5 contre les
références + mini-bilan de la tranche 320-329.

Quatre dossiers attendent toujours une décision humaine : purge É2, purge É3,
les 24 fonctions du lot 326, les 5 modules `vertex/ui/` reliques du lot 327.
