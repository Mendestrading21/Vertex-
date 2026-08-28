"""tests/test_replay_conseil_lot28.py — contrôle 074 : replay outillé.

La provenance du conseil existait (engine/version/via) mais AUCUN
mécanisme ne permettait de rejouer un conseil depuis son snapshot et de
prouver la reproduction. Cible : empreinte d'entrée dans la provenance +
`rejouer(snapshot, conseil)` qui vérifie l'empreinte ET la reproduction
champ par champ. Nés ROUGES.
"""
import copy

from vertex.engines.advice import AdviceEngine, empreinte_snapshot, rejouer

SNAP = {'symbol': 'TST', 'detail': {'price': 100.0, 'score': 50}}


def test_l_empreinte_d_entree_est_dans_la_provenance():
    c = AdviceEngine().evaluate(SNAP)
    emp = c['advice_provenance'].get('snapshot_fingerprint')
    assert emp == empreinte_snapshot(SNAP)
    assert len(emp) == 64


def test_rejouer_reproduit_bit_identique():
    c = AdviceEngine().evaluate(SNAP)
    r = rejouer(SNAP, c)
    assert r['identique'] is True
    assert r['empreinte_verifiee'] is True
    assert r['differences'] == []


def test_rejouer_refuse_un_snapshot_qui_ne_correspond_pas_au_conseil():
    c = AdviceEngine().evaluate(SNAP)
    autre = {'symbol': 'TST', 'detail': {'price': 999.0, 'score': 50}}
    r = rejouer(autre, c)
    assert r['empreinte_verifiee'] is False, (
        'le conseil enregistré ne vient PAS de ce snapshot — le dire')


def test_rejouer_detecte_un_conseil_altere():
    c = AdviceEngine().evaluate(SNAP)
    trafique = copy.deepcopy(c)
    trafique['note'] = 'ACHETER TOUT'          # altération
    r = rejouer(SNAP, trafique)
    assert r['identique'] is False
    assert any('note' in d for d in r['differences'])
