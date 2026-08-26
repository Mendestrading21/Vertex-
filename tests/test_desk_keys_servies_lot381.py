"""
LOT 381 — LES GARDIENS DES CLÉS DE SYNC GARDAIENT LES MAUVAISES LISTES.

Ouverture de la veine décidée au bilan 380 : auditer les **gardiens eux-mêmes**,
par mutation. Cibles choisies : ceux que `CLAUDE.md` nomme comme protégeant les
règles critiques — une défaillance y coûte le plus cher.

## Mutation testing sur 7 invariants historiques

```
clé renommée dans DESK_KEYS de vx_kit (source de vérité)   MORD
version du service worker rétrogradée                      MORD
vocabulaire des verdicts vidé (window.__VXVOCAB)           MORD
READONLY basculé à False                                   MORD
clé vxAlerts retirée du repli deskKeys() de system_page    AUCUN GARDIEN ⚠
```

Les invariants lourds sont réellement tenus. **Un trou, et il est sur la règle
critique n°1** — celle dont `CLAUDE.md` dit : « sinon un push l'efface côté
serveur ». Retirer `vxAlerts` du repli servi passe **les 2 754 tests**.

## Ce que l'audit a révélé de plus grave : les gardiens visent à côté

En vérifiant *pourquoi* rien ne mordait, j'ai mesuré quelles listes sont
réellement servies :

| liste | servie ? | gardée ? |
|-------|----------|----------|
| `vertex/static/vertex/js/vx-entities.js` (32 464 o, HTTP 200) | **oui** | oui |
| `system_page.py::deskKeys()` (inline dans `/system`) | **oui** | **NON** |
| `vx_kit.py` DESK_KEYS — dite « source de vérité » | **non — 0/8 pages** | oui |
| `journal.py` | non (page morte) | oui |

`vx_kit.JS` fait 21 727 octets et **n'apparaît sur aucune des huit pages** —
mesuré page par page. Or `CLAUDE.md` le décrit comme « kit global **présent sur
toutes les pages** », et les deux gardiens nommés s'y ancrent comme référence.

La chaîne fonctionne encore, parce que `vx-entities.js` est comparé à `vx_kit`.
Mais elle est **ancrée sur un module qui n'atteint plus le navigateur** : le jour
où `vx_kit` est purgé — et c'est un candidat de purge — la référence disparaît,
tandis que la seule liste servie non gardée continue de vivre.

Ce test comble le trou : il garde les listes **par ce qu'elles servent**, pas par
ce que la documentation croit.

## Trois fausses pistes en chemin — l'outil, encore

1. `.replace(…, 1)` a frappé `jget('vxAlerts',…)` ligne 105 au lieu de
   `DESK_KEYS` ligne 259 : « la source de vérité n'est pas gardée » était faux.
2. Même erreur sur l'apostrophe échappée.
3. La mutation d'apostrophe visait un bloc de `vx_kit.JS` qui **n'est servi nulle
   part** — le balayage JS avait raison de ne pas mordre.

Trois fois où j'aurais accusé un gardien sain. Le lot 379 l'avait formulé : *un
cas qui ne mord pas accuse d'abord la mutation*.
"""
#  MARCHES EST FUSIONNE DANS LE DASHBOARD (Black Glass).
#
#  `/markets` ne sert plus de page : la route redirige 302 vers `/#…`
#  pour preserver les favoris. Les listes d'espaces ci-dessous ne le
#  citent donc plus, et les appels directs visent `/`, qui porte
#  desormais ce contenu. La couverture n'est pas perdue : elle a
#  simplement suivi le contenu.
import re

import pytest

import terminal

