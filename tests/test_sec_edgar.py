"""Vertex Test 1.0 · Phase 3 — SEC EDGAR : LE PREMIER PRODUCTEUR POINT-IN-TIME.

Le registre de la phase 2 attend `available_at`. La SEC est la première source
qui le fournit **réellement** : chaque fait XBRL porte la période qu'il décrit
(`end`) *et* la date de dépôt (`filed`). C'est exactement la paire que
`yfinance.Ticker.info` ne donne pas — et l'absence de laquelle l'audit qualifie
de défaut P0.

Deux décisions de conversion portent tout ce fichier, et toutes deux vont dans
la direction prudente :

1. **une date de dépôt devient disponible à la FIN de la journée**, pas à son
   début. Un dépôt du 25 octobre n'est pas connaissable le 25 à 00:01 : le
   supposer donnerait à un backtest jusqu'à vingt-quatre heures d'avance sur le
   marché ;
2. **la journée est celle de New York**, fuseau du déposant, avec son heure
   d'été réelle — pas un décalage fixe qui se tromperait la moitié de l'année.

Le lot ne prétend à aucune ingestion réelle : `SEC_USER_AGENT` n'est pas
configuré sur cette machine, et le *fair-access* de la SEC exige un contact
que Vertex ne doit pas inventer. Les cases correspondantes sont
`HUMAN_REQUIRED` et le disent.
"""
from __future__ import annotations

import datetime as dt

import pytest

from vertex.data_sources import sec_edgar as SEC
from vertex.domain.instruments import Instrument
from vertex.storage import point_in_time as PIT


#  ─────────────────────────  fixture de FORME, pas de fond  ───────────────────
#
#  Structure documentée de `data.sec.gov/api/xbrl/companyfacts`. Les valeurs
#  sont illustratives : aucune donnée réelle n'est prétendue ici, faute de
#  pouvoir interroger la SEC sans User-Agent déclaré.

FAITS = {
    "cik": 320193,
    "entityName": "Exemple Inc.",
    "facts": {
        "us-gaap": {
            "EarningsPerShareDiluted": {
                "label": "Earnings Per Share, Diluted",
                "units": {
                    "USD/shares": [
                        {"start": "2026-07-01", "end": "2026-09-30",
                         "val": 1.64, "accn": "0000320193-26-000101",
                         "fy": 2026, "fp": "Q3", "form": "10-Q",
                         "filed": "2026-10-25", "frame": "CY2026Q3"},
                        {"start": "2026-07-01", "end": "2026-09-30",
                         "val": 1.58, "accn": "0000320193-26-000188",
                         "fy": 2026, "fp": "Q3", "form": "10-Q/A",
                         "filed": "2026-12-01", "frame": "CY2026Q3"},
                    ],
                },
            },
            "Revenues": {
                "units": {
                    "USD": [
                        {"start": "2026-07-01", "end": "2026-09-30",
                         "val": 94_930_000_000, "accn": "0000320193-26-000101",
                         "fy": 2026, "fp": "Q3", "form": "10-Q",
                         "filed": "2026-10-25"},
                    ],
                },
            },
        },
    },
}

INSTRUMENT = Instrument(conid=265598, cik="320193", ticker="AAPL")


#  ═══════════════  1. la conversion des dates, dans le sens prudent  ══════════

def test_une_date_de_depot_devient_disponible_a_la_FIN_de_la_journee():
    """Un dépôt du 25 octobre n'est pas connaissable le 25 à 00:01. Prendre le
    début de journée donnerait à un backtest jusqu'à vingt-quatre heures
    d'avance sur le marché — la faute exacte que la phase 2 existe pour rendre
    impossible."""
    iso = SEC.fin_de_journee_depot("2026-10-25")
    t = dt.datetime.fromisoformat(iso)
    assert t.tzinfo is not None, "un instant sans fuseau serait refusé par le registre"
    en_utc = t.astimezone(dt.timezone.utc)
    assert en_utc.date() >= dt.date(2026, 10, 25)
    assert en_utc > dt.datetime(2026, 10, 25, 12, 0, tzinfo=dt.timezone.utc), (
        "la fin de journée doit être postérieure à la mi-journée du dépôt")


