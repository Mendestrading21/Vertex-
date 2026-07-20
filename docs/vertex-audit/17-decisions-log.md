# 17 — Journal des décisions

Décisions structurantes prises pour la refonte VERTEX MAXIMUM. Chaque entrée : décision · raison · conséquences.

## D-01 — Lecture seule STRICTE conservée (invariant absolu)
**Décision.** Vertex ne transmet **jamais** d'ordre (ni live, ni paper). La partie « Desk / Exécution » de la
mission est reformulée en centre de **PRÉPARATION + simulation + contrôles pré-trade** : sizing, perte max, impact
marge/risque, greeks, **ticket prêt-à-coller dans TWS**. L'humain transmet manuellement dans IBKR.
**Raison.** Invariant produit historique (`READONLY=True`, workers `readonly=True`, 17 outils interdits) ; choix
explicite de l'utilisateur (« Lecture seule stricte »).
**Conséquences.** Toutes les mentions « transmission/live/paper execution » de la mission → prep/sim. Aucun lot
n'introduit de chemin d'ordre. Gardiens conservés.

## D-02 — Fondation d'abord (docs + skill), implémentation ensuite
**Décision.** Cette session ne produit **que** le skill `vertex-maximum`, les agents auditeurs, les rules et le
dossier `docs/vertex-audit/`. **Aucun code applicatif touché.**
**Raison.** Choix utilisateur (« Fondation d'abord ») ; l'utilisateur exige de ne pas réécrire aveuglément.
**Conséquences.** 919 tests restent verts (garde-fou). L'implémentation se fera par lots vérifiés (Phase 2+).

## D-03 — Consolider l'existant, ne pas reconstruire
**Décision.** La mission suppose à tort un frontend React componentisé ; la réalité = monolithe Flask + `vertex/`.
On **consolide/combler/polit** (design system, provenance, nav, moteurs) au lieu de reconstruire.
**Raison.** Base mature et fonctionnelle (8 espaces, `VXCharts`, moteurs, IBKR read-only, 919 tests).
**Conséquences.** Roadmap = dette de cohérence à résorber, pas réécriture. Skills `vertex-redesign-*` conservés.

## D-04 — Une seule grammaire visuelle (Black Glass), docs périmés déclassés
**Décision.** Source de vérité design = `glass.css` (Black Glass, zéro bleu, violet=options). Les docs
`VERTEX_DESIGN_TOKENS`/`VERTEX_CHART_LIBRARY` (palette orange/bleu) sont **périmés** et à réaligner.
**Raison.** Contradiction constatée entre docs et runtime (DES-01) ; risque d'induire un contributeur en erreur.
**Conséquences.** MetricCard unique + `.vx-card` canonique + contrat de graphe. Sidebar inline orange de
`terminal.py` (CMP-03) à supprimer en Phase 3.

## D-05 — Nav canonique = `PRIMARY_NAV` (8 espaces)
**Décision.** `PRIMARY_NAV` (shell) fait autorité ; `vertex/ui/nav.py` (10 items legacy) est un vestige à absorber.
**Raison.** Double navigation (IA-01) = risque de liens divergents/morts.
**Conséquences.** Phase 3 : redirections des routes legacy vers les espaces canoniques, retrait de la nav legacy,
bump SW.

## D-06 — Provenance unique (`ProvenancedValue`) comme cible
**Décision.** Introduire à terme une enveloppe unique (value·source·timestamp·quality·latency·environment·
isEstimated·isDelayed·isStale·error) portée du moteur au footer.
**Raison.** Provenance aujourd'hui éclatée (DAT-02) ; règle produit n°4.
**Conséquences.** Chantier Phase 2/6 ; ne rien afficher sans provenance ; absence ≠ 0 (DAT-01, P0).

## D-07 — Sécurité de l'audit
**Décision.** Aucun secret ni identifiant de compte dans les docs/captures ; identité modèle jamais commitée ;
aucun nom personnel dans code/UI/docs.
**Raison.** Contraintes projet + sécurité.
**Conséquences.** Masquage systématique ; runtime gitignoré.
