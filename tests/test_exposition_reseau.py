"""Vertex Test 1.0 — L'ÉCRAN DE SÉCURITÉ AFFIRMAIT UNE PROTECTION ABSENTE.

## Les deux mensonges, mesurés le 25 août 2026

La règle d'écoute vivait en ligne dans `terminal.py` :

```python
lan_ok = AUTH_ON or os.environ.get('VERTEX_LAN') == '1' or 'PORT' in os.environ
host = '0.0.0.0' if lan_ok else '127.0.0.1'
```

…et la **phrase qui l'explique** était écrite **deux fois ailleurs**, à partir
d'une supposition. Les deux mentaient.

**Au démarrage.** Avec `PORT` défini et sans code, le produit écoutait sur
toutes les interfaces et annonçait « **VERTEX_LAN=1 — SANS code !** » — en
nommant une variable qui n'est pas définie. L'opérateur la cherche dans son
`.env`, ne la trouve pas, conclut que le message est périmé. Son desk est
ouvert.

**Sur la page Système.** La carte « Verrou d'accès » affirmait, sans code :

> « par sécurité, le serveur n'écoute que **127.0.0.1** (pas d'accès WiFi/LAN) »

Faux dès que `VERTEX_LAN=1` ou `PORT` est posé — deux cas où il n'y a **ni code
ni restriction**. L'écran de sécurité affirmait une protection absente, à propos
du portefeuille réel de l'utilisateur.

## Ce que ce lot ne change pas

**Aucun comportement d'écoute.** La règle est reprise à l'identique, `PORT`
compris : un hébergeur comme Render impose ce port et exige `0.0.0.0`, et l'y
contraindre casserait le déploiement. La cause du défaut n'était pas la règle —
c'était qu'elle était *décrite* à deux endroits qui ne la lisaient pas.
"""
from __future__ import annotations

import pytest

from vertex.app.exposition import (LOCAL, MOTIF_LAN, MOTIF_LOCAL, MOTIF_PORT,
                                   MOTIF_VERROU, TOUTES, exposition, phrase)
from vertex.ui.pages.system_page import _lock_card


#  ═══════════  1. la règle d'écoute est INCHANGÉE  ════════════════════════════

@pytest.mark.parametrize('auth,env,attendu', [
    (False, {}, LOCAL),
    (True, {}, TOUTES),
    (False, {'VERTEX_LAN': '1'}, TOUTES),
    (False, {'PORT': '5002'}, TOUTES),
    (True, {'PORT': '5002'}, TOUTES),
])
def test_l_hote_est_exactement_celui_d_avant(auth, env, attendu):
    """Le lot corrige ce qui est DIT, pas ce qui est fait. Restreindre `PORT`
    à 127.0.0.1 casserait un déploiement Render, qui impose ce port et exige
    l'écoute sur toutes les interfaces."""
    assert exposition(auth, env)['hote'] == attendu


def test_VERTEX_LAN_autre_que_1_n_ouvre_rien():
    """Contre-épreuve : la règle teste l'égalité à `'1'`, pas la présence."""
    assert exposition(False, {'VERTEX_LAN': '0'})['hote'] == LOCAL
    assert exposition(False, {'VERTEX_LAN': 'oui'})['hote'] == LOCAL


#  ═══════════  2. le motif nomme la VRAIE cause  ══════════════════════════════

def test_le_motif_PORT_n_est_pas_confondu_avec_VERTEX_LAN():
    """LE défaut du message de démarrage : il annonçait `VERTEX_LAN=1` pour une
    ouverture causée par `PORT`."""
    assert exposition(False, {'PORT': '5002'})['motif'] == MOTIF_PORT
    assert exposition(False, {'VERTEX_LAN': '1'})['motif'] == MOTIF_LAN


def test_le_VERROU_prime_sur_l_hebergeur():
    """Sans cet ordre, un desk PROTÉGÉ tournant sur Render se décrirait
    « ouvert par l'hébergeur », alors que le code le protège de toute façon."""
    assert exposition(True, {'PORT': '5002'})['motif'] == MOTIF_VERROU


def test_sans_rien_le_motif_est_LOCAL():
    assert exposition(False, {})['motif'] == MOTIF_LOCAL


def test_protege_et_ouvert_sont_deux_choses_SEPAREES():
    """Les confondre est exactement ce qui a produit les deux mensonges."""
    e = exposition(False, {'PORT': '5002'})
    assert e['ouvert_au_reseau'] is True
    assert e['protege'] is False
    assert e['expose_sans_code'] is True


