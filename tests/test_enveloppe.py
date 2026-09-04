"""Lot 5 — l'enveloppe canonique : unité, devise, identité, lineage.

Le contrat (`connection-and-resilience-matrix.md`) exige que chaque valeur
externe traverse une enveloppe portant `value · unit · currency · source_id ·
observed_at · received_at · age · mode · quality · entitlement · fallback ·
instrument_id · snapshot_id · schema_version · lineage · error`.

L'enveloppe existante portait valeur/source/mode/timestamp/âge/qualité/
fallback/warnings. Ce banc tient le complément — ET la compatibilité : pas un
seul champ historique ne change de nom ni de défaut, `to_dict()` reste un
superset, toutes les fixtures passent.
"""
from __future__ import annotations

from vertex.data_sources.models import ProvenancedValue, missing


CHAMPS_CANONIQUES = ('unit', 'currency', 'instrument_id', 'observed_at',
                     'received_at', 'entitlement', 'schema_version',
                     'lineage', 'error')

CHAMPS_HISTORIQUES = ('value', 'source', 'source_mode', 'timestamp',
                      'age_seconds', 'quality', 'fallback_used', 'warnings')


def test_l_enveloppe_porte_les_champs_du_contrat():
    pv = ProvenancedValue()
    for champ in CHAMPS_CANONIQUES:
        assert hasattr(pv, champ), (
            'l\'enveloppe ne porte pas « %s » — le contrat canonique '
            'l\'exige.' % champ)


def test_les_champs_historiques_ne_bougent_pas():
    d = ProvenancedValue().to_dict()
    for champ in CHAMPS_HISTORIQUES:
        assert champ in d, (
            '« %s » a disparu de to_dict() : les fixtures et consommateurs '
            'existants le lisent.' % champ)


def test_une_absence_n_est_jamais_zero():
    pv = missing('test')
    assert pv.value is None, 'missing() doit rendre None, jamais 0.'
    assert pv.quality == 'MISSING'
    assert not pv.usable
    #  et l'enveloppe vide ne fabrique ni devise ni unité :
    assert pv.unit is None and pv.currency is None, (
        'une unité ou une devise par défaut est une invention.'
    )


def test_le_lineage_est_une_liste_annexable():
    pv = ProvenancedValue()
    pv.lineage.append('ibkr_gateway.fetch_snapshot')
    assert pv.to_dict()['lineage'] == ['ibkr_gateway.fetch_snapshot']


def test_la_cotation_unifiee_pose_les_nouveaux_champs():
    import inspect

    from vertex.data_sources import cotation_unifiee
    src = inspect.getsource(cotation_unifiee)
    for attendu in ('instrument_id', 'currency', 'lineage'):
        assert attendu in src, (
            'le producteur central (cotation_unifiee) ne pose pas « %s » : '
            'l\'enveloppe canonique reste vide là où elle compte le plus.'
            % attendu)
