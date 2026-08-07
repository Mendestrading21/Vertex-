"""
LOT 182 — GARDIEN GLOBAL de la règle critique n°2 : « tout JavaScript
généré depuis Python doit être syntaxiquement VALIDE » (deux
SyntaxError silencieuses ont déjà vécu — une apostrophe française non
échappée suffit à tuer une page en silence). Le lot 181 gardait
home_art ; celui-ci systématise : chaque bloc <script> inline de
CHAQUE route HTML servie est passé au vrai parseur (node --check),
plus les chaînes JS exposées par les modules (sync_center, heatmap
du vault). Survey honnête : tracking_page/vault/sync_center ont déjà
leurs gardiens de contenu — la lacune transverse était la SYNTAXE.
"""
import functools
import os
import re
import subprocess
import tempfile

import pytest

import terminal
from vertex.ui import sync_center

ROUTES = ('/', '/markets', '/opportunities', '/portfolio', '/journal',
          '/options', '/system', '/tracking', '/intelligence',
          '/titre/AAPL', '/company/AAPL', '/analysis/AAPL',
          '/login', '/widget-lab', '/design-system', '/system/design-system')

_INLINE = re.compile(r'<script(?![^>]*\bsrc=)([^>]*)>(.*?)</script>', re.S)


def _blocks(html):
    """Blocs <script> INLINE exécutables : src= et type json ignorés."""
    return [body for attrs, body in _INLINE.findall(html)
            if body.strip() and 'json' not in attrs.lower()]


def _check(js):
    """node --check : renvoie None si valide, sinon la dernière ligne d'erreur."""
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False) as f:
        f.write(js)
        path = f.name
    try:
        r = subprocess.run(['node', '--check', path], capture_output=True, text=True)
        return None if r.returncode == 0 else (r.stderr.strip().splitlines() or ['?'])[-1]
    finally:
        os.unlink(path)


@functools.lru_cache(maxsize=1)
def _sweep():
    """Un seul balayage pour toute la classe de tests : {route: (status, [blocs])}."""
    c = terminal.app.test_client()
    out = {}
    for r in ROUTES:
        resp = c.get(r, follow_redirects=True)
        out[r] = (resp.status_code, _blocks(resp.get_data(as_text=True)))
    return out


# ── Le balayage lui-même ─────────────────────────────────────────────────────

def test_toutes_les_routes_html_repondent_200():
    statuts = {r: s for r, (s, _) in _sweep().items()}
    assert statuts == {r: 200 for r in ROUTES}


def test_le_gardien_ne_tourne_pas_a_vide():
    # Si l'extraction cassait (regex, refonte des pages), le balayage passerait
    # sans rien vérifier — on exige un volume minimal de JS réellement contrôlé.
    total = sum(len(bs) for _, bs in _sweep().values())
    assert total >= 12


def test_chaque_bloc_inline_de_chaque_page_parse():
    erreurs = []
    for route, (_, blocs) in _sweep().items():
        for i, b in enumerate(blocs):
            err = _check(b)
            if err:
                erreurs.append('%s bloc %d : %s' % (route, i, err))
    assert erreurs == []


# ── Chaînes JS exposées par les modules (avant injection) ────────────────────

def test_sync_center_js_parse():
    assert _check(sync_center.JS) is None


def test_heatmap_du_vault_parse():
    assert _check(terminal._HEATMAP_JS) is None


# ── L'extracteur lui-même (le gardien du gardien) ────────────────────────────

def test_extraction_ignore_src_et_json_garde_l_inline():
    html = ('<script src="/a.js"></script>'
            '<script type="application/json">{"x": 1}</script>'
            '<script>var ok=1;</script>'
            '<script></script>')
    assert _blocks(html) == ['var ok=1;']
