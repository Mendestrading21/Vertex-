"""ENG-04 — un seul verdict = un seul mot + une seule couleur PARTOUT.

Les 5 décisions finales constitutionnelles doivent avoir une sémantique d'affichage
UNIQUE et COHÉRENTE, dérivée d'une source unique (`constitution.FINAL_DECISION_TONES`) :
- polarité correcte : positif → vert, prudence → ambre, négatif/risque → rouge ;
- contrat visuel Black Glass « zéro bleu » : aucune décision finale n'est bleue ;
- jamais de repli gris (« n/d ») : chaque décision a une tonalité sémantique pleine ;
- le badge CSS (`data-decision`) et le vocabulaire JS (`__VXVOCAB`) racontent la MÊME
  histoire — pas d'ATTENDRE ambre d'un côté et bleu de l'autre.

Régression (une décision redevient bleue/grise, ou une source diverge) = test rouge.
"""
from pathlib import Path

import pytest

from vertex.engines import recommendation as reco
from vertex.strategy.constitution import (
    ALLOWED_FINAL_DECISIONS,
    FINAL_DECISION_TONES,
)

ROOT = Path(__file__).resolve().parents[1]

# Polarité attendue de chaque décision canonique (indépendante de l'implémentation).
EXPECTED_TONE = {
    'ACHETER': 'green', 'RENFORCER': 'green',
    'ATTENDRE': 'amber',
    'REDUIRE': 'red', 'REFUSER': 'red',
}


def test_source_unique_couvre_exactement_les_decisions_autorisees():
    assert set(FINAL_DECISION_TONES) == set(ALLOWED_FINAL_DECISIONS)


@pytest.mark.parametrize('decision', ALLOWED_FINAL_DECISIONS)
def test_chaque_decision_a_la_bonne_polarite(decision):
    cell = reco.normalize(decision)
    assert cell['tone'] == EXPECTED_TONE[decision], (
        f'{decision} devrait être {EXPECTED_TONE[decision]}, obtenu {cell["tone"]}')


@pytest.mark.parametrize('decision', ALLOWED_FINAL_DECISIONS)
def test_aucune_decision_finale_n_est_bleue(decision):
    # « zéro bleu » : le bleu est réservé (et neutralisé) — jamais une décision finale.
    assert reco.normalize(decision)['tone'] != 'blue'


@pytest.mark.parametrize('decision', ALLOWED_FINAL_DECISIONS)
def test_aucune_decision_finale_ne_tombe_en_gris(decision):
    # gris = « inconnu/n-d » : une décision canonique DOIT être reconnue.
    cell = reco.normalize(decision)
    assert cell['tone'] != 'gray' and cell['cls'] != 'p-mut'


@pytest.mark.parametrize('decision', ALLOWED_FINAL_DECISIONS)
def test_le_libelle_remonte_aussi_par_le_mot_affiche(decision):
    # normalize(clé) et normalize(LIBELLÉ) doivent donner la même tonalité (cohérence mot↔couleur).
    label = FINAL_DECISION_TONES[decision][0]
    assert reco.normalize(label)['tone'] == reco.normalize(decision)['tone']


def test_le_badge_css_data_decision_raconte_la_meme_histoire():
    """Le CSS (badge `data-decision`) et le vocabulaire partagent la même polarité.

    On lit les blocs `[data-decision="X"]` de la CSS et on vérifie que la variable de
    couleur utilisée est cohérente avec la tonalité canonique (vert/ambre/rouge).
    """
    import re
    css_files = list((ROOT / 'vertex' / 'static' / 'vertex' / 'css').rglob('*.css'))
    blob = '\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in css_files)
    # famille de variable attendue par tonalité (tokens --vx-*)
    tone_token = {'green': ('pos', 'green', 'gain', 'up'),
                  'amber': ('warn', 'amber', 'caution'),
                  'red': ('neg', 'red', 'loss', 'down', 'risk')}
    seen = 0
    for decision, expected in EXPECTED_TONE.items():
        # capture le corps de la règle [data-decision="DECISION"] { ... }
        for m in re.finditer(r'\[data-decision\s*=\s*"%s"\]\s*\{([^}]*)\}' % decision, blob):
            body = m.group(1).lower()
            if 'color' not in body and 'background' not in body:
                continue
            seen += 1
            assert any(tok in body for tok in tone_token[expected]), (
                f'badge {decision} : couleur CSS incohérente avec {expected} → {body!r}')
    # au moins une règle a été vérifiée (sinon le test ne prouve rien)
    assert seen >= 1, 'aucune règle [data-decision] trouvée — le contrat badge a disparu ?'
