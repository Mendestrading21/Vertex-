"""tests/test_polish_opportunites_analyse.py — SKYLER LOT 57 : polish Opportunités + Analyse.

Inspection navigateur réelle (6 captures : 2 pages + fiche AAPL ×
desktop/mobile ; audit débordements : 0 — la table de comparaison mobile
défile dans `.vx-table-wrap` overflow-x:auto, conforme ; 0 erreur
console ; pairs de la fiche déjà cliquables data-open-analysis).
Deux défauts RÉELS trouvés dans la fiche et corrigés :

1. PERTE D'INFORMATION dans les lignes clé/valeur : `.vx-kv .k` était
   `nowrap + ellipsis` — « Politique par défaut » se rendait
   « Politique … » quand la valeur est longue. Le libellé peut
   maintenant passer à la ligne : l'information n'est JAMAIS tronquée.

2. LITTÉRAL COULEUR HORS PALETTE : l'étoile favori utilisait `#FFD27A`
   en dur (analysis_page.py) — remplacé par le token sémantique
   `var(--vx-warning)` (#D9BE3C, palette officielle). Le littéral
   analogue de `scorecard.py` est CÔTÉ MOTEUR (grade → couleur servie),
   hors périmètre d'un lot polish UI — dit au rapport, non touché.

Shell visible → SW v113 → v114.
"""
import re

PAGE = 'vertex/ui/pages/analysis_page.py'
UTIL = 'vertex/static/vertex/css/utilities.css'


def _read(p):
    return open(p, encoding='utf-8').read()


def test_kv_label_never_truncated():
    css = _read(UTIL)
    m = re.search(r"\.vx-kv \.k\{([^}]*)\}", css)
    assert m, 'règle .vx-kv .k introuvable'
    rule = m.group(1)
    assert 'text-overflow:ellipsis' not in rule, \
        'le libellé ne doit plus perdre d’information par ellipse'
    assert 'nowrap' not in rule


def test_fav_star_uses_semantic_token():
    src = _read(PAGE)
    assert '#FFD27A' not in src, 'littéral hors palette interdit côté UI'
    assert 'var(--vx-warning)' in src


def test_service_worker_bumped_to_at_least_v114():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 114
    assert 'td-shell-v113' not in body
