"""PRF-02 — fraîcheur & environnement des caches (aucune valeur périmée servie comme live).

Le seul cache PERSISTÉ sur disque est le profil entreprise (`company_cache.json`). C'est la
surface d'intégrité critique : il ne doit JAMAIS mélanger démo (synthétique/curé) et réel, et
sa décision de fraîcheur doit inclure TOUTES les entrées pertinentes (âge ET version de schéma),
avec un drapeau `stale` honnête (règles produit n°3/4/7).

Ce gardien verrouille :
1. la démo n'ÉCRIT jamais dans le cache réel (pas de fallback mock persisté en silence) ;
2. `stale` reflète honnêtement âge > 7 j ET désynchro de schéma (clé de fraîcheur complète) ;
3. une entrée réelle fraîche est servie `stale=False`.

(Les caches EN MÉMOIRE — yfinance/options/scan — sont process-scopés, mono-environnement, avec
un TTL qui se resserre en séance : `_YF_TTL_OPEN < _YF_TTL_CLOSED` → l'ouverture force du frais.)

Régression (démo qui persiste, schéma hors clé, `stale` figé) = test rouge.
"""
import json
import time

import pytest

from vertex.data import company


@pytest.fixture
def temp_cache(tmp_path, monkeypatch):
    """Redirige le cache disque vers un fichier temporaire isolé."""
    p = tmp_path / 'company_cache.json'
    monkeypatch.setattr(company, '_CACHE', str(p))
    return p


def _seed(path, sym, **entry):
    path.write_text(json.dumps({sym: entry}), encoding='utf-8')


# ── 1. la démo ne persiste JAMAIS dans le cache réel ───────────────────────
def test_demo_n_ecrit_jamais_dans_le_cache(temp_cache):
    assert not temp_cache.exists()
    out = company.get('NVDA', demo=True)          # aucun réseau, aucune écriture
    assert not temp_cache.exists(), 'la démo a écrit dans le cache entreprise réel'
    # secours curé servi, mais étiqueté périmé (jamais présenté comme frais)
    assert out['stale'] is True
    assert out['name'] or out['activity']         # pas de page vide


def test_demo_ne_reecrit_pas_une_entree_reelle_existante(temp_cache):
    _seed(temp_cache, 'NVDA', ts=time.time(), _v=company._SCHEMA_V, name='NVIDIA', sector='Technology')
    before = temp_cache.read_text(encoding='utf-8')
    company.get('NVDA', demo=True)
    assert temp_cache.read_text(encoding='utf-8') == before, 'la démo a muté le cache réel'


# ── 2. le drapeau `stale` est honnête : âge ET schéma dans la clé de fraîcheur ──
def test_entree_fraiche_du_bon_schema_est_non_stale(temp_cache):
    _seed(temp_cache, 'NVDA', ts=time.time(), _v=company._SCHEMA_V, name='NVIDIA')
    assert company.get('NVDA', demo=True)['stale'] is False


def test_entree_trop_vieille_est_stale(temp_cache):
    _seed(temp_cache, 'NVDA', ts=time.time() - 8 * 24 * 3600, _v=company._SCHEMA_V, name='NVIDIA')
    assert company.get('NVDA', demo=True)['stale'] is True


def test_schema_perime_force_stale_meme_si_recent(temp_cache):
    # entrée récente MAIS d'un schéma antérieur → la version DOIT compter dans la fraîcheur.
    _seed(temp_cache, 'NVDA', ts=time.time(), _v=company._SCHEMA_V - 1, name='NVIDIA')
    assert company.get('NVDA', demo=True)['stale'] is True


# ── 3. cohérence TTL des caches marché en mémoire (resserrement en séance) ──
def test_ttl_marche_se_resserre_en_seance():
    from terminal import _YF_TTL_OPEN, _YF_TTL_CLOSED
    assert _YF_TTL_OPEN < _YF_TTL_CLOSED, (
        'le TTL en séance doit être plus court qu\'hors séance, sinon une barre figée '
        'pourrait être servie comme fraîche à l\'ouverture')
