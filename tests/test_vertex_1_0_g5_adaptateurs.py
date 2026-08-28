"""Vertex 1.0 · G5 — LES QUATRE ADAPTATEURS IBKR, ÉPROUVÉS SANS TWS.

L'audit du 24 août 2026 a mesuré une zone aveugle que la couverture globale de
87 % masquait : `ibkr_contracts`, `ibkr_market_data`, `ibkr_option_chain` et
`ibkr_positions` étaient à **0 %**. La session TWS réelle prouvait la connexion
et les rôles ; elle ne faisait exécuter aucune ligne de ces quatre fichiers.

Ce banc les exécute pour de bon, sur une capture **réelle et anonymisée** prise
sur le port 7496 (`tests/fixtures/ibkr/g5_capture.json`). Deux familles :

- **contrat** : les fonctions pures — validation, normalisation, provenance —
  qui décident si une donnée est exploitable ou absente ;
- **rejeu** : les fonctions qui parlent au broker, pilotées par un double lisant
  la capture, de sorte que leurs conversions, leurs gardes de `NaN` et leur
  provenance s'exécutent vraiment.

Ce que ce banc NE prouve pas, et qui reste `HUMAN_REQUIRED` : le rythme, la
reconnexion, les droits du compte et le comportement d'une vraie séance. Un
rejeu ne remplace pas un broker ; il empêche seulement une régression de passer
inaperçue jusqu'à la prochaine fois où quelqu'un rallume TWS.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from vertex.data_sources import ibkr_contracts as C
from vertex.data_sources import ibkr_market_data as MD
from vertex.data_sources import ibkr_option_chain as OC
from vertex.data_sources import ibkr_replay as R
from vertex.data_sources.models import (
    GREEKS_BROKER, GREEKS_MODEL, MODE_DELAYED, MODE_FROZEN, MODE_LIVE,
    SOURCE_IBKR,
)

RACINE = Path(__file__).resolve().parents[1]
CAPTURE = RACINE / "tests" / "fixtures" / "ibkr" / "g5_capture.json"


@pytest.fixture(scope="module")
def capture() -> dict:
    paquet = json.loads(CAPTURE.read_text(encoding="utf-8"))
    assert paquet["version_fixture"] == R.VERSION_FIXTURE
    return paquet["fixture"]


@pytest.fixture()
def passerelle(capture):
    return R.PasserelleRejouee(capture)


#  ═══════════════════════  0. la capture est publiable  ═══════════════════════

def test_la_capture_versionnee_ne_contient_aucune_donnee_personnelle():
    """Un artefact publié « en espérant » qu'il soit propre finit dans un dépôt
    public avec un numéro de compte dedans."""
    brut = CAPTURE.read_text(encoding="utf-8")
    paquet = json.loads(brut)
    assert R.contient_donnee_sensible(paquet["fixture"]) == []
    assert R.MASQUE_COMPTE in brut or "U1" not in brut
    for ligne in paquet["fixture"]["positions_brutes"]:
        assert ligne["symbol"].startswith("TITRE_"), (
            "un symbole détenu est une donnée personnelle, même sans quantité")
        assert ligne["avgCost"] is None


def test_le_temoin_d_anonymisation_voit_reellement_quelque_chose():
    """Un détecteur qui regarde au mauvais endroit rend la même réponse qu'un
    détecteur satisfait. On lui présente donc un relevé SALE."""
    sale = {
        "raison": "le compte U8000001 a refusé",
        "positions": {"detenues_non_declarees": ["AAPL"],
                      "declarees_non_detenues": [],
                      "quantites_divergentes": [{"sym": "BAC", "broker": 10,
                                                 "bureau": 5}],
                      "concordant": False},
    }
    vus = R.contient_donnee_sensible(sale)
    assert any("compte" in x for x in vus)
    assert any("détenus" in x for x in vus)
    propre = R.anonymiser(sale)
    assert R.contient_donnee_sensible(propre) == []
    assert propre["positions"]["n_detenues_non_declarees"] == 1
    assert propre["positions"]["concordant"] is False


def test_enregistrer_anonymise_avant_d_ecrire(tmp_path):
    """Le chemin nominal : on lui donne un relevé sale, il écrit du propre."""
    p = R.enregistrer({"raison": "compte U8000001",
                       "positions": {"detenues_non_declarees": ["AAPL"],
                                     "concordant": False}},
                      tmp_path / "propre.json")
    ecrit = p.read_text(encoding="utf-8")
    assert "U8000001" not in ecrit and "AAPL" not in ecrit
    assert R.contient_donnee_sensible(R.charger(p)) == []


def test_le_filet_REFUSE_d_ecrire_ce_que_l_anonymiseur_a_laisse_passer(
        tmp_path, monkeypatch):
    """`enregistrer` anonymise PUIS contrôle. Le contrôle n'est donc pas
    redondant : il rattrape ce que l'anonymiseur ne sait pas encore voir — le
    jour où une nouvelle clé du relevé portera un compte. On neutralise
    l'anonymiseur pour prouver que le filet existe vraiment."""
    monkeypatch.setattr(R, "anonymiser", lambda r: dict(r))
    with pytest.raises(ValueError, match="anonymisation incomplète"):
        R.enregistrer({"raison": "compte U8000001"}, tmp_path / "fuite.json")
    assert not (tmp_path / "fuite.json").exists(), (
        "un refus qui écrit quand même le fichier ne refuse rien")