def test_la_journee_est_celle_de_NEW_YORK_avec_son_heure_d_ete_reelle():
    """Un décalage fixe se tromperait d'une heure la moitié de l'année, et
    déplacerait des dépôts d'un jour à la frontière de minuit."""
    ete = dt.datetime.fromisoformat(SEC.fin_de_journee_depot("2026-10-25"))
    hiver = dt.datetime.fromisoformat(SEC.fin_de_journee_depot("2026-01-15"))
    assert ete.utcoffset() != hiver.utcoffset(), (
        "octobre et janvier n'ont pas le même décalage à New York")


def test_une_periode_se_termine_a_la_fin_du_JOUR_decrit():
    """`end: 2026-09-30` désigne un trimestre clos ce jour-là, pas un instant
    à minuit avant qu'il ne soit clos."""
    iso = SEC.fin_de_periode("2026-09-30")
    t = dt.datetime.fromisoformat(iso).astimezone(dt.timezone.utc)
    assert t.tzinfo is not None
    assert t >= dt.datetime(2026, 9, 30, 12, 0, tzinfo=dt.timezone.utc)


def test_une_date_illisible_est_REFUSEE_et_non_devinee():
    for mauvais in ("", "25/10/2026", "2026-13-01", None):
        with pytest.raises(ValueError):
            SEC.fin_de_journee_depot(mauvais)


#  ═══════════════════  2. faits XBRL vers observations  ═══════════════════════

def test_chaque_fait_devient_une_observation_datee_des_DEUX_instants():
    obs = SEC.faits_vers_observations(FAITS, INSTRUMENT)
    assert obs, "la fixture porte des faits — n'en rendre aucun serait un défaut"
    o = [x for x in obs if x.champ == "us-gaap:Revenues"][0]
    assert o.valeur == 94_930_000_000
    assert o.devise == "USD"
    assert o.provider == SEC.PROVIDER
    assert o.provider_record_id == "0000320193-26-000101"
    #  la période décrite précède strictement la disponibilité
    assert o.observed_at < o.available_at


def test_le_depot_devient_available_at_et_la_periode_observed_at():
    """L'inversion des deux serait invisible à l'œil et fausserait TOUT."""
    obs = SEC.faits_vers_observations(FAITS, INSTRUMENT)
    o = [x for x in obs if x.champ == "us-gaap:Revenues"][0]
    assert dt.datetime.fromisoformat(o.observed_at).date() == dt.date(2026, 9, 30)
    assert dt.datetime.fromisoformat(o.available_at).astimezone(
        dt.timezone.utc).date() >= dt.date(2026, 10, 25)


def test_un_retraitement_devient_une_REVISION_ordonnee_par_depot():
    """Le même trimestre déposé deux fois — 10-Q puis 10-Q/A — donne deux
    observations, et la seconde porte un numéro de révision supérieur."""
    obs = [x for x in SEC.faits_vers_observations(FAITS, INSTRUMENT)
           if x.champ == "us-gaap:EarningsPerShareDiluted"]
    assert len(obs) == 2
    obs.sort(key=lambda o: o.available_at)
    assert obs[0].valeur == 1.64 and obs[0].revision == 0
    assert obs[1].valeur == 1.58 and obs[1].revision == 1
    assert obs[1].lineage, "une révision doit citer le dépôt qu'elle corrige"


def test_un_tag_ABSENT_ne_devient_jamais_zero():
    """Interdiction explicite de la doctrine des sources. Un tag manquant est
    une absence ; un zéro est une affirmation."""
    vide = {"cik": 1, "facts": {"us-gaap": {"Revenues": {"units": {}}}}}
    assert SEC.faits_vers_observations(vide, INSTRUMENT) == []
    sans_faits = {"cik": 1, "facts": {}}
    assert SEC.faits_vers_observations(sans_faits, INSTRUMENT) == []


def test_une_valeur_non_numerique_est_ignoree_et_non_coercee():
    """Forcer une chaîne en nombre fabriquerait une donnée que la SEC n'a pas
    publiée."""
    bancal = {"cik": 1, "facts": {"us-gaap": {"X": {"units": {"USD": [
        {"end": "2026-09-30", "val": "n/a", "accn": "a", "filed": "2026-10-25"},
        {"end": "2026-09-30", "val": 5, "accn": "b", "filed": "2026-10-26"},
    ]}}}}}
    obs = SEC.faits_vers_observations(bancal, INSTRUMENT)
    assert [o.valeur for o in obs] == [5]


