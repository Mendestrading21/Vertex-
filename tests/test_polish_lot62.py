"""tests/test_polish_lot62.py — SKYLER LOT 62 : purge finale des JS (pages/).

Le balayage des lots 58-61 couvrait pages Python + charts JS ; restaient
les JS de pages (`vertex/static/vertex/js/pages/`) : 19 fallbacks
d'anciennes palettes (options-gex — avec l'orange banni `#cf6128` et le
token INEXISTANT `--vx-text-dim` ACTIF —, options-intel,
options-structure, tracking). Purgés ; le gardien prospectif couvre
désormais TOUT `vertex/static/vertex/js/` récursivement — plus aucun
angle mort de ce type.

Shell visible → SW v117 → v118.
"""
import glob
import re

CURRENT = {'#F8F5F3', '#BABABA', '#8A8284', '#2BBE90', '#E9555F', '#D9BE3C',
           '#DBE1E8', '#30292B', '#0c0c0e', '#121214', '#c8bfae', '#9B7BFF',
           '#45D6E8', '#050505', '#151719'}


def _all_js():
    return sorted(glob.glob('vertex/static/vertex/js/**/*.js', recursive=True))


def _defined_tokens():
    names = set()
    for css in glob.glob('vertex/static/vertex/css/*.css'):
        names |= set(re.findall(r"(--vx-[a-z0-9-]+)\s*:",
                                open(css, encoding='utf-8').read()))
    return names


def test_all_js_fallbacks_match_current_palette():
    bad = []
    for path in _all_js():
        if '/vendor/' in path:
            continue                      # libs tierces : hors périmètre
        src = open(path, encoding='utf-8').read()
        for col in re.findall(r"var\(--vx-[a-z0-9-]+,(#[0-9A-Fa-f]{6})\)", src):
            if col not in CURRENT:
                bad.append('%s: %s' % (path, col))
    assert not bad, 'fallbacks hors palette actuelle :\n' + '\n'.join(sorted(set(bad)))


def test_all_js_referenced_tokens_exist():
    defined = _defined_tokens()
    bad = []
    for path in _all_js():
        if '/vendor/' in path:
            continue
        src = open(path, encoding='utf-8').read()
        for name in set(re.findall(r"var\((--vx-[a-z0-9-]+),#", src)):
            if name not in defined:
                bad.append('%s: %s' % (path, name))
    assert not bad, 'tokens inexistants référencés :\n' + '\n'.join(sorted(bad))


def test_no_banned_orange_in_js():
    bad = []
    for path in _all_js():
        if '/vendor/' in path:
            continue
        src = open(path, encoding='utf-8').read()
        for col in ('#cf6128', '#b9683d', '#cc892c'):
            if col in src:
                bad.append('%s: %s' % (path, col))
    assert not bad, 'oranges bannis :\n' + '\n'.join(sorted(bad))


def test_service_worker_bumped_to_at_least_v118():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 118
    assert 'td-shell-v117' not in body
