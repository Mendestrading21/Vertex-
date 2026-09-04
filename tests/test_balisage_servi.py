"""LE BALISAGE SERVI EST CORRECTEMENT IMBRIQUÉ.

Ce banc existe à cause d'un défaut précis, et il vaut la peine de le raconter :
le dossier `/analysis/<sym>` — la page la plus importante du produit — était
cassé depuis longtemps parce qu'une `<section>` était fermée par un `</div>`
orphelin. Un navigateur ignore une fermante qui ne correspond à rien : la
section restait ouverte et TOUT le dossier (scores, physique, workspace, rail)
s'imbriquait dans une carte collante. Cartes empilées les unes sur les autres,
colonnes réduites à un mot par ligne, texte se chevauchant.

AUCUN contrôle ne pouvait l'attraper :
  · pas de débordement horizontal — le contenu débordait verticalement ;
  · pas d'erreur console — un balisage mal fermé n'est pas une erreur JS ;
  · pas de bloc vide — les blocs contenaient du texte, simplement illisible ;
  · la suite était verte — aucun test ne rend une page.

On lit le HTML **servi**, pas le DOM. Un navigateur répare toujours : son
`outerHTML` est bien formé par construction. L'interroger reviendrait à demander
au correcteur s'il a corrigé quelque chose.
"""
import importlib.util
import os

import pytest

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OUTIL = os.path.join(_ROOT, 'tools', 'audit', 'balisage.py')

#: Les routes servies. Les deux fiches par symbole sont incluses : c'est
#: précisément là que le défaut vivait.
ROUTES = ('/', '/calendar', '/markets', '/opportunities', '/analysis',
          '/analysis/AAPL', '/options', '/options/dossier/AAPL', '/simulator',
          '/portfolio', '/follow-up', '/performance', '/intelligence',
          '/system', '/design-system', '/journal', '/tracking')


def _analyseur():
    spec = importlib.util.spec_from_file_location('vx2_balisage', _OUTIL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope='module')
def client():
    import terminal
    terminal.app.config['TESTING'] = True
    return terminal.app.test_client()


@pytest.fixture(scope='module')
def analyseur():
    return _analyseur()


@pytest.mark.parametrize('route', ROUTES)
def test_le_balisage_servi_est_bien_imbrique(client, analyseur, route):
    html = client.get(route).get_data(as_text=True)
    r = analyseur.analyser(html)
    assert not r['orphelines'], (
        '%s : fermante(s) orpheline(s) — le navigateur les IGNORE, ce qui '
        'laisse une balise ouverte avaler la suite de la page : %s'
        % (route, r['orphelines']))
    assert not r['non_fermees'], (
        '%s : balise(s) jamais fermée(s) — tout ce qui suit s\'imbrique dedans '
        'et la mise en page s\'effondre sans qu\'aucune erreur ne soit levée : %s'
        % (route, r['non_fermees']))


# ── Contre-épreuve : un détecteur qu'on ne met pas en défaut ne prouve rien ──

def test_l_analyseur_attrape_le_defaut_qui_l_a_motive(analyseur):
    casse = ('<html><body><main class="vx-content">'
             '<section class="vx-card" id="an-hero">'
             '<div class="an-identity-main"><span>AAPL</span></div>'
             '</div>'                       # ← la faute exacte trouvée en août
             '<section id="an-profile"><div>profil</div></section>'
             '</main></body></html>')
    r = analyseur.analyser(casse)
    assert r['orphelines'] and r['orphelines'][0]['tag'] == 'div'
    assert r['orphelines'][0]['attendait'] == 'section'
    assert 'section' in r['non_fermees']


def test_l_analyseur_ne_crie_pas_sur_du_balisage_sain(analyseur):
    sain = ('<html><body><main class="vx-content">'
            '<section class="vx-card" id="an-hero">'
            '<div class="an-identity-main"><span>AAPL</span></div>'
            '</section>'
            '<section id="an-profile"><div>profil</div></section>'
            '</main></body></html>')
    r = analyseur.analyser(sain)
    assert not r['orphelines'] and not r['non_fermees']


def test_le_javascript_et_les_commentaires_ne_comptent_pas_comme_du_balisage(analyseur):
    """Ces pages construisent une bonne part de leur HTML côté client. Une
    chaîne JS contenant « </div> » n'est pas une balise ; la compter ferait
    de ce banc une source de faux positifs, donc un banc qu'on désactive."""
    bruit = ('<html><body><main>'
             '<script>el.innerHTML=\'<div class="x">\'+v+\'</div>\';</script>'
             '<!-- <section> citée dans un commentaire -->'
             '<div><span>ok</span></div>'
             '</main></body></html>')
    r = analyseur.analyser(bruit)
    assert not r['orphelines'] and not r['non_fermees']
