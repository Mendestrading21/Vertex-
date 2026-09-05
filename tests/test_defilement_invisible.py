"""UN CONTRÔLE CACHÉ DERRIÈRE UN DÉFILEMENT INVISIBLE EST UN CONTRÔLE ABSENT.

## Le défaut mesuré

Le dépôt traite `overflow-x:auto` comme LE REMÈDE au débordement — la sonde
`mesurer_qa_espaces` écarte d'ailleurs explicitement ces conteneurs, et elle a
raison : un contenu large mais défilable reste atteignable.

Sauf quand la barre de défilement est masquée. Deux endroits le faisaient :

    .vx-page-header .vx-actions   overflow-x:auto  +  scrollbar-width:none
    .vx2-tabs                     overflow-x:auto  +  scrollbar-width:none

Mesuré à 390 px sur les douze espaces :

  · le sélecteur de densité d'Aujourd'hui recevait 119 px pour 210 px de
    contenu — « Confort » finissait à 408 px et « Dense » à 470, hors d'un
    écran de 390. Deux options sur trois, invisibles ;
  · la barre d'onglets `.vx2-tabs` débordait sur HUIT espaces. Six sous-vues
    hors écran sur Options (Radar, Scénarios, Positions, Événements,
    Positionnement, Scanner LEAPS), cinq sur Système, quatre sur Vertex IA.

Rien ne le signalait. Ni erreur, ni coupe visible, ni barre : le produit
paraissait simplement avoir moins de fonctions qu'il n'en a.

## Les deux remèdes, et pourquoi ils diffèrent

La rangée d'actions **REPLIE** : trois contrôles tiennent sur deux lignes.
La barre d'onglets **DÉFILE toujours**, mais avec une barre fine visible :
replier 960 px d'onglets mangerait l'écran. Ce n'est pas le défilement qui
était le défaut, c'est l'absence de signal.

## La leçon de cascade, payée une fois

Le correctif de `.vx2-tabs` écrit dans `responsive.css` était SANS EFFET. La
coque charge les feuilles dans un ordre contractuel où `vertex-2-0.css` est la
dernière : sa règle de base, à spécificité égale, gagne par ordre de source —
y compris sur une media query écrite plus haut. Mesuré, pas déduit : le
premier jet laissait les huit débordements en place.
"""
from __future__ import annotations

import os
import re

import pytest

_RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_CSS = os.path.join(_RACINE, 'vertex', 'static', 'vertex', 'css')


def _feuille(nom: str) -> str:
    with open(os.path.join(_CSS, nom), encoding='utf-8') as f:
        return f.read()


def _bloc(src: str, selecteur: str) -> str | None:
    """Corps de la première règle portant EXACTEMENT ce sélecteur."""
    m = re.search(r'(?:^|[},;/])\s*' + re.escape(selecteur) + r'\s*\{([^}]*)\}',
                  src, re.M)
    return m.group(1) if m else None


# ── 1. Anti-vide : les feuilles et les sélecteurs existent ──────────────────

def test_les_feuilles_visees_existent_et_sont_peuplees():
    for nom in ('responsive.css', 'vertex-2-0.css', 'components.css'):
        assert len(_feuille(nom)) > 2000, '%s quasi vide' % nom


def test_les_deux_selecteurs_sont_bien_ceux_du_produit():
    """Si un sélecteur disparaissait, les contrôles ci-dessous seraient vrais
    sur rien — la panne exacte que ce dépôt appelle « un gardien muet »."""
    assert _bloc(_feuille('vertex-2-0.css'), '.vx2-tabs') is not None
    assert _bloc(_feuille('responsive.css'),
                 '.vx-page-header .vx-actions') is not None


# ── 2. La rangée d'actions REPLIE au lieu de défiler sans barre ─────────────

def test_la_rangee_d_actions_replie():
    corps = _bloc(_feuille('responsive.css'), '.vx-page-header .vx-actions')
    assert 'flex-wrap:wrap' in corps.replace(' ', ''), (
        'la rangée d’actions ne replie plus : %s' % corps)


def test_la_rangee_d_actions_ne_masque_plus_sa_barre():
    corps = _bloc(_feuille('responsive.css'), '.vx-page-header .vx-actions')
    plat = corps.replace(' ', '')
    assert not ('overflow-x:auto' in plat and 'scrollbar-width:none' in plat), (
        'la rangée redéfile avec sa barre masquée : le sélecteur de densité '
        'redeviendrait invisible à 390 px — %s' % corps)


