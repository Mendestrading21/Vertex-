"""
vertex/engines/recommendation.py — LE SERVICE DE RECOMMANDATION UNIQUE.

Une seule façade pour TOUTE l'application (point 11 de la refonte) :
- position NEUVE  → enveloppe `decision_stack.evaluate` (le moteur canonique)
- position DÉTENUE → une SEULE fonction Python de gestion (remplace les 4
  conseillers JS divergents : manageJS / sAdvice / dkVerdict / …)
- un SEUL vocabulaire normalisé (label + tonalité), plus une table d'alias qui
  ramène tous les verdicts historiques (BUY, ACHETER FORT, ACCEPTÉ, RENFORCER,
  VERTEX S+, …) vers ce vocabulaire — le client le consomme via window.__VXVOCAB.

Analyse uniquement — aucune exécution.
"""

import json

from vertex.engines.decision_stack import DECISIONS  # vocab canonique "position neuve"

# ─── Vocabulaire "gestion de position détenue" ─────────────────────────────
HELD = {
    'ADD':         ('Renforcer', 'green'),
    'HOLD':        ('Conserver', 'blue'),
    'WATCH':       ('Surveiller', 'blue'),
    'RAISE_STOP':  ('Remonter le stop', 'amber'),
    'TRIM':        ('Alléger', 'amber'),
    'TAKE_PROFIT': ('Prendre profits', 'strong-green'),
    'EXIT':        ('Sortir', 'red'),
}

# ─── Tonalité → classe CSS pill (une seule table d'affichage) ──────────────
TONE_CLS = {
    'strong-green': 'p-good', 'green': 'p-good', 'blue': 'p-info',
    'amber': 'p-warn', 'red': 'p-bad', 'gray': 'p-mut',
}

# ─── Alias : tout verdict historique → (label, tonalité) normalisés ────────
# Ramène les 9 moteurs divergents à un affichage cohérent partout.
_ALIAS = {
    # config.verdict (EN)
    'BUY': 'green', 'WATCH': 'blue', 'WAIT': 'blue', 'AVOID': 'red',
    # engine.decide (FR)
    'ACHETER FORT': 'strong-green', 'ACHETER': 'green', 'SURVEILLER': 'blue',
    'ATTENDRE': 'blue', 'ÉVITER': 'red', 'EVITER': 'red',
    # ibkr.verdict
    'ACCEPTÉ': 'green', 'ACCEPTE': 'green', 'ACCEPTÉ SUR REPLI': 'blue',
    'ACCEPTE SUR REPLI': 'blue', 'ATTENTE': 'blue', 'REFUSÉ': 'red', 'REFUSE': 'red',
    # committee / vertex
    'RENFORCER': 'green', 'VERTEX BUY': 'green', 'VERTEX S+': 'strong-green',
    # gestion position (FR)
    'CONSERVER': 'blue', 'GARDER': 'blue', 'ALLÉGER': 'amber', 'ALLEGER': 'amber',
    'REMONTER LE STOP': 'amber', 'REMONTER STOP': 'amber', 'PRENDRE PROFITS': 'strong-green',
    'SÉCURISER': 'strong-green', 'SECURISER': 'strong-green', 'SORTIR': 'red', 'VENDRE': 'red',
}


def _labels_map():
    """Table complète {CLÉ_MAJ: {label, tone, cls}} : canoniques + gestion + alias."""
    out = {}
    for key, (label, tone) in DECISIONS.items():
        out[key] = {'label': label, 'tone': tone, 'cls': TONE_CLS.get(tone, 'p-mut')}
        out[label.upper()] = {'label': label, 'tone': tone, 'cls': TONE_CLS.get(tone, 'p-mut')}
    for key, (label, tone) in HELD.items():
        out[key] = {'label': label, 'tone': tone, 'cls': TONE_CLS.get(tone, 'p-mut')}
        out[label.upper()] = {'label': label, 'tone': tone, 'cls': TONE_CLS.get(tone, 'p-mut')}
    for raw, tone in _ALIAS.items():
        # label = forme jolie du canonique si connu, sinon Titre-case de l'alias
        out.setdefault(raw.upper(), {'label': raw.title(), 'tone': tone,
                                     'cls': TONE_CLS.get(tone, 'p-mut')})
    return out


