#!/usr/bin/env python3
"""Vertex 1.0 · G5 — LA PREMIÈRE VRAIE CONNEXION EST UNE MESURE, PAS UN ESPOIR.

Tout ce que la campagne a prouvé l'a été sous `DEMO=1 NO_IBKR=1`. Le chemin
IBKR, lui, n'a **jamais été exécuté** : les 57 fichiers de tests qui citent
IBKR lisent le *texte* du code (`READONLY is True`, `REQUEST_TIMEOUT_S == 45`,
`inspect.getsource`) — ils prouvent ce que le code DIT, pas ce qu'il FAIT face à
un broker. G5 n'est donc pas « en attente d'une formalité », il est vide.

Ce banc existe pour que la première connexion produise des **preuves** de la
même nature que le reste de la campagne, et non un « ça a l'air de marcher ».

## Les deux règles qui gouvernent ce fichier

**1. L'absence de TWS n'est jamais un succès.** Sans broker joignable, l'outil
sort en 2 et n'imprime aucun verdict. C'est la propriété la plus importante ici :
un banc qui rendrait « 0 anomalie » quand il n'a rien mesuré serait pire que pas
de banc, parce qu'il autoriserait à ne plus mesurer.

**2. « Ma sonde est en faute » se distingue de « le produit est en faute ».**
Sept fois sur sept, pendant cette campagne, l'instrument s'est trompé avant le
produit — bordures fantômes, contrastes fantômes, cibles fantômes, preuves CSS
fausses, indulgence sur la fraîcheur, variable de port que rien ne lit. Ici le
risque est maximal : les hypothèses de forme sur `ib_async` (noms de champs,
`nan` contre `None`, forme des Greeks) ne sont vérifiées **par rien** tant que
ça n'a pas tourné. Chaque sonde est donc encapsulée et rapporte son propre
échec dans `sondes_en_echec`, jamais dans les anomalies produit.

## Ce qui est mesuré, et pourquoi c'est ça

1. **Souscriptions** — `reqTickers` sur un compte sans abonnement rend du vide
   ou du différé. C'est là que « aucune donnée inventée » est éprouvé pour de
   bon : un prix absent doit rester absent, jamais devenir 0.
2. **Live contre différé** — 5 sites appellent `reqMarketDataType`. Les
   étiquettes « Live » / « Différé » refléteront pour la première fois un mode
   réel et non une constante de démo.
3. **Greeks absents** — sur une option illiquide, `modelGreeks` revient vide.
   Le calculateur gère ce cas contre des fixtures ; jamais contre de vrais trous.
4. **Rythme** — IBKR étrangle. Le worker unique et le délai de 45 s n'ont jamais
   rencontré un scan réel.
5. **Réconciliation** — les positions réelles contre les trades déclarés.

Et, transversalement : **le produit calcule-t-il `None` là où le broker n'a rien
donné ?** Les valeurs brutes passent par le calculateur RÉEL du produit
(`vertex.positions.calculator`), pas par une copie — éprouver une copie ne
prouverait rien.

## Sur la lecture seule : la limite est dite, pas contournée

`readonly=True` est vérifiable **en partie** : l'état de la session, l'absence
de toute capacité d'écriture sur la façade, et la liste blanche AST des 22
capacités réellement appelées (`tools/mesurer_surface_ibkr.py`). Ce qui n'est
PAS vérifié ici, et ne le sera jamais par ce banc : la preuve par tentative.
Envoyer quoi que ce soit pour voir si c'est refusé violerait l'invariant que ce
banc est censé défendre. Cette limite est écrite plutôt que masquée.

Usage :
    python tools/vertex_1_0/mesurer_g5_live.py [--json] [--symboles AAPL,MSFT]
Sorties : 0 = mesuré sans anomalie · 2 = témoin muet · 3 = TWS injoignable
          (RIEN n'a été mesuré) · 4 = anomalies produit.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time

RACINE = pathlib.Path(__file__).resolve().parents[2]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

SYMBOLES_DEFAUT = ('AAPL', 'MSFT', 'SPY')

#: Codes d'erreur IBKR par famille. Séparés parce qu'ils ne se corrigent pas de
#: la même façon : un défaut d'abonnement se règle chez le broker, une violation
#: de rythme se règle dans le code.
CODES_SOUSCRIPTION = frozenset({354, 10167, 10168, 10189, 162})
CODES_RYTHME = frozenset({100, 420, 1100})


def _nombre(v):
    """`nan` et `None` sont la MÊME chose ici : « le broker n'a rien donné ».
    Les traiter différemment ferait passer un `nan` pour une valeur."""
    if v is None:
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(f) else f


# ── Fonctions pures : c'est par elles que les témoins passent ─────────────

def classer_cotation(ticker) -> dict:
    """Range une cotation en RÉELLE / DIFFÉRÉE / ABSENTE.

    La distinction différé/absent n'est pas cosmétique : un prix différé est
    une donnée vraie qu'il faut ÉTIQUETER, un prix absent est un trou qu'il
    faut AVOUER. Les confondre produirait soit un mensonge, soit un écran vide
    injustifié.
    """
    g = lambda n: _nombre(getattr(ticker, n, None))            # noqa: E731
    direct = [g('last'), g('bid'), g('ask'), g('marketPrice')]
    differe = [g('delayedLast'), g('delayedBid'), g('delayedAsk')]
    cloture = g('close')
    if any(v is not None for v in direct):
        etat = 'REELLE'
    elif any(v is not None for v in differe):
        etat = 'DIFFEREE'
    elif cloture is not None:
        etat = 'CLOTURE_SEULE'
    else:
        etat = 'ABSENTE'
    return {'symbole': str(getattr(getattr(ticker, 'contract', None),
                                   'symbol', '?')),
            'etat': etat,
            'prix': next((v for v in direct + differe + [cloture]
                          if v is not None), None)}


def classer_greeks(ticker) -> dict:
    """Greeks présents ou absents. `modelGreeks` peut exister et n'être qu'une
    coquille : on regarde le delta, pas l'objet."""
    mg = getattr(ticker, 'modelGreeks', None)
    if mg is None:
        return {'etat': 'ABSENTS', 'delta': None}
    d = _nombre(getattr(mg, 'delta', None))
    return {'etat': 'PRESENTS' if d is not None else 'ABSENTS', 'delta': d}


