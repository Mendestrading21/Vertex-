"""vertex.app.config_validation — validation de configuration (§11).

Chaque variable attendue reçoit un statut : CONFIGURED / MISSING / INVALID.
Optionnelle et absente → MISSING avec la conséquence exacte (jamais une
panne silencieuse). Aucune valeur de secret n'est jamais renvoyée ni loggée.
"""
from __future__ import annotations

import os

# (nom, requis, validateur, conséquence si absent)
_SPEC = (
    ('VERTEX_READONLY', False, lambda v: v.lower() in ('', 'true', '1'),
     'lecture seule forcée par le code (READONLY=True en dur) quoi qu’il arrive'),
    #  Conséquence CALCULÉE, jamais écrite d'avance : « écoute 127.0.0.1
    #  uniquement » est FAUX dès que `VERTEX_LAN=1` ou `PORT` est posé — deux
    #  cas où il n'y a ni code ni restriction. Cette phrase était la troisième
    #  copie de la même promesse, et aucune des trois ne lisait l'état réel.
    ('VERTEX_CODE', False, lambda v: len(v) >= 4, None),
    ('VERTEX_SECRET', False, lambda v: len(v) >= 16,
     'secret de session aléatoire persistant (.vertex_secret) utilisé'),
    ('ANTHROPIC_API_KEY', False, lambda v: v.startswith('sk-'),
     'brief/analyste servis par la synthèse déterministe des moteurs'),
    ('ANTHROPIC_MODEL', False, lambda v: v.startswith('claude'),
     'modèle par défaut claude-sonnet-5 utilisé si une clé est présente'),
    ('IBKR_HOST', False, lambda v: len(v) > 0,
     '127.0.0.1 par défaut (TWS local)'),
    ('IBKR_PORT', False, lambda v: v.isdigit(),
     '7497 par défaut (TWS paper) — 7496 pour TWS réel'),
    ('IBKR_CLIENT_ID', False, lambda v: v.isdigit(),
     'client id par défaut'),
    ('IBKR_ACCOUNT_ID', False, lambda v: len(v) >= 4,
     'compte détecté automatiquement à la connexion (lecture seule)'),
    ('IBKR_MARKET_DATA_MODE', False, lambda v: v.upper() in ('LIVE', 'DELAYED', 'FROZEN'),
     'mode de données du broker par défaut'),
    ('TRADINGVIEW_WEBHOOK_SECRET', False, lambda v: len(v) >= 12,
     'webhook TradingView désactivé (503 honnête, rien d’inventé)'),
    ('TRADINGVIEW_DEFAULT_TIMEFRAME', False, lambda v: len(v) > 0,
     'timeframe D par défaut pour les liens TradingView'),
    ('VERTEX_TIMEZONE', False, lambda v: '/' in v,
     'Europe/Zurich par défaut'),
    ('MARKET_TIMEZONE', False, lambda v: '/' in v,
     'America/New_York par défaut'),
    #  BLOQUANT pour la SEC, et pourtant invisible jusqu'ici : `sec_edgar`
    #  REFUSE d'appeler sans lui (`EntitlementManquant`), mais la variable
    #  n'était ni dans ce tableau ni dans `.env.example`. L'utilisateur
    #  recevait un refus sans aucun moyen de découvrir quoi poser. Le
    #  fair-access de la SEC exige un contact réel ; Vertex ne l'invente pas.
    ('SEC_USER_AGENT', False, lambda v: '@' in v and len(v) >= 10,
     'fondamentaux SEC EDGAR indisponibles — la SEC exige un User-Agent '
     'nommant un contact réel, que Vertex n’invente pas'),
)

# Alias historiques acceptés (compat .env existants)
_ALIASES = {'TRADINGVIEW_WEBHOOK_SECRET': ('TRADINGVIEW_SECRET',)}


def _get(name: str) -> str:
    v = os.environ.get(name, '')
    if not v:
        for alias in _ALIASES.get(name, ()):
            v = os.environ.get(alias, '')
            if v:
                break
    return v or ''


def _consequence_sans_code() -> str:
    """Ce qui arrive REELLEMENT sans code, ici et maintenant.

    Mesure du 25 aout 2026 : la phrase figee « sans code : ecoute 127.0.0.1
    uniquement » etait servie telle quelle par `/api/system/config`, y compris
    quand `VERTEX_LAN=1` ou `PORT` ouvrait l'ecoute a tout le reseau. Une
    consequence ecrite d'avance decrit une intention, pas un etat.
    """
    from vertex.app.exposition import exposition
    etat = exposition(False)
    if etat['expose_sans_code']:
        return ('sans code ET DEJA EXPOSE : le serveur ecoute 0.0.0.0 a cause de '
                '%s — toute personne sur ce reseau peut lire le portefeuille'
                % ('VERTEX_LAN=1' if etat['motif'] == 'VERTEX_LAN'
                   else 'la variable PORT'))
    return 'sans code : ecoute 127.0.0.1 uniquement (pas de LAN/iPhone)'


def validate_config() -> dict:
    """Statut par variable — sans jamais exposer la moindre valeur."""
    out = {}
    for name, required, check, consequence in _SPEC:
        if consequence is None:                 # consequence calculee (voir ci-dessus)
            consequence = _consequence_sans_code()
        v = _get(name).strip()
        if not v:
            out[name] = {'status': 'MISSING', 'required': required,
                         'consequence': consequence}
        elif not check(v):
            out[name] = {'status': 'INVALID', 'required': required,
                         'consequence': consequence}
        else:
            out[name] = {'status': 'CONFIGURED', 'required': required}
    out['_summary'] = {
        'configured': sum(1 for k, v in out.items()
                          if not k.startswith('_') and v['status'] == 'CONFIGURED'),
        'missing': sum(1 for k, v in out.items()
                       if not k.startswith('_') and v['status'] == 'MISSING'),
        'invalid': sum(1 for k, v in out.items()
                       if not k.startswith('_') and v['status'] == 'INVALID'),
    }
    return out


__all__ = ['validate_config']
