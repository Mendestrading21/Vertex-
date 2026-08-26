"""tests/test_connections_lot55.py — SKYLER LOT 55 : connexions entre pages.

Directive utilisateur : « simplifier les connexions entre les pages ».
Audit réel préalable : l'infrastructure est déjà bonne (VX.openAnalysis
partout, délégation globale data-open-analysis, contexte sauvegardé,
tuiles KPI du briefing → domicile). Deux trous RÉELS trouvés et fermés
CENTRALEMENT :

1. FIL D'ARIANE MORT : « Vertex » et le segment d'espace étaient des
   <span>/<b> non cliquables — depuis une fiche `/analysis/AAPL`, cliquer
   « Analyse » doit ramener à `/analysis` et « Vertex » à `/`. Corrigé
   côté serveur (`_topbar`) ET côté client SPA (`updateCrumb` dérive le
   lien du menu latéral rendu — source unique, zéro duplication).

2. RETOUR CONTEXTUEL INCOMPLET : `SPACE_LABELS` (vx-shell.js §15)
   référençait les anciennes routes /performance et /intelligence mais
   PAS /options ni /journal — un retour depuis ces espaces affichait le
   chemin brut. Complété (les deux anciennes routes restent joignables,
   leurs libellés sont conservés).

Shell visible → SW v111 → v112.
"""
#  MARCHES EST FUSIONNE DANS LE DASHBOARD (Black Glass).
#
#  `/markets` ne sert plus de page : la route redirige 302 vers `/#…`
#  pour preserver les favoris. Les listes d'espaces ci-dessous ne le
#  citent donc plus, et les appels directs visent `/`, qui porte
#  desormais ce contenu. La couverture n'est pas perdue : elle a
#  simplement suivi le contenu.
import re

SHELL_PY = 'vertex/ui/shell/__init__.py'
SHELL_JS = 'vertex/static/vertex/js/vx-shell.js'
ROUTER_JS = 'vertex/static/vertex/js/vx-router.js'


def _read(p):
    return open(p, encoding='utf-8').read()


def test_breadcrumb_root_is_link_server_side():
    import terminal
    body = terminal.app.test_client().get('/').get_data(as_text=True)
    assert re.search(r'<a[^>]*class="vx-crumb-root"[^>]*href="/"', body)


def test_breadcrumb_space_is_link_server_side():
    import terminal
    body = terminal.app.test_client().get('/').get_data(as_text=True)
    m = re.search(r'<nav class="vx-breadcrumb"[^>]*>(.*?)</nav>', body, re.S)
    assert m, 'fil d’Ariane absent'
    assert re.search(r'<a[^>]*href="/markets"[^>]*>', m.group(1)), \
        'le segment d’espace doit être un lien vers la racine de l’espace'


def test_client_crumb_builds_links_from_sidebar():
    src = _read(ROUTER_JS)
    upd = src[src.index('function updateCrumb'):src.index('function updateActive')]
    assert 'vx-crumb-root' in upd
    assert 'data-nav-id' in upd            # href dérivé du menu rendu (source unique)
    assert 'href' in upd


def test_back_labels_cover_all_eight_spaces():
    src = _read(SHELL_JS)
    m = re.search(r'SPACE_LABELS = \{(.*?)\}', src, re.S)
    assert m, 'SPACE_LABELS introuvable'
    labels = m.group(1)
    for route in ("'/'", "'/opportunities'", "'/analysis'",
                  "'/portfolio'", "'/options'", "'/journal'", "'/system'"):
        assert route in labels, 'route absente du retour contextuel : %s' % route


def test_service_worker_bumped_to_at_least_v112():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 112
    assert 'td-shell-v111' not in body
