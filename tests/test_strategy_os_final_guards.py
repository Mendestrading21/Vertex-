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


DENY_LIST_FILES = (
    'vertex/ai/tool_registry.py',          # la liste NOIRE cite les noms pour les interdire
    # LOT 34 — l'outil de liste BLANCHE doit nommer les verbes d'execution :
    # c'est son travail de les tenir hors du code, et il les cite dans sa
    # documentation et dans le garde-fou qui empeche de les glisser dans la
    # liste. Meme raison que le registre ci-dessus, cas inverse.
    'tools/mesurer_surface_ibkr.py',
)


def test_no_order_execution_path():
    """AUCUN chemin d'exécution d'ordre dans tout le code applicatif."""
    offenders = []
    for path in _python_sources():
        rel = path.relative_to(ROOT).as_posix()  # forward-slash sur tout OS (Windows inclus)
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
    """Les listes de clés de sync desk sont identiques (règle critique n°1).

    Source de vérité : `vx_kit` (DESK_KEYS) et `vx-entities.js`, qui doivent
    porter exactement les mêmes clés. terminal.py n'en héberge plus aucune copie
    depuis la purge É1.

    ⚠ RÉDUIT AU LOT 17 DE SIGNAL OS. Ce test comparait aussi `journal.py`, dont
    la liste vivait en ligne dans `jvSyncPush` ; le module a été supprimé
    (0 consommateur, aucune route). Une comparaison en moins n'affaiblit rien
    ici : ce qui protège l'utilisateur, c'est `vx-entities.js` — le SEUL des
    trois que les huit pages chargent — et son repli inline dans
    `system_page.py`, gardés par `tests/test_desk_keys_servies_lot381.py`.
    """
    # vx_kit : liste nommée DESK_KEYS, ancre de comparaison (non servie).
    text = (ROOT / 'vertex/ui/vx_kit.py').read_text(encoding='utf-8', errors='ignore')
    m2 = re.search(r"DESK_KEYS\s*=\s*\[([^\]]+)\]", text)
    assert m2, 'liste de clés absente de vertex/ui/vx_kit.py'
    desk_keys = set(re.findall(r"'([^']+)'", m2.group(1)))
    assert 'vxWatchlist' in desk_keys and 'vxAlerts' in desk_keys
    ent = (ROOT / 'vertex/static/vertex/js/vx-entities.js').read_text(
        encoding='utf-8', errors='ignore')
    m3 = re.search(r"DESK_KEYS\s*=\s*\[([^\]]+)\]", ent)
    assert m3, 'DESK_KEYS absent de vx-entities.js'
    ent_keys = set(re.findall(r"'([^']+)'", m3.group(1)))
    assert ent_keys == desk_keys, f'vx-entities: clés désynchronisées {ent_keys ^ desk_keys}'
    # Le repli inline de `/system` est l'autre liste RÉELLEMENT SERVIE : elle
    # remplace ici l'ancre `journal.py` disparue, et c'est un gain — on compare
    # désormais deux listes que le navigateur reçoit, au lieu d'une servie et
    # d'une morte.
    sysp = (ROOT / 'vertex/ui/pages/system_page.py').read_text(
        encoding='utf-8', errors='ignore')
    for key in desk_keys:
        assert f"'{key}'" in sysp, (
            f'system_page.py (repli deskKeys) : clé de sync manquante {key}')


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
