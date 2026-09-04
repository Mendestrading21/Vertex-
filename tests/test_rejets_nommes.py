"""Vertex Test 1.0 — LE REJET DISAIT COMBIEN, JAMAIS POURQUOI.

`market/news_pipeline` promet, dans son propre docstring :

> il n'invente jamais un événement : titre + source + heure requis, sinon rejeté
> (le rejet est **compté, pas masqué**).

Un compte sans cause est pourtant une forme de masquage. La preuve est dans le
lot précédent : `rejected: 2` sur trois articles se lisait « la source envoie du
déchet », alors que le consommateur lisait la mauvaise clé (D-122). La
statistique a envoyé chercher le défaut du mauvais côté — pendant des semaines,
puisque rien ne journalise les rejets par cause.

Ce lot complète la promesse du module : le rejet dit désormais **pourquoi**.

## Deux compteurs, deux unités, et il faut le dire

- `rejected` compte les **items**.
- `rejets_par_cause` compte les **conditions**, et un item peut en manquer
  plusieurs.

Leur somme n'a donc pas à être égale. `rejets_note` le déclare, plutôt que de
laisser un lecteur conclure à une incohérence — un chiffre qu'on croit faux est
aussi inutile qu'un chiffre absent.

## Une seule implantation de la règle

`_valid` **dérive** de `raisons_rejet`. Deux implantations de la même condition
divergeraient au premier ajout, et c'est exactement le défaut que ce programme
paie depuis D-117.
"""
from __future__ import annotations

import pytest

from vertex.market.news_pipeline import CAUSES_REJET, collect, raisons_rejet


#  ═══════════  1. chaque cause est nommée  ════════════════════════════════════

@pytest.mark.parametrize('item,attendu', [
    ('pas un dict', ['non_dict']),
    (None, ['non_dict']),
    ({'pub': 'X', 'time': 't'}, ['titre_absent']),
    ({'title': 'T', 'time': 't'}, ['publieur_absent']),
    ({'title': 'T', 'pub': 'X'}, ['date_absente']),
    ({'title': '   ', 'pub': 'X', 'time': 't'}, ['titre_absent']),
])
def test_la_cause_du_rejet_est_NOMMEE(item, attendu):
    assert raisons_rejet(item) == attendu


def test_un_item_VALIDE_n_a_aucune_raison():
    """Contre-épreuve : une fonction qui trouve toujours une raison rejetterait
    tout le fil."""
    assert raisons_rejet({'title': 'T', 'pub': 'X', 'time': 't'}) == []
    assert raisons_rejet({'title': 'T', 'publisher': 'X', 'date': 'd'}) == []


def test_un_item_peut_CUMULER_les_causes():
    """Ne garder que la première ferait apparaître la seconde seulement une
    fois la première corrigée : deux passes au lieu d'une."""
    assert raisons_rejet({'title': 'Rien que le titre'}) == \
        ['publieur_absent', 'date_absente']


def test_toutes_les_causes_declarees_sont_ATTEIGNABLES():
    """Une cause qu'aucun item ne peut déclencher est du décor."""
    atteintes = set()
    for item in ('x', {'pub': 'X', 'time': 't'}, {'title': 'T', 'time': 't'},
                 {'title': 'T', 'pub': 'X'}):
        atteintes.update(raisons_rejet(item))
    assert atteintes == set(CAUSES_REJET)


#  ═══════════  2. le compte par cause est servi  ══════════════════════════════

ETAT = {'items': [
    {'title': 'Bon article', 'pub': 'DJ-N', 'time': 't'},
    {'title': 'Sans publieur', 'time': 't'},
    {'pub': 'X', 'time': 't'},
    {'title': 'Sans date', 'pub': 'X'},
    {'title': 'Rien que le titre'},
    'pas un dict',
]}


def test_le_pipeline_SERT_le_detail_des_rejets():
    r = collect(ETAT, portfolio_syms=[])
    assert r['rejets_par_cause'] == {'non_dict': 1, 'titre_absent': 1,
                                     'publieur_absent': 2, 'date_absente': 2}


def test_les_champs_HISTORIQUES_sont_conserves():
    """Une correction qui casse ses consommateurs n'est pas une correction."""
    r = collect(ETAT, portfolio_syms=[])
    for cle in ('events', 'rejected', 'raw_count', 'updated'):
        assert cle in r, cle
    assert r['rejected'] == 5 and r['raw_count'] == 6


def test_les_DEUX_compteurs_ne_comptent_pas_la_meme_chose_et_le_DISENT():
    """La somme par cause dépasse le nombre d'items rejetés dès qu'un item
    cumule. Sans la note, un lecteur conclurait à une incohérence — et un
    chiffre qu'on croit faux est aussi inutile qu'un chiffre absent."""
    r = collect(ETAT, portfolio_syms=[])
    assert sum(r['rejets_par_cause'].values()) > r['rejected']
    assert r['rejets_note'] and 'plusieurs conditions' in r['rejets_note']


