"""
vertex/ui/nav.py — LA NAVIGATION : source unique (Ch. II, loi anti-duplication).

Une seule liste d'items. terminal.py réinjecte cette nav dans toutes les pages au
chargement. Ajouter/renommer/réordonner une page = éditer ICI, et nulle part
ailleurs — fini les six copies à garder synchronisées à la main.
"""

# (chemin, icône, libellé) — l'ordre de cette liste EST l'ordre d'affichage.
ITEMS = [
    ('/',            '📊', 'Overview'),
    ('/brief',       '🌅', 'Matinal'),
    ('/review',      '🏛️', 'Comité'),
    ('/decisions',   '📝', 'Décisions'),
    ('/research',    '🔬', 'Recherche'),
    ('/health',      '🩺', 'Santé'),
    ('/strategie',   '🎯', 'Desk'),
    ('/journal',     '📖', 'Journal'),
    ('/suivi',       '⭐', 'Watchlist'),
    ('/entreprises', '🔍', 'Scanner'),
    ('/options',     '⚡', 'Options'),
    ('/sectors',     '🔄', 'Rotation'),
    ('/catalysts',   '📅', 'Events'),
    ('/anomalies',   '📡', 'Signals'),
    ('/heatmap',     '🗺️', 'Heatmap'),
    ('/equipe',      '🏆', 'Playbook'),
    ('/bordel',      '🧠', 'Intel'),
    ('/settings',    '⚙️', 'Settings'),
]

# Séparateurs de section dans la sidebar — clé = 1er chemin de la section.
SECTIONS = [
    ('/',          'MARCHÉ'),
    ('/strategie', 'TRADING'),
    ('/sectors',   'ANALYSE'),
    ('/equipe',    'STRATÉGIE'),
    ('/settings',  'SYSTÈME'),
]


def nav_array_js():
    """Le littéral JS `[[path,icon,label],...]` attendu par le shell des pages."""
    return '[' + ','.join("['%s','%s','%s']" % it for it in ITEMS) + ']'


def sections_js():
    """Le littéral JS `{path:'SECTION',...}` (VSEC) attendu par la sidebar."""
    return '{' + ','.join("'%s':'%s'" % s for s in SECTIONS) + '}'


def paths():
    return [p for p, _, _ in ITEMS]


__all__ = ['ITEMS', 'SECTIONS', 'nav_array_js', 'sections_js', 'paths']
