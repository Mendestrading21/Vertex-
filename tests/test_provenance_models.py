"""tests/test_provenance_models.py — SKYLER LOT 113 : provenance figée.

Trou réel de couverture : vertex/data_sources/models.py — les TYPES
porteurs de provenance (ProvenancedValue.usable, missing(),
AnalyticsPacket) sur lesquels repose toute la couche données. Les
constantes sont importées partout, mais les comportements n'avaient
AUCUN test direct.
Caractérisations nées vertes (dites) — moteur INTACT.
engines/backtest déjà couvert (golden + honnêteté — dit).
"""
from vertex.data_sources import models as M


def test_missing_is_fully_honest_by_default():
    pv = M.missing()
    assert pv.value is None and pv.source == M.SOURCE_UNAVAILABLE
    assert pv.source_mode == M.MODE_NONE and pv.quality == M.QUALITY_MISSING
    assert pv.fallback_used is False and pv.usable is False
    named = M.missing('spot indisponible')
    assert named.warnings == ['spot indisponible']


def test_usable_requires_value_and_living_quality():
    for q in (M.QUALITY_FRESH, M.QUALITY_RECENT, M.QUALITY_STALE):
        assert M.ProvenancedValue(value=1.0, quality=q).usable is True, (
            'STALE reste utilisable — dégradé, pas mort')
    for q in (M.QUALITY_EXPIRED, M.QUALITY_MISSING):
        assert M.ProvenancedValue(value=1.0, quality=q).usable is False, q
    assert M.ProvenancedValue(value=None, quality=M.QUALITY_FRESH).usable is False, (
        'jamais utilisable sans valeur, même « fraîche »')


def test_zero_and_false_are_real_values_not_missing():
    assert M.ProvenancedValue(value=0.0, quality=M.QUALITY_FRESH).usable is True
    assert M.ProvenancedValue(value=False, quality=M.QUALITY_FRESH).usable is True, (
        'le piège falsy est évité : seul None signifie « pas de donnée »')


def test_to_dict_contract_is_complete():
    #  Lot 5 : l'enveloppe est portee au contrat canonique du skill — les huit
    #  champs historiques ne bougent pas, neuf champs s'ajoutent (unite,
    #  devise, identite d'instrument, observation/reception, entitlement,
    #  version de schema, lineage, erreur). Le set reste EXACT : un champ qui
    #  apparait sans passer par ce banc est une derive de schema.
    d = M.missing('n/d').to_dict()
    assert set(d) == {'value', 'source', 'source_mode', 'timestamp',
                      'age_seconds', 'quality', 'fallback_used', 'warnings',
                      'unit', 'currency', 'instrument_id', 'observed_at',
                      'received_at', 'entitlement', 'schema_version',
                      'lineage', 'error'}
    assert d['warnings'] == ['n/d']
    #  et aucun nouveau champ n'invente une valeur sur une absence :
    assert d['unit'] is None and d['currency'] is None and d['error'] is None


def test_warning_lists_are_never_shared_between_instances():
    a, b = M.missing('a'), M.missing()
    b.warnings.append('b')
    assert a.warnings == ['a'] and b.warnings == ['b'], (
        'default_factory : pas de liste mutable partagée entre valeurs')


def test_analytics_packet_starts_missing_with_five_source_families():
    p = M.AnalyticsPacket(symbol='TST')
    assert set(p.sources) == {'spot', 'history', 'fundamentals',
                              'catalysts', 'options'}
    assert p.quality == {'overall': M.QUALITY_MISSING, 'warnings': []}
    assert p.as_of.endswith('Z') and 'T' in p.as_of      # ISO UTC auto


def test_set_source_stores_a_plain_dict_snapshot():
    p = M.AnalyticsPacket(symbol='TST')
    p.set_source('spot', M.ProvenancedValue(value=101.5, source=M.SOURCE_IBKR,
                                            quality=M.QUALITY_FRESH))
    stored = p.sources['spot']
    assert isinstance(stored, dict) and stored['value'] == 101.5
    assert stored['source'] == 'IBKR'
    d = p.to_dict()
    assert set(d) == {'symbol', 'as_of', 'sources', 'quality'}


def test_packets_never_share_their_sources_dict():
    p1, p2 = M.AnalyticsPacket(symbol='A'), M.AnalyticsPacket(symbol='B')
    p1.sources['spot'] = {'value': 1}
    assert p2.sources['spot'] == {}, (
        'default_factory : chaque paquet a SES sources — aucun état partagé')
