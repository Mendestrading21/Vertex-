"""tests/test_import_button_lot47.py — SKYLER LOT 47 : bouton Importer.

La restauration souveraine (lots 45/46) existait en API seulement — le
trader devait utiliser curl pour restaurer sa sauvegarde. La carte Mémoire
gagne un bouton « Importer » à côté d'« Exporter » : input file caché,
lecture FileReader, POST /api/skyler/memory/import, AFFICHAGE HONNÊTE du
résultat (stats ajoutées/ignorées/corrompues par magasin, ou l'erreur
structurée du serveur — empreinte invalide dite telle quelle, jamais
maquillée en succès). Shell visible → SW v106 → v107.
"""
import re


def _journal_body():
    import terminal
    return terminal.app.test_client().get(
        '/journal', follow_redirects=True).get_data(as_text=True)


def test_memory_card_has_import_button_next_to_export():
    body = _journal_body()
    assert 'Importer' in body
    assert 'vx-mem-import-file' in body               # input file caché
    assert body.count('/api/skyler/memory/export') >= 1   # Exporter conservé


def test_import_wiring_posts_to_import_route():
    body = _journal_body()
    assert '/api/skyler/memory/import' in body
    assert 'FileReader' in body


def test_import_result_honest_success_and_error_paths():
    """Le rendu du résultat couvre les DEUX chemins : stats du rejeu en
    succès, et l'erreur serveur affichée telle quelle en échec."""
    body = _journal_body()
    assert 'vx-mem-import-result' in body
    assert 'restaur' in body.lower()                  # message de succès
    assert 'skipped_decisions' in body or 'ignor' in body.lower()
    assert 'error' in body                            # chemin d\'erreur câblé


def test_import_survives_js_number_roundtrip(tmp_path, monkeypatch):
    """DÉFAUT RÉEL attrapé par la preuve navigateur : JSON.stringify replie
    100.0 en 100 — l'empreinte canonique doit être STABLE au round-trip JS
    (flottants entiers normalisés des DEUX côtés, documenté dans la note)."""
    import json
    import terminal
    from vertex.services import persist
    from vertex.engines import decision_memory as DM
    from vertex.engines import skyler_core as SK
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    c = terminal.app.test_client()
    d = {'symbol': 'JSR', 'as_of': 't', 'decision': 'ATTENDRE',
         'score': {'total': 20, 'level': 'REFUS_WATCH', 'insufficient_blocks': []},
         'level': 'REFUS_WATCH', 'contradictions': [], 'unknowns': []}
    r = DM.freeze(decision=d, packet={'schema_version': 1,
                                      'engine_version': SK.ENGINE_VERSION},
                  price=100.0, closes=None, portfolio_ctx=None, now=0,
                  session_date='2026-08-01')
    (tmp_path / 'skyler_memory.json').write_text(
        json.dumps(DM.append_decision(DM.empty_memory(), r)), encoding='utf-8')
    bundle = c.get('/api/skyler/memory/export').get_json()
    (tmp_path / 'skyler_memory.json').unlink()

    def js_roundtrip(o):                       # simule JSON.parse(JSON.stringify)
        if isinstance(o, float) and o.is_integer():
            return int(o)
        if isinstance(o, dict):
            return {k: js_roundtrip(v) for k, v in o.items()}
        if isinstance(o, list):
            return [js_roundtrip(v) for v in o]
        return o

    resp = c.post('/api/skyler/memory/import', json=js_roundtrip(bundle))
    assert resp.status_code == 200, resp.get_json()
    assert resp.get_json()['stats']['added_decisions'] == 1


def test_service_worker_bumped_to_at_least_v107():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 107
    assert 'td-shell-v106' not in body
