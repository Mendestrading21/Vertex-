"""vertex.data_sources.ibkr_historical — barres historiques IBKR (lecture seule)."""
from __future__ import annotations

import threading

from .models import SOURCE_IBKR, MODE_EOD, ProvenancedValue
from .provenance import stamp
from vertex.data_sources import ibkr_gateway


def bars_to_provenanced(bars: list[dict], timestamp: str = '') -> ProvenancedValue:
    """bars: [{'date','open','high','low','close','volume'}…] — validées basiquement."""
    cleaned, warnings = [], []
    for b in bars or []:
        o, h, l, c = b.get('open'), b.get('high'), b.get('low'), b.get('close')
        if None in (o, h, l, c):
            warnings.append(f"barre incomplète ignorée ({b.get('date')})")
            continue
        cleaned.append({'date': b.get('date'), 'open': float(o), 'high': float(h),
                        'low': float(l), 'close': float(c),
                        'volume': b.get('volume')})
    pv = stamp(value=cleaned or None, source=SOURCE_IBKR, source_mode=MODE_EOD,
               timestamp=timestamp)
    pv.warnings.extend(warnings)
    return pv


def fetch_daily_bars(gateway, symbol: str, duration: str = '1 Y') -> ProvenancedValue:
    Stock = ibkr_gateway.classe('Stock')
    ib = gateway.connect()
    contract = Stock(symbol, 'SMART', 'USD')
    ib.qualifyContracts(contract)
    raw = ib.reqHistoricalData(contract, endDateTime='', durationStr=duration,
                               barSizeSetting='1 day', whatToShow='TRADES',
                               useRTH=True, formatDate=1)
    bars = [{'date': str(b.date), 'open': b.open, 'high': b.high,
             'low': b.low, 'close': b.close, 'volume': b.volume} for b in raw]
    return bars_to_provenanced(bars)

#: Symboles dont la forme yfinance (`BRK-B`) n'est pas la forme IBKR (`BRK B`).
#: La conversion est mécanique ; elle est ici pour n'exister qu'une fois.
#: Le rôle « historique » n'a QU'UN identifiant client, et IBKR n'accepte
#: qu'une session par identifiant. Deux boucles du produit appellent ce module
#: — le scan de l'univers et la série longue du comparateur — et rien ne les
#: empêchait de partir ensemble : la seconde se voyait refuser la connexion, et
#: l'échec remontait en « TWS injoignable », c'est-à-dire en accusation contre
#: le courtier pour une collision née ici. Le verrou dit la vérité de la
#: ressource : une session à la fois.
_VERROU_SESSION = threading.Lock()


def _forme_ibkr(symbole: str) -> str:
    return symbole.replace('-', ' ').strip().upper()


#: Formes qui ne peuvent PAS etre une action americaine chez IBKR. Ce sont des
#: conventions yfinance : `^TNX` (indice), `GC=F` (future), `BTC-USD` (paire
#: crypto), `DX-Y.NYB` (indice avec suffixe de place).
#:
#: Mesure du 25 aout 2026, journal du courtier : ces symboles arrivaient bien
#: ici — le scan telecharge l'historique des indices et matieres premieres par
#: le MEME chemin que les actions — et `_contrat` tentait TROIS qualifications
#: d'action pour chacun, a chaque scan. Trois allers-retours perdus par symbole
#: et par cycle, plus trois erreurs 200 qui noient les vraies dans le journal.
#:
#: Verifie avant d'ecrire ce filtre : sur les 517 symboles de l'univers, ZERO
#: commence par `^`, finit par `=F` ou `-USD`, ou contient un point. Les deux
#: seuls a porter un tiret sont `BRK-B` et `BF-B`, des actions de classe B que
#: `_forme_ibkr` traite deja. Le filtre n'ecarte donc aucun titre reel.
_NON_ACTIONS = ('^', '=F', '-USD', '.')


def est_action_us(symbole: str) -> bool:
    """Ce symbole PEUT-il etre une action americaine ? (forme seule)

    Repondre `False` n'affirme pas que le titre n'existe pas — seulement qu'il
    ne peut pas etre qualifie comme action US, donc qu'il est inutile de le
    demander. L'appelant ira au repli, qui connait ces conventions.
    """
    s = str(symbole or '').strip().upper()
    if not s:
        return False
    if s.startswith('^') or '.' in s:
        return False
    return not (s.endswith('=F') or s.endswith('-USD'))


def _contrat(ib, symbole: str):
    """Le contrat action pour ce symbole, ou None si IBKR n'en connaît aucun.

    Deux essais, et le second n'est pas décoratif : `SMART` seul échoue sur des
    titres dont le nom est ambigu entre places (mesuré sur AVB — erreur 200,
    « aucune définition de titre »). Préciser la place primaire lève
    l'ambiguïté sans rien supposer du titre.
    """
    Stock = ibkr_gateway.classe('Stock')
    nom = _forme_ibkr(symbole)
    for essai in (Stock(nom, 'SMART', 'USD'),
                  Stock(nom, 'SMART', 'USD', primaryExchange='NYSE'),
                  Stock(nom, 'SMART', 'USD', primaryExchange='NASDAQ')):
        try:
            ib.qualifyContracts(essai)
            if getattr(essai, 'conId', 0):
                return essai
        except Exception:  # noqa: BLE001
            continue
    return None


