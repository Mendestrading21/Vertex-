"""
LOT 374 — L'ANGLE MORT DÉCLARÉ AU LOT 373 : les blocs `<script>` CONCATÉNÉS.

Le balayage du lot 373 ne voyait que les interpolations situées dans **une**
chaîne littérale contenant `<script`. Un bloc ouvert dans une constante et fermé
dans une autre lui échappait entièrement : tout ce qui est concaténé entre les
deux vit en contexte JS sans qu'aucun gardien ne le sache.

**Verdict : l'angle mort est réel, mais il n'a aucune surface exploitable.**

Le balayage trouve **15 chaînes littérales déséquilibrées**, soit 4 points de
concaténation. Trois n'assemblent que des **constantes de module**
(`_OPP_BRIEF_JS`, `_sync_ui.JS`, `_VX_JS_FULL`, `ART_JS`). Le quatrième —
`terminal.py::_vpage`, `'…<script>' + js + '</script>…'` — est le seul à recevoir
un **paramètre**. Or ses 7 appelants passent tous une constante de module, et,
surtout, **les 7 pages ainsi construites ne sont plus servies** : `/bordel`,
`/review`, `/research`, `/heatmap`, `/equipe`, `/settings` et `/health` renvoient
un **301** vers les pages du redesign (table `_LEGACY` de
`vertex/app/routes/redesign.py`).

C'est cette **inaccessibilité** qui rend le verdict « sain » ; le dernier test
ci-dessous l'ancre explicitement, pour que la sûreté ne repose pas sur un fait
tacite. Si l'une de ces routes est un jour reservie, le contexte JS de `_vpage`
devra être réaudité.

**Constat de poids mort, mesuré au passage** (pour les dossiers de purge en
attente de GO — rien n'est engagé ici) : ces 7 constantes représentent
**618 527 octets (604 Ko) de HTML assemblés à chaque import** de `terminal.py`,
pour n'être jamais renvoyés.
"""
import ast
import re

import pytest

import terminal

PAGES = ['/', '/markets', '/opportunities', '/analysis', '/portfolio',
         '/options', '/journal', '/system']

# Routes héritées dont le 301 est la raison pour laquelle `_vpage` est sûr.
HERITEES = ['/bordel', '/review', '/research', '/heatmap', '/equipe',
            '/settings', '/health']

CONSTANTES_MORTES = ['PAGE_SETTINGS', 'PAGE_REVIEW', 'PAGE_RESEARCH',
                     'PAGE_HEALTH', 'PAGE_HEATMAP', 'PAGE_EQUIPE', 'PAGE_BORDEL']

_OUVRE = re.compile(r'<script\b[^>]*>', re.I)
_FERME = re.compile(r'</script\s*>', re.I)

_SRC = open('terminal.py', encoding='utf-8').read()
_ARBRE = ast.parse(_SRC)


@pytest.fixture(scope='module')
def client():
    return terminal.app.test_client()


def _est_litteral(n, connus=frozenset()):
    """Valeur entièrement constante à l'import : littéral, ou concaténation de
    littéraux et de noms eux-mêmes constants (`connus`).

    La résolution des NOMS est indispensable : `_BORDEL_JS` concatène trois
    constantes de module (`_VXSCATTER_JS`, `_SCATTER_HELP_JS`,
    `_BORDEL_MARKET_JS`). Un détecteur qui ne regarde que les littéraux directs
    le déclare « calculé » et crie au loup — c'est l'erreur qu'a d'abord commise
    ce gardien.
    """
    if isinstance(n, ast.Constant):
        return True
    if isinstance(n, ast.Name):
        return n.id in connus
    if isinstance(n, ast.JoinedStr):
        return all(isinstance(v, ast.Constant) or _est_litteral(v, connus)
                   for v in n.values)
    if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
        return _est_litteral(n.left, connus) and _est_litteral(n.right, connus)
    return False


def _noms_litteraux_du_module():
    """Noms liés, au niveau module, à une valeur constante — par point fixe,
    pour suivre les chaînes de constantes qui se référencent entre elles."""
    connus, change = set(), True
    while change:
        change = False
        for n in _ARBRE.body:
            if not isinstance(n, ast.Assign):
                continue
            cibles = [c.id for c in n.targets if isinstance(c, ast.Name)]
            if not cibles or all(c in connus for c in cibles):
                continue
            if _est_litteral(n.value, connus):
                connus.update(cibles)
                change = True
    return connus


def _appels_vpage():
    return [n for n in ast.walk(_ARBRE)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == '_vpage']


def _litteraux_desequilibres():
    """Chaînes littérales dont les balises <script> ne s'équilibrent pas."""
    out = []
    for n in ast.walk(_ARBRE):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            o, f = len(_OUVRE.findall(n.value)), len(_FERME.findall(n.value))
            if o != f:
                out.append((n.lineno, o, f))
    return out


# ── 1. Anti-vide : le détecteur voit-il l'angle mort ? ──────────────────────

def test_le_detecteur_trouve_bien_des_blocs_concatenes():
    des = _litteraux_desequilibres()
    assert len(des) >= 4, (
        'seulement %d littéral(aux) déséquilibré(s) trouvé(s) dans terminal.py — '
        'le détecteur est cassé, les tests suivants seraient vides' % len(des))


