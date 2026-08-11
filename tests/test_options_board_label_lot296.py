"""SKYLER LOT 296 — gardien de l'étiquette de source du board d'options.

Contrat : en DEMO, le board d'options est SYNTHÉTIQUE — l'étiquette
« board réel » (codée en dur avant ce lot) était mensongère. La source
affichée doit suivre d.demo : « board démo » en démo, « board réel »
sinon. Les textes statiques des pages (servis identiques dans les deux
modes) ne revendiquent plus « réel ».
"""

STRUCTURE_JS = 'vertex/static/vertex/js/pages/options-structure.js'
INTEL_PAGE = 'vertex/ui/pages/options_intel_page.py'


def test_source_label_follows_demo_flag():
    with open(STRUCTURE_JS, encoding='utf-8') as f:
        js = f.read()
    assert "d.demo ? 'multileg_lab (board démo)' : 'multileg_lab (board réel)'" in js
    assert "(d.demo ? 'démo' : 'réel')" in js
    # Plus aucune étiquette « board réel » codée en dur : la seule
    # occurrence restante est la branche non-démo du ternaire source.
    assert js.count('board réel') == 1


def test_static_page_texts_do_not_claim_real():
    with open(INTEL_PAGE, encoding='utf-8') as f:
        src = f.read()
    assert 'board réel' not in src
