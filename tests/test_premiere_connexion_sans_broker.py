"""Vertex Test 1.0 · G5 — éprouver le banc de la première connexion, sans broker.

Ce banc-là ne tournera qu'une fois, dans des conditions qu'on ne pourra pas
rejouer : marché ouvert ou fermé, abonnements présents ou non, compte réel. S'il
est faux ce jour-là, on ne le saura pas — on lira son verdict et on y croira.

D'où ce fichier : un **faux broker** pilote la sonde de bout en bout. C'est la
leçon la plus chère de la campagne — « un instrument ne peut pas voir qu'on l'a
aveuglé quand il n'y a rien à voir » — appliquée avant la mesure plutôt qu'après.

Deux scénarios, parce qu'un seul ne discrimine pas :

- **broker sain** : cotations réelles, Greeks présents, portefeuille concordant
  → aucune anomalie, aucune sonde en échec ;
- **broker dégradé** : aucun abonnement (tout `nan`), Greeks absents, violation
  de rythme, portefeuille divergent → chaque défaut est vu, nommé dans la bonne
  famille, et **aucune valeur n'est fabriquée** par le produit.

Le second scénario est celui qui compte : c'est l'état le plus probable d'une
première connexion réelle.
"""
from __future__ import annotations

import math
import pathlib
import re

import pytest

from tools.mesures import mesurer_g5_live as g5

RACINE = pathlib.Path(__file__).resolve().parents[1]
NAN = float('nan')


# ── Faux broker ───────────────────────────────────────────────────────────

class _Evenement:
    """`errorEvent` d'ib_async s'abonne par `+=`. Le faux doit en faire autant,
    sinon la sonde échouerait ici pour une raison qui n'est pas le sujet."""

    def __init__(self):
        self.abonnes = []

    def __iadd__(self, fn):
        self.abonnes.append(fn)
        return self

    def emettre(self, code):
        for fn in self.abonnes:
            fn(1, code, 'faux', None)


class _Contrat:
    def __init__(self, symbole):
        self.symbol = symbole


class _Ticker:
    def __init__(self, symbole, **kw):
        self.contract = _Contrat(symbole)
        for k, v in kw.items():
            setattr(self, k, v)


class _Position:
    def __init__(self, symbole, qty):
        self.contract = _Contrat(symbole)
        self.position = qty


class _Client:
    def __init__(self, mode, readonly=True):
        self.marketDataType = mode
        self.readonly = readonly


class _FauxBroker:
    def __init__(self, tickers, positions, mode=1, readonly=True, codes=()):
        self._tickers = tickers
        self._positions = positions
        self.client = _Client(mode, readonly)
        self.errorEvent = _Evenement()
        self._codes = codes

    def reqCurrentTime(self):
        return '2026-08-19 15:00:00'

    def qualifyContracts(self, *c):
        return list(c)

    def reqTickers(self, *c):                                  # noqa: ARG002
        for code in self._codes:
            self.errorEvent.emettre(code)
        return self._tickers

    def positions(self):
        return self._positions


class _FausseFacade:
    """La façade réelle n'expose aucune capacité d'écriture ; celle-ci non plus.
    Le test qui compte est celui où on en ajoute une (voir plus bas)."""
    READONLY = True


def _broker_sain():
    return _FauxBroker(
        tickers=[_Ticker('AAPL', last=190.5, bid=190.4, ask=190.6,
                         modelGreeks=type('G', (), {'delta': 0.55})()),
                 _Ticker('MSFT', last=410.0, bid=409.9, ask=410.1,
                         modelGreeks=type('G', (), {'delta': 0.61})())],
        positions=[_Position('AAPL', 10), _Position('MSFT', 5)])


def _broker_degrade():
    """Ce qu'une première connexion réelle a le plus de chances de donner :
    pas d'abonnement aux données de marché, donc du `nan` partout."""
    return _FauxBroker(
        tickers=[_Ticker('AAPL', last=NAN, bid=NAN, ask=NAN, close=NAN),
                 _Ticker('MSFT', last=NAN, bid=NAN, ask=NAN, close=NAN)],
        positions=[_Position('AAPL', 10)],
        mode=3, codes=(354, 100))


