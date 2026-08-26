"""Vertex 1.0 - UNE PAGE NE PAIE PAS CINQ FOIS LE MEME ALLER-RETOUR COURTIER.

Mesure d'origine, machine reelle avec TWS ouvert : afficher le Portefeuille
enchaine cinq routes qui lisent toutes le MEME etat de compte -

    /state 27 s | /report 3 s | /audit 0 s | /reconcile 0 s | /alerts 19 s
    total 49,5 s

Chaque appel remettait un travail en file chez le worker options, derriere
la rotation des chaines. Apres memoire courte : 28,0 s, et /alerts passe de
19 s a 6 ms.

Ce que ce fichier NE pretend pas garder : la premiere attente. Elle vient de
la file du worker, partagee avec les chaines d'options - un defaut
d'architecture, anterieur, qu'un cache ne resout pas. Le dire vaut mieux que
laisser croire que 25 s sont devenues normales.
"""
from __future__ import annotations

import re

from vertex.app.routes import positions_api


def _source():
    return open(positions_api.__file__, encoding="utf-8").read()


def test_les_positions_courtier_sont_tenues_entre_deux_routes():
    src = _source()
    assert "_pos_memo" in src and "_POS_TTL_S" in src, (
        "sans memoire, chaque route remet un travail en file pour lire le "
        "meme etat de compte")
    deb = src.index("def _ibkr_positions")
    corps = src[deb:src.index("def _quotes", deb)]
    assert "_POS_TTL_S" in corps, "la lecture des positions doit consulter la borne"


def test_les_cotations_de_positions_sont_tenues_de_la_meme_facon():
    src = _source()
    deb = src.index("def _quotes")
    corps = src[deb:deb + 2600]
    assert "_q_memo" in corps, (
        "/state et /alerts demandaient chacune la cotation du meme panier")
    assert "clef" in corps, (
        "la cle doit etre le panier : deux paniers differents ne partagent "
        "jamais une reponse")


def test_un_echec_n_est_jamais_memorise():
    """Retenir un echec le ferait durer toute la borne : un compte lisible
    passerait pour muet alors qu il ne l etait qu un instant."""
    src = _source()
    deb = src.index("def _ibkr_positions")
    corps = src[deb:src.index("def _quotes", deb)]
    assert "if valeur is not None:" in corps, (
        "seule une lecture aboutie doit etre retenue")
    corps2 = src[src.index("def _quotes"):][:2600]
    assert "if valeur:" in corps2, "une cotation vide ne doit pas etre retenue"


def test_la_borne_de_fraicheur_est_unique_et_assez_longue():
    """Une borne repartie dans cinq routes, c est cinq bornes qui
    divergeront. Et une borne plus courte que la latence qu elle corrige
    (~20 s) expire avant la route suivante : c est la faute mesuree du
    premier essai, a 2 s, qui n avait rien change (49,5 -> 48,2 s)."""
    src = _source()
    assert len(re.findall(r"_POS_TTL_S\s*=", src)) == 1, (
        "la borne doit etre definie a UN seul endroit")
    m = re.search(r"_POS_TTL_S\s*=\s*([\d.]+)", src)
    assert m and float(m.group(1)) >= 5.0, (
        "une borne trop courte devant la latence ne sert a rien")


def test_la_limite_non_corrigee_est_dite_dans_le_code():
    """Un correctif qui tait ce qu il ne corrige pas se lit comme un
    correctif complet."""
    src = _source()
    assert "worker options" in src, (
        "le code doit dire que la file du worker n est pas corrigee ici")
