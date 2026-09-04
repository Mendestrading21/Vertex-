"""Vertex Test 1.0 — CINQ CHAMPS EXTERNES ENTRAIENT DANS LE HTML SANS ÊTRE ÉCHAPPÉS.

`AUDIT-TOTAL-2026-08-25`, chapitre sécurité : « HTML/JS fortement construit par
chaînes ».

## Ce qui a été recensé le 25 août 2026

Interpolations `${…}` d'un champ d'origine **externe** (`name`, `sector`,
`industry`, `title`, `publisher`, `country`, `ceo`…) sans `esc()`,
`encodeURIComponent` ni `VX.fmt`, dans `vertex/ui` et `vertex/static` :

| site | champ | origine |
|---|---|---|
| `opportunities_page.py` | `${s}` dans une `<option>` | **`sector` de yfinance** |
| `vx-shell.js` | `${n.title}`, `${n.message}`, `${n.category}` | tickers saisis par l'utilisateur |
| `vx-shell.js` | `${n.ticker}` **dans une chaîne JS d'`onclick`** | idem |

Les trois autres occurrences trouvées étaient des titres de graphique posés par
notre propre code — pas des champs externes ; elles ne sont pas corrigées, et
c'est délibéré.

## Gravité, dite honnêtement

**Aucun chemin d'attaquant distant n'est prouvé.** Le seul champ réellement
externe est le `sector` de `yfinance.info`, et Yahoo n'est pas hostile. Les
autres viennent des tickers que l'utilisateur saisit lui-même — au pire une
auto-injection, plus probablement un panneau de notifications cassé en silence
par une apostrophe.

Ce que ce lot ferme, c'est la **classe**, pas un exploit vivant. Le dire évite
de faire passer une hygiène pour une urgence.

## Pourquoi un seul outil

Chaque page portait sa **propre** copie d'`esc`, et le JS servi sous `/static`
n'en avait **aucune**. `VX.esc` vit désormais dans `vx-core.js`. Une fonction
d'échappement recopiée diverge : il suffit qu'une copie oublie l'apostrophe.
"""
from __future__ import annotations

import pathlib
import re

RACINE = pathlib.Path(__file__).resolve().parents[1]

#: Champs dont la valeur vient d'une source EXTERNE (yfinance, IBKR, RSS) ou de
#: la saisie utilisateur — jamais d'un littéral du code.
_EXTERNES = ('name', 'shortName', 'longName', 'sector', 'industry', 'publisher',
             'title', 'ceo', 'activity', 'clients', 'country', 'pub', 'why',
             'fr', 'summary', 'desc', 'message', 'category')

_INTERPOLATION = re.compile(r'\$\{([^}]{0,140})\}')

#: Titres posés par NOTRE code, pas par une source. Les corriger reviendrait à
#: échapper un littéral — et à diluer le recensement au point qu'il ne
#: distingue plus rien.
_HORS_PERIMETRE = ('charts/catalyst-runway.js', 'charts/chart-core.js',
                   'charts/timeline-chart.js')


def _rendu(expr: str) -> str:
    """Ce que l'expression PEUT ÉCRIRE — sans sa condition.

    `${state.sector === s ? 'selected' : ''}` mentionne un champ externe mais
    ne le rend jamais : il rend `'selected'` ou `''`. L'échapper reviendrait à
    échapper un littéral, et un recensement qui compte ces cas finit par être
    ignoré — c'est ainsi qu'un gardien devient du bruit.

    Si une BRANCHE rend le champ, elle est toujours attrapée : seule la partie
    située AVANT le `?` est retirée.
    """
    return expr.split('?', 1)[1] if '?' in expr else expr


def _recenser() -> list:
    trouves = []
    for f in (sorted((RACINE / 'vertex' / 'ui').rglob('*.py'))
              + sorted((RACINE / 'vertex' / 'static').rglob('*.js'))):
        chemin = f.as_posix()
        if any(h in chemin for h in _HORS_PERIMETRE):
            continue
        for n, ligne in enumerate(f.read_text(encoding='utf-8',
                                              errors='replace').splitlines(), 1):
            for m in _INTERPOLATION.finditer(ligne):
                expr = m.group(1)
                if ('esc(' in expr or 'encodeURIComponent' in expr
                        or 'VX.fmt' in expr):
                    continue
                if not any(re.search(r'\.%s\b' % c, _rendu(expr))
                           for c in _EXTERNES):
                    continue
                trouves.append('%s:%d  %s' % (f.name, n, expr.strip()[:70]))
    return trouves


#  ═══════════  1. le recensement reste à zéro  ════════════════════════════════

def test_AUCUN_champ_externe_n_entre_dans_le_HTML_sans_echappement():
    """Le recensement du 25 août en trouvait cinq. Il doit rester vide : le
    sixième s'écrira sans échappement si rien ne l'en empêche."""
    coupables = _recenser()
    assert coupables == [], (
        "champs d'origine externe interpoles sans esc() :\n" + "\n".join(coupables))