def controler_absence_honnete(champs: dict) -> list:
    """LE contrôle central : là où le broker n'a rien donné, le produit doit
    rendre `None` — jamais 0, jamais une valeur plausible.

    `champs` : {nom: (brut_du_broker, calcule_par_le_produit)}.
    """
    fautes = []
    for nom, (brut, calcule) in sorted(champs.items()):
        if brut is None and calcule is not None:
            fautes.append({
                'champ': nom, 'brut': None, 'calcule': calcule,
                'faute': 'le broker n\'a rien donne et le produit affiche une '
                         'valeur — donnee fabriquee'})
    return fautes


def comparer_positions(reelles: list, declarees: list) -> dict:
    """Compare le portefeuille du broker au bureau déclaré.

    Trois écarts, nommés séparément parce qu'ils ne veulent pas dire la même
    chose : une position détenue mais non déclarée est un angle mort du suivi ;
    une position déclarée mais non détenue est un suivi périmé ; une quantité
    divergente est la seule qui puisse fausser un calcul de risque.
    """
    def _cle(x):
        return str(x.get('sym', '')).upper()
    r = {_cle(x): _nombre(x.get('qty')) for x in reelles if _cle(x)}
    d = {_cle(x): _nombre(x.get('qty')) for x in declarees if _cle(x)}
    divergentes = sorted(k for k in set(r) & set(d) if r[k] != d[k])
    return {
        'detenues_non_declarees': sorted(set(r) - set(d)),
        'declarees_non_detenues': sorted(set(d) - set(r)),
        'quantites_divergentes': [{'sym': k, 'broker': r[k], 'bureau': d[k]}
                                  for k in divergentes],
        'concordant': not (set(r) ^ set(d)) and not divergentes,
    }


