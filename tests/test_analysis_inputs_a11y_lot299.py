"""SKYLER LOT 299 — gardien a11y des champs de la fiche Analyse.

Contrat : balayage des noms accessibles sur 8 pages racines + 18 vues
profondes — seuls 2 champs étaient sans étiquette, tous deux sur la
fiche Analyse : la question du copilote (#an-cp-q) et le montant du
ticket pré-trade (#an-pt-amt). Un placeholder n'est PAS une étiquette
(il disparaît à la saisie, lecture inconstante par les lecteurs
d'écran) → aria-label requis.
"""

ANALYSIS_PAGE = 'vertex/ui/pages/analysis_page.py'


def _src():
    with open(ANALYSIS_PAGE, encoding='utf-8') as f:
        return f.read()


def test_copilot_question_has_aria_label():
    src = _src()
    line = next(l for l in src.splitlines() if 'id="an-cp-q"' in l)
    assert 'aria-label=' in line


def test_pretrade_amount_has_aria_label():
    src = _src()
    line = next(l for l in src.splitlines() if 'id="an-pt-amt"' in l)
    assert 'aria-label=' in line
