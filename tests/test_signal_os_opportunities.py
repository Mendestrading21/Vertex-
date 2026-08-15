"""SIGNAL OS · OPPORTUNITÉS — des titres qui décrivaient le logiciel.

Inventaire des titres RENDUS, mesuré au navigateur sur les quatre vues :

| avant | ce qui n'allait pas |
| --- | --- |
| `Ce qui mérite ton attention` | une phrase d'accueil, pas un objet — c'est le `Here is what you need to know` que `COPY.md` proscrit |
| `Shortlist — méritent une analyse` | une shortlist **est** ce qui mérite une analyse |
| `Scatter d'asymétrie — qualité × timing` | « Scatter » est le TYPE de graphique ; l'utilisateur cherche un couple qualité × timing, pas un nuage de points |
| `Comparaison des meilleurs candidats` | trois mots pour un |
| `Les dossiers les plus utiles maintenant` | vague, et « maintenant » est vrai de toute la page |
| `Shortlist options — relais vers l'espace Options` | « relais vers l'espace » explique le LOGICIEL ; le lien juste dessous porte déjà l'action |
| `Classement Skyler — score canonique /40` × 3 | « canonique » est du vocabulaire interne |

`COPY.md` : « Préférer des noms d'objets ou de décisions. » Un titre nomme la
chose ; il n'annonce pas ce que la chose va faire.

## Ce que ce lot ne fait PAS

Il ne touche ni aux données, ni aux graphiques, ni à la structure de la page.
La forme des cartes d'opportunité (`ticker → grade → score → verdict →
asymétrie → catalyseur → invalidation`) et l'entonnoir restent tels quels : ils
étaient déjà conformes à `PAGES.md`. **Un lot de micro-copy, et il le dit.**
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_OPP = os.path.join(_ROOT, 'vertex', 'ui', 'pages', 'opportunities_page.py')
_JS = os.path.join(_ROOT, 'vertex', 'static', 'vertex', 'js', 'signal-os.js')


def _src():
    return io.open(_OPP, encoding='utf-8').read()


def _sans_commentaires(src):
    """L'explication d'un retrait cite ce qui a été retiré."""
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    src = re.sub(r'<!--.*?-->', '', src, flags=re.S)
    return '\n'.join(l for l in src.split('\n') if not l.lstrip().startswith('#'))


_TITRES = (
    '<span class="vx-card-title">Priorités</span>',
    '<span class="vx-card-title">Sélection</span>',
    '<span class="vx-card-title">Dossiers à étudier</span>',
    '<span class="vx-card-title">Shortlist options</span>',
    '<span class="vx-chart-title">Comparaison</span>',
    "title:'Qualité × timing'",
)


def test_les_titres_viennent_du_serveur():
    src = _src()
    for titre in _TITRES:
        assert titre in src, 'titre non écrit à la source : %s' % titre


def test_les_anciens_titres_ont_disparu_des_octets_servis():
    """Tant qu'un ancien libellé reste dans la source, le serveur l'envoie et
    une couche JS doit le corriger à l'écran — deux vérités."""
    code = _sans_commentaires(_src())
    for mort in ('Ce qui mérite ton attention',
                 'Shortlist — méritent une analyse',
                 "Scatter d\\'asymétrie",
                 'Comparaison des meilleurs candidats',
                 'Les dossiers les plus utiles maintenant',
                 'relais vers l’espace Options',
                 'score canonique /40'):
        assert mort not in code, 'ancien libellé toujours servi : « %s »' % mort


def test_le_graphique_garde_sa_question():
    """CONTRE-EXEMPLE. Raccourcir un titre de graphique ne doit pas faire
    disparaître la question à laquelle il répond — `CHARTS.md` l'exige, et
    « Qualité × timing » seul ne dit pas ce qu'on y cherche."""
    src = _src()
    i = src.index("title:'Qualité × timing'")
    voisinage = src[i:i + 260]
    assert 'question:' in voisinage, (
        'le scatter a perdu sa question en même temps que son ancien titre.')
    assert 'qualité × timing ?' in voisinage


def test_les_noms_accessibles_restent_explicites():
    """Un titre court à l'écran, un nom complet pour un lecteur d'écran :
    « Sélection » seul ne dit pas de quoi parle la région."""
    src = _src()
    for aria in ('aria-label="Entonnoir de sélection"',
                 'aria-label="Réponse du radar"',
                 'aria-label="Shortlist options"'):
        assert aria in src, 'nom accessible perdu : %s' % aria


def test_les_erreurs_ne_recrachent_plus_le_message_technique():
    """`COPY.md` : ne pas exposer de jargon réseau brut, traduire en impact.
    Deux zones concaténaient `e.message` dans un état d'erreur visible."""
    code = _sans_commentaires(_src())
    assert 'e.message' not in code, (
        'un message d\'exception brut est de nouveau affiché à l\'utilisateur.')
    for honnete in ('Simulation indisponible.',
                    'Impossible de charger les opportunités.'):
        assert honnete in code


def test_la_table_de_reecriture_ne_porte_plus_cette_page():
    js = io.open(_JS, encoding='utf-8').read()
    for mort in ('Quelles opportunités méritent réellement une analyse ?',
                 'Shortlist — méritent une analyse',
                 "Scanner d'anomalies"):
        assert mort not in js, (
            'entrée « %s » encore dans la table alors qu\'Opportunités est '
            'reconstruite.' % mort)