def test_une_fixture_de_version_inconnue_est_refusee(tmp_path):
    """Rejouer un format qu'on ne comprend pas produirait une preuve fausse."""
    p = tmp_path / "futur.json"
    p.write_text(json.dumps({"version_fixture": 999, "releve": {}}),
                 encoding="utf-8")
    with pytest.raises(ValueError, match="version"):
        R.charger(p)


#  ═══════════════════  1. ibkr_contracts — mapping et rejeu  ══════════════════

def test_contrat_action_conforme_ne_signale_rien():
    assert C.validate_stock_contract(
        {"symbol": "AAPL", "currency": "USD", "conId": 265598}, "AAPL") == []


@pytest.mark.parametrize("details,attendu", [
    ({"symbol": "AAPL", "currency": "USD", "conId": 1}, "mapping"),
    ({"symbol": "MSFT", "currency": "EUR", "conId": 1}, "devise"),
    ({"symbol": "MSFT", "currency": "USD", "conId": None}, "conId"),
])
def test_chaque_erreur_de_mapping_est_NOMMEE(details, attendu):
    """Un mapping faux ne doit pas rendre « invalide » : le risque diffère.
    Résoudre AAPL vers autre chose, coter en euros ou ne pas qualifier du tout
    ne se corrigent pas de la même façon."""
    problemes = C.validate_stock_contract(details, "MSFT")
    assert any(attendu in p for p in problemes), problemes


def test_le_contrat_option_herite_des_controles_action_et_ajoute_les_siens():
    p = C.validate_option_contract(
        {"symbol": "AAPL", "currency": "USD", "conId": 1,
         "multiplier": "10", "right": "X"}, "AAPL")
    assert any("multiplicateur" in x for x in p)
    assert any("option" in x for x in p)


def test_un_multiplicateur_100_est_accepte_sous_ses_trois_formes():
    for mult in ("100", 100, None):
        p = C.validate_option_contract(
            {"symbol": "AAPL", "currency": "USD", "conId": 1,
             "multiplier": mult, "right": "C"}, "AAPL")
        assert p == [], (mult, p)


def test_rejeu_qualify_stock_rend_le_contrat_reellement_capture(passerelle,
                                                                capture):
    d = C.qualify_stock(passerelle, "AAPL")
    attendu = capture["contrats"]["AAPL"]
    assert d["conId"] == attendu["conId"] and d["conId"]
    assert d["currency"] == attendu["currency"]
    assert C.validate_stock_contract(d, "AAPL") == []


def test_rejeu_qualify_stock_avoue_un_symbole_inconnu(passerelle):
    """Sans `conId`, le produit doit dire qu'il n'a pas qualifié — pas rendre
    un contrat vide qui passerait pour valide plus loin."""
    d = C.qualify_stock(passerelle, "SYMBOLE_INEXISTANT")
    assert d["conId"] is None
    assert any("conId" in p for p in C.validate_stock_contract(d, "SYMBOLE_INEXISTANT"))


#  ══════════════  2. ibkr_market_data — modes de marché et rejeu  ═════════════

