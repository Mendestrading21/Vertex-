"""Lot 37 — cleanup prouvé : les modules UI hérités sans consommateur sont retirés.

Après le retrait de la couche pages de terminal.py (lot 36), dix modules de
`vertex/ui/` n'avaient plus UN SEUL consommateur de production (mesuré :
grep imports sur vertex/ + terminal.py ; routes : toutes les URL héritées
appartiennent à vertex.app.routes.redesign — pages 2.0 ou 301) :

    nav, home_art, sync_center, vx_kit, design_system, signals,
    journal, options_lab, strategy_os, vault

Leurs capacités ont chacune UN propriétaire canonique servi :
navigation → vertex/ui/shell ; entités & desk (DESK_KEYS, journal, suivis,
favoris, notes) → vx-entities.js ; design system → vertex-2-0.css et
vertex/ui/pages/design_system_page.py ; stratégie → strategy_os_api (API) et
les pages 2.0 ; synchronisation → live-updates.js + /api/live/*.

Règle de convergence respectée : conserver → migrer → parité → retirer.
Rollback : git revert du lot.
"""
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_RETIRES = ['nav', 'home_art', 'sync_center', 'vx_kit', 'design_system',
            'signals', 'journal', 'options_lab', 'strategy_os', 'vault']

_VIVANTS = ['vx2.py', 'shell', 'pages', '__init__.py']


def test_les_modules_orphelins_sont_retires():
    restants = [m for m in _RETIRES
                if os.path.exists(os.path.join(_ROOT, 'vertex', 'ui', m + '.py'))]
    assert not restants, (
        'modules UI orphelins revenus : %s — leurs capacités ont un '
        'propriétaire canonique servi (voir docstring)' % restants)


def test_personne_ne_les_importe_plus():
    fautes = []
    for base in ('vertex', 'tests'):
        for racine, _, noms in os.walk(os.path.join(_ROOT, base)):
            if '__pycache__' in racine:
                continue
            for n in noms:
                if not n.endswith('.py'):
                    continue
                p = os.path.join(racine, n)
                src = open(p, encoding='utf-8', errors='ignore').read()
                for m in _RETIRES:
                    if ('from vertex.ui import ' + m) in src \
                            or ('from vertex.ui.' + m + ' import') in src \
                            or ('vertex.ui.' + m + ' as ') in src:
                        fautes.append((os.path.relpath(p, _ROOT), m))
    src_t = open(os.path.join(_ROOT, 'terminal.py'), encoding='utf-8').read()
    for m in _RETIRES:
        if 'from vertex.ui import ' + m in src_t:
            fautes.append(('terminal.py', m))
    assert not fautes, 'imports de modules retirés : %s' % fautes


def test_la_surface_vivante_reste():
    for v in _VIVANTS:
        assert os.path.exists(os.path.join(_ROOT, 'vertex', 'ui', v)), v


def test_les_routes_des_anciens_modules_redirigent_vers_les_proprietaires():
    """Les URL des capacités déplacées restent joignables (301 → page 2.0)."""
    import terminal
    c = terminal.app.test_client()
    for old, frag in (('/vault', '/system'), ('/archive', '/system'),
                      ('/strategy-os', '/intelligence')):
        r = c.get(old)
        assert r.status_code in (301, 302, 308), old
        assert (r.headers.get('Location') or '').startswith(frag), (
            old + ' → ' + str(r.headers.get('Location')))


def test_le_schema_vxvault_reste_servi():
    """La clé vxVault (archive) survit au retrait de vault.py : elle est dans
    le contrat de sync SERVI (vx-entities.js)."""
    import os
    ent = open(os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js',
                            'vx-entities.js'), encoding='utf-8').read()
    assert "'vxVault'" in ent
