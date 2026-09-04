"""
LOT 362, PUIS #783/G2 — LE SERVEUR A ÉTÉ DURCI, ET CE FICHIER LE DIT.

Le lot 362 avait mesuré, sans corriger, trois faits qui bornaient ce que la
règle n°6 de `CLAUDE.md` (« en cas de doute, les backups ») promettait
réellement. Son en-tête se terminait par une consigne explicite :

> ⚠️ Ce sont des tests de CARACTÉRISATION : ils décrivent le contrat actuel, ils
> ne le bénissent pas. Si le serveur est un jour durci (refus d'un push qui vide
> un desk non vide, ou snapshot supplémentaire avant perte), ces tests DOIVENT
> être mis à jour — c'est précisément leur rôle d'alerte.

C'est ce jour. Les trois faits sont repris un par un, avec ce qu'ils sont
devenus.

## 1. Un push vide effaçait le desk → il ne l'efface plus

Le serveur **fusionne** au lieu de remplacer : une clé qu'il détient avec du
contenu et que le push n'envoie pas est **conservée**. Le push reste accepté
(200) — le refuser casserait la sync d'un navigateur en difficulté, ce qui est
précisément le moment où l'on veut qu'elle continue de fonctionner.

**Pourquoi conserver, et non supprimer.** Une clé absente ne veut jamais dire
« supprimée » : aucun chemin du produit n'appelle `removeItem` sur une clé de
desk (vérifié sur tout le dépôt), et vider une liste écrit `'[]'`, qui est bien
envoyé. Une absence est donc toujours un défaut de lecture côté navigateur —
jamais une intention.

## 2. Le last-writer-wins était TOTAL → il l'est resté pour ce qui est envoyé

Une clé envoyée écrase, sans discussion : c'est le protocole, et il est correct.
Ce qui change, c'est le sort des clés **absentes**.

## 3. Le point de restauration ne bougeait pas → un instantané à la seconde

Le filet quotidien prend son image avant la première écriture du jour : il
rendait l'état d'hier. Un instantané `desk_avantperte_<date>-<heure>.json` est
désormais pris **au moment précis** où des clés sont menacées, et il est listé
par `/api/desk/backups` comme restaurable par `/api/desk/restore` — un
instantané qu'aucune sortie ne nomme n'est pas un filet, c'est un fichier.

Tout passe par un dossier temporaire : le vrai `desk_data.json` n'est jamais
touché.
"""
import glob
import json
import os
import time

import pytest

import terminal
from vertex.services import persist


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(persist, 'cache_path', lambda name: str(tmp_path / name))
    yield terminal.app.test_client()


PLEIN = {'myTrades': '[{"symbol":"ACN"}]',
         'vxJournal': '[{"note":"these"}]',
         'myFavs': '["ACN","ABT"]'}


def _push(client, ts, data):
    return client.post('/api/desk', json={'ts': ts, 'data': data})


def _desk(client):
    return client.get('/api/desk').get_json()


def _snapshots(tmp_path, motif='desk_backup_*.json'):
    return sorted(os.path.basename(p) for p in glob.glob(str(tmp_path / motif)))


# ── 1. Un push vide n'efface plus rien ───────────────────────────────────────

def test_un_push_vide_ne_vide_plus_le_desk_serveur(client):
    """LE DÉFAUT CENTRAL DU LOT 362, FERMÉ.

    C'est le scénario résiduel qu'il avait nommé : un navigateur dont l'écriture
    localStorage échoue en silence hydrate sans rien persister, puis pousse
    `{}`. Avant, le desk du serveur — trades, journal, favoris — disparaissait."""
    _push(client, 1000, PLEIN)
    r = _push(client, 2000, {})
    assert r.status_code == 200, 'la sync doit continuer de fonctionner'
    assert _desk(client)['data'] == PLEIN, (
        'un push vide efface de nouveau le desk du serveur')
    assert r.get_json()['conservees'] == sorted(PLEIN), (
        'la conservation n\'est plus ANNONCEE : un client qui perd son '
        'localStorage ne peut plus s\'en apercevoir')


