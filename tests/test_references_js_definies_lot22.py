"""Gardien : une aide appelée par une page doit être définie quelque part.

## Le défaut

`opportunities_page.py` appelait **six** fonctions introuvables dans tout le
dépôt : `VERD_FR`, `verdictDir`, `verdictWord`, `pbText`, `pbIcon`, `heatCell`.
Chacune levait un `ReferenceError` dès qu'elle s'exécutait.

Aucun contrôle ne l'attrapait, et pour une raison précise : **en démo, le scan
rend zéro ligne**. Les six chemins concernés ne s'exécutaient donc jamais. La
page paraissait saine — 0 erreur console, 0 bloc vide, suite verte — alors que
sa vue principale tombait dès la première carte avec un scan réel.

Trouvé en **injectant un scan fictif dans le navigateur**, pas en relisant.

## Ce que ce banc garde

Que ces six-là restent définies. Il ne prétend pas être un analyseur
JavaScript : il vérifie nommément celles dont l'absence a déjà cassé une page,
et refuse qu'un appel réapparaisse sans sa définition.
"""
import io
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: (fichier, nom, motif de définition acceptable)
AIDES = [
    ('vertex/ui/pages/opportunities_page.py', 'VERD_FR', r'\bconst\s+VERD_FR\s*='),
    ('vertex/ui/pages/opportunities_page.py', 'verdictDir', r'\bfunction\s+verdictDir\s*\('),
    ('vertex/ui/pages/opportunities_page.py', 'verdictWord', r'\bfunction\s+verdictWord\s*\('),
    ('vertex/ui/pages/opportunities_page.py', 'pbText', r'\bfunction\s+pbText\s*\('),
    ('vertex/ui/pages/opportunities_page.py', 'pbIcon', r'\bfunction\s+pbIcon\s*\('),
    ('vertex/ui/pages/opportunities_page.py', 'heatCell', r'\bfunction\s+heatCell\s*\('),
]


def _lire(rel):
    return io.open(os.path.join(RACINE, rel), encoding='utf-8').read()


def test_chaque_aide_appelee_est_definie():
    manquantes = []
    for rel, nom, motif in AIDES:
        src = _lire(rel)
        appelee = re.search(r'(?<![\w$.])' + re.escape(nom) + r'\s*[\[(]', src)
        definie = re.search(motif, src)
        if appelee and not definie:
            manquantes.append('%s : %s appelée, jamais définie' % (rel.split('/')[-1], nom))
    assert not manquantes, (
        "Ces aides sont appelées et introuvables — la page lève un "
        "ReferenceError dès que le chemin s'exécute. En démo le scan rend zéro "
        "ligne, donc RIEN ne le montre :\n  " + '\n  '.join(manquantes))


def test_le_libelle_du_verdict_vient_du_vocabulaire_canonique():
    """Un libellé de verdict ne s'invente pas dans une page.

    `VERD_FR` doit se construire depuis `window.__VXVOCAB`, servi par
    `recommendation.vocab_js()`. Une table écrite à la main divergerait du
    moteur au premier ajout de verdict, en silence.
    """
    src = _lire('vertex/ui/pages/opportunities_page.py')
    bloc = src[src.index('const VERD_FR'):src.index('const VERD_FR') + 400]
    assert '__VXVOCAB' in bloc, (
        'VERD_FR ne lit plus le vocabulaire canonique : une table écrite à la '
        'main divergerait du moteur au premier verdict ajouté')


def test_le_playbook_est_lu_et_non_rejoue():
    """`pbText`/`pbIcon` lisent `r.playbook`, attaché par `strategy_fit`.

    Rejouer les règles de playbook dans l'interface ferait de Vertex deux
    moteurs qui se contrediraient dès que l'un des deux changerait.
    """
    src = _lire('vertex/ui/pages/opportunities_page.py')
    for nom in ('pbText', 'pbIcon'):
        i = src.index('function %s(' % nom)
        corps = src[i:i + 220]
        assert 'r.playbook' in corps or 'playbook' in corps, (
            '%s ne lit plus `r.playbook` : le playbook viendrait alors de '
            'l\'interface, pas du moteur' % nom)