@pytest.mark.parametrize("type_ibkr,mode", [
    (1, MODE_LIVE), (2, MODE_FROZEN), (3, MODE_DELAYED), (4, MODE_DELAYED),
])
def test_les_quatre_types_de_donnees_ibkr_sont_etiquetes(type_ibkr, mode):
    """1 live, 2 figé, 3 différé, 4 différé-figé. Confondre différé et live est
    le mensonge que la provenance existe pour empêcher."""
    pv = MD.snapshot_to_provenanced({"last": 10.0, "time": "2026-08-24T10:00:00"},
                                    type_ibkr)
    assert pv.source_mode == mode and pv.source == SOURCE_IBKR


def test_un_type_de_donnees_inconnu_retombe_sur_DIFFERE_jamais_sur_LIVE():
    """Se tromper vers « différé » coûte une mention prudente ; se tromper vers
    « live » présente une donnée vieille comme fraîche."""
    assert MD.snapshot_to_provenanced({"last": 1.0}, 99).source_mode == MODE_DELAYED


def test_un_snapshot_sans_prix_rend_None_et_le_DIT():
    pv = MD.snapshot_to_provenanced({"bid": None, "ask": None, "close": None})
    assert pv.value is None
    assert any("sans prix" in w for w in pv.warnings)


def test_le_dernier_prix_manquant_se_replie_sur_la_cloture():
    pv = MD.snapshot_to_provenanced({"last": None, "close": 42.0})
    assert pv.value["price"] == 42.0


def test_un_marche_croise_est_signale_sans_etre_corrige():
    """Corriger un bid > ask fabriquerait un marché qui n'existe pas."""
    pv = MD.snapshot_to_provenanced({"last": 5.0, "bid": 6.0, "ask": 4.0})
    assert any("croisé" in w for w in pv.warnings)
    assert pv.value["bid"] == 6.0 and pv.value["ask"] == 4.0


def test_rejeu_fetch_snapshot_execute_les_gardes_de_NaN_du_produit(passerelle,
                                                                   capture):
    """IBKR ne rend pas `None` pour un champ absent : il rend `NaN`. Le double
    reproduit ce piège, sinon les gardes `t.last == t.last` passeraient pour
    inutiles."""
    pv = MD.fetch_snapshot(passerelle, "AAPL")
    attendu = capture["cotations_brutes"]["AAPL"]
    assert pv.source == SOURCE_IBKR
    assert pv.value["last"] == attendu["last"]
    assert pv.value["price"] is not None
    for champ in ("last", "bid", "ask", "close"):
        assert not (isinstance(pv.value[champ], float)
                    and math.isnan(pv.value[champ])), champ


def test_rejeu_fetch_snapshot_porte_le_mode_reellement_capture(passerelle,
                                                               capture):
    pv = MD.fetch_snapshot(passerelle, "MSFT")
    attendu = MD._MODE_BY_TYPE.get(int(capture["mode_donnees"]), MODE_DELAYED)
    assert pv.source_mode == attendu


#  ═══════════  3. positions du compte — capacité RETIRÉE au lot 2  ═══════════
#
#  Quatre bancs éprouvaient ici `ibkr_positions` (quantité nulle, quantité
#  illisible, défauts explicites, rejeu jusqu'à la provenance). Le module a
#  été SUPPRIMÉ : lire les positions du compte viole la frontière
#  market-data-only, readonly ou pas. L'intention de ces bancs — ne jamais
#  deviner une quantité, ne jamais gonfler le risque d'une ligne fermée —
#  vit désormais dans le dépôt du desk (`vertex/positions/repository.py`),
#  seule source de portefeuille. La non-réapparition du module est gardée par
#  `tests/test_frontiere_ibkr_lot02.py`.

#  ═════════════════  4. ibkr_option_chain — contrat et rejeu  ═════════════════

def test_le_mid_se_calcule_seulement_quand_les_DEUX_cotes_existent():
    assert OC.contract_row(symbol="a", expiry="20260918", strike=100,
                           right="c", bid=1.0, ask=3.0)["mid"] == 2.0
    assert OC.contract_row(symbol="a", expiry="20260918", strike=100,
                           right="c", bid=1.0)["mid"] is None
    assert OC.contract_row(symbol="a", expiry="20260918", strike=100,
                           right="c", bid=1.0, ask=0)["mid"] is None