def normalize(raw):
    """Verdict historique quelconque → {label, tone, cls}. '—' si vide/inconnu."""
    if raw is None or raw == '':
        return {'label': '—', 'tone': 'gray', 'cls': 'p-mut'}
    m = _labels_map().get(str(raw).strip().upper())
    return m or {'label': str(raw), 'tone': 'gray', 'cls': 'p-mut'}


def vocab_js():
    """Littéral JS de la table de vocabulaire — source unique injectée dans window.__VXVOCAB."""
    return json.dumps(_labels_map(), ensure_ascii=False)


def _num(x, d=None):
    try:
        if x is None or x == '':
            return d
        return float(x)
    except (TypeError, ValueError):
        return d


def position_decision(pos, underlying=None):
    """
    LA décision de gestion d'une position détenue (source unique).

    pos : {type('STK'/'CALL'/'PUT'), entry, stop, tp, current, pl_pct, dte}
    underlying : décision decision_stack du sous-jacent (dict) — optionnel.
    Retourne {verdict, label, tone, cls, reason, risk, action, confidence}.
    """
    pos = pos or {}
    is_opt = (pos.get('type') or 'STK') != 'STK'
    entry = _num(pos.get('entry'))
    stop = _num(pos.get('stop'))
    tp = _num(pos.get('tp'))
    cur = _num(pos.get('current'))
    pl = _num(pos.get('pl_pct'))
    dte = _num(pos.get('dte'))
    udec = (underlying or {}).get('final_decision')

    def out(key, reason, action, risk=None, conf=62):
        label, tone = HELD[key]
        return {'verdict': key, 'label': label, 'tone': tone,
                'cls': TONE_CLS.get(tone, 'p-mut'), 'reason': reason,
                'action': action, 'risk': risk, 'confidence': conf}

    # 1. Stop touché / perte lourde → discipline, on sort
    if stop is not None and cur is not None and cur <= stop:
        return out('EXIT', 'Le cours a atteint ou franchi le stop du plan.',
                   'Sortir maintenant — le scénario est invalidé.', 'perte au stop', 78)
    # Seuil de discipline aligné sur la constitution : action -20 % (stock_max_drawdown),
    # option -25 % (convexité tolère plus). Ne JAMAIS appliquer la limite portefeuille
    # (-25 %) à une action isolée — c'était une incohérence avec le hard gate -20 %.
    _dd_limit = -25 if is_opt else -20
    if pl is not None and pl <= _dd_limit:
        return out('EXIT', 'Perte au-delà du seuil de discipline (%d %%).' % _dd_limit,
                   'Couper la position, ne pas moyenner à la baisse.', 'perte non maîtrisée', 74)
    # 2. Option proche de l'expiration → le thêta commande
    if is_opt and dte is not None and dte <= 14:
        if pl is not None and pl > 0:
            return out('TAKE_PROFIT', 'Option à moins de 14 jours et en gain — le thêta va accélérer.',
                       'Prendre le profit avant l\'érosion temporelle.', 'thêta / expiration', 70)
        return out('EXIT', 'Option à moins de 14 jours sans marge — érosion thêta dominante.',
                   'Solder ou rouler avant l\'expiration.', 'thêta / expiration', 68)
    # 3. Objectif quasi atteint → sécuriser
    if tp is not None and cur is not None and cur > 0 and 0 <= (tp / cur - 1) * 100 <= 4:
        return out('TAKE_PROFIT', 'Le cours est à portée de l\'objectif du plan.',
                   'Sécuriser une partie, laisser courir le reste stop remonté.', 'proche cible', 71)
    # 4. Gros gain → alléger / protéger
    if pl is not None and pl >= 100:
        return out('TRIM', 'Gain supérieur à +100 % — l\'asymétrie s\'est inversée.',
                   'Alléger 25–50 % et remonter le stop sous le dernier support.', None, 69)
    if pl is not None and pl >= 40:
        return out('RAISE_STOP', 'Gain confortable (≥ +40 %) — protéger l\'acquis.',
                   'Remonter le stop au point mort ou sous le dernier plus-bas.', None, 66)
    # 5. Le sous-jacent se dégrade
    if udec in ('AVOID', 'NO_NEW_RISK'):
        return out('TRIM', 'Le moteur Vertex ne valide plus le sous-jacent.',
                   'Réduire l\'exposition, resserrer le stop.', 'signal dégradé', 60)
    if udec in ('STRONG_BUY', 'BUY') and (pl is None or pl >= 0):
        return out('ADD', 'Le plan reste valide et le moteur reste acheteur.',
                   'Renforcement possible sur repli, dans la limite du risque.', None, 63)
    # 6. Par défaut : on tient
    return out('HOLD', 'Le plan tient : cours au-dessus de l\'entrée, loin du stop.',
               'Conserver et surveiller le prochain niveau.', None, 60)


