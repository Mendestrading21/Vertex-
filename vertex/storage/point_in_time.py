"""vertex.storage.point_in_time — CE QUE VERTEX SAVAIT À T.

L'audit du 24 août 2026 nomme le défaut que ce module existe pour rendre
**impossible** : *« un score historique peut bénéficier d'informations
futures »*. Les fondamentaux venaient de `yfinance.Ticker.info`, qui rend la
valeur *actuelle* — révisions comprises — sans jamais dire à quelle date elle
est devenue connaissable. Rétrotester là-dessus mesure une clairvoyance, pas
une méthode.

## Trois instants, jamais confondus

| champ | ce qu'il désigne |
|---|---|
| `observed_at` | l'instant que la donnée **décrit** (fin de trimestre) |
| `available_at` | l'instant où elle est devenue **connaissable** (publication) |
| `received_at` | l'instant où Vertex l'a **reçue** |

`savoir_a()` filtre sur `available_at`. Un trimestre clos le 30 septembre et
publié le 25 octobre n'existe pas pour Vertex le 1er octobre. Filtrer sur
`observed_at` — l'erreur naturelle, celle qu'on écrit sans y penser — le
rendrait visible.

## Append-only, et ce que cela protège

Une révision **s'ajoute**. Ce que Vertex savait avant elle reste interrogeable,
sinon une décision passée deviendrait inexplicable : on lirait le chiffre
corrigé en croyant lire celui sur lequel la décision a été prise.

`remplacer()` existe et **lève** : l'immuabilité n'est pas une convention de
nommage qu'on respecte quand on y pense.

## Ce que ce module ne fait pas

Il n'ajuste rien. Un split est enregistré comme une **observation** portant son
facteur ; l'ajustement se calcule à la lecture et reste explicable. Réécrire
les prix passés effacerait ce que Vertex a réellement vu — et un registre qui
réécrit son passé ne sert plus à expliquer une décision.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from vertex.domain.instruments import Instrument
from vertex.storage import schemas


class RegistreImmuable(RuntimeError):
    """Toute tentative de modifier ce qui est écrit."""


def _instant(valeur: str, quoi: str) -> _dt.datetime:
    """Un instant réel, en UTC. Refuse ce qui n'en est pas un.

    Une chaîne sans fuseau — « 2026-10-25T20:05:00 » — ne désigne pas un
    instant : elle en désigne vingt-six. L'interpréter en UTC par défaut est
    une supposition silencieuse qui décale les publications d'une demi-journée
    et inverse l'ordre de deux dépêches.
    """
    if not valeur:
        raise ValueError("%s manquant" % quoi)
    try:
        dt = _dt.datetime.fromisoformat(str(valeur).replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("%s illisible : %r" % (quoi, valeur)) from exc
    if dt.tzinfo is None:
        raise ValueError(
            "%s sans fuseau horaire : %r — un instant sans fuseau n'en est "
            "pas un, et le supposer en UTC décalerait la publication"
            % (quoi, valeur))
    return dt.astimezone(_dt.timezone.utc)


def _maintenant() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


@dataclass(frozen=True)
class Observation:
    """Une valeur, d'où elle vient, quand elle décrit, quand elle fut connaissable."""

    instrument: Instrument
    champ: str
    valeur: object
    observed_at: str
    available_at: str
    provider: str
    provider_record_id: str = ""
    unite: str = ""
    devise: str = ""
    mode: str = "EOD"
    quality: str = "MEASURED"
    revision: int = 0
    lineage: tuple = field(default_factory=tuple)
    received_at: str = field(default_factory=_maintenant)
    schema_version: int = schemas.VERSION_COURANTE

    #  ── intégrité ────────────────────────────────────────────────────
    @property
    def checksum(self) -> str:
        """Empreinte du FAIT décrit, pas de l'instant où on l'a reçu.

        `received_at` est volontairement exclu : deux ingestions de la même
        donnée à deux heures différentes décrivent le même fait. L'inclure
        empêcherait toute déduplication — un incident réseau doublerait des
        observations et fausserait tout comptage.
        """
        noyau = json.dumps({
            "instrument_id": self.instrument.cle(), "champ": self.champ,
            "valeur": self.valeur, "unite": self.unite, "devise": self.devise,
            "observed_at": self.observed_at, "available_at": self.available_at,
            "provider": self.provider,
            "provider_record_id": self.provider_record_id,
            "revision": self.revision, "schema_version": self.schema_version,
        }, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(noyau.encode("utf-8")).hexdigest()

    def to_dict(self) -> dict:
        return {
            "instrument_id": self.instrument.cle(),
            "instrument": self.instrument.to_dict(),
            "champ": self.champ, "valeur": self.valeur,
            "unite": self.unite, "devise": self.devise,
            "observed_at": self.observed_at,
            "available_at": self.available_at,
            "received_at": self.received_at,
            "provider": self.provider,
            "provider_record_id": self.provider_record_id,
            "mode": self.mode, "quality": self.quality,
            "revision": self.revision, "lineage": list(self.lineage),
            "schema_version": self.schema_version,
            "checksum": self.checksum,
        }


class Registre:
    """Le journal append-only des observations.

    Un fichier JSON Lines par registre : une observation par ligne, jamais
    réécrite. Le format est délibérément lisible — un registre qu'on ne peut
    pas inspecter à l'œil devient un registre qu'on croit sur parole.
    """

    def __init__(self, racine):
        self.racine = Path(racine) if racine is not None else None
        self._lignes: list = []
        self._vus: set = set()
        if self.racine is not None:
            self.racine.mkdir(parents=True, exist_ok=True)
            self._relire()

    @classmethod
    def en_memoire(cls) -> "Registre":
        """Un registre sans disque — pour les tests et les calculs jetables."""
        return cls(None)

    def chemin_journal(self) -> Path:
        return self.racine / "observations.jsonl"

    def _relire(self):
        p = self.chemin_journal()
        if not p.exists():
            return
        for ligne in p.read_text(encoding="utf-8").splitlines():
            if not ligne.strip():
                continue
            d = json.loads(ligne)
            self._lignes.append(d)
            self._vus.add(d.get("checksum"))

    #  ── écriture ─────────────────────────────────────────────────────
    def ecrire(self, obs: Observation) -> bool:
        """Ajoute une observation. Rend `False` si elle était déjà connue.

        Rejouer une ingestion doit être **sans effet** : sans cela, une reprise
        après incident doublerait des observations.
        """
        o = _instant(obs.observed_at, "observed_at")
        a = _instant(obs.available_at, "available_at")
        if a < o:
            raise ValueError(
                "disponible avant d'être observée (%s < %s) — connaître un "
                "résultat avant la fin de la période qu'il décrit n'est pas "
                "une donnée, c'est une erreur d'ingestion"
                % (obs.available_at, obs.observed_at))
        _instant(obs.received_at, "received_at")

        d = obs.to_dict()
        if d["checksum"] in self._vus:
            return False
        self._vus.add(d["checksum"])
        self._lignes.append(d)
        if self.racine is not None:
            with self.chemin_journal().open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(d, ensure_ascii=False, default=str) + "\n")
        return True

    def remplacer(self, *_a, **_k):
        """N'existe que pour échouer.

        Append-only n'est pas une convention de nommage : un appelant qui
        cherche à corriger une valeur doit écrire une RÉVISION, qui laisse
        l'original interrogeable.
        """
        raise RegistreImmuable(
            "registre append-only : une correction s'écrit comme une révision "
            "(revision=N+1), jamais en remplaçant — sinon une décision passée "
            "devient inexplicable")

    #  ── lecture ──────────────────────────────────────────────────────
    def historique(self, instrument_id: str, champ: str) -> list:
        """Toutes les observations connues, dans l'ordre de disponibilité."""
        lot = [d for d in self._lignes
               if d["instrument_id"] == instrument_id and d["champ"] == champ]
        lot.sort(key=lambda d: _instant(d["available_at"], "available_at"))
        return [_depuis_dict(d) for d in lot]

    def savoir_a(self, instrument_id: str, champ: str, t: str):
        """Ce que Vertex savait de ce champ à l'instant `t`, ou `None`.

        Le filtre porte sur `available_at`. C'est TOUT le module : une donnée
        observée mais pas encore publiée n'existe pas pour une décision datée
        d'avant sa publication.
        """
        limite = _instant(t, "instant de la question")
        connues = [d for d in self._lignes
                   if d["instrument_id"] == instrument_id
                   and d["champ"] == champ
                   and _instant(d["available_at"], "available_at") <= limite]
        if not connues:
            return None
        connues.sort(key=lambda d: (_instant(d["available_at"], "available_at"),
                                    d.get("revision", 0)))
        return _depuis_dict(connues[-1])

    #  ── intégrité ────────────────────────────────────────────────────
    def verifier(self) -> list:
        """Les enregistrements dont le checksum ne correspond plus au contenu.

        Une ligne modifiée à la main doit être VUE, pas servie : un registre
        qu'on croit sur parole ne prouve rien.
        """
        anomalies = []
        for i, d in enumerate(self._lignes):
            attendu = d.get("checksum")
            try:
                recalcule = _depuis_dict(d).checksum
            except Exception as exc:  # noqa: BLE001
                anomalies.append({"ligne": i, "erreur": str(exc)[:120]})
                continue
            if attendu != recalcule:
                anomalies.append({"ligne": i, "champ": d.get("champ"),
                                  "checksum_enregistre": attendu,
                                  "checksum_recalcule": recalcule})
        return anomalies