def test_un_fait_sans_date_de_depot_est_ignore_et_COMPTE():
    """Sans `filed`, on ne peut pas dire quand il est devenu connaissable. Le
    laisser passer contaminerait le registre ; l'ignorer en silence cacherait
    un trou dans l'ingestion."""
    sans = {"cik": 1, "facts": {"us-gaap": {"X": {"units": {"USD": [
        {"end": "2026-09-30", "val": 5, "accn": "a"},
    ]}}}}}
    obs, rapport = SEC.faits_vers_observations(sans, INSTRUMENT, avec_rapport=True)
    assert obs == []
    assert rapport["ignores_sans_depot"] == 1


#  ═══════════════════  3. l'unité et la devise sont conservées  ═══════════════

def test_l_unite_xbrl_est_conservee_et_la_devise_extraite():
    obs = SEC.faits_vers_observations(FAITS, INSTRUMENT)
    eps = [o for o in obs if o.champ.endswith("EarningsPerShareDiluted")][0]
    assert eps.unite == "USD/shares"
    assert eps.devise == "USD", "une donnée financière sans devise n'est pas comparable"
    rev = [o for o in obs if o.champ.endswith("Revenues")][0]
    assert rev.unite == "USD" and rev.devise == "USD"


def test_une_unite_non_monetaire_ne_recoit_PAS_de_devise_inventee():
    """`shares` n'est pas une devise. En inventer une rendrait comparables des
    grandeurs qui ne le sont pas."""
    d = {"cik": 1, "facts": {"us-gaap": {"Actions": {"units": {"shares": [
        {"end": "2026-09-30", "val": 15_000, "accn": "a", "filed": "2026-10-25"},
    ]}}}}}
    o = SEC.faits_vers_observations(d, INSTRUMENT)[0]
    assert o.unite == "shares" and o.devise == ""


#  ═══════════  4. le fair-access : Vertex n'invente aucun contact  ════════════

def test_appeler_la_SEC_sans_USER_AGENT_est_REFUSE(monkeypatch):
    """Le fair-access SEC exige un contact réel. Vertex ne doit ni l'inventer,
    ni emprunter celui de l'utilisateur sans qu'il l'ait posé lui-même."""
    monkeypatch.delenv("SEC_USER_AGENT", raising=False)
    with pytest.raises(SEC.EntitlementManquant, match="SEC_USER_AGENT"):
        SEC.user_agent()


def test_un_user_agent_configure_est_utilise_tel_quel(monkeypatch):
    monkeypatch.setenv("SEC_USER_AGENT", "Vertex/1.0 (contact@exemple.fr)")
    assert SEC.user_agent() == "Vertex/1.0 (contact@exemple.fr)"


def test_le_module_ne_porte_aucun_contact_en_dur():
    """Un contact code en dur partirait chez un tiers sans que personne ne
    l'ait décidé."""
    from pathlib import Path
    src = Path(SEC.__file__).read_text(encoding="utf-8")
    assert "@gmail" not in src and "@hotmail" not in src
    assert "SEC_USER_AGENT" in src


#  ═══════════════  5. bout en bout : le registre reste honnête  ═══════════════

def test_les_observations_SEC_entrent_dans_le_registre_et_restent_point_in_time():
    """Le test qui relie les deux phases : après ingestion, ce que Vertex
    savait le 1er novembre n'est PAS ce qu'il sait le 15 décembre."""
    r = PIT.Registre.en_memoire()
    for o in SEC.faits_vers_observations(FAITS, INSTRUMENT):
        r.ecrire(o)
    cle = INSTRUMENT.cle()
    champ = "us-gaap:EarningsPerShareDiluted"
    assert r.savoir_a(cle, champ, "2026-10-01T00:00:00+00:00") is None
    assert r.savoir_a(cle, champ, "2026-11-01T00:00:00+00:00").valeur == 1.64
    assert r.savoir_a(cle, champ, "2026-12-15T00:00:00+00:00").valeur == 1.58


def test_reingerer_les_memes_faits_ne_duplique_rien():
    """La SEC republie l'intégralité de `companyfacts` à chaque appel : sans
    déduplication, chaque rafraîchissement doublerait l'historique."""
    r = PIT.Registre.en_memoire()
    obs = SEC.faits_vers_observations(FAITS, INSTRUMENT)
    for o in obs:
        r.ecrire(o)
    ecrits = sum(1 for o in SEC.faits_vers_observations(FAITS, INSTRUMENT)
                 if r.ecrire(o))
    assert ecrits == 0
    assert len(r.historique(INSTRUMENT.cle(),
                            "us-gaap:EarningsPerShareDiluted")) == 2


#  ═══════════════  6. l'URL et le chemin reseau, sans reseau  ═════════════════

