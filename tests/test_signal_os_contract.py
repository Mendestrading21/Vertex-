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
    # La couche ne pose plus que des attributs sémantiques : elle LIT une valeur
    # déjà rendue (« S+ », « pessimiste ») et permet au CSS de la colorer.
    assert "normalizeGrades" in js and "normalizeDecisionCards" in js


def test_la_table_de_reecriture_est_fermee():
    """LA propriété finale, et elle est plus forte que la précédente.

    Tant que la table existait, ce test énumérait ses entrées mortes une par
    une — et il a fini par se prendre les pieds dedans : le commentaire qui
    EXPLIQUE la fermeture cite les libellés retirés. Une énumération de chaînes
    interdites interdit aussi qu'on écrive pourquoi on les a retirées.

    La table entière a disparu. On garde donc la STRUCTURE, pas les mots :
    plus de `Map` de libellés, plus de passe de remplacement de texte.
    """
    js = _read(JS)
    assert 'const COPY' not in js, (
        'une table de micro-copy est revenue dans la couche visuelle : le '
        'serveur et l\'écran recommenceraient à dire deux choses différentes.')
    assert 'replaceStaticCopy' not in js, (
        'la passe de remplacement de texte est de retour.')
    assert '.textContent =' not in js and '.textContent=' not in js, (
        'la couche visuelle réécrit de nouveau du texte dans le DOM.')


def test_les_libelles_migres_sont_bien_a_la_source():
    """Contrepartie du test ci-dessus : la table est fermée PARCE QUE chaque
    libellé a été écrit à sa source, pas parce qu'on a renoncé aux libellés."""
    pages = {
        'briefing.py': ('Signal du jour', 'Top opportunités'),
        'markets_page.py': ('Vue globale', 'Risque principal', 'Top hausses',
                            'Top baisses', 'Qualité des données', 'Sélection',
                            'Santé du marché'),
        'opportunities_page.py': ('Priorités', 'Dossiers à étudier',
                                  'Shortlist options', 'Qualité × timing'),
        'analysis_page.py': ('>Récents<', '<span>Recherche</span>',
                             '<span>Portefeuille</span>'),
        'portfolio_page.py': ("('watchlist', 'Surveillance')",
                              'Exposition, risque et prochaine décision.'),
        'options_intel_page.py': ("('positions', 'Positions')",
                                  "('events', 'Catalyseurs')"),
    }
    for fichier, libelles in pages.items():
        src = (ROOT / 'vertex/ui/pages' / fichier).read_text(encoding='utf-8')
        for libelle in libelles:
            assert libelle in src, (
                '« %s » n\'est pas écrit à la source dans %s — la table étant '
                'fermée, plus rien ne le corrige à l\'écran.' % (libelle, fichier))


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