def test_la_ligne_de_contrat_porte_TOUS_les_champs_exiges_par_le_standard():
    """QUALITY_STANDARD §3 : contrat, spot, strike, DTE, bid/ask/mid, volume,
    OI, IV, Greeks, horodatage — disponibles ou explicitement manquants."""
    r = OC.contract_row(symbol="aapl", expiry="20260918", strike=200.0,
                        right="put", timestamp="2026-08-24T10:00:00")
    for champ in ("symbol", "underlying", "expiry", "strike", "right", "bid",
                  "ask", "mid", "last", "volume", "open_interest", "iv",
                  "delta", "gamma", "theta", "vega", "greeks_source",
                  "multiplier", "currency", "timestamp"):
        assert champ in r, champ
    assert r["symbol"] == "AAPL" and r["right"] == "P"
    assert r["iv"] is None and r["delta"] is None


def test_les_greeks_du_courtier_sont_etiquetes_comme_tels():
    """§6.8 : les Greeks IBKR sont préférés à tout modèle maison, et la source
    doit se lire — sinon on ne saura plus si un delta a été mesuré ou estimé."""
    assert OC.contract_row(symbol="a", expiry="e", strike=1, right="c",
                           delta=0.5)["greeks_source"] == GREEKS_BROKER
    assert OC.contract_row(symbol="a", expiry="e", strike=1, right="c",
                           greeks_source=GREEKS_MODEL)["greeks_source"] == GREEKS_MODEL


def test_une_chaine_vide_reste_une_chaine_tracee():
    pv = OC.chain_to_provenanced([], timestamp="2026-08-24T10:00:00")
    assert pv.value == [] and pv.source == SOURCE_IBKR
    assert pv.source_mode == MODE_DELAYED


def test_rejeu_fetch_expirations_rend_les_echeances_reellement_capturees(
        passerelle, capture):
    exp = OC.fetch_expirations(passerelle, "AAPL")
    attendues = capture["expirations_par_symbole"]["AAPL"][0]["expirations"]
    assert exp == sorted(set(attendues))
    assert all(len(e) == 8 and e.isdigit() for e in exp), exp


def test_rejeu_fetch_expirations_sur_un_symbole_sans_options_rend_le_vide(
        passerelle):
    assert OC.fetch_expirations(passerelle, "SYMBOLE_INEXISTANT") == []


#  ═══════════  5. la preuve négative : aucun chemin d'ordre nulle part  ═══════

METHODES_D_ORDRE = ("placeOrder", "cancelOrder", "reqIds", "bracketOrder",
                    "oneCancelsAll", "reqGlobalCancel", "exerciseOptions")


def test_le_broker_rejoue_n_expose_AUCUNE_methode_d_ordre(passerelle):
    """Ce n'est pas un oubli du double : c'est la moitié de la preuve. Un
    double qui exposerait `placeOrder` laisserait un futur appel d'ordre passer
    les tests sans jamais toucher TWS."""
    ib = passerelle.connect()
    for nom in METHODES_D_ORDRE:
        assert not hasattr(ib, nom), nom
    assert passerelle.READONLY is True


def test_aucun_des_adaptateurs_ne_nomme_une_methode_d_ordre():
    #  POS (positions du compte) a ete SUPPRIME au lot 2 : il reste trois
    #  adaptateurs de MARCHE, et la garde anti-ordre les couvre tous.
    for mod in (C, MD, OC):
        src = Path(mod.__file__).read_text(encoding="utf-8")
        for nom in METHODES_D_ORDRE:
            assert nom not in src, "%s cite %s" % (mod.__name__, nom)


def test_rejeu_fetch_contract_details_avoue_une_chaine_SANS_cotation(
        passerelle, capture):
    """Capture réelle prise hors séance : IBKR rend `-1` pour bid/ask et aucun
    Greek. `-1` n'est pas un prix, c'est la sentinelle « pas de donnée » — la
    garde `bid > 0` de l'adaptateur doit la transformer en `None`, jamais la
    laisser passer pour une cote négative.
    """
    opts = capture.get("contrats_options") or {}
    if not opts:
        pytest.skip("la capture ne porte aucun contrat d'option")
    cle = sorted(opts)[0]
    sym, echeance, strike, right = cle.split("|")
    pv = OC.fetch_contract_details(passerelle, sym, echeance,
                                   [float(strike)], right)
    assert pv.source == SOURCE_IBKR
    assert len(pv.value) == 1
    ligne = pv.value[0]
    assert ligne["bid"] is None and ligne["ask"] is None, (
        "-1 est une sentinelle IBKR, pas une cotation")
    assert ligne["mid"] is None
    assert ligne["greeks_source"] == GREEKS_MODEL, (
        "sans modelGreeks, la source doit dire ESTIMATION — l'étiqueter "
        "BROKER ferait passer un modèle maison pour une mesure du courtier")
    assert ligne["strike"] == float(strike) and ligne["right"] == right


