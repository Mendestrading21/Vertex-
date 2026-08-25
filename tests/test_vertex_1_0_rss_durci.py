"""Vertex 1.0 — 398 OCTETS QUI EN RENDAIENT 800 000.

`parse_rss` lit du XML **distant et non fiable** : Vertex va chercher lui-même
le flux Google News. Il passait par `minidom.parseString`, dont l'expansion
d'entités est active.

## Mesuré le 25 août 2026, sur le vrai `parse_rss`

| niveaux | charge envoyée | titre rendu | facteur |
|---|---:|---:|---:|
| 3 | 233 o | 800 o | ×100 |
| 5 | 343 o | 80 000 o | ×10 000 |
| 6 | **398 o** | **800 000 o** | **×100 000** |

Chaque niveau supplémentaire multiplie par dix : neuf niveaux tiennent encore
dans 563 octets et rendent 800 Mo. C'est un *billion laughs*, nommé par
`AUDIT-TOTAL-2026-08-25` au chapitre sécurité.

## Le premier correctif ne corrigeait RIEN, et c'est la mesure qui l'a dit

Première tentative : poser les gestionnaires sur `ET.XMLParser().parser`. En
Python 3.12, `XMLParser` est l'implantation C et **n'expose pas** `.parser` —
le `getattr(..., None)` rendait donc le durcissement **silencieusement
inopérant**. La mesure d'après montrait l'expansion intacte. Un durcissement
qui ne durcit rien est pire que pas de durcissement : il rassure.

D'où le banc `test_le_durcissement_AGIT_vraiment` : il ne vérifie pas qu'une
API existe, il vérifie qu'une charge hostile **ne passe pas**.

## Pourquoi pas `defusedxml`

Une dépendance nouvelle exige licence vérifiée, version verrouillée, audit et
rollback (`CLAUDE.md`). Le refus posé ici est plus **strict** que le défaut de
`defusedxml` — qui interdit les entités mais parse encore le DTD — et tient
dans la bibliothèque standard.
"""
from __future__ import annotations

import time

from vertex.services import news_plus as NP


def _bombe(niveaux: int) -> str:
    """Expansion d'entités bornée. Chaque niveau multiplie par dix."""
    ents = ''.join(
        '<!ENTITY e%d "%s">' % (i, ('&e%d;' % (i - 1)) * 10 if i else 'A' * 8)
        for i in range(niveaux))
    return ('<?xml version="1.0"?><!DOCTYPE rss [%s]>'
            '<rss><channel><item><title>&e%d;</title></item>'
            '</channel></rss>' % (ents, niveaux - 1))


#  ═══════════  1. le durcissement AGIT — pas seulement il existe  ═════════════

def test_le_durcissement_AGIT_vraiment():
    """LE banc du lot. La première correction posait des gestionnaires sur un
    objet qui n'existe pas en Python 3.12 : elle ne durcissait rien, et rien
    ne le disait. Ce banc mesure l'EFFET, pas la présence d'une API."""
    charge = _bombe(6)
    assert len(charge) < 500, 'la charge doit rester minuscule : %d o' % len(charge)
    t0 = time.monotonic()
    assert NP.parse_rss(charge) == []
    assert time.monotonic() - t0 < 1.0


def test_l_expansion_est_refusee_a_TOUTES_les_profondeurs():
    for niveaux in (3, 5, 6, 9):
        assert NP.parse_rss(_bombe(niveaux)) == [], 'passe a %d niveaux' % niveaux


def test_une_entite_EXTERNE_est_refusee():
    """Une entité externe ferait lire un fichier local — ou ouvrir une requête
    sortante — depuis un flux que Vertex ne contrôle pas."""
    xxe = ('<?xml version="1.0"?><!DOCTYPE r ['
           '<!ENTITY x SYSTEM "file:///etc/passwd">]>'
           '<rss><channel><item><title>&x;</title></item></channel></rss>')
    assert NP.parse_rss(xxe) == []


