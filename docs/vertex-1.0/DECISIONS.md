# Décisions actives — Vertex 1.0

| ID | Décision | Statut |
|---|---|---|
| D-001 | `main` est l'unique base de consolidation; aucune ancienne intégration n'est fusionnée en bloc. | active |
| D-002 | Nom produit unique: Vertex. « Skyler » reste un nom technique historique, pas une architecture parallèle. | active |
| D-003 | Entrée locale `python -m vertex`; WSGI `vertex.runtime:app`; `terminal.py` devient adaptateur. | active |
| D-004 | Options: 2/4/6 semaines, DTE préféré 120–240, cible 180. | active |
| D-005 | Actions: horizons 3/6/12 mois. | active |
| D-006 | WMB est contexte macro sourcé, jamais source de prix ou hard-gate override. | active |
| D-007 | TradingView demande une réévaluation, jamais une exécution. | active |
| D-008 | Un seul skill Claude: `/vertex-1-0`. | active |
| D-009 | Signal OS sera extrait composant par composant après comparaison, jamais fusionné globalement. | active |
| D-010 | Vertex 1.0 reste RC jusqu'à validation de tous les release gates sur le même SHA. | active |
| D-011 | Le runtime canonique active le corpus V4; le lancement direct de `terminal.py` conserve V3 uniquement comme rollback transitoire. | active |
| D-012 | Une capacité n'est « terminée » que si elle satisfait `QUALITY_STANDARD.md`. | active |
| D-013 | Les suppressions legacy suivent `CLEANUP_POLICY.md`; aucune suppression de masse aveugle. | active |
| D-014 | Sync du desk : **une clé omise par un push est conservée**, car aucun chemin du produit ne supprime une clé de localStorage — une absence est toujours un défaut de lecture. Supprimer se dit en envoyant la clé **vide**. Un instantané `desk_avantperte_*` est pris à la seconde dès qu'une clé est menacée. | active |
| D-015 | `performance_ledger` est **conservé**, pas supprimé. La preuve de non-usage existe (aucun chemin de production ne l'atteint), mais `CLEANUP_POLICY.md` exige **cinq** conditions et deux échouent : il n'a **aucun remplacement canonique en production** — rien d'autre n'implémente la discipline SIGNAL → ALERT → RECOMMENDATION → USER_DECISION → SIMULATED → REAL — et **trois fichiers de tests l'importent**. La vraie question n'est donc pas « le supprimer ? » mais « le brancher ? », et c'est une décision produit. | active |
| D-016 | Les 63 règles CSS **prouvées** inatteignables sont **recensées et gelées**, pas supprimées. Le plafond dans `tests/test_vertex_1_0_regles_mortes.py` **est** la « date de retrait » que `CLEANUP_POLICY.md` exige : il peut baisser, il ne peut pas monter en silence. La preuve a eu **trois trous** avant d'être fiable (corpus limité aux 8 espaces → 29 fausses preuves ; routes paramétrées absentes ; noms de classe assemblés à l'exécution) — ce qui justifie de garder la preuve reproductible plutôt que d'agir une fois. | active |
| D-017 | La preuve doit être reproductible **sur la machine où l'on décide**. Les gardiens ne comparent plus des chemins ni des octets dépendants de l'OS (séparateurs, CRLF, décodage cp1252 des sorties Node), et la disponibilité du navigateur se mesure par un **lancement réel**, jamais par la présence d'un fichier. Motif : sur Windows — la machine qui a TWS, donc celle où G5 se valide — la suite imposée par `CLAUDE.md` était rouge (25 échecs) et les gates navigateur G4 s'abstenaient partout, `_chromium()` ne connaissant que `/opt/pw-browsers/`. Une preuve qu'on ne peut pas rejouer là où l'on décide n'est pas une preuve. | active |
| D-018 | Un gardien de sécurité qui crie sur l'actualité ordinaire est désarmé. Le motif de clé d'API n'admet les tirets que derrière un préfixe d'émetteur (`sk-ant-`, `sk-proj-`) : une dépêche citant **SK Hynix** faisait virer le contrôle de fuite au rouge sur `/news-feed` à chaque passage. L'URL fautive est conservée dans le corps témoin SAIN, pour que le resserrement soit tenu. | active |
