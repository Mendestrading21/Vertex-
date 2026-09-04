"""tests/test_gateway_ia.py — LOT 11 : gateway IA unique.

Défaut mesuré : copilote, briefs et enrichissement appellent Anthropic en
DIRECT, sans limite de débit ni journal d'audit — seules gardes présentes
dans investment_agent. Cible : toute sortie IA passe par une porte partagée
(vertex/ai/gateway.py) ; un refus de budget rend le repli déterministe
HONNÊTE (jamais une 500, jamais un libellé mensonger).
Nés ROUGES sur le SHA courant.
"""
import json

import pytest

from vertex.ai import briefs, copilot


@pytest.fixture(autouse=True)
def _porte_propre():
    from vertex.ai import gateway
    gateway.reset_for_test()
    yield
    gateway.reset_for_test()


class _ClientInterdit:
    """Un client Anthropic qui NE DOIT PAS être atteint (budget refusé)."""

    def __init__(self):
        self.messages = self

    def create(self, **kw):                    # pragma: no cover — si atteint, échec
        raise AssertionError('appel Anthropic effectué malgré un budget refusé')


class _ClientOk:
    def __init__(self, text='Synthèse ancrée. Risques / à surveiller : x.'):
        self._text = text
        self.messages = self
        self.calls = 0

    def create(self, **kw):
        self.calls += 1

        class _Msg:
            pass
        m = _Msg()
        b = _Msg()
        b.text = self._text
        m.content = [b]
        return m


def _epuise(source):
    """Épuise le budget de la famille `source` via la porte partagée."""
    from vertex.ai import gateway
    n = 0
    while gateway.allow(source, symbol='TST'):
        n += 1
        assert n < 1000, 'budget sans plafond — la porte ne limite rien'
    return n


# ─────────────────────────────────────────── la porte elle-même

def test_les_budgets_par_famille_sont_independants():
    from vertex.ai import gateway
    _epuise('copilot')
    assert gateway.allow('briefs') is True, (
        'le budget copilote épuisé ne doit pas affamer les briefs')


def test_un_refus_de_budget_est_journalise():
    from vertex.ai import gateway
    from vertex.ai.audit import AUDIT
    avant = len(AUDIT.recent(200))
    _epuise('copilot')
    entrees = AUDIT.recent(200)[avant:]
    refus = [e for e in entrees if not e['ok'] and 'rate_limited' in e['errors']]
    assert refus, 'le refus de budget doit laisser une trace d\'audit'


# ─────────────────────────────────────────── copilote

def test_copilote_budget_refuse_repli_honnete(monkeypatch):
    import anthropic
    monkeypatch.setattr(briefs, 'available', lambda: True)
    monkeypatch.setattr(anthropic, 'Anthropic', lambda: _ClientInterdit())
    _epuise('copilot')
    r = copilot.answer('Que dit le positionnement ?', {}, 'AAPL')
    assert r['ok'] is True and r['source'] == 'deterministic'
    assert 'limite' in r['label'].lower(), (
        'le libellé doit dire la VRAIE raison (limite atteinte), pas '
        '« Claude non configuré » : %r' % r['label'])


def test_copilote_succes_claude_est_audite(monkeypatch):
    import anthropic
    from vertex.ai.audit import AUDIT
    monkeypatch.setattr(briefs, 'available', lambda: True)
    monkeypatch.setattr(anthropic, 'Anthropic', lambda: _ClientOk())
    avant = len(AUDIT.recent(200))
    r = copilot.answer('Climat ?', {}, 'MSFT')
    assert r['source'] == 'claude'
    entrees = [e for e in AUDIT.recent(200)[avant:] if e['source'] == 'copilot']
    assert entrees and entrees[-1]['ok'] is True
    assert entrees[-1]['symbol'] == 'MSFT'
    assert entrees[-1]['model'] == copilot.MODEL
    assert entrees[-1]['duration_ms'] is not None


