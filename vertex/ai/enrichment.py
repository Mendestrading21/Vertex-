"""vertex.ai.enrichment — orchestrateur « cerveau à jour » (Claude + web).

Au lancement (et à la demande), Claude va chercher sur le web les VRAIES
données du jour pour chaque surface — cotations différées, actualités,
références — et les renvoie AVEC citations. Chaque valeur est emballée en
provenance honnête (`claude_web · différé · estimation`) puis persistée dans un
instantané daté. Rien n'est jamais inventé :

  GARDE-FOU D'HONNÊTETÉ — un chiffre n'est conservé QUE si l'appel a réellement
  effectué une recherche web (citations présentes). Sinon → absent (« — »),
  jamais un nombre sorti de nulle part.

Sans clé ANTHROPIC_API_KEY : statut MISSING, aucune donnée produite (repli
honnête). L'app fonctionne, elle dit simplement « analyse Claude indisponible ».
"""
from __future__ import annotations

import time

from vertex.services import persist
from . import health, provenance as prov
from .response_validator import CERTAINTY_PHRASES
from .web_provider import ClaudeWebProvider

_STORE = 'ai_enrichment.json'

STATUS_OK = 'OK'
STATUS_MISSING = 'MISSING'      # pas de clé/provider → aucune analyse
STATUS_DEGRADED = 'DEGRADED'    # provider présent mais erreurs/partiel
STATUS_EMPTY = 'EMPTY'          # jamais lancé

MAX_SYMBOLS = 24                # borne : on n'enrichit pas des centaines de titres


def _now_iso() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def _num(x):
    try:
        f = float(x)
        return f if f == f else None       # rejette NaN
    except (TypeError, ValueError):
        return None


def _has_certainty(text: str) -> bool:
    low = (text or '').lower()
    return any(p.lower() in low for p in CERTAINTY_PHRASES)


# ─────────────────────────────────────────── prompts de recherche
_SYS = ("Tu es l'analyste de recherche de Vertex (lecture seule). Tu utilises la "
        "recherche web pour trouver des données FACTUELLES et RÉCENTES, toujours "
        "sourcées. Règles absolues : (1) ne JAMAIS inventer un chiffre — si tu ne "
        "trouves pas, mets null ; (2) aucun langage de certitude ; (3) aucune notion "
        "d'ordre/exécution ; (4) réponds UNIQUEMENT par un objet JSON valide, rien "
        "d'autre. Les prix trouvés sur le web sont DIFFÉRÉS : signale-le.")


def build_quote_research(symbol: str) -> tuple[str, str]:
    user = (
        f"Recherche le dernier cours de bourse connu de {symbol} (actions US). "
        "Rends STRICTEMENT ce JSON : {\"symbol\":\"%s\",\"price\":<nombre ou null>,"
        "\"currency\":\"USD\",\"change_pct\":<nombre ou null>,\"as_of\":\"<date "
        "trouvée>\",\"note\":\"<source + \\\"différé\\\">\"}. Si tu n'es pas sûr du "
        "chiffre, mets price=null." % symbol)
    return _SYS, user


def build_news_research(symbol: str) -> tuple[str, str]:
    user = (
        f"Recherche 1 à 3 actualités RÉCENTES et vérifiables sur {symbol}. Rends "
        "STRICTEMENT ce JSON : {\"symbol\":\"%s\",\"items\":[{\"headline\":\"...\","
        "\"impact\":\"HAUSSIER|BAISSIER|NEUTRE\",\"why\":\"1 phrase\",\"date\":"
        "\"AAAA-MM-JJ\"}]}. Aucune actualité fiable trouvée → items=[]." % symbol)
    return _SYS, user


# ─────────────────────────────────────────── parsing → provenance
def parse_quote(res: dict) -> dict:
    """Emballe une cotation Claude+web. Chiffre gardé SEULEMENT si recherche réelle."""
    data = (res or {}).get('data') or {}
    cits = (res or {}).get('citations') or []
    searched = (res or {}).get('searches', 0) > 0
    sourced = bool(cits)                 # un prix n'est gardé QUE s'il porte une citation réelle
    price = _num(data.get('price'))
    text = (res or {}).get('text') or ''
    # Garde-fou d'honnêteté : AUCUN prix sans citation (une recherche qui échoue
    # ou ne cite rien ne suffit pas) NI avec langage de certitude.
    if price is None or not sourced or _has_certainty(text):
        return prov.absent('prix trouvé mais sans source citable' if searched
                           else 'aucune recherche web aboutie')
    env = prov.wrap(price, source=prov.SRC_CLAUDE_WEB, citations=cits,
                    as_of=_now_iso(),
                    note=(str(data.get('note') or 'prix différé'))[:160])
    env['currency'] = (str(data.get('currency') or 'USD'))[:6]
    env['change_pct'] = _num(data.get('change_pct'))
    env['as_of_data'] = (str(data.get('as_of') or ''))[:40]
    return env


