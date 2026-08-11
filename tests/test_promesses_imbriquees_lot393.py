"""
LOT 393 — LES PROMESSES DE RETOUR IMBRIQUÉES : le dernier angle mort du 375.

Le lot 375 vérifiait les docstrings « Retourne {a, b, c} » sur les branches
`return {littéral}` — et concluait « sain, prouvé » sur six fonctions. Il
déclarait aussi son angle mort : *« Vérifier les formes IMBRIQUÉES demanderait
un analyseur d'un autre ordre ; c'est déclaré ici plutôt que tu. »*

**Il n'en fallait pas un.** Une promesse de retour se vérifie en APPELANT la
fonction : l'exécution tranche ce que l'analyse statique ne sait pas suivre.

## Le dénominateur

```text
fonctions portant une promesse « Retourne {…} »            7
   dont au moins un `return {littéral}`  (couvert par 375)  5
   dont AUCUN littéral → forme déléguée   (angle mort)      2
```

Deux, pas une famille. Le trou déclaré était réel mais étroit.

## Verdict — les deux promesses sont exactes, prouvé par exécution

```text
grade_packet   promises {overall, warnings, actionable_allowed}
               rendues  {overall, warnings, actionable_allowed}   → 0 manquante
select_calls   promises {per_category, primary, rejected, notes}
               rendues  {per_category, primary, rejected, notes}  → 0 manquante
```

Les fixtures sont celles de la suite (`test_data_sources`, `test_options_engine`)
— pas des entrées inventées pour l'occasion : le contrat est vérifié sur les
mêmes objets que le reste des tests.

## Le troisième cas, statique et déjà connu

`options_for_position` délègue à son `pack()` interne. Sa docstring cite **12
identifiants nus** (`role, role_label, sym, type, strike, exp, dte, premium,
pop, score, grade, why`) ; `pack()` en renvoie **13**. Le surnuméraire est
`delta` : **sous-déclaration, pas promesse fausse** — rien de ce qui est annoncé
ne manque. Mesure confirmée, identique à celle du lot 375.

## Ce que ce gardien ajoute

Ces trois fonctions étaient **hors de portée** du gardien du 375, qui n'inspecte
que les dicts littéraux. Une clé promise qui disparaîtrait aujourd'hui passerait
la suite. Ici la propriété est vérifiée là où elle est décidable : à l'exécution
pour les deux déléguées, statiquement pour la troisième.
"""
import ast
import importlib
import os
import re

import pytest

PROMESSE = re.compile(r'[Rr]etourne\s*\{([^}]{3,400})\}')

# Mesuré au lot 393. Le décompte rend visible l'apparition d'une nouvelle
# promesse déléguée, qui ne serait couverte par aucun des deux gardiens.
NB_PROMESSES = 7
NB_DELEGUEES = 2


def _fichiers():
    out = ['terminal.py']
    for rac, _d, noms in os.walk('vertex'):
        if '__pycache__' in rac:
            continue
        out += [os.path.join(rac, n) for n in sorted(noms) if n.endswith('.py')]
    return out


def _propres(fn):
    """Nœuds de la fonction SANS descendre dans les fonctions imbriquées —
    le correctif du lot 375, sans lequel `pack()` était comparé à la promesse
    de sa fonction englobante."""
    out = []

    def rec(n, racine=False):
        for c in ast.iter_child_nodes(n):
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)) \
                    and not racine:
                continue
            out.append(c)
            rec(c)

    rec(fn, racine=True)
    return out


def _promesses():
    """[(fichier, fonction, a_un_retour_litteral)]"""
    out = []
    for chemin in _fichiers():
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for fn in ast.walk(arbre):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not PROMESSE.search(ast.get_docstring(fn) or ''):
                continue
            rets = [n for n in _propres(fn)
                    if isinstance(n, ast.Return) and n.value is not None]
            out.append((chemin, fn.name, any(isinstance(r.value, ast.Dict) for r in rets)))
    return out


# ── 1. Le dénominateur ──────────────────────────────────────────────────────

def test_le_detecteur_de_promesses_voit_toujours_quelque_chose():
    """Sans lui, « 0 promesse fausse » serait vrai pour la mauvaise raison
    (leçon des lots 375-377)."""
    p = _promesses()
    assert len(p) == NB_PROMESSES, (
        '%d fonctions portant une promesse « Retourne {…} », %d mesurées au '
        'lot 393 — refaire la mesure : une nouvelle promesse déléguée ne serait '
        'couverte par aucun gardien' % (len(p), NB_PROMESSES))