def test_rejeu_fetch_contract_details_porte_les_GREEKS_du_courtier(capture):
    """L'autre branche : quand IBKR fournit ses `modelGreeks`, ils sont repris
    tels quels et étiquetés BROKER (§6.8).

    Le ticker est ici FABRIQUÉ et le dit : la capture réelle a été prise hors
    séance, donc aucune chaîne cotée n'existait à ce moment. Un chiffre inventé
    n'entre pas dans l'artefact publié — il reste dans le test, dont c'est
    précisément le rôle d'éprouver un chemin que le marché n'offrait pas.
    """
    opts = capture.get("contrats_options") or {}
    if not opts:
        pytest.skip("la capture ne porte aucun contrat d'option")
    cle = sorted(opts)[0]
    sym, echeance, strike, right = cle.split("|")
    truque = dict(capture)
    truque["cotations_brutes"] = dict(capture["cotations_brutes"])
    truque["cotations_brutes"][cle] = {
        "last": 4.20, "bid": 4.10, "ask": 4.30, "close": 4.15, "volume": 118.0,
        "time": "2026-08-24T13:45:00+00:00",
        "greeks": {"iv": 0.2841, "delta": 0.5123, "gamma": 0.0412,
                   "theta": -0.1875, "vega": 0.0933},
    }
    pv = OC.fetch_contract_details(R.PasserelleRejouee(truque), sym, echeance,
                                   [float(strike)], right)
    ligne = pv.value[0]
    assert ligne["greeks_source"] == GREEKS_BROKER
    assert ligne["iv"] == 0.2841 and ligne["delta"] == 0.5123
    assert ligne["bid"] == 4.10 and ligne["ask"] == 4.30
    assert ligne["mid"] == pytest.approx(4.20)
    assert ligne["volume"] == 118
    assert ligne["timestamp"] == "2026-08-24T13:45:00+00:00"


def test_rejeu_fetch_contract_details_sur_un_strike_inconnu_rend_une_chaine_vide(
        passerelle):
    """Un strike que le broker ne qualifie pas ne doit produire AUCUNE ligne —
    pas une ligne creuse qui serait comptée comme un contrat disponible."""
    pv = OC.fetch_contract_details(passerelle, "AAPL", "20990101", [1.0], "C")
    assert pv.value == [] and pv.source == SOURCE_IBKR


def test_une_option_ne_recoit_jamais_le_conId_de_son_sous_jacent(passerelle,
                                                                 capture):
    """Deux strikes de la même échéance partagent le symbole. Si la
    qualification se faisait par symbole, une option recevrait le conId de
    l'action et le produit coterait autre chose que ce qu'il croit."""
    opts = capture.get("contrats_options") or {}
    if not opts:
        pytest.skip("la capture ne porte aucun contrat d'option")
    conid_action = capture["contrats"]["AAPL"]["conId"]
    conids_options = {d["conId"] for d in opts.values()}
    assert conid_action not in conids_options
    assert len(conids_options) == len(opts), "deux options partagent un conId"


#  ═══════  6. le type de marché : OBSERVÉ, jamais supposé (défaut G5 mesuré)  ══

def test_le_type_de_marche_est_DEDUIT_des_champs_que_le_broker_a_remplis():
    """IBKR remplit `delayed*` au lieu des champs directs quand la donnée est
    différée. C'est une observation ; l'ancien code lisait
    `client.marketDataType`, un attribut qui n'existe pas dans ib_async 2.1.0."""
    assert MD.type_observe({"delayedLast": 10.0}) == 3
    assert MD.type_observe({"delayedBid": 9.9}) == 3
    assert MD.type_observe({"last": 10.0}) == MD.TYPE_INCONNU
    assert MD.type_observe({}) == MD.TYPE_INCONNU


