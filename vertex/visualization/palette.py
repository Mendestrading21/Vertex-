"""vertex.visualization.palette — registre central des couleurs sémantiques (§3).

UNE seule source de vérité pour les couleurs porteuses de sens. Interdit : une
couleur choisie au hasard pour différencier deux séries. Chaque couleur porte
une intention (marque, benchmark, positif, négatif, option…). Le thème
graphique JS (`chart-theme-obsidian-copper.js`) DOIT rester cohérent avec ce
registre — un test le vérifie.

Identité Vertex V4 : Obsidian Prism. Violet prism = marque/série de référence
(PAS « hausse »). Vert = positif. Magenta/teal = séries secondaires. Zéro bleu
dominant (le bleu de comparaison §6.2 reste différé, hors registre).
"""
from __future__ import annotations

# ── Couleurs de marque (série principale = VIOLET PRISM V4) ────────────
BRAND = '#9a5cff'          # série principale Vertex — VIOLET prism (identité, pas « hausse »)
COPPER = '#3a3f47'         # surface neutre sombre (legacy conservé)
COPPER_LIGHT = '#a875ff'   # violet clair (accents)
AMBER = '#e6a846'          # série secondaire / attente
BEIGE = '#c0b79f'          # benchmark clair (sable)
MAGENTA = '#d86cb7'        # série secondaire distincte (marque)
TEAL = '#53b9ad'           # macro / cross-asset / liquidité
STONE = '#6d746e'          # série neutre sombre

# ── États (direction / statut réel uniquement) ────────────────────────
POSITIVE = '#35d28b'       # vert — gain / donnée positive (distinct de la marque violette)
NEGATIVE = '#ff625f'       # corail — perte / risque
WARNING = '#e6a846'
NEUTRAL = '#7e8798'        # benchmark neutre (gris froid)
OPTION = '#a875ff'         # violet — RÉSERVÉ aux options / IV / Greeks
#                            (identité déployée : tokens.css, chart-theme, chart-core)

# ── Texte ──────────────────────────────────────────────────────────────
TEXT = '#f5f7fb'
TEXT_DIM = '#bec5d2'
TEXT_MUTED = '#858e9f'

# Palette de séries — ordre déterministe, jamais arc-en-ciel. La série 0 est
# toujours la marque ; les suivantes restent distinctes et neutres.
SERIES = (BRAND, NEUTRAL, MAGENTA, TEAL, AMBER, STONE)

# Rôle sémantique → couleur. C'est CE dictionnaire qui fait autorité.
SEMANTIC = {
    'brand': BRAND,
    'copper': COPPER,
    'copper_light': COPPER_LIGHT,
    'amber': AMBER,
    'beige': BEIGE,
    'magenta': MAGENTA,
    'teal': TEAL,
    'stone': STONE,
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
    """Heuristique « bleu dominant » : b nettement > r et > g, b élevé, ET rouge
    FAIBLE (le bleu vrai a peu de rouge ; le violet en a beaucoup).

    Sert au garde-fou zéro-bleu. Ne considère PAS le vert (#36c889) ni le
    violet option (#9c79d0, r élevé) comme bleus."""
    h = str(hex_color or '').lstrip('#')
    if len(h) != 6:
        return False
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return False
    return b > r + 30 and b > g + 30 and b > 90 and r < 110


def audit_no_blue() -> list:
    """Rend la liste des couleurs du registre qui seraient « bleu dominant ».
    Doit rester vide (identité Vertex sans bleu)."""
    return [name for name, col in SEMANTIC.items() if is_bluish(col)]


__all__ = [
    'BRAND', 'COPPER', 'COPPER_LIGHT', 'AMBER', 'BEIGE', 'MAGENTA', 'TEAL',
    'STONE', 'POSITIVE', 'NEGATIVE', 'WARNING', 'NEUTRAL', 'OPTION', 'TEXT',
    'TEXT_DIM', 'TEXT_MUTED', 'SERIES', 'SEMANTIC', 'STATUS_COLOR',
    'series_color', 'status_color', 'is_bluish', 'audit_no_blue',
]
