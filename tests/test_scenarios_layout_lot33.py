"""tests/test_scenarios_layout_lot33.py — LOT 33 : lignes de scénarios collées.

Mesuré au navigateur (dossier ACN peuplé) : la carte SCÉNARIOS rendait
« Pessimiste-4.2 %cible 189,63 » — libellé, valeur et note fusionnés.
Cause : les règles `.vx-scenario(-grid/-k/-v/-note)` n'ont JAMAIS existé
en dehors de la variante `.an-decision-grid` (même la feuille morte ne
portait que celle-là). La couche finale donne au motif sa base, scopée à
l'espace analysis, alignée sur le design de la variante. Né ROUGE.
"""
import re

CSS = 'vertex/static/vertex/css/vertex-2-0.css'


def test_le_motif_scenario_a_sa_base_servie():
    s = re.sub(r'/\*.*?\*/', '', open(CSS, encoding='utf-8').read(), flags=re.S)
    flat = s.replace(' ', '')
    for sel in ('#vx-content[data-space="analysis"].vx-scenario-grid{',
                '#vx-content[data-space="analysis"].vx-scenario{',
                '#vx-content[data-space="analysis"].vx-scenario-v{',
                '#vx-content[data-space="analysis"].vx-scenario-note{'):
        assert sel in flat, sel
    #  la note occupe sa propre ligne (pleine largeur) — plus jamais collée
    m = re.search(r'\.vx-scenario-note\{([^}]*)\}', flat)
    assert m and 'grid-column:1/-1' in m.group(1)
