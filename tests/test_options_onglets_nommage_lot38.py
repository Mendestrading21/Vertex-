"""Lot 38 — les onglets d'Options portent le nom de ce qu'ils ouvrent.

Dette consignée au lot 32 : l'onglet « Scanner » ouvrait la carte « Radar des
contrats » et l'onglet « LEAPS » ouvrait la carte « Scanner LEAPS » — noms
croisés hérités. Le contrat (`navigation-and-pages.md` §6) exige une sous-vue
Scanner : c'est la vue `leaps` qui EST le scanner (critères, lancement,
« Simuler ce contrat »). Les clés d'URL ne changent pas (favoris/liens).
"""
from pathlib import Path

SRC = (Path(__file__).resolve().parent.parent
       / 'vertex' / 'ui' / 'pages' / 'options_intel_page.py').read_text(encoding='utf-8')


def test_radar_s_appelle_radar():
    assert "('radar', 'Radar')" in SRC, (
        "l'onglet de la vue radar doit dire ce qu'il ouvre (« Radar des "
        "contrats ») — le libellé « Scanner » appartient au vrai scanner")


def test_leaps_s_appelle_scanner_leaps():
    assert "('leaps', 'Scanner LEAPS')" in SRC, (
        'la vue leaps EST le scanner du contrat (critères + « Simuler ce '
        'contrat ») — son onglet doit le dire')


def test_aucun_libelle_croise_residuel():
    assert "('radar', 'Scanner')" not in SRC
    assert "('leaps', 'LEAPS')" not in SRC
