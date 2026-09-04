"""CONTINUITY LOT 3 — gardiens de la couche de données (cache & SWR).

Cache client PERSISTANT (survit au reload), stale-while-revalidate, déduplication,
invalidation CIBLÉE, annulation anti-hors-ordre. Contrats statiques ; le comportement
runtime est validé au navigateur (le rapport de continuite 03 (archive, retiree du depot)).
"""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = (ROOT / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-core.js').read_text(encoding='utf-8')


def test_data_layer_public_api_present():
    for needle in ('VX.swr', 'VX.fetch.invalidate', 'VX.fetch.peek'):
        assert needle in CORE, needle


def test_cache_is_persistent_across_reload():
    """Le cache s'archive dans sessionStorage et se réhydrate au démarrage."""
    assert "sessionStorage" in CORE
    assert "vxDataCache" in CORE
    assert "function hydrate" in CORE          # réhydratation au boot


def test_persistence_bounds_large_payloads():
    """Les gros payloads (ex. /scan ~8 Mo) ne sont PAS archivés (quota sessionStorage)."""
    assert "PERSIST_MAX_ENTRY" in CORE
    assert "PERSIST_MAX" in CORE


def test_stale_while_revalidate_semantics():
    """VX.swr : rend le cache d'abord, revalide en fond, jamais de vide sur erreur."""
    assert "VX.swr" in CORE
    assert "stale" in CORE
    # garde l'ancien contenu sur erreur (jamais remplacer du valide par du vide)
    assert ".catch(() => {" in CORE or "catch(() => {" in CORE


def test_out_of_order_protection_via_cancel():
    """L'annulateur (alive) empêche une réponse obsolète d'écraser l'affichage."""
    assert "let alive = true" in CORE
    assert "if (!alive) return" in CORE
    assert "function cancel()" in CORE


def test_targeted_invalidation_not_blind_clear():
    """Invalidation par clé/préfixe/prédicat ; le refresh explicite passe par là."""
    assert "VX.fetch.invalidate = function" in CORE
    assert "VX.fetch.invalidate()" in CORE      # runAll utilise l'invalidation, pas cache.clear()


def test_inflight_dedup_preserved():
    """La déduplication in-flight (une requête identique ne part pas deux fois) demeure."""
    assert "inflight" in CORE
    assert "inflight.has(url)" in CORE
