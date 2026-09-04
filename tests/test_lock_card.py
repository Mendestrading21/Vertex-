"""SKYLER LOT 283 — gardien de la carte « Verrou d'accès » (Système).

Contexte : le bouton « Se déconnecter & verrouiller » ne vivait que dans
PAGE_SETTINGS, page héritée jamais routée (preuves lots 248/259) — aucun
utilisateur ne pouvait verrouiller son desk depuis l'UI. La carte du lot
283 est le SEUL point de verrouillage atteignable : ce gardien fige son
contrat dans les deux états du verrou.
"""
from vertex.ui.pages import system_page


def test_lock_card_active_offers_logout():
    """Verrou actif → bouton /logout + faits exacts (30 j, anti-force-brute)."""
    html = system_page._lock_card(True)
    assert 'href="/logout"' in html
    assert 'id="vx-lock-btn"' in html
    assert 'verrouiller' in html
    assert '30 jours' in html and 'anti-force-brute' in html
    assert '>actif<' in html


def test_lock_card_inactive_is_honest_without_button():
    """Sans code : état honnête (repli 127.0.0.1, VERTEX_CODE) et PAS de bouton."""
    html = system_page._lock_card(False)
    assert '/logout' not in html
    assert '127.0.0.1' in html
    assert 'VERTEX_CODE' in html
    assert '>inactif<' in html


def test_system_page_renders_lock_card_and_no_leftover_placeholder():
    """La vue Connexions porte la carte ; le placeholder est consommé."""
    html = system_page.render('connections')
    assert 'Verrou d' in html and 'vx-lock-badge' in html
    assert '%%LOCKCARD%%' not in html
    # Les autres vues ne portent pas la carte (domicile unique : Connexions).
    assert 'vx-lock-badge' not in system_page.render('data')
