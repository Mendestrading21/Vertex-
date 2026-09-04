"""Lot 2 — la frontière IBKR market-data-only, gardée par le scanner du skill.

`readonly=True` empêche l'ordre ; il ne protège pas la confidentialité du
compte. Ce banc tient la SECONDE frontière : aucun appel de compte, de
positions, de portefeuille ou de P&L courtier dans le code produit et les
outils — `managedAccounts`, `accountSummary`, `positions`, `portfolio`,
`reqPnL` et leurs voisins, énumérés par le scanner du skill maître.

Le scanner (`check_ibkr_boundary.py`) analyse l'AST — pas les chaînes — de
`terminal.py`, `vertex/` et `tools/`. Ce banc l'exécute en mode `--enforce` :
un seul appel interdit le fait échouer, avec le fichier et la ligne.

Écrit AVANT la migration (13 appels le faisaient échouer), vert depuis
qu'elle est terminée. Toute réintroduction — y compris « juste en lecture
seule », y compris dans un outil — le remet au rouge.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys

SCANNER = (pathlib.Path(__file__).resolve().parents[1]
           / '.claude' / 'skills' / 'vertex-2-0' / 'scripts'
           / 'check_ibkr_boundary.py')


def test_aucun_appel_de_compte_courtier_dans_le_code_produit():
    r = subprocess.run([sys.executable, str(SCANNER), '--enforce'],
                       capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, (
        'La frontière IBKR market-data-only est violée :\n' + r.stdout
    )
