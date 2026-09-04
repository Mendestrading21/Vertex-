"""Vertex Test 1.0 — LE PIPELINE REJETAIT DEUX ARTICLES SUR TROIS, ET LES DISAIT MALFORMÉS.

Suite directe de D-117, qui avait trouvé la même divergence de clé dans
`engines/events.py`. Le recensement complet montre qu'elle vivait à **trois**
endroits, et que le pire n'était pas celui déjà corrigé.

## Les trois producteurs, deux clés

| producteur | clé émise |
|---|---|
| `data_sources/ibkr_news` | `pub` |
| `options/legacy_engine` (fil yfinance) | `pub` |
| `services/news_plus.rss_news` | `publisher` |

## Le défaut, mesuré le 26 août 2026

`market/news_pipeline._valid()` exigeait `publisher` **ou** `source`. Les
dépêches IBKR et le fil yfinance n'ont ni l'un ni l'autre :

```text
articles fournis : 3        (1 IBKR, 1 yfinance, 1 RSS)
evenements gardes: 1
REJETES          : 2
```

**Deux sur trois perdus** — et c'est le pipeline qui alimente `importance`,
`positions_concerned`, la déduplication à corroborations et le brief quotidien.

Pire que la perte : le rejet était **compté comme une malformation**. Un
lecteur du champ `rejected` en conclut que la source envoie du déchet, pas
qu'on lit la mauvaise clé. Une statistique de qualité qui accuse la source d'un
défaut du consommateur est plus nuisible qu'un silence.

Et l'ironie tient : la dépêche écartée est celle du **courtier** — la source la
plus directe dont dispose le desk.

## La correction

`news_plus.nom_publieur` devient le lecteur unique. `events.py` abandonne la
copie privée qu'il avait reçue en D-117 : deux copies de cette règle
divergeraient au premier producteur ajouté.

Un article réellement **sans** publieur reste rejeté, et c'est juste : un
événement non attribuable n'est pas un événement.
"""
from __future__ import annotations

import pytest

from vertex.engines import events as E
from vertex.market.news_pipeline import collect
from vertex.services.news_plus import CLES_PUBLIEUR, nom_publieur

#: Les formes REELLES des trois producteurs, plus un article non attribuable.
ITEMS = [
    {'title': 'Apple Bites Into Record Q3', 'pub': 'DJ-N',
     'time': '2026-08-26 12:00', 'link': ''},                    # IBKR
    {'title': 'Apple lifts guidance', 'pub': 'Yahoo',
     'time': '2026-08-26 12:10', 'link': 'https://y.example/1'},  # yfinance
    {'title': 'Apple beats estimates', 'publisher': 'Reuters',
     'time': '2026-08-26 12:20', 'link': 'https://r.example/1'},  # RSS
    {'title': 'Sans publieur', 'time': '2026-08-26 12:25'},       # non attribuable
]


#  ═══════════  1. le lecteur unique  ══════════════════════════════════════════

@pytest.mark.parametrize('item,attendu', [
    ({'pub': 'DJ-N'}, 'DJ-N'),
    ({'publisher': 'Reuters'}, 'Reuters'),
    ({'source': 'interne'}, 'interne'),
    ({'prov': 'radar'}, 'radar'),
])
def test_les_QUATRE_formes_de_cle_sont_lues(item, attendu):
    assert nom_publieur(item) == attendu


def test_une_ABSENCE_reste_une_absence():
    """Inventer « externe » ici la ferait passer pour servie. C'est au
    consommateur de décider quoi faire d'un article non attribuable."""
    for vide in ({}, {'pub': ''}, {'pub': '   '}, {'pub': None}, None, 'texte'):
        assert nom_publieur(vide) == ''


def test_la_PREMIERE_cle_renseignee_gagne_et_l_ordre_est_stable():
    assert CLES_PUBLIEUR[0] == 'publisher'
    assert nom_publieur({'publisher': 'A', 'pub': 'B'}) == 'A'


def test_les_espaces_sont_retires():
    assert nom_publieur({'pub': '  DJ-N  '}) == 'DJ-N'


#  ═══════════  2. le pipeline ne rejette plus ce qu'il ne sait pas lire  ══════

def test_les_depeches_IBKR_et_yfinance_ne_sont_PLUS_rejetees():
    """Le défaut mesuré : 2 articles sur 3 perdus."""
    r = collect({'items': ITEMS}, portfolio_syms=['AAPL'])
    assert len(r['events']) == 3, r
    assert {e['source'] for e in r['events']} == {'DJ-N', 'Yahoo', 'Reuters'}


def test_un_article_SANS_publieur_reste_rejete():
    """Contre-épreuve : accepter tout ferait entrer des événements non
    attribuables — un événement sans source n'est pas un événement."""
    r = collect({'items': ITEMS}, portfolio_syms=['AAPL'])
    assert r['rejected'] == 1
    assert 'Sans publieur' not in {e['title'] for e in r['events']}


def test_le_champ_source_de_l_evenement_porte_le_VRAI_nom():
    """Il valait `''` pour tout ce qui venait du courtier."""
    r = collect({'items': [ITEMS[0]]}, portfolio_syms=[])
    assert r['events'][0]['source'] == 'DJ-N'


def test_un_titre_ou_une_heure_manquants_restent_rejetes():
    """Les deux autres conditions de validité ne bougent pas."""
    r = collect({'items': [{'pub': 'X', 'time': 't'},
                           {'title': 'T', 'pub': 'X'}]}, portfolio_syms=[])
    assert r['rejected'] == 2 and r['events'] == []


def test_la_CORROBORATION_devient_atteignable_pour_le_courtier():
    """Conséquence concrète : trois sources sur le même fait ne pouvaient pas
    se corroborer si deux étaient jetées avant la déduplication."""
    memes = [
        {'title': 'Apple beats Q3 estimates', 'pub': 'DJ-N', 'time': '1'},
        {'title': 'Apple beats Q3 estimates today', 'publisher': 'Reuters', 'time': '2'},
    ]
    r = collect({'items': memes}, portfolio_syms=[])
    assert sum(e.get('corroborations', 1) for e in r['events']) >= 2


#  ═══════════  3. un seul propriétaire, et events.py l'utilise  ═══════════════

def test_events_py_n_a_PLUS_sa_copie_privee_de_la_regle():
    """Elle lui avait été donnée en D-117. Deux copies divergent au premier
    producteur ajouté."""
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'engines'
           / 'events.py').read_text(encoding='utf-8')
    assert 'nom_publieur' in src
    assert "n.get('publisher') or n.get('pub')" not in src


def test_le_pipeline_ne_choisit_PLUS_sa_cle():
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'market'
           / 'news_pipeline.py').read_text(encoding='utf-8')
    assert 'nom_publieur' in src
    assert "item.get('publisher') or item.get('source')" not in src


def test_le_packet_et_le_pipeline_donnent_le_MEME_nom():
    """Deux surfaces qui nommeraient différemment la même dépêche rendraient
    les deux illisibles."""
    depeche = {'title': 'Apple Bites Into Record Q3', 'pub': 'DJ-N', 'time': 't'}
    du_pipeline = collect({'items': [depeche]}, portfolio_syms=[])['events'][0]['source']
    paquet = E.build('AAPL', news=[dict(depeche)], earnings=[], macro=[],
                     anomaly={}, as_of='2026-08-26T12:00:00Z')
    du_packet = [e for e in paquet['events'] if e['kind'] == 'news'][0]['source']
    assert du_pipeline == 'DJ-N'
    assert du_packet == 'news.DJ-N'