def test_le_type_du_payload_reste_valide(client):
    """La validation de forme n'a pas bougé : elle porte toujours sur le type."""
    assert _push(client, 1000, None).status_code == 400
    assert _push(client, 1000, []).status_code == 400
    assert client.post('/api/desk', json={'data': {}}).status_code == 400   # ts absent
    assert _push(client, 1000, {}).status_code == 200


def test_une_valeur_vide_n_est_pas_du_travail_a_proteger(client):
    """Le contre-exemple qui empêche la garde de tout figer.

    Une liste vide qui disparaît ne fait rien perdre. Si le serveur protégeait
    aussi ces clés-là, il empilerait indéfiniment des `'[]'` que plus personne
    n'envoie — et « conservees » cesserait de signaler quoi que ce soit."""
    _push(client, 1000, {'myTrades': '[]', 'vxJournal': '{}', 'myFavs': 'null',
                         'myRecos': '[{"s":"ACN"}]'})
    r = _push(client, 2000, {})
    assert r.get_json()['conservees'] == ['myRecos'], (
        'les valeurs vides sont protegees comme du travail : %s'
        % r.get_json()['conservees'])
    assert sorted(_desk(client)['data']) == ['myRecos']


def test_une_cle_envoyee_ecrase_toujours(client):
    """Le last-writer-wins reste ENTIER sur ce qui est envoyé — y compris pour
    vider volontairement une liste. Sinon l'utilisateur ne pourrait plus rien
    supprimer, ce qui serait une régression d'un autre genre."""
    _push(client, 1000, PLEIN)
    _push(client, 2000, dict(PLEIN, myTrades='[]'))
    assert _desk(client)['data']['myTrades'] == '[]', (
        'une suppression volontaire ne passe plus : le desk devient '
        'inmodifiable a la baisse')


# ── 2. Un push partiel ne perd plus les clés absentes ────────────────────────

def test_supprimer_une_cle_se_dit_desormais_EXPLICITEMENT(client):
    """LA CONTREPARTIE DU DURCISSEMENT, ET ELLE A MORDU POUR DE VRAI.

    Si l'omission ne supprime plus, un appelant qui veut supprimer doit envoyer
    la clé **vide**. Ce n'est pas une subtilité théorique : la première
    exécution de la suite sous le nouveau contrat a laissé le marqueur de
    `tests/test_desk_cycle.py` dans le desk RÉEL, parce que son `finally`
    remettait l'état d'origine en *omettant* la clé qu'il venait de créer.

    Le contrat est donc écrit ici, et vérifié : omettre conserve, envoyer vide
    supprime."""
    _push(client, 1000, PLEIN)
    _push(client, 2000, dict(PLEIN, vxJournal='[]'))
    assert _desk(client)['data']['vxJournal'] == '[]'
    #  … et la clé vidée ne se fait plus protéger au push suivant.
    r = _push(client, 3000, {'myFavs': '["ACN"]'})
    assert 'vxJournal' not in r.get_json()['conservees'], (
        'une cle VIDEE est de nouveau traitee comme du travail a proteger : '
        'plus rien ne pourrait jamais quitter le desk')


def test_un_push_partiel_conserve_les_cles_absentes(client):
    _push(client, 1000, PLEIN)
    r = _push(client, 2000, {'myFavs': '["ACN"]'})
    d = _desk(client)['data']
    assert sorted(d) == ['myFavs', 'myTrades', 'vxJournal']
    assert d['myFavs'] == '["ACN"]'                     # la clé envoyée gagne
    assert d['myTrades'] == PLEIN['myTrades']           # les absentes survivent
    assert r.get_json()['conservees'] == ['myTrades', 'vxJournal']


# ── 3. Le point de restauration suit désormais la perte ──────────────────────

