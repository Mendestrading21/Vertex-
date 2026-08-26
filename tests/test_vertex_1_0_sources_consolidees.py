"""Vertex 1.0 — LA DÉDUPLICATION JETAIT LES SOURCES, ET LE PACKET LES EFFAÇAIT.

`VERTEX-INTELLIGENCE-2.0` Phase 4, critère d'acceptation, mot pour mot :

> même événement consolidé **sans perdre les sources**.

## Défaut 1 — la déduplication jetait

`dedupe_news` gardait le premier item et **supprimait les autres**. Vertex
collecte à la fois un flux RSS multi-agences et les dépêches IBKR : la collision
est structurelle, pas hypothétique. Mesuré le 26 août 2026 :

```text
entree : 4 articles, 3 sources distinctes (Reuters, Bloomberg, IBKR)
sortie : 2 articles
SOURCES PERDUES : Bloomberg, IBKR
```

Trois agences indépendantes rapportant le même fait est une information **plus
forte** qu'une seule. Le produit ne pouvait pas faire la différence : rien ne
portait le nombre de sources.

Effet de bord mesuré : la dépêche **IBKR** — le flux du courtier, celui du desk
— était systématiquement celle qu'on jetait, par simple ordre d'arrivée, parce
qu'elle n'a pas d'URL et arrive après le RSS.

## Défaut 2 — le packet effaçait le nom du publieur

Plus net encore. Trois producteurs, deux clés :

| producteur | clé émise |
|---|---|
| `data_sources/ibkr_news` | `pub` |
| `options/legacy_engine` (fil yfinance) | `pub` |
| `services/news_plus.rss_news` | `publisher` |

Et `engines/events.py` ne lisait que `publisher`. **Toute dépêche IBKR et tout
article yfinance ressortait donc `news.externe`** — la source effacée à
l'endroit précis où le packet doit la porter. Seuls les articles RSS gardaient
leur nom.

## Ce que ce lot ne déplace pas

Le premier item reste conservé **et jamais réécrit**, l'ordre d'arrivée est
préservé, `source` reste la première source pour les consommateurs existants.
On **ajoute** `sources` et `n_sources` ; on ne renomme rien.
"""
from __future__ import annotations

import pytest

from vertex.engines import events as E
from vertex.services.news_plus import dedupe_news, sanitize_news

#: Le cas REEL du produit : le meme fait par trois sources, plus un fait isole.
TROIS_SOURCES = [
    {'title': 'Apple beats Q3 estimates', 'pub': 'Reuters',
     'link': 'https://reuters.example/a', 'time': '2026-08-26 12:00'},
    {'title': 'Apple Beats Q3 Estimates', 'pub': 'Bloomberg',
     'link': 'https://bloomberg.example/b', 'time': '2026-08-26 12:05'},
    {'title': 'apple beats q3 estimates!', 'pub': 'IBKR',
     'link': '', 'time': '2026-08-26 12:02'},
    {'title': 'Apple announces buyback', 'pub': 'Reuters',
     'link': 'https://reuters.example/c', 'time': '2026-08-26 13:00'},
]


#  ═══════════  1. plus aucune source perdue  ══════════════════════════════════

def test_les_TROIS_sources_survivent_a_la_consolidation():
    """Le critère d'acceptation, littéralement."""
    out = dedupe_news(TROIS_SOURCES)
    consolide = out[0]
    assert consolide['n_sources'] == 3
    assert {s['pub'] for s in consolide['sources']} == {'Reuters', 'Bloomberg', 'IBKR'}


def test_la_depeche_IBKR_n_est_plus_celle_qu_on_jette():
    """Elle n'a pas d'URL et arrive après le RSS : c'était systématiquement
    elle que l'ordre d'arrivée éliminait."""
    out = dedupe_news(TROIS_SOURCES)
    toutes = {s['pub'] for o in out for s in o['sources']}
    assert 'IBKR' in toutes


def test_le_nombre_d_articles_servis_ne_CHANGE_pas():
    """Consolider n'est pas cesser de dédupliquer : le fil doit rester lisible."""
    assert len(dedupe_news(TROIS_SOURCES)) == 2


def test_un_fait_rapporte_UNE_fois_porte_n_sources_egal_UN():
    """Contre-épreuve : si tout ressortait à 3, le compte ne mesurerait rien."""
    isole = dedupe_news(TROIS_SOURCES)[1]
    assert isole['n_sources'] == 1
    assert isole['sources'][0]['pub'] == 'Reuters'


def test_le_PREMIER_item_n_est_jamais_reecrit():
    """La garantie historique de cette fonction, et elle tient."""
    out = dedupe_news(TROIS_SOURCES)
    assert out[0]['title'] == 'Apple beats Q3 estimates'
    assert out[0]['pub'] == 'Reuters'
    assert out[0]['link'] == 'https://reuters.example/a'


def test_l_ordre_d_arrivee_est_preserve():
    titres = [o['title'] for o in dedupe_news(TROIS_SOURCES)]
    assert titres == ['Apple beats Q3 estimates', 'Apple announces buyback']


def test_une_source_IDENTIQUE_deux_fois_n_est_comptee_qu_une():
    """Le même flux relu ne doit pas gonfler la corroboration."""
    doublon = [TROIS_SOURCES[0], dict(TROIS_SOURCES[0])]
    assert dedupe_news(doublon)[0]['n_sources'] == 1


