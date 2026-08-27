"""vertex/strategy/legacy_adapter.py — STRATÉGIE OPTIONS PERSONNALISÉE (échelle 1/2/3/6/9/12 mois).

Profil utilisateur (encodé d'après ses réponses) :
  • style       : croissance + équilibre, offensif maîtrisé
  • instrument  : ACHAT de Calls/Puts simples (directionnel)
  • delta       : MIX par échéance — agressif/OTM sur le court (pari rapide),
                  conservateur/ITM sur le long (LEAPS solides)
  • tailles     : 5 k (ultra-risque) · 15 k (risque contrôlé) · risque 5-10 %/trade
  • SPÉCULATION : ne garde PAS jusqu'à l'échéance → on valorise l'option EN COURS
                  DE ROUTE (mark-to-market Black-Scholes, temps restant), pas à
                  l'expiration. C'est le cœur de cette stratégie.
  • scénarios   : pessimiste / probable / exceptionnel + cible technique + ±1σ
  • direction   : Call ET Put, pondérés par le RÉGIME de marché
  • sorties     : objectif +50/+100 % · stop −50 % · cours cible · alerte théta

Tout est calculé en Black-Scholes depuis le cours + la volatilité → fonctionne
PARTOUT, même sans chaîne d'options réseau (donc visible en mode démo, iPhone).
⛔ ANALYSE ÉDUCATIVE — jamais un conseil financier, jamais un ordre.
"""
import math

#  `R` est LU dans le moteur, jamais recopie : une declaration qui porterait
#  sa propre copie du taux finirait par annoncer autre chose que ce qui a
#  ete calcule — c'est exactement le defaut de D-084.
from vertex.options.legacy_engine import R, _bs_price, _greeks

# ── Échelle d'échéances + delta cible MIX (court agressif → long conservateur) ─
HORIZONS = [
    {'key': 'm1',  'label': '1 mois',  'months': 1,  'dte': 30,  'delta': 0.45},
    {'key': 'm2',  'label': '2 mois',  'months': 2,  'dte': 60,  'delta': 0.48},
    {'key': 'm3',  'label': '3 mois',  'months': 3,  'dte': 90,  'delta': 0.52},
    {'key': 'm6',  'label': '6 mois',  'months': 6,  'dte': 180, 'delta': 0.58},
    {'key': 'm9',  'label': '9 mois',  'months': 9,  'dte': 270, 'delta': 0.65},
    {'key': 'm12', 'label': '12 mois', 'months': 12, 'dte': 365, 'delta': 0.70},
]

SIZING = [
    #  `ton` et non `color` : le rouge et l'orange d'ici etaient des hex EN DUR
    #  — `#EF4444` et `#FFB23F`, ce dernier appartenant a la palette
    #  Obsidian Copper abandonnee. Un moteur qui impose une couleur impose
    #  aussi une palette, et la page ne peut plus rester coherente.
    #
    #  La surface mappe `ton` -> jeton semantique : `risque` = corail,
    #  `prudence` = ambre. Meme sens, une seule source de couleur.
    {'key': 'ultra',    'label': '5 k ultra',     'budget': 5000,  'ton': 'risque'},
    {'key': 'controle', 'label': '15 k contrôlé', 'budget': 15000, 'ton': 'prudence'},
]
def horizons_annotes():
    """Les échéances, chacune disant si la constitution ACTIVE la recommande.

    ## Le défaut

    `HORIZONS` va de 30 à 365 jours. La constitution, elle, déclare une bande
    préférée et une cible — v4 : **120–240, cible 180**. Rien ne le disait à
    l'écran : un lecteur choisissait « 1 mois » (30 jours) sans savoir qu'il
    sortait de la doctrine que le reste du produit applique.

    Ce n'est pas un défaut de la table — offrir une échelle et en préférer un
    point sont deux choses. Le défaut était le **silence**.

    ## Pourquoi c'est dérivé et jamais recopié

    La bande est lue dans `release.etat_actif()` à chaque appel. Une copie
    ici finirait par annoncer autre chose que ce que les moteurs appliquent —
    c'est exactement le défaut de D-084, et la raison pour laquelle `R` est
    importé du moteur plus haut plutôt que redéclaré.

    Quand aucune constitution n'est active (entrée directe par `terminal.py`,
    mode de repli V3), `dans_la_bande` vaut `None` : **on ne sait pas**, et on
    le dit — jamais `False`, qui se lirait « déconseillé par la doctrine ».
    """
    try:
        from vertex.strategy import release
        etat = release.etat_actif() or {}
    except Exception as e:                       # profil illisible : on le NOMME
        etat = {'erreur': '%s: %s' % (type(e).__name__, str(e)[:80])}

    bande = etat.get('dte_prefere')
    cible = etat.get('dte_cible')
    bas, haut = (bande[0], bande[-1]) if (bande and len(bande) >= 2) else (None, None)

    out = []
    for h in HORIZONS:
        dte = h.get('dte')
        dans = None if bas is None else (bas <= dte <= haut)
        out.append({**h,
                    'dans_la_bande': dans,
                    'est_la_cible': (cible is not None and dte == cible),
                    'ecart_a_la_cible': (None if cible is None else dte - cible)})
    return {'horizons': out,
            'bande_preferee': bande,
            'dte_cible': cible,
            'constitution': etat.get('version'),
            'note': ('`dans_la_bande` a None quand aucune constitution n est '
                     'active : on ne sait pas, et un False se lirait '
                     '« deconseille par la doctrine »'),
            'erreur': etat.get('erreur')}


