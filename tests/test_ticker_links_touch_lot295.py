"""SKYLER LOT 295 — gardien des cibles tactiles tickers/liens dim.

Contrat : au balayage des 12 vues profondes restantes, deux familles
sous la règle tactile : les boutons tickers `.vx-link` (shortlist
Opportunités, 21px mesurés) et les liens nus dans `.vx-dim` (Journal →
Hypothèses, 16px mesurés). En ≤640px : `.vx-link` reçoit
min-height:40px et `.vx-dim a` le même padding que `.vx-meta a`
(lot 293).
"""

RESPONSIVE_CSS = 'vertex/static/vertex/css/responsive.css'


def _mobile_block():
    with open(RESPONSIVE_CSS, encoding='utf-8') as f:
        return f.read().split('@media (max-width:640px)', 1)[1]


def test_ticker_buttons_touch_target_on_mobile():
    assert '.vx-link{min-height:40px}' in _mobile_block()


def test_dim_links_touch_target_on_mobile():
    assert '.vx-dim a{display:inline-block;padding:13px 0}' in _mobile_block()