def test_copilote_echec_claude_est_audite_et_replie(monkeypatch):
    import anthropic
    from vertex.ai.audit import AUDIT

    class _Boom(_ClientOk):
        def create(self, **kw):
            raise RuntimeError('panne api')
    monkeypatch.setattr(briefs, 'available', lambda: True)
    monkeypatch.setattr(anthropic, 'Anthropic', lambda: _Boom())
    avant = len(AUDIT.recent(200))
    r = copilot.answer('Climat ?', {}, 'NVDA')
    assert r['ok'] is True and r['source'] == 'deterministic'
    entrees = [e for e in AUDIT.recent(200)[avant:] if e['source'] == 'copilot']
    assert entrees and entrees[-1]['ok'] is False and entrees[-1]['errors']


# ─────────────────────────────────────────── briefs

def test_brief_desc_budget_refuse_prend_le_chemin_gratuit(monkeypatch):
    monkeypatch.setattr(briefs, 'available', lambda: True)
    monkeypatch.setattr(briefs, 'Anthropic', _ClientInterdit)
    monkeypatch.setattr(briefs, '_google_fr', lambda t: 'traduction gratuite')
    _epuise('briefs')
    briefs._cache.clear()
    assert briefs.fr_desc('TST', 'An english description.') == 'traduction gratuite'


def test_brief_profil_budget_refuse_rend_vide_pas_d_appel(monkeypatch):
    monkeypatch.setattr(briefs, 'available', lambda: True)
    monkeypatch.setattr(briefs, 'Anthropic', _ClientInterdit)
    _epuise('briefs')
    briefs._cache.clear()
    assert briefs.company_brief('TST', 'Sells widgets.') == {}


def test_brief_succes_est_audite(monkeypatch):
    from vertex.ai.audit import AUDIT
    reponse = json.dumps({'sells': 'widgets', 'earns': 'ventes',
                          'clients': 'PME', 'moat': 'réseau'})
    monkeypatch.setattr(briefs, 'available', lambda: True)
    monkeypatch.setattr(briefs, 'Anthropic', lambda: _ClientOk(text=reponse))
    briefs._cache.clear()
    avant = len(AUDIT.recent(200))
    out = briefs.company_brief('TST', 'Sells widgets to SMBs.')
    assert out.get('sells') == 'widgets'
    entrees = [e for e in AUDIT.recent(200)[avant:] if e['source'] == 'briefs']
    assert entrees and entrees[-1]['ok'] is True


# ─────────────────────────────────────────── enrichissement

def test_enrichissement_budget_epuise_surface_absente_honnete():
    from vertex.ai import enrichment as E

    class _Provider:
        model = 'x'

        def available(self):
            return True

        def research_json(self, s, u):        # pragma: no cover — si atteint, échec
            raise AssertionError('recherche effectuée malgré un budget épuisé')
    _epuise('enrichment')
    snap = E.run(['ACN'], provider=_Provider(), want_news=False,
                 persist_store=False)
    q = snap['surfaces']['quotes']['ACN']
    assert q.get('value') is None, 'jamais un chiffre sous budget épuisé'
    assert snap['errors'], 'le budget épuisé doit être une erreur consignée'
    assert any('budget' in e.lower() or 'rate' in e.lower()
               for e in snap['errors'])


def test_enrichissement_appels_reussis_sont_audites(monkeypatch, tmp_path):
    from vertex.ai import enrichment as E
    from vertex.ai.audit import AUDIT

    class _Provider:
        model = 'x'

        def available(self):
            return True

        def research_json(self, s, u):
            return {'data': {'symbol': 'ACN', 'price': 300.5, 'currency': 'USD',
                             'change_pct': 1.0, 'as_of': '2026-08-28',
                             'note': 'src différé'},
                    'citations': ['https://exemple.test'], 'raw': ''}
    avant = len(AUDIT.recent(200))
    snap = E.run(['ACN'], provider=_Provider(), want_news=False,
                 persist_store=False)
    assert snap['status'] == E.STATUS_OK
    entrees = [e for e in AUDIT.recent(200)[avant:] if e['source'] == 'enrichment']
    assert entrees and entrees[-1]['ok'] is True
