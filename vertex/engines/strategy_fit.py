"""
vertex/engines/strategy_fit.py — COUCHE STRATÉGIE (présentation, Ch. II).

Re-pondère l'analyse déjà calculée selon le profil « offensif croissance » :
choix du véhicule (ACTION vs OPTION), score stratégie, playbook, et tilt du
climat de marché. NE TOUCHE JAMAIS les moteurs quant : lit uniquement des champs déjà
présents sur les lignes (rows). Pur, sans état, sans dépendance externe.

Extrait verbatim du monolithe. Analyse uniquement, aucune exécution.
"""


def _vehicle_of(r, best):
    v = r.get('verdict')
    score = r.get('score') or 0
    if v == 'AVOID':
        return {'reco': '—', 'tone': 'mut', 'why': "signal trop faible — ni action ni option aujourd'hui"}
    if not best:
        return {'reco': 'ACTION', 'tone': 'blue',
                'why': "aucune option propre (illiquide / hors séance) — jouer le titre en action"}
    q = best.get('quality') or 0
    pop = best.get('pop') or 0
    iv = best.get('iv') or 0
    pot = best.get('pot') or 0
    if q < 45 or pop < 35:
        return {'reco': 'ACTION', 'tone': 'blue',
                'why': "option de faible qualité / liquidité — l'action est plus sûre"}
    o = 0
    o += 1 if q >= 70 else 0
    o += 1 if pop >= 50 else 0
    o += 1 if pot >= 100 else 0            # forte asymétrie (gain option ≥ +100% si cible)
    o += 1 if score >= 72 else 0           # conviction élevée
    o += 1 if 0 < iv <= 45 else 0          # IV pas chère → l'option paie
    o -= 2 if iv >= 62 else 0              # IV chère → surpayer la prime, préférer l'action
    o -= 1 if score < 62 else 0            # conviction moyenne
    if o >= 3:
        return {'reco': 'OPTION', 'tone': 'orange', 'opt': {'strike': best.get('strike'),
                'exp': best.get('exp'), 'q': q, 'pop': pop, 'pot': pot},
                'why': "levier + risque défini : qualité %d, POP %d%%, gain visé +%d%%" % (q, pop, pot)}
    if o <= 0:
        why = ("IV chère (%d%%) — l'action évite de surpayer la prime" % round(iv)) if iv >= 62 \
            else "conviction / liquidité moyenne — l'action est plus souple (ni théta ni échéance)"
        return {'reco': 'ACTION', 'tone': 'blue', 'why': why}
    return {'reco': 'AU CHOIX', 'tone': 'gold',
            'why': "les deux jouables — option pour le levier, action pour tenir sans échéance"}


def _attach_vehicle(rows, board):
    """Attache r['vehicle'] à chaque titre (meilleur CALL du board comme référence)."""
    best = {}
    for c in (board or []):
        if c.get('type') != 'CALL':
            continue
        s = c.get('sym')
        if s and (s not in best or (c.get('quality') or 0) > (best[s].get('quality') or 0)):
            best[s] = c
    for r in rows or []:
        r['vehicle'] = _vehicle_of(r, best.get(r.get('symbol')))


# ─── COUCHE STRATÉGIE (présentation) : re-pondère l'analyse selon le profil de l'utilisateur ──
# Profil : OFFENSIF CROISSANCE — action socle + CALL comme levier · R:R ≥ 2:1 · tendance propre.
# ⛔ Ne touche jamais les moteurs quant : lit uniquement les champs déjà calculés (st_*, rs, regime, plan…).
def _strat_score(r):
    """Score /100 ré-pondéré vers l'offensif croissance (momentum/force/tendance surpondérés)."""
    score = r.get('score') or 0
    def g(v, d): return v if isinstance(v, (int, float)) else d
    mom = g(r.get('st_mom'), score); tech = g(r.get('st_tech'), score)
    fund = g(r.get('st_fund'), 50); risk = g(r.get('st_risk'), 50); rs = g(r.get('rs'), 50)
    regime = r.get('regime'); pos52 = r.get('pos52'); ext = r.get('ext_atr'); rsi = r.get('rsi')
    s = (0.30 * mom + 0.16 * tech + 0.10 * fund + 0.10 * risk
         + 0.22 * max(0, min(100, rs))
         + 0.12 * (100 if regime == 'TREND' else 45 if regime == 'NEUTRAL' else 12))
    if regime == 'CHOP':
        s -= 12
    if pos52 is not None and pos52 >= 80 and regime == 'TREND':
        s += 5
    if ext is not None and abs(ext) >= 3:
        s -= 8
    if rsi is not None and rsi >= 78:
        s -= 5
    if r.get('vx_notrade'):
        s -= 10
    return int(max(0, min(100, round(s))))