def test_un_desk_protege_n_est_PAS_marque_expose_sans_code():
    """Contre-épreuve. Un avertissement présent partout ne distingue plus rien."""
    assert exposition(True, {'PORT': '5002'})['expose_sans_code'] is False
    assert exposition(True, {})['expose_sans_code'] is False


def test_un_desk_LOCAL_n_est_pas_marque_expose():
    assert exposition(False, {})['expose_sans_code'] is False


#  ═══════════  3. la phrase dit l'état réel  ══════════════════════════════════

def test_la_phrase_nomme_PORT_quand_c_est_PORT():
    p = phrase(exposition(False, {'PORT': '5002'}))
    assert 'PORT' in p
    assert 'VERTEX_LAN=1' not in p, "le message d'origine nommait une variable absente"
    assert 'SANS CODE' in p


def test_la_phrase_nomme_VERTEX_LAN_quand_c_est_VERTEX_LAN():
    p = phrase(exposition(False, {'VERTEX_LAN': '1'}))
    assert 'VERTEX_LAN=1' in p and 'SANS CODE' in p


def test_la_phrase_d_un_desk_protege_ne_crie_pas():
    p = phrase(exposition(True, {}))
    assert 'VERTEX_CODE' in p and 'SANS CODE' not in p


def test_la_phrase_locale_ne_promet_pas_une_ouverture():
    p = phrase(exposition(False, {}))
    assert '127.0.0.1' in p and '0.0.0.0' not in p


#  ═══════════  4. la carte de sécurité, là où le mensonge était  ══════════════

def test_la_carte_AVOUE_l_exposition_sans_code(monkeypatch):
    """Le défaut le plus grave : la carte affirmait « le serveur n'écoute que
    127.0.0.1 » alors qu'il écoutait sur toutes les interfaces."""
    monkeypatch.setenv('VERTEX_LAN', '1')
    carte = _lock_card(False)
    assert '0.0.0.0' in carte
    assert 'VERTEX_LAN' in carte
    assert 'expos' in carte, "le badge doit dire l'exposition"
    assert "n&#8217;est joignable que" not in carte, (
        "la carte ne doit plus promettre une restriction absente")


def test_la_carte_nomme_PORT_et_pas_VERTEX_LAN_quand_c_est_PORT(monkeypatch):
    monkeypatch.delenv('VERTEX_LAN', raising=False)
    monkeypatch.setenv('PORT', '5002')
    carte = _lock_card(False)
    assert 'PORT' in carte
    assert 'VERTEX_LAN' not in carte


def test_la_carte_LOCALE_dit_encore_la_restriction_REELLE(monkeypatch):
    """Contre-épreuve : quand la restriction existe VRAIMENT, la carte doit
    continuer de le dire — sinon on aurait remplacé un mensonge par un silence."""
    monkeypatch.delenv('VERTEX_LAN', raising=False)
    monkeypatch.delenv('PORT', raising=False)
    carte = _lock_card(False)
    assert '127.0.0.1' in carte
    assert 'expos' not in carte


def test_la_carte_d_un_desk_PROTEGE_est_inchangee(monkeypatch):
    """Le chemin nominal ne doit pas régresser : le bouton de verrouillage est
    le seul atteignable de l'UI."""
    monkeypatch.setenv('PORT', '5002')
    carte = _lock_card(True)
    assert 'vx-lock-btn' in carte and '/logout' in carte
    assert 'expos' not in carte


#  ═══════════  5. un seul propriétaire, et il le reste  ═══════════════════════

def test_terminal_ne_recalcule_PLUS_la_regle_lui_meme():
    """La cause du défaut n'était pas la règle : c'est qu'elle était décrite à
    deux endroits qui ne la lisaient pas. Si `terminal.py` la réécrit un jour,
    les deux descriptions divergeront de nouveau — en silence."""
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1]
           / 'terminal.py').read_text(encoding='utf-8')
    assert "lan_ok = AUTH_ON or" not in src, (
        "la regle est recalculee dans terminal.py au lieu d'etre lue")
    assert 'from vertex.app.exposition import' in src


def test_la_carte_ne_recalcule_PAS_la_regle_non_plus():
    import pathlib
    src = (pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'ui'
           / 'pages' / 'system_page.py').read_text(encoding='utf-8')
    i = src.index('def _lock_card')
    bloc = src[i:i + 3000]
    assert 'exposition' in bloc
    assert "VERTEX_LAN') == '1'" not in bloc, (
        "la carte redérive la regle : elle divergera au premier changement")
