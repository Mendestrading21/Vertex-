"""tests/test_a11y_peuple_lot30.py — LOT 30 : a11y révélée en mode peuplé.

Lighthouse sur Opportunités PEUPLÉE : 96. Deux causes mesurées :
- `opacity:.7` sur `.vx-chart-question` (glass.css) rend le jeton AA à
  3,84:1 — l'opacité détruit le contraste que le jeton garantit ;
- le bouton plein écran des graphiques porte un texte visible
  (« ⤢ Agrandir ») absent de son `aria-label` (« Plein écran ») — un
  utilisateur de commande vocale dit ce qu'il VOIT. Nés ROUGES.
"""
import re


def test_la_question_de_graphique_garde_son_contraste():
    v2 = open('vertex/static/vertex/css/vertex-2-0.css', encoding='utf-8').read()
    flat = re.sub(r'/\*.*?\*/', '', v2, flags=re.S).replace(' ', '')
    assert '.vx-chart-question' in flat and 'opacity:1' in flat, (
        'la couche finale doit annuler l\'opacité .7 de glass.css')
    #  la DERNIÈRE règle du sélecteur gagne la cascade — c'est elle qu'on juge
    regles = re.findall(r'\.vx-chart-question[^{]*\{([^}]*)\}', flat)
    assert regles and 'var(--vx-smoke)' in regles[-1], (
        'hiérarchie par le jeton AA mesuré, jamais par une opacité')


def test_le_bouton_plein_ecran_contient_son_texte_visible():
    js = open('vertex/static/vertex/js/charts/chart-core.js', encoding='utf-8').read()
    m = re.search(r'vx-chart-fs"[^>]*aria-label="([^"]+)"[^>]*>([^<]+)<', js)
    assert m, 'bouton plein écran introuvable'
    label, visible = m.group(1), m.group(2).replace('⤢', '').strip()
    assert visible.lower() in label.lower(), (
        'le nom accessible doit contenir le texte visible : %r vs %r'
        % (label, visible))


def test_aucune_page_ne_repose_une_opacite_sur_la_question():
    """Le mini-thème local d'une page écrasait la couche finale (opacity:.66
    dans briefing et opportunities) — interdit par la doctrine ET mesuré
    sous AA. Gardien : plus aucune opacité locale sur les questions."""
    import glob
    for f in glob.glob('vertex/ui/pages/*.py') + glob.glob('vertex/static/vertex/js/**/*.js', recursive=True):
        src = open(f, encoding='utf-8', errors='ignore').read()
        for lig in src.splitlines():
            if ('vx-chart-question{' in lig.replace(' ', '') or
                    'vx-card-question{' in lig.replace(' ', '')):
                assert 'opacity' not in lig, (f, lig.strip()[:100])