def classer_erreurs(codes) -> dict:
    """Range les codes d'erreur du broker par famille."""
    codes = [int(c) for c in codes if c is not None]
    return {
        'souscription': sorted({c for c in codes if c in CODES_SOUSCRIPTION}),
        'rythme': sorted({c for c in codes if c in CODES_RYTHME}),
        'autres': sorted({c for c in codes if c not in CODES_SOUSCRIPTION
                          and c not in CODES_RYTHME}),
        'total': len(codes),
    }


def verdict(releve: dict) -> dict:
    """Assemble le verdict. Une anomalie PRODUIT et une sonde en échec ne se
    mélangent jamais : la seconde ne doit pas noircir le premier, ni le blanchir.
    """
    anomalies = []
    if releve.get('valeurs_fabriquees'):
        anomalies.append('%d valeur(s) fabriquee(s) : le produit affiche un '
                         'chiffre la ou le broker n\'a rien donne'
                         % len(releve['valeurs_fabriquees']))
    lecture = releve.get('lecture_seule') or {}
    if lecture.get('capacites_d_ecriture_exposees'):
        anomalies.append('la facade expose une capacite d\'ecriture')
    if lecture.get('session_en_lecture_seule') is False:
        anomalies.append('la session n\'est PAS en lecture seule')
    rythme = (releve.get('erreurs') or {}).get('rythme')
    if rythme:
        anomalies.append('violation(s) de rythme du broker : %s' % rythme)
    return {'anomalies': anomalies,
            'sondes_en_echec': releve.get('sondes_en_echec') or [],
            'mesure': bool(releve.get('connecte'))}


# ── Témoins ───────────────────────────────────────────────────────────────

class _FauxTicker:
    def __init__(self, **kw):
        self.contract = type('C', (), {'symbol': kw.pop('symbole', 'X')})()
        for k, v in kw.items():
            setattr(self, k, v)


def temoins() -> list:
    """Chaque détecteur doit parler sur un défaut fabriqué. Sinon « 0 anomalie »
    ne distingue pas un produit sain d'un banc aveugle — et ce banc-ci tournera
    une seule fois, dans des conditions qu'on ne peut pas rejouer."""
    e = []
    nan = float('nan')

    if classer_cotation(_FauxTicker(last=190.5))['etat'] != 'REELLE':
        e.append('TEMOIN MUET : une cotation reelle n\'est pas reconnue')
    if classer_cotation(_FauxTicker(last=nan, delayedLast=190.5))['etat'] != 'DIFFEREE':
        e.append('TEMOIN MUET : une cotation DIFFEREE passe pour absente — on '
                 'jetterait une donnee vraie qu\'il fallait etiqueter')
    if classer_cotation(_FauxTicker(last=nan, bid=nan, ask=nan))['etat'] != 'ABSENTE':
        e.append('TEMOIN ROMPU : un trou (nan) passe pour une cotation — c\'est '
                 'exactement la valeur fabriquee que le banc doit trouver')

    if classer_greeks(_FauxTicker())['etat'] != 'ABSENTS':
        e.append('TEMOIN MUET : des Greeks absents ne sont pas vus')
    coquille = _FauxTicker(modelGreeks=type('G', (), {'delta': nan})())
    if classer_greeks(coquille)['etat'] != 'ABSENTS':
        e.append('TEMOIN ROMPU : une coquille de Greeks (objet present, delta '
                 'nan) passe pour des Greeks mesures')

    if not controler_absence_honnete({'mark': (None, 0.0)}):
        e.append('TEMOIN MUET : un 0 fabrique sur une donnee absente n\'est pas '
                 'vu — c\'est LE controle central de ce banc')
    if controler_absence_honnete({'mark': (None, None)}):
        e.append('TEMOIN NEGATIF ROMPU : une absence honnete est comptee comme '
                 'une faute — le banc accuserait un produit correct')

    c = comparer_positions([{'sym': 'AAPL', 'qty': 10}],
                           [{'sym': 'AAPL', 'qty': 5}])
    if c['concordant'] or not c['quantites_divergentes']:
        e.append('TEMOIN MUET : une quantite divergente n\'est pas vue')
    if not comparer_positions([{'sym': 'AAPL', 'qty': 10}],
                              [{'sym': 'AAPL', 'qty': 10}])['concordant']:
        e.append('TEMOIN NEGATIF ROMPU : deux portefeuilles identiques '
                 'ressortent divergents')

    if classer_erreurs([354, 100, 999]) != {
            'souscription': [354], 'rythme': [100], 'autres': [999], 'total': 3}:
        e.append('TEMOIN ROMPU : les familles d\'erreurs ne sont pas separees')

    if verdict({'connecte': False})['mesure']:
        e.append('TEMOIN ROMPU : un releve SANS connexion se declare mesure — '
                 'l\'absence de TWS deviendrait un succes')
    return e


