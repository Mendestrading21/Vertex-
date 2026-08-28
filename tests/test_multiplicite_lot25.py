"""tests/test_multiplicite_lot25.py — LOT 25 : correction de multiplicité.

Pipeline anti-illusion, point 10 : « corriger la multiplication des essais
et conserver les essais rejetés ». Le registre conservait les rejetés ;
la CORRECTION n'existait pas — 50 essais à α=5 % produisent ~2,5 faux
positifs, et rien ne le rappelait au moment de juger. Nés ROUGES.
"""
import pytest

from vertex.research.factory import Experiment
from vertex.research.registry import ExperimentRegistry


def test_le_registre_compte_tous_les_essais_y_compris_rejetes():
    r = ExperimentRegistry()
    a, b = Experiment('a'), Experiment('b')
    r.add(a); r.add(b)
    b.advance('REJECTED')
    assert r.n_essais() == 2, 'un essai rejeté reste un essai TENTÉ'


def test_seuil_bonferroni():
    from vertex.research import multiplicity as M
    assert M.seuil_corrige(0.05, 1) == 0.05
    assert M.seuil_corrige(0.05, 50) == 0.001
    with pytest.raises(ValueError):
        M.seuil_corrige(0.05, 0)


def test_verdict_honnete_sous_multiplicite():
    from vertex.research import multiplicity as M
    #  p=0.01 « significatif » seul, mais PAS après 50 essais
    seul = M.jugement(p_value=0.01, alpha=0.05, n_essais=1)
    multi = M.jugement(p_value=0.01, alpha=0.05, n_essais=50)
    assert seul['significatif'] is True
    assert multi['significatif'] is False
    assert multi['seuil_corrige'] == 0.001
    assert 'essais' in multi['note']
