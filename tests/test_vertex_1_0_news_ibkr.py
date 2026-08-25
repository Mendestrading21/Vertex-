"""Vertex 1.0 - LES DEPECHES VIENNENT DU COURTIER, PAS DU WEB.

Le compte est abonne a des fournisseurs professionnels ; le fil les
ignorait et lisait yfinance puis un repli RSS. Mesure du jour sur
U8000001 : 12 symboles servis en 8,9 s sur UNE session, fil a 45 articles,
provenance « depeches ibkr » sans aucun repli web.

Le piege que ce fichier garde surtout : `reqHistoricalNews` REJETTE la
requete entiere (erreur 321) si un seul fournisseur de la liste n est pas
abonne. Interroger les huit codes rendus par `reqNewsProviders` donnait
donc ZERO depeche alors que quatre repondaient.
"""
from __future__ import annotations

from vertex.data_sources import ibkr_news, ibkr_link


def test_seuls_les_fournisseurs_mesures_sont_interroges():
    """DJNL rend systematiquement zero, et DJ-RTA/RTE/RTG ne sont pas
    abonnes : les garder couterait un aller-retour par symbole pour rien,
    et un seul non-abonne fait tomber toute la requete."""
    assert set(ibkr_news.FOURNISSEURS) == {"BRFG", "DJ-N", "DJ-RT", "BRFUPDN"}
    for interdit in ("DJ-RTA", "DJ-RTE", "DJ-RTG", "DJNL"):
        assert interdit not in ibkr_news.FOURNISSEURS


def test_chaque_fournisseur_est_interroge_SEPAREMENT():
    """Le defaut mesure : la liste complete passee en une fois rendait
    erreur 321 et zero depeche. Un refus doit en isoler UN."""
    src = open(ibkr_news.__file__, encoding="utf-8").read()
    assert "for code in FOURNISSEURS:" in src, (
        "les fournisseurs doivent etre interroges un par un")
    deb = src.index("for code in FOURNISSEURS:")
    corps = src[deb:deb + 700]
    assert "continue" in corps, "un refus doit isoler un fournisseur, pas tous"


def test_le_prefixe_technique_est_retire_du_titre():
    """`reqHistoricalNews` prefixe ses titres — « {A:800015:L:en}Apple... ».
    Affiche tel quel, le fil commencerait par une accolade."""
    assert ibkr_news._titre("{A:800015:L:en}Apple Bites Into Record Q3") == (
        "Apple Bites Into Record Q3")
    assert ibkr_news._titre("Sans prefixe") == "Sans prefixe"


def test_le_role_news_a_son_propre_identifiant():
    """La boucle news tourne toutes les 60 s, celle du scan par salves de
    plusieurs minutes : partager un identifiant les ferait s evincer."""
    ids = ibkr_link.CLIENT_IDS
    assert "news" in ids
    assert len(set(ids.values())) == len(ids), "deux roles partagent un identifiant"


def test_un_titre_sans_depeche_est_ABSENT_du_lot():
    """Present avec une liste vide, il passerait pour servi et le repli
    n irait jamais le chercher."""
    src = open(ibkr_news.__file__, encoding="utf-8").read()
    deb = src.index("def depeches_lot")
    corps = src[deb:]
    assert "if art:" in corps, (
        "seul un symbole REELLEMENT servi doit entrer dans le lot")


def test_un_lot_vide_ne_touche_pas_au_courtier():
    assert ibkr_news.depeches_lot([]) == {}


def test_la_boucle_news_met_le_courtier_en_tete_et_garde_le_repli():
    import terminal
    src = open(terminal.__file__, encoding="utf-8").read()
    deb = src.index("def _news_loop")
    corps = src[deb:deb + 4200]
    assert "depeches_lot" in corps, "le courtier doit etre interroge en premier"
    assert "rss_news" in corps, (
        "le repli web doit rester : ce que le courtier ne sert pas doit "
        "descendre la chaine, pas disparaitre de l ecran")
    assert "source_detail" in corps, (
        "la provenance doit compter les contributeurs : un fil bascule "
        "entierement sur le web se lirait sinon comme avant")
