"""AUCUNE EXCEPTION PYTHON NE SORT DANS UNE CHARGE SERVIE.

## Le défaut, mesuré

`/options/AAPL` rendait **HTTP 200** avec :

```json
"error": "IndexError: single positional indexer is out-of-bounds"
```

Un type et un message internes, en anglais, livrés au client. Deux fautes en
une : une divulgation de détail d'implémentation, et un « état » qui ne dit
rien de ce qui manque réellement.

`tests/test_instantane.py` l'avait relevé — « une exception Python brute servie
comme état » — et `ticker_api` portait un commentaire affirmant que l'aveu était
désormais structuré. Il l'était à moitié : la FORME du pack avait été corrigée,
le MESSAGE était resté brut. Trois routes faisaient la même chose :
`ticker_api`, `weekly_api`, `correlations_api`, toutes avec le motif
`except Exception as e` puis `'%s: %s' % (type(e).__name__, e)`.

## Ce que ce banc garde

Le vocabulaire d'erreur du dépôt est fait de **codes stables** —
`options_lab_unavailable`, `empreinte_absente`, `symbole_invalide`. Ce banc
interdit qu'un texte d'exception les remplace, à deux endroits :

1. **dans le code** — aucune source de `vertex/` ne compose une charge servie à
   partir de `type(e).__name__` ou de `str(exc)` sur une exception large ;
2. **dans les octets réellement servis** — les routes concernées sont
   exercées et leur charge est inspectée.

## Ce qu'il n'interdit PAS

`str(exc)` sur une exception **applicative volontaire** reste correct :
`PayloadError` porte des codes stables (`payload_json_objet_requis`,
`symbole_invalide`), qui SONT le message destiné à l'appelant. Trois routes en
usent légitimement et ne sont pas visées — les confondre avec une fuite aurait
supprimé une bonne pratique.
"""
from __future__ import annotations

import ast
import json
import os
import re

import pytest

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: Signatures d'exception Python qui n'ont rien à faire dans une charge servie.
_SIGNATURES = (
    'IndexError', 'KeyError', 'TypeError', 'ValueError', 'AttributeError',
    'ZeroDivisionError', 'IndexingError', 'Traceback (most recent call last)',
    'object has no attribute', 'not subscriptable', 'out-of-bounds',
)

#: Routes qui rendaient une exception brute, plus leur voisine restée saine.
_ROUTES = (
    '/options/AAPL',
    '/api/correlations/AAPL',
    '/api/ticker/AAPL',
    '/api/company/AAPL',
    '/healthz',
)


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


#: Modules qui COMPOSENT une réponse HTTP. Le balayage statique se limite à
#: eux, et c'est la leçon la plus chère de ce lot : appliqué à tout `vertex/`,
#: il criait sur des champs `erreur` INTERNES dont le contrat est justement de
#: NOMMER LA CAUSE — `test_echeances_doctrine`, `test_fondamentaux_dates` et
#: `test_legacy_basket_risk` l'exigent noir sur blanc (« un profil illisible est
#: nommé et non avalé », « une collecte en échec porte son motif »).
#: Les avoir « corrigés » aurait troqué une fuite contre une perte de
#: diagnostic. Un échec interne doit dire pourquoi ; une charge SERVIE ne doit
#: pas dire avec quelle exception Python. Ce sont deux contrats distincts.
def _sources():
    routes = os.path.join(_RACINE, 'vertex', 'app', 'routes')
    for racine, dirs, noms in os.walk(routes):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for nom in noms:
            if nom.endswith('.py'):
                yield os.path.join(racine, nom)


# ── 1. Anti-vide : le détecteur mord-il ? ───────────────────────────────────

def test_le_detecteur_reconnait_une_charge_fautive():
    """Un banc qui ne trouve rien sur une charge FABRIQUÉE fautive ne prouve
    rien sur les charges réelles."""
    fautif = json.dumps({'sym': 'X', 'error': 'IndexError: single positional '
                                              'indexer is out-of-bounds'})
    trouve = [s for s in _SIGNATURES if s in fautif]
    assert trouve, 'le détecteur ne voit pas une exception servie évidente'

    sain = json.dumps({'sym': 'X', 'error': 'options_pack_unavailable',
                       'note': 'chaîne d’options indisponible pour ce titre'})
    assert [s for s in _SIGNATURES if s in sain] == [], (
        'le détecteur crie sur une charge saine — il serait inutilisable')


# ── 2. Dans le CODE : aucune charge composée depuis une exception large ─────