def test_l_url_normalise_le_CIK_sur_dix_chiffres():
    """La SEC nomme ses fichiers `CIK0000320193.json`. Un CIK court donnerait
    un 404 silencieux que rien ne distinguerait d'un emetteur sans depots."""
    assert SEC.url_companyfacts("320193").endswith("CIK0000320193.json")
    assert SEC.url_companyfacts(320193) == SEC.url_companyfacts("0000320193")
    assert SEC.url_companyfacts("320193").startswith("https://data.sec.gov")


def test_un_CIK_illisible_est_REFUSE():
    for mauvais in ("", "AAPL", None):
        with pytest.raises(ValueError, match="CIK"):
            SEC.url_companyfacts(mauvais)


def test_le_chargement_transmet_le_USER_AGENT_declare(monkeypatch):
    """Le fair-access n'est pas une formalite : sans en-tete, la SEC bloque.
    On verifie que l'en-tete PART, sans appeler la SEC."""
    monkeypatch.setenv("SEC_USER_AGENT", "Vertex/1.0 (contact@exemple.fr)")
    vus = {}

    def _lecteur(url, entete):
        vus['url'] = url
        vus['entete'] = dict(entete)
        return {"cik": 320193, "facts": {}}

    out = SEC.charger_companyfacts("320193", lecteur=_lecteur)
    assert out["cik"] == 320193
    assert vus['entete']["User-Agent"] == "Vertex/1.0 (contact@exemple.fr)"
    assert vus['url'].endswith("CIK0000320193.json")


def test_le_chargement_REFUSE_avant_meme_de_construire_l_URL(monkeypatch):
    """L'ordre compte : sans User-Agent, aucune requete ne doit partir, pas
    meme une requete qui echouerait proprement."""
    monkeypatch.delenv("SEC_USER_AGENT", raising=False)
    appele = []
    with pytest.raises(SEC.EntitlementManquant):
        SEC.charger_companyfacts("320193",
                                 lecteur=lambda u, e: appele.append(1))
    assert appele == [], "le lecteur ne doit pas etre atteint"


def test_un_fait_dont_la_DATE_est_illisible_est_compte_et_ecarte():
    """Une date que Vertex ne sait pas lire ne devient pas une date par
    defaut : elle sortirait de l'ingestion sans que rien ne le signale."""
    d = {"cik": 1, "facts": {"us-gaap": {"X": {"units": {"USD": [
        {"end": "pas-une-date", "val": 5, "accn": "a", "filed": "2026-10-25"},
        {"end": "2026-09-30", "val": 7, "accn": "b", "filed": "25/10/2026"},
        {"end": "2026-09-30", "val": 9, "accn": "c", "filed": "2026-10-25"},
    ]}}}}}
    obs, rapport = SEC.faits_vers_observations(d, INSTRUMENT, avec_rapport=True)
    assert [o.valeur for o in obs] == [9]
    assert rapport["ignores_date_illisible"] == 2
    assert rapport["faits_lus"] == 3


def test_un_booleen_n_est_pas_un_nombre():
    """`True` vaut 1 en Python. L'accepter ferait entrer un drapeau XBRL dans
    une serie numerique comme s'il valait une unite."""
    d = {"cik": 1, "facts": {"us-gaap": {"X": {"units": {"USD": [
        {"end": "2026-09-30", "val": True, "accn": "a", "filed": "2026-10-25"},
    ]}}}}}
    obs, rapport = SEC.faits_vers_observations(d, INSTRUMENT, avec_rapport=True)
    assert obs == [] and rapport["ignores_valeur_non_numerique"] == 1


def test_une_fin_de_periode_illisible_est_aussi_REFUSEE():
    """La garde vaut pour les deux dates. Une periode devinee daterait un
    trimestre d'un instant ou il n'etait pas clos."""
    for mauvais in ("", "30-09-2026", None):
        with pytest.raises(ValueError, match="fin de période"):
            SEC.fin_de_periode(mauvais)


def test_une_unite_VIDE_ne_recoit_pas_de_devise():
    """XBRL laisse parfois l'unite vide. En deduire une devise attribuerait un
    libelle monetaire a une grandeur dont on ignore la nature."""
    d = {"cik": 1, "facts": {"us-gaap": {"X": {"units": {"": [
        {"end": "2026-09-30", "val": 3, "accn": "a", "filed": "2026-10-25"},
    ]}}}}}
    o = SEC.faits_vers_observations(d, INSTRUMENT)[0]
    assert o.unite == "" and o.devise == ""