RISK_PCT = (5, 10)          # risque cible par trade (info)
IV_MAX = 0.85              # filtre « IV pas trop chère » (vol annualisée)

_BEAR = {'AVOID', 'ÉVITER', 'EVITER', 'SELL', 'VENDRE', 'REDUCE', 'ALLÉGER', 'ALLEGER'}


#: Ce que ce module PRODUIT, et qu'il doit dire.
#:
#: Chaque autre moteur de pricing du dépôt trace ses hypothèses —
#: `scenario_pricer` (`model_source`, `limitations`), `multileg_lab` et
#: `double_prob` (bloc `model`). Celui-ci n'en déclarait **aucune**, alors que
#: c'est le plus modélisé des quatre : ni la prime, ni l'IV, ni le strike ne
#: viennent d'une cotation. Le strike est CHOISI pour viser un delta, la prime
#: est CALCULÉE, et l'IV est DÉDUITE de l'ATR.
#:
#: Mesuré le 26 août 2026 sur les 578 contrats réellement cotés du board :
#: l'IV médiane par titre s'étale de **2,52×** entre p10 (0,248) et p90
#: (0,625). Sur cet intervalle, la prime d'un call ATM à 180 jours varie de
#: **+128 %**. Le proxy assigne pourtant l'IV depuis le seul ATR : deux titres
#: de même ATR reçoivent la même IV, quelle que soit celle que le marché cote.
#:
#: Et la sortie sert un DIMENSIONNEMENT EN DOLLARS sur cette prime — nombre de
#: contrats, coût, `maxloss`. Un chiffre modélisé qui prend la forme d'un
#: montant engagé doit dire qu'il est modélisé.
MODELE = {
    'type': 'black_scholes_europeen',
    'estimated': True,
    'prix_source': 'MODEL_ESTIMATE',
    #  Renseigne par titre : COTEE quand le board porte des contrats,
    #  PROXY_ATR sinon. Le bloc global dit la regle, chaque `pick` dit
    #  ce qui lui est REELLEMENT arrive.
    'iv_source': 'COTEE_SI_DISPONIBLE_SINON_PROXY_ATR',
    'strike_source': 'CHOISI_POUR_DELTA_CIBLE',
    'r': R,
    'q': 0.0,
    'read_only': True,
}

#: Limites de ce constructeur. Elles ne remplacent pas une cotation : elles
#: disent pourquoi il ne faut pas la confondre avec une.
LIMITATIONS = [
    "prime MODELISEE, jamais cotee : aucun contrat reel ne correspond "
    "necessairement a ce strike ni a cette echeance",
    "IV COTEE quand le board porte des contrats du titre ; sinon proxy ATR, "
    "et le pick le dit. Le proxy est mesurablement BIAISE : sur 30 titres "
    "reels (26 aout 2026, ATR de Wilder), il surevalue l'IV dans 30 cas sur "
    "30 — mediane +40 %, jusqu'a +78 % — car l'ATR mesure la volatilite "
    "REALISEE et une prime se paie sur l'IMPLICITE. Effet sur la prime d'un "
    "call ATM 180 j : +34,9 % de mediane, soit ~2 contrats de moins sur un "
    "budget de 15 k",
    "structure par terme non modelisee : une seule IV par titre sert tous les "
    "horizons, de 1 a 12 mois",
    "taux sans risque constant (%.3f), sans courbe par echeance" % R,
    "dividende non applique (q = 0) : sur un titre distributeur, la prime d'un "
    "call est SURESTIMEE",
    "modele europeen : l'exercice anticipe n'est pas modelise",
    "le dimensionnement en dollars decoule de la prime MODELISEE — le cout "
    "reel d'une position depend de la cotation du jour",
]