def test_un_fil_SAIN_ne_compte_aucun_rejet():
    """Contre-épreuve : des compteurs toujours non nuls ne mesureraient rien."""
    r = collect({'items': [{'title': 'T', 'pub': 'X', 'time': 't'}]}, portfolio_syms=[])
    assert r['rejected'] == 0
    assert set(r['rejets_par_cause'].values()) == {0}
    assert len(r['events']) == 1


def test_un_fil_VIDE_ne_fait_pas_tomber_le_pipeline():
    for vide in ({}, {'items': []}, {'items': None}):
        r = collect(vide, portfolio_syms=[])
        assert r['rejected'] == 0 and r['events'] == []


#  ═══════════  2 bis. la seconde perte, trouvée par ce banc  ═══════════════════

def test_une_manchette_COURTE_n_est_plus_jetee_en_silence():
    """Défaut trouvé en écrivant ce lot : un article passait la validation puis
    **disparaissait**, après elle, sans que personne le compte.

    `news_dedup._key` ne garde que les tokens de trois caractères hors mots
    vides. Un titre qui n'en produit aucun donnait une clé vide, et l'événement
    était jeté. Ce ne sont pas des cas théoriques — ce sont des manchettes
    financières ordinaires, où les tickers font deux lettres :

        'AI up 5%'  'BP up'  'GM & F up 3%'   -> tous perdus

    Sur neuf titres réalistes, **quatre perdus sans trace**.
    """
    from vertex.market.news_dedup import deduplicate
    titres = ['AI up 5%', 'BP up', 'GM & F up 3%', 'Apple beats estimates']
    ev = [{'title': t, 'source': 'X', 'time': '1'} for t in titres]
    out = deduplicate(ev)
    assert len(out) == len(titres), out
    assert {o['title'] for o in out} == set(titres)


def test_un_evenement_sans_cle_se_DECLARE():
    """Le conserver ne suffit pas : un lecteur doit savoir qu'il n'a pas été
    rapproché, sinon il le croira unique alors qu'on n'en sait rien."""
    from vertex.market.news_dedup import CLE_ABSENTE, deduplicate
    out = deduplicate([{'title': 'BP up', 'source': 'X', 'time': '1'}])
    assert out[0]['dedup'] == CLE_ABSENTE
    assert out[0]['corroborations'] == 1


def test_les_VRAIS_doublons_sont_toujours_fusionnes():
    """Contre-épreuve : tout conserver ferait du fil une liste de redites."""
    from vertex.market.news_dedup import deduplicate
    out = deduplicate([
        {'title': 'Apple beats Q3 estimates', 'source': 'A', 'time': '1'},
        {'title': 'Apple estimates beats Q3', 'source': 'B', 'time': '2'}])
    assert len(out) == 1
    assert out[0]['corroborations'] == 2
    assert 'dedup' not in out[0]


def test_le_pipeline_ne_perd_plus_l_article_court():
    """Bout en bout : validé puis servi, au lieu de validé puis évaporé."""
    r = collect({'items': [{'title': 'BP up', 'pub': 'DJ-N', 'time': 't'}]},
                portfolio_syms=[])
    assert r['rejected'] == 0
    assert len(r['events']) == 1, 'valide puis disparu'


#  ═══════════  3. une seule implantation de la règle  ═════════════════════════

def test_la_validite_DERIVE_des_raisons():
    """Deux implantations de la même condition divergeraient au premier ajout
    — c'est le défaut que ce programme paie depuis D-117."""
    from vertex.market import news_pipeline as P
    assert P._valid({'title': 'T', 'pub': 'X', 'time': 't'}) is True
    assert P._valid({'title': 'T', 'time': 't'}) is False
    import inspect
    assert 'raisons_rejet' in inspect.getsource(P._valid)


def test_le_defaut_de_D_122_serait_desormais_LISIBLE():
    """Le cas exact qui a envoyé chercher du mauvais côté : trois articles, deux
    rejetés. Avant, `rejected: 2` sans plus. Maintenant, la cause est nommée —
    et si la clé était de nouveau mal lue, `publieur_absent` le dirait."""
    trois = {'items': [
        {'title': 'IBKR', 'pub': 'DJ-N', 'time': 't'},
        {'title': 'yfinance', 'pub': 'Yahoo', 'time': 't'},
        {'title': 'RSS', 'publisher': 'Reuters', 'time': 't'},
    ]}
    r = collect(trois, portfolio_syms=[])
    assert r['rejected'] == 0, 'D-122 doit rester corrige'
    assert r['rejets_par_cause']['publieur_absent'] == 0
