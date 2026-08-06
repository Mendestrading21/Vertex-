"""tests/test_offline_lot82.py — SKYLER LOT 82 : offline/service worker.

Défaut réel trouvé par le scénario offline Playwright : le service worker
n'était enregistré QUE par les pages legacy de terminal.py — le shell
canonique (les 8 espaces) ne l'enregistrait JAMAIS (registration absente,
0 précache, offline = page d'erreur navigateur). Corrigé PAR la source :
le shell enregistre /sw.js au load (même idiome que les pages legacy).
Preuve APRÈS : SW actif + précache td-shell-v127 rempli (polices
incluses) + rechargement OFFLINE rendu depuis le cache.
Shell visible → SW v126 → v127.
"""
import re


def test_shell_registers_service_worker():
    # L'enregistrement vit dans vx-shell.js (externe — pas de <script> inline,
    # le gardien anti-reflet du fuzz lot 43 interdit toute balise script nue).
    js = open('vertex/static/vertex/js/vx-shell.js', encoding='utf-8').read()
    assert "serviceWorker" in js and "register('/sw.js')" in js, (
        'le shell canonique doit enregistrer le service worker '
        '(sinon aucun offline/précache sur les 8 espaces)')
    shell = open('vertex/ui/shell/__init__.py', encoding='utf-8').read()
    assert '/static/vertex/js/vx-shell.js' in shell


def test_service_worker_bumped_to_at_least_v127():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 127
    assert 'td-shell-v126' not in body
