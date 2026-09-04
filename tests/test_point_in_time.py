"""Vertex Test 1.0 · Phase 2 — CE QUE VERTEX SAVAIT À T, ET RIEN DE PLUS.

L'audit du 24 août 2026 nomme le défaut que ce lot existe pour rendre
impossible : *« un score historique peut bénéficier d'informations futures »*.
Les fondamentaux venaient de `yfinance.Ticker.info`, qui rend la valeur
**actuelle** — révisions comprises — sans dire à quelle date elle est devenue
connaissable. Rétrotester là-dessus mesure une clairvoyance, pas une méthode.

La distinction qui porte tout ce fichier :

- `observed_at` — l'instant que la donnée **décrit** (fin du trimestre) ;
- `available_at` — l'instant où elle est devenue **connaissable** (publication) ;
- `received_at` — l'instant où Vertex l'a **reçue**.

Un résultat de trimestre clos le 30 septembre publié le 25 octobre ne doit pas
exister pour Vertex le 1er octobre. Filtrer sur `observed_at` le rendrait
visible — et c'est exactement l'erreur qu'un registre point-in-time doit rendre
impossible, pas seulement déconseiller.

Ces tests sont écrits AVANT l'implémentation : ils décrivent l'acceptation.
"""
from __future__ import annotations

import datetime as dt

import pytest

from vertex.domain import instruments as I
from vertex.storage import point_in_time as PIT
from vertex.storage import schemas as S


def _t(iso: str) -> str:
    return iso


#  ═══════════════════  1. l'identité d'un instrument  ═════════════════════════

def test_un_ticker_n_est_PAS_une_identite():
    """Les tickers se recyclent et se changent. `FB` est devenu `META` ; un
    ticker rendu à la corbeille peut être réattribué à une autre société des
    années plus tard. Bâtir l'identité dessus mélangerait deux entreprises dans
    la même série historique."""
    ancien = I.Instrument(conid=107113386, ticker="FB", currency="USD")
    actuel = I.Instrument(conid=107113386, ticker="META", currency="USD")
    assert ancien.cle() == actuel.cle(), (
        "un changement de ticker ne change pas l'instrument")
    autre = I.Instrument(conid=999, ticker="META", currency="USD")
    assert autre.cle() != actuel.cle(), (
        "deux sociétés ayant porté le même ticker ne sont pas la même")


def test_la_cle_prefere_le_conid_puis_le_cik_puis_le_ticker():
    """Ordre d'autorité : le conId est stable chez le courtier qui détient les
    positions ; le CIK est stable chez l'émetteur ; le ticker ne l'est pas.
    Un instrument sans aucun des deux premiers reste utilisable, mais sa clé
    DIT qu'elle est fragile."""
    assert I.Instrument(conid=1, cik="0000320193", ticker="AAPL").cle() == "IB:1"
    assert I.Instrument(cik="0000320193", ticker="AAPL").cle() == "CIK:0000320193"
    c = I.Instrument(ticker="AAPL", exchange="NASDAQ").cle()
    assert c.startswith("TICKER:")
    assert I.Instrument(ticker="AAPL").fragile is True
    assert I.Instrument(conid=1, ticker="AAPL").fragile is False


def test_un_instrument_sans_aucun_identifiant_est_REFUSE():
    """Un enregistrement sans identité ne pourra jamais être relu ni relié.
    L'accepter reviendrait à écrire dans le vide."""
    with pytest.raises(ValueError, match="identifiant"):
        I.Instrument(currency="USD")


def test_le_cik_est_normalise_sur_dix_chiffres():
    """La SEC publie tantôt `320193`, tantôt `0000320193`. Deux écritures du
    même émetteur produiraient deux séries distinctes."""
    assert I.Instrument(cik="320193").cik == "0000320193"
    assert I.Instrument(cik="0000320193").cle() == I.Instrument(cik=320193).cle()


def test_la_devise_fait_partie_de_l_identite_de_cotation():
    """La même société cotée en USD et en EUR n'a pas la même série de prix.
    Les confondre produirait des rendements fantômes au taux de change."""
    usd = I.Instrument(ticker="SAP", exchange="NYSE", currency="USD")
    eur = I.Instrument(ticker="SAP", exchange="XETRA", currency="EUR")
    assert usd.cle() != eur.cle()


#  ═══════════════  2. le registre : append-only et point-in-time  ═════════════

@pytest.fixture()
def registre(tmp_path):
    return PIT.Registre(tmp_path / "pit")


def _obs(**kw):
    base = dict(
        instrument=I.Instrument(conid=265598, ticker="AAPL"),
        champ="eps_diluted",
        valeur=1.64,
        unite="USD_par_action",
        devise="USD",
        observed_at="2026-09-30T00:00:00+00:00",
        available_at="2026-10-25T20:05:00+00:00",
        provider="SEC_EDGAR",
        provider_record_id="0000320193-26-000101",
        mode="EOD",
    )
    base.update(kw)
    return PIT.Observation(**base)


