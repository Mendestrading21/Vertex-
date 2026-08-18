"""tests/test_polish_lot59.py — SKYLER LOT 59 : Journal + Système + transversal.

Clôture de la passe polish : le balayage du lot 58 est GÉNÉRALISÉ à
TOUTES les pages (gardien transversal prospectif). Trouvé et corrigé :

- ~45 fallbacks `var(--x,#hex)` d'anciennes palettes dans 7 fichiers de
  pages (system_page : 3 oranges bannis `#cf6128` de plus ; performance
  (= /journal) : un `--vx-brand,#84aa31` VERT aberrant ; tracking,
  analysis, markets, opportunities, design_system_demo) ;
- DEUX tokens INEXISTANTS référencés avec fallback — leurs fallbacks se
  rendaient donc réellement : `--vx-text-dim` (déjà vu au lot 58 sur
  /options, restait 6 pages) et `--vx-neutral` (Opportunités, #9d978e) ;
- vérifié SAIN (non touché, dit) : les états vides/erreur passent par
  `VX.states.empty/error` sur les 8 pages (déjà harmonisés).

Shell visible → SW v115 → v116.
"""
import glob
import re

# valeurs ACTUELLES autorisées en fallback (tokens.css + palette officielle)
CURRENT = {'#F8F5F3', '#BABABA', '#8A8284', '#989092', '#2BBE90', '#E9555F', '#D9BE3C',
           '#D28A54', '#30292B', '#0c0c0e', '#121214', '#c8bfae', '#9B7BFF',
           '#45D6E8'}


def _pages():
    return sorted(glob.glob('vertex/ui/pages/*.py'))


def _defined_tokens():
    names = set()
    for css in glob.glob('vertex/static/vertex/css/*.css'):
        src = open(css, encoding='utf-8').read()
        names |= set(re.findall(r"(--vx-[a-z0-9-]+)\s*:", src))
    return names


def test_all_pages_fallbacks_match_current_palette():
    bad = []
    for page in _pages():
        src = open(page, encoding='utf-8').read()
        for col in re.findall(r"var\(--vx-[a-z0-9-]+,(#[0-9A-Fa-f]{6})\)", src):
            if col not in CURRENT:
                bad.append('%s: %s' % (page, col))
    assert not bad, 'fallbacks hors palette actuelle :\n' + '\n'.join(sorted(set(bad)))


def test_all_referenced_tokens_exist():
    """Un token inexistant rend TOUJOURS son fallback — divergence silencieuse
    (deux cas réels : --vx-text-dim, --vx-neutral). Gardien prospectif."""
    defined = _defined_tokens()
    bad = []
    for page in _pages():
        src = open(page, encoding='utf-8').read()
        for name in set(re.findall(r"var\((--vx-[a-z0-9-]+),#", src)):
            if name not in defined:
                bad.append('%s: %s' % (page, name))
    assert not bad, 'tokens inexistants référencés :\n' + '\n'.join(sorted(bad))


def test_no_banned_orange_in_pages():
    bad = []
    for page in _pages():
        src = open(page, encoding='utf-8').read()
        for col in ('#cf6128', '#b9683d', '#cc892c'):
            if col in src:
                bad.append('%s: %s' % (page, col))
    assert not bad, 'oranges bannis présents :\n' + '\n'.join(sorted(bad))


def test_service_worker_bumped_to_at_least_v116():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 116
    assert 'td-shell-v115' not in body
