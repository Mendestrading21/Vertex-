"""vertex.domain.instruments — L'IDENTITÉ CANONIQUE D'UN INSTRUMENT.

Un ticker n'est pas une identité. `FB` est devenu `META` sans changer de
société ; et un ticker rendu à la corbeille peut être réattribué à une autre
entreprise des années plus tard. Bâtir une série historique sur le ticker
mélange donc deux sociétés dans la même courbe — silencieusement, et d'autant
plus dangereusement que le graphique reste joli.

## L'ordre d'autorité

1. **conId IBKR** — stable chez le courtier qui détient réellement les
   positions. C'est l'identité la plus forte dont Vertex dispose, parce que
   c'est celle sur laquelle le P&L est calculé.
2. **CIK SEC** — stable chez l'émetteur, et c'est la seule clé qui relie les
   dépôts réglementaires à une société.
3. **ticker + place + devise** — utilisable, mais **fragile**, et l'objet le
   dit (`fragile`). Un appelant peut décider de refuser une clé fragile pour
   une preuve historique ; il ne peut pas le décider s'il l'ignore.

## La devise fait partie de l'identité de cotation

La même société cotée en USD et en EUR n'a pas la même série de prix. Les
confondre produirait des rendements fantômes qui ne sont que du change.
"""
from __future__ import annotations

from dataclasses import dataclass, field


def normaliser_cik(cik) -> str:
    """Le CIK sur dix chiffres, comme la SEC le publie dans ses index.

    Elle écrit tantôt `320193`, tantôt `0000320193` : deux écritures du même
    émetteur produiraient deux séries distinctes, et la moitié des dépôts
    manquerait dans chacune.
    """
    if cik in (None, ""):
        return ""
    brut = str(cik).strip().upper().removeprefix("CIK")
    brut = brut.lstrip("-_ ").strip()
    if not brut.isdigit():
        return ""
    return brut.zfill(10)


@dataclass(frozen=True)
class Instrument:
    """L'identité d'un instrument, et ce qu'elle vaut."""

    conid: int | None = None
    cik: str = ""
    ticker: str = ""
    exchange: str = ""
    currency: str = "USD"
    figi: str = ""
    isin: str = ""
    #: Renseigné par l'appelant quand il connaît l'historique des noms — sert
    #: à expliquer une série, jamais à l'identifier.
    anciens_tickers: tuple = field(default_factory=tuple)

    def __post_init__(self):
        object.__setattr__(self, "cik", normaliser_cik(self.cik))
        object.__setattr__(self, "ticker", str(self.ticker or "").strip().upper())
        object.__setattr__(self, "exchange", str(self.exchange or "").strip().upper())
        object.__setattr__(self, "currency", str(self.currency or "").strip().upper())
        if not (self.conid or self.cik or self.ticker):
            raise ValueError(
                "instrument sans identifiant : ni conId, ni CIK, ni ticker — "
                "un enregistrement sans identité ne pourra jamais être relu "
                "ni relié à quoi que ce soit")

    @property
    def fragile(self) -> bool:
        """La clé repose-t-elle sur le seul ticker ?

        Ce n'est pas un défaut en soi — beaucoup d'instruments n'ont ni conId
        ni CIK. C'est une propriété que l'appelant doit pouvoir LIRE avant de
        bâtir une preuve historique dessus.
        """
        return not (self.conid or self.cik)

    def cle(self) -> str:
        """La clé canonique du registre. Stable dans le temps, par construction."""
        if self.conid:
            return "IB:%d" % int(self.conid)
        if self.cik:
            return "CIK:%s" % self.cik
        #  Le ticker seul ne suffit pas : place et devise entrent dans la clé,
        #  sinon SAP/NYSE/USD et SAP/XETRA/EUR partageraient une série.
        return "TICKER:%s.%s.%s" % (self.ticker, self.exchange or "?",
                                    self.currency or "?")

    def to_dict(self) -> dict:
        return {"conid": self.conid, "cik": self.cik, "ticker": self.ticker,
                "exchange": self.exchange, "currency": self.currency,
                "figi": self.figi, "isin": self.isin,
                "cle": self.cle(), "fragile": self.fragile}


__all__ = ["Instrument", "normaliser_cik"]
