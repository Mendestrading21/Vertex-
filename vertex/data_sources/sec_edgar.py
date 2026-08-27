"""vertex.data_sources.sec_edgar — LE PREMIER PRODUCTEUR POINT-IN-TIME.

Le registre de la phase 2 attend une date de **disponibilité**. La SEC est la
première source qui la fournit réellement : chaque fait XBRL porte la période
qu'il décrit (`end`) *et* la date de dépôt (`filed`). C'est exactement la paire
que `yfinance.Ticker.info` ne donne pas — et dont l'absence vaut au domaine
fondamental d'être classé défaut P0 par l'audit du 24 août.

## Deux conversions, toutes deux dans le sens prudent

La SEC ne publie que des **dates**, sans heure ni fuseau. Le registre refuse
un instant sans fuseau, à juste titre : « 2026-10-25 » désigne vingt-six
instants. Il faut donc choisir, et le choix se fait dans la direction qui ne
donne jamais d'avance à un backtest.

1. **Un dépôt devient disponible à la FIN de sa journée.** Prendre le début
   donnerait jusqu'à vingt-quatre heures d'avance sur le marché — précisément
   la faute que la phase 2 existe pour rendre impossible.
2. **La journée est celle de New York**, fuseau du déposant, avec son heure
   d'été réelle. Un décalage fixe se tromperait d'une heure la moitié de
   l'année, et déplacerait d'un jour les dépôts faits près de minuit.

## Fair-access : Vertex n'invente aucun contact

La SEC exige un `User-Agent` nommant un contact réel. Vertex le lit dans
`SEC_USER_AGENT` et **refuse** d'appeler sans lui. Ni contact codé en dur, ni
emprunt de l'adresse de l'utilisateur : une donnée personnelle ne part pas chez
un tiers parce que le code en avait besoin.

## Ce que ce module ne fait jamais

Il ne transforme pas un tag absent en zéro. Un tag manquant est une **absence**,
un zéro est une **affirmation** — et une affirmation fausse se propage dans
tous les ratios calculés en aval. Il ne force pas non plus une valeur non
numérique : la coercer fabriquerait une donnée que la SEC n'a pas publiée.
"""
from __future__ import annotations

import datetime as _dt
import os
from zoneinfo import ZoneInfo

from vertex.domain.instruments import Instrument, normaliser_cik
from vertex.storage.point_in_time import Observation

#: Nom du fournisseur dans la provenance des observations.
PROVIDER = "SEC_EDGAR"

#: Fuseau du déposant. Les heures de dépôt de la SEC sont new-yorkaises.
_NY = ZoneInfo("America/New_York")

#: Racine de l'API XBRL. Aucune clé : seul le User-Agent est exigé.
BASE = "https://data.sec.gov"

#: Unités XBRL qui ne sont PAS des devises. Leur en attribuer une rendrait
#: comparables des grandeurs qui ne le sont pas.
_NON_MONETAIRES = ("shares", "pure", "Rate", "Y", "D")


class EntitlementManquant(RuntimeError):
    """Ce qu'il faut poser avant d'appeler la source."""


def user_agent() -> str:
    """Le `User-Agent` déclaré, ou un refus explicite.

    Le fair-access de la SEC exige un contact réel. Vertex ne l'invente pas et
    n'emprunte pas celui de l'utilisateur : c'est à lui de le poser.
    """
    v = (os.environ.get("SEC_USER_AGENT") or "").strip()
    if not v:
        raise EntitlementManquant(
            "SEC_USER_AGENT n'est pas défini. Le fair-access de la SEC exige "
            "un User-Agent nommant un contact réel (par exemple "
            "'Vertex/1.0 (prenom.nom@exemple.fr)'). Vertex ne l'invente pas.")
    return v


#  ────────────────────────────  conversion des dates  ─────────────────────────

def _jour(valeur, quoi: str) -> _dt.date:
    if not valeur or not isinstance(valeur, str):
        raise ValueError("%s manquante ou illisible : %r" % (quoi, valeur))
    try:
        return _dt.date.fromisoformat(valeur)
    except ValueError as exc:
        raise ValueError("%s illisible : %r" % (quoi, valeur)) from exc


def fin_de_journee_depot(date_iso) -> str:
    """L'instant où un dépôt daté devient connaissable : fin de journée à NY.

    Le choix de la FIN est le cœur du module. Un dépôt du 25 octobre n'est pas
    connaissable le 25 à 00:01 ; supposer le début donnerait à un backtest
    jusqu'à vingt-quatre heures d'avance sur le marché.
    """
    j = _jour(date_iso, "date de dépôt")
    return _dt.datetime.combine(j, _dt.time(23, 59, 59), tzinfo=_NY).isoformat()


def fin_de_periode(date_iso) -> str:
    """La fin de la période décrite : `end: 2026-09-30` clôt ce jour-là.

    Prendre minuit au début du 30 septembre daterait le trimestre d'un instant
    où il n'était pas encore clos.
    """
    j = _jour(date_iso, "fin de période")
    return _dt.datetime.combine(j, _dt.time(23, 59, 59), tzinfo=_NY).isoformat()