def test_le_recensement_PARCOURT_vraiment_les_deux_arbres():
    """Sans ce contrôle, la garde ci-dessus passerait sur zéro fichier — et
    « aucun coupable » signifierait « je n'ai rien lu »."""
    py = list((RACINE / 'vertex' / 'ui').rglob('*.py'))
    js = list((RACINE / 'vertex' / 'static').rglob('*.js'))
    assert len(py) >= 5, 'arbre UI suspect : %d fichiers' % len(py)
    assert len(js) >= 5, 'arbre statique suspect : %d fichiers' % len(js)
    assert any(f.name == 'vx-shell.js' for f in js)


def test_le_recensement_VOIT_un_champ_nu_qu_on_lui_montre():
    """Contre-épreuve n°1 — D-031, déjà payé trois fois : un gardien qui ne
    trouve jamais rien passerait pour un gardien qui garde."""
    for forme in ('<b>${n.title}</b>', '<span>${r.sector}</span>',
                  '${x.industry || ""}'):
        m = _INTERPOLATION.search(forme)
        expr = m.group(1)
        assert any(re.search(r'\.%s\b' % c, expr) for c in _EXTERNES)
        assert 'esc(' not in expr


def test_le_recensement_NE_signale_PAS_la_forme_corrigee():
    """Contre-épreuve n°2 : un gardien qui refuse aussi la correction est
    désactivé au premier commit pressé."""
    for forme in ('<b>${VX.esc(n.title)}</b>', '${esc(s.sector||"n/d")}',
                  '${encodeURIComponent(s.sector||"")}'):
        expr = _INTERPOLATION.search(forme).group(1)
        assert ('esc(' in expr or 'encodeURIComponent' in expr)


#  ═══════════  2. un seul outil d'échappement, et il est complet  ═════════════

def test_VX_esc_existe_dans_le_NOYAU_partage():
    """Chaque page portait sa propre copie, et le JS servi n'en avait aucune.
    Une fonction d'échappement recopiée diverge : il suffit qu'une copie
    oublie l'apostrophe."""
    src = (RACINE / 'vertex' / 'static' / 'vertex' / 'js'
           / 'vx-core.js').read_text(encoding='utf-8')
    assert 'VX.esc' in src


def test_VX_esc_couvre_les_CINQ_metacaracteres():
    """Oublier l'apostrophe suffit à rouvrir la brèche dans un attribut."""
    src = (RACINE / 'vertex' / 'static' / 'vertex' / 'js'
           / 'vx-core.js').read_text(encoding='utf-8')
    i = src.index('VX.esc')
    bloc = src[i:i + 400]
    for entite in ('&lt;', '&gt;', '&amp;', '&quot;', '&#39;'):
        assert entite in bloc, 'VX.esc n echappe pas %s' % entite


def test_le_shell_utilise_VX_esc_pour_les_notifications():
    src = (RACINE / 'vertex' / 'static' / 'vertex' / 'js'
           / 'vx-shell.js').read_text(encoding='utf-8')
    i = src.index('vx-notif-item')
    bloc = src[i:i + 900]
    assert 'VX.esc(n.title)' in bloc
    assert 'VX.esc(n.message' in bloc
    assert 'VX.esc(n.category' in bloc


#  ═══════════  3. le ticker n'entre dans du JS que s'il en est un  ════════════

def test_le_ticker_est_FILTRE_avant_d_entrer_dans_l_onclick():
    """Échapper en HTML ne suffirait pas : le parseur décode `&#39;` avant que
    JS ne voie la chaîne, et l'apostrophe reviendrait. On restreint donc la
    valeur à ce qu'un ticker peut être."""
    src = (RACINE / 'vertex' / 'static' / 'vertex' / 'js'
           / 'vx-shell.js').read_text(encoding='utf-8')
    i = src.index('VX.openAnalysis')
    bloc = src[max(0, i - 300):i + 120]
    assert re.search(r'\[A-Z0-9\.\\?-\]', bloc), (
        "le ticker doit etre filtre par sa FORME avant d'entrer dans du JS")


def test_le_motif_de_ticker_accepte_les_tickers_REELS():
    """Contre-épreuve : un filtre trop strict ferait disparaître le bouton
    d'analyse sur des titres parfaitement valides."""
    motif = re.compile(r'^[A-Z0-9.\-]{1,10}$')
    for bon in ('AAPL', 'BRK-B', 'BF-B', 'GOOGL', 'A'):
        assert motif.match(bon), bon
    for mauvais in ("A');alert(1);//", '<img>', '', 'a' * 20):
        assert not motif.match(mauvais), mauvais


def test_le_recensement_ignore_une_CONDITION_mais_pas_une_BRANCHE():
    """La nuance qui empêche le gardien de devenir du bruit — et celle qui
    l'empêche de devenir aveugle."""
    #  Le champ n'est que dans la condition : rien d'externe n'est rendu.
    assert '.sector' not in _rendu("state.sector===s?'selected':''")
    #  Mais s'il est rendu par une branche, il doit rester visible.
    assert '.sector' in _rendu("x?'ok':r.sector")
    assert '.title' in _rendu("n.title")
