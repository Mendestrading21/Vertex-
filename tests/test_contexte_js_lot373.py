"""
LOT 373 — LA FAUTE DU LOT 372 SOUS SES AUTRES HABILLAGES.

Le lot 372 a corrigé `json.dumps` nu vers un gabarit `%%…%%` dans trois pages.
Mais la faute réelle est plus large : **toute valeur non littérale interpolée à
l'intérieur d'une région `<script>`** peut fermer la balise. Ce lot balaie les
autres formes (f-strings, `%`-format) et les autres producteurs de HTML.

**Verdict : aucune faille exploitable — mais un danger latent trouvé.**

`vertex.engines.recommendation.vocab_js()` est un `json.dumps` **nu** injecté
dans `<script id="vx-vocab">window.__VXVOCAB={vocab};</script>` — c'est-à-dire
**sur les 8 pages**, l'endroit le plus exposé de l'application. Il ne tient
aujourd'hui que parce que son contenu est **100 % constant** (`DECISIONS`,
`HELD`, `_ALIAS`, `TONE_CLS` : des tables littérales du module) et ne contient
ni `<`, ni `>`, ni `&`. **Rien ne le vérifiait.** Une seule étiquette future
contenant `<` ferait sortir le script sur les huit pages à la fois.

On garde donc l'invariant plutôt que de durcir : appliquer `json_for_script` ici
changerait les octets servis sur les 8 pages **sans aucun gain** — `vocab_js`
sérialise avec `ensure_ascii=False` alors que `json_for_script` laisse la valeur
par défaut, si bien que tous les accents deviendraient `\\uXXXX`. Un durcissement
qui coûte un bump de service worker pour zéro sécurité n'est pas un durcissement.

Les deux `%%VIEW%%` restés bruts (`markets_page`, `performance_page`) vivent dans
`const VIEW='%%VIEW%%'` — une chaîne JS entre apostrophes, dont une charge
s'échapperait. Ils tiennent par la **liste blanche appliquée avant la
substitution** ; sondés ici sur un rendu réel.

Note de méthode : ma première passe d'audit a manqué **`vertex/ui/shell/__init__.py`
en entier** — le producteur HTML central — parce qu'elle listait les fichiers avec
`os.listdir`, qui ne descend pas dans les sous-dossiers. C'est précisément là que
vivait le `json.dumps` nu. Le dernier test ci-dessous verrouille cette leçon.
"""
import ast
import json
import os
import re

import pytest

import terminal
from vertex.engines.recommendation import vocab_js
from vertex.ui.shell import json_for_script

