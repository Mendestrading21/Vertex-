"""tests/test_news_plus_lot102.py — SKYLER LOT 102 : gardien XSS des news figé.

Trou réel de couverture : vertex/services/news_plus.py — la règle n°5 du
projet (« tout texte externe passe par sanitize_news avant d'être servi,
rendu en innerHTML ») n'était testée qu'indirectement au point de sortie
d'une route (test_events_timeline). Le gardien lui-même (échappement,
liens javascript:, balises cassées), le sentiment lexical, le parse RSS
et la déduplication n'avaient AUCUN test direct.
Caractérisations nées vertes (dites) — moteur INTACT, aucun réseau.
"""
from vertex.services import news_plus as np


# ------------------------------------------------------------ sanitize (XSS)

def test_script_tags_stripped_and_metacharacters_escaped():
    items = [{'title': '<script>alert(1)</script>Apple & "Co" <b>up</b>',
              'sym': "AA'PL"}]
    out = np.sanitize_news(items)
    t = out[0]['title']
    assert '<' not in t and '>' not in t and '"' not in t and "'" not in t
    assert 'alert(1)Apple &amp; &quot;Co&quot; up' == t, (
        'balises retirées PUIS méta-caractères échappés — sûr en innerHTML')
    assert out[0]['sym'] == 'AA&#39;PL'


def test_unclosed_tag_cannot_smuggle_html():
    # Balise jamais fermée : la regex ne la voit pas, l'échappement la neutralise.
    out = np.sanitize_news([{'title': '<img src=x onerror=alert(1)'}])
    assert out[0]['title'].startswith('&lt;img'), (
        'même une balise cassée sort inerte — le < est encodé')


def test_dangerous_link_schemes_are_dropped_https_kept():
    items = [{'title': 'a', 'link': 'javascript:alert(1)'},
             {'title': 'b', 'link': 'data:text/html,<script>x</script>'},
             {'title': 'c', 'link': '  HTTPS://ex.com/a?q="x"&r=\'y\'<z>  '}]
    out = np.sanitize_news(items)
    assert out[0]['link'] is None and out[1]['link'] is None, (
        'seul http(s) sort — jamais un schéma exécutable')
    lk = out[2]['link']
    assert lk.startswith('HTTPS://ex.com/') and '%22' in lk and '%27' in lk
    assert '<' not in lk and '>' not in lk        # sûr en href ET window.open


def test_every_documented_field_is_sanitized():
    """LOT 32 — la docstring de `sanitize_news` énumère les champs assainis ;
    seuls title/fr/publisher/sym étaient éprouvés. Retirer `why` ou `time` de la
    liste passait les 3 159 tests. Ce test tient la liste ENTIÈRE : un champ
    qu'on cesse d'assainir se voit ici, qu'une route le serve déjà ou non."""
    charge = '<b>x</b>'
    champs = ('title', 'fr', 'pub', 'publisher', 'sym', 'why', 'time')
    out = np.sanitize_news([{k: charge for k in champs}])[0]
    oublies = [k for k in champs if out[k] != 'x']
    assert not oublies, 'champs non assainis : %s' % oublies


def test_sanitize_skips_non_dicts_and_preserves_other_keys():
    out = np.sanitize_news([None, 'texte', 42, {'title': 'ok', 'senti': -1}])
    assert len(out) == 1 and out[0]['senti'] == -1
    assert np.sanitize_news(None) == []


# ----------------------------------------------------------------- sentiment

def test_sentiment_lexical_fr_en_and_neutral():
    assert np.sentiment('Apple beats estimates, shares surge') == 1
    assert np.sentiment('Le titre plonge après une enquête') == -1
    assert np.sentiment('beat announced but lawsuit filed') == 0   # mixte 1-1
    assert np.sentiment('') == 0 and np.sentiment(None) == 0


def test_aggregate_rounds_and_skips_items_without_symbol():
    items = [{'sym': 'AAPL', 'senti': 1}, {'sym': 'AAPL', 'senti': 0},
             {'sym': 'AAPL'}, {'senti': -1}]
    agg = np.aggregate(items)
    assert agg == {'AAPL': {'score': 0.33, 'n': 3}}, (
        'senti absent compte 0, item sans sym ignoré, arrondi à 2 décimales')


# ------------------------------------------------------------------ parse_rss

def test_parse_rss_strips_publisher_suffix_and_caps_items():
    xml = ('<rss><channel>'
           + ''.join(f'<item><title>Titre {i} - Éditeur{i}</title>'
                     f'<link>https://ex.com/{i}</link>'
                     f'<pubDate>D{i}</pubDate></item>' for i in range(6))
           + '</channel></rss>')
    out = np.parse_rss(xml, n=4)
    assert len(out) == 4                              # cap n respecté
    assert out[0]['title'] == 'Titre 0' and out[0]['publisher'] == 'Éditeur0'
    assert out[0]['link'] == 'https://ex.com/0'


def test_parse_rss_garbage_xml_returns_empty_never_raises():
    assert np.parse_rss('pas du xml <<<') == []
    assert np.parse_rss('<rss><channel><item><title></title></item></channel></rss>') == []


# ---------------------------------------------------------------- dedupe_news

def test_dedupe_by_normalized_title_and_link_keeps_first():
    items = [{'title': 'Apple beats!', 'link': 'https://a.com/1'},
             {'title': 'APPLE — BEATS', 'link': 'https://a.com/2'},   # même titre normalisé
             {'title': 'Autre news', 'link': 'https://a.com/1'},      # même lien
             {'title': 'Troisième', 'link': 'https://a.com/3'},
             'pas-un-dict']
    out = np.dedupe_news(items)
    assert [i['title'] for i in out] == ['Apple beats!', 'Troisième'], (
        'premier conservé tel quel, ordre préservé, non-dicts ignorés')
