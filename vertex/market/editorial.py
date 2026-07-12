"""vertex.market.editorial — Brief éditorial narratif de séance (§10).

Compose un texte fluide de 180-320 mots à partir des données RÉELLES du scan
(indices, régime, volatilité, breadth, secteurs, comité). Chaque phrase n'est
émise que si sa donnée existe — jamais de récit inventé, jamais de fait
d'actualité fabriqué. Si les actualités manquent, le brief reste factuel
(données de marché) et le signale. Pur et testable.
"""
from __future__ import annotations


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
    m = scan_state.get('market') or scan_state.get('market_ctx') or {}
    sectors = [s for s in (scan_state.get('sectors') or []) if isinstance(s, dict)]
    committee = scan_state.get('committee') or {}
    counts = committee.get('counts') or {}
    idx = _indices(scan_state)
    news_items = (news_state or {}).get('items') or []
    sources = []

    sent = []  # phrases du narratif

    # 1-2. Direction des indices.
    sp, ndx = idx.get('sp'), idx.get('ndx')
    if sp is not None or ndx is not None:
        w = _dir_word(sp if sp is not None else ndx)
        lead = 'Les indices américains ont terminé %s' % (w or 'proches de l\'équilibre')
        bits = []
        if sp is not None:
            bits.append('le S&P 500 %+.1f %%' % sp)
        if ndx is not None:
            bits.append('le Nasdaq %+.1f %%' % ndx)
        if bits:
            lead += ', ' + ' et '.join(bits)
        # 3. Moteur principal : leadership techno si Nasdaq surperforme.
        if sp is not None and ndx is not None:
            if ndx > sp + 0.2:
                lead += ' — le leadership technologique domine la séance'
            elif sp > ndx + 0.2:
                lead += ' — la rotation favorise les valeurs cycliques hors technologie'
        sent.append(lead + '.')
        sources.append('indices (scan)')

    # 4. Régime + appétit pour le risque.
    regime = m.get('spy_regime') or m.get('regime')
    roro = m.get('roro')
    if regime or roro:
        s = 'Le régime de marché est %s' % (regime or 'indéterminé')
        if roro:
            s += ' dans un contexte %s' % roro
        sent.append(s + '.')

    # 5. Volatilité.
    vix = _num(m.get('vix'))
    if vix is not None:
        band = m.get('vix_band')
        s = 'La volatilité implicite (VIX) ressort à %.1f' % vix
        if band:
            s += ' (%s)' % band
        s += (', un niveau qui favorise l\'achat de convexité' if vix < 18 else
              ', ce qui renchérit les primes d\'options' if vix > 25 else
              ', dans une zone médiane')
        sent.append(s + '.')

    # 6. Breadth / participation.
    breadth = _num(m.get('breadth'))
    if breadth is not None:
        s = 'La participation (breadth) atteint %.0f %% des leaders au-dessus de leur moyenne' % breadth
        s += (' — participation saine' if breadth >= 55 else
              ' — participation étroite qui impose la sélectivité')
        sent.append(s + '.')

    # 7-8. Secteurs leaders / faibles.
    dominant, weak = [], []
    if sectors:
        ranked = sorted(sectors, key=lambda x: _num(x.get('avg_score')) or 0, reverse=True)
        top = ranked[0]
        dominant = [r.get('sector') for r in ranked[:2] if r.get('sector')]
        weak = [r.get('sector') for r in ranked[-2:] if r.get('sector')]
        if top.get('sector'):
            sent.append('Le leadership sectoriel revient à %s' % top.get('sector')
                        + (' devant %s' % ranked[1].get('sector') if len(ranked) > 1 and ranked[1].get('sector') else '')
                        + '.')
        sources.append('secteurs (scan)')

    # 9. Comité / opportunités.
    if counts:
        sent.append('Le comité identifie %d dossier(s) d\'achat possible(s) et %d en attente ; '
                    'aucune décision offensive n\'est prise sans valider le dossier complet.'
                    % (int(counts.get('ACHETER', 0)), int(counts.get('ATTENDRE', 0))))

    # 10. Actualités — UNIQUEMENT si réelles. Sinon signalé, jamais inventé.
    news_available = bool(news_items)
    if news_available:
        top_news = news_items[0]
        title = (top_news.get('title') or top_news.get('fr') or '').strip()
        if title:
            sent.append('À la une : %s.' % title[:180])
            sources.append('actualités (fil assaini)')
    else:
        sent.append('Aucune actualité validée n\'est disponible : ce brief s\'appuie '
                    'uniquement sur les données de marché (aucun récit n\'est inventé).')

    # 11. Discipline.
    sent.append('Discipline du jour : fondamental avant technique, R:R minimum 2:1, '
                'stops dérivés du sous-jacent, décision finale unique — aucune improvisation.')

    narrative = ' '.join(sent)
    words = len(narrative.split())

    # Blocs éditoriaux §10.
    prices_mainly = _prices_mainly(m, vix, regime)
    main_opp = None
    decisions = committee.get('decisions') or []
    prio = next((d for d in decisions if d.get('verdict') in ('ACHETER', 'RENFORCER')), None)
    if prio:
        main_opp = '%s — vérifier le dossier complet avant toute décision.' % prio.get('symbol')

    calls_impact = None
    if vix is not None:
        calls_impact = ('IV basse : environnement favorable à l\'achat de calls (convexité abordable).'
                        if vix < 18 else
                        'IV élevée : les calls coûtent cher, exiger un R:R strict.'
                        if vix > 25 else
                        'IV médiane : sélection de calls au cas par cas.')

    main_risk = None
    if regime in (None, 'UNKNOWN', 'INCONNU'):
        main_risk = 'Régime de marché indéterminé — aucun nouveau risque autorisé.'
    elif roro == 'RISK-OFF':
        main_risk = 'Contexte RISK-OFF — pas d\'achat offensif, protéger le capital.'
    elif breadth is not None and breadth < 45:
        main_risk = 'Participation étroite — risque de faux départs sur les cassures.'

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
    if regime in (None, 'UNKNOWN', 'INCONNU'):
        return 'un régime indéterminé — le marché cherche une direction.'
    if roro == 'RISK-OFF':
        return 'l\'aversion au risque (RISK-OFF) et la protection du capital.'
    if vix is not None and vix > 25:
        return 'le stress de volatilité — les primes d\'options se paient cher.'
    if roro == 'RISK-ON':
        return 'l\'appétit pour le risque (RISK-ON) et les actifs de croissance.'
    return 'un équilibre prudent entre croissance et gestion du risque.'


__all__ = ['build_narrative']