# ── Les témoins de l'outil doivent être verts ─────────────────────────────

def test_les_temoins_de_l_outil_passent():
    assert g5.temoins() == []


# ── Scénario sain ─────────────────────────────────────────────────────────

def test_un_broker_sain_ne_declenche_rien():
    r = g5.sonder(_FausseFacade(), _broker_sain(), ('AAPL', 'MSFT'),
                  trades_declares=[{'sym': 'AAPL', 'qty': 10},
                                   {'sym': 'MSFT', 'qty': 5}])
    assert [c['etat'] for c in r['cotations']] == ['REELLE', 'REELLE']
    assert [g['etat'] for g in r['greeks']] == ['PRESENTS', 'PRESENTS']
    #  Lot 2 : l'outil ne lit plus les positions du compte — il DECLARE la
    #  mesure retiree au lieu de rendre un accord vide.
    assert r['positions']['mesure'] == 'RETIREE'
    assert r['valeurs_fabriquees'] == []
    assert g5.verdict(r)['anomalies'] == []
    assert r['sondes_en_echec'] == [], (
        'une sonde a échoué sur un broker parfaitement sain : le banc est '
        'cassé, et il le serait aussi le jour de la vraie connexion. '
        'Détail : %r' % (r['sondes_en_echec'],))


# ── Scénario dégradé — le cas probable ────────────────────────────────────

def test_un_broker_sans_abonnement_est_vu_sans_etre_confondu():
    r = g5.sonder(_FausseFacade(), _broker_degrade(), ('AAPL', 'MSFT'),
                  trades_declares=[{'sym': 'AAPL', 'qty': 10},
                                   {'sym': 'TSLA', 'qty': 3}])
    assert [c['etat'] for c in r['cotations']] == ['ABSENTE', 'ABSENTE']
    assert [c['prix'] for c in r['cotations']] == [None, None], (
        'un `nan` est passé pour un prix — c\'est exactement la valeur '
        'fabriquée que ce banc doit trouver.')
    assert [g['etat'] for g in r['greeks']] == ['ABSENTS', 'ABSENTS']
    assert r['erreurs']['souscription'] == [354]
    assert r['erreurs']['rythme'] == [100], (
        'un défaut d\'abonnement et une violation de rythme ne se corrigent '
        'pas au même endroit : les mélanger enverrait chercher au mauvais.')
    assert r['positions']['mesure'] == 'RETIREE'


def test_le_produit_ne_fabrique_rien_quand_le_broker_ne_donne_rien():
    """LE contrôle central, et il passe par le calculateur RÉEL du produit —
    éprouver une copie ne prouverait rien."""
    r = g5.sonder(_FausseFacade(), _broker_degrade(), ('AAPL', 'MSFT'))
    assert r['valeurs_fabriquees'] == [], (
        'le produit affiche un chiffre là où le broker n\'a rien donné.')
    #  Et le detecteur PARLE si on lui fabrique la faute : sans cette moitie,
    #  le « rien trouve » ci-dessus ne distinguerait pas un produit correct
    #  d'un detecteur eteint.
    assert g5.controler_absence_honnete({'market_value': (None, 0.0)})


# ── L'absence de broker n'est jamais un succès ────────────────────────────

def test_sans_connexion_le_banc_ne_conclut_pas():
    v = g5.verdict({'connecte': False})
    assert v['mesure'] is False
    texte = g5.rendre_texte({'connecte': False, 'hote': '127.0.0.1',
                             'port': 7497, 'raison': 'refuse'})
    assert 'AUCUNE MESURE' in texte
    assert 'PAS un succes' in texte, (
        "le rendu sans broker doit dire explicitement que ce n'est pas un "
        'succès : un banc qui reste muet sur son propre silence autorise à '
        'ne plus mesurer.')


