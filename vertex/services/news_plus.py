"""
vertex/services/news_plus.py — NEWS MULTI-SOURCES + SENTIMENT.

1. `rss_news(sym)` — repli Google News RSS quand yfinance ne rend rien
   pour un titre (throttle, panne) : mêmes clés que le fil existant
   (title/link/publisher/time). Erreurs avalées → liste vide, jamais
   d'exception qui remonte dans la boucle.

2. `sentiment(text)` — score -1/0/+1 par heuristique lexicale FR/EN
   (fonctionne SANS clé IA, partout, gratuitement). Si l'IA est
   disponible (ANTHROPIC_API_KEY), les briefs l'affinent déjà — cette
   heuristique reste la base honnête et déterministe.

Analyse only.
"""

import re
import xml.dom.minidom as minidom

_POS = ('beat', 'beats', 'surge', 'soar', 'rally', 'record', 'upgrade', 'raises',
        'strong', 'growth', 'profit', 'wins', 'approval', 'breakthrough', 'buyback',
        'dépasse', 'bondit', 'record', 'relève', 'hausse', 'accord', 'approbation')
_NEG = ('miss', 'misses', 'fall', 'falls', 'plunge', 'drop', 'cut', 'cuts', 'downgrade',
        'lawsuit', 'probe', 'recall', 'layoff', 'warning', 'weak', 'loss', 'fraud', 'halt',
        'chute', 'plonge', 'abaisse', 'baisse', 'procès', 'enquête', 'rappel', 'avertissement')


def sentiment(text):
    """Score lexical : +1 positif · -1 négatif · 0 neutre/mixte."""
    t = ' ' + (text or '').lower() + ' '
    pos = sum(1 for w in _POS if w in t)
    neg = sum(1 for w in _NEG if w in t)
    return 1 if pos > neg else -1 if neg > pos else 0


def aggregate(items):
    """Sentiment agrégé par ticker : {sym: {'score': -1..1, 'n': N}}."""
    by = {}
    for it in items or []:
        s = it.get('sym')
        if not s:
            continue
        d = by.setdefault(s, {'sum': 0, 'n': 0})
        d['sum'] += it.get('senti', 0)
        d['n'] += 1
    return {s: {'score': round(d['sum'] / d['n'], 2) if d['n'] else 0, 'n': d['n']}
            for s, d in by.items()}


def parse_rss(xml_text, n=4):
    """Parse un flux RSS Google News → [{title, link, publisher, time}]."""
    out = []
    try:
        doc = minidom.parseString(xml_text)
        for item in doc.getElementsByTagName('item')[:n]:
            def _txt(tag):
                els = item.getElementsByTagName(tag)
                return els[0].firstChild.nodeValue.strip() if els and els[0].firstChild else ''
            title = _txt('title')
            if not title:
                continue
            # Google News suffixe " - Éditeur" au titre
            pub = _txt('source') or (title.rsplit(' - ', 1)[1] if ' - ' in title else '')
            out.append({'title': re.sub(r'\s+-\s+[^-]+$', '', title),
                        'link': _txt('link'), 'publisher': pub, 'time': _txt('pubDate')})
    except Exception:
        return []
    return out


def rss_news(sym, n=4, timeout=6):
    """Repli réseau : Google News RSS pour un ticker. [] en cas d'échec."""
    try:
        import requests
        r = requests.get('https://news.google.com/rss/search',
                         params={'q': '%s stock' % sym, 'hl': 'en-US', 'gl': 'US'},
                         timeout=timeout, headers={'User-Agent': 'VertexDesk/1.0'})
        if r.status_code != 200:
            return []
        return parse_rss(r.text, n=n)
    except Exception:
        return []


_TAG_RE = re.compile(r'<[^>]*>')


def _clean_text(s):
    """Neutralise tout HTML/JS d'un texte externe : balises retirées, méta-caractères
    échappés. Le résultat est sûr dans innerHTML, dans un attribut ET dans une
    chaîne JS inline côté client."""
    s = _TAG_RE.sub('', str(s))
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace('"', '&quot;').replace("'", '&#39;'))


def sanitize_news(items):
    """Assainit une liste d'items de news EXTERNES (yfinance/RSS/traduction) avant
    de la servir au client. XSS : les titres/liens de publishers tiers sont rendus
    en innerHTML côté client — on neutralise ici, au point unique de sortie.
    - title/fr/pub/publisher/sym/why : balises retirées + échappement complet ;
    - link : schéma http(s) obligatoire (sinon supprimé) + quotes/chevrons encodés
      (sûr en href="…" comme dans window.open('…'))."""
    out = []
    for it in (items or []):
        if not isinstance(it, dict):
            continue
        d = dict(it)
        for k in ('title', 'fr', 'pub', 'publisher', 'sym', 'why', 'time'):
            if d.get(k) is not None:
                d[k] = _clean_text(d[k])
        lk = d.get('link')
        if lk:
            lk = str(lk).strip()
            if not lk.lower().startswith(('http://', 'https://')):
                d['link'] = None
            else:
                d['link'] = (lk.replace('"', '%22').replace("'", '%27')
                               .replace('<', '%3C').replace('>', '%3E'))
        out.append(d)
    return out


__all__ = ['sentiment', 'aggregate', 'parse_rss', 'rss_news', 'sanitize_news']