def test_un_flux_TROP_VOLUMINEUX_est_refuse_AVANT_le_parsing():
    """Un flux hostile ne doit pas être lu du tout, pas seulement mal lu."""
    assert NP.parse_rss('<rss>' + 'A' * (NP.TAILLE_MAX_FLUX + 1) + '</rss>') == []


def test_le_plafond_laisse_une_marge_confortable_a_un_vrai_flux():
    """Un RSS Google News fait quelques dizaines de kilo-octets. Un plafond
    trop serré transformerait la protection en panne."""
    assert NP.TAILLE_MAX_FLUX >= 1024 * 1024


#  ═══════════  2. LA contre-épreuve : le flux sain passe toujours  ════════════

def test_un_flux_SAIN_est_toujours_lu():
    """Un durcissement qui casse la fonctionnalité est pire que le défaut : il
    supprime la source au lieu de la protéger."""
    sain = ('<?xml version="1.0"?><rss><channel>'
            '<item><title>NVDA record - Reuters</title>'
            '<link>https://x/1</link><pubDate>D1</pubDate>'
            '<source url="u">Reuters</source></item>'
            '<item><title>Chip demand - Bloomberg</title>'
            '<link>https://x/2</link><pubDate>D2</pubDate></item>'
            '</channel></rss>')
    out = NP.parse_rss(sain)
    assert len(out) == 2
    assert out[0] == {'title': 'NVDA record', 'link': 'https://x/1',
                      'publisher': 'Reuters', 'time': 'D1'}
    #  L'éditeur vient du suffixe du titre quand `<source>` manque.
    assert out[1]['publisher'] == 'Bloomberg'
    assert out[1]['title'] == 'Chip demand'


def test_le_plafond_n_est_PAS_applique_a_tort():
    """Contre-épreuve du plafond : un flux volumineux mais licite passe."""
    gros = ('<rss><channel>'
            + '<item><title>T - E</title><link>l</link></item>' * 200
            + '</channel></rss>')
    assert len(gros) < NP.TAILLE_MAX_FLUX
    assert len(NP.parse_rss(gros, n=4)) == 4


def test_un_flux_a_ESPACE_DE_NOMS_reste_lisible():
    """Certains agrégateurs préfixent leurs balises. Les rejeter ferait perdre
    la source sans rien protéger."""
    ns = ('<rss xmlns:x="urn:x"><channel>'
          '<x:item><x:title>Titre - Ed</x:title><x:link>l</x:link></x:item>'
          '</channel></rss>')
    out = NP.parse_rss(ns)
    assert out and out[0]['title'] == 'Titre'


#  ═══════════  3. le contrat d'origine est intact  ════════════════════════════

def test_le_cap_n_est_respecte():
    xml = ('<rss><channel>'
           + ''.join('<item><title>T%d - E%d</title><link>l%d</link></item>'
                     % (i, i, i) for i in range(6))
           + '</channel></rss>')
    assert len(NP.parse_rss(xml, n=4)) == 4


def test_un_titre_VIDE_est_ignore():
    assert NP.parse_rss(
        '<rss><channel><item><title></title></item></channel></rss>') == []


def test_du_charabia_rend_une_liste_vide_et_ne_LEVE_jamais():
    """C'est un repli réseau : il ne doit pas emporter l'appelant."""
    for mauvais in ('pas du xml <<<', '', None, b'\\x00\\x01', '<rss>'):
        assert NP.parse_rss(mauvais) == []


#  ═══════════  4. la raison reste écrite là où elle s'applique  ═══════════════

def test_le_motif_du_refus_est_documente_dans_le_module():
    """Un durcissement dont la raison n'est pas écrite se fait relâcher par le
    prochain lot pressé — surtout celui-ci, dont la première version ne
    marchait pas."""
    import pathlib
    src = pathlib.Path(NP.__file__).read_text(encoding='utf-8')
    assert 'billion laughs' in src.lower()
    assert 'defusedxml' in src, (
        "la raison de NE PAS ajouter la dependance doit rester ecrite")
    assert 'expat' in src
