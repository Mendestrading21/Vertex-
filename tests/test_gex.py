"""tests/test_gex.py — moteur GEX (exposition gamma dealers) : formule + honnêteté.

Vérifie le calcul réel (valeurs calculées à la main), la convention de signe
call/put, le net GEX / régime, les murs, la bascule zero-gamma, et l'honnêteté
(donnée absente → ignorée / vide, jamais inventée). Aucun ordre — lecture seule.
"""
from vertex.options import gex


def test_contract_gex_formula_exact():
    """GEX $ d'un contrat = gamma × OI × 100 × spot² × 1 %, signé call(+)/put(−)."""
    # spot=100, CALL K105 gamma0.05 OI1000 ; PUT K95 gamma0.04 OI2000
    prof = gex.compute([
        {'type': 'CALL', 'strike': 105, 'gamma': 0.05, 'oi': 1000, 'spot': 100},
        {'type': 'PUT', 'strike': 95, 'gamma': 0.04, 'oi': 2000, 'spot': 100},
    ])
    assert prof['empty'] is False
    assert prof['spot'] == 100
    assert prof['contracts_used'] == 2
    by_k = {s['strike']: s for s in prof['strikes']}
    # 0.05*1000*100*100^2*0.01 = 500 000
    assert round(by_k[105]['call_gex']) == 500000
    assert by_k[105]['put_gex'] == 0.0
    # −(0.04*2000*100*100^2*0.01) = −800 000
    assert round(by_k[95]['put_gex']) == -800000
    # net total = 500 000 − 800 000 = −300 000 → régime accélérateur
    assert round(prof['net_gex_total']) == -300000
    assert prof['regime'] == 'accelerateur'


def test_walls_and_normalized():
    prof = gex.compute([
        {'type': 'CALL', 'strike': 110, 'gamma': 0.03, 'oi': 5000, 'spot': 100},
        {'type': 'CALL', 'strike': 105, 'gamma': 0.02, 'oi': 1000, 'spot': 100},
        {'type': 'PUT', 'strike': 90, 'gamma': 0.03, 'oi': 4000, 'spot': 100},
    ])
    assert prof['call_wall'] == 110          # plus forte concentration call GEX
    assert prof['put_wall'] == 90            # put GEX le plus négatif
    # GEX normalisé : somme des |normalized| cohérente (chaque strike en % du |total|)
    tot = sum(abs(s['normalized']) for s in prof['strikes'])
    assert 99.0 <= tot <= 101.0             # ~100 % (arrondis)


def test_positive_net_is_stabilising_regime():
    prof = gex.compute([
        {'type': 'CALL', 'strike': 105, 'gamma': 0.06, 'oi': 3000, 'spot': 100},
        {'type': 'PUT', 'strike': 95, 'gamma': 0.01, 'oi': 500, 'spot': 100},
    ])
    assert prof['net_gex_total'] > 0
    assert prof['regime'] == 'stabilisant'   # dealers long gamma → volatilité amortie


def test_zero_gamma_flip_between_strikes():
    """Net GEX cumulé : négatif en bas (puts), positif en haut (calls) → bascule au milieu."""
    prof = gex.compute([
        {'type': 'PUT', 'strike': 90, 'gamma': 0.05, 'oi': 2000, 'spot': 100},
        {'type': 'CALL', 'strike': 110, 'gamma': 0.05, 'oi': 2000, 'spot': 100},
    ])
    assert prof['zero_gamma'] is not None
    assert 90 <= prof['zero_gamma'] <= 110


def test_missing_gamma_or_oi_is_ignored_not_invented():
    prof = gex.compute([
        {'type': 'CALL', 'strike': 105, 'gamma': None, 'oi': 1000, 'spot': 100},   # gamma absent
        {'type': 'CALL', 'strike': 106, 'gamma': 0.05, 'oi': None, 'spot': 100},    # OI absent
        {'type': 'CALL', 'strike': 107, 'gamma': 0.05, 'oi': 1000, 'spot': 100},    # exploitable
    ])
    assert prof['contracts_used'] == 1
    assert [s['strike'] for s in prof['strikes']] == [107]


def test_empty_chain_is_honest():
    prof = gex.compute([])
    assert prof['empty'] is True
    assert prof['net_gex_total'] is None
    assert prof['zero_gamma'] is None
    assert prof['reason']


def test_no_spot_refuses_without_inventing():
    prof = gex.compute([{'type': 'CALL', 'strike': 105, 'gamma': 0.05, 'oi': 1000}])
    assert prof['empty'] is True
    assert prof['spot'] is None


def test_spot_inferred_from_contract_when_not_passed():
    prof = gex.compute([{'type': 'CALL', 'strike': 105, 'gamma': 0.05, 'oi': 1000, 'spot': 250}])
    assert prof['spot'] == 250


def test_bool_and_nan_rejected():
    prof = gex.compute([
        {'type': 'CALL', 'strike': 105, 'gamma': True, 'oi': 1000, 'spot': 100},        # bool → ignoré
        {'type': 'CALL', 'strike': 106, 'gamma': float('nan'), 'oi': 1000, 'spot': 100},  # NaN → ignoré
        {'type': 'CALL', 'strike': 107, 'gamma': 0.05, 'oi': 1000, 'spot': 100},         # ok
    ])
    assert prof['contracts_used'] == 1


def test_pure_no_mutation_of_input():
    chain = [{'type': 'CALL', 'strike': 105, 'gamma': 0.05, 'oi': 1000, 'spot': 100}]
    snapshot = dict(chain[0])
    gex.compute(chain)
    assert chain[0] == snapshot                # entrée non mutée (fonction pure)


def test_vanna_computed_when_iv_dte_present():
    """Vanna $ par strike + net total quand IV/DTE réels présents (BS, convention GEX)."""
    prof = gex.compute([
        {'type': 'CALL', 'strike': 105, 'gamma': 0.05, 'oi': 1000, 'spot': 100,
         'iv': 30.0, 'dte': 30},
        {'type': 'PUT', 'strike': 95, 'gamma': 0.04, 'oi': 2000, 'spot': 100,
         'iv': 35.0, 'dte': 30},
    ])
    assert prof['net_vanna_total'] is not None
    by_k = {s['strike']: s for s in prof['strikes']}
    assert by_k[105]['vanna'] is not None
    # OTM call (K>S) : d2<0 → vanna>0 → exposition call positive (convention)
    assert by_k[105]['vanna'] > 0


def test_vanna_none_when_iv_absent():
    prof = gex.compute([{'type': 'CALL', 'strike': 105, 'gamma': 0.05, 'oi': 1000, 'spot': 100}])
    assert prof['net_vanna_total'] is None
    assert prof['strikes'][0]['vanna'] is None
