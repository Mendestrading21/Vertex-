"""Vertex 1.0 · G5 — TROIS SOURCES DE P&L, ET AUCUNE NE GAGNE EN SILENCE.

Mesure prise sur le compte réel le 24 août 2026, TWS port 7496, lecture seule :

| source | P&L non réalisé |
|---|---:|
| `accountSummary` (tag `UnrealizedPnL`) | **1 024,03 USD** |
| `reqPnL` (souscription temps réel) | **928,57 USD** |
| somme des lignes de `portfolio()` | **1 024,03 USD** |

**95,46 USD d'écart** entre deux sources du même courtier, pour le même compte,
au même instant. Ce n'est pas une anomalie de Vertex : `reqPnL` et
`accountSummary` ne calculent pas sur la même base — c'est une particularité
connue d'IBKR.

Ce qui serait un défaut de Vertex, en revanche, c'est d'en **choisir une en
silence**. Le P&L affiché deviendrait vrai ou faux selon la source retenue,
sans que rien à l'écran ne permette de le savoir.

Ce banc garde le comportement inverse : les trois sont lues, l'écart est
**nommé et chiffré**, et la réconciliation ne tranche pas — elle rapporte.
"""
from __future__ import annotations

import pytest

from vertex.data_sources import ibkr_compte as CPT


#  ═════════════════  1. le résumé de compte, sans ligne BASE  ═════════════════

class _Ligne:
    def __init__(self, tag, value, currency):
        self.tag, self.value, self.currency = tag, value, currency


def test_une_vraie_devise_l_emporte_TOUJOURS_sur_la_ligne_BASE():
    """IBKR publie certains tags deux fois : dans la devise réelle et en
    `BASE`. Retenir `BASE` mélangerait des montants convertis avec des montants
    natifs, et le total ne voudrait plus rien dire."""
    lignes = [_Ligne("UnrealizedPnL", "1024.03", "BASE"),
              _Ligne("UnrealizedPnL", "1024.03", "USD"),
              _Ligne("NetLiquidation", "7850.36", "USD")]
    r = CPT.resume_depuis_lignes(lignes)
    assert r["valeurs"]["UnrealizedPnL"]["devise"] == "USD"
    assert r["valeurs"]["NetLiquidation"]["valeur"] == 7850.36


def test_l_ordre_d_arrivee_ne_change_pas_le_resultat():
    """Contre-épreuve : si `BASE` arrive en second et écrase, le défaut serait
    invisible la moitié du temps."""
    a = CPT.resume_depuis_lignes([_Ligne("X", "1", "USD"), _Ligne("X", "9", "BASE")])
    b = CPT.resume_depuis_lignes([_Ligne("X", "9", "BASE"), _Ligne("X", "1", "USD")])
    assert a["valeurs"]["X"] == b["valeurs"]["X"]
    assert a["valeurs"]["X"]["devise"] == "USD"


def test_un_tag_ABSENT_rend_None_jamais_zero():
    """Un zéro est une affirmation. Dire « pas de liquidités » quand on ne sait
    pas fausserait tout calcul de capacité."""
    r = CPT.resume_depuis_lignes([_Ligne("NetLiquidation", "100", "USD")])
    assert r["valeurs"].get("TotalCashValue") is None
    assert CPT.valeur(r, "TotalCashValue") is None
    assert CPT.valeur(r, "NetLiquidation") == 100.0


def test_une_valeur_illisible_est_ecartee_et_COMPTEE():
    r = CPT.resume_depuis_lignes([_Ligne("X", "n/a", "USD"),
                                  _Ligne("Y", "2.5", "USD")])
    assert r["valeurs"].get("X") is None
    assert r["ecartes"] == ["X"]
    assert CPT.valeur(r, "Y") == 2.5


def test_l_identifiant_de_compte_est_MASQUE():
    """Un numéro de compte ne doit pas se retrouver dans un journal, un
    artefact ou une capture d'écran."""
    r = CPT.resume_depuis_lignes([], compte="U10360059")
    assert "10360059" not in str(r)
    assert r["compte"] == CPT.MASQUE


#  ═══════════  2. la réconciliation : nommer l'écart, pas le lisser  ══════════

def test_les_trois_sources_concordantes_ne_signalent_rien():
    """Une réconciliation qui crie sur un compte sain serait ignorée dès la
    première fausse alerte."""
    r = CPT.reconcilier_pnl(resume=1024.03, temps_reel=1024.03,
                            portefeuille=1024.03, vertex=1024.03)
    assert r["concordant"] is True
    assert r["ecarts"] == []


