"""tests/test_charts_2026_lot61.py — SKYLER LOT 61 : runway anti-collision +
purge des fallbacks périmés dans les JS de charts.

Reprise du travail continu (« continue »). Deux défauts réels :

1. CATALYST RUNWAY (briefing) : l'alternance haut/bas par simple PARITÉ
   d'index laissait se chevaucher deux étiquettes proches placées du même
   côté (vu sur capture lot 56 : ALB J-7 / ARE J-7 / Inflation J-8
   illisibles) et les étiquettes de bord sortaient du viewBox. Corrigé :
   côté choisi selon la PLACE réelle restante de chaque côté (déterministe,
   jamais d'aléatoire) + x d'étiquette borné à la piste.

2. Le gardien anti-palette-périmée du lot 59 couvrait les pages Python
   mais PAS les JS de charts : 25 fallbacks d'anciennes palettes restaient
   (chart-core, catalyst-runway, anomaly-scan — avec le token INEXISTANT
   `--vx-text-dim` actif — regime-aura ; + 3e token fantôme `--vx-bg-app`).
   Purgés ; gardien prospectif étendu au répertoire charts.

Shell visible → SW v116 → v117.
"""
import glob
import re

RUNWAY = 'vertex/static/vertex/js/charts/catalyst-runway.js'

CURRENT = {'#F8F5F3', '#BABABA', '#8A8284', '#989092', '#2BBE90', '#E9555F', '#D9BE3C',
           '#D28A54', '#E1A06E', '#30292B', '#0c0c0e', '#121214', '#c8bfae', '#9B7BFF',
           '#45D6E8', '#050505', '#151719'}


def _charts_js():
    return sorted(glob.glob('vertex/static/vertex/js/charts/*.js'))


def _defined_tokens():
    names = set()
    for css in glob.glob('vertex/static/vertex/css/*.css'):
        names |= set(re.findall(r"(--vx-[a-z0-9-]+)\s*:",
                                open(css, encoding='utf-8').read()))
    return names


def test_runway_no_parity_side_choice():
    src = open(RUNWAY, encoding='utf-8').read()
    assert 'i % 2' not in src, 'la parité ne gère pas les collisions réelles'
    assert 'MIN_GAP' in src            # anti-collision par place restante
    assert 'lastTop' in src and 'lastBot' in src


def test_runway_labels_clamped_to_track():
    src = open(RUNWAY, encoding='utf-8').read()
    assert re.search(r"Math\.min\(Math\.max\(", src), \
        'les étiquettes de bord doivent être bornées au viewBox'


def test_charts_js_fallbacks_match_current_palette():
    bad = []
    for path in _charts_js():
        src = open(path, encoding='utf-8').read()
        for col in re.findall(r"var\(--vx-[a-z0-9-]+,(#[0-9A-Fa-f]{6})\)", src):
            if col not in CURRENT:
                bad.append('%s: %s' % (path, col))
    assert not bad, 'fallbacks hors palette actuelle :\n' + '\n'.join(sorted(set(bad)))


def test_charts_js_referenced_tokens_exist():
    defined = _defined_tokens()
    bad = []
    for path in _charts_js():
        src = open(path, encoding='utf-8').read()
        for name in set(re.findall(r"var\((--vx-[a-z0-9-]+),#", src)):
            if name not in defined:
                bad.append('%s: %s' % (path, name))
    assert not bad, 'tokens inexistants référencés :\n' + '\n'.join(sorted(bad))


def test_service_worker_bumped_to_at_least_v117():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 117
    assert 'td-shell-v116' not in body