def test_ce_que_vertex_savait_filtre_sur_la_DISPONIBILITE_pas_l_observation():
    """LE test du lot. Un trimestre clos le 30 septembre et publié le 25 octobre
    n'existe pas pour Vertex le 1er octobre. Filtrer sur `observed_at` le
    rendrait visible et transformerait un backtest en clairvoyance."""
    r = PIT.Registre.en_memoire()
    r.ecrire(_obs())
    avant = r.savoir_a("IB:265598", "eps_diluted", "2026-10-01T00:00:00+00:00")
    apres = r.savoir_a("IB:265598", "eps_diluted", "2026-11-01T00:00:00+00:00")
    assert avant is None, (
        "la donnée était observée mais PAS ENCORE PUBLIÉE — la voir serait "
        "utiliser une information future")
    assert apres is not None and apres.valeur == 1.64


def test_une_revision_ne_REECRIT_jamais_la_valeur_d_origine():
    """La SEC republie. Le registre est append-only : la révision s'ajoute, et
    ce que Vertex savait AVANT elle reste interrogeable — sinon on ne pourrait
    plus expliquer une décision passée."""
    r = PIT.Registre.en_memoire()
    r.ecrire(_obs(valeur=1.64, revision=0))
    r.ecrire(_obs(valeur=1.58, revision=1,
                  available_at="2026-12-01T12:00:00+00:00",
                  provider_record_id="0000320193-26-000188"))
    assert r.savoir_a("IB:265598", "eps_diluted",
                      "2026-11-01T00:00:00+00:00").valeur == 1.64
    assert r.savoir_a("IB:265598", "eps_diluted",
                      "2026-12-15T00:00:00+00:00").valeur == 1.58
    assert len(r.historique("IB:265598", "eps_diluted")) == 2


def test_ecrire_deux_fois_le_MEME_enregistrement_ne_le_duplique_pas():
    """Rejouer une ingestion doit être sans effet. Sans cela, un incident
    réseau doublerait des observations et fausserait tout comptage."""
    r = PIT.Registre.en_memoire()
    assert r.ecrire(_obs()) is True
    assert r.ecrire(_obs()) is False
    assert len(r.historique("IB:265598", "eps_diluted")) == 1


def test_le_registre_REFUSE_de_modifier_une_observation_ecrite():
    """Append-only n'est pas une convention de nommage : la tentative doit
    échouer."""
    r = PIT.Registre.en_memoire()
    r.ecrire(_obs())
    with pytest.raises(PIT.RegistreImmuable):
        r.remplacer("IB:265598", "eps_diluted", 99.0)


def test_une_disponibilite_anterieure_a_l_observation_est_REFUSEE():
    """Connaître un résultat avant la fin du trimestre qu'il décrit n'est pas
    une donnée : c'est une erreur d'ingestion, et la laisser passer
    contaminerait tous les backtests en aval."""
    with pytest.raises(ValueError, match="disponible avant"):
        PIT.Registre.en_memoire().ecrire(
            _obs(observed_at="2026-09-30T00:00:00+00:00",
                 available_at="2026-09-01T00:00:00+00:00"))


def test_une_observation_sans_date_de_disponibilite_est_REFUSEE():
    """Sans `available_at`, on ne peut PAS répondre « que savait-on à T ». La
    déduire de `observed_at` serait précisément l'hypothèse fausse."""
    with pytest.raises(ValueError, match="available_at"):
        PIT.Registre.en_memoire().ecrire(_obs(available_at=""))


#  ═══════════════════  3. fuseaux, heure d'été, comparabilité  ════════════════

def test_les_instants_sont_compares_en_UTC_quel_que_soit_leur_fuseau():
    """Publication à 16:05 New York = 20:05 UTC.

    Deux écritures du MÊME instant dans deux fuseaux différents doivent donner
    la même réponse ; une écriture qui *ressemble* à « plus tard » mais désigne
    un instant antérieur doit donner l'autre. Comparer des chaînes naïves —
    « 22:00 » > « 20:05 » — inverserait précisément ce cas.
    """
    r = PIT.Registre.en_memoire()
    r.ecrire(_obs(available_at="2026-10-25T16:05:00-04:00"))
    q = lambda t: r.savoir_a("IB:265598", "eps_diluted", t)  # noqa: E731

    #  Le même instant (21:00 UTC), écrit de trois façons : même réponse.
    assert q("2026-10-25T21:00:00+00:00") is not None
    assert q("2026-10-25T22:00:00+01:00") is not None
    assert q("2026-10-25T17:00:00-04:00") is not None

    #  « 22:00 » dans un fuseau très en avance désigne 19:00 UTC : AVANT la
    #  publication. La chaîne semble plus tardive, l'instant ne l'est pas.
    assert q("2026-10-25T22:00:00+03:00") is None
    assert q("2026-10-25T20:04:59+00:00") is None


