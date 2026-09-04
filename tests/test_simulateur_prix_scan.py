"""tests/test_simulateur_prix_scan.py — LOT 31 : le simulateur contredisait sa page.

Mesuré en mode peuplé : classe Actions, ACN (présent au scan), quantité
saisie → « Simulation impossible : demande… un prix de référence », alors
que les Hypothèses de la même page promettent « le prix de référence est
le prix RÉEL du scan courant ». Cible : le prix vient du scan (provenance
dite), la saisie manuelle PRIME (déclaration utilisateur), le refus ne
subsiste que sans l'un ni l'autre — jamais un prix supposé. Né ROUGE.
"""


def _js():
    return open('vertex/static/vertex/js/pages/simulator.js', encoding='utf-8').read()


def test_le_prix_d_action_vient_du_scan_quand_il_existe():
    js = _js()
    assert 'prixDuScan' in js, (
        'le chemin Actions doit consulter le scan courant avant de refuser')
    #  la saisie manuelle garde la priorité (déclaration utilisateur)
    assert 'p.mid' in js.split('prixDuScan')[0] or "String(p.mid" in js


def test_le_refus_ne_reclame_plus_un_prix_deja_connu():
    js = _js()
    assert 'demande une quantité et un prix de référence. ' not in js, (
        'l\'ancien message exigeait un prix que la page promettait de lire')
    assert 'absent du scan courant' in js, (
        'le refus restant nomme la vraie cause : ni scan, ni saisie')


def test_la_provenance_du_prix_est_dite():
    assert 'prix du scan courant' in _js(), (
        'quand le prix vient du scan, la provenance est affichée')
