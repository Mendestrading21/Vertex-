"""vertex.visualization.palette — registre central des couleurs sémantiques (§3).

UNE seule source de vérité pour les couleurs porteuses de sens. Interdit : une
couleur choisie au hasard pour différencier deux séries. Chaque couleur porte
une intention (marque, benchmark, positif, négatif, option…). Le thème
graphique JS (`chart-theme-obsidian-copper.js`) DOIT rester cohérent avec ce
registre — un test le vérifie.

Identité Vertex : CUIVRE SOBRE sur fond obsidienne. La marque reste une série
de référence (PAS « hausse ») : le cuivre ne remplace jamais l'émeraude ou le
corail sémantiques. Tout bleu dominant reste interdit. Le cyan #45D6E8 reste
réservé aux comparaisons techniques.
"""
from __future__ import annotations

# ── Couleurs de marque (cuivre = identité, jamais direction financière) ──
BRAND = '#D28A54'          # cuivre Vertex, série principale (pas « hausse »)
BRAND_HOVER = '#E1A06E'    # cuivre clair, interaction / survol
COPPER = '#8A8284'         # série neutre acier (gris chaud)
COPPER_LIGHT = BRAND_HOVER  # alias historique conservé pour compatibilité
AMBER = '#D9BE3C'          # série secondaire / attention
BEIGE = '#c8bfae'          # benchmark clair (sable)
TECHNICAL = '#45D6E8'      # cyan — comparaison technique UNIQUEMENT (doctrine §3)

# ── États (direction / statut réel uniquement) ────────────────────────
POSITIVE = '#2BBE90'       # ÉMERAUDE — gain / donnée positive (distinct de la marque)
NEGATIVE = '#E9555F'       # corail — perte / risque
WARNING = '#D9BE3C'
NEUTRAL = '#BABABA'        # benchmark neutre (gris chaud)
OPTION = '#9B7BFF'         # violet contrôlé — RÉSERVÉ aux options / IV / Greeks
#                            (identité déployée : tokens.css, chart-theme, chart-core)

# ── Texte ──────────────────────────────────────────────────────────────
TEXT = '#F8F5F3'
TEXT_DIM = '#BABABA'
TEXT_MUTED = '#989092'

# Palette de séries — ordre déterministe, jamais arc-en-ciel. La série 0 est
# toujours la marque ; la série 1 TRANCHE (cyan de comparaison technique —
# lot 56 : trois blancs-gris consécutifs étaient indistinguables sur un même
# graphique comparé) ; les suivantes descendent en neutralité.
SERIES = (BRAND, TECHNICAL, BEIGE, OPTION, AMBER, COPPER)

# Rôle sémantique → couleur. C'est CE dictionnaire qui fait autorité.
SEMANTIC = {
    'brand': BRAND,
    'brand_hover': BRAND_HOVER,
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

    Sert au garde-fou zéro-bleu. Ne considère PAS l'émeraude (#2BBE90) ni le
    violet option (#9B7BFF, r élevé) ni le cyan de comparaison (#45D6E8, g élevé)
    comme bleus identitaires."""
    h = str(hex_color or '').lstrip('#')
    if len(h) != 6:
        return False
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        return False
    return b > r + 30 and b > g + 30 and b > 90 and r < 110


# Nom historique conservé pour l'API du garde-fou. Le cuivre actuel n'est pas
# bleu ; l'ensemble reste l'allow-list explicite des couleurs identitaires.
BRAND_BLUES = {BRAND.lower(), BRAND_HOVER.lower()}


def audit_no_blue() -> list:
    """Rend la liste des couleurs du registre « bleu dominant » NON autorisées.
    L'allow-list identitaire historique est admise ; tout autre bleu doit être vide."""
    return [name for name, col in SEMANTIC.items()
            if is_bluish(col) and str(col).lower() not in BRAND_BLUES]


__all__ = [
    'BRAND', 'BRAND_HOVER', 'COPPER', 'COPPER_LIGHT', 'AMBER', 'BEIGE', 'TECHNICAL', 'POSITIVE', 'NEGATIVE',
    'WARNING', 'NEUTRAL', 'OPTION', 'TEXT', 'TEXT_DIM', 'TEXT_MUTED',
    'SERIES', 'SEMANTIC', 'STATUS_COLOR', 'series_color', 'status_color',
    'is_bluish', 'audit_no_blue',
]
