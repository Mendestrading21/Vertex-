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

_POS = ('beat', 'beats', 'surge', 'soar', 'rally', 'record', 'upgrade', 'raises',
        'strong', 'growth', 'profit', 'wins', 'approval', 'breakthrough', 'buyback',
        'dépasse', 'bondit', 'record', 'relève', 'hausse', 'accord', 'approbation')
_NEG = ('miss', 'misses', 'fall', 'falls', 'plunge', 'drop', 'cut', 'cuts', 'downgrade',
        'lawsuit', 'probe', 'recall', 'layoff', 'warning', 'weak', 'loss', 'fraud', 'halt',
        'chute', 'plonge', 'abaisse', 'baisse', 'procès', 'enquête', 'rappel', 'avertissement')


def sentiment(text):
    """Score lexical TERNAIRE : rend EXACTEMENT +1, -1 ou 0. Jamais autre chose.

    CONTRAT (lot 609, explicité après mesure) — le domaine est {-1, 0, +1} et
    rien d'autre. Ce n'est pas une intensité : trois mots positifs valent un
    seul, et « 3 positifs / 2 négatifs » rend la même chose que « 1 positif ».
    Le comparateur est `pos > neg`, pas une amplitude.

    POURQUOI ON NE LE REND PAS CONTINU. Une forme `(pos-neg)/(pos+neg)` donnerait
    des décimales — donc l'apparence d'une mesure — construites sur un lexique de
    22 mots positifs et 22 négatifs. Un « 0,333 » issu de trois mots-clés a l'air
    d'une mesure et n'en est pas une. Tant qu'on ne peut pas montrer que
    l'amplitude est FONDÉE, le ternaire est plus honnête que le continu.

    CE QUI EN DÉPEND, mesuré : `news_impact.score_importance` ajoute +5 quand le
    score est signé, ce qui participe au choix de l'« Actualité dominante »
    affichée sur `/`. La valeur a donc une conséquence visible — mais deux états
    utiles seulement (signé / neutre).

    Gardien : `tests/test_sentiment_contrat_lot609.py`.
    """
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


#: Plafond de taille d'un flux. Un RSS Google News fait quelques dizaines de
#: kilo-octets ; deux mega-octets laissent une marge confortable et bornent ce
#: qu'un flux hostile peut faire avaler au processus avant meme le parsing.
TAILLE_MAX_FLUX = 2 * 1024 * 1024


class FluxRefuse(ValueError):
    """Ce flux ne sera pas parse — et on dit pourquoi."""


