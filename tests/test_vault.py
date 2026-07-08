"""
tests/test_vault.py — Archive Vault (coffre-fort interne).

La page est montée, routée (/vault + /archive), rangée dans SYSTEM,
synchronisée (clé vxVault dans le contrat unifié), et son moteur embarque
les composants demandés + le schéma d'item complet.
"""

import terminal
from vertex.ui import nav, vault


def test_vault_routes_serve_page():
    c = terminal.app.test_client()
    for p in ('/vault', '/archive'):
        r = c.get(p)
        assert r.status_code == 200 and b'avRoot' in r.data, p


def test_vault_in_nav_system_section():
    items = dict((p, l) for p, _, l in nav.ITEMS)
    assert items.get('/vault') == 'Archive Vault'
    # placé APRÈS Settings → section SYSTEM, pas dans le cœur de l'expérience
    paths = nav.paths()
    assert paths.index('/vault') > paths.index('/settings')


def test_vault_components_architecture():
    for comp in ('vaultSearch', 'vaultFilters', 'vaultList', 'vaultCard',
                 'vaultDetail', 'vaultEditor', 'avRender'):
        assert comp in vault.JS, comp


def test_vault_item_schema_complete():
    for field in ('id', 'title', 'type', 'content', 'tags', 'createdAt',
                  'updatedAt', 'source', 'status', 'priority', 'linkedPage'):
        assert field in vault.JS, field


def test_vault_types_and_actions():
    for t in ('prompt', 'analyse', 'idee', 'version', 'technote',
              'design', 'bug', 'feature', 'texte'):
        assert "'" + t + "'" in vault.JS or t + ':' in vault.JS, t
    for action in ('avArchive', 'avRestore', 'avDel', 'avImp', 'avExport', 'avImport'):
        assert action in vault.JS, action
    assert 'confirm(' in vault.JS            # suppression définitive = confirmation


def test_vault_synced_via_desk_contract():
    assert "'vxVault'" in vault.JS
    assert "vxVault" in open('terminal.py', encoding='utf-8').read()
