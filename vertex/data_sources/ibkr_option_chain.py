"""vertex.data_sources.ibkr_option_chain — chaînes d'options IBKR (lecture seule).

Greeks : quand IBKR fournit ses modelGreeks, ils sont étiquetés BROKER_GREEKS
et PRÉFÉRÉS à tout modèle maison (§6.8). La chaîne complète n'est jamais tirée
pour tout l'univers : le chargement suit l'entonnoir §14 (expirations →
strikes filtrés → finalistes).
"""
from __future__ import annotations

from .models import SOURCE_IBKR, MODE_DELAYED, GREEKS_BROKER, ProvenancedValue
from .provenance import stamp


#: Annulations d'abonnement qui ont echoue. Une ligne de marche laissee
#: ouverte est une ressource perdue ; l'avaler en silence ferait
#: disparaitre la fuite jusqu'a ce que le compte sature.
_ECHECS_FERMETURE: list = []


def contract_row(*, symbol: str, expiry: str, strike: float, right: str,
                 bid=None, ask=None, last=None, volume=None, open_interest=None,
                 iv=None, delta=None, gamma=None, theta=None, vega=None,
                 multiplier='100', currency='USD', underlying=None,
                 greeks_source: str = GREEKS_BROKER, timestamp: str = '') -> dict:
    """Ligne de contrat normalisée — TOUT contrat manipulé par les moteurs a cette forme."""
    mid = None
    if bid is not None and ask is not None and float(ask) > 0:
        mid = (float(bid) + float(ask)) / 2
    return {
        'symbol': symbol.upper(), 'underlying': (underlying or symbol).upper(),
        'expiry': expiry, 'strike': float(strike), 'right': right.upper()[:1],
        'bid': bid, 'ask': ask, 'mid': mid, 'last': last,
        'volume': volume, 'open_interest': open_interest,
        'iv': iv, 'delta': delta, 'gamma': gamma, 'theta': theta, 'vega': vega,
        'greeks_source': greeks_source,
        'multiplier': multiplier, 'currency': currency,
        'timestamp': timestamp,
    }


def chain_to_provenanced(rows: list[dict], timestamp: str = '') -> ProvenancedValue:
    return stamp(value=list(rows or []), source=SOURCE_IBKR,
                 source_mode=MODE_DELAYED, timestamp=timestamp)


def fetch_expirations(gateway, symbol: str) -> list[str]:
    """Étape 1 de l'entonnoir : seulement les expirations (pas les chaînes)."""
    from ib_async import Stock
    ib = gateway.connect()
    stock = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(stock)
    params = ib.reqSecDefOptParams(stock.symbol, '', stock.secType, stock.conId)
    expirations: set[str] = set()
    for p in params:
        expirations.update(p.expirations)
    return sorted(expirations)


#: Ticks generiques demandes pour une chaine : 100 = volume d'options,
#: 101 = OPEN INTEREST, 106 = volatilite implicite du modele. Sans le 101,
#: `Ticker.callOpenInterest` reste `NaN` — et c'est la raison pour laquelle
#: `open_interest` etait code en dur a `None` dans cet adaptateur, case
#: « NON COUVERT » du protocole G5.
TICKS_CHAINE = '100,101,106'

#: Delai d'arrivee des Greeks et de l'OI. Mesure du board en production :
#: « greeks + OI arrivent en ~2 s ». On garde la meme marge que le chemin
#: deja eprouve plutot que d'en inventer une plus courte.
ATTENTE_TICKS_S = 2.6


def _oi(ticker, right: str):
    """L'open interest du BON cote, ou `None`.

    IBKR expose `callOpenInterest` et `putOpenInterest` separement : lire le
    mauvais donnerait a un call l'interet ouvert des puts. Absence rendue par
    `NaN` (et parfois `-1`, sentinelle du courtier) — jamais convertie en 0 :
    « aucune donnee » et « aucun contrat ouvert » sont deux verdicts opposes
    quand on juge la liquidite d'une option.
    """
    brut = getattr(ticker, 'callOpenInterest' if right.upper().startswith('C')
                   else 'putOpenInterest', None)
    if brut is None or brut != brut or brut < 0:
        return None
    return int(brut)


def fetch_contract_details(gateway, symbol: str, expiry: str,
                           strikes: list[float], right: str = 'C') -> ProvenancedValue:
    """Étape finale de l'entonnoir : détails complets pour une poignée de finalistes.

    ## L'open interest, case « NON COUVERT » du protocole G5

    Cet adaptateur rendait `open_interest=None` **en dur**. La cause n'était
    pas IBKR : `reqTickers` ne demande simplement pas le tick générique 101,
    donc l'information n'arrivait jamais. Le board de production, lui,
    l'obtient depuis toujours par `reqMktData(genericTickList='100,101,106')`.

    `QUALITY_STANDARD` §3 exige l'OI pour une option candidate, et le mandat
    options en fait un critère de liquidité. Une valeur toujours absente rendait
    ce critère inapplicable sans que rien ne le dise.

    ## Ce qui est fermé, et pourquoi

    Un abonnement laissé ouvert consomme une ligne de marché — ressource bornée
    et partagée avec le reste du produit. L'annulation est dans un `finally` :
    une exception au milieu de la lecture ne doit pas laisser N lignes ouvertes.
    """
    from ib_async import Option
    ib = gateway.connect()
    contracts = [Option(symbol, expiry, k, right, 'SMART', currency='USD')
                 for k in strikes]
    contracts = [c for c in ib.qualifyContracts(*contracts) if c.conId]
    if not contracts:
        return chain_to_provenanced([])
    tickers, ouverts = [], []
    try:
        for c in contracts:
            tickers.append(ib.reqMktData(c, genericTickList=TICKS_CHAINE,
                                         snapshot=False))
            ouverts.append(c)
        ib.sleep(ATTENTE_TICKS_S)
        rows = []
        for c, t in zip(contracts, tickers):
            mg = getattr(t, 'modelGreeks', None)
            rows.append(contract_row(
                symbol=symbol, expiry=expiry, strike=c.strike, right=right,
                bid=t.bid if t.bid and t.bid > 0 else None,
                ask=t.ask if t.ask and t.ask > 0 else None,
                last=t.last if t.last == t.last else None,
                volume=int(t.volume) if t.volume and t.volume == t.volume else None,
                open_interest=_oi(t, right),
                iv=getattr(mg, 'impliedVol', None) if mg else None,
                delta=getattr(mg, 'delta', None) if mg else None,
                gamma=getattr(mg, 'gamma', None) if mg else None,
                theta=getattr(mg, 'theta', None) if mg else None,
                vega=getattr(mg, 'vega', None) if mg else None,
                greeks_source=GREEKS_BROKER if mg else 'MODEL_ESTIMATE',
                timestamp=t.time.isoformat() if t.time else ''))
    finally:
        for c in ouverts:
            try:
                ib.cancelMktData(c)
            except Exception:                                 # noqa: BLE001
                #  Une annulation qui echoue ne doit pas emporter la lecture
                #  reussie des autres lignes — mais elle n'est pas silencieuse
                #  pour autant : le compteur la rend visible.
                _ECHECS_FERMETURE.append((symbol, expiry, getattr(c, 'strike', None)))
    return chain_to_provenanced(rows)
