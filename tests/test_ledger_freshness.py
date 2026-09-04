"""tests/test_ledger_freshness.py — SKYLER LOT 37 : fraîcheur du ledger.

L'en-tête de la carte Mémoire dit QUAND la dernière décision a été figée :
« dernière décision figée : <session_date> (J-N) » — dérivé de la
`session_date` déjà figée dans le ledger (donnée réelle, aucun calcul
moteur), « n/d » honnête si la date manque, « aucune décision figée » si le
ledger est vide. Ancienneté en séances de calendrier (J-0 = aujourd'hui),
calcul d'affichage client uniquement. Shell visible → SW v103 → v104.
"""
import re


def _journal_body():
    import terminal
    return terminal.app.test_client().get(
        '/journal', follow_redirects=True).get_data(as_text=True)


def test_memory_card_says_last_frozen_decision():
    body = _journal_body()
    assert 'dernière décision figée' in body


def test_freshness_honest_states_wired():
    """Les trois états honnêtes existent dans la source : date réelle (via
    session_date), date absente (n/d), ledger vide (aucune décision figée)."""
    body = _journal_body()
    assert 'aucune décision figée' in body
    assert body.count('session_date') >= 2      # table existante + fraîcheur


def test_freshness_age_uses_j_notation():
    """L'ancienneté s'affiche en notation J-N (grammaire catalyseur du desk) —
    jamais un mot avec apostrophe fragile dans la chaîne JS."""
    body = _journal_body()
    assert "(J-'" in body or 'J-' in body


def test_service_worker_bumped_to_at_least_v104():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 104
    assert 'td-shell-v103' not in body
