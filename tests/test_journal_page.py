"""
tests/test_journal_page.py — Journal : espace servi et contrat de données.

Historique : la page journal était générée par vertex/ui/journal.py, module
retiré au lot 37 (aucune route ne le servait — /journal appartient à
redesign). Ce qui reste vrai et gardé : l'URL /journal sert la coque 2.0,
/performance aussi (deux espaces canoniques), et le contrat de données
vxJournal (auto-journalisation du Desk) vit dans le JS réellement servi.
"""

import terminal


def test_route_serves_journal():
    c = terminal.app.test_client()
    for p in ('/journal', '/performance'):
        r = c.get(p)
        assert r.status_code == 200 and b'vx-app' in r.data, p


def test_contrat_vxjournal_dans_le_js_servi():
    ent = open('vertex/static/vertex/js/vx-entities.js', encoding='utf-8').read()
    assert "'vxJournal'" in ent          # clé de sync préservée
    assert 'journal()' in ent            # lecteur canonique
    assert '/api/desk' in ent            # sync serveur du desk