def parse_news(res: dict) -> dict:
    data = (res or {}).get('data') or {}
    cits = (res or {}).get('citations') or []
    items = []
    for it in (data.get('items') or [])[:3]:
        if not isinstance(it, dict):
            continue
        head = str(it.get('headline') or '').strip()[:200]
        if not head:
            continue
        impact = str(it.get('impact') or 'NEUTRE').upper()
        if impact not in ('HAUSSIER', 'BAISSIER', 'NEUTRE'):
            impact = 'NEUTRE'
        items.append({'headline': head, 'impact': impact,
                      'why': str(it.get('why') or '')[:280],
                      'date': str(it.get('date') or '')[:40]})
    if not items:
        return prov.absent('aucune actualité fiable trouvée')
    return prov.wrap(items, source=prov.SRC_CLAUDE_WEB, citations=cits, as_of=_now_iso())


# ─────────────────────────────────────────── orchestration
def _make_provider():
    return ClaudeWebProvider()


def run(symbols, *, provider=None, want_news=True, persist_store=True) -> dict:
    """Enrichit les surfaces via Claude+web. Rend l'instantané (et le persiste).

    Sans provider disponible (pas de clé) → instantané MISSING, aucune donnée.
    Chaque erreur par titre est capturée : l'enrichissement n'est jamais bloquant.
    """
    provider = provider or _make_provider()
    syms = [str(s).upper()[:12] for s in (symbols or []) if s][:MAX_SYMBOLS]
    snap = {'as_of': _now_iso(), 'source': prov.SRC_CLAUDE_WEB,
            'model': getattr(provider, 'model', ''), 'symbols': syms,
            'surfaces': {'quotes': {}, 'news': {}}, 'errors': []}

    if not provider.available():
        snap['status'] = STATUS_MISSING
        snap['note'] = ('Analyse Claude+web indisponible (clé ANTHROPIC_API_KEY '
                        'absente) — aucune donnée estimée produite. L\'app sert '
                        'les données réelles/moteur uniquement.')
        if persist_store:
            _save(snap)
        return snap

    errors = []
    for sym in syms:
        try:
            s, u = build_quote_research(sym)
            snap['surfaces']['quotes'][sym] = parse_quote(provider.research_json(s, u))
        except Exception as exc:                       # noqa: BLE001 — jamais bloquant
            snap['surfaces']['quotes'][sym] = prov.absent('erreur recherche cotation')
            errors.append('%s quote: %s' % (sym, exc.__class__.__name__))
        if want_news:
            try:
                s, u = build_news_research(sym)
                snap['surfaces']['news'][sym] = parse_news(provider.research_json(s, u))
            except Exception as exc:                   # noqa: BLE001
                snap['surfaces']['news'][sym] = prov.absent('erreur recherche actualité')
                errors.append('%s news: %s' % (sym, exc.__class__.__name__))

    snap['errors'] = errors[:20]
    got = sum(1 for e in snap['surfaces']['quotes'].values() if e.get('value') is not None)
    snap['status'] = STATUS_OK if not errors else STATUS_DEGRADED
    snap['note'] = ('%d/%d cotations trouvées via Claude+web (différées, sourcées).'
                    % (got, len(syms)) if syms else 'aucun titre à enrichir.')
    if errors:
        health.record_failure('; '.join(errors[:3]))
    else:
        health.record_success()
    if persist_store:
        _save(snap)
    return snap


def _save(snap: dict) -> None:
    persist.save_json(_STORE, snap)


def load_snapshot() -> dict:
    return persist.load_json(_STORE, {'status': STATUS_EMPTY, 'surfaces': {},
                                      'note': 'aucun enrichissement encore lancé.'})


def quote_for(symbol: str) -> dict:
    """Enveloppe de provenance de la cotation Claude d'un titre (ou absente)."""
    q = (load_snapshot().get('surfaces', {}).get('quotes', {}) or {})
    return q.get(str(symbol).upper()) or prov.absent()


def status() -> dict:
    snap = load_snapshot()
    q = snap.get('surfaces', {}).get('quotes', {}) or {}
    return {'status': snap.get('status', STATUS_EMPTY), 'as_of': snap.get('as_of'),
            'model': snap.get('model'), 'note': snap.get('note'),
            'symbols': len(snap.get('symbols', [])),
            'quotes_found': sum(1 for e in q.values() if e.get('value') is not None),
            'errors': snap.get('errors', [])}


__all__ = ['run', 'load_snapshot', 'quote_for', 'status', 'build_quote_research',
           'build_news_research', 'parse_quote', 'parse_news',
           'STATUS_OK', 'STATUS_MISSING', 'STATUS_DEGRADED', 'STATUS_EMPTY']
