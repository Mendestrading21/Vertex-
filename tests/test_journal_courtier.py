"""LE JOURNAL DU COURTIER DIT UNE FOIS, PAS CINQUANTE — sans rien taire.

## Le défaut mesuré

Sans TWS ouvert, `ib_async` écrit deux lignes par tentative et par port, sur
quatre ports, pour quatre workers, en boucle. Relevé à un premier lancement
réel de `python -m vertex` sans session courtier : **168 lignes**
« API connection failed: ConnectionRefusedError » en une minute.

Le message est vrai. Il est en anglais, il est répété, et il décrit un état
parfaitement NORMAL : personne n'a de TWS ouvert la première fois qu'il lance
Vertex. Quelqu'un qui découvre le produit y voit une application cassée.

## La ligne que ce banc défend

Un filtre qui TAIT une erreur serait exactement ce que ce dépôt interdit.
Celui-ci n'en tait aucune : il garde la PREMIÈRE, traduite et complète, compte
les répétitions (`repetitions_tues()`), et laisse passer INTACT tout message
qui n'est pas cette répétition — un refus de permission, une collision de
`clientId`, une erreur de marché doivent rester lisibles mot pour mot.

L'état, lui, ne dépend pas du journal : il vit dans `etat()` et sur la page
Système → Connexions, qui dit « IBKR non activé (aucune session TWS/Gateway
détectée) ». Ce qui disparaît est la répétition, pas l'information.
"""
from __future__ import annotations

import logging

import pytest

from vertex.data_sources import ibkr_link as _link


@pytest.fixture()
def journal():
    """Un logger isolé portant le filtre, et le relevé de ce qui en sort."""
    sorties = []

    class _Collecte(logging.Handler):
        def emit(self, record):
            sorties.append((record.levelname, record.getMessage()))

    lg = logging.getLogger('banc.ib_async.%d' % id(sorties))
    lg.handlers = [_Collecte()]
    lg.setLevel(logging.DEBUG)
    lg.propagate = False
    filtre = _link._FiltreRepetitions()
    lg.addFilter(filtre)
    return lg, sorties, filtre


_REFUS = ("API connection failed: ConnectionRefusedError(111, "
          "\"Connect call failed ('127.0.0.1', 7496)\")")


# ── 1. Anti-vide : le motif réel est bien celui que le filtre vise ──────────

def test_le_motif_vise_est_celui_que_la_bibliotheque_ecrit():
    """Si `ib_async` changeait son libellé, le filtre laisserait tout passer et
    ce banc garderait une règle sans objet. On vise donc le texte RÉEL."""
    assert any(m in _REFUS for m in _link._REPETITIONS), (
        'le message réel du courtier ne correspond plus aux motifs filtrés : %s'
        % (_link._REPETITIONS,))


# ── 2. La première passe, traduite ; les suivantes sont comptées ────────────

def test_la_premiere_occurrence_passe_et_parle_francais(journal):
    lg, sorties, _f = journal
    lg.error(_REFUS)
    assert len(sorties) == 1, 'la première occurrence a été avalée'
    niveau, message = sorties[0]
    assert 'TWS' in message and 'Systeme' in message, (
        'le message de remplacement ne dit ni ce qui manque ni où regarder : %r'
        % message)
    assert 'ConnectionRefusedError' not in message, (
        'le remplacement recopie le type Python au lieu de l’expliquer')
    assert niveau == 'WARNING', (
        'un état normal est journalisé en ERROR : %s' % niveau)


def test_les_repetitions_sont_COMPTEES_et_non_perdues(journal):
    lg, sorties, f = journal
    for _ in range(60):
        lg.error(_REFUS)
        lg.error('Make sure API port on TWS/IBG is open')
    assert len(sorties) == 1, 'les répétitions passent encore : %d' % len(sorties)
    assert f.tues == 119, (
        'le compte des répétitions est faux (%d) — un filtre qui perd son '
        'compte tait vraiment quelque chose' % f.tues)


def test_le_compte_est_LISIBLE_depuis_le_module():
    """`repetitions_tues()` existe pour que le silence soit vérifiable."""
    assert isinstance(_link.repetitions_tues(), int)


# ── 3. Ce qui n'est PAS cette répétition passe intact ───────────────────────

@pytest.mark.parametrize('message', [
    'Error 326, reqId -1: Unable to connect as the client id is already in use',
    'Error 10197, reqId 3: No market data during competing live session',
    'Error 162: Historical Market Data Service error message',
    'peer closed connection',
])
def test_les_AUTRES_messages_du_courtier_passent_mot_pour_mot(journal, message):
    """Le contrôle le plus important. Un filtre trop large transformerait une
    collision de `clientId` ou un refus de permission en silence — et ces
    messages-là sont la seule explication d'un écran vide."""
    lg, sorties, _f = journal
    lg.error(message)
    assert [m for _n, m in sorties] == [message], (
        'un message du courtier a été modifié ou avalé : %r' % sorties)


def test_un_record_INFORMATABLE_ne_fait_pas_lever_le_filtre():
    """Un `record` dont le formatage est impossible ne doit pas faire LEVER le
    filtre : une exception ici emporterait la ligne qu'il devait laisser
    passer, et toutes les suivantes du même logger.

    Le filtre est éprouvé DIRECTEMENT, pas au travers d'un handler : un
    handler naïf casse de son côté sur le même record, et le banc mesurerait
    alors sa propre maladresse au lieu du filtre. Première version de ce
    contrôle, corrigée.
    """
    filtre = _link._FiltreRepetitions()
    record = logging.LogRecord('ib_async', logging.ERROR, __file__, 1,
                               'valeur %d', ('pas un entier',), None)
    assert filtre.filter(record) is True, (
        'un record informatable est REJETÉ par le filtre : la ligne serait '
        'perdue alors qu’elle n’a rien à voir avec la répétition visée')
    assert filtre.tues == 0


# ── 4. La pose est idempotente ──────────────────────────────────────────────

def test_poser_le_filtre_deux_fois_est_sans_effet():
    """`_start_workers` peut être appelé deux fois (import + `_start_app`) ;
    le second appel ne doit pas empiler un second filtre."""
    _link.calmer_le_journal_du_courtier()
    assert _link.calmer_le_journal_du_courtier() is False, (
        'la pose n’est pas idempotente : les filtres s’empileraient')
    poses = [f for f in logging.getLogger('ib_async').filters
             if isinstance(f, _link._FiltreRepetitions)]
    assert len(poses) == 1, '%d filtres empilés sur `ib_async`' % len(poses)


def test_le_demarrage_des_boucles_pose_bien_le_filtre():
    """Dénominateur : le filtre le mieux écrit ne sert à rien s'il n'est
    jamais installé."""
    import inspect

    import terminal
    src = inspect.getsource(terminal._demarrer_les_boucles)
    assert 'calmer_le_journal_du_courtier()' in src, (
        'les boucles démarrent sans poser le filtre : les 168 lignes '
        'reviendraient au premier lancement sans TWS')
    #  Et AVANT le premier thread, sinon les premières rafales passent.
    assert src.index('calmer_le_journal_du_courtier') < src.index('threading.Thread'), (
        'le filtre est posé APRÈS le démarrage des threads')
