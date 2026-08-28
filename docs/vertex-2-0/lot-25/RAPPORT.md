# Lot 25 — Dettes consignées soldées (RAPPORT)

Date : 2026-08-28 · Autorisation utilisateur : exécution complète

## Livré

1. **Signatures sans courtier** : le paramètre `ibkr_positions` et la
   branche morte qui aurait fabriqué des positions IBKR sont RETIRÉS de
   `repository.load_positions`, `recalculator.recalculate_all` et
   `detector.startup_position_report` (tous les appelants passaient déjà
   None depuis le lot 2). `tests/test_signatures_sans_ibkr_lot25.py`.
2. **Vie privée du copilote** (contrat IA « portefeuille exclu par défaut,
   minimisé après action explicite ») : positions déclarées ET post-mortem
   ne partent dans le prompt QUE si la case « Inclure mes positions
   déclarées » est cochée (décochée par défaut, dans les DEUX panneaux —
   dossier Analyse et GEX). L'exclusion est DITE au modèle
   (`NON_TRANSMISES…`) — sans quoi Claude conclurait « aucune position »,
   un mensonge. Le repli déterministe ne compte jamais la chaîne
   d'exclusion. `tests/test_copilote_pii_lot25.py` (5 bancs) ; bancs
   historiques réécrits vers le contrat cible.
3. **Correction de multiplicité** (pipeline anti-illusion, point 10) :
   `vertex/research/multiplicity.py` (seuil de Bonferroni + `jugement()`
   honnête nommant la correction) et `ExperimentRegistry.n_essais()`
   (essais TENTÉS, rejetés compris). `tests/test_multiplicite_lot25.py`.
4. **ADR** : le registre d'essais reste en mémoire — critères de révision
   écrits (`ADR-REGISTRE-EN-MEMOIRE.md`).
5. **VX2-DESIGN-02 soldé** : 41 jetons `:root` portaient DEUX valeurs
   (tokens.css gardait l'ancienne marque olive #84aa31…, corrigée
   seulement par cascade). tokens.css est aligné sur la valeur SERVIE
   (iso-visuel prouvé : la valeur calculée finale ne change pas) ; gardien
   permanent `tests/test_jetons_sans_conflit_lot25.py` (un jeton = une
   valeur hors media et hors couche finale, les redéfinitions scopées
   restant des thèmes légitimes). Le résolveur de la page Design System
   suit désormais la cascade réelle (multi-feuilles, multi-sauts).
6. **VX2-DESIGN-03 mesuré et clos** : les hex « en dur » restants sont
   LÉGITIMES — définitions d'alias de jetons, thème JS canvas
   (propriétaire déclaré côté JS, un canvas ne lit pas var() à la
   peinture), et motif `cssv('--vx-…', fallback)`. Les 2 seuls littéraux
   de page convertibles (briefing) passent à `var(--vx-ink)`.

Service worker **v269**, épingles + empreinte /static suivies.

## Preuves

Suite complète : **4379 passés · 152 ignorés · 0 échec** (141 s).

## Dettes restantes (les DEUX grosses, nommées — pas absorbables sans
programme dédié)

- Strangler complet de `terminal.py` (~7000 lignes, doubles écrivains
  myRecos/myFavs/myNotes) — programme à part entière.
- Refonte de la file worker IBKR unique (corps du lot 6 historique).