def test_l_ecart_REEL_mesure_est_nomme_et_chiffre():
    """Les chiffres du 24 août 2026, sur le compte réel."""
    r = CPT.reconcilier_pnl(resume=1024.03, temps_reel=928.57,
                            portefeuille=1024.03, vertex=None)
    assert r["concordant"] is False
    noms = {e["paire"] for e in r["ecarts"]}
    assert ("resume", "temps_reel") in noms
    ecart = [e for e in r["ecarts"] if e["paire"] == ("resume", "temps_reel")][0]
    assert round(ecart["ecart"], 2) == 95.46
    assert ecart["source_a"] == 1024.03 and ecart["source_b"] == 928.57


def test_la_reconciliation_ne_DESIGNE_aucun_gagnant():
    """Le point du lot. Choisir une source en silence rendrait le P&L affiché
    vrai ou faux selon un arbitrage que personne n'a pris."""
    r = CPT.reconcilier_pnl(resume=1024.03, temps_reel=928.57,
                            portefeuille=1024.03, vertex=None)
    assert "valeur_retenue" not in r
    assert "gagnant" not in r
    assert r["note"] and "ne tranche pas" in r["note"].lower()


def test_une_source_ABSENTE_n_est_pas_un_ecart():
    """Vertex n'ayant pas calculé son P&L, l'absence ne doit pas se compter
    comme une divergence — sinon toute réconciliation partielle crierait."""
    r = CPT.reconcilier_pnl(resume=1024.03, temps_reel=1024.03,
                            portefeuille=None, vertex=None)
    assert r["concordant"] is True
    assert r["sources_absentes"] == ["portefeuille", "vertex"]


def test_toutes_les_sources_absentes_ne_CONCLUENT_pas():
    """Zéro source ne prouve pas la concordance : elle prouve qu'on n'a rien
    mesuré. Rendre `concordant: True` serait un mensonge confortable."""
    r = CPT.reconcilier_pnl(resume=None, temps_reel=None,
                            portefeuille=None, vertex=None)
    assert r["concordant"] is None
    assert "aucune source" in r["note"].lower()


def test_la_tolerance_est_EXPLICITE_et_ne_masque_pas_un_ecart_reel():
    """Une tolérance existe — les arrondis de centimes ne sont pas des
    divergences — mais elle est dite, et 95 USD la dépassent largement."""
    proche = CPT.reconcilier_pnl(resume=1024.03, temps_reel=1024.02,
                                 portefeuille=None, vertex=None)
    assert proche["concordant"] is True
    assert proche["tolerance"] == CPT.TOLERANCE_DEFAUT
    loin = CPT.reconcilier_pnl(resume=1024.03, temps_reel=928.57,
                               portefeuille=None, vertex=None,
                               tolerance=1.0)
    assert loin["concordant"] is False


def test_une_tolerance_absurde_ne_peut_pas_tout_faire_concorder():
    """Une tolérance qui avale n'importe quel écart transformerait la
    réconciliation en décoration."""
    with pytest.raises(ValueError, match="tolérance"):
        CPT.reconcilier_pnl(resume=1.0, temps_reel=1000.0,
                            portefeuille=None, vertex=None,
                            tolerance=CPT.TOLERANCE_MAX + 1)


#  ═══════════════  3. la provenance : d'où vient chaque chiffre  ══════════════

def test_chaque_source_de_pnl_est_NOMMEE_dans_le_rapport():
    """« Le P&L » n'existe pas : il y a le P&L du résumé, celui de la
    souscription temps réel, celui des lignes, et celui de Vertex. Un rapport
    qui ne les nomme pas empêche de comprendre un écart."""
    r = CPT.reconcilier_pnl(resume=1.0, temps_reel=2.0,
                            portefeuille=3.0, vertex=4.0)
    assert set(r["sources"]) == {"resume", "temps_reel", "portefeuille", "vertex"}
    for nom, v in r["sources"].items():
        assert v is not None, nom


def test_le_module_ne_porte_aucune_methode_d_ordre():
    from pathlib import Path
    src = Path(CPT.__file__).read_text(encoding="utf-8")
    for interdit in ("placeOrder", "cancelOrder", "reqIds"):
        assert interdit not in src, interdit


def test_les_metadonnees_textuelles_sont_ecartees_sans_etre_des_erreurs():
    """Sur le compte reel, `ecartes` contient AccountType, Currency,
    RealCurrency — des tags TEXTUELS legitimes. La liste n'est pas un journal
    d'erreurs ; elle sert a voir le jour ou un tag NUMERIQUE y tombe."""
    lignes = [_Ligne("AccountType", "INDIVIDUAL", "USD"),
              _Ligne("Currency", "USD", "USD"),
              _Ligne("NetLiquidation", "7850.36", "USD")]
    r = CPT.resume_depuis_lignes(lignes)
    assert r["ecartes"] == ["AccountType", "Currency"]
    assert CPT.valeur(r, "NetLiquidation") == 7850.36