class DisponibiliteInconnue(RuntimeError):
    """Cette valeur ne peut pas servir de preuve historique."""


def exiger_disponibilite(valeur, *, contexte: str):
    """Refuse une valeur dont on ignore QUAND elle est devenue connaissable.

    `AUDIT-TOTAL-2026-08-25` P0.2 : « aucun nouveau score historique ne doit
    contourner ce socle ». Une intention ne tient pas ; un refus, si.

    ## Pourquoi un refus et pas un avertissement

    Mesuré le 25 août 2026 : les fondamentaux de `yfinance.info` ne portent
    qu'un `as_of` **au niveau du lot**, égal à l'instant de RÉCEPTION. Le P/E
    servi aujourd'hui reflète un dépôt dont la date de publication est
    inconnue de Vertex. Joindre cette valeur à une date passée donnerait à un
    rétrotest une information que le marché n'avait pas — le défaut P0 que la
    phase 2 rend impossible plutôt qu'improbable.

    ## Ce que ce refus ne dit PAS

    Il ne dit pas que la valeur est fausse. Elle est parfaitement utilisable
    pour décrire le PRÉSENT — c'est son usage actuel dans la fiche d'un titre.
    Il dit qu'elle ne peut pas servir de preuve sur le PASSÉ.

    Accepte un `Observation`, un dict, ou tout objet portant `available_at`.
    """
    dispo = None
    if isinstance(valeur, Observation):
        dispo = valeur.available_at
    elif isinstance(valeur, dict):
        dispo = valeur.get('available_at')
    else:
        dispo = getattr(valeur, 'available_at', None)
    if not dispo:
        raise DisponibiliteInconnue(
            "%s : la date de DISPONIBILITE est inconnue, cette valeur ne peut "
            "pas fonder une preuve historique. Elle reste utilisable pour "
            "decrire le present." % contexte)
    return valeur


def _depuis_dict(d: dict) -> Observation:
    d = schemas.migrer(dict(d))
    ins = d.get("instrument") or {}
    return Observation(
        instrument=Instrument(
            conid=ins.get("conid"), cik=ins.get("cik", ""),
            ticker=ins.get("ticker", ""), exchange=ins.get("exchange", ""),
            currency=ins.get("currency", "USD")),
        champ=d["champ"], valeur=d["valeur"],
        unite=d.get("unite", ""), devise=d.get("devise", ""),
        observed_at=d["observed_at"], available_at=d["available_at"],
        received_at=d.get("received_at", ""),
        provider=d.get("provider", ""),
        provider_record_id=d.get("provider_record_id", ""),
        mode=d.get("mode", "EOD"), quality=d.get("quality", "MEASURED"),
        revision=int(d.get("revision", 0)),
        lineage=tuple(d.get("lineage") or ()),
        schema_version=d["schema_version"])


__all__ = ["Observation", "Registre", "RegistreImmuable"]