def test_un_instant_sans_fuseau_est_REFUSE():
    """« 2026-10-25T20:05:00 » ne désigne pas un instant : il en désigne
    vingt-six. L'interpréter en UTC par défaut serait une supposition
    silencieuse qui décale les publications d'une demi-journée."""
    with pytest.raises(ValueError, match="fuseau"):
        PIT.Registre.en_memoire().ecrire(_obs(available_at="2026-10-25T20:05:00"))


def test_le_changement_d_heure_ne_deplace_pas_une_publication():
    """Les États-Unis quittent l'heure d'été le 1er novembre 2026. Une
    publication du 30 octobre (-04:00) et une du 5 novembre (-05:00) doivent
    rester dans l'ordre où elles se sont produites."""
    r = PIT.Registre.en_memoire()
    r.ecrire(_obs(champ="pib", available_at="2026-10-30T16:00:00-04:00",
                  observed_at="2026-09-30T00:00:00+00:00", valeur=1))
    r.ecrire(_obs(champ="pib", available_at="2026-11-05T16:00:00-05:00",
                  observed_at="2026-09-30T00:00:00+00:00", valeur=2,
                  revision=1, provider_record_id="autre"))
    h = r.historique("IB:265598", "pib")
    assert [o.valeur for o in h] == [1, 2]


#  ═════════════════  4. actions sur titre : split et changement  ══════════════

def test_un_split_est_une_OBSERVATION_pas_une_reecriture_du_passe():
    """Ajuster rétroactivement les prix stockés effacerait ce que Vertex a
    réellement vu. Le facteur est enregistré ; l'ajustement se calcule à la
    lecture, et reste explicable."""
    r = PIT.Registre.en_memoire()
    r.ecrire(_obs(champ="split_facteur", valeur=4.0, unite="ratio",
                  observed_at="2026-08-31T00:00:00+00:00",
                  available_at="2026-08-31T00:00:00+00:00",
                  provider_record_id="split-2026-08-31"))
    avant = r.savoir_a("IB:265598", "split_facteur",
                       "2026-08-30T00:00:00+00:00")
    apres = r.savoir_a("IB:265598", "split_facteur",
                       "2026-09-01T00:00:00+00:00")
    assert avant is None and apres.valeur == 4.0


def test_un_changement_de_ticker_garde_la_serie_sur_la_meme_cle():
    """La série de META doit contenir ce qui a été observé du temps de FB."""
    r = PIT.Registre.en_memoire()
    fb = I.Instrument(conid=107113386, ticker="FB")
    meta = I.Instrument(conid=107113386, ticker="META")
    r.ecrire(_obs(instrument=fb, champ="revenu", valeur=1,
                  provider_record_id="a"))
    r.ecrire(_obs(instrument=meta, champ="revenu", valeur=2, revision=1,
                  available_at="2026-11-25T20:05:00+00:00",
                  provider_record_id="b"))
    assert len(r.historique(meta.cle(), "revenu")) == 2


#  ══════════════════════  5. intégrité et provenance  ═════════════════════════

def test_chaque_observation_porte_les_seize_champs_du_contrat():
    """QUALITY_STANDARD §1 et le programme phase 2 : une valeur sans provenance
    complète ne peut être ni auditée ni rejouée."""
    d = _obs().to_dict()
    for champ in ("instrument_id", "champ", "valeur", "unite", "devise",
                  "observed_at", "available_at", "received_at", "provider",
                  "provider_record_id", "mode", "quality", "revision",
                  "lineage", "schema_version", "checksum"):
        assert champ in d, champ


def test_le_checksum_change_si_la_valeur_change():
    """Un checksum qui ne bouge pas ne détecte rien."""
    a = _obs(valeur=1.64).checksum
    b = _obs(valeur=1.58).checksum
    assert a and b and a != b


def test_le_checksum_ne_depend_PAS_de_l_instant_de_reception():
    """Deux ingestions de la même donnée à deux heures différentes décrivent le
    même fait. Sinon la déduplication ne dédupliquerait jamais rien."""
    a = _obs(received_at="2026-10-25T20:06:00+00:00").checksum
    b = _obs(received_at="2026-10-26T09:00:00+00:00").checksum
    assert a == b


def test_le_registre_detecte_un_fichier_altere(tmp_path):
    """Une ligne modifiée à la main doit être vue, pas servie."""
    r = PIT.Registre(tmp_path / "pit")
    r.ecrire(_obs())
    chemin = r.chemin_journal()
    contenu = chemin.read_text(encoding="utf-8").replace('1.64', '9.99')
    chemin.write_text(contenu, encoding="utf-8")
    anomalies = PIT.Registre(tmp_path / "pit").verifier()
    assert anomalies, "un enregistrement altéré doit être signalé"