def test_un_tag_a_la_fois_textuel_et_numerique_garde_le_NOMBRE():
    """IBKR publie parfois le meme tag deux fois. Si l'une des deux lignes est
    lisible, la valeur existe — l'ecarter serait perdre une donnee reelle."""
    r = CPT.resume_depuis_lignes([_Ligne("X", "n/a", "BASE"),
                                  _Ligne("X", "12.5", "USD")])
    assert CPT.valeur(r, "X") == 12.5
    assert r["ecartes"] == []


#  ═══════  4. la ligne fautive : un total ne dit pas OU regarder  ═════════════

def test_la_ligne_qui_diverge_est_NOMMEE_avec_ses_deux_valorisations():
    """Mesure du 24 aout 2026 : le total divergeait de 270,13 et UNE seule
    ligne en etait responsable — URA, marquee 7 760,00 par Vertex et 8 032,84
    par le courtier."""
    r = CPT.reconcilier_positions_pnl(
        vertex_positions=[{'symbol': 'URA', 'unrealized_pnl': 751.19,
                           'market_value': 7760.00},
                          {'symbol': 'AAPL', 'unrealized_pnl': 2.09,
                           'market_value': 311.09}],
        broker_positions=[{'symbol': 'URA', 'unrealized_pnl': 1024.03,
                           'market_value': 8032.84},
                          {'symbol': 'AAPL', 'unrealized_pnl': 2.09,
                           'market_value': 311.09}])
    assert len(r['lignes_divergentes']) == 1
    d = r['lignes_divergentes'][0]
    assert d['symbole'] == 'URA'
    assert round(d['ecart'], 2) == 272.84
    assert d['valeur_vertex'] == 7760.00 and d['valeur_courtier'] == 8032.84
    assert "vient de la" in r['note'].replace('à', 'a')


def test_les_trois_familles_d_ecart_ne_sont_PAS_confondues():
    """Une ligne mal valorisee, une ligne suivie a tort et une ligne ignoree
    n'appellent pas la meme correction."""
    r = CPT.reconcilier_positions_pnl(
        vertex_positions=[{'symbol': 'A', 'unrealized_pnl': 1.0},
                          {'symbol': 'FANTOME', 'unrealized_pnl': 5.0}],
        broker_positions=[{'symbol': 'A', 'unrealized_pnl': 9.0},
                          {'symbol': 'IGNOREE', 'unrealized_pnl': 3.0}])
    assert [x['symbole'] for x in r['lignes_divergentes']] == ['A']
    assert r['absentes_chez_le_courtier'] == ['FANTOME']
    assert r['absentes_chez_vertex'] == ['IGNOREE']


def test_un_pnl_ABSENT_d_un_cote_n_est_pas_une_divergence():
    """On ne peut pas comparer ce qui n'a pas ete calcule. Compter l'absence
    comme un ecart ferait crier la reconciliation sur toute position non cotee."""
    r = CPT.reconcilier_positions_pnl(
        vertex_positions=[{'symbol': 'A', 'unrealized_pnl': None}],
        broker_positions=[{'symbol': 'A', 'unrealized_pnl': 9.0}])
    assert r['lignes_divergentes'] == []


def test_des_lignes_concordantes_ne_signalent_rien():
    r = CPT.reconcilier_positions_pnl(
        vertex_positions=[{'symbol': 'A', 'unrealized_pnl': 1.0}],
        broker_positions=[{'symbol': 'a', 'unrealized_pnl': 1.0}])
    assert r['lignes_divergentes'] == []
    assert r['absentes_chez_vertex'] == [] and r['absentes_chez_le_courtier'] == []
    assert 'aucune ligne' in r['note']


def test_une_fermeture_de_souscription_en_echec_est_CONSIGNEE():
    """Une souscription `reqPnL` qu'on croit fermee alors qu'elle tient encore
    consomme une ligne de donnees chez le courtier, et la suivante se voit
    refuser — sans que rien ne relie ce refus a l'oubli qui l'a cause."""
    assert hasattr(CPT, 'DERNIERE_FERMETURE_EN_ECHEC')
    from pathlib import Path
    src = Path(CPT.__file__).read_text(encoding='utf-8')
    deb = src.index('def pnl_temps_reel')
    corps = src[deb:deb + 2000]
    assert 'DERNIERE_FERMETURE_EN_ECHEC' in corps, (
        "l'echec d'annulation doit etre consigne, pas avale")
    assert 'cancelPnL' in corps, 'la souscription doit etre annulee'
