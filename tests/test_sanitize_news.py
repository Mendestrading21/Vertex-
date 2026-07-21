"""SEC-01 — gardien anti-XSS de la sanitisation des news EXTERNES (règle produit n°5).

Les titres/liens de publishers tiers (yfinance/RSS/IBKR/traduction) sont rendus en
`innerHTML` côté client → ils DOIVENT être neutralisés au point unique de sortie
`news_plus.sanitize_news()`. Ce gardien verrouille : (1) le sanitiseur neutralise
réellement les charges XSS classiques ; (2) tout endpoint qui sert de la news externe
l'appelle. Régression = test rouge.
"""
from pathlib import Path

from vertex.services.news_plus import sanitize_news

ROOT = Path(__file__).resolve().parents[1]


def _blob(d):
    return ' '.join(str(v) for v in d.values() if v is not None).lower()


def test_sanitize_news_neutralise_les_scripts_et_handlers():
    out = sanitize_news([
        {'title': '<script>alert(1)</script>Titre'},
        {'fr': '<img src=x onerror=alert(1)>News'},
        {'publisher': '<svg/onload=alert(1)>Reuters'},
        {'why': '"><script>steal()</script>'},
    ])
    assert len(out) == 4
    for d in out:
        b = _blob(d)
        assert '<script' not in b
        assert '<img' not in b and '<svg' not in b
        assert 'onerror=' not in b and 'onload=' not in b
    # le TEXTE utile est conservé (on neutralise, on ne détruit pas l'information)
    assert 'titre' in _blob(out[0]) and 'news' in _blob(out[1])


def test_sanitize_news_liens_schema_http_uniquement():
    out = sanitize_news([
        {'title': 'a', 'link': 'javascript:alert(1)'},
        {'title': 'b', 'link': 'http://ex.com/x'},
        {'title': 'c', 'link': 'https://ex.com/"><script>'},
    ])
    assert out[0]['link'] is None                         # schéma non http(s) → supprimé
    assert out[1]['link'] == 'http://ex.com/x'            # http(s) conservé tel quel
    lk = out[2]['link'] or ''
    assert '"' not in lk and '<' not in lk and '>' not in lk  # quotes/chevrons encodés


def test_sanitize_news_tolere_entrees_invalides():
    # ne casse pas sur None / non-dict / liste vide (robustesse au point de sortie)
    assert sanitize_news(None) == []
    assert sanitize_news([None, 42, 'x']) == []


def test_tout_point_qui_sert_de_la_news_appelle_sanitize():
    """Règle produit n°5 : le contenu externe passe par sanitize_news AVANT d'être servi."""
    content = (ROOT / 'vertex' / 'app' / 'routes' / 'content.py').read_text(encoding='utf-8')
    term = (ROOT / 'terminal.py').read_text(encoding='utf-8')
    assert 'sanitize_news' in content, 'content.py (flux news) doit sanitiser'
    assert term.count('sanitize_news') >= 2, 'terminal.py doit sanitiser la news servie (scan + IBKR)'
