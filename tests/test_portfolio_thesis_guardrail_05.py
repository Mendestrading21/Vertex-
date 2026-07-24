"""tests/test_portfolio_thesis_guardrail_05.py — PR n°5 (gardiens Portefeuille).

Verrouille les invariants produit de la refonte Portefeuille :
  · GARDE-FOU PERDANTS (Constitution §18) : jamais « renforcer » un perdant sans
    confirmation positive explicite ; message d'interdiction présent.
  · État de thèse honnête : « cassée » vient du franchissement de l'invalidation,
    jamais d'une simple baisse ; six états dont « données insuffisantes ».
  · Gestion des gagnants indicative (§19) : paliers +20/+50/+100, jamais de sortie
    automatique.
  · READONLY absolu : aucun bouton d'exécution d'ordre dans la page.
  · Migration performance Journal → Portefeuille (un seul domicile, §6).
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as fh:
        return fh.read()


PF = 'vertex/ui/pages/portfolio_page.py'
JR = 'vertex/ui/pages/performance_page.py'


# ── Garde-fou perdants (LOT D — le test gardien exigé) ───────────────────
def test_loser_reinforcement_forbidden_message_present():
    src = _read(PF)
    assert 'Renforcement interdit : aucune confirmation positive détectée' in src, \
        'le message d’interdiction du renforcement d’un perdant doit exister'


def test_loser_reinforcement_gated_on_positive_confirmation():
    """Un perdant ne peut recevoir « renforcer » que via une confirmation explicite."""
    src = _read(PF)
    assert 'hasPositiveConfirmation' in src
    # la confirmation vient de faits explicites du snapshot, jamais du prix/P&L
    assert 'nextAction' in src
    # dans nextAction, la branche perte interdit le renforcement sans confirmation
    idx = src.find('function nextAction')
    assert idx != -1
    body = src[idx:idx + 900]
    assert 'hasPositiveConfirmation' in body and 'Renforcement interdit' in body


def test_no_naive_reinforce_suggestion_on_price_drop():
    """Aucune suggestion « renforcer » déclenchée par une simple baisse de prix."""
    src = _read(PF).lower()
    # aucune formule encourageant à renforcer une perte
    assert 'renforcer la perte' not in src
    assert 'moyenner à la baisse' not in src


# ── État de thèse honnête (LOT B) ────────────────────────────────────────
def test_thesis_state_from_invalidation_not_price_drop():
    src = _read(PF)
    assert 'function thesisState' in src
    idx = src.find('function thesisState')
    body = src[idx:idx + 1100]
    # « cassée » = invalidation atteinte (franchissement du stop pré-défini)
    assert 'Cassée' in body and 'invalidation' in body.lower()
    assert 'mark<=stop' in body.replace(' ', '')
    # état honnête « données insuffisantes » quand pas de marque
    assert 'Données insuffisantes' in body


def test_thesis_state_has_six_honest_states():
    src = _read(PF)
    for label in ('Cassée', 'Fragilisée', 'Renforcée par les faits', 'Intacte',
                  'À surveiller', 'Données insuffisantes'):
        assert label in src, f'état de thèse manquant : {label}'


# ── Gestion des gagnants (LOT C) ─────────────────────────────────────────
def test_winner_rules_indicative_never_auto_exit():
    src = _read(PF)
    assert 'function winnerRule' in src
    assert 'sécuriser 25-50 %' in src and '+100' in src
    assert 'laisser courir' in src  # règle par défaut d'une thèse qui tient
    # jamais une sortie automatique
    assert 'vente automatique' not in src.lower()


# ── Tableau canonique (LOT B) ────────────────────────────────────────────
def test_canonical_positions_table_columns():
    src = _read(PF)
    for col in ('Prix moyen', 'Prix actuel', 'Valeur marché', 'Poids', 'Conviction',
                'État de thèse', 'Invalidation', 'Catalyseur', 'Prochaine action'):
        assert col in src, f'colonne canonique manquante : {col}'


# ── READONLY absolu (§21) ────────────────────────────────────────────────
def test_no_order_execution_button():
    src = _read(PF).lower()
    # aucun bouton d'achat/vente/passage d'ordre
    for bad in ('acheter maintenant', 'passer un ordre', 'envoyer l’ordre',
                'envoyer un ordre', 'place order', 'buy order', 'sell order'):
        assert bad not in src, f'chemin d’exécution interdit détecté : {bad}'


# ── Migration performance Journal → Portefeuille (LOT G, §6) ─────────────
def test_performance_migrated_to_portfolio():
    pf = _read(PF)
    assert "('performance', 'Performance')" in pf
    assert 'equityCard' in pf and 'drawdownCard' in pf and 'renderPerformance' in pf


def test_journal_no_longer_owns_portfolio_performance():
    jr = _read(JR)
    # les courbes de performance de portefeuille ne vivent plus au Journal
    assert 'equityCard' not in jr and 'drawdownCard' not in jr and 'heatmapCard' not in jr
    # mais le Journal garde la méthode/discipline
    assert 'profitFactor' in jr and 'winRate' in jr
    # et pointe vers le domicile unique
    assert '/portfolio?view=performance' in jr
