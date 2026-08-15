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
SHELL = ROOT / "vertex/ui/shell/__init__.py"


def _read(path: Path) -> str:
    assert path.is_file(), f"Fichier Signal OS manquant: {path.relative_to(ROOT)}"
    return path.read_text(encoding="utf-8")


def test_signal_os_assets_are_loaded_globally_after_the_historical_theme():
    """La propriété n'a pas changé — le mécanisme, si.

    Signal OS arrivait par `loadSignalOS()` dans `live-updates.js` : un `<link>`
    créé en JS et injecté à l'exécution. Le document se peignait donc une fois
    SANS la feuille (flash de l'ancien thème à chaque navigation complète), le
    service worker ne la voyait pas dans le HTML de shell qu'il met en cache, et
    l'ordre de cascade dépendait du moment où le script s'exécutait plutôt que de
    la position dans le `<head>`.

    Ce test garde donc la même chose — chargé globalement, APRÈS la couche
    historique — mais là où elle est désormais vraie : dans le shell.
    """
    shell = _read(SHELL)
    assert '<link rel="stylesheet" href="/static/vertex/css/signal-os.css">' in shell, (
        'la feuille Signal OS n\'est plus déclarée dans le shell : elle ne '
        'couvre plus les huit espaces.')
    assert '/static/vertex/js/signal-os.js' in shell
    assert shell.index('neon-glass.css') < shell.index('signal-os.css'), (
        'Signal OS passe AVANT la couche historique : la cascade s\'inverse et '
        'neon-glass.css reprend la main sur la nouvelle identité.')
    live = _read(LIVE)
    assert 'appendChild(css)' not in live, (
        'l\'injection à l\'exécution est revenue dans live-updates.js — flash de '
        'l\'ancien thème, et la feuille sort du contrat de cache du shell.')


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
    # Pages NON encore reconstruites : leur micro-copy passe encore par la table.
    assert "Exposition, risque et prochaine décision." in js
    assert "Convexité, volatilité et risque événementiel." in js


def test_la_copy_des_pages_reconstruites_a_quitte_la_table():
    """La table de réécriture est une MIGRATION, pas une architecture.

    Tant qu'un libellé y figure, il existe deux fois : dans les octets servis et
    à l'écran. Ce test vérifie que les pages déjà reconstruites — shell,
    Aujourd'hui — écrivent le leur à la source ET ne le réécrivent plus après
    coup. Sans lui, la table ne rétrécirait jamais.
    """
    js = _read(JS)
    brief = (ROOT / 'vertex/ui/pages/briefing.py').read_text(encoding='utf-8')
    for libelle in ('Signal du jour', 'Top opportunités'):
        assert libelle in brief, (
            '« %s » n\'est plus écrit à la source dans briefing.py' % libelle)
        assert libelle not in js, (
            '« %s » est revenu dans la table de réécriture : le serveur et '
            'l\'écran ne diraient plus la même chose.' % libelle)
    for mort in ('Brief Vertex', 'Meilleures opportunités',
                 'Depuis ta dernière visite'):
        assert mort not in js, (
            'entrée « %s » toujours dans la table alors qu\'Aujourd\'hui est '
            'reconstruite.' % mort)


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