# playbooks = mêmes règles que la page Stratégie, priorisés pour l'offensif (momentum/levier d'abord)
_PLAYBOOKS_PY = [
    ('🚀', 'Momentum Breakout', '#22C55E', 'Acheter la force qui casse ses plus-hauts.',
     lambda r: r.get('regime') == 'TREND' and (r.get('rs') or 0) >= 70 and (r.get('pos52') or 0) >= 80),
    ('⚡', 'Levier LEAPS', '#FF7A18', 'CALL long terme sur forte conviction — levier, perte max = la prime.',
     lambda r: (r.get('vx_edge') or 0) >= 60 and r.get('regime') == 'TREND'),
    ('🎯', 'Repli sur tendance', '#38BDF8', 'Entrer sur un creux dans une tendance saine — meilleur R:R.',
     lambda r: r.get('regime') == 'TREND' and 40 <= (r.get('rsi') or 0) <= 58 and (r.get('pos52') or 0) >= 40),
    ('💎', 'Qualité forte', '#A78BFA', 'Meilleurs scores validés ACHAT — le socle du portefeuille.',
     lambda r: (r.get('score') or 0) >= 72 and r.get('verdict') == 'BUY'),
    ('🔄', 'Retournement de bas', '#FFB23F', 'Rebond depuis le bas du range — à CONFIRMER.',
     lambda r: (r.get('pos52') or 0) <= 25 and (r.get('change') or 0) > 0),
    ('🛡️', 'Socle défensif', '#34D399', 'Titres solides peu volatils — amortir les chocs.',
     lambda r: (r.get('score') or 0) >= 58 and (abs(r['ext_atr']) if r.get('ext_atr') is not None else 2) <= 1 and r.get('regime') != 'CHOP'),
]


def _playbook_of(r):
    for ic, name, col, desc, f in _PLAYBOOKS_PY:
        try:
            if f(r):
                return {'ic': ic, 'name': name, 'col': col, 'desc': desc}
        except Exception:
            pass
    return None


def _attach_strategy(rows, detail):
    """Attache par titre : strat_score (profil offensif), playbook, R:R et rr_ok (≥ 2:1)."""
    for r in rows or []:
        r['strat_score'] = _strat_score(r)
        r['playbook'] = _playbook_of(r)
        sym = r.get('symbol')
        plan = ((detail or {}).get(sym) or {}).get('plan') or {}
        rr = plan.get('rr_res')
        if rr is None:
            rr = r.get('vx_rr')
        r['rr'] = rr
        r['rr_ok'] = bool(rr is not None and rr >= 2)


def _strat_tilt(mctx):
    """Oriente l'analyse selon le climat : quels playbooks pousser + taille de levier CALL."""
    if not mctx:
        return None
    br = mctx.get('breadth') or {}
    reg = mctx.get('spy_regime'); roro = mctx.get('roro'); vb = mctx.get('vix_band')
    s = 35 if reg == 'TREND' else 18 if reg == 'NEUTRAL' else 6 if reg == 'CHOP' else 14
    s += 25 if roro == 'RISK-ON' else 2 if roro == 'RISK-OFF' else 12
    a50 = br.get('above50')
    s += round((a50 if a50 is not None else 50) / 100 * 25)
    s += 15 if vb == 'calme' else 2 if vb == 'stress' else 8
    s = int(max(0, min(100, round(s))))
    if s >= 65:
        return {'score': s, 'regime': 'FAVORABLE', 'col': '#22C55E', 'call_size': 'normale → agressive',
                'emphasis': ['Momentum Breakout', 'Levier LEAPS', 'Repli sur tendance'],
                'note': "Marché porteur : ton profil offensif est dans son élément. Privilégie le momentum et le levier CALL long (LEAPS)."}
    if s >= 40:
        return {'score': s, 'regime': 'NEUTRE', 'col': '#FFB23F', 'call_size': 'réduite (½ taille)',
                'emphasis': ['Repli sur tendance', 'Qualité forte'],
                'note': "Marché mitigé : sois sélectif. Repli sur tendance + qualité forte ; CALL en taille réduite et échéances plus longues."}
    return {'score': s, 'regime': 'DANGEREUX', 'col': '#EF4444', 'call_size': 'minime / cash',
            'emphasis': ['Socle défensif', 'Qualité forte'],
            'note': "Marché dangereux : défense. Réduis le levier CALL, garde du cash, socle défensif seulement. Discipline > FOMO."}


__all__ = ['vehicle_of', 'attach_vehicle', 'strat_score', 'playbook_of', 'attach_strategy', 'strat_tilt']

# Alias publics (API du module) vers les fonctions extraites verbatim.
vehicle_of = _vehicle_of
attach_vehicle = _attach_vehicle
strat_score = _strat_score
playbook_of = _playbook_of
attach_strategy = _attach_strategy
strat_tilt = _strat_tilt
