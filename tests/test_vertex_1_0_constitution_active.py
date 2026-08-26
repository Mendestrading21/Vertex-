"""Vertex 1.0 — LE DÉMARRAGE AUTOMATIQUE APPLIQUAIT UNE AUTRE CONSTITUTION.

`CLAUDE.md` : « la constitution stratégique ne change qu'au moyen d'une nouvelle
version explicite et revue humainement ». Elle changeait selon la **commande de
lancement**, et rien ne l'affichait.

## Le recensement du 26 août 2026

| lanceur | commande | constitution |
|---|---|---|
| `Lancer_VERTEX.bat` | `python -m vertex` | **V4** |
| `Lancer_VERTEX_DEMO.bat` | `python -m vertex` | **V4** |
| `render.yaml` | `gunicorn vertex.runtime:app` | **V4** |
| `Installer_Demarrage_Auto.bat` | `pythonw terminal.py` | **V3** |

Le dernier est celui du **démarrage automatique de Windows** — celui qui fait
tourner Vertex à chaque ouverture de session, donc la façon dont il tourne le
plus souvent chez qui l'a installé. Il court-circuitait `vertex.runtime`, donc
`activate_release_profile()`, donc V4.

Ce n'était pas un oubli de conception : `vertex/strategy/release.py` déclare
qu'« un lancement direct de `terminal.py` reste **volontairement** un mode
legacy ». Le défaut est qu'un **lanceur livré à l'utilisateur** empruntait ce
mode legacy, sans le dire.

## Les deux constitutions diffèrent sur 29 points

Pas une révision cosmétique — un autre mandat :

| | V3 (démarrage auto) | V4 (nommée par `CLAUDE.md`) |
|---|---|---|
| `swing_3_6m.preferred_dte` | `[90, 180]` | `[120, 240]` |
| `swing_3_6m.target_dte` | 135 | **180** |
| `universes.SWING_3_6M` | `[75, 210]` | `[120, 240]` |
| `holding_period_days.maximum` | 28 | 45 |
| `profit_management.time_stop_sessions` | `[5, 8]` | `[30, 45]` |
| `equity_profile` (3/6/12 mois) | **absent** | présent |
| `holding_period_weeks` (2/4/6) | **absent** | présent |
| `daily_intelligence` (WMB Brief) | **absent** | présent |

Les horizons actions 3/6/12 mois et les revues à 2/4/6 semaines — deux
invariants du mandat — n'existent **pas** dans V3.

## Ce que ce lot fait

Le lanceur passe par `-m vertex`, et `/healthz` **dit** quelle constitution
s'applique : version, identifiant, répertoire, activation, et la fenêtre DTE
réellement en vigueur. Un état qui dépend de la commande de lancement doit être
lisible depuis le produit, sinon personne ne saura lequel des deux mandats il
regarde.
"""
from __future__ import annotations

import json
import os
import pathlib
import re

import pytest

RACINE = pathlib.Path(__file__).resolve().parents[1]


#  ═══════════  1. aucun lanceur livré ne court-circuite le runtime  ═══════════

def test_AUCUN_lanceur_ne_demarre_terminal_directement():
    """Le recensement qui a trouvé le défaut. `Installer_Demarrage_Auto.bat`
    lançait `pythonw terminal.py` — donc V3, à chaque ouverture de session."""
    coupables = []
    for bat in sorted(RACINE.glob('*.bat')):
        src = bat.read_text(encoding='utf-8', errors='replace')
        for ligne in src.splitlines():
            if re.search(r'python\w*\.exe\\?"?\s+terminal\.py', ligne):
                coupables.append('%s : %s' % (bat.name, ligne.strip()[:90]))
    assert coupables == [], (
        'lanceurs qui court-circuitent vertex.runtime (donc V4) :\n'
        + '\n'.join(coupables))


def test_le_recensement_LIT_vraiment_les_lanceurs():
    """Sans ce contrôle, « aucun coupable » voudrait dire « je n'ai rien lu »."""
    bats = list(RACINE.glob('*.bat'))
    assert len(bats) >= 3, 'lanceurs introuvables : %s' % bats
    assert any(b.name == 'Installer_Demarrage_Auto.bat' for b in bats)


def test_le_recensement_VOIT_la_forme_fautive_qu_on_lui_montre():
    """Contre-épreuve — D-031, payé six fois : un gardien qui ne trouve jamais
    rien passerait pour un gardien qui garde."""
    fautif = r'/tr "cmd /c cd /d \"%~dp0\" ^&^& \".venv\Scripts\pythonw.exe\" terminal.py"'
    assert re.search(r'python\w*\.exe\\?"?\s+terminal\.py', fautif)


