# -*- coding: utf-8 -*-
"""LOT 218 — gardien de l'invariant CLAUDE.md « sans code d'accès, le
serveur n'écoute que 127.0.0.1 » (exposition réseau intelligente).

Lacune mesurée au lot 218 : la règle d'écoute vivait dans terminal.py
(_start_app) sans AUCUN test (« lan_ok », « 0.0.0.0 », « VERTEX_LAN »
absents de tests/) — on pouvait passer l'écoute par défaut à 0.0.0.0
et exposer le desk à tout le Wi-Fi sans casser la suite.

La règle est épinglée à la SOURCE (le bloc __main__ ne s'exécute pas
sous pytest) puis re-déroulée en table de vérité sur la même expression,
pour garder la LOGIQUE et pas seulement le texte.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / 'terminal.py').read_text(encoding='utf-8')

LAN_OK = "lan_ok = AUTH_ON or os.environ.get('VERTEX_LAN') == '1' or 'PORT' in os.environ"
HOST = "host = '0.0.0.0' if lan_ok else '127.0.0.1'"


def test_la_regle_d_ecoute_est_exactement_celle_de_l_invariant():
    # Les deux lignes de la décision, telles quelles : verrou actif OU
    # opt-in explicite VERTEX_LAN=1 OU cloud ($PORT) → LAN ; sinon local seul.
    assert LAN_OK in SRC
    assert HOST in SRC


def test_le_repli_par_defaut_reste_127_0_0_1():
    # Table de vérité re-déroulée sur la MÊME expression que la source
    # (si la ligne source change, le test au-dessus casse d'abord).
    def decide(auth_on, env):
        lan_ok = auth_on or env.get('VERTEX_LAN') == '1' or 'PORT' in env
        return '0.0.0.0' if lan_ok else '127.0.0.1'

    assert decide(False, {}) == '127.0.0.1'                    # défaut : local SEUL
    assert decide(True, {}) == '0.0.0.0'                       # verrou VERTEX_CODE actif
    assert decide(False, {'VERTEX_LAN': '1'}) == '0.0.0.0'     # opt-in explicite
    assert decide(False, {'VERTEX_LAN': '0'}) == '127.0.0.1'   # opt-in raté ≠ opt-in
    assert decide(False, {'PORT': '10000'}) == '0.0.0.0'       # cloud (Render impose $PORT)


def test_la_config_documente_la_consequence_du_sans_code():
    # config_validation explique la conséquence à l'utilisateur — le message
    # doit rester honnête (« 127.0.0.1 uniquement »), pas prometteur.
    cfg = (ROOT / 'vertex' / 'app' / 'config_validation.py').read_text(encoding='utf-8')
    assert re.search(r"127\.0\.0\.1 uniquement", cfg)
