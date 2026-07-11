"""Gardiens finaux Strategy OS (§38) — noms canoniques exigés par le cahier.

Certains invariants sont déjà testés sous d'autres noms ; ces tests portent
les noms canoniques et vérifient l'invariant directement (pas de simple alias).
"""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_EXECUTION_NAMES = (
    'place_order', 'placeOrder', 'submit_order', 'submitOrder', 'transmit_order',
    'modify_order', 'cancel_order', 'exercise_option', 'transfer_cash',
    'withdraw_cash', 'rebalance_automatically', 'auto_execute', 'whatIfOrder',
    'bracketOrder', 'MarketOrder(', 'LimitOrder(',
)


def _python_sources():
    out = subprocess.run(['git', 'ls-files', '*.py'], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    for rel in out.splitlines():
        p = ROOT / rel
        if p.is_file() and 'tests' not in Path(rel).parts:
            yield p


DENY_LIST_FILES = ('vertex/ai/tool_registry.py',)  # la liste NOIRE cite les noms pour les interdire


def test_no_order_execution_path():
    """AUCUN chemin d'exécution d'ordre dans tout le code applicatif."""
    offenders = []
    for path in _python_sources():
        rel = str(path.relative_to(ROOT))
        if rel in DENY_LIST_FILES:
            continue
        text = path.read_text(encoding='utf-8', errors='ignore')
        for needle in FORBIDDEN_EXECUTION_NAMES:
            for i, line in enumerate(text.splitlines(), 1):
                if needle in line and not line.strip().startswith('#') \
                        and 'interdit' not in line and 'FORBIDDEN' not in line \
                        and 'forbidden' not in line:
                    offenders.append(f'{rel}:{i}: {needle}')
    assert not offenders, 'chemins d’exécution détectés:\n' + '\n'.join(offenders[:20])


def test_ibkr_readonly():
    """Toute connexion IBKR du dépôt force readonly=True."""
    connect_sites = []
    for path in _python_sources():
        lines = path.read_text(encoding='utf-8', errors='ignore').splitlines()
        for i, line in enumerate(lines, 1):
            if '.connect(' in line and ('clientId' in line or 'client_id' in line):
                window = ' '.join(lines[i - 1:i + 2])  # l'appel peut être multi-lignes
                connect_sites.append((path, i, window))
    for path, i, window in connect_sites:
        assert 'readonly=True' in window, \
            f'{path.relative_to(ROOT)}:{i}: connexion IBKR sans readonly=True'
    assert connect_sites, 'aucun site de connexion IBKR trouvé (test devenu aveugle ?)'


def test_all_sync_keys_match():
    """Les 4 listes de clés de sync desk sont identiques (règle critique n°1)."""
    terminal = (ROOT / 'terminal.py').read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'__DESK_KEYS\s*=\s*\[([^\]]+)\]', terminal)
    assert m, '__DESK_KEYS introuvable dans terminal.py'
    desk_keys = set(re.findall(r"'([^']+)'", m.group(1)))
    # vx_kit : liste nommée DESK_KEYS ; journal : liste inline dans jvSyncPush.
    text = (ROOT / 'vertex/ui/vx_kit.py').read_text(encoding='utf-8', errors='ignore')
    m2 = re.search(r"DESK_KEYS\s*=\s*\[([^\]]+)\]", text)
    assert m2, 'liste de clés absente de vertex/ui/vx_kit.py'
    keys = set(re.findall(r"'([^']+)'", m2.group(1)))
    assert keys == desk_keys, f'vx_kit: clés désynchronisées {keys ^ desk_keys}'
    journal = (ROOT / 'vertex/ui/journal.py').read_text(encoding='utf-8', errors='ignore')
    for key in desk_keys:
        assert f"'{key}'" in journal, f'journal.py: clé de sync manquante {key}'


def test_ibkr_confirms_signal():
    """Un signal TradingView seul ne devient jamais ACTIONABLE : il déclenche
    une réévaluation, et le pipeline exige des données techniques/de marché
    confirmées (IBKR ou source validée) pour dépasser RADAR."""
    from vertex.data_sources.tradingview_signal_store import TradingViewSignalStore
    import time
    store = TradingViewSignalStore()
    res = store.add('NVDA', 'BREAKOUT_CONFIRMED', time.time())
    assert res['accepted'] and res['entry']['action'] == 'REEVALUATE'

    from vertex.scanner.candidate_pipeline import evaluate_candidate
    tv_only = {'symbol': 'NVDA',
               'sentiment': {'news_tone': 'POSITIVE'},
               'catalysts': {'has_catalyst': True},
               # AUCUNE donnée technique confirmée par le broker/source validée :
               'technical': {},
               'data_quality': {'actionable_allowed': False}}
    out = evaluate_candidate(tv_only)
    assert out['outcome'] != 'ACTIONABLE'
    confirmed = dict(tv_only)
    confirmed['technical'] = {'trend': 'UP', 'relative_strength': 80,
                              'reward_risk': 2.3}
    confirmed['fundamentals'] = {'revenue_growth': 0.2, 'margin': 0.25}
    confirmed['data_quality'] = {'actionable_allowed': True}
    confirmed['reconciliation_ok'] = True
    out2 = evaluate_candidate(confirmed)
    assert out2['outcome'] in ('WATCH', 'ACTIONABLE'), \
        'avec confirmation broker, le candidat progresse'


def test_no_temporary_migration_adapters_left():
    """Les adaptateurs temporaires de migration ont tous disparu."""
    for path in _python_sources():
        text = path.read_text(encoding='utf-8', errors='ignore')
        assert 'DeprecationWarning' not in text or 'adapter' not in text.lower(), \
            f'{path}: adaptateur de migration résiduel'
