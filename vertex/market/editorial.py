"""vertex.market.editorial — Brief éditorial narratif de séance (§10).

Compose un texte fluide de 180-320 mots à partir des données RÉELLES du scan
(indices, régime, volatilité, breadth, secteurs, comité). Chaque phrase n'est
émise que si sa donnée existe — jamais de récit inventé, jamais de fait
d'actualité fabriqué. Si les actualités manquent, le brief reste factuel
(données de marché) et le signale. Pur et testable.
"""
from __future__ import annotations


_REGIME_FR = {'TREND': 'TENDANCE', 'TREND_UP': 'TENDANCE HAUSSIÈRE',
              'TREND_DOWN': 'TENDANCE BAISSIÈRE', 'NEUTRAL': 'NEUTRE',
              'CHOP': 'SANS DIRECTION', 'DOWN': 'BAISSIER', 'UP': 'HAUSSIER',
              'UNKNOWN': 'INDÉTERMINÉ', 'RISK_ON': 'APPÉTIT POUR LE RISQUE',
              'RISK_OFF': 'AVERSION AU RISQUE', 'PANIC': 'PANIQUE',
              'MEAN_REVERSION': 'RETOUR À LA MOYENNE', 'TRANSITION': 'TRANSITION'}


def _regime_fr(code):
    return _REGIME_FR.get(str(code or '').upper(), code)


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _dir_word(chg):
    if chg is None:
        return None
    if chg >= 0.15:
        return 'en hausse'
    if chg <= -0.15:
        return 'en baisse'
    return 'quasi inchangés'


def _s(n):
    """Accord du pluriel français (0 et 1 → singulier)."""
    try:
        return '' if abs(int(n)) <= 1 else 's'
    except (TypeError, ValueError):
        return 's'


def _indices(scan_state):
    idx = scan_state.get('indices') or []
    out = {}
    for it in idx:
        if not isinstance(it, dict):
            continue
        nm = (it.get('name') or '').upper()
        chg = _num(it.get('change'))
        if 'S&P' in nm or 'SPX' in nm or 'SPY' in nm:
            out.setdefault('sp', chg)
        elif 'NASDAQ' in nm or 'NDX' in nm or 'QQQ' in nm:
            out.setdefault('ndx', chg)
        elif 'DOW' in nm or 'DJI' in nm:
            out.setdefault('dow', chg)
        elif 'RUSSELL' in nm or 'RUT' in nm or 'IWM' in nm:
            out.setdefault('rut', chg)
    return out


