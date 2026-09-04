"""
LOT 166 — Caractérisation de la couche IA optionnelle
(`vertex/ai/briefs.py` — traduction FR des news + mini-profils ;
dégradation propre sans clé). Tout est testé HORS LIGNE :
`_google_fr` est monkeypatché selon son contrat (« None si échec »),
aucun appel Anthropic ni Google réel.

Ces tests figent la détection de clé, l'ordre de dégradation et le
cache — les changer devient une décision explicite.
"""

import pytest

from vertex.ai import briefs


@pytest.fixture()
def _no_key(monkeypatch):
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)


# ── available : la clé doit être RÉELLE ──────────────────────────────────────

def test_available_rejette_absence_placeholder_et_mauvais_prefixe(monkeypatch):
    monkeypatch.delenv('ANTHROPIC_API_KEY', raising=False)
    assert briefs.available() is False
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-ant-xxxxxxxx')   # placeholder
    assert briefs.available() is False
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'autre-format')      # mauvais préfixe
    assert briefs.available() is False


def test_available_vraie_forme_acceptee(monkeypatch):
    monkeypatch.setenv('ANTHROPIC_API_KEY', 'sk-ant-abc123reel')
    assert briefs.available() is (briefs.Anthropic is not None)


# ── fr_news sans clé : repli Google + honnêteté ──────────────────────────────

def test_fr_news_repli_google_et_cache(_no_key, monkeypatch):
    calls = []
    monkeypatch.setattr(briefs, '_google_fr',
                        lambda t: calls.append(t) or 'Titre un FR\nTitre deux FR')
    items = [{'title': 'Title one'}, {'title': 'Title two'}]
    out, why = briefs.fr_news('L166A', items)
    assert [i['fr'] for i in out] == ['Titre un FR', 'Titre deux FR']
    assert why is None and len(calls) == 1
    # CACHE : mêmes titres → aucun second appel réseau.
    out2, _ = briefs.fr_news('L166A', [{'title': 'Title one'}, {'title': 'Title two'}])
    assert [i['fr'] for i in out2] == ['Titre un FR', 'Titre deux FR']
    assert len(calls) == 1


def test_fr_news_desalignement_de_lignes_titres_d_origine(_no_key, monkeypatch):
    # Google renvoie 1 ligne pour 2 titres : appariement impossible →
    # on garde les titres ANGLAIS d'origine (fidélité > traduction).
    monkeypatch.setattr(briefs, '_google_fr', lambda t: 'Une seule ligne')
    out, _ = briefs.fr_news('L166B', [{'title': 'Alpha'}, {'title': 'Beta'}])
    assert [i['fr'] for i in out] == ['Alpha', 'Beta']


def test_fr_news_echec_reseau_titres_d_origine(_no_key, monkeypatch):
    monkeypatch.setattr(briefs, '_google_fr', lambda t: None)   # contrat : None si échec
    out, why = briefs.fr_news('L166C', [{'title': 'Gamma'}])
    assert out[0]['fr'] == 'Gamma' and why is None


def test_fr_news_liste_vide_intacte(_no_key):
    assert briefs.fr_news('L166D', []) == ([], None)


# ── company_brief : dégradation propre → {} ──────────────────────────────────

def test_company_brief_sans_resume_ou_sans_cle_dict_vide(_no_key):
    assert briefs.company_brief('X', '') == {}
    assert briefs.company_brief('X', 'Une description factuelle.') == {}


# ── fr_label / fr_desc : ordre de dégradation et cache ───────────────────────

def test_fr_label_traduit_cache_et_replis(_no_key, monkeypatch):
    calls = []
    monkeypatch.setattr(briefs, '_google_fr',
                        lambda t: calls.append(t) or 'Technologie')
    assert briefs.fr_label('L166-Technology') == 'Technologie'
    assert briefs.fr_label('L166-Technology') == 'Technologie'   # caché
    assert len(calls) == 1
    monkeypatch.setattr(briefs, '_google_fr', lambda t: None)
    assert briefs.fr_label('L166-Health Care') == 'L166-Health Care'  # échec → origine
    assert briefs.fr_label('') == ''                                  # vide intact


def test_fr_desc_google_ok_puis_echec_texte_d_origine(_no_key, monkeypatch):
    monkeypatch.setattr(briefs, '_google_fr', lambda t: 'Description traduite.')
    assert briefs.fr_desc('L166E', 'Original description.') == 'Description traduite.'
    monkeypatch.setattr(briefs, '_google_fr', lambda t: None)
    assert briefs.fr_desc('L166F', 'Original again.') == 'Original again.'
    assert briefs.fr_desc('L166G', '') == ''                          # vide intact


def test_google_fr_texte_vide_none():
    assert briefs._google_fr('') is None