def _devise(unite: str) -> str:
    """La devise portée par une unité XBRL, ou rien.

    `USD` et `USD/shares` sont libellés en dollars ; `shares` ne l'est pas.
    Inventer une devise pour une grandeur non monétaire la rendrait comparable
    à un montant, ce qu'elle n'est pas.
    """
    if not unite:
        return ""
    tete = unite.split("/")[0]
    if tete in _NON_MONETAIRES or len(tete) != 3 or not tete.isalpha():
        return ""
    return tete.upper()


#  ───────────────────────────  faits XBRL → observations  ────────────────────

def faits_vers_observations(companyfacts: dict, instrument: Instrument,
                            *, avec_rapport: bool = False):
    """Convertit un `companyfacts` SEC en observations point-in-time.

    Ce qui est **ignoré** est compté, jamais silencieux : un fait sans date de
    dépôt ne peut pas être daté en disponibilité, et le laisser passer
    contaminerait le registre — mais l'écarter sans le dire cacherait un trou
    dans l'ingestion.

    Les retraitements deviennent des **révisions** : le même (tag, période,
    unité) déposé plusieurs fois est ordonné par date de dépôt, et chaque
    révision cite le dépôt qu'elle corrige dans son `lineage`.
    """
    rapport = {"faits_lus": 0, "ignores_sans_depot": 0,
               "ignores_valeur_non_numerique": 0, "ignores_date_illisible": 0}
    par_serie: dict = {}

    for taxonomie, tags in ((companyfacts or {}).get("facts") or {}).items():
        for tag, corps in (tags or {}).items():
            for unite, entrees in ((corps or {}).get("units") or {}).items():
                for e in (entrees or []):
                    rapport["faits_lus"] += 1
                    val = e.get("val")
                    if not isinstance(val, (int, float)) or isinstance(val, bool):
                        rapport["ignores_valeur_non_numerique"] += 1
                        continue
                    if not e.get("filed"):
                        rapport["ignores_sans_depot"] += 1
                        continue
                    try:
                        observed = fin_de_periode(e.get("end"))
                        available = fin_de_journee_depot(e.get("filed"))
                    except ValueError:
                        rapport["ignores_date_illisible"] += 1
                        continue
                    cle = ("%s:%s" % (taxonomie, tag), e.get("end"), unite)
                    par_serie.setdefault(cle, []).append(
                        (e.get("filed"), observed, available, val, e))

    sorties = []
    for (champ, _fin, unite), lot in par_serie.items():
        #  Ordonné par dépôt : la révision N corrige la N-1, et c'est la date
        #  de dépôt — pas l'ordre du fichier — qui fait foi.
        lot.sort(key=lambda x: x[0])
        precedent = ""
        for rang, (_filed, observed, available, val, e) in enumerate(lot):
            sorties.append(Observation(
                instrument=instrument,
                champ=champ,
                valeur=val,
                unite=unite,
                devise=_devise(unite),
                observed_at=observed,
                available_at=available,
                provider=PROVIDER,
                provider_record_id=str(e.get("accn") or ""),
                mode="EOD",
                quality="MEASURED",
                revision=rang,
                lineage=((precedent,) if precedent else ()),
            ))
            precedent = str(e.get("accn") or "")

    sorties.sort(key=lambda o: (o.champ, o.available_at))
    return (sorties, rapport) if avec_rapport else sorties


#  ─────────────────────────────  accès réseau  ───────────────────────────────

def url_companyfacts(cik) -> str:
    """L'URL XBRL d'un émetteur. Le CIK est normalisé sur dix chiffres."""
    c = normaliser_cik(cik)
    if not c:
        raise ValueError("CIK illisible : %r" % (cik,))
    return "%s/api/xbrl/companyfacts/CIK%s.json" % (BASE, c)


def charger_companyfacts(cik, *, lecteur=None, timeout: float = 20.0) -> dict:
    """Récupère `companyfacts` chez la SEC. REFUSE sans `SEC_USER_AGENT`.

    `lecteur` permet d'injecter une lecture (fixture, cache disque) sans
    toucher au réseau : c'est ce qui rend ce chemin éprouvable là où la SEC
    n'est pas appelable.
    """
    entete = {"User-Agent": user_agent(), "Accept-Encoding": "gzip, deflate"}
    url = url_companyfacts(cik)
    if lecteur is not None:
        return lecteur(url, entete)
    import json
    import urllib.request
    requete = urllib.request.Request(url, headers=entete)
    with urllib.request.urlopen(requete, timeout=timeout) as reponse:
        brut = reponse.read()
        #  L'en-tête DEMANDE gzip et la SEC l'accorde : décoder sans
        #  décompresser levait `UnicodeDecodeError: byte 0x8b` — les deux
        #  premiers octets d'un flux gzip. Ce chemin n'avait jamais été
        #  exercé en réseau réel, seulement par `lecteur` injecté ; le défaut
        #  attendait donc le premier appel véritable.
        if (reponse.headers.get("Content-Encoding") or "").lower() == "gzip":
            import gzip as _gz
            brut = _gz.decompress(brut)
        return json.loads(brut.decode("utf-8"))


__all__ = [
    "PROVIDER", "BASE", "EntitlementManquant", "user_agent",
    "fin_de_journee_depot", "fin_de_periode",
    "faits_vers_observations", "url_companyfacts", "charger_companyfacts",
]