PAGES = ['/', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']

# Contrat DESK_KEYS — la liste que TOUTE copie servie doit porter à l'identique.
ATTENDUES = {
    'myTrades', 'myTradesClosed', 'myTradesEquity', 'myRecos', 'myRecosClosed',
    'myCapital', 'simCash', 'simStart', 'simTrades', 'simClosed', 'myFavs',
    'myNotes', 'vxJournal', 'myTradeLog', 'vxVault', 'vxAlerts', 'vxWatchlist',
}


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


def _cles(bloc):
    return set(re.findall(r"'([A-Za-z][A-Za-z0-9_]*)'", bloc))


# ── 1. La liste servie qui n'était gardée par RIEN ──────────────────────────

def test_le_repli_deskKeys_de_system_porte_le_contrat_complet(client):
    """`/system` embarque un repli inline utilisé quand `VXEntities` n'est pas
    chargé. Il est SERVI, et aucun test ne le vérifiait : retirer une clé y
    passait les 2 754 tests. Une clé manquante = un push qui efface cette
    donnée côté serveur (règle critique n°1)."""
    html = client.get('/system').get_data(as_text=True)
    m = re.search(r'function deskKeys\(\)\{.*?\[(.*?)\]', html, re.S)
    assert m, 'le repli deskKeys() n\'est plus servi sur /system — gardien à revoir'
    manquantes = ATTENDUES - _cles(m.group(1))
    assert not manquantes, (
        'clés absentes du repli servi de /system : %s — un push les effacerait '
        'côté serveur' % ', '.join(sorted(manquantes)))


def test_le_repli_deskKeys_n_invente_aucune_cle(client):
    """Gardien pas trop strict, mais symétrique : une clé EN TROP côté repli
    créerait une donnée fantôme dans le blob synchronisé."""
    html = client.get('/system').get_data(as_text=True)
    m = re.search(r'function deskKeys\(\)\{.*?\[(.*?)\]', html, re.S)
    assert m
    superflues = _cles(m.group(1)) - ATTENDUES
    assert not superflues, 'clés inconnues dans le repli servi : %s' % sorted(superflues)


# ── 2. L'autre liste servie : le fichier statique ───────────────────────────

def test_vx_entities_est_bien_servi_et_porte_le_contrat(client):
    """La seule autre copie servie. Elle est déjà gardée par
    `test_strategy_os_final_guards`, mais celui-ci la lit sur DISQUE ; ici on la
    vérifie telle qu'elle est **servie**."""
    r = client.get('/static/vertex/js/vx-entities.js')
    assert r.status_code == 200, 'vx-entities.js non servi (%s)' % r.status_code
    js = r.get_data(as_text=True)
    m = re.search(r'DESK_KEYS\s*=\s*\[(.*?)\]', js, re.S)
    assert m, 'DESK_KEYS absent de vx-entities.js servi'
    assert _cles(m.group(1)) == ATTENDUES, (
        'vx-entities.js servi désynchronisé : %s'
        % sorted(_cles(m.group(1)) ^ ATTENDUES))


@pytest.mark.parametrize('page', PAGES)
def test_chaque_page_charge_le_fichier_de_cles_servi(client, page):
    """Si une page cesse de charger `vx-entities.js`, elle retombe sur le repli
    inline — d'où l'importance que les deux portent la même liste."""
    html = client.get(page).get_data(as_text=True)
    assert 'vx-entities.js' in html, '%s ne charge plus vx-entities.js' % page


# ── 3. Le constat qui a motivé ce lot, ancré ────────────────────────────────

def test_vx_kit_reste_hors_des_pages_servies(client):
    """`vx_kit.JS` (21 727 o) est la « source de vérité » selon la doc et les
    deux gardiens nommés — mais il n'atteint AUCUNE des 8 pages. Mesuré ici.

    Ce test ne juge pas : il **ancre le fait**. S'il échoue un jour, c'est que
    `vx_kit` est redevenu servi — et alors sa liste rejoint le périmètre à
    garder par ce qu'elle sert, comme les deux autres."""
    from vertex.ui import vx_kit
    assert len(vx_kit.JS) > 1000, 'vx_kit.JS vidé — gardien à revoir'
    servies = [p for p in PAGES
               if 'var DESK_KEYS=' in client.get(p).get_data(as_text=True)]
    assert not servies, (
        'vx_kit est redevenu servi sur %s — étendre le périmètre de ce gardien'
        % ', '.join(servies))


def test_les_deux_listes_servies_sont_identiques(client):
    """LA propriété qui protège les données : les deux copies **servies** ne
    doivent jamais diverger, quelle que soit celle que le navigateur utilise."""
    stat = re.search(r'DESK_KEYS\s*=\s*\[(.*?)\]',
                     client.get('/static/vertex/js/vx-entities.js').get_data(as_text=True),
                     re.S)
    repli = re.search(r'function deskKeys\(\)\{.*?\[(.*?)\]',
                      client.get('/system').get_data(as_text=True), re.S)
    assert stat and repli, 'une des deux listes servies est introuvable'
    assert _cles(stat.group(1)) == _cles(repli.group(1)), (
        'les deux listes SERVIES divergent : %s'
        % sorted(_cles(stat.group(1)) ^ _cles(repli.group(1))))
