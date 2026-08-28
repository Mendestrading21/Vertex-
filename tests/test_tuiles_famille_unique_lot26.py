"""Contrôle 048 — les familles de tuiles historiques rendent une seule tuile.

Le dépôt porte trois noms pour la même chose : `vx-kpi`, `vx-stat`,
`vx-metric`. Ils sont employés 138 fois ; les migrer changerait 138 fichiers
sans rien changer à l'écran. Ce qui a été unifié, c'est l'IMPLÉMENTATION :
une seule surface, un seul libellé, un seul chiffre — dont seule la TAILLE
varie, et cette variation est déclarée.

La preuve visuelle se fait au navigateur (`tools/vertex_2_0_tuiles.py`, qui
compare les styles calculés et sort en erreur au moindre écart non voulu).
Ce banc-ci garde ce que la CI peut vérifier sans navigateur : que la règle
d'unification EXISTE encore, qu'elle nomme les TROIS familles, et que la
seule chose qu'on ait laissée diverger soit la taille du chiffre.

Il ne remplace pas l'outil : il empêche qu'on retire la règle sans le voir.
"""
from __future__ import annotations

import pathlib
import re

CSS = pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'static' / 'vertex' / 'css' / 'vertex-2-0.css'

FAMILLES = ('.vx-card.vx-kpi', '.vx-stat:not(.vx-stat-xl)', '.vx-metric')


def _regles(texte: str) -> list[tuple[str, str]]:
    """(sélecteurs, corps) pour chaque règle de premier niveau, commentaires ôtés."""
    texte = re.sub(r'/\*.*?\*/', '', texte, flags=re.S)
    return [(m.group(1).strip(), m.group(2))
            for m in re.finditer(r'([^{}@]+)\{([^{}]*)\}', texte)]


def _regle_partagee(regles, marqueurs):
    for sel, corps in regles:
        if all(m in sel for m in marqueurs):
            return sel, corps
    return None, None


def test_les_trois_familles_partagent_une_regle_de_surface():
    """Une même règle doit poser la boîte des trois tuiles à la fois."""
    _, corps = _regle_partagee(_regles(CSS.read_text(encoding='utf-8')), FAMILLES)
    assert corps is not None, (
        'aucune règle ne nomme les trois familles ensemble : '
        + ', '.join(FAMILLES) + ". L'unification du contrôle 048 a disparu."
    )
    for propriete in ('display', 'padding'):
        assert propriete in corps, (
            'la règle partagée ne pose plus « %s » : les trois tuiles peuvent '
            'à nouveau diverger sur ce point.' % propriete
        )


def test_le_libelle_et_le_chiffre_ont_chacun_une_seule_voix():
    """Libellé et chiffre sont déclarés une fois pour les trois familles."""
    regles = _regles(CSS.read_text(encoding='utf-8'))
    for quoi, marqueurs, attendus in (
            ('libellé', ('.vx-kpi-label', '.vx-stat-k', '.vx-metric-k'),
             ('font-size', 'font-weight', 'text-transform')),
            ('chiffre', ('.vx-kpi-value', '.vx-stat-v', '.vx-metric-v'),
             ('font-weight', 'color', 'font-variant-numeric'))):
        _, corps = _regle_partagee(regles, marqueurs)
        assert corps is not None, (
            'le %s des tuiles n\'est plus déclaré une seule fois pour les trois '
            'familles (%s).' % (quoi, ', '.join(marqueurs))
        )
        for prop in attendus:
            assert prop in corps, (
                'la règle partagée du %s ne pose plus « %s ».' % (quoi, prop)
            )


def test_la_taille_du_chiffre_est_le_seul_ecart_et_il_est_declare():
    """Trois tailles, trois déclarations séparées, aucune ambiguïté."""
    regles = _regles(CSS.read_text(encoding='utf-8'))
    tailles = {}
    for sel, corps in regles:
        for cle, marqueur in (('kpi', '.vx-kpi-value'), ('stat', '.vx-stat-v'),
                              ('metric', '.vx-metric-v')):
            if marqueur in sel and ',' not in sel:
                m = re.search(r'font-size:\s*([\d.]+)px', corps)
                if m:
                    tailles[cle] = float(m.group(1))
    assert set(tailles) == {'kpi', 'stat', 'metric'}, (
        'chaque famille doit déclarer SA taille de chiffre, seule et nommée ; '
        'trouvé : %s' % sorted(tailles)
    )
    assert tailles['metric'] < tailles['stat'] < tailles['kpi'], (
        'les trois tailles doivent former une échelle croissante compacte → '
        'courante → forte ; trouvé %s' % tailles
    )


def test_le_halo_permanent_des_chiffres_est_neutralise():
    """La direction Black Glass interdit le halo permanent."""
    texte = CSS.read_text(encoding='utf-8')
    for jeton in ('--vx-glow-pos', '--vx-glow-neg'):
        assert re.search(re.escape(jeton) + r'\s*:\s*none', texte), (
            'le jeton %s n\'est plus neutralisé : `cockpit.css`, qui EST servie, '
            'reposerait un halo de 15 px sur chaque chiffre positif ou négatif.'
            % jeton
        )
