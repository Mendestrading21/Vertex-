"""tests/test_a11y_lot73.py — SKYLER LOT 73 : accessibilité, angles restants.

Balayage outillé des 8 pages (noms accessibles, labels d'inputs,
focusabilité des contrôles) : 7 pages à 0 défaut ; 4 défauts réels sur
/opportunities — les tickers cliquables (`span.sym vx-ticker` avec
data-open-analysis) n'étaient PAS focusables au clavier, et la délégation
globale de vx-entities.js n'écoutait que `click` (aucune activation
Enter/Espace possible).

Corrigé : role="button" + tabindex="0" sur les tickers cliquables
d'Opportunités + délégation clavier globale (Enter/Espace) dans
vx-entities.js pour TOUT [data-open-analysis]/[data-entity-menu] —
prospectif, couvre les usages futurs. Shell visible → SW v123 → v124.
"""
import re

PAGE = 'vertex/ui/pages/opportunities_page.py'
ENT = 'vertex/static/vertex/js/vx-entities.js'


def test_clickable_tickers_are_keyboard_focusable():
    src = open(PAGE, encoding='utf-8').read()
    offenders = [l for l in src.splitlines()
                 if 'data-open-analysis' in l and 'vx-ticker' in l
                 and 'tabindex' not in l]
    assert not offenders, (
        'tickers cliquables non focusables (tabindex manquant) : '
        + ' | '.join(o.strip()[:80] for o in offenders))


def test_entities_delegate_handles_keyboard():
    src = open(ENT, encoding='utf-8').read()
    assert "document.addEventListener('keydown'" in src, (
        'délégation clavier au niveau document requise (Enter/Espace)')
    seg = src[src.index("document.addEventListener('keydown'"):]
    seg = seg[:seg.index('});') + 3]
    assert 'data-open-analysis' in seg and 'Enter' in seg, (
        'le délégué clavier doit activer les contrôles data-open-analysis')


def test_service_worker_bumped_to_at_least_v124():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 124
    assert 'td-shell-v123' not in body
