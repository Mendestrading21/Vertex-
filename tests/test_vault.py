"""tests/test_vault.py — CE QUI RESTE VIVANT de l'Archive Vault.

Ce fichier comptait SIX tests ; QUATRE lisaient `vertex/ui/vault.py`, module
supprimé au lot 17 (0 consommateur en production, aucune route). Ils
vérifiaient les composants, le schéma d'item, les types et actions, et la clé
de sync — d'un JavaScript que plus aucune page ne servait.

Les DEUX conservés gardent du vivant, et il aurait été facile de les emporter
avec le fichier :
- `/vault` et `/archive` redirigent bien vers Système › Archive (301) ;
- l'entrée de navigation existe et reste APRÈS Settings, donc en section
  SYSTEM et non dans le cœur du parcours.

La clé `vxVault` reste gardée là où elle compte — `DESK_KEYS` de
`vx-entities.js` et le repli de `system_page.py`, cf.
`tests/test_desk_keys_servies_lot381.py`.
"""

import terminal
from vertex.ui import nav


def test_vault_routes_serve_page():
    # Redesign : /vault et /archive redirigent vers Système/Archive (301),
    # qui lit le même vxVault (schéma préservé, gardé plus bas).
    c = terminal.app.test_client()
    for p in ('/vault', '/archive'):
        r = c.get(p)
        assert r.status_code == 301, p
        assert '/system' in r.headers['Location'], p
        r2 = c.get(p, follow_redirects=True)
        assert r2.status_code == 200 and b'vx-app' in r2.data, p


def test_vault_in_nav_system_section():
    items = dict((p, l) for p, _, l in nav.ITEMS)
    assert items.get('/vault') == 'Archive Vault'
    # placé APRÈS Settings → section SYSTEM, pas dans le cœur de l'expérience
    paths = nav.paths()
    assert paths.index('/vault') > paths.index('/settings')