def _iv_du_titre(board, sym, atr_pct):
    """L'IV a employer pour ce titre, et d'ou elle vient.

    La cotation l'emporte des qu'elle existe : le proxy ATR est mesurablement
    biaise (30 titres sur 30 surevalues, mediane +40 %). Preferer une erreur
    connue a une cotation reelle serait un choix, et le mauvais.

    Rend `(sigma, source, n_contrats)` — `source` vaut `'COTEE'` ou
    `'PROXY_ATR'`, et le `pick` le porte, pour qu'un lecteur sache lequel des
    deux il regarde.
    """
    if board:
        from vertex.options.entrees_mesurees import iv_cotee
        q = iv_cotee(board, sym)
        if q['valeur'] is not None:
            return q['valeur'], 'COTEE', q['n_contrats']
    return _iv_proxy(atr_pct), 'PROXY_ATR', 0


def _iv_proxy(atr_pct):
    v = (atr_pct or 2.0) / 100.0 * math.sqrt(252)
    return max(0.22, min(1.10, v))


def _round_strike(S, k):
    step = 1 if S < 50 else 2.5 if S < 100 else 5 if S < 250 else 10
    return round(k / step) * step


# Lot 9b : mémo du solveur de strike (fonction PURE). Clés = args EXACTS → byte-identique ;
# hit quand prix/vol/échéance inchangés (hors séance), cassant la boucle ~90 itérations
# × 12 legs × 6 picks appelée à chaque scan. Borné (garde-fou mémoire).
_STRIKE_MEMO = {}


def _strike_for_delta(S, T, sig, is_call, target):
    key = (S, T, sig, is_call, target)
    if key in _STRIKE_MEMO:
        return _STRIKE_MEMO[key]
    best, bd = S, 9.9
    k = S * 0.55
    while k <= S * 1.45:
        delta, *_ = _greeks(S, k, T, sig, is_call)
        diff = abs(abs(delta) - target)
        if diff < bd:
            bd, best = diff, k
        k += S * 0.01
    if len(_STRIKE_MEMO) > 20000:
        _STRIKE_MEMO.clear()
    _STRIKE_MEMO[key] = best
    return best


def _hold_days(dte):
    """Durée de détention type (spéculation) : ~1/3 de l'échéance, bornée 5-45 j."""
    return int(max(5, min(round(dte * 0.34), 45)))


def _val(S_t, K, dte_rest_days, sig, is_call):
    """Valeur mark-to-market de l'option à un cours S_t, avec le temps RESTANT."""
    T = max(dte_rest_days / 365.0, 1.0 / 365.0)
    return _bs_price(S_t, K, T, sig, is_call)


def _bias(market):
    """Régime de marché → 'favorable' / 'neutral' / 'dangerous' (défensif)."""
    if isinstance(market, dict):
        blob = ' '.join(str(market.get(k, '')) for k in
                        ('regime', 'state', 'label', 'spy_regime', 'verdict', 'tone')).lower()
        if any(w in blob for w in ('favor', 'risk-on', 'risk on', 'haussier', 'bull', 'vert')):
            return 'favorable'
        if any(w in blob for w in ('danger', 'risk-off', 'risk off', 'baissier', 'bear', 'rouge', 'stress')):
            return 'dangerous'
        sc = market.get('score') or market.get('market_score')
        if isinstance(sc, (int, float)):
            return 'favorable' if sc >= 60 else 'dangerous' if sc < 40 else 'neutral'
    return 'neutral'


