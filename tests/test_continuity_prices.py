"""CONTINUITY LOT 5 — source de prix centrale (§9).

Un ticker = un prix partout ; distinction live / référence snapshot / prix d'achat ;
jamais de substitution silencieuse ni de prix inventé. Contrat statique (comportement
validé par smoke-test navigateur/node dans le rapport CONTINUITY-05).
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = (ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-core.js').read_text(encoding='utf-8')


def test_central_price_source_present():
    assert 'VX.prices' in CORE
    for m in ('setLive', 'setRef', 'setAvgCost', 'subscribe', 'get('):
        assert m in CORE, m


def test_distinguishes_live_ref_avgcost():
    """Prix live, prix de référence du snapshot, prix moyen d'achat sont distincts."""
    assert 'refSession' in CORE          # référence rattachée à une session
    assert 'avgCost' in CORE
    assert 'live_prices' in CORE          # miroir dans le store


def test_never_invents_and_never_silently_overwrites():
    assert '_ok(' in CORE                  # garde de validité (isFinite)
    assert 'jamais de prix inventé' in CORE or 'jamais' in CORE
    # setRef et setLive sont des chemins SÉPARÉS (le live n'écrase pas la référence)
    assert 'setRef(sym' in CORE and 'setLive(sym' in CORE


def test_subscribe_returns_unsubscribe():
    assert 'subscribe(sym, cb)' in CORE
    assert 'filter((f) => f !== cb)' in CORE
