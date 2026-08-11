"""
LOT 372 — `json.dumps` NU DANS UN BLOC `<script>` : la faille de la tranche.

Les lots 367-371 ont couvert `?view=`, les segments de chemin, les 4 étiquettes
de `render_shell` et les deux routes `/memory/`. Restait la dernière grande
surface : les interpolations SERVEUR dans le `page_js` des pages.

**Ce qui a été trouvé.** `/opportunities` recevait `params=request.args` et n'en
filtrait que les **CLÉS** (`sym`, `sector`, `setup`, `decision`) — jamais les
**VALEURS**. Celles-ci partaient dans `json.dumps(p)`, injecté tel quel dans un
bloc `<script>` :

    const VIEW="radar";const PARAMS={"sym": "</script><img src=x onerror=alert(1)>"};

`json.dumps` échappe `"` et `\\` mais **ni `<` ni `/`** : l'analyseur HTML voit
la balise fermante, termine le script, et **tout ce qui suit devient du HTML
ACTIF**. Sondé et confirmé sur les 4 clés × 2 charges, HTTP 200, charge présente
dans les octets servis. Contrairement à la faille du lot 368 (qui exigeait que
le moteur de décision produise un symbole hostile), celle-ci est déclenchable à
distance **par un simple lien**.

**Correctif.** `vertex.ui.shell.json_for_script` neutralise `<`, `>` et `&` en
échappements `\\uXXXX`. Un moteur JS les relit à l'identique dans un littéral de
chaîne : comportement client inchangé (vérifié ci-dessous par aller-retour
`json.loads`), mais l'analyseur HTML ne peut plus voir de balise fermante.
Preuve MD5 : **0/8** page divergente — le trafic normal est octet pour octet
identique.

Note de méthode : le premier détecteur cherchait `<img …>` dans TOUTE la page et
répondait « actif » même quand la balise restait à l'intérieur d'un bloc
`<script>` non refermé — où elle est **inerte**. Les tests ci-dessous retirent
d'abord les blocs `<script>…</script>`, comme le fait l'analyseur, puis
cherchent la charge dans ce qui reste.
"""
import ast
import json
import re

import pytest

import terminal
from vertex.ui.shell import json_for_script

# Clés effectivement retenues par `/opportunities`.
CLES = ('sym', 'sector', 'setup', 'decision')

# Charges qui SORTENT du bloc <script> (les seules réellement dangereuses ici).
CHARGES_SORTIE = [
    ('sortie de balise', '</script><img src=x onerror=alert(1)>'),
    ('sortie casse mixte', '</ScRiPt><img src=x onerror=alert(1)>'),
    ('sortie espacée', '</script ><img src=x onerror=alert(1)>'),
]

_BLOC_SCRIPT = re.compile(r'<script\b[^>]*>.*?</script\s*>', re.S | re.I)


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


def html_actif(html: str) -> str:
    """Ce que l'analyseur HTML exécute : la page une fois les <script> consommés."""
    return _BLOC_SCRIPT.sub(' ', html)


# ── 1. Anti-vide : la sonde atteint bien un rendu complet ────────────────────

def test_la_sonde_atteint_une_page_reellement_rendue(client):
    """Sans ce test, des 404 ou une page d'erreur rendraient tous les « non »
    ci-dessous vides de sens (piège rencontré aux lots 368 et 371)."""
    r = client.get('/opportunities?view=radar&sym=AAPL')
    assert r.status_code == 200, 'la page doit être servie (%s)' % r.status_code
    html = r.get_data(as_text=True)
    assert len(html) > 20000, 'page trop courte (%d o) — rendu incomplet' % len(html)
    assert 'const PARAMS=' in html, 'const PARAMS n\'est plus servie — gardien à revoir'
    assert 'AAPL' in html, 'la valeur légitime n\'atteint pas le rendu'


# ── 2. Aucune charge ne sort du bloc <script> ────────────────────────────────

@pytest.mark.parametrize('cle', CLES)
@pytest.mark.parametrize('nom,charge', CHARGES_SORTIE)
def test_une_valeur_hostile_ne_sort_jamais_du_bloc_script(client, cle, nom, charge):
    r = client.get('/opportunities?view=radar&%s=%s' % (cle, charge))
    assert r.status_code == 200, 'la page doit rester servie (%s)' % r.status_code
    html = r.get_data(as_text=True)
    assert charge not in html, (
        'la charge « %s » ressort telle quelle dans les octets servis (clé %s)'
        % (nom, cle))
    assert not re.search(r'<img\s+src=x\s+onerror', html_actif(html), re.I), (
        'HTML ACTIF pollué par « %s » sur la clé %s' % (nom, cle))