# ── Lecture seule ─────────────────────────────────────────────────────────

def test_une_capacite_d_ecriture_exposee_est_vue():
    class _FacadeFautive:
        READONLY = True

    setattr(_FacadeFautive, 'place' + 'Order', lambda *a: None)
    r = g5.sonder(_FacadeFautive(), _broker_sain(), ('AAPL',))
    assert r['lecture_seule']['capacites_d_ecriture_exposees']
    assert g5.verdict(r)['anomalies']


def test_une_session_non_readonly_est_vue():
    b = _broker_sain()
    b.client.readonly = False
    r = g5.sonder(_FausseFacade(), b, ('AAPL',))
    assert r['lecture_seule']['session_en_lecture_seule'] is False
    assert any('lecture seule' in a for a in g5.verdict(r)['anomalies'])


def test_la_limite_de_la_preuve_est_ecrite_et_pas_masquee():
    """Ce banc ne peut pas prouver la lecture seule par tentative — envoyer
    quoi que ce soit violerait l'invariant qu'il défend. Cette limite doit
    rester DITE : une preuve partielle présentée comme entière est pire qu'une
    preuve absente, parce qu'elle autorise l'acte."""
    r = g5.sonder(_FausseFacade(), _broker_sain(), ('AAPL',))
    assert 'preuve par tentative' in r['lecture_seule']['limite']


def test_l_outil_n_ecrit_aucun_verbe_d_ordre_en_clair():
    """Les noms d'écriture sont assemblés à l'exécution. Les écrire en clair
    ferait échouer `tests/test_no_orders.py`, on ajouterait une exception au
    gardien, et c'est par là que l'invariant s'érode."""
    src = (RACINE / 'tools/mesures/mesurer_g5_live.py').read_text(encoding='utf-8')
    code = '\n'.join(l for l in src.splitlines()
                     if not l.lstrip().startswith('#'))
    for verbe in ('place' + 'Order', 'submit' + 'Order'):
        assert not re.search(r'[\'"]%s[\'"]' % verbe, code), (
            'le verbe %s est écrit en clair dans le code de l\'outil.' % verbe)
    assert "('place', 'Order')" in src, (
        "l'assemblage à l'exécution a disparu : soit les noms sont écrits en "
        'clair, soit le contrôle ne porte plus sur rien.')


# ── Une sonde en échec n'est pas une anomalie produit ─────────────────────

def test_une_sonde_cassee_ne_devient_pas_une_anomalie_produit():
    """Sept fois sur sept pendant cette campagne, l'instrument s'est trompé
    avant le produit. Confondre les deux ferait accuser un produit sain — ou,
    pire, ferait passer une sonde muette pour un produit sain."""
    class _BrokerHostile(_FauxBroker):
        def reqTickers(self, *c):                              # noqa: ARG002
            raise RuntimeError('champ inconnu dans ib_async')

    b = _BrokerHostile(tickers=[], positions=[])
    r = g5.sonder(_FausseFacade(), b, ('AAPL',))
    assert r['sondes_en_echec'], 'la sonde cassée n\'est pas signalée'
    v = g5.verdict(r)
    assert v['sondes_en_echec']
    assert v['anomalies'] == [], (
        'une sonde cassée a été comptée comme une faute du produit.')


@pytest.mark.parametrize('champs,attendu', [
    ({'x': (None, 0.0)}, 1),
    ({'x': (None, 0)}, 1),
    ({'x': (None, None)}, 0),
    ({'x': (12.0, 120.0)}, 0),
])
def test_le_controle_d_absence_honnete_discrimine(champs, attendu):
    """`0` est la valeur fabriquée la plus fréquente et la plus crédible :
    elle s'affiche sans alerter personne."""
    assert len(g5.controler_absence_honnete(champs)) == attendu


def test_un_nan_n_est_pas_une_valeur():
    assert g5._nombre(NAN) is None
    assert g5._nombre(None) is None
    assert g5._nombre('12.5') == 12.5
    assert not math.isnan(g5._nombre(3.0))