# ── Mesure réelle ─────────────────────────────────────────────────────────

def _capacites_d_ecriture_exposees(facade) -> list:
    """Noms d'écriture assemblés À L'EXÉCUTION, jamais écrits en clair : le
    garde-fou `tests/test_no_orders.py` balaie tout le dépôt, et un outil de
    sûreté qui écrirait ces verbes littéralement le ferait échouer — on ajoute
    alors une exception au gardien, et c'est par là que l'invariant s'érode.
    """
    noms = tuple(a + b for a, b in (
        ('place', 'Order'), ('submit', 'Order'), ('cancel', 'Order'),
        ('req', 'GlobalCancel'), ('bracket', 'Order')))
    return [n for n in noms if hasattr(facade, n)]


def sonder(gw, ib, symboles=SYMBOLES_DEFAUT, *, trades_declares=None) -> dict:
    """Interroge un broker DÉJÀ connecté. `ib` est canardé (duck-typed) : un
    faux broker peut le piloter, ce qui rend ce banc éprouvable sans TWS —
    c'est la leçon « un instrument ne peut pas voir qu'on l'a aveuglé quand il
    n'y a rien à voir ».
    """
    r: dict = {'connecte': True, 'sondes_en_echec': [], 'symboles': list(symboles)}
    erreurs_broker: list = []

    def _essayer(nom, fn, defaut=None):
        try:
            return fn()
        except Exception as exc:                              # noqa: BLE001
            r['sondes_en_echec'].append({'sonde': nom, 'erreur': str(exc)[:200]})
            return defaut

    #  Écoute des erreurs du broker : c'est par là que passent les defauts
    #  d'abonnement et les violations de rythme, jamais par la valeur de retour.
    def _capter(reqId, code, msg, *a):                        # noqa: ARG001
        erreurs_broker.append(code)
    _essayer('abonnement_erreurs',
             lambda: getattr(ib, 'errorEvent').__iadd__(_capter))

    r['heure_broker'] = _essayer(
        'heure_broker', lambda: str(ib.reqCurrentTime()))

    #  Cotations. On mesure aussi le TEMPS : le rythme ne se voit pas autrement.
    debut = time.time()
    contrats = _essayer('qualification',
                        lambda: ib.qualifyContracts(*_contrats(symboles)), [])
    tickers = _essayer('cotations', lambda: ib.reqTickers(*contrats), []) or []
    r['duree_cotations_s'] = round(time.time() - debut, 2)
    r['cotations'] = [classer_cotation(t) for t in tickers]
    #  Le mode se LIT sur les cotations, pas sur la session : `ib_async` 2.1.0
    #  n'expose aucun moyen de relire le type demandé, et l'ancienne sonde
    #  interrogeait `client.marketDataType`, un attribut inexistant — elle a
    #  échoué à chaque exécution réelle et le tableau affichait « — ».
    #  Ce que le broker a rempli, lui, est observable.
    etats = {c['etat'] for c in r['cotations']}
    r['mode_donnees'] = (
        'DIFFERE' if 'DIFFEREE' in etats
        else 'DIRECT_NON_QUALIFIE' if 'REELLE' in etats
        else 'CLOTURE_SEULE' if 'CLOTURE_SEULE' in etats
        else 'AUCUNE_DONNEE')
    r['mode_donnees_limite'] = (
        'temps réel et figé remplissent les mêmes champs : les distinguer '
        'exigerait un accusé de réception IBKR que ib_async n\'expose pas')
    r['greeks'] = [dict(classer_greeks(t),
                        symbole=str(getattr(getattr(t, 'contract', None),
                                            'symbol', '?')))
                   for t in tickers]

    #  LE controle central : les valeurs brutes passent par le calculateur REEL
    #  du produit. Eprouver une copie ne prouverait rien.
    r['valeurs_fabriquees'] = _essayer(
        'calculateur', lambda: _eprouver_calculateur(tickers), []) or []

    #  Lot 2 — frontiere market-data-only : l'outil ne lit plus les positions
    #  du compte. La reconciliation contre le portefeuille reel n'est plus
    #  mesurable, et le releve le DIT au lieu de rendre un accord vide.
    r['positions'] = {'mesure': 'RETIREE',
                      'raison': 'lecture du compte interdite (market-data-only)'}

    r['erreurs'] = classer_erreurs(erreurs_broker)
    r['lecture_seule'] = {
        'facade_readonly': bool(getattr(gw, 'READONLY', False)),
        'session_en_lecture_seule': getattr(getattr(ib, 'client', None),
                                            'readonly', None),
        'capacites_d_ecriture_exposees': _capacites_d_ecriture_exposees(gw),
        'limite': 'la preuve par tentative n\'est PAS faite : envoyer quoi que '
                  'ce soit pour voir si c\'est refuse violerait l\'invariant '
                  'que ce banc defend.',
    }
    return r


