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

MISE À JOUR DU 25 AOÛT 2026 — la règle a DÉMÉNAGÉ, sans changer d'un iota.
Elle vivait en ligne dans `terminal.py`, et la phrase qui l'explique était
écrite trois fois ailleurs (message de démarrage, carte « Verrou d'accès »,
`config_validation`) à partir d'une supposition. Les trois mentaient dès que
`VERTEX_LAN=1` ou `PORT` était posé. Le propriétaire unique est désormais
`vertex/app/exposition.py`, et ce gardien l'épingle LÀ — l'intention est
inchangée : personne ne doit pouvoir passer l'écoute par défaut à 0.0.0.0
sans casser la suite.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = (ROOT / 'terminal.py').read_text(encoding='utf-8')

def test_la_regle_d_ecoute_est_exactement_celle_de_l_invariant():
    # La règle elle-même, éprouvée sur son propriétaire : verrou actif OU
    # opt-in explicite VERTEX_LAN=1 OU cloud ($PORT) → LAN ; sinon local seul.
    from vertex.app.exposition import exposition
    assert exposition(False, {})['hote'] == '127.0.0.1'
    assert exposition(True, {})['hote'] == '0.0.0.0'
    assert exposition(False, {'VERTEX_LAN': '1'})['hote'] == '0.0.0.0'
    assert exposition(False, {'VERTEX_LAN': '0'})['hote'] == '127.0.0.1'
    assert exposition(False, {'PORT': '10000'})['hote'] == '0.0.0.0'


def test_terminal_LIT_la_regle_au_lieu_de_la_recalculer():
    # Ce que le gardien d'origine protégeait vraiment : que personne ne
    # réécrive la décision ailleurs. Deux copies divergent toujours.
    assert 'from vertex.app.exposition import' in SRC
    assert "lan_ok = AUTH_ON or" not in SRC


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


def test_la_config_documente_la_consequence_REELLE_du_sans_code(monkeypatch):
    # `config_validation` explique la conséquence à l'utilisateur. Le message
    # était FIGÉ — « 127.0.0.1 uniquement » — et servi tel quel même quand
    # `VERTEX_LAN=1` ou `PORT` ouvrait l'écoute à tout le réseau. Il est
    # désormais calculé : ce banc garde les DEUX cas.
    from vertex.app.config_validation import validate_config

    monkeypatch.delenv('VERTEX_LAN', raising=False)
    monkeypatch.delenv('PORT', raising=False)
    local = validate_config()['VERTEX_CODE']['consequence']
    assert re.search(r"127\.0\.0\.1 uniquement", local)

    monkeypatch.setenv('PORT', '10000')
    expose = validate_config()['VERTEX_CODE']['consequence']
    assert '0.0.0.0' in expose and 'PORT' in expose
    assert '127.0.0.1 uniquement' not in expose, (
        "la consequence promettait une restriction absente")