PAGES = ['/', '/markets', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']

_OUVRE = re.compile(r'<script\b[^>]*>', re.I)
_FERME = re.compile(r'</script\s*>', re.I)
_GABARIT = re.compile(r'%%[A-Z_0-9]+%%')
_BLOC = re.compile(r'<script\b[^>]*>.*?</script\s*>', re.S | re.I)

# Substitutions vers un gabarit situé DANS un <script> qui ne passent NI par un
# littéral NI par `json_for_script`. Chacune doit être justifiée ici.
EXCEPTIONS = {
    # `view` est réduit à la liste blanche `_VIEWS` AVANT la substitution
    # (sondé ci-dessous sur un rendu réel + gardien du lot 367).
    ('vertex/ui/pages/markets_page.py', '%%VIEW%%'),
    ('vertex/ui/pages/performance_page.py', '%%VIEW%%'),
}


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


def _fichiers_html():
    """TOUS les producteurs de HTML — récursivement (leçon de ce lot)."""
    out = ['terminal.py']
    for base in ('vertex/ui', 'vertex/app'):
        for rac, _d, noms in os.walk(base):
            for nom in sorted(noms):
                if nom.endswith('.py'):
                    c = os.path.join(rac, nom)
                    if c not in out:
                        out.append(c)
    return out


def _regions_script(texte):
    res, pos = [], 0
    while True:
        o = _OUVRE.search(texte, pos)
        if not o:
            return res
        f = _FERME.search(texte, o.end())
        res.append((o.end(), f.start() if f else len(texte)))
        pos = f.end() if f else len(texte)


def _substitutions_en_contexte_js():
    """[(fichier, gabarit, code substitué, sûr?)] pour les gabarits dans un <script>."""
    out = []
    for chemin in _fichiers_html():
        src = open(chemin, encoding='utf-8', errors='ignore').read()
        try:
            arbre = ast.parse(src)
        except SyntaxError:
            continue
        noms = set()
        for n in ast.walk(arbre):
            if isinstance(n, ast.Constant) and isinstance(n.value, str) \
                    and '<script' in n.value.lower():
                for deb, fin in _regions_script(n.value):
                    noms.update(_GABARIT.findall(n.value[deb:fin]))
        if not noms:
            continue
        for n in ast.walk(arbre):
            if not (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr == 'replace' and len(n.args) == 2):
                continue
            motif, val = n.args
            if not (isinstance(motif, ast.Constant) and motif.value in noms):
                continue
            code = ast.unparse(val)
            sur = isinstance(val, ast.Constant) or 'json_for_script' in code
            out.append((chemin, motif.value, code, sur))
    return out


# ── 1. Anti-vide : le détecteur voit-il quelque chose ? ─────────────────────

def test_le_detecteur_trouve_bien_des_gabarits_en_contexte_js():
    subs = _substitutions_en_contexte_js()
    assert len(subs) >= 5, (
        'seulement %d substitution(s) en contexte JS trouvée(s) — le détecteur '
        'est cassé, les tests suivants seraient vides' % len(subs))


def test_le_balayage_couvre_le_shell():
    """La faute de ma première passe : `os.listdir` ne descend pas dans les
    sous-dossiers, donc `vertex/ui/shell/__init__.py` — le producteur HTML
    central — n'était jamais lu."""
    assert 'vertex/ui/shell/__init__.py' in _fichiers_html(), (
        'le balayage ne couvre pas le shell — angle mort du lot 373')


# ── 2. Toute interpolation en contexte JS est sûre ou justifiée ─────────────

def test_aucune_interpolation_js_non_justifiee():
    fautes = [(c, g, code) for c, g, code, sur in _substitutions_en_contexte_js()
              if not sur and (c, g) not in EXCEPTIONS]
    assert not fautes, (
        'valeur non littérale injectée dans un bloc <script> sans '
        '`json_for_script` et sans justification : %s'
        % '; '.join('%s %s ← %s' % f for f in fautes))


def test_les_exceptions_existent_encore():
    """Gardien pas TROP permissif : une exception qui ne correspond plus à rien
    doit être retirée, sinon la liste blanche se périme en silence."""
    vus = {(c, g) for c, g, _code, _sur in _substitutions_en_contexte_js()}
    mortes = EXCEPTIONS - vus
    assert not mortes, 'exceptions périmées à retirer : %s' % sorted(mortes)


# ── 3. Le vocabulaire ne peut pas sortir de sa balise ───────────────────────

@pytest.mark.parametrize('interdit', ['<', '>', '&'])
def test_le_vocabulaire_ne_contient_aucun_caractere_de_balise(interdit):
    """`vocab_js()` est un `json.dumps` NU injecté dans un <script> sur les
    8 pages : il ne tient QUE parce que son contenu est constant et sans `<`.
    Si une étiquette en introduit un, il faut passer par `json_for_script`."""
    assert interdit not in vocab_js(), (
        'window.__VXVOCAB contient « %s » : le bloc <script> peut être fermé '
        'sur les 8 pages — sérialiser via `json_for_script`' % interdit)


def test_le_vocabulaire_reste_un_json_valide_et_non_vide():
    table = json.loads(vocab_js())
    assert isinstance(table, dict) and len(table) >= 10, (
        'table de vocabulaire vide ou dégénérée (%s entrées)' % len(table))


@pytest.mark.parametrize('page', PAGES)
def test_le_bloc_vocab_est_unique_et_clos_sur_chaque_page(client, page):
    html = client.get(page).get_data(as_text=True)
    blocs = re.findall(r'<script id="vx-vocab">(.*?)</script>', html, re.S)
    assert len(blocs) == 1, '%s : %d bloc(s) vx-vocab' % (page, len(blocs))
    assert '<' not in blocs[0], '%s : le bloc vocab contient « < »' % page


# ── 4. Les deux `const VIEW='…'` bruts, sondés sur un rendu réel ────────────

CHARGES = [
    ("sortie d'apostrophe", "';alert(1);'"),
    ('sortie de balise', '</script><img src=x onerror=alert(1)>'),
    ('concaténation JS', "'-alert(1)-'"),
    ('apostrophe nue', "o'brien"),
]


@pytest.mark.parametrize('route', ['/markets', '/journal'])
@pytest.mark.parametrize('nom,charge', CHARGES)
def test_une_vue_hostile_est_remplacee_par_la_liste_blanche(client, route, nom, charge):
    r = client.get('%s?view=%s' % (route, charge))
    assert r.status_code == 200, 'la page doit rester servie (%s)' % r.status_code
    html = r.get_data(as_text=True)
    assert len(html) > 20000, 'rendu incomplet (%d o) — la sonde ne prouverait rien' % len(html)
    vues = re.findall(r"const VIEW\s*=\s*'([^']*)'", html)
    assert vues, "const VIEW n'est plus servie — gardien à revoir"
    for v in vues:
        assert re.fullmatch(r'[a-z_]+', v), 'const VIEW hostile servie : %r' % v
    assert charge not in html, 'la charge « %s » ressort dans la page' % nom
    assert not re.search(r'<img\s+src=x\s+onerror', _BLOC.sub(' ', html), re.I), (
        'HTML actif pollué par « %s » sur %s' % (nom, route))


@pytest.mark.parametrize('route,vue', [('/markets', 'sectors'), ('/journal', 'overview')])
def test_une_vue_legitime_traverse_bien(client, route, vue):
    """Gardien pas TROP strict : la liste blanche ne doit pas tout écraser."""
    html = client.get('%s?view=%s' % (route, vue)).get_data(as_text=True)
    assert "const VIEW='%s'" % vue in html, (
        '%s : la vue légitime « %s » n\'atteint pas le rendu' % (route, vue))


# ── 5. `json_for_script` : la propriété dont dépend tout le reste ───────────

def test_json_for_script_rend_impossible_la_sortie_de_balise():
    charge = {'x': '</script><img src=x onerror=alert(1)>'}
    sortie = json_for_script(charge)
    assert '</' not in sortie and '<' not in sortie
    assert json.loads(sortie) == charge, 'la valeur doit être préservée'
