"""tests/test_polish_inspection.py — SKYLER LOT 64 : tour d'inspection honnête.

Audit navigateur étendu des 8 pages × 2 viewports (débordements : 0 ;
boutons sans nom accessible : 0 ; erreurs console : 0). UNE classe de
défauts réels trouvée : des éléments `.vx-truncate` (ellipse CSS)
perdaient de l'information SANS `title` — impossible de lire le texte
complet (signal des Meilleures opportunités sur Aujourd'hui, secteurs
sur Marchés mobile, thèses/catalyseurs du Portefeuille, setup
d'Opportunités, leçons du Journal, logs de Système).

Corrigé aux 8 points d'appel + GARDIEN PROSPECTIF : tout usage de
`vx-truncate` dans les pages doit porter un `title` sur la même ligne
(l'aria/lecteur d'écran et la souris retrouvent toujours le texte
entier — cohérent avec la règle « jamais de perte d'info » du lot 57).

Shell visible → SW v119 → v120.
"""
import glob
import re


def test_every_truncate_has_title():
    bad = []
    for page in sorted(glob.glob('vertex/ui/pages/*.py')):
        for n, line in enumerate(open(page, encoding='utf-8'), 1):
            if 'vx-truncate' in line and 'title=' not in line:
                bad.append('%s:%d' % (page, n))
    assert not bad, 'vx-truncate sans title (info perdue) :\n' + '\n'.join(bad)


def test_service_worker_bumped_to_at_least_v120():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 120
    assert 'td-shell-v119' not in body
