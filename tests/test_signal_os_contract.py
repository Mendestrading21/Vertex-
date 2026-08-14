"""Gardiens de la migration visuelle Vertex Signal OS.

Ces tests ne figent pas des pixels. Ils protègent les invariants produit :
chargement global, couverture des huit espaces, palette sémantique, absence de
réseau dans la couche de micro-copy et purge du cache PWA après changement.
"""
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "vertex/static/vertex/css/signal-os.css"
JS = ROOT / "vertex/static/vertex/js/signal-os.js"
LIVE = ROOT / "vertex/static/vertex/js/live-updates.js"
SYSTEM = ROOT / "vertex/app/routes/system.py"
DOC = ROOT / "docs/design/VERTEX_SIGNAL_OS.md"


def _read(path: Path) -> str:
    assert path.is_file(), f"Fichier Signal OS manquant: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def test_signal_os_assets_are_loaded_globally_after_the_historical_theme():
    live = _read(LIVE)
    assert "/static/vertex/css/signal-os.css" in live
    assert "/static/vertex/js/signal-os.js" in live
    assert "appendChild(css)" in live
    assert "appendChild(js)" in live
    assert live.index("signal-os.css") < live.index("appendChild(css)")


def test_signal_os_covers_all_eight_canonical_spaces():
    css = _read(CSS)
    for space in (
        "briefing",
        "markets",
        "opportunities",
        "analysis",
        "portfolio",
        "options",
        "journal",
        "system",
    ):
        assert f'[data-space="{space}"]' in css, f"Espace non couvert: {space}"


def test_signal_os_keeps_one_color_one_meaning_contract():
    css = _read(CSS)
    assert "--vx-brand:var(--vx-option)" in css
    assert "var(--vx-positive)" in css
    assert "var(--vx-negative)" in css
    assert "var(--vx-warning)" in css
    assert "var(--vx-info-soft)" in css
    assert '[data-grade="S+"]' in css
    assert '[data-grade="S"]' in css
    assert '[data-grade="A"]' in css
    assert '[data-grade="B"]' in css


def test_signal_os_copy_layer_is_local_and_read_only():
    js = _read(JS)
    forbidden = ("fetch(", "XMLHttpRequest", "EventSource", ".submit(", "sendBeacon")
    for token in forbidden:
        assert token not in js, f"La couche visuelle ne doit pas faire de réseau: {token}"
    assert "Signal du jour" in js
    assert "Top opportunités" in js
    assert "Exposition, risque et prochaine décision." in js
    assert "Convexité, volatilité et risque événementiel." in js


def test_signal_os_uses_no_external_asset_or_import():
    css = _read(CSS)
    js = _read(JS)
    combined = css + "\n" + js
    assert "@import" not in css
    assert "http://" not in combined
    assert "https://" not in combined


def test_pwa_cache_is_bumped_for_signal_os_assets():
    system = _read(SYSTEM)
    match = re.search(r"const CACHE='td-shell-v(\d+)'", system)
    assert match, "Version du cache PWA introuvable"
    assert int(match.group(1)) >= 188, (
        "Tout octet servi modifié exige un bump du cache PWA; "
        f"version actuelle: v{match.group(1)}"
    )


def test_design_contract_documents_the_decision_hierarchy():
    doc = _read(DOC)
    for phrase in (
        "Quel est le signal ?",
        "Quelles preuves le soutiennent ?",
        "Quel est le risque maximal ?",
        "scénario pessimiste",
        "scénario probable",
        "scénario exceptionnel",
        "Lecture seule",
    ):
        assert phrase.lower() in doc.lower()