def test_la_part_deleguee_reste_celle_qui_est_verifiee_ici():
    """Si une promesse cessait d'avoir un retour littéral, elle basculerait dans
    l'angle mort du 375 sans que rien ne le signale."""
    deleguees = [(c, f) for c, f, litt in _promesses() if not litt]
    assert len(deleguees) == NB_DELEGUEES, (
        '%d promesses sans retour littéral, %d couvertes ici : %s — les '
        'nouvelles doivent être vérifiées PAR EXÉCUTION et inscrites dans ce '
        'gardien' % (len(deleguees), NB_DELEGUEES, deleguees))


# ── 2. Les deux promesses déléguées, vérifiées PAR EXÉCUTION ───────────────

def test_grade_packet_tient_sa_promesse():
    td = importlib.import_module('test_data_sources')
    from vertex.data_sources import quality

    pkt = td.M.AnalyticsPacket('NVDA')
    pkt.set_source('spot', td.P.stamp(495.0, td.M.SOURCE_IBKR, td.M.MODE_LIVE, now=td.NOW))
    pkt.set_source('options', td.P.stamp([{}], td.M.SOURCE_IBKR, td.M.MODE_DELAYED,
                                         now=td.NOW))
    rendu = quality.grade_packet(pkt)
    promises = {'overall', 'warnings', 'actionable_allowed'}
    manquantes = promises - set(rendu or {})
    assert not manquantes, (
        'grade_packet annonce %s et ne rend pas %s — une promesse de retour '
        'fausse : l\'appelant lit une clé absente' % (sorted(promises), sorted(manquantes)))


def test_select_calls_tient_sa_promesse():
    te = importlib.import_module('test_options_engine')

    rendu = te.call_selector.select_calls(te.liquid_chain(), te.setup_long(),
                                          te.PROFILE, rate_curve=te.CURVE)
    promises = {'per_category', 'primary', 'rejected', 'notes'}
    manquantes = promises - set(rendu or {})
    assert not manquantes, (
        'select_calls annonce %s et ne rend pas %s — promesse de retour fausse'
        % (sorted(promises), sorted(manquantes)))


# ── 3. Le troisième cas : promesse en identifiants nus, vérifiée statiquement

def test_options_for_position_ne_promet_rien_qui_manque():
    """Sa docstring énumère les clés d'une suggestion en identifiants NUS (sans
    quotes) ; le constructeur est le `pack()` interne. Sous-déclaration tolérée
    (`delta` non annoncé), promesse fausse interdite."""
    arbre = ast.parse(open('vertex/engines/recommendation.py', encoding='utf-8').read())
    fn = next(n for n in ast.walk(arbre)
              if isinstance(n, ast.FunctionDef) and n.name == 'options_for_position')
    doc = ast.get_docstring(fn) or ''
    bloc = re.search(r'suggestions:\s*\[\{([^}]+)\}\]', doc)
    assert bloc, 'la docstring n\'énumère plus les clés de suggestion — mesure à refaire'
    annoncees = {m for m in re.findall(r'[a-z_]{3,}', bloc.group(1))}

    pack = next(n for n in ast.walk(fn)
                if isinstance(n, ast.FunctionDef) and n.name == 'pack')
    rendues = set()
    for r in ast.walk(pack):
        if isinstance(r, ast.Return) and isinstance(r.value, ast.Dict):
            rendues |= {k.value for k in r.value.keys
                        if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    assert rendues, 'pack() ne renvoie plus de dict littéral — mesure à refaire'
    manquantes = annoncees - rendues
    assert not manquantes, (
        'options_for_position annonce %s que `pack()` ne rend pas : promesse '
        'fausse' % sorted(manquantes))


def test_la_sous_declaration_connue_reste_une_sous_declaration():
    """Anti-péremption de la caractérisation du lot 375 : `pack()` rend une clé
    de plus que la docstring n'en annonce. Tolérée — mais si l'écart changeait
    de sens, il faudrait le revoir."""
    arbre = ast.parse(open('vertex/engines/recommendation.py', encoding='utf-8').read())
    fn = next(n for n in ast.walk(arbre)
              if isinstance(n, ast.FunctionDef) and n.name == 'options_for_position')
    pack = next(n for n in ast.walk(fn)
                if isinstance(n, ast.FunctionDef) and n.name == 'pack')
    rendues = set()
    for r in ast.walk(pack):
        if isinstance(r, ast.Return) and isinstance(r.value, ast.Dict):
            rendues |= {k.value for k in r.value.keys if isinstance(k, ast.Constant)}
    assert len(rendues) == 13, (
        '`pack()` rend %d clés, 13 mesurées aux lots 375 et 393 — revoir '
        'l\'écart avec la docstring (12 annoncées, `delta` non déclarée)'
        % len(rendues))
