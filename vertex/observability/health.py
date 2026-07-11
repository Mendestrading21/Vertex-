"""vertex.observability.health — état de santé synthétique (§37)."""


def health_summary(components: dict) -> dict:
    """components : {'ibkr': bool|None, 'ai': bool|None, 'tradingview': bool|None,
    'scan': bool|None} — None = non configuré (mode dégradé assumé, pas une panne)."""
    degraded = [k for k, v in components.items() if v is False]
    absent = [k for k, v in components.items() if v is None]
    status = 'ok' if not degraded else 'degraded'
    return {'status': status, 'degraded': degraded, 'absent': absent,
            'note': 'l’application fonctionne en mode dégradé sans IBKR, sans IA '
                    'et sans TradingView — par conception'}
