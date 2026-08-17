"""SIGNAL OS · LOT 33 — L'ÉNUMÉRATION DES SORTIES N'EST PLUS MANUELLE.

Réserve n°1 du lot 32, ouverte en toutes lettres : « l'énumération reste
manuelle ». Le gardien du lot 177 nomme trois sorties de news ; le lot 32 en a
trouvé une quatrième — et il l'a trouvée par accident, en cherchant pourquoi une
mutation ne mordait pas. Un gardien qui liste des noms ne verra jamais la sortie
qu'on ajoutera demain.

Ce test renverse la charge de la preuve : il empoisonne les états partagés, puis
interroge **toutes** les routes GET de l'application. Rien à tenir à jour.

## Deux protections, et pourquoi elles ne sont pas décoratives

1. **Le réseau est coupé, et la coupure est PROUVÉE** avant tout balayage. La
   première version coupait `socket.socket` — et des requêtes sont quand même
   parties vers Yahoo : `yfinance` passe par `curl_cffi`, donc par libcurl, qui
   ouvre ses sockets en C. Aucun patch Python ne l'arrête. La coupure se fait
   donc aussi par les variables de proxy, pointées sur un port mort local.
   `prouver_la_coupure()` le vérifie avec un vrai client HTTP ; si la preuve
   échoue, le test **refuse de balayer** plutôt que de faire sortir des requêtes.
2. **Aucune écriture dans le dépôt** : la persistance est redirigée vers
   `tmp_path` (`/api/skyler/<sym>` journalise une séance — lot 389).

GET uniquement : rien n'est muté, READONLY n'est pas frôlé.

## L'anti-vacuité

Un balayage qui n'atteint rien passe tout. Deux garde-fous contre ce faux vert :
un plancher de routes réellement servies, et un témoin — `/news-feed` DOIT
montrer la charge **neutralisée**, ce qui prouve que le poison est bien arrivé
jusqu'aux sorties.
"""
import re

import pytest

from tools import mesurer_sorties_news as sonde


@pytest.fixture(scope='module')
def balayage(tmp_path_factory):
    import terminal
    from vertex.app.state import news_state, scan_state
    from vertex.services import persist

    sauve_items = news_state.get('items')
    sauve_base = persist._BASE_DIR
    persist._BASE_DIR = str(tmp_path_factory.mktemp('sorties'))
    sonde.couper_le_reseau()
    # SANS CECI, le minuteur de `interroger()` tue pytest : l'action par défaut
    # de SIGALRM est de terminer le processus. Mesuré — la suite sortait en 142
    # (128+14), et le `| tail` du shell masquait le code derrière un exit 0.
    sonde.armer_l_alarme()
    ok, detail = sonde.prouver_la_coupure()
    assert ok, ('coupure reseau NON PROUVEE (%s) — balayer sans elle ferait '
                'sortir de vraies requetes' % detail)

    news_state['items'] = [dict(sonde.CHARGE)]
    scan_state.setdefault('detail', {})['TSTQ'] = {'price': 100.0,
                                                   'news': [dict(sonde.CHARGE)]}
    client = terminal.app.test_client()
    yield client
    news_state['items'] = sauve_items
    scan_state.get('detail', {}).pop('TSTQ', None)
    persist._BASE_DIR = sauve_base


def test_le_temoin_prouve_que_le_poison_atteint_les_sorties(balayage):
    """Sans ce témoin, un balayage qui n'atteint rien passerait tout vert."""
    items = balayage.get('/news-feed').get_json()['items']
    assert items, 'la charge n\'a pas atteint /news-feed — balayage sans objet'
    assert 'alert(1)' in items[0]['title'], 'le titre injecte n\'est pas ressorti'
    assert '<script>' not in items[0]['title'], 'sortie connue non neutralisee'


def test_les_news_du_scan_sont_assainies_A_L_INGESTION_pas_a_la_sortie(balayage):
    """ANCRE D'UN FAIT MESURÉ, pas un jugement.

    Le balayage a d'abord accusé `/scan` et `/api/ticker/<sym>` : empoisonné
    directement, `scan_state['detail'][sym]['news']` ressortait brut. Vérifié
    avant d'accuser — en production ce store a **un seul écrivain**
    (`terminal.py`, boucle de scan) et il assainit AVANT de déposer. L'état que
    mon sondage fabriquait n'existe pas.

    Conséquence mesurée, et c'est elle qui compte : `/api/events/<sym>` et
    `/api/skyler/<sym>` rassainissent à la sortie ce qui l'est déjà — le
    résultat servi est DOUBLEMENT échappé (`&amp;#39;` au lieu de `&#39;`).
    Aucun consommateur ne rend ces titres aujourd'hui, donc rien n'est cassé à
    l'écran ; ce test ancre l'état pour que le jour où un rendu apparaît, on
    choisisse un domicile au lieu d'en découvrir deux."""
    from vertex.app.state import scan_state
    from vertex.services import news_plus
    assaini = news_plus.sanitize_news([{'title': "AT&T releve : Barron's y croit",
                                        'publisher': "Barron's", 'time': '10:00'}])
    assert assaini[0]['title'] == 'AT&amp;T releve : Barron&#39;s y croit'
    scan_state['detail']['TSTQ'] = {'price': 100.0, 'news': assaini}
    blob = balayage.get('/api/events/TSTQ').get_data(as_text=True)
    assert '&amp;amp;' in blob or '&amp;#39;' in blob, (
        'la sortie ne double plus l\'echappement : le domicile a change — '
        'verifier que les news du scan ne sont plus assainies qu\'UNE fois')


def test_aucune_route_get_ne_sert_de_balisage_externe(balayage):
    """LA propriété. Elle ne nomme aucune route : elle les interroge toutes."""
    import terminal
    coupables = []
    servies = 0
    for chemin in sonde.chemins_get(terminal.app):
        # Budget court : ce gardien tourne dans une suite de 40 s. Une route qui
        # n'a pas répondu en 2 s est comptée NON COUVERTE, jamais propre — et le
        # plancher ci-dessous interdit qu'il n'en reste presque plus.
        corps = sonde.interroger(balayage, chemin, secondes=2)
        if corps is None:
            continue                       # route injoignable : ne prouve rien
        servies += 1
        trouves = [m for m in sonde.MARQUEURS if m in corps]
        if trouves:
            coupables.append('%s → %s' % (chemin, ', '.join(trouves)))
    assert servies >= 100, (
        'balayage trop maigre (%d routes servies) — un test qui n\'atteint rien '
        'passe toujours' % servies)
    assert not coupables, (
        '%d route(s) servent du balisage externe vivant :\n  %s'
        % (len(coupables), '\n  '.join(coupables)))
