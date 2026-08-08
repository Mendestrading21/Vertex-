"""
LOT 365 — Un moteur qui annonce une dimension qu'il ne calcule pas.

Suite du lot 364 (« ce que le projet dit de lui-même est-il vrai ? »), appliquée
aux IDENTIFIANTS cités en prose. Audit : **23 appels `nom()` cités, 0 mort** ;
117 constantes citées, dont 16 qui ne sont pas des identifiants Python (noms de
contrats de gouvernance, notation mathématique `S_T`, nom de document). Une
seule divergence réelle en est sortie :

`vertex/positions/thesis_health.py` annonçait **7 dimensions** —
FUNDAMENTAL, CATALYST, TECHNICAL, SENTIMENT, **PORTFOLIO_FIT**, RISK,
DATA_QUALITY — alors que son code n'en évalue que **cinq** sections
(`# FUNDAMENTAL`, `# CATALYST`, `# TECHNICAL`, `# SENTIMENT`,
`# RISK / DATA_QUALITY`). **Aucune ligne ne regardait l'adéquation au
portefeuille.**

Ce n'est pas anodin : `portfolio_fit` existe vraiment ailleurs
(`vertex/scanner/stages.py`, `vertex/strategy/executive_engine.py`), ce qui rend
la confusion plus facile — on pouvait croire que la santé de thèse en tenait
compte. Elle n'en tient pas compte.

Correctif du lot 365 : la docstring dit désormais ce que le module évalue
**et** ce qu'il n'évalue pas. Aucune dimension n'a été ajoutée — inventer un
calcul aurait été pire que le mensonge.

Contrat figé ici : toute dimension nommée dans la docstring doit exister comme
section du code, et l'absence de PORTFOLIO_FIT doit rester écrite noir sur
blanc tant qu'elle n'est pas implémentée.
"""
import ast
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODULE = os.path.join(_ROOT, 'vertex', 'positions', 'thesis_health.py')


def _source():
    with open(_MODULE, encoding='utf-8') as f:
        return f.read()


def _docstring():
    return ast.get_docstring(ast.parse(_source()), clean=False) or ''


def _sections():
    """Sections évaluées, lues des commentaires de section du corps du module."""
    return {m.group(1).strip()
            for m in re.finditer(r'^\s{4}# ([A-Z][A-Z_ /]+)', _source(), re.M)}


def test_les_sections_du_code_sont_bien_celles_attendues():
    # Anti-vide : si les commentaires de section disparaissaient, les tests
    # suivants passeraient sans rien vérifier.
    sections = _sections()
    assert {'FUNDAMENTAL', 'CATALYST', 'SENTIMENT'} <= sections
    assert any(s.startswith('TECHNICAL') for s in sections)
    assert any('DATA_QUALITY' in s for s in sections)


def test_chaque_dimension_annoncee_existe_dans_le_code():
    doc = _docstring()
    # Les dimensions annoncées comme évaluées sont sur la ligne « Dimensions
    # RÉELLEMENT évaluées ici : … » (jusqu'au tiret d'explication).
    m = re.search(r'Dimensions RÉELLEMENT évaluées ici\s*:(.+?)—', doc, re.S)
    assert m, 'la docstring ne déclare plus ses dimensions évaluées'
    annoncees = {d.strip() for d in re.split(r'[,\n]', m.group(1))
                 if re.fullmatch(r'[A-Z][A-Z_ /]*', d.strip() or 'x')}
    annoncees = {a for a in annoncees if a}
    assert annoncees, 'aucune dimension lisible dans la docstring'

    sections = ' | '.join(_sections())
    manquantes = [a for a in sorted(annoncees)
                  if not all(mot in sections for mot in a.split(' / '))]
    assert manquantes == [], (
        'dimension annoncée mais absente du code : %s (sections réelles : %s)'
        % (manquantes, sorted(_sections())))


def test_portfolio_fit_reste_annonce_comme_NON_evalue():
    doc, src = _docstring(), _source()
    # On cherche dans le CODE seul : la docstring cite légitimement
    # `portfolio_fit` pour dire où il est calculé (ailleurs).
    corps = src.replace(doc, '')
    calcule = bool(re.search(r'^\s{4}# PORTFOLIO_FIT', corps, re.M)
                   or 'portfolio_fit' in corps)
    if calcule:
        # Si un jour la dimension est implémentée, ce gardien doit être revu —
        # c'est exactement son rôle de le réclamer.
        raise AssertionError(
            'PORTFOLIO_FIT semble désormais calculé dans thesis_health : '
            'mettre à jour la docstring ET ce gardien.')
    assert 'PORTFOLIO_FIT' in doc and "n'est PAS évalué ici" in doc, (
        "la docstring doit dire explicitement que PORTFOLIO_FIT n'est pas "
        'évalué ici — sinon le lecteur suppose que la santé de thèse en tient '
        'compte (défaut du lot 365)')
