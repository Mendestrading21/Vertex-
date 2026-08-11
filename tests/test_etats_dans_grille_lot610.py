"""LOT 610 — UN ÉTAT POSÉ DANS UNE GRILLE OCCUPE TOUTE SA LARGEUR.

Mesuré en vrai Chromium : `VX.states.error(...)` écrit en **enfant direct** d'une
`.vx-grid` (cas de `#vx-mk-macro-regime`, ajouté au lot 603) tombe dans une
**colonne implicite** — bandeau large de **22 px**, contenu **coupé de 102 px**.

Et le défaut n'était **pas mobile** : identique à **390 px et à 1440 px**. La
preuve du lot 603 vérifiait la **présence** du texte attendu ; elle ne pouvait
pas voir qu'il était **illisible**.

Le correctif est une règle de **famille** (606-C) plutôt qu'un `vx-col-12` posé
sur le seul site fautif : tout état, présent ou futur, prend la grille entière.

Ce gardien vérifie la règle **dans l'octet servi**, pas seulement dans la source
— un fichier CSS peut exister et ne pas être servi.
"""

import io
import os
import re
import tempfile

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'css', 'layout.css')

# Les trois classes d'état que `VX.states` peut produire.
_CLASSES = ('.vx-state', '.vx-error-banner', '.vx-stale-banner')


def _regle():
    """Le bloc de la règle, lu sur disque."""
    src = io.open(_CSS, encoding='utf-8').read()
    m = re.search(r"((?:\.vx-grid\s*>\s*\.[\w-]+\s*,?\s*)+)\{([^}]*)\}", src)
    assert m, 'aucune règle `.vx-grid > .état` dans layout.css'
    return m.group(1), m.group(2)


def test_la_regle_existe_et_prend_toute_la_grille():
    selecteurs, corps = _regle()
    assert 'grid-column' in corps and '1 / -1' in corps.replace(' ', ' '), (
        "un état dans une grille doit occuper toutes les colonnes "
        "(`grid-column: 1 / -1`), sinon il tombe dans une colonne implicite : "
        "mesuré 22 px de large, contenu coupé de 102 px")


def test_la_regle_couvre_LES_TROIS_classes_d_etat():
    """606-C : garder la famille, pas le cas. Si une seule classe était couverte,
    le prochain état ajouté retomberait dans le trou."""
    selecteurs, _ = _regle()
    manquantes = [c for c in _CLASSES if ('.vx-grid > ' + c[1:]) not in
                  selecteurs.replace('.vx-grid>', '.vx-grid > ')
                  and ('.vx-grid > ' + c) not in
                  selecteurs.replace('.vx-grid>', '.vx-grid > ')]
    assert not manquantes, 'classes d’état non couvertes : %s' % manquantes


def test_la_regle_est_dans_l_octet_SERVI():
    """Un fichier CSS peut exister sans être servi. On demande la feuille à
    l'application, pas au disque."""
    os.environ['DEMO'] = '1'
    os.environ['NO_IBKR'] = '1'
    os.environ.pop('START_ON_IMPORT', None)
    # `_BASE_DIR` est un état GLOBAL partagé par toute la session pytest : le
    # détourner sans le rendre casse `test_persist` en aval. Mesuré : ce test a
    # fait tomber un test étranger avant d'être corrigé.
    import vertex.services.persist as persist
    _avant = persist._BASE_DIR
    persist._BASE_DIR = tempfile.mkdtemp()
    try:
        import terminal
        cli = terminal.app.test_client()
        r = cli.get('/static/vertex/css/layout.css')
    finally:
        persist._BASE_DIR = _avant
    assert r.status_code == 200, 'layout.css non servie (%d)' % r.status_code
    servi = r.get_data(as_text=True).replace('.vx-grid>', '.vx-grid > ')
    for c in _CLASSES:
        assert ('.vx-grid > ' + c) in servi, (
            '%s non couverte dans la feuille SERVIE' % c)
    assert '1 / -1' in servi


def test_le_site_du_lot_603_est_bien_un_hote_de_grille():
    """Garde-fou de volume (591-C) : si `#vx-mk-macro-regime` cessait d'être une
    grille, la règle deviendrait sans objet et ce fichier passerait en ne
    vérifiant plus rien de réel."""
    src = io.open(os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'markets_page.py'),
                  encoding='utf-8').read()
    m = re.search(r'<div class="([^"]*)" id="vx-mk-macro-regime"', src)
    assert m and 'vx-grid' in m.group(1), (
        "`#vx-mk-macro-regime` doit rester une grille — c'est le cas mesuré")
    assert "VX.states.error('Appétit pour le risque indisponible')" in src, (
        "l'état d'échec du lot 603 doit toujours être posé dans cette grille")