# ── 3. La barre d'onglets défile AVEC un signal ─────────────────────────────

def test_la_barre_d_onglets_retrouve_une_barre_sur_mobile():
    src = _feuille('vertex-2-0.css')
    base = _bloc(src, '.vx2-tabs')
    assert 'scrollbar-width:none' in base.replace(' ', ''), (
        'la base a changé : ce banc garde une surcharge qui n’a plus d’objet')
    #  La surcharge doit venir APRÈS la base, dans CETTE feuille.
    apres = src[src.index(base):]
    assert 'scrollbar-width:thin' in apres.replace(' ', ''), (
        'aucune surcharge mobile après la règle de base : les onglets hors '
        'écran redeviendraient invisibles sur huit espaces')
    assert '@media (max-width:768px)' in apres, (
        'la surcharge n’est pas bornée au mobile — la barre apparaîtrait aussi '
        'sur desktop, où elle n’a pas lieu d’être')


def test_la_surcharge_vit_dans_la_COUCHE_FINALE_et_non_ailleurs():
    """La leçon de cascade, et elle a coûté un premier jet sans effet.

    `vertex/ui/shell/CSS_ORDER` est un CONTRAT d'ordre, pas une liste : le
    bundle concatène les feuilles dans cet ordre exact. `vertex-2-0.css` y est
    la dernière, donc sa règle de base `.vx2-tabs{scrollbar-width:none}`, à
    spécificité égale, l'emporte par ordre de source sur toute surcharge
    écrite plus haut — media query comprise. Écrite dans `responsive.css`, la
    correction laissait les huit débordements en place ; mesuré, pas déduit.
    """
    from vertex.ui.shell import CSS_ORDER

    assert 'vertex-2-0.css' in CSS_ORDER and 'responsive.css' in CSS_ORDER
    assert CSS_ORDER.index('responsive.css') < CSS_ORDER.index('vertex-2-0.css'), (
        'l’ordre de cascade a changé : `responsive.css` n’est plus AVANT la '
        'couche finale, et ce banc raisonne sur cet ordre')
    assert CSS_ORDER[-1] == 'vertex-2-0.css', (
        'la couche finale n’est plus la dernière : la surcharge de `.vx2-tabs` '
        'peut de nouveau être écrasée sans que rien ne le dise')

    #  Et le corollaire : aucune surcharge `.vx2-tabs` ne doit traîner dans
    #  `responsive.css`, où elle donnerait l'ILLUSION d'un correctif.
    #  Les COMMENTAIRES sont retirés d'abord : celui qui explique ce
    #  déplacement cite `.vx2-tabs{scrollbar-width:none}` en prose, et le
    #  balayage se déclenchait dessus. Troisième fois que cette leçon se
    #  présente dans ce dépôt — un contrôle qui lit du texte doit d'abord
    #  écarter ce qui n'a aucun effet.
    resp = re.sub(r'/\*.*?\*/', '', _feuille('responsive.css'), flags=re.S)
    for bloc in re.findall(r'\.vx2-tabs[^{]*\{([^}]*)\}', resp):
        assert 'scrollbar-width' not in bloc.replace(' ', ''), (
            'une surcharge de barre `.vx2-tabs` vit dans `responsive.css`, où '
            'la couche finale l’écrase : elle ferait croire le défaut corrigé '
            '— %s' % bloc)


# ── 4. Contre-épreuve : le bon motif reste employé ailleurs ─────────────────

def test_l_autre_barre_d_onglets_garde_son_signal():
    """`.vx-tabs` avait reçu ce remède bien avant. S'il disparaissait, ce banc
    garderait une règle que le produit n'applique plus qu'à moitié."""
    corps = _feuille('responsive.css').replace(' ', '')
    assert '.vx-tabs{scrollbar-width:thin' in corps, (
        'la barre d’onglets historique a reperdu son signal mobile')


def test_le_lecteur_de_regles_discrimine():
    """Contre-épreuve du lecteur : il doit trouver un bloc existant et rendre
    `None` sur un sélecteur absent, sinon les contrôles ci-dessus passeraient
    pour de mauvaises raisons."""
    faux = '.vx-quelque-chose-qui-n-existe-pas{color:red}'
    assert _bloc(faux, '.vx-quelque-chose-qui-n-existe-pas') == 'color:red'
    assert _bloc(faux, '.vx-autre-chose') is None
