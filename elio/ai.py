"""
elio/ai.py — Couche IA optionnelle (traduction FR des news + synthèse marché).

Utilise l'API Anthropic SI une clé ANTHROPIC_API_KEY est présente (env ou .env).
Sinon, dégradation propre : renvoie les titres d'origine (anglais), aucun crash.

⛔ La clé n'est JAMAIS écrite en dur : lue depuis l'environnement / .env (non commité).
"""
import os
import json
import hashlib

try:
    from anthropic import Anthropic
except Exception:
    Anthropic = None

MODEL = 'claude-haiku-4-5-20251001'   # rapide + économique pour de la traduction
_cache = {}


def available():
    """Vrai si le package + une VRAIE clé sont là (rejette le placeholder). Statut UI."""
    k = os.environ.get('ANTHROPIC_API_KEY', '') or ''
    return Anthropic is not None and k.startswith('sk-ant-') and 'xxxx' not in k


def fr_news(ticker, items):
    """Traduit les titres en FR + 1 phrase 'pourquoi ça bouge'. Renvoie (items+'fr', why|None)."""
    if not items:
        return items, None
    titles = [i.get('title', '') for i in items]
    key = ticker + ':' + hashlib.md5('|'.join(titles).encode('utf-8', 'ignore')).hexdigest()
    if key in _cache:                       # cache : on ne re-traduit jamais 2x les mêmes titres
        c = _cache[key]
        for it, fr in zip(items, c['fr']):
            it['fr'] = fr
        return items, c['why']
    if not available():                     # pas de clé → fallback anglais, zéro appel
        for it in items:
            it['fr'] = it.get('title')
        return items, None
    try:
        client = Anthropic()                # lit ANTHROPIC_API_KEY de l'environnement
        lst = '\n'.join(f'{i + 1}. {t}' for i, t in enumerate(titles))
        prompt = (
            f"Tu es analyste marché. Traduis ces titres d'actualité financière sur {ticker} "
            f"en français (fidèle, concis, vocabulaire trader) et donne UNE phrase de synthèse "
            f"'pourquoi le titre bouge'.\n"
            f"Réponds STRICTEMENT en JSON, rien d'autre : "
            f'{{"fr": [liste meme ordre], "why": "une phrase"}}\n\nTitres:\n{lst}'
        )
        msg = client.messages.create(model=MODEL, max_tokens=800,
                                     messages=[{'role': 'user', 'content': prompt}])
        txt = msg.content[0].text.strip()
        if txt.startswith('```'):
            txt = txt.split('\n', 1)[1].rsplit('```', 1)[0] if '\n' in txt else txt
        data = json.loads(txt)
        frs = data.get('fr') or titles
        why = data.get('why')
        _cache[key] = {'fr': frs, 'why': why}
        for it, fr in zip(items, frs):
            it['fr'] = fr
        return items, why
    except Exception:
        for it in items:
            it['fr'] = it.get('title')
        return items, None


def company_brief(sym, summary):
    """Extrait d'une description factuelle un mini-profil FR :
    {sells, earns, clients, moat}. N'invente RIEN (fidèle à la source, aucun chiffre
    ajouté). Cache par contenu ; renvoie {} si pas de clé / erreur (dégradation propre)."""
    if not summary:
        return {}
    key = 'brief:' + hashlib.md5((sym + summary).encode('utf-8', 'ignore')).hexdigest()
    if key in _cache:
        return _cache[key]
    if not available():
        return {}
    try:
        client = Anthropic()
        prompt = (
            f"À partir de cette description factuelle de l'entreprise {sym}, produis un JSON "
            f"compact en français. Sois fidèle : n'invente rien, n'ajoute aucun chiffre absent. "
            f'Clés (valeurs courtes) : "sells" (ce qu\'elle vend, ~6 mots), '
            f'"earns" (comment elle gagne de l\'argent, ~10 mots), '
            f'"clients" (ses clients types, ~6 mots), '
            f'"moat" (son avantage concurrentiel, ~10 mots). '
            f"Réponds UNIQUEMENT par le JSON, sans préambule.\n\n{summary}"
        )
        msg = client.messages.create(model=MODEL, max_tokens=400,
                                     messages=[{'role': 'user', 'content': prompt}])
        txt = (msg.content[0].text or '').strip()
        if txt.startswith('```'):
            txt = txt.split('\n', 1)[1].rsplit('```', 1)[0] if '\n' in txt else txt
        data = json.loads(txt)
        out = {k: data.get(k) for k in ('sells', 'earns', 'clients', 'moat') if data.get(k)}
        _cache[key] = out
        return out
    except Exception:
        return {}


def fr_desc(sym, summary):
    """Traduit une description d'entreprise (longBusinessSummary) en français.
    Cache par contenu ; fallback = texte d'origine si pas de clé / erreur."""
    if not summary:
        return summary
    key = 'desc:' + hashlib.md5((sym + summary).encode('utf-8', 'ignore')).hexdigest()
    if key in _cache:
        return _cache[key]
    if not available():
        return summary
    try:
        client = Anthropic()
        prompt = (
            f"Traduis en français clair et naturel cette description de l'activité de "
            f"l'entreprise {sym} (vocabulaire économique, fidèle, sans ajouter d'info). "
            f"Réponds UNIQUEMENT par la traduction, sans guillemets ni préambule.\n\n{summary}"
        )
        msg = client.messages.create(model=MODEL, max_tokens=600,
                                     messages=[{'role': 'user', 'content': prompt}])
        fr = (msg.content[0].text or '').strip()
        if fr:
            _cache[key] = fr
            return fr
    except Exception:
        pass
    return summary
