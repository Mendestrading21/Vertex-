"""Lot 7 — la réponse /scan est mise en cache (construite une fois par publish de scan).

Gardien du MÉCANISME : octets gzip valides (jamais double-gzippés), ETag stable entre
deux hits, 304 sur revalidation If-None-Match, et repli JSON non compressé honnête.
"""
import gzip
import json


def test_scan_response_cache_gzip_etag_304():
    import terminal
    client = terminal.app.test_client()

    r1 = client.get('/scan', headers={'Accept-Encoding': 'gzip'})
    assert r1.status_code == 200
    etag = r1.headers.get('ETag')
    assert etag                                   # ETag posé
    body1 = r1.get_data()
    if r1.headers.get('Content-Encoding') == 'gzip':
        raw = gzip.decompress(body1)              # décompresse SANS erreur (pas de double-gzip)
    else:
        raw = body1
    assert isinstance(json.loads(raw), dict)      # JSON valide

    r2 = client.get('/scan', headers={'Accept-Encoding': 'gzip'})
    assert r2.headers.get('ETag') == etag         # ETag stable → cache servi
    assert r2.get_data() == body1                 # octets identiques

    r3 = client.get('/scan', headers={'If-None-Match': etag})
    assert r3.status_code == 304                  # revalidation → rien à renvoyer

    r4 = client.get('/scan')                      # client sans gzip
    assert r4.status_code == 200
    assert r4.headers.get('Content-Encoding') in (None, '')
    assert isinstance(json.loads(r4.get_data()), dict)


def test_scan_cache_disabled_flag(monkeypatch):
    monkeypatch.setenv('VERTEX_SCAN_CACHE', '0')
    import terminal
    r = terminal.app.test_client().get('/scan')
    assert r.status_code == 200 and isinstance(json.loads(r.get_data()), dict)
