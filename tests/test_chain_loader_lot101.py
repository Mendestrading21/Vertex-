"""tests/test_chain_loader_lot101.py — SKYLER LOT 101 : entonnoir de chaîne figé.

Trou réel de couverture : vertex/options/chain_loader.py n'avait qu'UN test
indirect (bornes de funnel_plan dans test_options_engine) — la logique de
sélection pure (bornes DTE inclusives, priorité fenêtre préférée, tri par
distance au centre, fenêtre de strikes ±35 %, échantillonnage gardant les
extrêmes) n'était figée nulle part. C'est elle qui garantit qu'on ne
demande JAMAIS toute la chaîne au broker (§14).
Caractérisations nées vertes (dites) — moteur INTACT. Date injectée
(today) → déterministe.
"""
import datetime as dt

from vertex.options import chain_loader as cl
from vertex.strategy import constitution as C

PROFILE = C.load_profile()          # DTE : absolu 60-540, préféré 90-210
TODAY = dt.date(2026, 1, 1)


def _exp(days):
    return (TODAY + dt.timedelta(days=days)).isoformat()


def test_absolute_dte_bounds_are_inclusive_and_bad_dates_skipped():
    exps = [_exp(59), _exp(60), _exp(540), _exp(541), 'pas-une-date']
    picked = cl.pick_expiries(exps, PROFILE, today=TODAY)
    assert sorted(e['dte'] for e in picked) == [60, 540], (
        'bornes constitution INCLUSIVES ; hors bornes et dates pourries exclues')
    assert all(e['preferred'] is False for e in picked)


def test_preferred_window_first_then_distance_to_center():
    # centre préféré = (90+210)/2 = 150
    exps = [_exp(60), _exp(90), _exp(150), _exp(210), _exp(400)]
    picked = cl.pick_expiries(exps, PROFILE, today=TODAY)
    assert len(picked) == cl.MAX_EXPIRIES == 4
    assert [e['dte'] for e in picked] == [150, 90, 210, 60], (
        'préférées d\'abord (150 pile au centre, puis 90/210 ex æquo dans '
        'l\'ordre stable), la non-préférée la plus proche ferme la marche')
    assert [e['preferred'] for e in picked] == [True, True, True, False]
    assert all('_dist' not in e for e in picked)   # champ interne jamais fui


def test_empty_or_none_expirations_yield_empty_plan():
    assert cl.pick_expiries([], PROFILE, today=TODAY) == []
    assert cl.pick_expiries(None, PROFILE, today=TODAY) == []


def test_strike_window_is_exact_35_pct_and_sorted():
    # spot 100 → fenêtre [65, 135] bornes incluses
    ks = cl.pick_strikes([64.9, 65.0, 100.0, 135.0, 135.1, 80.0], 100.0)
    assert ks == [65.0, 80.0, 100.0, 135.0]


def test_nonpositive_spot_returns_empty_never_guesses():
    assert cl.pick_strikes([90.0, 100.0], 0.0) == []
    assert cl.pick_strikes([90.0, 100.0], -5.0) == []


def test_sampling_caps_at_14_and_keeps_both_extremes():
    strikes = [float(k) for k in range(70, 131)]   # 61 strikes dans la fenêtre
    ks = cl.pick_strikes(strikes, 100.0)
    assert len(ks) == cl.MAX_STRIKES_PER_EXPIRY == 14
    assert ks[0] == 70.0 and ks[-1] == 130.0, (
        'l\'échantillonnage garde l\'ITM léger ET le très OTM (ultra-convexe)')
    assert ks == sorted(ks) and len(set(ks)) == 14


def test_funnel_plan_drops_expiries_without_plausible_strikes():
    exps = [_exp(150), _exp(120)]
    strikes = {_exp(150): [95.0, 105.0], _exp(120): [500.0]}  # 500 hors fenêtre
    plan = cl.funnel_plan(exps, strikes, 100.0, PROFILE, right='P', today=TODAY)
    assert [p['expiry'] for p in plan] == [_exp(150)], (
        'une expiration sans strike plausible ne part JAMAIS au broker')
    assert plan[0]['right'] == 'P' and plan[0]['dte'] == 150


def test_funnel_plan_entry_contract():
    plan = cl.funnel_plan([_exp(150)], {_exp(150): [100.0]}, 100.0,
                          PROFILE, today=TODAY)
    assert set(plan[0]) == {'expiry', 'dte', 'preferred', 'strikes', 'right'}
    assert plan[0]['preferred'] is True and plan[0]['right'] == 'C'