def options_for_position(sym, board, held_type='STK'):
    """
    « Options disponibles sur cette position » (point 6).

    Sélectionne, dans le board d'options, les meilleurs véhicules autour d'un
    sous-jacent détenu : meilleur CALL, meilleur PUT, LEAPS, covered call (revenu)
    et protective put (protection) — pour une position longue en actions.
    Retourne {sym, held_type, suggestions:[{role, role_label, sym, type, strike,
    exp, dte, premium, pop, score, grade, why}], note}.
    """
    sym = (sym or '').upper()
    rows = [c for c in (board or []) if (c.get('sym') or '').upper() == sym]

    def best(cands, key=lambda c: (c.get('quality') or 0)):
        cands = [c for c in cands if c.get('quality') is not None]
        return max(cands, key=key) if cands else None

    calls = [c for c in rows if c.get('type') == 'CALL']
    puts = [c for c in rows if c.get('type') == 'PUT']

    def pack(role, label, c, why):
        if not c:
            return None
        return {'role': role, 'role_label': label, 'sym': sym, 'type': c.get('type'),
                'strike': c.get('strike'), 'exp': (c.get('exp') or '')[:10], 'dte': c.get('dte'),
                'premium': c.get('mid'), 'pop': c.get('pop'), 'score': c.get('quality'),
                'grade': c.get('grade'), 'delta': c.get('delta'), 'why': why}

    sugg = []
    sugg.append(pack('CALL', 'Meilleur CALL', best(calls),
                     'Le contrat haussier le mieux noté du board sur ce titre.'))
    sugg.append(pack('PUT', 'Meilleur PUT / hedge', best(puts),
                     'Pari baissier ou couverture directionnelle sur le titre.'))
    leaps = best([c for c in rows if (c.get('dte') or 0) >= 300])
    sugg.append(pack('LEAPS', 'LEAPS (≥ 300 j)', leaps,
                     'Exposition longue durée — le temps pèse peu, quasi-action.'))
    if held_type == 'STK':
        cc = best([c for c in calls if 0.15 <= (c.get('delta') or 0) <= 0.40
                   and 20 <= (c.get('dte') or 0) <= 90])
        sugg.append(pack('COVERED_CALL', 'Covered call (revenu)', cc,
                         'Vendu contre tes actions : encaisse une prime, plafonne le gain.'))
        pp = best([c for c in puts if -0.45 <= (c.get('delta') or 0) <= -0.12
                   and 25 <= (c.get('dte') or 0) <= 180])
        sugg.append(pack('PROTECTIVE_PUT', 'Protective put (protection)', pp,
                         'Assurance sur ta position longue contre une chute du titre.'))

    sugg = [s for s in sugg if s]
    note = None if sugg else ('Aucun contrat chargé pour ' + sym
                              + ' — le board d\'options se remplit au scan.')
    return {'sym': sym, 'held_type': held_type, 'suggestions': sugg, 'note': note}


__all__ = ['DECISIONS', 'HELD', 'normalize', 'vocab_js', 'position_decision',
           'options_for_position', 'TONE_CLS']
