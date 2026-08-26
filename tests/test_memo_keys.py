"""PRF-03 — complétude & non-ambiguïté des clés de mémoïsation (memos critiques).

Un memo doit inclure DANS SA CLÉ toutes les entrées qui changent sa sortie, sinon il
sert une valeur périmée en silence. Les briefs FR (`company_brief`, `fr_desc`, `fr_news`)
sont des memos CRITIQUES : une collision de clé rendrait le profil/description/actus d'une
entreprise pour une AUTRE — violation directe de « données réelles uniquement ».

Ce gardien verrouille :
1. déterminisme : même entrée → clé byte-identique (le cache renvoie exactement la valeur mise) ;
2. non-collision : deux entrées DISTINCTES qui se concatènent à l'identique (`('AB','Cfoo')`
   vs `('ABC','foo')`) obtiennent des clés DIFFÉRENTES — l'ancienne clé `md5(sym+summary)`
   sans séparateur échouait ici ;
3. complétude : chaque partie qui change la sortie change la clé.

Régression (clé qui perd une entrée, séparateur retiré) = test rouge.
"""
import pytest

from vertex.ai import briefs


# ── 1. déterminisme byte-identique de la clé ───────────────────────────────
def test_cle_deterministe_byte_identique():
    k1 = briefs._content_key('brief', 'AAPL', 'Fabrique des iPhone.')
    k2 = briefs._content_key('brief', 'AAPL', 'Fabrique des iPhone.')
    assert k1 == k2


# ── 2. non-collision : concaténation ambiguë → clés distinctes ─────────────
def test_pas_de_collision_par_concatenation():
    # 'AB'+'Cfoo' == 'ABC'+'foo' == 'ABCfoo' : l'ancienne clé sans séparateur collisionnait.
    k1 = briefs._content_key('brief', 'AB', 'Cfoo')
    k2 = briefs._content_key('brief', 'ABC', 'foo')
    assert k1 != k2


@pytest.mark.parametrize('prefix', ['brief', 'desc', 'news'])
def test_chaque_partie_change_la_cle(prefix):
    base = briefs._content_key(prefix, 'AAPL', 'texte')
    assert briefs._content_key(prefix, 'MSFT', 'texte') != base   # le symbole compte
    assert briefs._content_key(prefix, 'AAPL', 'autre') != base   # le contenu compte


def test_prefixes_isoles():
    # deux memos différents (profil vs description) sur les mêmes entrées ne se mélangent pas.
    assert briefs._content_key('brief', 'AAPL', 'x') != briefs._content_key('desc', 'AAPL', 'x')


# ── 3. au niveau du memo : pas de fuite entre entrées ambiguës ─────────────
def test_company_brief_lit_le_cache_byte_identique(monkeypatch):
    monkeypatch.setattr(briefs, 'available', lambda: False)  # aucun appel réseau
    briefs._cache.clear()
    key = briefs._content_key('brief', 'AAPL', 'Fabrique des iPhone.')
    briefs._cache[key] = {'sells': 'iPhone', 'moat': 'écosystème'}
    r1 = briefs.company_brief('AAPL', 'Fabrique des iPhone.')
    r2 = briefs.company_brief('AAPL', 'Fabrique des iPhone.')
    assert r1 == r2 == {'sells': 'iPhone', 'moat': 'écosystème'}
    briefs._cache.clear()


def test_company_brief_pas_de_fuite_entre_entrees_qui_se_concatenent(monkeypatch):
    monkeypatch.setattr(briefs, 'available', lambda: False)
    briefs._cache.clear()
    # on empoisonne la clé de ('AB','Cfoo')…
    briefs._cache[briefs._content_key('brief', 'AB', 'Cfoo')] = {'sells': 'MAUVAIS'}
    # …('ABC','foo') se concatène pareil mais DOIT avoir sa propre clé → rien de périmé.
    assert briefs.company_brief('ABC', 'foo') == {}
    briefs._cache.clear()
