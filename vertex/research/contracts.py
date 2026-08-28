"""vertex.research.contracts — contrats du laboratoire de stratégies (lot 12A).

`StrategySpec` fige TOUT ce qui définit une stratégie testable — univers
point-in-time, coûts, slippage, liquidité, périodes, seed, propriétaire —
et le condense en un manifeste immuable haché : deux specs identiques ont
le même hash, tout changement de paramètre en change le hash (aucun
changement silencieux possible, replay déterministe adressable).

`StrategyEvidence` porte le résultat avec ses métriques MINIMALES
obligatoires et un statut discipliné : `VALIDÉ_HORS_ÉCHANTILLON` exige la
preuve d'un walk-forward réussi (jamais un beau backtest seul).

`tableau_comparatif` refuse tout classement sur un ratio unique : les axes
minimaux (rendement, drawdown, exposition, turnover, coûts, échantillon,
stabilité) sont toujours co-présents.

Séparation stricte : ce module n'importe RIEN du conseil canonique
(advice/skyler_core/executive_engine) et réciproquement — gardien AST dans
tests/test_labo_strategies_lot12a.py. Aucun backtest ne modifie jamais un
AdviceResult.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field


class SpecError(ValueError):
    pass


class EvidenceError(ValueError):
    pass


#  Familles de recherche admises (chacune entre séparément, avec une thèse
#  économique — aucun catalogue activé par défaut).
FAMILLES = ('tendance/momentum', 'breakout', 'retour à la moyenne',
            'force relative', 'événement/catalyseur', 'factoriel/qualité',
            'volatilité/options', 'carry', 'paires/relatif', 'couverture')

SPEC_CHAMPS_REQUIS = (
    'strategy_id', 'version', 'famille', 'these', 'univers_point_in_time',
    'classe_actif', 'timeframe', 'signal_entree', 'sortie', 'invalidation',
    'sizing_theorique', 'contraintes', 'benchmark', 'calendrier_decision',
    'donnees_requises', 'couts', 'slippage', 'liquidite',
    'periode_entrainement', 'periode_validation', 'seed',
    'moteur_proprietaire')

STATUTS = ('EXPLORATOIRE', 'VALIDÉ_HORS_ÉCHANTILLON', 'DÉGRADÉ', 'REJETÉ')

#  Un ratio seul ne classe jamais une stratégie : ces axes sont TOUJOURS
#  co-présents dans l'évidence et dans le tableau comparatif.
METRIQUES_MINIMALES = ('rendement_annualise_pct', 'drawdown_max_pct',
                       'exposition_moyenne_pct', 'turnover_annuel',
                       'couts_annuels_pct')


@dataclass(frozen=True)
class StrategySpec:
    strategy_id: str
    version: str
    famille: str
    these: str
    univers_point_in_time: dict
    classe_actif: str
    timeframe: str
    signal_entree: str
    sortie: str
    invalidation: str
    sizing_theorique: str
    contraintes: dict
    benchmark: str
    calendrier_decision: str
    donnees_requises: list
    couts: dict
    slippage: dict
    liquidite: dict
    periode_entrainement: tuple
    periode_validation: tuple
    seed: int
    moteur_proprietaire: str

    def __post_init__(self):
        #  seed=0 est un seed VALIDE : le test d'absence compare par identité
        #  aux sentinelles vides, jamais par falsy (0 != None).
        manquants = [c for c in SPEC_CHAMPS_REQUIS
                     if getattr(self, c) in (None, '', [], {}, ())]
        if manquants:
            raise SpecError('champs requis absents: %s' % manquants)
        if self.famille not in FAMILLES:
            raise SpecError('famille hors catalogue: %r (admises: %s)'
                            % (self.famille, ', '.join(FAMILLES)))

    def manifest(self) -> dict:
        """Manifeste immuable de replay : contenu canonique + hash sha256.

        JSON à clés triées (déterministe) — le hash EST l'identité de
        l'essai ; tout changement de paramètre change le hash."""
        contenu = {c: getattr(self, c) for c in SPEC_CHAMPS_REQUIS}
        canonique = json.dumps(contenu, ensure_ascii=False, sort_keys=True,
                               default=list)
        return {'schema': 'strategy-spec/1.0',
                'manifest_hash': hashlib.sha256(
                    canonique.encode('utf-8')).hexdigest(),
                'contenu': contenu}


@dataclass
class StrategyEvidence:
    spec_manifest_hash: str
    statut: str
    population: int
    periode: tuple
    benchmark: str
    observations: int
    trades_theoriques: int
    metriques: dict
    stabilite: dict
    qualite_donnees: dict
    biais_connus: list = field(default_factory=list)
    preuves: dict = field(default_factory=dict)

    def __post_init__(self):
        if self.statut not in STATUTS:
            raise EvidenceError('statut inconnu: %r (admis: %s)'
                                % (self.statut, ', '.join(STATUTS)))
        absentes = [m for m in METRIQUES_MINIMALES
                    if (self.metriques or {}).get(m) is None]
        if absentes:
            raise EvidenceError('métriques minimales absentes: %s — un ratio '
                                'seul ne décrit jamais une stratégie' % absentes)
        if self.statut == 'VALIDÉ_HORS_ÉCHANTILLON':
            wf = (self.preuves or {}).get('walk_forward') or {}
            if wf.get('passed') is not True:
                raise EvidenceError(
                    'VALIDÉ_HORS_ÉCHANTILLON exige la preuve d\'un '
                    'walk-forward réussi (preuves.walk_forward.passed) — '
                    'un beau backtest historique ne suffit jamais')
        if not self.stabilite:
            raise EvidenceError('stabilité (régimes / sous-périodes) requise')


def tableau_comparatif(evidences, tri=None) -> dict:
    """Tableau de comparaison : les axes minimaux TOUJOURS co-présents.

    `tri` est refusé : classer sur un ratio unique est interdit par
    contrat — l'interprétation reste humaine, sur l'ensemble des axes."""
    if tri is not None:
        raise EvidenceError('classement sur un ratio unique interdit '
                            '(tri=%r refusé) : comparer sur tous les axes' % tri)
    lignes = []
    for ev in evidences or []:
        ligne = {m: ev.metriques.get(m) for m in METRIQUES_MINIMALES}
        ligne.update({'spec_manifest_hash': ev.spec_manifest_hash,
                      'statut': ev.statut, 'observations': ev.observations,
                      'population': ev.population, 'periode': ev.periode,
                      'benchmark': ev.benchmark, 'stabilite': ev.stabilite,
                      'biais_connus': list(ev.biais_connus)})
        lignes.append(ligne)
    return {'lignes': lignes, 'classement_par_ratio_unique': False,
            'note': ('comparaison multi-axes — aucun classement automatique ; '
                     'l\'interprétation reste humaine')}


__all__ = ['StrategySpec', 'StrategyEvidence', 'tableau_comparatif',
           'SpecError', 'EvidenceError', 'FAMILLES', 'SPEC_CHAMPS_REQUIS',
           'STATUTS', 'METRIQUES_MINIMALES']
