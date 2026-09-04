"""tests/test_polish_inspection_angles_neufs.py — SKYLER LOT 65 : tour d'inspection (angles neufs).

Angles audités en navigateur réel sur les 8 pages : doublons d'id (0),
liens internes morts (0 sur 13 testés), focus clavier visible (8/8
tabulations sur chaque page), SVG informatifs sans aria → UN seul cas
réel : le SVG du Catalyst Runway (briefing) n'était couvert par aucun
`role="img"`/`aria-label` (le Regime Aura, lui, l'était déjà).

Corrigé : le SVG du runway porte `role="img"` + `aria-label` reprenant
le VERDICT réel déjà calculé (prochain catalyseur + fenêtre) — aucune
donnée nouvelle, même texte que la ligne de verdict rendue dessous.

Shell visible → SW v120 → v121.
"""
import re

RUNWAY = 'vertex/static/vertex/js/charts/catalyst-runway.js'


def test_runway_svg_has_aria():
    src = open(RUNWAY, encoding='utf-8').read()
    m = re.search(r"<svg[^>]*viewBox[^>]*>", src)
    assert m, 'svg du runway introuvable'
    assert 'role="img"' in m.group(0)
    assert 'aria-label' in m.group(0)


def test_service_worker_bumped_to_at_least_v121():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 121
    assert 'td-shell-v120' not in body