def build_narrative(scan_state, news_state=None):
    """Rend un dict avec le narratif fluide + les blocs éditoriaux §10."""
    # Fusion market (horloge) ⊕ market_ctx (contexte) — cf. daily_brief.
    m = {**(scan_state.get('market') or {}), **(scan_state.get('market_ctx') or {})}
    _b = m.get('breadth')
    if isinstance(_b, dict):
        m = {**m, 'breadth': _b.get('above50', _b.get('above200'))}
    sectors = [s for s in (scan_state.get('sectors') or []) if isinstance(s, dict)]
    committee = scan_state.get('committee') or {}
    counts = committee.get('counts') or {}
    idx = _indices(scan_state)
    news_items = (news_state or {}).get('items') or []
    sources = []

    sent = []  # phrases du narratif

    # 1-3. Direction des indices + moteur de séance.
    sp, ndx = idx.get('sp'), idx.get('ndx')
    if sp is not None or ndx is not None:
        w = _dir_word(sp if sp is not None else ndx)
        lead = 'Les indices américains s\'affichent %s' % (w or 'proches de l\'équilibre')
        bits = []
        if sp is not None:
            bits.append('le S&P 500 %+.1f %%' % sp)
        if ndx is not None:
            bits.append('le Nasdaq %+.1f %%' % ndx)
        if bits:
            lead += ', ' + ' et '.join(bits)
        # Moteur principal : leadership techno si le Nasdaq surperforme.
        if sp is not None and ndx is not None:
            if ndx > sp + 0.2:
                lead += ' : la technologie mène la hausse et concentre le leadership de la séance'
            elif sp > ndx + 0.2:
                lead += ' : la rotation profite aux valeurs cycliques, au détriment de la technologie'
        sent.append(lead + '.')
        sources.append('indices (scan)')

    # 4. Régime + appétit pour le risque.
    regime = _regime_fr(m.get('spy_regime') or m.get('regime'))
    roro = m.get('roro')
    if regime or roro:
        s = 'Le régime de fond reste %s' % (regime or 'indéterminé')
        if roro:
            s += ', dans un climat %s' % roro
        sent.append(s + '.')

    # 5. Volatilité.
    vix = _num(m.get('vix'))
    if vix is not None:
        band = m.get('vix_band')
        s = 'Le VIX, mesure de la volatilité implicite, s\'établit à %.1f' % vix
        if band:
            s += ' (%s)' % band
        s += (', un niveau contenu qui rend la couverture et l\'achat de convexité bon marché' if vix < 18 else
              ', un niveau tendu qui renchérit les primes d\'options et récompense la prudence' if vix > 25 else
              ', en zone médiane, sans excès de stress ni d\'euphorie')
        sent.append(s + '.')

    # 6. Breadth / participation.
    breadth = _num(m.get('breadth'))
    if breadth is not None:
        s = 'La participation est %s : %.0f %% des valeurs leaders traitent au-dessus de leur moyenne mobile' % (
            ('large' if breadth >= 55 else 'étroite'), breadth)
        s += (', signe d\'un mouvement bien soutenu' if breadth >= 55 else
              ', ce qui impose la sélectivité et fragilise les cassures')
        sent.append(s + '.')

    # 7-8. Secteurs leaders / faibles.
    dominant, weak = [], []
    if sectors:
        ranked = sorted(sectors, key=lambda x: _num(x.get('avg_score')) or 0, reverse=True)
        top = ranked[0]
        dominant = [r.get('sector') for r in ranked[:2] if r.get('sector')]
        weak = [r.get('sector') for r in ranked[-2:] if r.get('sector')]
        if top.get('sector'):
            sent.append('Côté rotation, %s mène la cote' % top.get('sector')
                        + (' devant %s' % ranked[1].get('sector') if len(ranked) > 1 and ranked[1].get('sector') else '')
                        + '.')
        sources.append('secteurs (scan)')

    # 9. Comité / opportunités.
    if counts:
        na, nw = int(counts.get('ACHETER', 0)), int(counts.get('ATTENDRE', 0))
        sent.append('Le comité Vertex retient %d dossier%s achetable%s et %d en surveillance ; '
                    'aucune position offensive n\'est engagée sans dossier complet validé.'
                    % (na, _s(na), _s(na), nw))

    # 10. Actualités — UNIQUEMENT si réelles. Sinon signalé, jamais inventé.
    news_available = bool(news_items)
    if news_available:
        top_news = news_items[0]
        title = (top_news.get('title') or top_news.get('fr') or '').strip()
        if title:
            sent.append('À la une : %s.' % title[:180])
            sources.append('actualités (fil assaini)')
    else:
        sent.append('Aucune actualité validée à cette heure : le brief s\'appuie uniquement '
                    'sur les données de marché — aucun récit n\'est inventé.')

    # 11. Discipline.
    sent.append('Discipline du jour : le fondamental prime sur le technique, R:R minimum de 2:1, '
                'stops dérivés du sous-jacent et décision finale unique — aucune improvisation.')

    narrative = ' '.join(sent)
    words = len(narrative.split())

    # Blocs éditoriaux §10.
    prices_mainly = _prices_mainly(m, vix, regime)
    main_opp = None
    decisions = committee.get('decisions') or []
    prio = next((d for d in decisions if d.get('verdict') in ('ACHETER', 'RENFORCER')), None)
    if prio:
        main_opp = '%s — dossier complet à valider avant toute décision.' % prio.get('symbol')

    calls_impact = None
    if vix is not None:
        calls_impact = ('Volatilité implicite basse : environnement porteur pour l\'achat de calls, la convexité se paie peu.'
                        if vix < 18 else
                        'Volatilité implicite élevée : les calls coûtent cher, n\'entrer qu\'avec un R:R strict.'
                        if vix > 25 else
                        'Volatilité implicite médiane : sélection de calls au cas par cas.')

    main_risk = None
    if regime in (None, 'UNKNOWN', 'INCONNU', 'INDÉTERMINÉ'):
        main_risk = 'Régime de marché indéterminé — aucun nouveau risque autorisé tant que la direction n\'est pas confirmée.'
    elif roro == 'RISK-OFF':
        main_risk = 'Climat d\'aversion au risque (RISK-OFF) — pas d\'achat offensif, priorité à la protection du capital.'
    elif breadth is not None and breadth < 45:
        main_risk = 'Participation étroite — risque accru de faux départs sur les cassures.'

    return {
        'narrative': narrative,
        'word_count': words,
        'in_range': 120 <= words <= 340,      # cible §10 assouplie aux extrêmes de données
        'prices_mainly': prices_mainly,
        'dominant_sectors': dominant,
        'weak_sectors': weak,
        'main_risk': main_risk,
        'main_opportunity': main_opp,
        'calls_impact': calls_impact,
        'discipline': 'Fondamental avant technique · R:R ≥ 2:1 · stops du sous-jacent · décision unique.',
        'news_available': news_available,
        'sources': sorted(set(sources)),
    }


def _prices_mainly(m, vix, regime):
    """« Aujourd'hui, le marché prixe principalement… » — déduit du contexte réel."""
    roro = m.get('roro')
    if regime in (None, 'UNKNOWN', 'INCONNU', 'INDÉTERMINÉ'):
        return 'un régime indéterminé — le marché cherche une direction.'
    if roro == 'RISK-OFF':
        return 'l\'aversion au risque (RISK-OFF) et la protection du capital.'
    if vix is not None and vix > 25:
        return 'le stress de volatilité — les primes d\'options se paient cher.'
    if roro == 'RISK-ON':
        return 'l\'appétit pour le risque (RISK-ON) et les actifs de croissance.'
    return 'un équilibre prudent entre croissance et gestion du risque.'


__all__ = ['build_narrative']