def test_un_instantane_est_pris_a_la_seconde_ou_la_perte_menace(client, tmp_path):
    """Le trou exact que le lot 362 avait mesuré : le filet quotidien remontait
    à avant la première sync du jour, donc restaurer perdait la journée."""
    _push(client, 1000, PLEIN)
    _push(client, 2000, dict(PLEIN,
                             vxJournal='[{"note":"these"},{"note":"ajout du jour"}]'))
    assert _snapshots(tmp_path, 'desk_avantperte_*.json') == [], (
        'un instantane avant-perte a ete pris alors que RIEN ne menacait : '
        'le declencheur est trop large')

    r = _push(client, 3000, {})                          # l'ancienne perte
    avant_perte = _snapshots(tmp_path, 'desk_avantperte_*.json')
    assert len(avant_perte) == 1, 'aucun instantane pris au moment de la perte'
    assert r.get_json()['instantane'] == avant_perte[0]

    #  Et il contient le travail DE LA JOURNÉE, pas l'état d'hier.
    snap = json.loads((tmp_path / avant_perte[0]).read_text(encoding='utf-8'))
    assert 'ajout du jour' in snap['data']['vxJournal'], (
        'l\'instantane ne contient pas le travail de la journee : il ne comble '
        'pas le trou du filet quotidien')


def test_l_instantane_avant_perte_est_listable_et_restaurable(client, tmp_path):
    """« Une portée n'est pas une sortie » : un instantané que `/api/desk/backups`
    ne nomme pas et que `/api/desk/restore` refuse n'est pas un filet."""
    _push(client, 1000, PLEIN)
    r = _push(client, 2000, {})
    nom = r.get_json()['instantane']

    listes = client.get('/api/desk/backups').get_json()['backups']
    par_nom = {b['name']: b for b in listes}
    assert nom in par_nom, 'l\'instantane avant-perte n\'est pas liste'
    assert par_nom[nom]['type'] == 'avant-perte'
    assert par_nom[nom]['date'] == time.strftime('%Y%m%d')

    _push(client, 3000, {'myFavs': '[]'})
    assert client.post('/api/desk/restore', json={'name': nom}).status_code == 200
    assert _desk(client)['data']['myTrades'] == PLEIN['myTrades']


def test_le_restore_refuse_toujours_un_nom_hors_grammaire(client):
    """La validation stricte du nom protège d'une traversée de chemin. Élargir
    la grammaire à une seconde famille ne devait pas l'affaiblir."""
    for mauvais in ('../desk_data.json', 'desk_avantperte_.json',
                    'desk_avantperte_20260101.json',     # heure manquante
                    'desk_avantperte_20260101-12345.json',
                    'desk_backup_2026010.json', 'desk_data.json', ''):
        assert client.post('/api/desk/restore',
                           json={'name': mauvais}).status_code == 400, (
            'nom accepte a tort : %r' % mauvais)


def test_les_deux_filets_ont_leur_propre_rotation(client, tmp_path):
    from vertex.app.routes import desk as _desk_mod
    assert _desk_mod.BACKUP_KEEP == 7
    assert _desk_mod.AVANT_PERTE_KEEP == 20

    for j in range(1, 10):
        (tmp_path / ('desk_backup_2026010%d.json' % j)).write_text(
            json.dumps({'ts': j, 'data': PLEIN}))
    for i in range(25):
        (tmp_path / ('desk_avantperte_20260101-0000%02d.json' % i)).write_text(
            json.dumps({'ts': i, 'data': PLEIN}))
    _push(client, 1000, PLEIN)
    _push(client, 2000, {})                              # déclenche les deux rotations
    assert len(_snapshots(tmp_path)) == 7
    assert len(_snapshots(tmp_path, 'desk_avantperte_*.json')) == 20, (
        'la rotation avant-perte ne borne plus : %d fichiers'
        % len(_snapshots(tmp_path, 'desk_avantperte_*.json')))


def test_les_instantanes_avant_perte_sont_gitignores():
    """Ce sont des données personnelles : trades, journal, positions."""
    import pathlib
    ig = pathlib.Path(__file__).resolve().parents[1].joinpath(
        '.gitignore').read_text(encoding='utf-8')
    assert 'desk_avantperte_*.json' in ig, (
        'les instantanes avant-perte ne sont plus ignores par git : des '
        'donnees personnelles peuvent etre commitees')