def test_le_recensement_n_accuse_PAS_la_forme_corrigee():
    """Un gardien qui refuse aussi la correction est désactivé au premier
    commit pressé."""
    sain = r'\".venv\Scripts\pythonw.exe\" -m vertex'
    assert not re.search(r'python\w*\.exe\\?"?\s+terminal\.py', sain)


def test_tous_les_lanceurs_passent_par_le_runtime_canonique():
    """Contre-épreuve positive : ils doivent lancer QUELQUE CHOSE, et ce
    quelque chose doit être `-m vertex`.

    L'installeur du démarrage automatique le fait par **indirection** depuis
    D-141 : il ne lance plus une commande composée — `schtasks /tr` refusait le
    `^&^&` et la tâche n'était jamais créée — mais pointe sur
    `_vertex_autostart.cmd`. Le banc suit donc le fichier désigné : exiger
    `-m vertex` dans l'installeur lui-même interdirait la seule forme qui
    fonctionne.
    """
    for nom in ('Lancer_VERTEX.bat', 'Lancer_VERTEX_DEMO.bat',
                '_vertex_autostart.cmd'):
        src = (RACINE / nom).read_text(encoding='utf-8', errors='replace')
        assert '-m vertex' in src, '%s ne lance pas le runtime canonique' % nom
    #  L'installeur, lui, doit designer ce lanceur — et lui seul.
    inst = (RACINE / 'Installer_Demarrage_Auto.bat').read_text(
        encoding='utf-8', errors='replace')
    assert '_vertex_autostart.cmd' in inst


def test_l_installeur_VERIFIE_la_tache_au_lieu_de_l_affirmer():
    """Le défaut du 26 août 2026 : `schtasks` répondait « Argument ou option
    non valide - '^&^&' », la tâche n'était pas créée, et l'installeur
    affichait quand même « OK : VERTEX demarrera automatiquement ».

    Un statut qui s'affirme sans se vérifier est un mensonge — et celui-là
    portait sur la constitution appliquée (D-110).
    """
    inst = (RACINE / 'Installer_Demarrage_Auto.bat').read_text(
        encoding='utf-8', errors='replace')
    #  Le message de succes doit venir APRES une interrogation de la tache.
    i_ok = inst.index('OK : la tache VertexAutoStart')
    avant = inst[:i_ok]
    assert avant.count('schtasks /query') >= 2, (
        "le « OK » doit suivre une VERIFICATION, pas un code de retour")
    assert 'echec' in avant.lower() or 'Echec' in avant


def test_l_installeur_ne_compose_PLUS_de_commande():
    """`schtasks /tr` ne reçoit pas de commande composée. Le `^&^&` qui a
    empêché toute création ne doit pas revenir — hors du commentaire qui
    explique le défaut."""
    inst = (RACINE / 'Installer_Demarrage_Auto.bat').read_text(
        encoding='utf-8', errors='replace')
    fautives = [l for l in inst.splitlines()
                if '^&^&' in l and not l.strip().upper().startswith('REM')]
    assert fautives == [], fautives


def test_le_deploiement_distant_passe_aussi_par_le_runtime():
    src = (RACINE / 'render.yaml').read_text(encoding='utf-8', errors='replace')
    assert 'vertex.runtime:app' in src
    assert 'terminal:app' not in src


#  ═══════════  2. les deux constitutions diffèrent VRAIMENT  ══════════════════

def _profil(chemin):
    return json.loads((RACINE / chemin).read_text(encoding='utf-8'))


def test_V3_et_V4_ne_sont_PAS_la_meme_doctrine():
    """Si l'écart était cosmétique, ce lot serait du zèle. Il ne l'est pas."""
    from vertex.strategy.constitution import diff_profiles
    v3 = _profil('vertex/strategy/profiles/vertex_strategy_v3.json')
    v4 = _profil('vertex/strategy/release_profiles/vertex_strategy_v4.json')
    ecarts = diff_profiles(v3, v4)
    assert len(ecarts) >= 25, 'seulement %d ecarts' % len(ecarts)


def test_V3_ignore_les_horizons_ACTIONS_du_mandat():
    """« Actions : horizons 3/6/12 mois » — invariant `CLAUDE.md`, absent de V3."""
    v3 = _profil('vertex/strategy/profiles/vertex_strategy_v3.json')
    v4 = _profil('vertex/strategy/release_profiles/vertex_strategy_v4.json')
    assert 'equity_profile' not in v3
    assert v4['equity_profile']['decision_horizons_months'] == [3, 6, 12]