def _items_surs(brut: str, n: int) -> list:
    """Les `n` premiers `<item>` d'un flux, lus par un parseur QUI REFUSE le DTD.

    ## La mesure qui justifie ce refus

    `parse_rss` lit du XML **distant et non fiable** (Google News). Il passait
    par `minidom.parseString`, dont l'expansion d'entites est active. Mesure du
    25 aout 2026, sur le vrai `parse_rss` :

    | niveaux | charge envoyee | titre rendu | facteur |
    |---|---:|---:|---:|
    | 3 | 233 o | 800 o | x100 |
    | 5 | 343 o | 80 000 o | x10 000 |
    | 6 | **398 o** | **800 000 o** | **x100 000** |

    Chaque niveau supplementaire multiplie par dix : neuf niveaux tiennent
    encore dans 500 octets et rendent 800 Mo. C'est un *billion laughs*, et il
    est atteignable depuis un flux que Vertex va chercher lui-meme.

    ## Pourquoi expat directement, et pas `ElementTree`

    Premiere tentative : poser les gestionnaires sur `ET.XMLParser().parser`.
    En Python 3.12, `XMLParser` est l'implantation C et n'expose PAS `.parser`
    — le `getattr(..., None)` rendait donc le durcissement **silencieusement
    inoperant**, et la mesure d'apres montrait l'expansion intacte. Un
    durcissement qui ne durcit rien est pire que pas de durcissement : il
    rassure. C'est la mesure qui l'a dit, pas la relecture.

    ## Pourquoi refuser le DOCTYPE, et pas seulement les entites

    Un flux RSS n'a jamais besoin d'une declaration de type. La refuser a la
    racine supprime l'expansion d'entites, les entites externes et les
    references recursives d'un seul geste — et se raisonne en une phrase, ce
    qu'une liste d'interdictions particulieres ne permet pas.

    ## Pourquoi pas `defusedxml`

    Une dependance nouvelle exige licence verifiee, version verrouillee, audit
    et rollback (CLAUDE.md). Le refus ci-dessus est plus STRICT que le defaut
    de `defusedxml` — qui interdit les entites mais parse encore le DTD — et
    tient dans la bibliotheque standard.
    """
    from xml.parsers import expat

    analyseur = expat.ParserCreate()

    def _refuser(*_a, **_k):
        raise FluxRefuse('declaration de type de document refusee')

    def _refuser_externe(*_a, **_k):
        raise FluxRefuse('entite externe refusee')

    analyseur.StartDoctypeDeclHandler = _refuser
    analyseur.EntityDeclHandler = _refuser
    analyseur.ExternalEntityRefHandler = _refuser_externe

    items, pile, courant, texte = [], [], None, []

    def _debut(nom, _attrs):
        nonlocal courant, texte
        local = nom.rsplit(':', 1)[-1]
        pile.append(local)
        if local == 'item' and len(items) < n:
            courant = {}
        texte = []

    def _texte(donnees):
        if courant is not None:
            texte.append(donnees)

    def _fin(nom):
        nonlocal courant, texte
        local = nom.rsplit(':', 1)[-1]
        if pile:
            pile.pop()
        if courant is None:
            texte = []
            return
        if local == 'item':
            items.append(courant)
            courant = None
        elif local not in courant:
            courant[local] = ''.join(texte).strip()
        texte = []

    analyseur.StartElementHandler = _debut
    analyseur.CharacterDataHandler = _texte
    analyseur.EndElementHandler = _fin
    analyseur.Parse(brut.encode('utf-8') if isinstance(brut, str) else brut, True)
    return items[:n]


def parse_rss(xml_text, n=4):
    """Parse un flux RSS Google News -> [{title, link, publisher, time}].

    Rend `[]` sur n'importe quelle entree invalide ou hostile, et ne leve
    jamais : c'est un repli reseau, il ne doit pas emporter l'appelant.
    """
    out = []
    try:
        brut = xml_text if isinstance(xml_text, str) else (xml_text or '')
        if len(brut) > TAILLE_MAX_FLUX:
            #  Refus AVANT parsing : un flux hostile ne doit pas etre lu du
            #  tout, pas seulement mal lu.
            return []
        for champs in _items_surs(brut, n):
            title = champs.get('title') or ''
            if not title:
                continue
            #  Google News suffixe « - Editeur » au titre.
            pub = champs.get('source') or (title.rsplit(' - ', 1)[1]
                                           if ' - ' in title else '')
            out.append({'title': re.sub(r'\s+-\s+[^-]+$', '', title),
                        'link': champs.get('link') or '',
                        'publisher': pub,
                        'time': champs.get('pubDate') or ''})
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


def dedupe_news(items):
    """Déduplication des news (SKYLER LOT 4) : même TITRE NORMALISÉ (casse,
    ponctuation, espaces) ou même LIEN → un seul item conservé (le premier,
    jamais réécrit). Ordre d'arrivée préservé ; entrées non-dict ignorées."""
    out, seen_titles, seen_links = [], set(), set()
    for it in (items or []):
        if not isinstance(it, dict):
            continue
        title_key = re.sub(r'[^a-z0-9]+', ' ', str(it.get('title') or '').lower()).strip()
        link = str(it.get('link') or '').strip()
        if (title_key and title_key in seen_titles) or (link and link in seen_links):
            continue
        if title_key:
            seen_titles.add(title_key)
        if link:
            seen_links.add(link)
        out.append(it)
    return out


__all__ = ['sentiment', 'aggregate', 'parse_rss', 'rss_news', 'sanitize_news', 'dedupe_news']
