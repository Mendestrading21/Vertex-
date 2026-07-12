"""vertex.visualization.palette — registre central des couleurs sémantiques (§3).

UNE seule source de vérité pour les couleurs porteuses de sens. Interdit : une
couleur choisie au hasard pour différencier deux séries. Chaque couleur porte
une intention (marque, benchmark, positif, négatif, option…). Le thème
graphique JS (`chart-theme-obsidian-copper.js`) DOIT rester cohérent avec ce
registre — un test le vérifie.

Identité Vertex : Obsidian Copper Deep. Zéro bleu dominant.
"""
from __future__ import annotations

# ── Couleurs de marque (série principale = orange cuivré) ──────────────
BRAND = '#cf6128'          # série principale Vertex
COPPER = '#914b2b'
COPPER_LIGHT = '#b9683d'
AMBER = '#ce8a29'          # série secondaire
BEIGE = '#c8ad8d'          # benchmark clair

# ── États (direction / statut réel uniquement) ────────────────────────
POSITIVE = '#39b978'
NEGATIVE = '#dc6254'
WARNING = '#cc892c'
NEUTRAL = '#8e8981'        # benchmark neutre
OPTION = '#85609f'         # violet sombre — RÉSERVÉ aux options / IA
#                            (identité déployée : tokens.css, chart-theme, chart-core)

# ── Texte ──────────────────────────────────────────────────────────────
TEXT = '#f1efeb'
TEXT_DIM = '#b6b1aa'
TEXT_MUTED = '#817c75'

# Palette de séries — ordre déterministe, jamais arc-en-ciel. La série 0 est
# toujours la marque ; les suivantes descendent en neutralité.
SERIES = (BRAND, BEIGE, NEUTRAL, OPTION, AMBER, COPPER)

# Rôle sémantique → couleur. C'est CE dictionnaire qui fait autorité.
SEMANTIC = {
    'brand': BRAND,
    'copper': COPPER,
    'copper_light': COPPER_LIGHT,
    'amber': AMBER,
    'beige': BEIGE,
    'benchmark': NEUTRAL,
    'positive': POSITIVE,
    'negative': NEGATIVE,
    'warning': WARNING,
    'neutral': NEUTRAL,
    'option': OPTION,
    'text': TEXT,
    'text_dim': TEXT_DIM,
    'text_muted': TEXT_MUTED,
}

# Statut canonique d'interprétation → couleur (cohérent avec schemas.STATUSES).
STATUS_COLOR = {
    'FAVORABLE': POSITIVE,
    'NEUTRE': NEUTRAL,
    'DEFAVORABLE': NEGATIVE,
    'BLOQUANT': NEGATIVE,
    'INCONNU': TEXT_MUTED,
}


def series_color(index: int) -> str:
    """Couleur déterministe pour la série n° `index` (boucle sans arc-en-ciel)."""
    return SERIES[index % len(SERIES)]


def status_color(status: str) -> str:
    return STATUS_COLOR.get(status, TEXT_MUTED)


def is_bluish(hex_color: str) -> bool:
    """Heuristique « bleu dominant » : b nettement > r et > g, et b élevé.

    Sert au garde-fou zéro-bleu. Ne considère PAS le vert (#39b978) ni le
    violet option (#806096) comme bleus."""
    h = str(hex_color or '').lstrip('#')
    if len(h) != 6:
        return False
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return False
    return b > r + 30 and b > g + 30 and b > 90


def audit_no_blue() -> list:
    """Rend la liste des couleurs du registre qui seraient « bleu dominant ».
    Doit rester vide (identité Vertex sans bleu)."""
    return [name for name, col in SEMANTIC.items() if is_bluish(col)]


__all__ = [
    'BRAND', 'COPPER', 'COPPER_LIGHT', 'AMBER', 'BEIGE', 'POSITIVE', 'NEGATIVE',
    'WARNING', 'NEUTRAL', 'OPTION', 'TEXT', 'TEXT_DIM', 'TEXT_MUTED',
    'SERIES', 'SEMANTIC', 'STATUS_COLOR', 'series_color', 'status_color',
    'is_bluish', 'audit_no_blue',
]
