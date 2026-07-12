"""vertex.ai.provenance — étiquetage d'honnêteté des données enrichies par Claude.

INVARIANT PRODUIT : une valeur produite par Claude ne doit JAMAIS être affichée
comme une donnée broker réelle. Ce module est le point de passage unique : toute
valeur issue de l'IA est emballée dans une enveloppe qui porte sa source réelle,
son horodatage, ses citations (liens) et le fait qu'elle est une ESTIMATION
DIFFÉRÉE — jamais un prix live ni un chiffre inventé sans source.

Précédence honnête : donnée broker RÉELLE > estimation Claude+web (étiquetée) > —.
"""
from __future__ import annotations

import time

# Sources canoniques (jamais « réel » sans preuve broker).
SRC_BROKER = 'broker'          # IBKR live/différé confirmé par le serveur — la vérité
SRC_CLAUDE_WEB = 'claude_web'  # Claude + recherche web : réel mais DIFFÉRÉ, avec citations
SRC_CLAUDE = 'claude'          # Claude sans web : interprétation, PAS un chiffre nouveau
SRC_ENGINE = 'engine'          # moteur déterministe interne
SRC_NONE = 'none'              # aucune donnée — honnête « — »

_LABELS = {
    SRC_BROKER: 'Broker (réel)',
    SRC_CLAUDE_WEB: 'via Claude · web · différé',
    SRC_CLAUDE: 'Analyse Claude',
    SRC_ENGINE: 'Moteur Vertex',
    SRC_NONE: '—',
}


def _now_iso() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def label(source: str) -> str:
    """Libellé humain court d'une source (pour badges UI)."""
    return _LABELS.get(source, source)


def wrap(value, *, source, as_of=None, citations=None, estimation=None, note=''):
    """Emballe une valeur avec sa provenance honnête.

    value      : la donnée (nombre, texte, liste…) — None si absente.
    source     : une des constantes SRC_*.
    as_of      : horodatage ISO de la donnée (défaut : maintenant).
    citations  : liste de {title, url} — les liens réels d'où vient la donnée.
    estimation : True si c'est une estimation/différé (auto-déduit si non fourni).
    note       : précision libre (ex. « prix différé 15 min »).
    """
    if estimation is None:
        # Tout ce qui vient de Claude est une estimation ; le broker seul est « réel ».
        estimation = source in (SRC_CLAUDE_WEB, SRC_CLAUDE)
    cits = [c for c in (citations or []) if isinstance(c, dict) and c.get('url')]
    return {
        'value': value,
        'source': source,
        'source_label': label(source),
        'as_of': as_of or _now_iso(),
        'citations': cits,
        'estimation': bool(estimation),
        'is_real_broker': source == SRC_BROKER,
        'note': note or '',
    }


def absent(note='donnée indisponible') -> dict:
    """Enveloppe honnête d'une donnée absente — jamais un 0 inventé."""
    return wrap(None, source=SRC_NONE, estimation=False, note=note)


def is_trustworthy_number(env) -> bool:
    """Un nombre est-il exploitable pour un calcul ? True seulement si présent."""
    return isinstance(env, dict) and env.get('value') is not None


def prefer(*envelopes):
    """Choisit la meilleure enveloppe selon la précédence honnête.

    Broker réel d'abord, puis Claude+web, puis Claude, puis moteur, puis absent.
    Ignore les enveloppes sans valeur. Ne fabrique jamais.
    """
    order = {SRC_BROKER: 0, SRC_CLAUDE_WEB: 1, SRC_CLAUDE: 2, SRC_ENGINE: 3, SRC_NONE: 9}
    best = None
    for env in envelopes:
        if not isinstance(env, dict) or env.get('value') is None:
            continue
        rank = order.get(env.get('source'), 8)
        if best is None or rank < best[0]:
            best = (rank, env)
    return best[1] if best else absent()


__all__ = [
    'SRC_BROKER', 'SRC_CLAUDE_WEB', 'SRC_CLAUDE', 'SRC_ENGINE', 'SRC_NONE',
    'label', 'wrap', 'absent', 'is_trustworthy_number', 'prefer',
]
