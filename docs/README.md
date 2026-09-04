# Documentation Vertex

## Autorité

La seule doctrine active est le skill maître
[`.claude/skills/vertex-2-0/SKILL.md`](../.claude/skills/vertex-2-0/SKILL.md).
Aucun document de `docs/` ne le remplace, ne le complète ni ne le contredit.

Tout ce qui vit sous `docs/` est une **preuve** : un état mesuré à une date, sur
un SHA, avec ses limites. Une preuve peut justifier une décision ; elle ne peut
jamais autoriser un comportement que le skill interdit, ni faire croire qu'une
capacité absente est livrée.

## Carte du dossier

| Chemin | Rôle | Statut |
|---|---|---|
| [`ARBORESCENCE.md`](ARBORESCENCE.md) | audit du dépôt : propriétaire et preuve de consommation de chaque dossier | vivant |
| [`vertex-2-0/`](vertex-2-0/) | preuves du programme 2.0 en cours : rapports de lots, captures avant/après, audit 150 | vivant |
| [`vertex-1.0/`](vertex-1.0/) | contrats et archives techniques du runtime 1.0 (architecture, décisions, release) | vivant, référencé par les tests |
| [`refactor/`](refactor/) | journal de la refonte SKYLER : 665 rapports de lots + registres | archive, référencée par les tests |
| [`skyler/`](skyler/) | statut, baseline et convergence de branches SKYLER | archive, référencée par les tests |
| [`visual/`](visual/) | bibliothèque et registre de widgets | vivant, référencé par le code |
| [`archives/`](archives/) | rapports historiques sans consommateur : audits, couvertures, contrats périmés | archive |

## Où écrire une nouvelle preuve

- Un lot du programme 2.0 → `docs/vertex-2-0/lot-NN/RAPPORT.md`, avec ses
  captures 1600/1024/390 px à côté.
- Une décision d'architecture du runtime 1.0 → `docs/vertex-1.0/DECISIONS.md`.
- Rien de neuf ne va à la racine de `docs/` : la racine porte l'index et
  l'audit d'arborescence, pas les rapports.

## Ce que ces documents ne sont pas

Les chiffres, statuts, listes de pages et « GO » qu'ils contiennent décrivent le
commit de leur époque. Ils ne décrivent pas le commit courant. Avant de s'appuyer
sur l'un d'eux, remesurer sur le SHA candidat.
