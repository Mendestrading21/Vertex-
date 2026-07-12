"""vertex.market.daily_brief — le Brief Vertex quotidien (§15).

Types : PRE_MARKET / INTRADAY / CLOSE / WEEKLY (choisi par l'horloge de
New York). Composition déterministe depuis les DONNÉES RÉELLES : scan
(indices, secteurs, VIX, breadth), comité, actualités validées/sourcées
(news_pipeline), positions déclarées. Structure §15 en 10 sections,
150-280 mots + version compacte 8-12 lignes. AUCUN événement inventé :
si le flux d'actualités est vide, la section le DIT au lieu de broder.
"""
from __future__ import annotations

import time
from datetime import datetime
from zoneinfo import ZoneInfo

from vertex.market import news_pipeline
from vertex.market.news_impact import potential_impact


def brief_kind(now=None) -> str:
    ny = now or datetime.now(ZoneInfo('America/New_York'))
    if ny.weekday() >= 5:
        return 'WEEKLY'
    mins = ny.hour * 60 + ny.minute
    if mins < 570:            # avant 9h30
        return 'PRE_MARKET'
    if mins < 955:            # avant ~15h55
        return 'INTRADAY'
    return 'CLOSE'


def _idx(scan_state):
    idx = scan_state.get('indices') or []
    return {i.get('name'): i for i in idx if isinstance(i, dict)}


def build_daily_brief(scan_state: dict, news_state: dict | None = None,
                      portfolio_syms: list[str] | None = None,
                      kind: str | None = None) -> dict:
    """Brief complet : sections, texte principal, compact, sources, méta."""
    kind = kind or brief_kind()
    m = scan_state.get('market') or scan_state.get('market_ctx') or {}
    by = _idx(scan_state)
    sectors = scan_state.get('sectors') or []
    committee = (scan_state.get('committee') or {})
    counts = committee.get('counts') or {}
    source = scan_state.get('source') or 'aucune'
    demo = source == 'demo'
    syms = portfolio_syms or []

    news = news_pipeline.collect(news_state or {}, syms) if news_state is not None \
        else {'events': [], 'rejected': 0, 'raw_count': 0}
    top_events = news['events'][:4]

    sections: list[tuple[str, str]] = []

    # 1. Situation générale
    regime = m.get('spy_regime') or m.get('regime') or 'n/d'
    roro = m.get('roro') or ''
    sections.append(('Situation générale',
                     f"Régime {regime}{' · ' + roro if roro else ''} — "
                     + ('participation saine.' if (m.get('breadth') or 0) >= 55
                        else 'sélectivité obligatoire.')))
    # 2. Indices
    parts = []
    for name in ('S&P 500', 'Nasdaq', 'Dow Jones', 'Russell 2000'):
        e = by.get(name) or {}
        if e.get('change') is not None:
            parts.append(f"{name} {e['change']:+.1f} %")
    sections.append(('Indices', ' · '.join(parts) + '.' if parts
                     else 'Indices indisponibles dans le dernier scan.'))
    # 3. Taux et volatilité
    vix = m.get('vix')
    tnx = (by.get('Taux 10 ans') or {}).get('price')
    vol_txt = []
    if vix is not None:
        vol_txt.append(f"VIX {vix}{' (' + m.get('vix_band', '') + ')' if m.get('vix_band') else ''}")
    if tnx is not None:
        vol_txt.append(f'10 ans {tnx}')
    sections.append(('Taux et volatilité', ' · '.join(vol_txt) + '.' if vol_txt
                     else 'Taux et volatilité non fournis par le scan.'))
    # 4. Actualité dominante — UNIQUEMENT des événements réels et sourcés
    if top_events:
        lead = top_events[0]
        imp = potential_impact(lead)
        sections.append(('Actualité dominante',
                         f"{lead.get('title_fr') or lead['title']} "
                         f"({lead['source']}, impact {imp['direction'].lower().replace('_', ' ')})."))
    else:
        sections.append(('Actualité dominante',
                         'Flux d’actualités hors ligne dans cet environnement — '
                         'aucun événement affiché plutôt qu’un événement inventé.'))
    # 5-6. Secteurs
    if sectors and isinstance(sectors[0], dict):
        sections.append(('Secteurs leaders',
                         f"{sectors[0].get('sector', 'n/d')} en tête "
                         f"(score {sectors[0].get('avg_score', 'n/d')})."))
        if len(sectors) > 1:
            sections.append(('Secteurs faibles', f"{sectors[-1].get('sector', 'n/d')} à la traîne."))
    else:
        sections.append(('Secteurs', 'Rotation sectorielle non calculée par le dernier scan.'))
    # 7. Entreprises importantes (comité + événements entreprises réels)
    decisions = committee.get('decisions') or []
    prio = next((d for d in decisions if d.get('verdict') in ('ACHETER', 'RENFORCER')), None)
    ent = []
    if prio:
        ent.append(f"{prio.get('symbol')} ressort du comité — dossier complet requis avant décision")
    for ev in top_events:
        if ev['category'] in ('RESULTATS', 'GUIDANCE') and ev.get('entities'):
            ent.append(f"{ev['entities'][0]} : {ev.get('title_fr') or ev['title']} ({ev['source']})")
            break
    sections.append(('Entreprises', ' · '.join(ent) + '.' if ent
                     else f"Comité : {counts.get('ACHETER', 0)} achat(s) possibles, "
                          f"{counts.get('ATTENDRE', 0)} en attente."))
    # 8. Options et volatilité
    board = scan_state.get('options_board') or []
    sections.append(('Options', f"{len(board)} contrat(s) sur le board Vertex Dynamic Options — "
                     'sélection CALL prioritaire, R:R minimal 2:1.' if board
                     else 'Board options vide — aucun contrat ne force le R:R 2:1.'))
    # 9. Portefeuille
    sections.append(('Portefeuille', f"{len(syms)} position(s) déclarée(s) suivie(s)."
                     if syms else 'Aucune position déclarée — surveillance générale.'))
    # 10. Plan et discipline
    sections.append(('Plan et discipline',
                     'Aucune improvisation : fondamental avant technique, décision finale '
                     'unique, R:R 2:1 minimum, stops dérivés du sous-jacent.'))

    text = ' '.join(f'{label} : {body}' for label, body in sections)
    words = len(text.split())
    compact = [f'{label} : {body}' for label, body in sections][:12]
    sources = sorted({ev['source'] for ev in top_events} | {source})

    return {
        'kind': kind,
        'sections': [{'label': l, 'text': b} for l, b in sections],
        'text': text,
        'word_count': words,
        'compact': compact[:12],
        'what_changed': [f"{ev.get('title_fr') or ev['title']} ({ev['source']})"
                         for ev in top_events[:3]],
        'watching': [s.get('symbol') for s in decisions[:3] if s.get('symbol')],
        'main_risk': ('Régime UNKNOWN — risque neuf bloqué' if regime in ('UNKNOWN', 'n/d')
                      else f'Invalidation du régime {regime}'),
        'main_opportunity': (prio.get('symbol') if prio else None),
        'sources': sources,
        'news_rejected': news['rejected'],
        'as_of': scan_state.get('updated') or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'generator': 'deterministic',
        'demo': demo,
    }


__all__ = ['build_daily_brief', 'brief_kind']
