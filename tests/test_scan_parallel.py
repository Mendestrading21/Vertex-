"""Lot 3 — le scan parallèle doit produire un résultat BYTE-IDENTIQUE au mode série.

analyse()/research.* sont pures et le RNG Monte-Carlo/bootstrap est local (seed dérivé
du prix) : paralléliser la boucle par titre ne peut pas changer un seul chiffre. Ce
gardien fige cette invariance (workers=4 == workers=1) sur des données démo déterministes.
"""
import json


def _scan_blob(workers, monkeypatch):
    import terminal
    from vertex.app import state
    monkeypatch.setenv('VERTEX_SCAN_WORKERS', str(workers))
    monkeypatch.setattr(terminal, 'DEMO_MODE', True)   # données démo déterministes (seed = CRC ticker)
    terminal._ANALYSE_MEMO.clear()                     # calcul frais des deux côtés
    terminal.scan()
    return json.dumps({'rows': state.scan_state.get('rows'),
                       'detail': state.scan_state.get('detail')}, sort_keys=True, default=str)


def test_parallel_scan_is_byte_identical_to_serial(monkeypatch):
    from vertex.app import state
    saved = dict(state.scan_state)
    try:
        serial = _scan_blob(1, monkeypatch)
        parallel = _scan_blob(4, monkeypatch)
        assert serial == parallel and len(serial) > 1000   # non vide + identique
    finally:
        state.scan_state.clear()
        state.scan_state.update(saved)
