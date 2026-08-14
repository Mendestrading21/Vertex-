"""tests/test_polish_lot58.py — SKYLER LOT 58 : polish Portefeuille + Options.

Inspection systématique (leçons lots 56-57 : littéraux hors palette et
troncatures). Trouvé et corrigé :

1. `/options` (`options_intel_page.py`) : ~28 fallbacks `var(--x,#hex)`
   d'une ANCIENNE palette chaude (dont l'orange banni `#cf6128` et le
   cuivre `#b9683d`) — et surtout `--vx-text-dim` N'EXISTE PAS dans
   tokens.css : son fallback `#8a837a` se rendait DONC RÉELLEMENT sur
   toute la page (défaut actif, pas dormant). Tous les fallbacks
   réalignés sur les tokens EXISTANTS et leurs valeurs actuelles ;
   le tag démo passe du couple orange à `var(--vx-warning)`.

2. `/portfolio` (`portfolio_page.py`) : 4 fallbacks périmés de la même
   ancienne palette (#b7b2aa/#17191c/#dc6255/#39b878) réalignés ; le
   libellé de scénario ellipsé (150 px, layout de barres fixes) reçoit
   un `title` — l'info complète reste accessible sans casser
   l'alignement (l'aria-label la portait déjà).

Shell visible → SW v114 → v115.
"""
import re

OPTIONS = 'vertex/ui/pages/options_intel_page.py'
PORTFOLIO = 'vertex/ui/pages/portfolio_page.py'

# valeurs ACTUELLES des tokens (tokens.css) + palette officielle
CURRENT = {'#F8F5F3', '#BABABA', '#8A8284', '#989092', '#2BBE90', '#E9555F', '#D9BE3C',
           '#D28A54', '#30292B', '#0c0c0e', '#121214'}


def _read(p):
    return open(p, encoding='utf-8').read()


def _fallbacks(src):
    return re.findall(r"var\(--vx-[a-z0-9-]+,(#[0-9A-Fa-f]{6})\)", src)


def test_options_fallbacks_match_current_palette():
    bad = [c for c in _fallbacks(_read(OPTIONS)) if c not in CURRENT]
    assert not bad, 'fallbacks hors palette actuelle : %s' % sorted(set(bad))


def test_options_no_undefined_token_and_no_orange():
    src = _read(OPTIONS)
    assert '--vx-text-dim' not in src, \
        'token inexistant dans tokens.css — son fallback se rend toujours'
    assert '#cf6128' not in src and '#b9683d' not in src, 'orange/cuivre bannis'


def test_portfolio_fallbacks_match_current_palette():
    bad = [c for c in _fallbacks(_read(PORTFOLIO)) if c not in CURRENT]
    assert not bad, 'fallbacks hors palette actuelle : %s' % sorted(set(bad))


def test_portfolio_truncated_label_has_title():
    src = _read(PORTFOLIO)
    m = re.search(r"text-overflow:ellipsis[^>]*>'", src)
    if m:
        # la ligne qui ellipse doit porter un title avec le texte complet
        line_start = src.rfind('\n', 0, m.start())
        line = src[line_start:src.find('\n', m.end())]
        assert 'title=' in line, 'libellé ellipsé sans title (info inaccessible)'


def test_service_worker_bumped_to_at_least_v115():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 115
    assert 'td-shell-v114' not in body