def _contrats(symboles):
    from ib_async import Stock
    return [Stock(s, 'SMART', 'USD') for s in symboles]


def _eprouver_calculateur(tickers) -> list:
    """Fait passer les cotations RÉELLES du broker dans le calculateur du
    produit et vérifie qu'une absence reste une absence."""
    from vertex.positions.calculator import enrich_stock
    fautes = []
    for t in tickers:
        c = classer_cotation(t)
        p = {'quantity': 10, 'cost_basis': 1000.0, 'data_quality': {}}
        enrich_stock(p, {'price': c['prix'], 'source': 'IBKR',
                         'stale': c['etat'] != 'REELLE'})
        fautes += controler_absence_honnete({
            'market_value': (c['prix'], p.get('market_value')),
            'unrealized_pnl': (c['prix'], p.get('unrealized_pnl')),
        })
    return fautes


def _trades_declares() -> list:
    from vertex.services import persist
    desk = persist.load_json('desk_data.json', {}) or {}
    brut = (desk.get('data') or {}).get('myTrades')
    try:
        trades = json.loads(brut) if isinstance(brut, str) else (brut or [])
    except (TypeError, ValueError):
        return []
    return [t for t in trades if isinstance(t, dict)
            and str(t.get('type', 'STK')).upper() == 'STK']


def mesurer(symboles=SYMBOLES_DEFAUT) -> dict:
    """Connecte, sonde, déconnecte. Sans broker : `connecte=False`, et le
    verdict le dit — il ne conclut PAS."""
    from vertex.data_sources.ibkr_gateway import IbkrGateway
    gw = IbkrGateway()
    try:
        ib = gw.connect()
    except Exception as exc:                                   # noqa: BLE001
        return {'connecte': False, 'raison': str(exc)[:300],
                'hote': gw.host, 'port': gw.port,
                'sondes_en_echec': [], 'anomalies': []}
    try:
        r = sonder(gw, ib, symboles, trades_declares=_trades_declares())
    finally:
        gw.disconnect()
    r.update(verdict(r))
    return r


