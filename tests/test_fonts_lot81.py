"""tests/test_fonts_lot81.py — SKYLER LOT 81 : polices auto-hébergées.

Constat du lot 80 : Inter + JetBrains Mono chargées depuis
fonts.googleapis.com (shell + pages legacy de terminal.py) — offline en
polices système, ping Google à chaque chargement. Corrigé : fichiers
VARIABLES woff2 locaux (un seul par famille, subset latin, ~80 kB au
total) + `fonts.css` @font-face local + remplacement de toutes les
références CDN. Preuve navigateur : 0 requête externe au chargement.
Shell visible → SW v125 → v126.
"""
import os
import re


def _servable_sources():
    yield 'terminal.py'
    for root, dirs, files in os.walk('vertex/ui'):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f.endswith('.py'):
                yield os.path.join(root, f)


def test_no_google_fonts_reference_anywhere():
    offenders = []
    for p in _servable_sources():
        src = open(p, encoding='utf-8', errors='ignore').read()
        if 'fonts.googleapis' in src or 'fonts.gstatic' in src:
            offenders.append(p)
    assert not offenders, f'références CDN Google restantes : {offenders}'


def test_local_fonts_shipped():
    assert os.path.getsize('vertex/static/vertex/fonts/inter-var.woff2') > 10000
    assert os.path.getsize('vertex/static/vertex/fonts/jetbrains-mono-var.woff2') > 10000
    css = open('vertex/static/vertex/css/fonts.css', encoding='utf-8').read()
    assert '/static/vertex/fonts/inter-var.woff2' in css
    assert '/static/vertex/fonts/jetbrains-mono-var.woff2' in css
    assert 'font-display: swap' in css
    assert 'https://' not in css, 'fonts.css doit être 100 % local'


def test_shell_links_local_fonts_css():
    #  Lot 30 : fonts.css entre dans le bundle agrégé — PREMIÈRE de la
    #  cascade (les @font-face avant tout consommateur). Toujours locale.
    from vertex.ui.shell import CSS_ORDER
    assert CSS_ORDER[0] == 'fonts.css'


def test_service_worker_bumped_to_at_least_v126():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 126
    assert 'td-shell-v125' not in body
