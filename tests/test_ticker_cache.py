"""Lot 8 — options_pack (dossier options d'une fiche) est mis en cache par symbole ~3 min.

Réouverture instantanée dans la fenêtre, sans re-refetch yfinance live. Copie profonde
en entrée/sortie → la mutation par un appelant ne corrompt jamais le cache. ?fresh / arg
force la reconstruction. VERTEX_TICKER_TTL=0 désactive.
"""


def test_options_pack_ttl_cache(monkeypatch):
    import terminal
    calls = []
    monkeypatch.setattr(terminal, '_options_pack_build',
                        lambda sym: {'sym': sym, 'spot': 100.0, 'contracts': []})
    # compter les vraies constructions
    build = terminal._options_pack_build
    monkeypatch.setattr(terminal, '_options_pack_build',
                        lambda sym: (calls.append(sym), build(sym))[1])
    terminal._OPTPACK_CACHE.clear()

    a = terminal.options_pack('ZZ')
    b = terminal.options_pack('ZZ')
    assert len(calls) == 1 and a == b                 # 2e appel servi du cache

    a['contracts'].append('x')                        # muter la copie de l'appelant
    d = terminal.options_pack('ZZ')
    assert d['contracts'] == []                       # cache non corrompu (deepcopy)

    terminal.options_pack('ZZ', fresh=True)
    assert len(calls) == 2                            # fresh=True reconstruit


def test_options_pack_cache_disabled(monkeypatch):
    import terminal
    monkeypatch.setenv('VERTEX_TICKER_TTL', '0')
    calls = []
    monkeypatch.setattr(terminal, '_options_pack_build',
                        lambda s: (calls.append(s), {'sym': s})[1])
    terminal._OPTPACK_CACHE.clear()
    terminal.options_pack('YY')
    terminal.options_pack('YY')
    assert len(calls) == 2                            # aucun cache