def test_temps_reel_et_fige_ne_sont_PAS_distinguables_par_les_champs():
    """Les deux remplissent `last`. Revendiquer LIVE présenterait une clôture
    de la veille comme un cours de séance : on rend INCONNU."""
    assert MD.type_observe({"last": 1.0, "bid": 1.0, "ask": 1.1}) == MD.TYPE_INCONNU


def test_un_type_non_observe_est_AVOUE_et_non_presente_comme_du_differe():
    """Le défaut mesuré le 24 août 2026 : le mode retombait silencieusement sur
    DELAYED à chaque appel. La direction prudente est conservée, mais elle se
    dit — sinon une ignorance se lit comme une mesure."""
    pv = MD.snapshot_to_provenanced({"last": 10.0}, MD.TYPE_INCONNU)
    assert pv.source_mode == MODE_DELAYED
    assert any("non observé" in w for w in pv.warnings)


def test_un_type_REELLEMENT_connu_ne_porte_aucun_aveu():
    """Contre-épreuve : l'aveu ne doit pas être collé partout, sinon il ne
    distingue plus rien."""
    for t in (1, 2, 3, 4):
        pv = MD.snapshot_to_provenanced({"last": 10.0}, t)
        assert not any("non observé" in w for w in pv.warnings), t


def test_rejeu_fetch_snapshot_sur_donnee_DIFFEREE_etiquette_DELAYED_sans_aveu(
        capture):
    """Quand le broker remplit les champs différés, le mode est MESURÉ."""
    truque = dict(capture)
    truque["cotations_brutes"] = dict(capture["cotations_brutes"])
    truque["cotations_brutes"]["AAPL"] = {
        "last": None, "bid": None, "ask": None, "close": 300.0,
        "delayedLast": 310.0, "delayedBid": 309.9, "delayedAsk": 310.1,
        "time": "2026-08-24T10:00:00+00:00"}
    pv = MD.fetch_snapshot(R.PasserelleRejouee(truque), "AAPL")
    assert pv.source_mode == MODE_DELAYED
    assert not any("non observé" in w for w in pv.warnings), (
        "ici le différé a été CONSTATÉ : l'aveu serait faux")


#  ═══════  L'OPEN INTEREST : case « NON COUVERT » du protocole G5  ════════════
#
#  `fetch_contract_details` rendait `open_interest=None` **en dur**. La cause
#  n'etait pas IBKR : `reqTickers` ne demande pas le tick generique 101, donc
#  l'information n'arrivait jamais. Le board de production, lui, l'obtient
#  depuis toujours par `reqMktData(genericTickList='100,101,106')`.
#
#  `QUALITY_STANDARD` §3 exige l'OI pour une option candidate, et le mandat
#  options en fait un critere de liquidite : une valeur toujours absente rendait
#  ce critere inapplicable sans que rien ne le dise.
#
#  Les cotations ci-dessous sont FABRIQUEES pour eprouver le chemin. La capture
#  reelle n'en porte pas, et on ne lui en injecte pas : un artefact de preuve ne
#  se complete pas avec des chiffres inventes.

def _avec_oi(capture, valeurs):
    """La capture, plus une cotation d'option FABRIQUEE portant `valeurs`."""
    opts = capture.get("contrats_options") or {}
    if not opts:
        pytest.skip("la capture ne porte aucun contrat d'option")
    cle = sorted(opts)[0]
    truque = dict(capture)
    truque["cotations_brutes"] = dict(capture["cotations_brutes"])
    truque["cotations_brutes"][cle] = {
        "last": 4.20, "bid": 4.10, "ask": 4.30, "close": 4.15, "volume": 118.0,
        "time": "2026-08-24T13:45:00+00:00", **valeurs,
    }
    return cle, truque


def test_l_open_interest_arrive_desormais_jusqu_a_la_ligne(capture):
    """La case fermee. Avant : `None` quoi que le courtier envoie."""
    cle, truque = _avec_oi(capture, {"callOpenInterest": 4213.0,
                                     "putOpenInterest": 77.0})
    sym, echeance, strike, right = cle.split("|")
    pv = OC.fetch_contract_details(R.PasserelleRejouee(truque), sym, echeance,
                                   [float(strike)], right)
    assert pv.value[0]["open_interest"] == 4213


