"""tests/test_catalyst_type_ui_lot33.py — SKYLER LOT 33 : by_catalyst_type en UI.

La carte Mémoire (page Performance, /journal) surface les découpes
d'OBSERVATION `by_catalyst` et `by_catalyst_type` avec la MÊME mécanique de
badges que les cellules niveau/régime/décision (lot 26) — et le libellé de
la section DIT que ces découpes sont de l'observation (jamais consommées
par la sélection niveau → régime → global). Shell visible → SW v101 → v102.
"""
import re


def _journal_body():
    import terminal
    return terminal.app.test_client().get(
        '/journal', follow_redirects=True).get_data(as_text=True)


def test_memory_card_renders_catalyst_observation_groups():
    body = _journal_body()
    assert 'by_catalyst_type' in body
    assert "'by_catalyst'" in body or '"by_catalyst"' in body


def test_context_section_says_observation():
    """Le libellé de la section calibration par contexte dit que les découpes
    catalyseur/type sont de l'OBSERVATION — jamais vendues comme des règles."""
    body = _journal_body()
    assert 'observation' in body


def test_same_badge_mechanic_no_new_renderer():
    """Pas de second moteur de rendu : les nouvelles découpes passent par la
    même boucle de badges (un seul littéral `calibration_by_context`)."""
    body = _journal_body()
    assert body.count('calibration_by_context') == 1


def test_service_worker_bumped_to_at_least_v102():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 102
    assert 'td-shell-v101' not in body