@pytest.mark.parametrize('cle', CLES)
def test_le_bloc_PARAMS_ne_contient_aucune_balise_fermante(client, cle):
    charge = '</script><img src=x onerror=alert(1)>'
    html = client.get('/opportunities?view=radar&%s=%s' % (cle, charge)).get_data(as_text=True)
    m = re.search(r'const PARAMS=(\{.*?\});', html, re.S)
    assert m, 'const PARAMS introuvable — gardien à revoir'
    assert '</' not in m.group(1), (
        'le littéral PARAMS contient une balise fermante : %s' % m.group(1)[:120])


# ── 3. Le correctif ne change RIEN pour le client ────────────────────────────

@pytest.mark.parametrize('valeur', [
    'AAPL', 'Technologie', '', 'breakout', 'BUY',
    '</script><img src=x onerror=alert(1)>', 'a&b', 'x<y>z', "guillemet\"et\\anti",
    {'sym': 'MSFT', 'sector': '<Santé & Bien-être>'},
])
def test_json_for_script_preserve_exactement_la_valeur(valeur):
    """Les échappements `\\uXXXX` sont relus à l'identique : aucune régression
    fonctionnelle possible côté client."""
    assert json.loads(json_for_script(valeur)) == valeur


@pytest.mark.parametrize('brut', ['<', '>', '&'])
def test_json_for_script_neutralise_les_caracteres_de_balise(brut):
    sortie = json_for_script({'v': brut})
    assert brut not in sortie, '« %s » sort tel quel : %s' % (brut, sortie)
    assert '\\u00' in sortie, 'aucun échappement produit : %s' % sortie


def test_json_for_script_ne_touche_pas_aux_valeurs_legitimes():
    """Gardien pas TROP strict : une valeur normale doit rester lisible telle
    quelle dans la source servie (sinon le débogage devient impossible)."""
    assert json_for_script({'sym': 'AAPL'}) == '{"sym": "AAPL"}'
    assert json_for_script('radar') == '"radar"'


# ── 4. Contrat statique : plus jamais de `json.dumps` nu vers un `page_js` ───

def _appels_json_dumps_vers_un_gabarit(chemin):
    """Repère `X.replace('%%…%%', json.dumps(…))` — la forme exacte de la faille."""
    src = open(chemin, encoding='utf-8').read()
    fautes = []
    for n in ast.walk(ast.parse(src)):
        if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == 'replace' and len(n.args) == 2):
            continue
        motif, val = n.args
        if not (isinstance(motif, ast.Constant) and isinstance(motif.value, str)
                and motif.value.startswith('%%')):
            continue
        if (isinstance(val, ast.Call) and isinstance(val.func, ast.Attribute)
                and val.func.attr == 'dumps'):
            fautes.append((n.lineno, motif.value))
    return fautes


@pytest.mark.parametrize('page', ['opportunities_page', 'analysis_page', 'portfolio_page'])
def test_aucune_page_n_injecte_un_json_dumps_nu(page):
    chemin = 'vertex/ui/pages/%s.py' % page
    fautes = _appels_json_dumps_vers_un_gabarit(chemin)
    assert not fautes, (
        '%s injecte `json.dumps` nu dans un gabarit (%s) — utiliser '
        '`json_for_script` : une valeur contenant `</script>` sortirait du bloc'
        % (chemin, ', '.join('L%d %s' % f for f in fautes)))


def test_le_contrat_statique_mord_vraiment():
    """Anti-vide du contrat : sur une source fautive, le détecteur doit lever."""
    import tempfile
    faute = ('import json\n'
             "def render():\n"
             "    return _JS.replace('%%PARAMS%%', json.dumps({'a': 1}))\n")
    with tempfile.NamedTemporaryFile('w', suffix='.py', delete=False,
                                     encoding='utf-8') as fh:
        fh.write(faute)
        tmp = fh.name
    assert _appels_json_dumps_vers_un_gabarit(tmp), (
        'le détecteur ne repère pas la faute historique — gardien inutile')