def fetch_universe_bars(symboles, duration: str = '1 Y', *, gateway=None,
                        journal=None):
    """Barres quotidiennes IBKR pour TOUT l'univers → ``{symbole: DataFrame}``.

    La forme rendue est celle que le scan attend déjà de yfinance (index de
    dates, colonnes Open/High/Low/Close/Volume) : c'est ce qui permet de mettre
    IBKR en TÊTE de la chaîne existante sans réécrire le scan.

    ## Pourquoi un lot, et pas 515 appels à `fetch_daily_bars`

    Une seule session, un seul carnet de contrats. Mesuré sur cette machine :
    70 requêtes d'affilée en 31 s (0,45 s/symbole), **zéro violation de
    pacing** — donc l'univers complet en ~4 min. Rouvrir une session par
    symbole coûterait davantage que les barres elles-mêmes.

    ## Ce qu'elle ne fait pas

    Elle ne remplit aucun trou. Un symbole qu'IBKR ne connaît pas, ou qui ne
    rend aucune barre, est **absent** du dictionnaire : l'appelant le verra
    manquant et ira le chercher au repli. Rendre une trame vide le ferait
    passer pour servi, et le titre disparaîtrait du scan sans que rien ne le
    signale.
    """
    symboles = [str(x) for x in (symboles or [])]
    if not symboles:
        return {}, {'servis': 0, 'inconnus': [], 'vides': [], 'non_actions': []}

    #  Ce qui ne peut PAS etre une action US n'est pas demande au courtier.
    #  Nomme, jamais retire en silence : l'appelant doit pouvoir constater que
    #  ces symboles partent au repli, et non qu'ils ont echoue.
    non_actions = [s for s in symboles if not est_action_us(s)]
    symboles = [s for s in symboles if est_action_us(s)]
    if not symboles:
        return {}, {'servis': 0, 'inconnus': [], 'vides': [],
                    'non_actions': non_actions}

    import pandas as pd
    #  `notre` : on ne ferme QUE ce qu'on a ouvert. Une passerelle fournie par
    #  l'appelant lui appartient — la refermer couperait la session sous les
    #  pieds du chemin qui nous l'a prêtée.
    notre = gateway is None
    if notre:
        from .ibkr_gateway import IbkrGateway
        from . import ibkr_link
        gateway = IbkrGateway(client_id=ibkr_link.client_id('historique'))

    frames, inconnus, vides, refus = {}, [], [], {}
    fermeture = None
    verrou = _VERROU_SESSION if notre else None
    if verrou:
        verrou.acquire()
    try:
        ib = gateway.connect()                  # lève si TWS est absent
        frames, inconnus, vides, refus = _boucle(
            ib, symboles, duration, pd, journal)
    finally:
        #  FERMER, sinon le scan suivant se heurte à son propre identifiant.
        #  Mesuré : la session precedente restait ouverte sur clientId 23, TWS
        #  refusait la seconde, et l'echec remontait en « TWS injoignable » —
        #  un message qui accuse le courtier alors que la fuite etait ici.
        if notre:
            try:
                gateway._ib.disconnect() if gateway._ib else None
            except Exception as exc:  # noqa: BLE001
                #  Meme une fermeture qui echoue se DIT. Avalee, elle laisserait
                #  croire la session rendue alors qu'elle peut encore tenir
                #  l'identifiant — et le prochain scan echouerait sur un « TWS
                #  injoignable » dont la cause serait ici, invisible.
                fermeture = '%s: %s' % (type(exc).__name__, exc)
        if verrou:
            verrou.release()
    return frames, {'servis': len(frames), 'inconnus': inconnus,
                    'vides': vides, 'refus': refus, 'fermeture': fermeture,
                    #  Ecartes AVANT la moindre requete, par leur forme. Les
                    #  compter parmi les 'inconnus' ferait croire qu'IBKR les a
                    #  refuses, alors qu'on ne les lui a jamais demandes.
                    'non_actions': non_actions}


def _boucle(ib, symboles, duration, pd, journal):
    frames, inconnus, vides, refus = {}, [], [], {}
    for sym in symboles:
        contrat = _contrat(ib, sym)
        if contrat is None:
            inconnus.append(sym)
            continue
        try:
            brut = ib.reqHistoricalData(
                contrat, endDateTime='', durationStr=duration,
                barSizeSetting='1 day', whatToShow='TRADES',
                useRTH=True, formatDate=1)
        except Exception as exc:  # noqa: BLE001
            #  La RAISON, pas seulement le rang. Classe en « vide » sans dire
            #  pourquoi, une erreur de programmation (mesure vecue : un
            #  NameError sur `duration`) se lisait « ce titre n'a pas de
            #  donnees » — un defaut du code deguise en defaut du marche.
            refus[sym] = '%s: %s' % (type(exc).__name__, exc)
            vides.append(sym)
            continue
        if not brut:
            vides.append(sym)
            continue
        df = pd.DataFrame(
            [{'Open': b.open, 'High': b.high, 'Low': b.low,
              'Close': b.close, 'Volume': b.volume} for b in brut],
            index=pd.to_datetime([str(b.date) for b in brut]))
        if df.dropna().empty:
            vides.append(sym)
            continue
        frames[sym] = df
        if journal:
            journal(sym, len(df))
    return frames, inconnus, vides, refus
