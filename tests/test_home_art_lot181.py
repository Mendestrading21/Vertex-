"""
LOT 181 — Caractérisation de la COUCHE ARTISTIQUE de l'accueil
(`vertex/ui/home_art.py`, 171 lignes, ZÉRO test — VIVANTE : appliquée
sur PAGE_DAILY et PAGE_STRATEGIE dans terminal.py). Deux fonctions
pures d'injection HTML + un tableau graphique nourri par
/api/market/summary. Figé : l'injection avant </body>, le
progressive enhancement, la syntaxe JS RÉELLE (node --check — deux
SyntaxError silencieuses ont déjà vécu, règle critique n°2) et le
câblage effectif dans les pages servies.
"""
import subprocess

from vertex.ui import home_art as ha


# ── apply / apply_desk : injection pure ──────────────────────────────────────

def test_apply_injecte_style_et_script_une_fois_avant_body():
    page = '<html><body><p>contenu</p></body></html>'
    out = ha.apply(page)
    assert out.count('</body>') == 1
    assert out.index('<p>contenu</p>') < out.index('<style>')   # contenu intact avant
    assert '<style>' + ha.ART_CSS in out
    assert '<script>' + ha.ART_JS in out
    assert out.endswith('</script></body></html>')


def test_apply_sans_body_page_inchangee():
    # Pas de </body> → no-op silencieux, jamais une exception ni un doublon.
    assert ha.apply('<div>fragment</div>') == '<div>fragment</div>'


def test_apply_desk_css_seul_aucun_script():
    out = ha.apply_desk('<body>x</body>')
    assert '<style>' + ha.DESK_CSS in out
    assert '<script>' not in out                    # le desk n'ajoute AUCUN JS


# ── Le JS injecté est du JavaScript VALIDE (règle critique n°2) ──────────────

def test_art_js_syntaxe_validee_par_node(tmp_path):
    # Deux SyntaxError silencieuses ont déjà vécu dans des chaînes JS générées
    # depuis Python — la couche artistique est vérifiée par un vrai parseur.
    f = tmp_path / 'art.js'
    f.write_text(ha.ART_JS, encoding='utf-8')
    r = subprocess.run(['node', '--check', str(f)], capture_output=True, text=True, encoding='utf-8')
    assert r.returncode == 0, r.stderr


# ── Progressive enhancement et contrat de données ────────────────────────────

def test_progressive_enhancement_fallbacks_presents():
    # Sans IntersectionObserver → tout devient visible (catch → artin partout) ;
    # sans #ovMarket → le script s'arrête proprement ; reduced-motion respecté
    # dans les DEUX CSS.
    assert "catch(e){document.querySelectorAll('.ovchap,.ovc')" in ha.ART_JS
    assert "if(!mk)return;" in ha.ART_JS
    assert 'prefers-reduced-motion' in ha.ART_CSS
    assert 'prefers-reduced-motion' in ha.DESK_CSS


def test_tableau_nourri_par_market_summary_rafraichi_90s_onglet_visible():
    assert "fetch('/api/market/summary')" in ha.ART_JS
    assert 'if(!document.hidden)load()' in ha.ART_JS   # pas de fetch onglet caché
    assert '},90000);' in ha.ART_JS                    # cadence 90 s


def test_chiffres_localises_fr_et_lecture_vix_14_22():
    # Affichage localisé + les bandes NARRATIVES du VIX (≤14 serein, ≥22 stress)
    # — distinctes des bandes de données 16/22 du moteur (lot 153).
    assert "toLocaleString('fr-FR')" in ha.ART_JS
    assert 'vx.price<=14' in ha.ART_JS
    assert 'vx.price>=22' in ha.ART_JS
    assert "'—'" in ha.ART_JS                          # VIX absent → tiret honnête


# ── Statut : ORPHELIN documenté (lot 36) ────────────────────────────────────

def test_module_orphelin_plus_aucun_cablage_dans_terminal():
    """La couche pages de terminal.py (PAGE_DAILY…) est retirée au lot 36 :
    home_art n'a PLUS de consommateur servi. Le module et ses tests de pureté
    restent en attendant le lot de retrait dédié (preuves de convergence) —
    mais terminal.py ne doit pas le réimporter sans nouvelle doctrine."""
    src = open('terminal.py', encoding='utf-8').read()
    assert 'home_art' not in src