def test_le_detecteur_voit_les_appels_vpage():
    assert len(_appels_vpage()) >= 7, (
        "seulement %d appel(s) à `_vpage` — le détecteur ne voit plus la "
        'surface concaténée' % len(_appels_vpage()))


# ── 2. Le contexte JS concaténé ne reçoit jamais de valeur calculée ─────────

def _args_js_de_vpage():
    """[(ligne, nœud)] du `js` de chaque appel à `_vpage`."""
    out = []
    for appel in _appels_vpage():
        arg = next((k.value for k in appel.keywords if k.arg == 'js'), None)
        if arg is None and len(appel.args) >= 4:
            arg = appel.args[3]
        if arg is not None:
            out.append((appel.lineno, arg))
    return out


def test_le_js_concatene_ne_peut_pas_fermer_sa_propre_balise():
    """LA propriété qui protège, vérifiée sur les VALEURS RÉELLES.

    `_vpage` assemble `'<script>' + js + '</script>'`. Peu importe comment `js`
    est construit : ce qui compte est qu'il ne contienne pas lui-même de balise
    fermante, sinon le reste de la page passe en HTML actif.

    Un invariant syntaxique (« `js` doit être un littéral ») serait le mauvais
    outil : `_BORDEL_JS` concatène trois constantes dont deux sont produites par
    `_extract(PAGE_DAILY, …)` — constantes à l'import, mais pas littérales. Ce
    gardien a d'abord fait cette erreur et criait au loup.
    """
    fautes = []
    for ligne, arg in _args_js_de_vpage():
        if not isinstance(arg, ast.Name):
            continue
        valeur = getattr(terminal, arg.id, None)
        assert isinstance(valeur, str), (
            'L%d : `js=%s` n\'est pas une chaîne du module — gardien à revoir'
            % (ligne, arg.id))
        if _FERME.search(valeur):
            fautes.append((ligne, arg.id))
    assert not fautes, (
        'le JS concaténé de `_vpage` contient une balise fermante et sortirait '
        'de son bloc <script> : %s' % '; '.join('L%d %s' % f for f in fautes))


def test_le_js_concatene_reste_une_valeur_dimport_et_non_une_donnee_de_requete():
    """Complément statique : si `js` cessait d'être une constante du module pour
    devenir une expression calculée par requête, une valeur externe entrerait en
    contexte JS **sans passer par aucun gardien** — l'angle mort de ce lot."""
    connus = _noms_litteraux_du_module()
    fautes = []
    for ligne, arg in _args_js_de_vpage():
        if _est_litteral(arg, connus):
            continue
        if isinstance(arg, ast.Name) and isinstance(getattr(terminal, arg.id, None), str):
            continue                       # constante du module (même calculée à l'import)
        fautes.append((ligne, ast.unparse(arg)[:60]))
    assert not fautes, (
        '`js` calculé hors import injecté dans le <script> concaténé de '
        '`_vpage` : %s — sérialiser via `vertex.ui.shell.json_for_script` ou '
        'prouver la sûreté' % '; '.join('L%d ← %s' % f for f in fautes))


def test_les_appels_vpage_passent_bien_un_js():
    """Anti-vide du test précédent : s'il n'y a plus aucun `js`, il passerait
    à vide."""
    assert len(_args_js_de_vpage()) >= 7, (
        'seulement %d appel(s) `_vpage` avec un `js`' % len(_args_js_de_vpage()))


# ── 3. L'assemblage reste équilibré sur les octets servis ───────────────────

@pytest.mark.parametrize('page', PAGES)
def test_les_balises_script_sont_equilibrees_sur_les_pages_servies(client, page):
    html = client.get(page).get_data(as_text=True)
    o, f = len(_OUVRE.findall(html)), len(_FERME.findall(html))
    assert o == f, '%s : %d <script> ouverts pour %d fermés' % (page, o, f)
    assert o >= 8, (
        '%s : seulement %d bloc(s) <script> — page incomplète, le test '
        'précédent ne prouverait rien' % (page, o))


# ── 4. Le fait dont dépend le verdict : ces pages ne sont pas servies ───────

@pytest.mark.parametrize('route', HERITEES)
def test_les_routes_heritees_redirigent_toujours(client, route):
    """La sûreté du `<script>` concaténé de `_vpage` tient à ce que les 7 pages
    qu'il produit soient **inaccessibles**. Si l'une redevient servie, ce
    contexte JS doit être réaudité — d'où ce gardien."""
    r = client.get(route)
    assert r.status_code in (301, 302, 308), (
        '%s ne redirige plus (HTTP %s) : la page héritée construite par `_vpage` '
        'redevient servie — réauditer son bloc <script> concaténé'
        % (route, r.status_code))
    cible = r.headers.get('Location') or ''
    assert cible.startswith('/'), (
        '%s redirige hors du site (%r) — redirection ouverte' % (route, cible))


def test_les_constantes_heritees_existent_encore_mais_ne_sont_pas_servies():
    """Anti-péremption : si ces constantes disparaissent (purge É2/É3 engagée),
    ce gardien doit être revu plutôt que de passer à vide."""
    presentes = [n for n in CONSTANTES_MORTES if hasattr(terminal, n)]
    assert presentes, (
        'aucune constante héritée trouvée — la purge a eu lieu, ce gardien et '
        'sa liste `CONSTANTES_MORTES` sont à mettre à jour')
    for n in presentes:
        assert isinstance(getattr(terminal, n), str)
