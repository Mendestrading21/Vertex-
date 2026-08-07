# -*- coding: utf-8 -*-
"""LOT 228 — gardien d'intégrité SKYLER-INDEX ↔ rapports de lot.

Le journal de bord de la boucle (SKYLER-INDEX.md + SKYLER-LOT-N.md)
est la mémoire du travail : une référence morte ou un rapport orphelin
la corrompent en silence. Calibré au lot 228 : 218 rapports cités,
TOUS existants ; 13 rapports pré-index (lots 01-09, batch correctness
pré-Institutional+) hors périmètre PAR CONSTRUCTION — le périmètre est
désormais écrit dans l'en-tête de l'index.
"""
import re
import pathlib

DOCS = pathlib.Path(__file__).resolve().parent.parent / 'docs' / 'refactor' / 'validation'
INDEX = DOCS / 'SKYLER-INDEX.md'
PRE_INDEX = re.compile(r'^SKYLER-LOT-0[1-9][A-E]?\.md$')   # lots 01-09 (+08A-E)


def _cited():
    return set(re.findall(r"`(SKYLER-LOT-[\w.-]+\.md)`", INDEX.read_text(encoding='utf-8')))


def test_toute_reference_de_l_index_existe_sur_disque():
    morts = sorted(c for c in _cited() if not (DOCS / c).exists())
    assert morts == [], 'references MORTES dans SKYLER-INDEX : ' + ', '.join(morts)


def test_tout_rapport_du_perimetre_a_sa_ligne_d_index():
    cited = _cited()
    orphelins = sorted(p.name for p in DOCS.glob('SKYLER-LOT-*.md')
                       if p.name not in cited and not PRE_INDEX.match(p.name))
    assert orphelins == [], 'rapports SANS ligne d\'index : ' + ', '.join(orphelins)


def test_le_perimetre_est_documente_dans_l_en_tete():
    head = INDEX.read_text(encoding='utf-8')[:600]
    assert 'lots' in head and '10' in head and 'STATUS.md' in head, (
        'l\'en-tête doit dire que les lots 01-09 vivent hors index (STATUS.md)')


def test_le_gardien_ne_tourne_pas_a_vide():
    # si le format des lignes changeait, _cited() rendrait vide et les deux
    # tests ci-dessus passeraient sans rien vérifier — on exige du volume.
    assert len(_cited()) >= 200