#  ═══════════════════════  6. schéma et migration  ════════════════════════════

def test_une_observation_porte_la_version_de_schema_courante():
    assert _obs().schema_version == S.VERSION_COURANTE


def test_une_version_future_est_REFUSEE_et_non_devinee():
    """Lire un format qu'on ne comprend pas produirait une donnée fausse
    présentée comme sûre."""
    with pytest.raises(ValueError, match="version"):
        S.migrer({"schema_version": S.VERSION_COURANTE + 99})


def test_chaque_migration_est_REVERSIBLE():
    """Le programme exige des migrations réversibles : un lot qu'on ne peut pas
    annuler n'a pas de rollback, donc pas de droit d'être publié."""
    for v, (avant, apres) in S.MIGRATIONS.items():
        assert callable(avant) and callable(apres), v


def test_migrer_puis_retrograder_rend_l_enregistrement_d_origine():
    if not S.MIGRATIONS:
        pytest.skip("aucune migration déclarée à cette version")
    for v, (monter, descendre) in S.MIGRATIONS.items():
        origine = {"schema_version": v - 1, "champ": "x", "valeur": 1}
        assert descendre(monter(dict(origine))) == origine, v


def test_un_enregistrement_sans_version_est_REFUSE():
    """Sans version, on ne sait pas comment lire — et le supposer produirait
    une donnée fausse. Le refus est la seule reponse honnete."""
    with pytest.raises(ValueError, match="sans version"):
        S.migrer({"champ": "x", "valeur": 1})
    with pytest.raises(ValueError, match="sans version"):
        S.migrer({"schema_version": "1", "champ": "x"})


def test_un_saut_de_format_sans_migration_declaree_est_REFUSE(monkeypatch):
    """Une version passee dont la migration n'existe pas ne s'improvise pas a
    la lecture : combler le trou en devinant serait inventer de la donnee."""
    monkeypatch.setattr(S, "VERSION_COURANTE", 3)
    monkeypatch.setattr(S, "MIGRATIONS", {})
    with pytest.raises(ValueError, match="aucune migration"):
        S.migrer({"schema_version": 1, "champ": "x"})


def test_une_migration_declaree_est_appliquee_de_proche_en_proche(monkeypatch):
    """Contre-epreuve du refus : quand le couple existe, la montee se fait
    version par version, et l'enregistrement porte la version d'arrivee."""
    monkeypatch.setattr(S, "VERSION_COURANTE", 3)
    monkeypatch.setattr(S, "MIGRATIONS", {
        2: (lambda d: {**d, "ajoute_v2": True},
            lambda d: {k: v for k, v in d.items() if k != "ajoute_v2"}),
        3: (lambda d: {**d, "ajoute_v3": True},
            lambda d: {k: v for k, v in d.items() if k != "ajoute_v3"}),
    })
    out = S.migrer({"schema_version": 1, "champ": "x"})
    assert out["schema_version"] == 3
    assert out["ajoute_v2"] is True and out["ajoute_v3"] is True


def test_le_registre_sur_DISQUE_relit_ce_qu_il_a_ecrit(tmp_path):
    """Un registre qui ne se relit pas n'est pas un registre : la preuve
    disparaitrait au redemarrage."""
    r1 = PIT.Registre(tmp_path / "pit")
    r1.ecrire(_obs())
    r2 = PIT.Registre(tmp_path / "pit")
    trouve = r2.savoir_a("IB:265598", "eps_diluted", "2026-11-01T00:00:00+00:00")
    assert trouve is not None and trouve.valeur == 1.64
    assert r2.verifier() == [], "un journal intact ne doit rien signaler"
    assert r2.ecrire(_obs()) is False, "la deduplication survit au redemarrage"


def test_un_registre_intact_ne_signale_RIEN(tmp_path):
    """Contre-epreuve de la detection d'alteration : un verificateur qui crie
    sur un journal sain serait ignore des la premiere fausse alerte."""
    r = PIT.Registre(tmp_path / "pit2")
    r.ecrire(_obs())
    r.ecrire(_obs(champ="revenu", valeur=94_000, provider_record_id="autre"))
    assert r.verifier() == []


def test_un_instant_de_QUESTION_sans_fuseau_est_aussi_refuse():
    """La garde vaut dans les deux sens : demander « que savait-on a 20:05 »
    sans dire ou serait une question a vingt-six reponses."""
    r = PIT.Registre.en_memoire()
    r.ecrire(_obs())
    with pytest.raises(ValueError, match="fuseau"):
        r.savoir_a("IB:265598", "eps_diluted", "2026-11-01T00:00:00")
