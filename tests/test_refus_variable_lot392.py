"""
LOT 392 — LES REFUS CONSTRUITS EN VARIABLE : l'angle mort du lot 377, mesuré.

Le lot 377 avait prouvé « **39 refus, 39 motivés, 0 muet** » — mais son
détecteur déballe `jsonify(...)` puis exige un dict **littéral**. Une réponse
assemblée dans une variable (`out = {}` … `out['ok'] = False` …
`return jsonify(out), 400`) lui est invisible. Il le déclarait ; ce lot le
mesure.

## Le dénominateur, resserré par la mesure

```text
retours déballés donnant un dict LITTÉRAL (périmètre du 377)   417
retours déballés donnant une VARIABLE  (angle mort)            393
   dont dans une fonction de ROUTE                              34
   dont enveloppés (jsonify/tuple) → réellement SERVIS           31
   soit                                                          30 routes distinctes
```

Le volume brut de l'angle mort (393) est du même ordre que le périmètre couvert
(417) — mais **359 de ces retours sont des aides internes**, pas des réponses
d'API. La surface qui compte est de **30 routes**.

## Le verdict : rien de malhonnête, prouvé à l'exécution

Les 30 routes ont été sollicitées avec des entrées que le serveur doit refuser
(symbole inexistant, corps vide, identifiant inconnu). On ne raisonne pas sur le
code : on lit **la réponse réellement servie**.

```text
12 refus identifiés · 12 motivés · 0 MUET
```

Les motifs prennent plusieurs formes, toutes honnêtes : `reason`, `error`,
`available: false`, `empty` + `generator`, ou l'`audit_trail` qui énumère ce qui
manquait — la forme déjà relevée au lot 377.

Trois réponses ne portent aucune clé de motif mais **ne sont pas des refus**, et
n'inventent rien :

```text
/desc/ZZZZINEXISTANT     {"summary":"", "industry":"", "employees":null, …}
/api/positions/state     zéros + delta_global:null + note « jamais estimés en agrégat »
/api/desk                {}
```

Une absence rendue comme une absence : c'est exactement l'invariant n°4.

## Une fausse alerte de ma sonde

Mon premier détecteur signalait `run_startup_sequence` comme un refus MUET. Il ne
l'est pas : c'est un rapport de démarrage dont **le motif vit entièrement dans
`steps`**, chaque étape portant son statut et son message
(`'DEGRADED', 'SSE indisponible — polling seul'`). Ma liste de clés de motif ne
contenait simplement pas `steps`. **Neuvième fois de la tranche que l'instrument
est en cause avant le code.**

## Ce que ce gardien ajoute

Le 377 ne peut pas couvrir ces routes — son détecteur est statique et exige un
littéral. Ici la propriété est vérifiée **à l'exécution, sur la réponse servie**.
Le stockage est redirigé vers un dossier temporaire : ces routes journalisent
(leçon des lots 387-389).
"""
import ast
import json
import os
import tempfile

import pytest

# Routes prouvées refuser au lot 392, avec l'entrée qui déclenche le refus.
REFUS = [
    ('/api/anomalies/ZZZZINEXISTANT', 'GET'),
    ('/api/evidence/ZZZZINEXISTANT', 'GET'),
    ('/api/options/strategies/ZZZZINEXISTANT', 'GET'),
    ('/api/strategy/decision/ZZZZINEXISTANT', 'GET'),
    ('/api/options/scanner/ZZZZINEXISTANT', 'GET'),
    ('/api/skyler/memory/cell/ZZZZ/INEXISTANT', 'GET'),
    ('/api/tracking/ZZZZINEXISTANT', 'GET'),
    ('/api/portfolio/context', 'GET'),
    ('/api/planning/ticket', 'POST'),
    ('/api/tracking', 'POST'),
]

# Un motif peut prendre plusieurs formes honnêtes — on ne fige pas UNE clé,
# sinon renommer un champ ferait échouer du code sain (leçon du lot 383).
MOTIF = ('error', 'err', 'message', 'msg', 'reason', 'detail', 'why', 'note',
         'status', 'state', 'audit_trail', 'missing', 'steps', 'sources',
         'available', 'empty', 'insufficient', 'data_quality', 'coverage',
         'generator', 'why_not', 'explain')

# Mesuré au lot 392 : 30 routes servent une réponse construite en variable.
MIN_ROUTES_VARIABLE = 25


@pytest.fixture(scope='module')
def client():
    import terminal
    from vertex.services import persist
    # Ces routes journalisent (journal, mémoire, séances) : jamais dans le
    # stockage réel depuis un test.
    persist._BASE_DIR = tempfile.mkdtemp(prefix='lot392-')
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


def _deballe(v):
    if isinstance(v, ast.Tuple) and v.elts:
        return _deballe(v.elts[0])
    if isinstance(v, ast.Call) and v.args:
        f = v.func
        if (isinstance(f, ast.Name) and f.id in ('jsonify', 'dict')) or \
           (isinstance(f, ast.Attribute) and f.attr == 'jsonify'):
            return _deballe(v.args[0])
    return v