def test_le_TYPE_de_l_exception_n_entre_pas_dans_un_champ_d_erreur_SERVI():
    """`type(e).__name__` livre le détail interne — mais SEULEMENT s'il finit
    dans une charge.

    Ce banc a d'abord visé toute occurrence dans `vertex/`. Il criait alors sur
    `snapshot.py` et `persist.py`, qui gardent le type pour leurs MÉTRIQUES
    internes : jamais servi, et précieux pour diagnostiquer. Interdire ça aurait
    supprimé une bonne pratique au nom d'une règle trop large — le défaut même
    que ce dépôt reproche aux outils d'analyse.

    Le critère retenu est donc : le type entre-t-il dans la VALEUR d'un champ
    `error` / `erreur` d'un dictionnaire ? C'est là, et là seulement, qu'il
    part vers le client.
    """
    motif = re.compile(
        r"""['"]err(?:or|eur)['"]\s*:\s*[^,}\n]*type\(\s*\w+\s*\)\.__name__"""
        r"""|\[\s*['"]err(?:or|eur)['"]\s*\]\s*=\s*[^\n]*type\(\s*\w+\s*\)\.__name__""")
    fautes = []
    for chemin in sorted(_sources()):
        with open(chemin, encoding='utf-8', errors='ignore') as f:
            for num, ligne in enumerate(f, 1):
                if motif.search(ligne):
                    fautes.append('%s:%d' % (os.path.relpath(chemin, _RACINE), num))
    assert fautes == [], (
        'le type de l’exception entre dans un champ d’erreur servi — employer '
        'un code stable (`options_pack_unavailable`, `empreinte_absente`) : %s'
        % '; '.join(fautes))


def test_le_critere_distingue_bien_le_SERVI_de_l_INTERNE():
    """Contre-épreuve du critère ci-dessus : il doit mordre sur la forme
    fautive et se taire sur la forme interne, sinon il ne discrimine rien."""
    motif = re.compile(
        r"""['"]err(?:or|eur)['"]\s*:\s*[^,}\n]*type\(\s*\w+\s*\)\.__name__"""
        r"""|\[\s*['"]err(?:or|eur)['"]\s*\]\s*=\s*[^\n]*type\(\s*\w+\s*\)\.__name__""")
    fautif = ["out['error'] = f'{type(e).__name__}: {e}'",
              "return jsonify({'error': '%s: %s' % (type(e).__name__, e)})"]
    interne = ["_STATS['last_error'] = type(exc).__name__",
               "e.erreur = ('%s: %s' % (type(exc).__name__, exc))[:200]"]
    for ligne in fautif:
        assert motif.search(ligne), 'critère aveugle sur : %s' % ligne
    for ligne in interne:
        assert not motif.search(ligne), 'critère trop large sur : %s' % ligne


def test_str_d_exception_LARGE_ne_devient_pas_une_charge():
    """`str(exc)` reste licite sur une exception APPLICATIVE (`PayloadError`,
    dont le message EST un code stable). Il ne l'est pas sur `except Exception`,
    où le texte vient de la bibliothèque et non du produit."""
    fautes = []
    for chemin in sorted(_sources()):
        with open(chemin, encoding='utf-8', errors='ignore') as f:
            src = f.read()
        try:
            arbre = ast.parse(src)
        except SyntaxError:
            continue
        for n in ast.walk(arbre):
            if not isinstance(n, ast.ExceptHandler) or n.name is None:
                continue
            large = (n.type is None
                     or (isinstance(n.type, ast.Name) and n.type.id == 'Exception'))
            if not large:
                continue
            seg = ast.get_source_segment(src, n) or ''
            motif = r'str\(\s*%s\s*\)' % re.escape(n.name)
            if re.search(motif, seg) and ('jsonify' in seg or "'error'" in seg
                                          or '"error"' in seg):
                fautes.append('%s:%d' % (os.path.relpath(chemin, _RACINE), n.lineno))
    assert fautes == [], (
        'texte d’une exception LARGE servi au client : %s' % '; '.join(fautes))


# ── 3. Sur les OCTETS SERVIS ────────────────────────────────────────────────

@pytest.mark.parametrize('route', _ROUTES)
def test_la_charge_servie_ne_porte_aucune_signature_d_exception(client, route):
    reponse = client.get(route)
    assert reponse.status_code < 500, '%s : %d' % (route, reponse.status_code)
    corps = reponse.get_data(as_text=True)
    trouvees = sorted({s for s in _SIGNATURES if s in corps})
    assert trouvees == [], (
        '%s sert une signature d’exception %s — extrait : %s'
        % (route, trouvees, corps[:300]))


def test_les_routes_exercees_rendent_bien_quelque_chose(client):
    """Dénominateur : si ces routes rendaient du vide, l'absence de signature
    ci-dessus serait vraie pour rien."""
    for route in _ROUTES:
        corps = client.get(route).get_data(as_text=True)
        assert len(corps) > 20, '%s rend %d octets' % (route, len(corps))


# ── 4. Le bon motif reste employé ───────────────────────────────────────────

def test_le_vocabulaire_de_codes_stables_est_bien_VIVANT():
    """Si plus aucune route ne servait de code stable, c'est que la convention
    aurait été abandonnée — et ce banc garderait une règle morte."""
    codes = set()
    for chemin in sorted(_sources()):
        with open(chemin, encoding='utf-8', errors='ignore') as f:
            src = f.read()
        codes |= set(re.findall(r"['\"]error['\"]\s*:\s*'([a-z_]{6,})'", src))
        codes |= set(re.findall(r"['\"]reason['\"]\s*:\s*'([a-z_]{6,})'", src))
    assert len(codes) >= 10, (
        'seulement %d codes d’erreur stables trouvés : la convention semble '
        'abandonnée (%s)' % (len(codes), sorted(codes)))
    for attendu in ('options_pack_unavailable', 'correlations_unavailable',
                    'weekly_rebuild_unavailable'):
        assert attendu in codes, 'code de remplacement absent : %s' % attendu
