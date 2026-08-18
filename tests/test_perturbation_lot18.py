"""tests/test_perturbation_lot18.py — SKYLER LOT 18 : analyse de perturbation.

Le facteur `robustness` de la confiance cesse d'être un proxy (blocs
insuffisants) : le moteur RE-DÉCIDE sous une liste FIXE et déterministe de
variations documentées des entrées (score technique ±10, R:R ±0,5, confiance
du régime ±0,2, un contexte retiré à la fois) et la robustesse devient la
fraction des perturbations applicables qui laissent la décision inchangée —
avec la liste exacte de celles qui la font basculer. Aucun aléatoire.
Changement de règle = changement de version : ENGINE_VERSION 0.4.0 → 0.5.0.
"""
import pytest

from vertex.engines import skyler_core as SK


def _detail(score=83, rr=3.5, verdict='ACHETER'):
    return {'score': score, 'verdict': verdict,
            'plan': {'entry': 100, 'stop': 94, 'tp1': 106, 'tp2': 112,
                     'tp3': 118, 'rr_res': rr}}


def _market():
    return {'regime': {'label': 'TREND_UP', 'confidence': 0.9,
                       'adjustments': {'new_risk_allowed': True}}}


def _octx():
    return {'available': True, 'universe': 'LEAPS', 'best_in_mandate': True,
            'best': {'quality': 100, 'iv': 0.4}}


def _kw():
    return dict(market=_market(), events={'events': [{'label': 'Résultats', 'dte': 30}]},
                anomaly={'events': [], 'extreme': None}, as_of='t',
                options_ctx=_octx(),
                data_quality_ctx={'available': True, 'overall': 'FRESH',
                                  'warnings': [], 'actionable_allowed': True},
                reconciliation_ctx={'available': True, 'actionable_allowed': True})


# ─── Version et contrat ─────────────────────────────────────────────────────────

def test_engine_version_bumped_for_perturbation():
    parts = tuple(int(x) for x in SK.ENGINE_VERSION.split('.'))
    assert parts >= (0, 5, 0)


def test_perturbation_list_fixed_and_deterministic():
    assert len(SK.PERTURBATIONS) >= 10
    assert 'score_technique_-10' in SK.PERTURBATIONS
    assert 'sans_market' in SK.PERTURBATIONS
    import inspect
    src = inspect.getsource(SK)
    assert 'import random' not in src and 'random.' not in src


def test_perturbation_analysis_shape():
    r = SK.perturbation_analysis('ACHETER', 'PTX', _detail(), **_kw())
    assert r['n_applicable'] >= 1
    assert 0.0 <= r['value'] <= 1.0
    assert isinstance(r['flipped'], list)
    for f in r['flipped']:
        assert f['perturbation'] in SK.PERTURBATIONS
        assert f['decision'] in ('ACHETER', 'ATTENDRE', 'REFUSER')
    assert r['basis']


def test_perturbation_deterministic():
    a = SK.perturbation_analysis('ACHETER', 'PTX', _detail(), **_kw())
    b = SK.perturbation_analysis('ACHETER', 'PTX', _detail(), **_kw())
    assert a == b


# ─── Cas frontière : la décision bascule sous perturbation ──────────────────────

def test_borderline_buy_flips_under_score_minus_10():
    """Score 83 → 28/40 = ACHETER limite ; −10 points techniques → 27 = ATTENDRE.
    La perturbation doit détecter cette fragilité."""
    d = SK.decide('PTX', _detail(score=83), **_kw())
    assert d['decision'] == 'ACHETER'
    r = SK.perturbation_analysis('ACHETER', 'PTX', _detail(score=83), **_kw())
    assert any(f['perturbation'] == 'score_technique_-10' and f['decision'] == 'ATTENDRE'
               for f in r['flipped'])
    assert r['value'] < 1.0


def test_solid_refusal_is_robust():
    """Dossier vide refusé partout : presque aucune perturbation ne change REFUSER."""
    weak = {'score': 10, 'verdict': 'ATTENDRE'}
    r = SK.perturbation_analysis('REFUSER', 'PTX', weak, as_of='t')
    assert r['value'] >= 0.8
    assert r['stable'] + len(r['flipped']) == r['n_applicable']


def test_inapplicable_perturbations_listed_not_counted():
    """Sans plan, R:R ±0,5 est non applicable — listé, exclu de la fraction."""
    weak = {'score': 10, 'verdict': 'ATTENDRE'}
    r = SK.perturbation_analysis('REFUSER', 'PTX', weak, as_of='t')
    assert 'rr_-0.5' in r['not_applicable']
    assert r['n_applicable'] + len(r['not_applicable']) == len(SK.PERTURBATIONS)


# ─── La confiance consomme la robustesse mesurée ────────────────────────────────

def test_confidence_robustness_from_perturbation():
    d = SK.decide('PTX', _detail(score=83), **_kw())
    rob = d['confidence']['factors']['robustness']
    assert 'perturbation' in rob['basis']
    assert rob['value'] == d['perturbation']['value']
    assert d['perturbation']['n_applicable'] >= 1


def test_fragile_decision_lowers_confidence_vs_proxy():
    """La robustesse mesurée d'une décision frontière est < 1 — l'ancien proxy
    (blocs insuffisants) aurait pu la surestimer."""
    d = SK.decide('PTX', _detail(score=83), **_kw())
    assert d['confidence']['factors']['robustness']['value'] < 1.0


def test_decide_still_deterministic_and_consistent():
    a = SK.decide('PTX', _detail(), **_kw())
    b = SK.decide('PTX', _detail(), **_kw())
    assert a == b
    # la décision de base n'est jamais modifiée par l'analyse de perturbation
    assert a['decision'] == 'ACHETER'


# ─── La mémoire fige la confiance 0.5.0 séparée ─────────────────────────────────

def test_memory_freezes_measured_robustness_under_new_version():
    from vertex.engines import decision_memory as DM
    d = SK.decide('PTX', _detail(score=83), **_kw())
    p = SK.build_packet('PTX', _detail(score=83), **{k: v for k, v in _kw().items()})
    r = DM.freeze(decision=d, packet=p, price=100.0, closes=None,
                  portfolio_ctx=None, now=0)
    assert r['engine_version'] == SK.ENGINE_VERSION
    assert r['confidence'] == d['confidence']['value']
    assert r['confidence_factors']['robustness']['value'] == d['perturbation']['value']