def test_V3_ignore_les_revues_a_2_4_6_semaines():
    """« détention typique 2/4/6 semaines » — invariant `CLAUDE.md`."""
    v3 = _profil('vertex/strategy/profiles/vertex_strategy_v3.json')
    v4 = _profil('vertex/strategy/release_profiles/vertex_strategy_v4.json')
    assert 'holding_period_weeks' not in (v3.get('options_profile') or {})
    assert (v4['options_profile']['holding_period_weeks']['preferred_checkpoints']
            == [2, 4, 6])


def test_la_fenetre_DTE_du_mandat_est_bien_celle_de_V4():
    """« DTE préféré 120–240 ; cible 180 » — `CLAUDE.md`."""
    v4 = _profil('vertex/strategy/release_profiles/vertex_strategy_v4.json')
    swing = v4['options_profile']['swing_3_6m']
    assert swing['preferred_dte'] == [120, 240]
    assert swing['target_dte'] == 180


#  ═══════════  3. l'état actif est LISIBLE  ═══════════════════════════════════

def test_le_temoin_distingue_les_DEUX_modes():
    """Le cœur du lot : un état qui dépend de la commande de lancement doit
    être lisible, sinon personne ne sait lequel des deux mandats il regarde."""
    from vertex.strategy import release as R
    legacy = R._ORIGINAL_LOAD_PROFILE(
        profiles_dir=RACINE / 'vertex' / 'strategy' / 'profiles')
    canonique = R.load_release_profile()
    assert legacy.version == 3 and canonique.version == 4
    assert legacy.options_profile['swing_3_6m']['preferred_dte'] == [90, 180]
    assert canonique.options_profile['swing_3_6m']['preferred_dte'] == [120, 240]


def test_l_etat_actif_nomme_le_repertoire_ET_la_fenetre():
    """Nommer la version ne suffit pas : c'est la fenêtre DTE qui change la
    décision, et c'est elle qu'il faut pouvoir lire."""
    from vertex.strategy import release as R
    R.activate_release_profile()
    e = R.etat_actif()
    assert e['version'] == 4
    assert e['strategy_id'] == 'vertex_strategy_v4'
    assert e['repertoire'] == 'release_profiles'
    assert e['release_active'] is True
    assert e['dte_prefere'] == [120, 240] and e['dte_cible'] == 180
    assert e['erreur'] is None
    assert e['read_only'] is True


def test_l_etat_actif_AVOUE_une_erreur_au_lieu_de_taire_la_version():
    """Un témoin qui rendrait `version: None` sans dire pourquoi laisserait
    croire à un champ non implémenté plutôt qu'à une constitution illisible."""
    from vertex.strategy import release as R
    vrai = R.constitution.load_profile

    def casse(*a, **k):
        raise RuntimeError('profil illisible')
    R.constitution.load_profile = casse
    try:
        e = R.etat_actif()
        assert e['version'] is None
        assert e['erreur'] and 'illisible' in e['erreur']
    finally:
        R.constitution.load_profile = vrai


#  ═══════════  4. /healthz le dit  ════════════════════════════════════════════

@pytest.fixture()
def client(tmp_path, monkeypatch):
    os.environ.setdefault('NO_IBKR', '1')
    os.environ.setdefault('START_ON_IMPORT', '0')
    from vertex.services import persist
    monkeypatch.setattr(persist, '_BASE_DIR', str(tmp_path))
    from vertex.strategy.release import activate_release_profile
    activate_release_profile()
    import terminal
    return terminal.app.test_client()


def test_healthz_DIT_quelle_constitution_s_applique(client):
    r = client.get('/healthz')
    assert r.status_code == 200
    c = r.get_json()['constitution']
    assert c['version'] == 4
    assert c['dte_prefere'] == [120, 240]
    assert c['release_active'] is True


def test_healthz_reste_disponible_et_sans_donnee_sensible(client):
    """Ce point de contrôle est interrogé par l'hébergeur : il ne doit ni
    tomber, ni exposer autre chose que de l'état."""
    corps = client.get('/healthz').get_data(as_text=True)
    assert client.get('/healthz').status_code == 200
    for interdit in ('VERTEX_CODE', 'password', 'token', 'U1036'):
        assert interdit not in corps


def test_la_route_alias_expose_la_meme_chose(client):
    a = client.get('/healthz').get_json()['constitution']
    b = client.get('/api/healthz').get_json()['constitution']
    assert a == b
