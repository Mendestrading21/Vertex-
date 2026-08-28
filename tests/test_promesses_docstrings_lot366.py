"""
LOT 366 — Généralisation du lot 365 : un moteur annonce-t-il, dans sa
docstring, des sorties qu'il ne produit pas ?

Le lot 365 avait trouvé `thesis_health` annonçant la dimension PORTFOLIO_FIT
sans jamais la calculer. Ce lot a passé les **110 modules** de `vertex/engines`,
`vertex/positions`, `vertex/options`, `vertex/scanner`, `vertex/strategy` et
`vertex/ai` à la même question. Verdict : **la trouvaille du lot 365 était
isolée**, aucune autre promesse non tenue.

Deux enseignements de méthode, payés comptant pendant l'audit :

  1. Une première passe cherchait tout jeton MAJUSCULE de ≥4 lettres →
     **139 « suspects »**, noyés dans les mots français en capitales
     (ANOMALIES, PORTEFEUILLE, CROISSANCE…). Inexploitable. Le filtre retenu
     exige un **souligné** : un identifiant machine, pas un mot de prose.
     10 candidats, triables à la main.
  2. Chercher l'identifiant **dans le seul module** produit des faux positifs :
     `ULTRA_CONVEX` et `MODEL_ESTIMATE` sont bien produits, mais via
     `vertex/options/models.py` (`CALL_CATEGORIES`, `GREEKS_MODEL`). La
     recherche doit couvrir le **paquet**.

Contrat figé ici : tout identifiant machine (CAPS_SNAKE) cité dans la docstring
d'un module de moteur doit exister dans le code du paquet `vertex/`, sauf s'il
appartient à l'une des familles légitimes recensées ci-dessous — noms de
contrats de gouvernance, notation mathématique, et l'absence assumée de
PORTFOLIO_FIT (lot 365).
"""
import ast
import os
import re

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_RACINES = ('vertex/engines', 'vertex/positions', 'vertex/options',
            'vertex/scanner', 'vertex/strategy', 'vertex/ai')

# Identifiant MACHINE : souligné exigé (sinon on ramasse la prose française).
_PAT = re.compile(r'\b([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)+)\b')

# Familles légitimes, recensées et vérifiées au lot 366.
_CONTRATS_GOUVERNANCE = {          # vivent dans .claude/skills/… et les rapports
    'SKYLER_ARCHITECTURE', 'ADVERSARIAL_COMMITTEE', 'OPTIONS_CORRECTNESS',
    'SCENARIO_CALIBRATION', 'DECISION_ENGINE', 'PORTFOLIO_FIT',
}
_NOTATION_MATH = {'S_T'}
_TOLERES = _CONTRATS_GOUVERNANCE | _NOTATION_MATH


def _modules():
    out = []
    for rel in _RACINES:
        for racine, dirs, noms in os.walk(os.path.join(_ROOT, rel)):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            out += [os.path.join(racine, n) for n in noms
                    if n.endswith('.py') and n != '__init__.py']
    return sorted(out)


@pytest.fixture(scope='module')
def code_du_paquet():
    """Tout le code de `vertex/`, docstrings de module retirées."""
    morceaux = []
    for racine, dirs, noms in os.walk(os.path.join(_ROOT, 'vertex')):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for n in noms:
            if not n.endswith('.py'):
                continue
            with open(os.path.join(racine, n), encoding='utf-8',
                      errors='ignore') as f:
                src = f.read()
            try:
                doc = ast.get_docstring(ast.parse(src), clean=False)
            except SyntaxError:
                doc = None
            morceaux.append(src.replace(doc, '', 1) if doc else src)
    return '\n'.join(morceaux)


def test_le_gardien_ne_tourne_pas_a_vide():
    fichiers = _modules()
    assert len(fichiers) >= 90, 'le balayage des moteurs ne trouve plus rien'
    avec_doc = 0
    for chemin in fichiers:
        with open(chemin, encoding='utf-8', errors='ignore') as f:
            try:
                if ast.get_docstring(ast.parse(f.read())):
                    avec_doc += 1
            except SyntaxError:
                pass
    assert avec_doc >= 60, 'plus assez de docstrings de module pour vérifier'


def test_aucun_moteur_n_annonce_une_sortie_qu_il_ne_produit_pas(code_du_paquet):
    fautes = []
    for chemin in _modules():
        with open(chemin, encoding='utf-8', errors='ignore') as f:
            src = f.read()
        try:
            doc = ast.get_docstring(ast.parse(src), clean=False) or ''
        except SyntaxError:
            continue
        for jeton in sorted(set(_PAT.findall(doc))):
            if jeton in _TOLERES:
                continue
            motif = r'\b%s\b' % re.escape(jeton)
            if re.search(motif, code_du_paquet) or \
                    re.search(r'\b%s\b' % re.escape(jeton.lower()), code_du_paquet):
                continue
            fautes.append('%s annonce %s (introuvable dans le code)'
                          % (os.path.relpath(chemin, _ROOT), jeton))
    assert fautes == [], (
        'promesse de docstring non tenue — corriger la DOC (jamais implémenter '
        'à la volée un calcul manquant, règle du lot 365) : %s' % '; '.join(fautes))


def test_les_familles_tolerees_restent_justifiees():
    # Une tolérance sans justification devient un trou : chaque contrat de
    # gouvernance cité doit exister dans le skill ou les rapports.
    corpus = []
    skill_root = os.path.join(_ROOT, '.claude/skills/vertex-2-0')
    for racine, _, noms in os.walk(skill_root):
        for nom in noms:
            if nom.endswith('.md'):
                with open(os.path.join(racine, nom), encoding='utf-8',
                          errors='ignore') as f:
                    corpus.append(f.read())
    for racine, _, noms in os.walk(os.path.join(_ROOT, 'docs')):
        for n in noms:
            if n.endswith('.md'):
                with open(os.path.join(racine, n), encoding='utf-8',
                          errors='ignore') as f:
                    corpus.append(f.read())
    texte = '\n'.join(corpus)
    orphelins = [c for c in sorted(_CONTRATS_GOUVERNANCE) if c not in texte]
    assert orphelins == [], (
        'contrat de gouvernance toléré mais introuvable dans le SKILL ou les '
        'rapports : %s' % orphelins)