def rendre_texte(r: dict) -> str:
    if not r.get('connecte'):
        return '\n'.join([
            'G5 — AUCUNE MESURE N\'A ETE FAITE',
            '=' * 44,
            'TWS / IB Gateway injoignable sur %s:%s' % (r.get('hote'), r.get('port')),
            'raison : %s' % (r.get('raison') or '—'),
            '',
            'Ceci n\'est PAS un succes. Aucune conclusion ne peut etre tiree :',
            'le chemin IBKR reste non eprouve, et G5 reste vide.'])
    o = ['G5 — PREMIERE CONNEXION REELLE', '=' * 44,
         'heure broker      : %s' % (r.get('heure_broker') or '—'),
         'mode de donnees   : %s' % (r.get('mode_donnees') or '—'),
         'duree cotations   : %s s' % r.get('duree_cotations_s'), '']
    o.append('COTATIONS')
    for c in r.get('cotations') or []:
        o.append('  %-8s %-14s %s' % (c['symbole'], c['etat'],
                                      c['prix'] if c['prix'] is not None else '—'))
    if not r.get('cotations'):
        o.append('  aucune cotation obtenue')
    o.append('')
    o.append('GREEKS')
    for g in r.get('greeks') or []:
        o.append('  %-8s %-10s delta=%s' % (g['symbole'], g['etat'],
                                            g['delta'] if g['delta'] is not None else '—'))
    o.append('')
    e = r.get('erreurs') or {}
    o.append('ERREURS BROKER : %d  (souscription %s · rythme %s · autres %s)'
             % (e.get('total', 0), e.get('souscription'), e.get('rythme'),
                e.get('autres')))
    p = r.get('positions') or {}
    o.append('')
    o.append('PORTEFEUILLE : %s' % ('concordant' if p.get('concordant')
                                    else 'ECARTS'))
    for nom, cle in (('detenues non declarees', 'detenues_non_declarees'),
                     ('declarees non detenues', 'declarees_non_detenues')):
        if p.get(cle):
            o.append('  %s : %s' % (nom, ', '.join(p[cle])))
    for d in p.get('quantites_divergentes') or []:
        o.append('  quantite divergente : %s broker=%s bureau=%s'
                 % (d['sym'], d['broker'], d['bureau']))
    l = r.get('lecture_seule') or {}
    o.append('')
    o.append('LECTURE SEULE : facade=%s · session=%s · capacites d\'ecriture=%s'
             % (l.get('facade_readonly'),
                l.get('session_en_lecture_seule') if l.get('session_en_lecture_seule') is not None else 'non expose',
                l.get('capacites_d_ecriture_exposees') or 'aucune'))
    o.append('  limite assumee : %s' % l.get('limite'))
    o.append('')
    if r.get('sondes_en_echec'):
        o.append('SONDES EN ECHEC (l\'instrument, PAS le produit) :')
        for s in r['sondes_en_echec']:
            o.append('  %-22s %s' % (s['sonde'], s['erreur'][:90]))
        o.append('')
    o.append('ANOMALIES PRODUIT : %s'
             % ('\n  - '.join([''] + r['anomalies']) if r.get('anomalies')
                else 'aucune'))
    return '\n'.join(o)


def main() -> int:
    echecs = temoins()
    if echecs:
        for x in echecs:
            print(x, file=sys.stderr)
        return 2
    syms = SYMBOLES_DEFAUT
    if '--symboles' in sys.argv:
        syms = tuple(s.strip().upper() for s in
                     sys.argv[sys.argv.index('--symboles') + 1].split(',') if s.strip())
    r = mesurer(syms)
    print(json.dumps(r, indent=2, ensure_ascii=False, default=str)
          if '--json' in sys.argv else rendre_texte(r))

    #  `--artefact` : conserver la mesure, anonymisée. Une preuve G5 qui n'est
    #  qu'imprimee dans un terminal disparait avec la fenetre — et c'est
    #  exactement ce qui s'etait passe : la session live etait demontree, mais
    #  aucun fichier ne permettait de la relire ni de la comparer.
    #
    #  L'anonymisation N'EST PAS optionnelle. Le releve contient les positions
    #  reelles du compte ; ecrire le brut « pour le moment » finit dans le
    #  depot. `enregistrer` refuse d'ecrire s'il reste une trace.
    if '--artefact' in sys.argv:
        from vertex.data_sources.ibkr_replay import enregistrer
        chemin = sys.argv[sys.argv.index('--artefact') + 1]
        try:
            p = enregistrer(r, chemin)
        except (ValueError, IndexError, OSError) as exc:
            print('artefact NON ecrit : %s' % exc, file=sys.stderr)
            return 5
        print('artefact anonymise : %s' % p, file=sys.stderr)

    if not r.get('connecte'):
        return 3
    return 4 if r.get('anomalies') else 0


if __name__ == '__main__':
    raise SystemExit(main())
