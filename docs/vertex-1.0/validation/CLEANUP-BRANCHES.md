# #782 — 697 branches : lesquelles peut-on perdre sans rien perdre ?

Instrument : `tools/vertex_1_0/mesurer_branches.py` — **il ne supprime rien**
Gardien : `tests/test_vertex_1_0_branches.py` (5 tests)
Mesure figée : `docs/vertex-1.0/inventory/branches.json`

---

## Le résultat

```text
697 branches distantes
 31  FUSIONNEE          tous les commits sont dans main — perte NULLE prouvée
  1  CONTENU_IDENTIQUE  commits inédits, mais diff vide
 51  CONTENUE_AILLEURS  une autre branche la contient entièrement
614  UNIQUE             contient du travail que main n'a pas

694 arbres distincts sur 697
```

**32 branches sont supprimables sur preuve**, et 51 de plus le sont tant que la
branche qui les contient survit.

## Ce que la mesure a réfuté

Je m'attendais à ce que la série Skyler V2 — 623 branches `lot-*` — soit une
**chaîne linéaire** : `lot-120` contenant `lot-119`, et ainsi de suite. Les
compteurs le suggéraient fortement : 274, 275, 276, incrémentés de 1 d'un lot au
suivant. Si l'hypothèse tenait, une seule branche — la pointe — aurait suffi à
tout conserver, et 622 auraient été supprimables d'un coup.

Vérifié directement :

```text
git merge-base --is-ancestor lot-100 lot-101   →  ÉCHOUE
```

Les branches ont été **refaites**, pas empilées. Le regroupement par arbre le
confirme : **694 contenus distincts sur 697**, et seulement trois paires
byte-identiques :

```text
skyler-v2-lot-601 = integration/vertex-skyler-v2
skyler-v2-lot-625 = agent/vertex-total-rebuild-obsidian-v2
vertex-1-0-governance = main
```

**Il n'y a donc pas de collapse facile.** Les 614 branches portent réellement 614
états différents du dépôt. C'était l'hypothèse séduisante, et elle était fausse ;
la vérifier a évité de supprimer 622 branches en croyant qu'une seule les
contenait.

## Ce que l'outil ne dit pas, et ne dira jamais

Il ne dit pas si une branche `UNIQUE` **mérite** d'être gardée. Un travail inédit
peut être abandonné, remplacé par mieux, ou simplement faux — et c'est le cas de
toute la série Skyler V2, que `CLAUDE.md` et `DECISIONS.md` (D-001, D-009)
qualifient d'historique et interdisent comme base.

Cette lecture-là demande un humain. C'est exactement le partage que
`CLEANUP_POLICY.md` prévoit : la machine produit la preuve, la personne décide.

## Le témoin qui compte le plus

Une classification qui range **l'inconnu du côté rassurant** est plus dangereuse
que pas de classification : elle délivrerait un permis de supprimer sur une
preuve qui n'existe pas. Le témoin négatif vérifie donc qu'une référence
fabriquée ressort `INACCESSIBLE`, jamais `FUSIONNEE`.

Un test vérifie aussi que **l'instrument ne sait pas supprimer** — pas de
`push --delete`, pas de `branch -D`. Un outil de nettoyage qui peut supprimer est
un outil qui supprimera ; la preuve et l'acte restent séparés.

## Une leçon d'outillage

La première version du gardien appelait la mesure complète et prenait **77 s** —
plus que toute la suite. Un gardien lent finit désactivé, et un gardien désactivé
ne garde rien. La passe coûteuse (614 `git branch --contains`) est devenue
optionnelle : elle reste dans le rapport, elle sort du chemin des tests.

## Recommandation, et décision humaine

Ce que je recommanderais — et que **je ne fais pas** :

1. **supprimer les 32 branches prouvées sans perte** — geste sûr, mesuré,
   réversible tant que `main` existe ;
2. **statuer en bloc sur les 623 `agent/skyler-v2-lot-*`** : la gouvernance les
   déclare déjà historiques et interdites comme base. Les garder coûte un dépôt
   que plus personne ne sait lire ; les supprimer perd 623 états distincts d'un
   travail abandonné. Un compromis existe : conserver les quelques pointes
   nommées dans `DECISIONS.md` et laisser partir le reste.

**HUMAN_REQUIRED** — toute suppression est irréversible côté distant. Je ne
supprimerai rien sans instruction explicite.
