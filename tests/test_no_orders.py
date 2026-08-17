"""
tests/test_no_orders.py — GARDE-FOU DE SÛRETÉ (non négociable).

VERTEX est un terminal d'ANALYSE, en LECTURE SEULE. Ces tests échouent si du
code d'exécution d'ordre apparaît, ou si le verrou IBKR readonly est retiré.
Ils protègent l'invariant produit : aucun ordre ne peut jamais être passé.
"""

import os
import re
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Appels d'exécution d'ordre formellement interdits dans tout le dépôt.
FORBIDDEN = [
    r'\bplaceOrder\b',
    r'\bsubmitOrder\b',
    r'\bbracketOrder\b',
    r'\bMarketOrder\b',
    r'\bLimitOrder\b',
    r'\bStopOrder\b',
    r'\breqGlobalCancel\b',
    r'\.placeOrder\(',
    # Noms d'exécution étendus (§2 Ultimate) — appels et définitions
    r'(?:\.|\bdef\s+|\bfunction\s+)auto_close_position\s*\(',
    r'(?:\.|\bdef\s+|\bfunction\s+)auto_rebalance\s*\(',
    r'(?:\.|\bdef\s+|\bfunction\s+)one_click_trade\s*\(',
    r'(?:\.|\bdef\s+|\bfunction\s+)auto_execute\s*\(',
]

def _fichiers(*extensions):
    """Code applicatif et moteurs — on exclut les fichiers de test (qui citent
    volontairement les motifs interdits), le cache et les bibliotheques
    minifiees de tiers.

    LOT 31 — l'extension `.js` a ete AJOUTEE apres une mutation qui a SURVECU :
    un `placeOrder(` place dans un fichier `.js` passait tous les tests, parce
    que ce balayage ne regardait que le Python. Or Vertex est massivement
    ecrit en JavaScript : le garde-fou le plus important du produit ignorait
    la moitie du produit.
    """
    for ext in extensions:
        for path in glob.glob(os.path.join(ROOT, '**', '*' + ext), recursive=True):
            base = os.path.basename(path)
            if ('/.git/' in path or '__pycache__' in path
                    or base.startswith('test_') or base.endswith('.min.js')):
                continue
            yield path


def _py_files():
    return _fichiers('.py')


def _sans_commentaires_python(src):
    """Blanchit les COMMENTAIRES d'un source Python, rien d'autre.

    LOT 34 — ce balayage signale une MENTION, pas un APPEL. Il a accusé la
    docstring d'un outil de sûreté qui doit nommer le verbe qu'il sert
    justement à tenir hors du code. Interdire de NOMMER la chose dans un
    commentaire n'ajoute aucune sûreté : ça pousse à écrire des documents
    vagues à l'endroit précis où il faut être exact.

    Les CHAÎNES restent scannées : `getattr(ib, 'placeOrder')` doit continuer
    d'être vu, et c'est justement la forme qu'aucune liste ne rattrape ailleurs.
    Un échec de `tokenize` (fichier illisible) rend la source INTACTE — on
    scanne trop plutôt que trop peu.
    """
    try:
        import io
        import tokenize
        lignes = src.splitlines(keepends=True)
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type != tokenize.COMMENT:
                continue
            i, d, f = tok.start[0] - 1, tok.start[1], tok.end[1]
            lignes[i] = lignes[i][:d] + ' ' * (f - d) + lignes[i][f:]
        return ''.join(lignes)
    except Exception:
        return src


def _sans_docstrings_python(src):
    """Blanchit les DOCSTRINGS (module, classe, fonction) — pas les autres
    chaînes. Même raison : documenter l'interdit n'est pas l'enfreindre."""
    try:
        import ast
        arbre = ast.parse(src)
        lignes = src.splitlines(keepends=True)
        for n in ast.walk(arbre):
            if not isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef,
                                  ast.AsyncFunctionDef)):
                continue
            corps = getattr(n, 'body', None) or []
            if not (corps and isinstance(corps[0], ast.Expr)
                    and isinstance(corps[0].value, ast.Constant)
                    and isinstance(corps[0].value.value, str)):
                continue
            d = corps[0].value
            for i in range(d.lineno - 1, d.end_lineno):
                lignes[i] = re.sub(r'\S', ' ', lignes[i])
        return ''.join(lignes)
    except Exception:
        return src


