"""tests/test_prime_derivee_lot33.py — LOT 33 : prime « — » à côté de son propre montant.

Mesuré (chaîne du dossier ACN) : PRIME affichait « — » pendant que
RISQUE MAX (= prime payée) affichait 3 443 $ sur la même ligne — le coût
par contrat EST la prime × 100 (multiplicateur US). La colonne dérive
désormais la prime du coût quand mid/premium manquent : une conversion
d'unité exacte, jamais une estimation. Né ROUGE.
"""


def test_la_prime_se_derive_du_cout_quand_mid_manque():
    js = open('vertex/static/vertex/js/charts/option-chain.js', encoding='utf-8').read()
    assert 'c.cost / 100' in js, (
        'prime par action = coût par contrat / 100 — la même grandeur dans '
        'une autre unité, affichée au lieu d\'un tiret contradictoire')
