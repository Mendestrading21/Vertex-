"""Lot 3 — une position déclarée porte le même schéma quelle que soit la porte.

Mesuré avant ce lot : le modal 2.0 (`VXEntities.openAddModal`) ne demandait ni
objectif, ni devise, ni stratégie, ni frais — le legacy (`vx_kit.addPosition`)
les demande tous. Conséquence : `positions/models.py` lit
`snap.tgt || trade.myTgt` pour `tp1`, donc une position déclarée depuis le 2.0
n'avait JAMAIS d'objectif, dans tout le pipeline. Deux déclarations
« identiques » divergeaient selon la porte d'entrée.

Le schéma historique du desk est le propriétaire canonique. Ce banc tient la
parité du côté 2.0 ; le legacy est éprouvé par ses propres bancs.
"""
from __future__ import annotations

import pathlib
import re

SRC = (pathlib.Path(__file__).resolve().parents[1]
       / 'vertex' / 'static' / 'vertex' / 'js' / 'vx-entities.js')


def _formulaire_et_confirm() -> tuple[str, str]:
    s = SRC.read_text(encoding='utf-8')
    d = s.index("if (dest === 'position') {")
    form = s[d:s.index('`;', d)]
    d2 = s.index("} else if (dest === 'position') {")
    confirm = s[d2:s.index('} else if', d2 + 10)]
    return form, confirm


def test_le_formulaire_2_0_demande_les_champs_du_contrat():
    form, _ = _formulaire_et_confirm()
    for champ, pourquoi in (
            ('f-tgt', "l'objectif — sans lui tp1 reste None dans tout le pipeline"),
            ('f-ccy', 'la devise — DeclaredPosition l\'exige, USD implicite est une invention'),
            ('f-strategy', 'la stratégie — le contrat la porte, le legacy la demande'),
            ('f-fees', 'les frais — le coût déclaré est amputé sans eux')):
        assert champ in form, (
            'le modal 2.0 ne demande plus « %s » : %s.' % (champ, pourquoi))


def test_l_ecriture_2_0_porte_le_schema_historique_complet():
    _, confirm = _formulaire_et_confirm()
    for cle in ('myStop', 'myTgt', 'currency', 'strategy', 'fees',
                'entryPrice', 'entrySnap'):
        assert cle in confirm, (
            "l'écriture 2.0 ne pose plus `%s` : une position déclarée ici "
            'diverge à nouveau de la même déclaration faite depuis le legacy.'
            % cle)
    # l'objectif doit aller DANS le snapshot aussi : models.py lit snap.tgt d'abord
    assert re.search(r'entrySnap\s*:\s*\{[^}]*tgt', confirm), (
        "entrySnap ne porte plus l'objectif (snap.tgt) — models.py le lit en premier."
    )
