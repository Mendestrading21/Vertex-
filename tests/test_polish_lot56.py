"""tests/test_polish_lot56.py — SKYLER LOT 56 : polish Aujourd'hui + Marchés.

Inspection navigateur réelle d'abord (captures desktop 1440 + mobile 390,
audit débordements : 0). Deux défauts RÉELS trouvés et corrigés :

1. LISIBILITÉ des séries comparées (« Indices — performance comparée »,
   Marchés) : les trois premières séries de `C.colors.series` étaient des
   blancs-gris quasi identiques (#DBE1E8 / #c8bfae / #BABABA) —
   indistinguables sur le même graphique. Réordonné avec les couleurs
   EXISTANTES de la palette pour un contraste réel : marque, cyan, sable,
   violet, jaune, gris. Aucun littéral nouveau.

2. SLASH ORPHELIN mobile : `.vx-crumb-root` est masqué < 720 px mais son
   séparateur « / » restait affiché → fil d'Ariane « / Aujourd'hui / … ».
   Le séparateur adjacent est masqué avec lui.

Shell visible → SW v112 → v113.
"""
import re

CORE = 'vertex/static/vertex/js/charts/chart-core.js'
RESP = 'vertex/static/vertex/css/responsive.css'


def _read(p):
    return open(p, encoding='utf-8').read()


def test_multiline_series_start_distinct():
    src = _read(CORE)
    m = re.search(r"series:\s*\[([^\]]+)\]", src)
    assert m, 'palette series introuvable'
    cols = [c.strip().strip("'\"") for c in m.group(1).split(',')]
    # les 3 premières séries doivent être visuellement distinctes :
    # la marque cuivre, PUIS le cyan technique
    assert cols[0] == '#D28A54'
    assert cols[1] == '#45D6E8', 'la 2e série doit trancher (cyan), pas un gris proche'
    # aucun littéral hors palette existante
    allowed = {'#D28A54', '#45D6E8', '#9B7BFF', '#2BBE90', '#E9555F',
               '#D9BE3C', '#BABABA', '#8A8284', '#c8bfae'}
    assert set(cols) <= allowed, set(cols) - allowed


def test_mobile_crumb_no_orphan_slash():
    css = _read(RESP)
    m = re.search(r"\.vx-breadcrumb \.vx-crumb-root\s*(,[^{]+)?\{", css)
    assert m, 'règle mobile du crumb introuvable'
    # le séparateur qui suit la racine doit être masqué avec elle
    assert re.search(r"vx-crumb-root\s*\+\s*span", css), \
        'le séparateur adjacent doit être masqué (slash orphelin)'


def test_service_worker_bumped_to_at_least_v113():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 113
    assert 'td-shell-v112' not in body
