"""tests/test_ui_memory_graph_lot16.py — SKYLER LOT 16 : surfaçage UI.

La mémoire décisionnelle (lot 10) et le knowledge graph (lot 11) deviennent
visibles : carte « Mémoire décisionnelle » sur la vue Performance (à côté de
la calibration) et section « Dépendances cachées » sur Portefeuille → Risque.
Shell visible modifié → service worker bumpé v94 → v95 (gardiens mis à jour).
États empty/error honnêtes ; aucune donnée inventée côté client.
"""


def _body(path):
    import terminal
    return terminal.app.test_client().get(path, follow_redirects=True).get_data(as_text=True)


# ─── Carte Mémoire décisionnelle (Performance) ──────────────────────────────────

def test_performance_page_has_memory_card():
    body = _body('/journal')
    assert 'vx-pf-memory' in body
    assert 'loadMemory' in body
    assert 'Mémoire décisionnelle' in body or 'M&eacute;moire d&eacute;cisionnelle' in body
    assert '/api/skyler/memory' in body


def test_memory_card_keeps_calibration_card():
    """La mémoire s'AJOUTE — la carte Calibration (lot 8e) reste intacte."""
    body = _body('/journal')
    assert 'vx-pf-calibration' in body
    assert 'loadCalibration' in body


def test_memory_card_honest_states():
    body = _body('/journal')
    assert 'Aucune décision figée' in body        # état vide honnête
    assert 'biais' in body.lower()


# ─── Dépendances cachées (Portefeuille → Risque) ────────────────────────────────

def test_portfolio_risk_view_has_hidden_deps_section():
    body = _body('/portfolio?view=risk')
    assert 'renderHiddenDeps' in body
    assert '/api/skyler/graph' in body
    assert 'Dépendances cachées' in body or 'D&eacute;pendances cach&eacute;es' in body


def test_hidden_deps_only_on_portfolio_not_today():
    """Une donnée = un seul domicile : Aujourd'hui ne charge pas le graphe."""
    body = _body('/')
    assert '/api/skyler/graph' not in body


# ─── Service worker : shell visible changé → bump ≥ v95 (prospectif) ────────────

def test_service_worker_bumped_to_at_least_v95():
    import re
    body = _body('/sw.js')
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 95
    #  Le numero doit avoir DEPASSE v94, pas rester dessus. Ecrire ici la
    #  version COURANTE viderait l'assertion de sens a chaque bump.
    assert 'td-shell-v94' not in body
