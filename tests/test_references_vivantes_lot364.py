"""
LOT 364 — « ce que le projet dit de lui-même est-il vrai ? », suite du lot 71.

Le lot 71 avait trouvé une docstring citant un gardien INEXISTANT
(`tests/test_readonly_gateway.py`) et posé un contrat : toute référence
`tests/test_*.py` **dans `vertex/`** doit exister. Deux angles morts restaient :

  · le monolithe `terminal.py` n'était pas balayé ;
  · les **documents vivants** (ceux qu'on lit pour décider) non plus.

Audit du lot 364 : 0 chemin de module `vertex/**.py` mort, 0 route `/api/…`
citée hors de l'`url_map` (29 routes citées, toutes réelles), et **7 références
de tests inexistants, toutes dans `docs/`**. Six pointaient vers les trois
gardiens que la purge É1 (lot 323) a elle-même supprimés — comme le plan le
prévoyait, mais sans que rien ne l'écrive. La septième est la citation
historique du défaut du lot 71 lui-même.

Contrat posé ici — un document **vivant** (celui sur lequel on s'appuie
aujourd'hui) peut citer un gardien disparu **à condition de dire qu'il a été
retiré**, sur la même ligne. Les rapports `SKYLER-LOT-NNN.md` sont des
**archives** : ils décrivent l'état de leur époque, on ne les réécrit pas.
"""
import os
import re

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_PAT_TEST = re.compile(r'tests/test_[A-Za-z0-9_]+\.py')
_PAT_MODULE = re.compile(r'vertex/[A-Za-z0-9_/]+\.py')

# Documents VIVANTS : on s'en sert pour décider, ils doivent dire vrai.
_DOCS_VIVANTS = (
    'CLAUDE.md',
    'docs/refactor/validation/ANNEXE-E1-RETRAITS.md',
    'docs/refactor/validation/SKYLER-INDEX.md',
    'docs/skyler/STATUS.md',
)


def _lire(rel):
    with open(os.path.join(_ROOT, rel), encoding='utf-8', errors='ignore') as f:
        return f.read()


def _sources_python():
    fichiers = [os.path.join(_ROOT, 'terminal.py')]
    for racine, dirs, noms in os.walk(os.path.join(_ROOT, 'vertex')):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        fichiers.extend(os.path.join(racine, n) for n in noms if n.endswith('.py'))
    return sorted(fichiers)


# ── 1. Le contrat du lot 71, étendu au monolithe ─────────────────────────────

def test_aucune_source_python_ne_cite_un_gardien_inexistant():
    fautes = []
    for chemin in _sources_python():
        with open(chemin, encoding='utf-8', errors='ignore') as f:
            src = f.read()
        for ref in sorted(set(_PAT_TEST.findall(src))):
            if not os.path.exists(os.path.join(_ROOT, ref)):
                fautes.append('%s -> %s' % (os.path.relpath(chemin, _ROOT), ref))
    assert fautes == [], (
        'la doc ment sur qui garde quoi (lot 71 étendu à terminal.py) : %s'
        % '; '.join(fautes))


def test_aucune_source_python_ne_cite_un_module_inexistant():
    fautes = []
    for chemin in _sources_python():
        with open(chemin, encoding='utf-8', errors='ignore') as f:
            src = f.read()
        for ref in sorted(set(_PAT_MODULE.findall(src))):
            if not os.path.exists(os.path.join(_ROOT, ref)):
                fautes.append('%s -> %s' % (os.path.relpath(chemin, _ROOT), ref))
    assert fautes == [], 'chemin de module cité mais inexistant : %s' % '; '.join(fautes)


# ── 2. Les documents vivants : citer un gardien mort, c'est le dire ──────────

@pytest.mark.parametrize('doc', _DOCS_VIVANTS)
def test_un_document_vivant_qui_cite_un_gardien_disparu_le_signale(doc):
    src = _lire(doc)
    manquants = [r for r in sorted(set(_PAT_TEST.findall(src)))
                 if not os.path.exists(os.path.join(_ROOT, r))]
    non_signales = []
    for ref in manquants:
        nom = os.path.basename(ref)
        # La disparition doit être écrite sur une ligne qui nomme le fichier.
        dit = any(nom in ligne and 'RETIRÉ' in ligne for ligne in src.splitlines())
        if not dit:
            non_signales.append(ref)
    assert non_signales == [], (
        "%s cite un gardien qui n'existe plus sans dire qu'il a été retiré : %s"
        % (doc, ', '.join(non_signales)))


def test_le_gardien_ne_tourne_pas_a_vide():
    # Si les motifs cassaient, tout passerait sans rien vérifier.
    total = sum(len(set(_PAT_TEST.findall(_lire(d)))) for d in _DOCS_VIVANTS)
    assert total >= 5, 'aucune référence de gardien trouvée dans les docs vivants'
    assert len(_sources_python()) >= 150