def _routes_a_reponse_variable():
    fichiers = ['terminal.py']
    for rac, _d, noms in os.walk('vertex'):
        if '__pycache__' in rac:
            continue
        fichiers += [os.path.join(rac, n) for n in sorted(noms) if n.endswith('.py')]
    vues = set()
    for chemin in fichiers:
        try:
            arbre = ast.parse(open(chemin, encoding='utf-8').read())
        except SyntaxError:
            continue
        for fn in ast.walk(arbre):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            urls = [a.value for d in fn.decorator_list for a in getattr(d, 'args', [])
                    if isinstance(a, ast.Constant) and isinstance(a.value, str)
                    and a.value.startswith('/')]
            if not urls:
                continue
            if any(isinstance(n, ast.Return) and n.value is not None
                   and isinstance(_deballe(n.value), ast.Name)
                   and isinstance(n.value, (ast.Call, ast.Tuple))
                   for n in ast.walk(fn)):
                vues.update((u, fn.name) for u in urls)
    return vues


# ── 1. Le dénominateur : sans lui, « 0 muet » ne prouverait rien ────────────

def test_l_angle_mort_du_lot_377_existe_toujours():
    """Ces routes construisent leur réponse dans une VARIABLE : le détecteur du
    lot 377, qui exige un dict littéral, ne les voit pas. Si ce compte
    s'effondrait, le présent gardien deviendrait sans objet — et passerait au
    vert pour la mauvaise raison (leçon des lots 375-377)."""
    n = len(_routes_a_reponse_variable())
    assert n >= MIN_ROUTES_VARIABLE, (
        'seulement %d routes servant une réponse construite en variable '
        '(30 mesurées au lot 392) — détecteur cassé ou refonte majeure : '
        'refaire la mesure avant de faire confiance aux tests suivants' % n)


def test_le_gardien_du_lot_377_reste_borne_aux_litteraux():
    """Explique pourquoi CE gardien existe. Si le 377 se mettait à déballer les
    variables, les deux se recouvriraient et il faudrait fusionner."""
    src = open('tests/test_refus_api_lot377.py', encoding='utf-8').read()
    assert 'return v if isinstance(v, ast.Dict) else None' in src, (
        'le détecteur du lot 377 ne se limite plus aux dicts littéraux : '
        'vérifier s\'il couvre désormais les réponses construites en variable, '
        'auquel cas ce gardien fait double emploi')


# ── 2. LA propriété, vérifiée sur la réponse SERVIE ────────────────────────

@pytest.mark.parametrize('url,methode', REFUS)
def test_un_refus_servi_dit_toujours_pourquoi(client, url, methode):
    """Un refus muet laisse l'utilisateur devant un écran vide sans savoir si la
    donnée manque, si la requête est invalide ou si le service est tombé.
    Vérifié sur la réponse réelle, pas sur le code."""
    r = client.open(url, method=methode, json={} if methode == 'POST' else None)
    corps = json.loads(r.get_data(as_text=True) or 'null')
    assert isinstance(corps, dict), '%s : réponse non-JSON (%d)' % (url, r.status_code)
    motifs = set(corps) & set(MOTIF)
    assert motifs, (
        '%s %s → HTTP %d : refus SERVI SANS MOTIF. Clés rendues : %s — '
        'l\'utilisateur ne peut pas distinguer « donnée absente » de '
        '« requête invalide » ni de « service en panne » (invariant n°4)'
        % (methode, url, r.status_code, sorted(corps)[:10]))


# ── 3. Une absence reste une absence — rien n'est inventé ──────────────────

def test_un_symbole_inconnu_ne_recoit_pas_une_description_inventee(client, tmp_path,
                                                                   monkeypatch):
    """`/desc/<sym>` ne porte aucune clé de motif : ce n'est pas un refus, mais
    il ne doit pas non plus fabriquer un contenu plausible.

    ⚠ Lot 399 — sur une machine EN LIGNE, cette route interroge yfinance puis
    **écrit `desc_cache.json` à la racine du dépôt**
    (`descriptions_api.CHEMIN`). Le
    défaut était invisible ici (le réseau échoue) et invisible au recensement du
    lot 389 (l'écriture est conditionnée à la RÉUSSITE du fetch). Le cache
    mémoire et le chemin disque sont donc isolés : la route reste la vraie,
    seule sa destination change.
    """
    #  #779/G1 — la route, son cache memoire et son chemin disque vivent dans
    #  `vertex/app/routes/descriptions_api.py`. Le test vise le module qui les
    #  tient ; l'isolation du disque reste ce qu'elle etait.
    from vertex.app.routes import descriptions_api as _desc
    monkeypatch.setattr(_desc, 'CHEMIN', str(tmp_path / 'desc_cache.json'))
    monkeypatch.setattr(_desc, '_cache', {})
    corps = json.loads(client.get('/desc/ZZZZINEXISTANT').get_data(as_text=True))
    for champ in ('summary', 'industry', 'country'):
        assert corps.get(champ) == '', (
            '/desc rend un %s NON VIDE pour un symbole inexistant : %r — '
            'un texte inventé servi comme réel' % (champ, corps.get(champ)))
    assert corps.get('employees') is None, \
        'un effectif est servi pour un symbole inexistant : %r' % corps.get('employees')


def test_les_greeks_agreges_restent_declares_non_estimes(client):
    """`/api/positions/state` rend des zéros sans clé de motif. Ce qui le rend
    honnête est ailleurs : `delta_global` à `null` et une note explicite."""
    corps = json.loads(client.get('/api/positions/state').get_data(as_text=True))
    pf = corps.get('portfolio') or {}
    assert 'greeks_note' in pf, (
        'la note sur les Greeks agrégés a disparu : des zéros seraient servis '
        'sans dire qu\'ils ne sont pas des estimations')
    assert 'jamais estim' in pf['greeks_note'], \
        'la note ne dit plus que les Greeks ne sont jamais estimés : %r' % pf['greeks_note']