def _leg(S, sig, plan, is_call, h):
    T = h['dte'] / 365.0
    k = _round_strike(S, _strike_for_delta(S, T, sig, is_call, h['delta']))
    prem = _bs_price(S, k, T, sig, is_call)
    if prem <= 0:
        return None
    delta, gamma, theta, vega = _greeks(S, k, T, sig, is_call)
    be = (k + prem) if is_call else (k - prem)
    hold = _hold_days(h['dte'])
    rest = h['dte'] - hold                                 # temps restant à la revente
    em = S * sig * math.sqrt(hold / 365.0)                 # mouvement attendu sur la détention
    sgn = 1.0 if is_call else -1.0

    def scen(mult):
        st = max(S + sgn * mult * em, 0.01)
        val = _val(st, k, rest, sig, is_call)
        pct = round((val - prem) / prem * 100) if prem else 0
        return {'px': round(st, 2), 'val': round(val, 2), 'pct': pct}

    scenarios = {'pess': scen(-0.5), 'prob': scen(1.0), 'except': scen(2.0)}

    # cible TECHNIQUE (plan) valorisée en cours de route
    tp_px = (plan.get('tp2') if is_call else plan.get('stop'))
    tp_tech = None
    if tp_px:
        val = _val(tp_px, k, rest, sig, is_call)
        tp_tech = {'px': round(tp_px, 2), 'pct': round((val - prem) / prem * 100) if prem else 0}

    # gain à l'ÉCHÉANCE (intrinsèque) sur un mouvement +1σ plein horizon (repère)
    emT = S * sig * math.sqrt(T)
    tgtT = max(S + sgn * emT, 0.01)
    intrinsicT = max((tgtT - k) if is_call else (k - tgtT), 0.0)
    gain_exp = round((intrinsicT - prem) / prem * 100) if prem else 0

    sizes = []
    for s in SIZING:
        contracts = int(s['budget'] // (prem * 100)) if prem > 0 else 0
        cost = round(contracts * prem * 100)
        #  `ton` remplace `color` : le moteur ne dicte plus un hex. La
        #  surface mappe `risque` -> corail et `prudence` -> ambre, comme
        #  elle le fait deja pour les etats.
        sizes.append({'key': s['key'], 'label': s['label'], 'ton': s['ton'],
                      'budget': s['budget'], 'contracts': contracts, 'cost': cost,
                      'maxloss': cost,
                      'gain_prob': round(contracts * 100 * (scenarios['prob']['val'] - prem))})

    exit_rules = {
        'tp50': round(prem * 1.5, 2), 'tp100': round(prem * 2.0, 2),
        'stop50': round(prem * 0.5, 2),
        'theta_alert_dte': max(0, h['dte'] - 45),          # zone théta chaude
    }
    return {'key': h['key'], 'label': h['label'], 'dte': h['dte'], 'hold': hold,
            'strike': k, 'premium': round(prem, 2), 'breakeven': round(be, 2),
            'delta': round(abs(delta), 2), 'gamma': round(gamma, 4),
            'theta_day': round(theta, 3), 'vega': round(vega, 3),
            'scenarios': scenarios, 'tp_tech': tp_tech, 'gain_exp': gain_exp,
            'exit': exit_rules, 'sizes': sizes}


def _legs(S, sig, plan, is_call):
    return [leg for leg in (_leg(S, sig, plan, is_call, h) for h in HORIZONS) if leg]


# ── CONSTRUCTEUR DE PORTEFEUILLE (grosses sommes 50k/100k/200k) ───────────────
# Profil utilisateur : 8-12 positions · mix étalé · ~87 % déployé (10-15 % cash)
# CŒUR contrôlé (3-6-9 mois, delta haut, façon « action ») + SATELLITES offensifs
# (1-2 mois OTM, levier) · risque ≤ 10 %/position.
_CORE_HORIZONS = ['m3', 'm6', 'm9']
_SAT_HORIZONS = ['m1', 'm2', 'm3']
_DEPLOY = 0.87
_CORE_SHARE = 0.66
_MAX_POS_RISK = 0.10


def _candidates(rows, detail, bias, limit, board=None):
    out = []
    for r in (rows or []):
        sym = r.get('symbol')
        d = detail.get(sym) if detail else None
        if not d:
            continue
        S = d.get('price')
        if not S or S <= 0:
            continue
        sig, iv_src, n_ctr = _iv_du_titre(board, sym, d.get('atr_pct'))
        bullish = (d.get('verdict') or '').upper() not in _BEAR
        primary = 'PUT' if bias == 'dangerous' else ('CALL' if bullish else 'PUT')
        legs = {l['key']: l for l in _legs(S, sig, (d.get('plan') or {}), primary == 'CALL')}
        if not legs:
            continue
        out.append({'sym': sym, 'S': round(S, 2), 'grade': d.get('grade'),
                    'score': d.get('score'), 'dir': primary, 'legs': legs,
                    'iv_source': iv_src, 'iv_n_contrats': n_ctr})
        if len(out) >= limit:
            break
    return out


def build_portfolio(rows, detail, market=None, capital=100000, n_core=6, n_sat=4,
                    board=None):
    """Alloue un capital (50k/100k/200k…) en portefeuille d'options selon le profil."""
    bias = _bias(market)
    cand = _candidates(rows, detail, bias, n_core + n_sat, board=board)
    deploy = capital * _DEPLOY
    core_budget, sat_budget = deploy * _CORE_SHARE, deploy * (1 - _CORE_SHARE)
    positions = []

    def add(group, budget, horizons, role):
        if not group:
            return
        per = budget / len(group)
        for idx, c in enumerate(group):
            leg = c['legs'].get(horizons[idx % len(horizons)]) or next(iter(c['legs'].values()), None)
            if not leg:
                continue
            unit = leg['premium'] * 100
            if unit <= 0:
                continue
            contracts = int(per // unit)
            if contracts < 1 and unit <= capital * 0.12:
                contracts = 1
            while contracts > 1 and contracts * unit > capital * _MAX_POS_RISK:
                contracts -= 1
            if contracts < 1:
                continue
            cost = round(contracts * unit)
            sc = leg['scenarios']
            positions.append({
                'sym': c['sym'], 'role': role, 'dir': c['dir'], 'grade': c['grade'],
                'horizon': leg['label'], 'dte': leg['dte'], 'strike': leg['strike'],
                'premium': leg['premium'], 'delta': leg['delta'], 'contracts': contracts,
                'cost': cost, 'maxloss': cost,
                'gain_prob': round(contracts * 100 * (sc['prob']['val'] - leg['premium'])),
                'gain_exc': round(contracts * 100 * (sc['except']['val'] - leg['premium'])),
                'prob_pct': sc['prob']['pct'], 'exc_pct': sc['except']['pct'],
                #  Cette ligne porte un COUT et un `maxloss` en dollars : elle
                #  doit dire si sa prime vient d'une cotation ou d'un proxy.
                'iv_source': c.get('iv_source'), 'iv_n_contrats': c.get('iv_n_contrats')})

    add(cand[:n_core], core_budget, _CORE_HORIZONS, 'CŒUR')
    add(cand[n_core:n_core + n_sat], sat_budget, _SAT_HORIZONS, 'SATELLITE')
    deployed = sum(p['cost'] for p in positions)
    gp = sum(p['gain_prob'] for p in positions)
    ge = sum(p['gain_exc'] for p in positions)
    return {'model': dict(MODELE), 'limitations': list(LIMITATIONS),
            'capital': capital, 'deployed': deployed, 'cash': round(capital - deployed),
            'positions': positions, 'n': len(positions), 'maxloss': deployed,
            'gain_prob': gp, 'gain_exc': ge,
            'gain_prob_pct': round(gp / capital * 100, 1) if capital else 0,
            'gain_exc_pct': round(ge / capital * 100, 1) if capital else 0,
            'regime': bias}


def build(rows, detail, market=None, top_n=6, board=None):
    """Stratégie pour les meilleures convictions. Call ET Put, pondérés régime."""
    bias = _bias(market)
    picks = []
    for r in (rows or [])[:top_n]:
        sym = r.get('symbol')
        d = detail.get(sym) if detail else None
        if not d:
            continue
        S = d.get('price')
        if not S or S <= 0:
            continue
        sig, iv_src, n_ctr = _iv_du_titre(board, sym, d.get('atr_pct'))
        iv_expensive = sig > IV_MAX
        verdict = (d.get('verdict') or '').upper()
        bullish = verdict not in _BEAR
        # direction privilégiée = croisement conviction × régime
        if bias == 'dangerous':
            primary = 'PUT'
        elif bias == 'favorable':
            primary = 'CALL' if bullish else 'PUT'
        else:
            primary = 'CALL' if bullish else 'PUT'
        plan = d.get('plan') or {}
        picks.append({
            'symbol': sym, 'price': round(S, 2), 'grade': d.get('grade'),
            'score': d.get('score'), 'iv': round(sig * 100),
            #  `iv` porte le MEME nom que l'IV COTEE du board, et n'a pas le
            #  meme sens : celle-ci est deduite de l'ATR. Le dire ici, au plus
            #  pres de la valeur, est la seule facon qu'un lecteur ne les
            #  confonde pas.
            'iv_source': iv_src, 'iv_estimated': iv_src == 'PROXY_ATR',
            'iv_n_contrats': n_ctr,
            'iv_expensive': iv_expensive, 'regime': bias, 'primary': primary,
            'call': _legs(S, sig, plan, True),
            'put': _legs(S, sig, plan, False),
        })
    _h = horizons_annotes()
    return {'picks': picks, 'horizons': _h['horizons'],
            'doctrine_echeances': {k: _h[k] for k in
                                   ('bande_preferee', 'dte_cible',
                                    'constitution', 'note', 'erreur')},
            'sizing': SIZING,
            'regime': bias, 'risk_pct': list(RISK_PCT),
            'model': dict(MODELE), 'limitations': list(LIMITATIONS),
            'profile': {'style': 'Croissance + équilibre (spéculation, sortie avant échéance)',
                        'instrument': 'Achat Calls / Puts directionnels',
                        'delta': 'Delta MIX : agressif court · conservateur long',
                        'sizing': '5 k ultra-risque · 15 k contrôlé · 5-10 %/trade'}}
