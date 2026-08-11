"""SKYLER LOT 298 — gardien TRANSVERSAL du mode de fraîcheur « live ».

Leçon des lots 296/297 : deux étiquettes de fraîcheur mentaient parce
que le mode « live » était codé EN DUR pour des données de MARCHÉ qui
ont un repli (cotes desk) ou une variante démo (board). Règle
codifiée : un mode « live » codé en dur n'est permis QUE pour l'état
interne du serveur (system_page — registre des jobs, rapport de
démarrage : ces données n'ont ni repli ni variante démo). Partout
ailleurs, le mode doit suivre un drapeau réel (__pfLive, d.demo…).
"""
import glob
import re

# Exceptions documentées :
# - system_page : cartes d'état INTERNE du serveur (registre des jobs,
#   rapport de démarrage) — pas de repli ni de variante démo possible ;
# - widget_lab : bibliothèque de design FIGÉE — ses pastilles « live »
#   sont des spécimens d'exposition, pas des affirmations sur des données.
ALLOWED = {'vertex/ui/pages/system_page.py', 'vertex/ui/pages/widget_lab.py'}

SCAN = (['terminal.py']
        + glob.glob('vertex/ui/**/*.py', recursive=True)
        + glob.glob('vertex/static/vertex/js/**/*.js', recursive=True))


def _offenders(pattern):
    out = []
    for path in SCAN:
        norm = path.replace('\\', '/')
        if norm in ALLOWED:
            continue
        with open(path, encoding='utf-8') as f:
            for i, line in enumerate(f, 1):
                if re.search(pattern, line):
                    out.append(f'{norm}:{i}: {line.strip()[:90]}')
    return out


def test_no_hardcoded_live_update_indicator():
    bad = _offenders(r",\s*'live'\)")
    assert not bad, ('mode « live » codé en dur (updateIndicator) — le mode '
                     'doit suivre un drapeau réel (__pfLive, d.demo…) : '
                     + ' | '.join(bad))


def test_no_hardcoded_live_chart_mode():
    bad = _offenders(r"mode:\s*'live'")
    assert not bad, ('mode:\'live\' codé en dur (VXCharts) — le mode doit '
                     'suivre un drapeau réel : ' + ' | '.join(bad))
