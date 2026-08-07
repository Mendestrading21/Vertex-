"""SKYLER LOT 297 — gardien du mode de fraîcheur du stress test (risque).

Contrat : le pied du stress test (/portfolio?view=risk) affichait un
chip « Live » codé EN DUR — même en DEMO ou sur cotes de repli. Comme
ses cartes jumelles (P&L, exposition options), il doit suivre
`window.__pfLive` : « live » seulement quand /api/pos-quotes le
confirme, « fallback » sinon.
"""

PORTFOLIO_PAGE = 'vertex/ui/pages/portfolio_page.py'


def test_risk_footer_mode_follows_pflive():
    with open(PORTFOLIO_PAGE, encoding='utf-8') as f:
        src = f.read()
    assert ("VX.updateIndicator(Date.now(),'risk_engine (positions réelles)',"
            "window.__pfLive?'live':'fallback')") in src


def test_no_hardcoded_live_mode_left():
    # Plus aucun updateIndicator au mode 'live' codé en dur dans la page.
    with open(PORTFOLIO_PAGE, encoding='utf-8') as f:
        src = f.read()
    assert ",'live')" not in src
