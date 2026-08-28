"""Lot 10 — l'autorité de conseil a UN nom : AdviceEngine.evaluate(snapshot).

Trois décideurs coexistaient sans hiérarchie déclarée : `decide.py` (verdicts
du scan, appelé par le monolithe), `skyler_core.decide` (le packet complet de
la fiche Analyse — score40, hard gates, scénarios, audit trail) et
`executive.decide` (Strategy OS). Le contrat du skill exige UNE autorité.

Ce lot la NOMME sans toucher une formule : `AdviceEngine.evaluate` est une
FAÇADE de délégation stricte vers le décideur du packet (skyler_core) — le
seul qui porte hard gates, audit trail et version de moteur. Les deux autres
sont déclarés producteurs de preuves ; leur unification SÉMANTIQUE changerait
des verdicts, et un verdict ne change que sur décision humaine.

Le banc tient trois propriétés :
1. la façade existe, avec la signature du contrat ;
2. elle DÉLÈGUE — même entrée, même sortie que le décideur du packet,
   au champ de provenance près ;
3. le résultat porte sa provenance (moteur + version) — un conseil sans
   version n'est pas auditable.
"""
from __future__ import annotations


def test_l_api_du_contrat_existe():
    from vertex.engines.advice import AdviceEngine
    assert hasattr(AdviceEngine, 'evaluate')


def test_evaluate_delegue_sans_changer_le_verdict():
    from vertex.engines import skyler_core as sk
    from vertex.engines.advice import AdviceEngine

    detail = {'score': 62, 'trend': 1.2, 'regime': 'TREND_UP', 'verdict': 'ACHETER',
              'series': {'close': [100 + i for i in range(60)]}}
    direct = sk.decide('TESTX', dict(detail))
    via = AdviceEngine.evaluate({'symbol': 'TESTX', 'detail': dict(detail)})
    #  les cles reelles du packet : verdict, score, gates, audit.
    for cle in ('decision', 'score', 'gates', 'audit_trail'):
        assert cle in via, 'AdviceResult ne porte pas %s' % cle
    assert via['decision'] == direct['decision'], (
        'la façade a CHANGÉ le verdict : %r != %r — la délégation doit être '
        'stricte, un verdict ne change que sur décision humaine.'
        % (via['decision'], direct['decision']))


def test_le_resultat_porte_sa_provenance():
    from vertex.engines.advice import AdviceEngine
    r = AdviceEngine.evaluate({'symbol': 'TESTX', 'detail': {'score': 50}})
    prov = r.get('advice_provenance') or {}
    assert prov.get('engine') and prov.get('version'), (
        'un conseil sans moteur ni version n\'est pas auditable.')


def test_un_snapshot_sans_symbole_rend_un_refus_jamais_un_verdict():
    from vertex.engines.advice import AdviceEngine
    r = AdviceEngine.evaluate({})
    assert r.get('decision') is None, (
        'sans symbole, la façade a fabriqué un verdict : %r' % r.get('decision'))


def test_un_detail_vide_delegue_le_refus_structure_au_decideur():
    """Le décideur du packet sait rendre « données insuffisantes » avec sa
    note READONLY et son audit — la façade ne le réinvente pas en plus
    pauvre (six bancs de fuzz épinglent cette forme)."""
    from vertex.engines.advice import AdviceEngine
    r = AdviceEngine.evaluate({'symbol': 'ZZZINCONNU', 'detail': {}})
    assert 'note' in r and 'audit_trail' in r, (
        'le refus structuré du décideur a été remplacé par un objet maigre.')