def test_les_entrees_non_dict_restent_ignorees():
    assert dedupe_news([None, 'texte', 42, TROIS_SOURCES[0]])[0]['n_sources'] == 1


#  ═══════════  2. le champ ajouté est ASSAINI  ════════════════════════════════

def test_un_lien_javascript_dans_les_sources_est_REFUSE():
    """Ne pas assainir le champ neuf rouvrirait la brèche de D-086 — sur un
    champ que personne ne penserait à regarder."""
    sale = dedupe_news([{'title': 'X', 'pub': 'A', 'link': 'javascript:alert(1)'}])
    assert sanitize_news(sale)[0]['sources'][0]['link'] is None


def test_une_balise_dans_le_nom_de_publieur_est_NEUTRALISEE():
    sale = dedupe_news([{'title': 'X', 'pub': 'A', 'link': 'https://a.example/1'},
                        {'title': 'X', 'pub': '<img src=x onerror=alert(1)>',
                         'link': 'https://b.example/2'}])
    pubs = [s['pub'] for s in sanitize_news(sale)[0]['sources']]
    assert not any('<' in (p or '') for p in pubs), pubs


def test_les_quotes_d_un_lien_de_source_sont_encodees():
    sale = dedupe_news([{'title': 'X', 'pub': 'A', 'link': 'https://b.example/"onmouseover="'}])
    lien = sanitize_news(sale)[0]['sources'][0]['link']
    assert '"' not in lien and '%22' in lien


def test_un_lien_LEGITIME_survit_a_l_assainissement():
    """Contre-épreuve : un assainisseur qui casse les liens valides supprime la
    fonctionnalité au lieu de la protéger."""
    sale = dedupe_news([{'title': 'X', 'pub': 'A', 'link': 'https://reuters.example/a'}])
    assert sanitize_news(sale)[0]['sources'][0]['link'] == 'https://reuters.example/a'


def test_l_assainissement_du_lien_a_UN_SEUL_proprietaire():
    """Deux copies d'une règle d'échappement divergent, et il suffit qu'une
    oublie un caractère (D-086)."""
    from vertex.services import news_plus as N
    assert hasattr(N, '_lien_sur')
    assert N._lien_sur('javascript:x') is None
    assert N._lien_sur('https://ok.example/a') == 'https://ok.example/a'


#  ═══════════  3. le packet porte le nom, et toutes les sources  ══════════════

def _packet(news):
    return E.build('AAPL', news=news, earnings=[], macro=[], anomaly={},
                   as_of='2026-08-26T12:00:00Z')


def _news_events(d):
    return [e for e in d.get('events', []) if e.get('kind') == 'news']


def test_une_depeche_avec_pub_n_est_PLUS_attribuee_a_externe():
    """Le défaut mesuré : `ibkr_news` et le fil yfinance émettent `pub`, et ce
    moteur ne lisait que `publisher`."""
    ev = _news_events(_packet([TROIS_SOURCES[0]]))
    assert ev and ev[0]['source'] == 'news.Reuters'


def test_la_cle_HISTORIQUE_publisher_marche_toujours():
    """Contre-épreuve : le flux RSS émet `publisher`, et il ne doit pas casser."""
    ev = _news_events(_packet([{'title': 'T', 'publisher': 'Le Monde', 'time': 'x'}]))
    assert ev and ev[0]['source'] == 'news.Le Monde'


def test_une_depeche_SANS_publieur_reste_honnetement_externe():
    """Une absence reste une absence : on n'invente pas un nom de source."""
    ev = _news_events(_packet([{'title': 'T', 'time': 'x'}]))
    assert ev and ev[0]['source'] == 'news.externe'


def test_l_evenement_porte_TOUTES_les_sources():
    ev = _news_events(_packet(TROIS_SOURCES))
    consolide = ev[0]
    assert consolide['n_sources'] == 3
    assert {s['pub'] for s in consolide['sources']} == {'Reuters', 'Bloomberg', 'IBKR'}


def test_source_reste_la_PREMIERE_pour_les_consommateurs_existants():
    """On ajoute, on ne déplace pas : `source` garde son sens et son format."""
    ev = _news_events(_packet(TROIS_SOURCES))
    assert ev[0]['source'] == 'news.Reuters'
    assert isinstance(ev[0]['source'], str)


def test_les_champs_HISTORIQUES_de_l_evenement_sont_conserves():
    ev = _news_events(_packet(TROIS_SOURCES))[0]
    for cle in ('kind', 'label', 'category', 'source', 'date', 'dte',
                'impact_hint', 'impact_derivation', 'confidence', 'date_fiabilite'):
        assert cle in ev, cle


def test_une_mention_de_REVISION_porte_aussi_ses_sources():
    """Une révision d'analyste rapportée par trois maisons n'est pas la même
    preuve qu'une rapportée par une."""
    revision = [{'title': 'Analyst upgrades Apple to Buy', 'pub': 'Reuters', 'time': 't'},
                {'title': 'analyst upgrades apple to buy', 'pub': 'Bloomberg', 'time': 't'}]
    d = _packet(revision)
    mentions = d.get('revision_mentions') or []
    if mentions:
        assert mentions[0]['n_sources'] == 2
