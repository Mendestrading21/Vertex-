"""tests/test_freshness_lot79.py — SKYLER LOT 79 : fraîcheur des données affichées.

Audit navigateur : chaque zone à chiffres marché porte sa fraîcheur —
soit en propre (cartes VXCharts : « À l'instant · multileg_lab (board
réel) »), soit héritée de l'indicateur de page (Opportunités : « Il y a
2 min · <source> » + puce #op-fresh au-dessus de la dominante et de la
shortlist). Les 5 signalements de ma sonde stricte étaient des FAUX
POSITIFS (troncature à 400 chars / héritage de page) — vérifiés un à un
en navigateur, dits. SAIN — lot documentaire.

Gardiens PROSPECTIFS (nés verts, dits) : l'architecture de fraîcheur ne
doit pas se défaire silencieusement.
"""

OPPS = 'vertex/ui/pages/opportunities_page.py'


def _src():
    return open(OPPS, encoding='utf-8').read()


def test_opportunities_header_carries_scan_freshness():
    src = _src()
    assert 'VX.updateIndicator(scan&&(scan.scan_ts||scan.updated)' in src, (
        "l'en-tête d'Opportunités doit afficher l'âge du scan (source des scores)")
    assert 'op-fresh' in src and 'VX.freshness' in src, (
        'la puce de fraîcheur vivante doit rester au-dessus des cartes')


def test_opportunities_cards_footers_carry_timestamp_and_source():
    src = _src()
    assert src.count('VX.updateIndicator(scan.scan_ts||scan.updated') >= 2, (
        'les pieds de cartes (radar, options) doivent porter ts + source')