def test_un_CALL_ne_recoit_jamais_l_open_interest_des_PUTS(capture):
    """IBKR expose les deux cotes separement. Lire le mauvais donnerait a un
    call l'interet ouvert des puts — un chiffre plausible et faux, la pire
    espece."""
    cle, truque = _avec_oi(capture, {"callOpenInterest": 4213.0,
                                     "putOpenInterest": 77.0})
    sym, echeance, strike, _ = cle.split("|")
    pv = OC.fetch_contract_details(R.PasserelleRejouee(truque), sym, echeance,
                                   [float(strike)], "C")
    assert pv.value[0]["open_interest"] == 4213
    assert pv.value[0]["open_interest"] != 77


def test_un_open_interest_ABSENT_reste_None_et_ne_devient_pas_zero(capture):
    """« Aucune donnee » et « aucun contrat ouvert » sont deux verdicts opposes
    quand on juge la liquidite d'une option. Les confondre ferait ecarter un
    contrat parfaitement liquide — ou pire, en retenir un qui ne l'est pas."""
    cle, truque = _avec_oi(capture, {})       # aucun champ d'OI
    sym, echeance, strike, right = cle.split("|")
    pv = OC.fetch_contract_details(R.PasserelleRejouee(truque), sym, echeance,
                                   [float(strike)], right)
    assert pv.value[0]["open_interest"] is None


def test_la_sentinelle_negative_du_courtier_devient_None(capture):
    """IBKR rend parfois `-1` pour « pas de donnee ». Le laisser passer
    afficherait un interet ouvert NEGATIF."""
    cle, truque = _avec_oi(capture, {"callOpenInterest": -1.0})
    sym, echeance, strike, _ = cle.split("|")
    pv = OC.fetch_contract_details(R.PasserelleRejouee(truque), sym, echeance,
                                   [float(strike)], "C")
    assert pv.value[0]["open_interest"] is None


def test_un_open_interest_REELLEMENT_nul_est_conserve(capture):
    """Contre-epreuve. Un contrat sans aucun interet ouvert est une INFORMATION
    — et une information decisive pour un mandat qui exige de la liquidite.
    La confondre avec l'absence la ferait disparaitre."""
    cle, truque = _avec_oi(capture, {"callOpenInterest": 0.0})
    sym, echeance, strike, _ = cle.split("|")
    pv = OC.fetch_contract_details(R.PasserelleRejouee(truque), sym, echeance,
                                   [float(strike)], "C")
    assert pv.value[0]["open_interest"] == 0


def test_l_adaptateur_DEMANDE_bien_le_tick_101(capture):
    """Le defaut n'etait pas dans la lecture, il etait dans la DEMANDE. Sans ce
    banc, on pourrait retirer le `genericTickList` sans qu'aucun test bronche —
    et l'OI redeviendrait `None` partout, en silence."""
    cle, truque = _avec_oi(capture, {"callOpenInterest": 12.0})
    sym, echeance, strike, right = cle.split("|")
    passerelle = R.PasserelleRejouee(truque)
    OC.fetch_contract_details(passerelle, sym, echeance, [float(strike)], right)
    ib = passerelle.connect()
    assert any("101" in t for t in getattr(ib, "ticks_demandes", [])), (
        "le tick generique 101 n'a pas ete demande : l'open interest ne peut "
        "pas arriver")


def test_chaque_abonnement_ouvert_est_REFERME(capture):
    """Une ligne de marche laissee ouverte est une ressource bornee, partagee
    avec le reste du produit."""
    cle, truque = _avec_oi(capture, {"callOpenInterest": 12.0})
    sym, echeance, strike, right = cle.split("|")
    passerelle = R.PasserelleRejouee(truque)
    OC.fetch_contract_details(passerelle, sym, echeance, [float(strike)], right)
    ib = passerelle.connect()
    assert ib.appels.count("reqMktData") == ib.appels.count("cancelMktData")


def test_aucun_abonnement_ouvert_si_AUCUN_contrat_ne_qualifie(capture):
    """Contre-epreuve : sans ce court-circuit, on ouvrirait une session et une
    attente de 2,6 s pour ne rien lire."""
    passerelle = R.PasserelleRejouee(capture)
    pv = OC.fetch_contract_details(passerelle, "SYMBOLE_INCONNU", "20260824",
                                   [100.0], "C")
    assert pv.value == []
    assert passerelle.connect().appels.count("reqMktData") == 0
