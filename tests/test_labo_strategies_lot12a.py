"""tests/test_labo_strategies_lot12a.py — LOT 12A : labo de stratégies.

Bancs nés ROUGES : les contrats nommés StrategySpec/StrategyEvidence,
le manifeste immuable à replay déterministe et le tableau comparatif
anti-ratio-unique n'existent pas encore. Le gardien de séparation
(research ⟂ conseil canonique) est une caractérisation qui doit rester
vraie pour toujours.
"""
import ast
import os

import pytest


def _spec_kwargs(**over):
    d = dict(
        strategy_id='mom-01', version='1.0.0', famille='tendance/momentum',
        these='les gagnants persistants surperforment à 3-12 mois',
        univers_point_in_time={'source': 'sp500-constituents',
                               'as_of': '2020-01-01'},
        classe_actif='actions', timeframe='1d',
        signal_entree='clôture > MM200 et RS 12-1 > 70e percentile',
        sortie='clôture < MM200', invalidation='drawdown titre > 20 %',
        sizing_theorique='equal-weight 5 %', contraintes={'max_positions': 20},
        benchmark='SPY', calendrier_decision='mensuel, 1er jour ouvré',
        donnees_requises=['close ajusté', 'constituants datés'],
        couts={'commission_pct': 0.05}, slippage={'pct': 0.05},
        liquidite={'adv_min_usd': 5_000_000},
        periode_entrainement=('2010-01-01', '2017-12-31'),
        periode_validation=('2018-01-01', '2020-12-31'),
        seed=42, moteur_proprietaire='vertex.research.factory')
    d.update(over)
    return d


# ─────────────────────────────────── StrategySpec

def test_spec_refuse_un_champ_requis_absent():
    from vertex.research import contracts as C
    for champ in ('seed', 'benchmark', 'couts', 'slippage', 'liquidite',
                  'univers_point_in_time', 'periode_validation',
                  'moteur_proprietaire', 'invalidation'):
        kw = _spec_kwargs()
        kw[champ] = None
        with pytest.raises(C.SpecError):
            C.StrategySpec(**kw)


def test_spec_refuse_une_famille_hors_catalogue():
    from vertex.research import contracts as C
    with pytest.raises(C.SpecError):
        C.StrategySpec(**_spec_kwargs(famille='martingale'))


def test_manifest_deterministe_meme_spec_meme_hash():
    from vertex.research import contracts as C
    a = C.StrategySpec(**_spec_kwargs()).manifest()
    b = C.StrategySpec(**_spec_kwargs()).manifest()
    assert a['manifest_hash'] == b['manifest_hash']
    assert len(a['manifest_hash']) == 64          # sha256 hex


def test_manifest_change_si_un_parametre_change():
    from vertex.research import contracts as C
    a = C.StrategySpec(**_spec_kwargs()).manifest()
    b = C.StrategySpec(**_spec_kwargs(seed=43)).manifest()
    assert a['manifest_hash'] != b['manifest_hash'], (
        'changement silencieux de paramètre = interdit — le hash doit bouger')


# ─────────────────────────────────── StrategyEvidence

def _evidence_kwargs(**over):
    d = dict(
        spec_manifest_hash='0' * 64, statut='EXPLORATOIRE',
        population=480, periode=('2018-01-01', '2020-12-31'), benchmark='SPY',
        observations=756, trades_theoriques=120,
        metriques={'rendement_annualise_pct': 8.2, 'drawdown_max_pct': -18.4,
                   'exposition_moyenne_pct': 72.0, 'turnover_annuel': 1.4,
                   'couts_annuels_pct': 0.6, 'volatilite_pct': 14.1},
        stabilite={'regimes': {'TREND': 0.6, 'CHOP': -0.1},
                   'sous_periodes_positives': '2/3'},
        qualite_donnees={'trous': 0, 'survivorship_controle': True},
        biais_connus=['période courte'], preuves={})
    d.update(over)
    return d


def test_evidence_refuse_un_statut_inconnu():
    from vertex.research import contracts as C
    with pytest.raises(C.EvidenceError):
        C.StrategyEvidence(**_evidence_kwargs(statut='PARFAIT'))


def test_valide_hors_echantillon_exige_un_walk_forward_reussi():
    from vertex.research import contracts as C
    with pytest.raises(C.EvidenceError):
        C.StrategyEvidence(**_evidence_kwargs(statut='VALIDÉ_HORS_ÉCHANTILLON'))
    ok = C.StrategyEvidence(**_evidence_kwargs(
        statut='VALIDÉ_HORS_ÉCHANTILLON',
        preuves={'walk_forward': {'passed': True, 'total_folds': 5,
                                  'positive_folds': 4}}))
    assert ok.statut == 'VALIDÉ_HORS_ÉCHANTILLON'


def test_evidence_refuse_metriques_minimales_absentes():
    from vertex.research import contracts as C
    kw = _evidence_kwargs()
    del kw['metriques']['drawdown_max_pct']
    with pytest.raises(C.EvidenceError):
        C.StrategyEvidence(**kw)


# ─────────────────────────────────── comparaison anti-ratio-unique

def test_tableau_comparatif_porte_toujours_les_axes_minimaux():
    from vertex.research import contracts as C
    ev = C.StrategyEvidence(**_evidence_kwargs())
    t = C.tableau_comparatif([ev])
    ligne = t['lignes'][0]
    for axe in ('rendement_annualise_pct', 'drawdown_max_pct',
                'exposition_moyenne_pct', 'turnover_annuel',
                'couts_annuels_pct', 'observations', 'statut'):
        assert axe in ligne, axe
    assert t['classement_par_ratio_unique'] is False


def test_tableau_refuse_un_tri_sur_ratio_unique():
    from vertex.research import contracts as C
    ev = C.StrategyEvidence(**_evidence_kwargs())
    with pytest.raises(C.EvidenceError):
        C.tableau_comparatif([ev], tri='sharpe')


# ─────────────────────────────────── séparation conseil canonique

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CANONIQUE = ('vertex.engines.advice', 'vertex.engines.skyler_core',
              'vertex.strategy.executive_engine')


def _imports_de(chemin):
    with open(chemin, encoding='utf-8') as f:
        arbre = ast.parse(f.read())
    noms = set()
    for n in ast.walk(arbre):
        if isinstance(n, ast.Import):
            noms.update(a.name for a in n.names)
        elif isinstance(n, ast.ImportFrom) and n.module:
            noms.add(n.module)
    return noms


def test_le_labo_n_importe_jamais_le_conseil_canonique():
    dossier = os.path.join(_RACINE, 'vertex', 'research')
    for base, _, fichiers in os.walk(dossier):
        for f in fichiers:
            if not f.endswith('.py'):
                continue
            imports = _imports_de(os.path.join(base, f))
            for interdit in _CANONIQUE:
                assert not any(i == interdit or i.startswith(interdit + '.')
                               for i in imports), (f, interdit)


def test_le_conseil_canonique_n_importe_jamais_le_labo():
    for mod in ('vertex/engines/advice.py', 'vertex/engines/skyler_core.py',
                'vertex/strategy/executive_engine.py'):
        chemin = os.path.join(_RACINE, mod)
        if not os.path.exists(chemin):
            continue
        imports = _imports_de(chemin)
        assert not any(i == 'vertex.research' or i.startswith('vertex.research.')
                       for i in imports), mod


def test_seed_zero_est_un_seed_valide_pas_une_absence():
    from vertex.research import contracts as C
    spec = C.StrategySpec(**_spec_kwargs(seed=0))
    assert spec.manifest()['contenu']['seed'] == 0
