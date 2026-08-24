"""Vertex 1.0 - AUCUNE ECRITURE innerHTML NUE VIA $().

Le defaut, vecu trois fois avant d etre compris : une page a des vues
(?view=regime, sectors, macro...). Changer de vue REMPLACE le DOM, et une
requete encore en vol reprend la main ensuite sur un element supprime -
« unhandledrejection: Cannot set properties of null (setting innerHTML) ».
Intermittent, donc longtemps mis sur le compte du hasard.

Ce qui a mis sur la piste n est pas une trace : c est une INCOHERENCE.
markets_page.py gardait deja trois ecritures (if(el), if(t), if(f)) et en
laissait vingt et une nues.

La premiere correction n a traite QUE /markets - et l erreur est revenue
le lendemain sur `/`. Le recensement a alors montre 169 ecritures nues
dans ONZE fichiers : le defaut etait produit-wide, pas propre a une page.
Ce gardien tient le plafond a zero pour que la lecon ne se reperde pas.
"""
from __future__ import annotations

import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: `$('x').innerHTML=` sans garde. La forme SURE est `($('x')||{})`.
MOTIF_NU = re.compile(r"\$\('[a-zA-Z0-9\-_]+'\)\.innerHTML\s*=")


def _fichiers_servis():
    out = []
    for rac, _d, noms in os.walk(os.path.join(RACINE, 'vertex')):
        if '__pycache__' in rac:
            continue
        for n in noms:
            if n.endswith(('.py', '.js')):
                out.append(os.path.join(rac, n).replace(os.sep, '/'))
    return sorted(out)


def test_le_balayage_couvre_bien_les_pages_et_le_js():
    """Un gardien qui tourne a vide rendrait « 0 defaut » sans rien lire."""
    f = _fichiers_servis()
    assert len(f) >= 60, "le balayage ne couvre presque rien"
    assert any(x.endswith('ui/pages/briefing.py') for x in f)
    assert any(x.endswith('js/vx-shell.js') for x in f)


def test_aucune_ecriture_innerHTML_nue():
    """169 ecritures nues mesurees dans 11 fichiers le jour du correctif.

    Le plafond est ZERO et non un nombre a faire baisser : la forme sure
    coute une parenthese, il n y a donc aucun cas ou la forme nue se
    justifie."""
    fautifs = []
    for p in _fichiers_servis():
        try:
            s = open(p, encoding='utf-8', errors='ignore').read()
        except OSError:
            continue
        n = len(MOTIF_NU.findall(s))
        if n:
            fautifs.append('%s: %d' % (os.path.relpath(p, RACINE).replace(os.sep, '/'), n))
    assert not fautifs, (
        'ecriture innerHTML sans garde - une requete en vol qui revient sur '
        'un DOM remplace rompra la promesse :' + '\n  ' + '\n  '.join(fautifs))


def test_la_forme_sure_est_bien_celle_qui_est_servie():
    """Contre-epreuve : le remplacement a bien eu lieu, il n a pas juste
    fait disparaitre les ecritures."""
    p = os.path.join(RACINE, 'vertex', 'ui', 'pages', 'briefing.py')
    s = open(p, encoding='utf-8').read()
    assert "||{}).innerHTML" in s, (
        'la page d accueil doit porter la forme sure - 16 ecritures y ont '
        'ete converties')
