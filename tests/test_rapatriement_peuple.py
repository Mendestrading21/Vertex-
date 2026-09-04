"""tests/test_rapatriement_peuple.py — LOT 29 : orphelines du mode peuplé.

Le mode démo (DEMO=1 — la vraie variable, pas VERTEX_DEMO) a révélé ce que
les vérifications en mode dégradé ne pouvaient pas voir : 20 classes
rendues UNIQUEMENT avec des données n'avaient AUCUNE règle servie (leurs
règles vivaient dans la feuille morte supprimée au lot 24). Effet mesuré
au navigateur : « Nouveau risqueAutorisé », « Confiance42 % » — libellés
collés aux valeurs dans les puces de régime de Marchés. Nés ROUGES.
"""
import re

CSS = 'vertex/static/vertex/css/vertex-2-0.css'


def _css():
    return open(CSS, encoding='utf-8').read()


def test_les_puces_de_regime_ont_leurs_regles_servies():
    s = _css()
    for sel in ('#vx-content[data-space="markets"] .vx-mk-chips',
                '#vx-content[data-space="markets"] .vx-mk-chip'):
        assert sel in s, sel
    bloc = s.split('.vx-mk-chip{', 1)[1][:300] if '.vx-mk-chip{' in s.replace(' ', '') else \
        re.search(r'\.vx-mk-chip\s*\{([^}]*)\}', s).group(1)
    assert 'flex-direction:column' in bloc.replace(' ', ''), (
        'libellé AU-DESSUS de la valeur — sinon ils se collent en ligne')


def test_les_leaders_et_le_regime_ont_leurs_regles():
    s = _css()
    for sel in ('.vx-mk-lead-row', '.vx-mk-regime-name', '.vx-mk-lead-bar'):
        assert sel in s, sel


def test_l_identite_du_dossier_analyse_a_ses_regles():
    s = _css()
    for sel in ('.an-identity', '.an-main-column', '.an-scorecard-note'):
        assert sel in s, sel


def test_les_greeks_et_scenarios_options_ont_leurs_regles():
    s = _css()
    for sel in ('.vx-greeks', '.vx-greek', '.vx-scenario-head'):
        assert sel in s, sel


def test_aucun_jeton_neon_dans_le_rapatriement():
    #  hors commentaires : seul le CODE compte (le §27 mentionne --ng- pour
    #  documenter le remplacement — c'est une mention, pas un usage).
    code = re.sub(r'/\*.*?\*/', '', _css(), flags=re.S)
    assert '--ng-' not in code, 'les jetons neon ne reviennent jamais'
