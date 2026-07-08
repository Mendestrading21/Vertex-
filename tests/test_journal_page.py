"""
tests/test_journal_page.py — Trade Journal 2.0 (page).

La page journal est montée depuis vertex/ui/journal.py : racine présente,
formulaire compatible (mêmes ids que l'auto-journalisation du Desk),
décisions épinglées conservées, et le moteur d'analyse embarqué.
"""

import terminal
from vertex.ui import journal


def test_page_mounts_new_module():
    assert 'tjRoot' in terminal.PAGE_JOURNAL
    assert journal.BODY in terminal.PAGE_JOURNAL


def test_form_ids_are_backward_compatible():
    # l'auto-journalisation du Desk et la saisie manuelle utilisent ces ids
    for fid in ('jTicker', 'jEntry', 'jStop', 'jTp', 'jExit', 'jPnl',
                'jLesson', 'jMistake', 'jConf', 'jDisc', 'jTrigger'):
        assert fid in journal.JS, fid


def test_storage_schema_is_preserved():
    # même clé localStorage + même sync desk que l'ancien journal
    assert "localStorage.getItem('vxJournal'" in journal.JS
    assert "/api/desk" in journal.JS


def test_pinned_decisions_kept():
    # les hôtes du bloc « décisions épinglées » (partagé avec /decisions)
    assert 'djStats' in journal.JS and 'djList' in journal.JS
    assert '_DECJ_JS' in open('terminal.py', encoding='utf-8').read()


def test_analysis_engine_sections_present():
    for marker in ('aiScore', 'stats(', 'coach(', 'gamify(', 'mistakes(',
                   'Coach Vertex', 'Base de connaissances', 'boucle de progression'):
        assert marker in journal.JS or marker in journal.BODY, marker


def test_route_serves_journal():
    c = terminal.app.test_client()
    r = c.get('/journal')
    assert r.status_code == 200 and b'tjRoot' in r.data
