"""
elio/research.py — Lecture technique du graphique (texte) + recherche par titre.

chart_read(detail) renvoie une phrase d'analyse graphique en français, dérivée
UNIQUEMENT des indicateurs déjà calculés par analyse() (zéro donnée inventée).
"""


def _sig(d, k):
    return bool((d.get('signals') or {}).get(k))


def chart_read(d):
    """Analyse graphique condensée (FR) d'un titre, depuis ses indicateurs."""
    if not d:
        return None
    parts = []

    # Structure de tendance
    if _sig(d, 'stacked'):
        parts.append('tendance haussière nette (MM20 > MM50 > MM200 empilées)')
    elif _sig(d, 'above200') and _sig(d, 'above50'):
        parts.append('au-dessus des MM50 et MM200 (fond haussier)')
    elif _sig(d, 'above200'):
        parts.append('au-dessus de la MM200 mais sous la MM50 (consolidation)')
    else:
        parts.append('sous la MM200 (structure fragile)')

    # Momentum
    rsi = float(d.get('rsi', 50))
    if rsi >= 78:
        parts.append(f'RSI {rsi:.0f} (surchauffe, risque de repli)')
    elif rsi >= 60:
        parts.append(f'RSI {rsi:.0f} (momentum fort)')
    elif rsi >= 48:
        parts.append(f'RSI {rsi:.0f} (momentum sain)')
    else:
        parts.append(f'RSI {rsi:.0f} (momentum faible)')

    # Position dans le range 52s
    pos = float(d.get('pos52', 50))
    if pos >= 92:
        parts.append(f'collé aux plus-hauts 52s ({pos:.0f}%)')
    elif pos <= 25:
        parts.append(f'bas de range 52s ({pos:.0f}%)')

    # Sur-extension
    ext = float(d.get('ext_atr', 0))
    if ext >= 4:
        parts.append(f'sur-étendu ({ext:.1f} ATR au-dessus de la MM20)')

    # Volume
    volx = float(d.get('volx', 1))
    if volx >= 1.5:
        parts.append(f'volume soutenu ({volx:.1f}× la moyenne)')
    elif volx < 0.7:
        parts.append('volume sec (peu de conviction)')

    # Force relative
    rs = float(d.get('rs', 50))
    if rs >= 70:
        parts.append(f'surperforme le marché (force relative {rs:.0f})')
    elif rs <= 35:
        parts.append(f'sous-performe le marché (force relative {rs:.0f})')

    # NOUVEAUX SIGNAUX — cassure, compression, pente de tendance, divergence
    if d.get('breakout'):
        parts.append('🚀 cassure confirmée : nouveau plus-haut 20j porté par le volume')
    if d.get('squeeze'):
        br = d.get('bb_rank')
        parts.append(f'🧨 compression de volatilité (bandes au plus bas 6 mois{f", rang {br}%" if br is not None else ""}) — cassure souvent imminente')
    if _sig(d, 'stacked') and d.get('ma50_rising') is False:
        parts.append('⚠️ MM50 qui s\'aplatit (tendance qui s\'essouffle malgré l\'empilement)')
    if d.get('rsi_div') == 'bear':
        parts.append('⚠️ divergence baissière du RSI (prix au plus-haut, momentum en repli)')
    elif d.get('rsi_div') == 'bull':
        parts.append('↗️ divergence haussière du RSI (prix au plus-bas, momentum qui remonte)')
    if d.get('pullback'):
        parts.append('🎯 repli sain sur tendance (cours revenu près des moyennes, RSI apaisé) — entrée à moindre risque')
    if d.get('accumulation'):
        parts.append('🟢 accumulation détectée (OBV monte, prix à plat) — smart money qui charge')
    elif d.get('distribution'):
        parts.append('🔴 distribution cachée (OBV baisse, prix qui monte) — faiblesse sous le capot')

    return ' · '.join(parts)


def chart_verdict(d):
    """Une ligne de synthèse 'ce que dit le graphique pour un call'."""
    if not d:
        return None
    score = int(d.get('score', 0))
    if _sig(d, 'stacked') and score >= 72 and float(d.get('ext_atr', 0)) < 4:
        return ('✓ Graphique favorable à un CALL : tendance propre, pas sur-étendu, '
                'point d\'entrée correct.')
    if _sig(d, 'stacked') and float(d.get('ext_atr', 0)) >= 4:
        return '⚠ Tendance haussière mais sur-étendu : attendre un repli avant un call.'
    if not _sig(d, 'above200'):
        return '⛔ Graphique défavorable à un call : sous la MM200, tendance non confirmée.'
    return '≈ Graphique mitigé : tendance pas encore alignée, prudence.'
