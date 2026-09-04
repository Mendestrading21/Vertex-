"""Controle 075 — ce que Vertex rend quand JavaScript est entierement coupe.

Le controle etait « RÉUSSI partiellement » sur une limite honnete : le repli
sans Canvas etait verifie, le cas « JS entierement desactive » ne l'etait pas.
Il l'est maintenant, et la mesure a montre un defaut reel : **53 squelettes**
sur dix pages -- 22 sur la seule page d'accueil -- promettaient une donnee
qu'aucun script ne viendrait chercher. Un ecran qui fait semblant de charger
ment plus qu'un ecran qui dit non.

La coque porte desormais deux choses, et ce banc garde les deux :

  1. un `<noscript><style>` qui masque tous les squelettes -- sans script,
     ils ne sont plus une attente mais un mensonge ;
  2. un bandeau qui dit *pourquoi* l'ecran est muet, dans le flux du contenu
     et non derriere la barre laterale fixe (premiere version : ses premiers
     mots passaient sous la barre).

La preuve visuelle se fait au navigateur, moteur JS coupe
(`tools/audit/sans_js.py` : 0 constat sur les 12 pages, contre-epreuve
executee). Ce banc garde ce que la CI verifie sans navigateur : que les deux
dispositifs existent, et qu'ils sont au bon endroit.
"""
from __future__ import annotations

import pathlib
import re

SHELL = pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'ui' / 'shell' / '__init__.py'
CSS = pathlib.Path(__file__).resolve().parents[1] / 'vertex' / 'static' / 'vertex' / 'css' / 'vertex-2-0.css'


def _shell() -> str:
    return SHELL.read_text(encoding='utf-8')


def test_les_squelettes_sont_masques_quand_js_est_coupe():
    src = _shell()
    bloc = re.search(r'<noscript><style>(.*?)</style></noscript>', src, re.S)
    assert bloc, (
        "la coque ne porte plus de <noscript><style> : sans lui, 53 squelettes "
        "promettent une donnee qu'aucun script ne chargera."
    )
    corps = bloc.group(1)
    for classe in ('.vx-skeleton', '.vx2-skeleton'):
        assert classe in corps, (
            '%s n\'est plus masquee sans JavaScript.' % classe
        )
    assert 'display:none' in corps.replace(' ', ''), (
        'le bloc <noscript> ne masque plus rien.'
    )
    # Les accolades doivent etre DOUBLEES : la coque est un f-string, et une
    # accolade simple y est lue comme un champ a formater. La premiere version
    # de ce bloc a fait tomber toutes les pages en boucle de redirection.
    assert '{{display:none !important}}' in corps, (
        "les accolades du bloc <noscript> doivent etre doublees : la coque est "
        "un f-string, une accolade simple leve NameError et l'application "
        "repond 302 en boucle."
    )


def test_le_bandeau_sans_js_est_dans_la_colonne_de_contenu():
    src = _shell()
    assert 'vx2-noscript' in src, (
        "le bandeau qui explique l'absence de donnees a disparu de la coque."
    )
    debut_contenu = src.find('id="vx-content"')
    place = src.find('vx2-noscript')
    assert debut_contenu != -1 and place > debut_contenu, (
        "le bandeau doit vivre DANS #vx-content : pose avant `.vx-app`, la barre "
        "laterale fixe recouvrait ses premiers mots -- mesure au navigateur."
    )
    assert 'role="alert"' in src[place - 200:place + 200], (
        "le bandeau doit s'annoncer comme une alerte."
    )


def test_le_bandeau_a_un_style_servi():
    assert '.vx2-noscript{' in CSS.read_text(encoding='utf-8'), (
        "le bandeau sans JavaScript n'a plus de regle dans la feuille servie : "
        "il rendrait du texte nu, sans cadre ni couleur de prudence."
    )
