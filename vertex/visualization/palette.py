"""vertex.visualization.palette — registre central des couleurs sémantiques.

Vertex Signal OS applique une règle stricte : une couleur = une fonction.
Violet = identité et série principale ; violet profond = options / volatilité ;
émeraude = positif ; corail = négatif ; jaune = attente ; cyan = comparaison
technique ; gris = benchmark et contexte neutre.

Le thème JavaScript `chart-theme-obsidian-copper.js` est le miroir exact de ce
registre. Un test compare les deux sources afin d'éviter toute dérive.
"""
from __future__ import annotations

# ── Identité et séries ──────────────────────────────────────────────────────
BRAND = '#9B7BFF'          # série principale Vertex / interaction
COPPER = '#8A8284'         # série neutre acier
COPPER_LIGHT = '#EEF1F5'   # repère clair / contraste ponctuel
AMBER = '#D9BE3C'          # attention / série secondaire
BEIGE = '#c8bfae'          # benchmark clair
TECHNICAL = '#45D6E8'      # comparaison technique uniquement

# ── États financiers réels ─────────────────────────────────────────────────
POSITIVE = '#2BBE90'       # gain / validation réelle
NEGATIVE = '#E9555F'       # perte / risque / invalidation
WARNING = '#D9BE3C'        # attente / seuil / prudence
NEUTRAL = '#BABABA'        # benchmark neutre
OPTION = '#7F5DF0'         # options, IV et Greeks — distinct du violet de marque

# ── Texte ──────────────────────────────────────────────────────────────────
TEXT = '#F8F5F3'
TEXT_DIM = '#BABABA'
TEXT_MUTED = '#8A8284'

# Ordre déterministe, jamais arc-en-ciel. La première série est l'identité
# Vertex ; la deuxième tranche clairement pour une comparaison technique.
SERIES = (BRAND, TECHNICAL, BEIGE, COPPER_LIGHT, AMBER, COPPER)

SEMANTIC = {
    'brand': BRAND,
    'copper': COPPER,
    'copper_light': COPPER_LIGHT,
    'amber': AMBER,
    'beige': BEIGE,
    'technical': TECHNICAL,
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

STATUS_COLOR = {
    'FAVORABLE': POSITIVE,
    'NEUTRE': NEUTRAL,
    'DEFAVORABLE': NEGATIVE,
    'BLOQUANT': NEGATIVE,
    'INCONNU': TEXT_MUTED,
}


def series_color(index: int) -> str:
    """Couleur déterministe pour la série n° ``index``."""
    return SERIES[index % len(SERIES)]


def status_color(status: str) -> str:
    return STATUS_COLOR.get(status, TEXT_MUTED)


def is_bluish(hex_color: str) -> bool:
    """Détecte un bleu dominant non autorisé.

    Le violet de marque possède une composante rouge forte ; le cyan technique
    possède une composante verte forte. Ils ne sont donc pas classés comme bleu
    identitaire par cette heuristique.
    """
    h = str(hex_color or '').lstrip('#')
    if len(h) != 6:
        return False
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return False
    return b > r + 30 and b > g + 30 and b > 90 and r < 110


# Exceptions historiques du garde-fou. Le violet n'est pas considéré comme
# bleu par ``is_bluish`` ; cette liste reste explicite pour les tests hérités.
BRAND_BLUES = {BRAND.lower(), COPPER_LIGHT.lower()}


def audit_no_blue() -> list:
    """Liste les couleurs bleues dominantes non autorisées du registre."""
    return [name for name, col in SEMANTIC.items()
            if is_bluish(col) and str(col).lower() not in BRAND_BLUES]


__all__ = [
    'BRAND', 'COPPER', 'COPPER_LIGHT', 'AMBER', 'BEIGE', 'TECHNICAL',
    'POSITIVE', 'NEGATIVE', 'WARNING', 'NEUTRAL', 'OPTION', 'TEXT',
    'TEXT_DIM', 'TEXT_MUTED', 'SERIES', 'SEMANTIC', 'STATUS_COLOR',
    'series_color', 'status_color', 'is_bluish', 'audit_no_blue',
]