def test_no_order_execution_calls():
    """Aucun appel d'exécution d'ordre dans le code source — Python ET
    JavaScript. Mesuré au lot 31 : le balayage ignorait le JS, et une mutation
    y a survecu. Lot 34 : commentaires et docstrings Python sont exclus — ils
    ne s'exécutent pas, et les nommer est le travail d'un document de sûreté."""
    hits = []
    for path in _fichiers('.py', '.js'):
        try:
            src = open(path, encoding='utf-8').read()
        except Exception:
            continue
        scanne = src
        if path.endswith('.py'):
            scanne = _sans_docstrings_python(_sans_commentaires_python(src))
        for pat in FORBIDDEN:
            for m in re.finditer(pat, scanne):
                line = scanne[:m.start()].count('\n') + 1
                hits.append(f'{os.path.relpath(path, ROOT)}:{line}  {pat}')
    assert not hits, 'Code d\'exécution d\'ordre détecté (INTERDIT) :\n' + '\n'.join(hits)


def test_le_balayage_voit_encore_un_vrai_appel_malgre_l_exclusion():
    """TÉMOIN du lot 34 — exclure commentaires et docstrings ne doit RIEN
    aveugler d'exécutable. Trois formes, dont la chaîne (nom calculé), qui reste
    scannée exprès."""
    src = ('"""Docstring qui nomme placeOrder — a ignorer."""\n'
           '# commentaire qui nomme placeOrder — a ignorer\n'
           'ib.placeOrder(c, o)\n'
           "getattr(ib, 'placeOrder')()\n")
    vu = _sans_docstrings_python(_sans_commentaires_python(src))
    assert vu.count('placeOrder') == 2, (
        'le blanchiment a mange un appel reel, ou laisse passer une mention : %r' % vu)
    assert re.search(r'\.placeOrder\(', vu) and "getattr(ib, 'placeOrder')" in vu


def test_ibkr_is_readonly():
    """Toute connexion IBKR doit forcer readonly=True."""
    connects = []
    for path in _py_files():
        try:
            src = open(path, encoding='utf-8').read()
        except Exception:
            continue
        for m in re.finditer(r'\.connect\s*\(', src):
            seg = src[m.start():m.start() + 220]
            # LOT 31 — LE TROU, prouve par mutation : l'ancienne version
            # n'exigeait `readonly=True` QUE si le mot « readonly » figurait
            # deja dans l'appel. Le RETIRER purement et simplement passait donc
            # tous les tests — exactement le geste qu'un correctif distrait
            # produit. Un garde-fou qui ne se declenche que si la protection
            # est encore la ne protege rien.
            #
            # Une connexion IBKR est reconnue par `clientId=` : c'est ce qui la
            # distingue de la facade sans argument (`gateway.connect()`) et de
            # tout autre `.connect(` du depot. Les quatre sites reels du
            # produit le portent (ibkr_gateway + trois dans terminal.py).
            if not re.search(r'clientId\s*=', seg):
                continue
            assert re.search(r'readonly\s*=\s*True', seg), (
                '%s:%d : connexion IBKR SANS readonly=True. Le verrou lecture '
                'seule est l\'invariant produit absolu — il ne se retire pas, '
                'meme temporairement.'
                % (os.path.relpath(path, ROOT), src[:m.start()].count('\n') + 1))
            connects.append(path)
    # Le produit DOIT garder au moins un point de connexion IBKR verrouille :
    # sans cette assertion, supprimer la passerelle rendrait le test vide et
    # vert — un garde-fou qui disparait avec ce qu'il garde.
    assert connects, (
        'aucune connexion IBKR verrouillee trouvee : soit la passerelle a '
        'disparu, soit le motif de detection ne la reconnait plus.')


def test_config_readonly_invariant():
    """Le module de config affirme explicitement l'invariant lecture seule."""
    from vertex.app import config
    assert config.READONLY is True
    assert config.ANALYSIS_ONLY is True
