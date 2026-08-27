"""Vertex 1.0 · G4 — un âge affiché doit pouvoir REDEVENIR faux tout seul.

Ce fichier garde le défaut mesuré au chantier hors-ligne, et il garde deux
choses de nature différente, à ne pas confondre :

1. **le produit** — l'âge affiché est re-calculable (il porte son horodatage)
   et quelque chose le re-calcule sans rien demander au réseau ;
2. **l'instrument** — le classement par chiffre discrimine, et sa fenêtre
   d'observation est lue dans le produit au lieu d'être recopiée.

Le second point n'est pas de la coquetterie. La première version de la mesure
créditait 12 chiffres sur 15 comme « datés » : elle comptait la bannière
« Démo » — qui qualifie la NATURE de la donnée — comme un énoncé d'âge, et elle
observait 26 s alors que le re-datage a une période de 30 s. Deux erreurs qui
allaient toutes les deux dans le sens de l'indulgence : l'instrument déclarait
sain un produit qui ne l'était pas. Un gardien qui ne tiendrait que le produit
laisserait cette dérive revenir.

Ce que le défaut était, mesuré en vrai Chromium avec l'horloge de la page
avancée de deux heures : sur Marchés, **11 lignes de provenance sur 11 figées**
— « Il y a 21 min » indéfiniment, réseau vivant. Le calcul était juste
(`VX.fmt.ago` rendait bien « Aujourd'hui à 14:49 » sous horloge décalée) ; c'est
le RENDU qui n'était jamais rejoué, faute de toute tâche `VX.refresh` sur cette
page. Et réseau coupé, plus aucune page ne repeint — y compris celles qui
rafraîchissent d'habitude.
"""
from __future__ import annotations

import pathlib
import re

import pytest

RACINE = pathlib.Path(__file__).resolve().parents[1]
CORE = RACINE / 'vertex/static/vertex/js/vx-core.js'
BRIEFING = RACINE / 'vertex/ui/pages/briefing.py'


def _core() -> str:
    return CORE.read_text(encoding='utf-8')


# ── Le produit ───────────────────────────────────────────────────────────

def test_l_age_affiche_porte_son_horodatage():
    """Sans horodatage dans le DOM, l'âge ne peut PAS être recalculé : il est
    figé à la peinture, et il ment dès la minute suivante."""
    src = _core()
    bloc = src[src.index('VX.updateIndicator'):src.index('VX.states')]
    assert 'data-ts=' in bloc, (
        "`VX.updateIndicator` n'émet plus `data-ts` — l'âge redevient "
        'incalculable après coup, donc figé à la valeur peinte.')
    assert 'vx-update-age' in bloc, (
        "l'âge n'est plus isolé dans `.vx-update-age` — le re-datage ne peut "
        'plus le remplacer sans réécrire la source et le mode avec.')


def test_la_puce_de_fraicheur_conserve_son_instant_de_reference():
    src = _core()
    bloc = src[src.index('    chip(a) {'):src.index('_ms(ts) {')]
    assert re.search(r"data-at=[\"'].*a\.at", bloc), (
        "`VX.freshness.chip` n'émet plus `data-at` — la puce ne peut plus se "
        "ré-évaluer, elle reste sur l'état calculé au moment de la peinture.")
    assert 'r.at = at' in src, (
        "`assess` ne conserve plus l'instant de référence — `chip` n'a plus "
        'rien à inscrire.')


def test_quelque_chose_re_date_sans_rien_demander_au_reseau():
    """Le point entier du correctif : re-dater DOIT être possible hors ligne.
    Une tâche qui referait un `fetch` ne servirait à rien au moment où le
    problème se pose."""
    src = _core()
    assert "'freshness-retick'" in src, (
        'aucune tâche de re-datage enregistrée — les âges redeviennent figés.')
    assert 'persistent: true' in src[src.index("'freshness-retick'") - 200:
                                     src.index("'freshness-retick'") + 200], (
        'le re-datage doit être une tâche de SHELL : une tâche de page est '
        'arrêtée au teardown, et les âges regèlent à la première navigation.')
    corps = src[src.index('_retick(racine)'):src.index("'freshness-retick'")]
    for interdit in ('fetch(', 'XMLHttpRequest', 'VX.fetch'):
        assert interdit not in corps, (
            'le re-datage appelle %s : il ne fonctionnerait plus hors ligne, '
            'précisément le cas pour lequel il existe.' % interdit)


def test_les_kpi_de_tete_portent_un_age_et_ne_l_ecrivent_pas_a_la_main():
    """Les chiffres de l'accueil ne portaient AUCUNE date : la seule marque de
    la carte etait le badge « Demo ». La regle du produit est que l'age vienne
    d'un helper, jamais d'une etiquette ecrite a la main.

    Black Glass sert cet age par `VX.updateIndicator(<horodatage reel>, ...)`
    plutot que par `VX.freshness.chip`. L'exigence porte sur ce qui compte —
    un horodatage DERIVE de la donnee — pas sur le nom du helper.
    """
    src = BRIEFING.read_text(encoding='utf-8')
    assert 'VX.updateIndicator(' in src, "l'accueil ne date plus rien"

    #  Le point dur : l'horodatage doit venir de la DONNEE. Un
    #  `updateIndicator(Date.now(), ...)` redaterait la carte a chaque rendu.
    fautifs = [l.strip()[:90] for l in src.splitlines()
               if 'updateIndicator(Date.now()' in l]
    assert fautifs == [], (
        "l'accueil se date de l'instant du rendu : %r" % fautifs)

    #  Et au moins une carte lit l'horodatage REEL du scan.
    assert 'scan.scan_ts' in src or 'scan_state' in src, (
        "aucune carte de l'accueil ne lit l'horodatage du scan")



# ── L'instrument ─────────────────────────────────────────────────────────

def test_le_classement_par_chiffre_discrimine_les_trois_familles():
    """Trois familles, trois issues distinctes. Un classeur qui rangerait tout
    dans la même rendrait « 0 anomalie » sur n'importe quel produit."""
    from tools.vertex_1_0.mesurer_hors_ligne import classer_chiffres

    def m(etat, genre='etat', datable=False):
        return {'etat': etat, 'genre': genre, 'datable': datable, 'texte': ''}

    entree = [
        {'valeur': 'frais', 'marques': [m('snapshot')]},
        {'valeur': 'degrade', 'marques': [m('stale')]},
        {'valeur': 'age', 'marques': [m('fallback', 'age', True)]},
        {'valeur': 'demo', 'marques': [m('fallback')]},
        {'valeur': 'rien', 'marques': []},
    ]
    c = classer_chiffres(entree)
    assert [x['valeur'] for x in c['date_faux']] == ['frais']
    assert [x['valeur'] for x in c['date']] == ['degrade', 'age']
    assert [x['valeur'] for x in c['nu']] == ['demo', 'rien'], (
        'une bannière « Démo » qualifie la NATURE de la donnée, pas son âge : '
        "la compter comme une date était l'indulgence qui créditait 12 "
        'chiffres sur 15 à tort.')


def test_une_provenance_live_n_est_pas_une_affirmation_de_fraicheur():
    """`.vx-update[data-mode=live]` dit D'OÙ vient la donnée, pas qu'elle est
    fraîche — son âge est écrit à côté. Les confondre faisait ressortir
    « daté faux » les quatre chiffres de Système, dont la portée contient une
    ligne `/healthz Live`."""
    from tools.vertex_1_0.mesurer_hors_ligne import classer_chiffres
    c = classer_chiffres([{'valeur': 'x', 'marques': [
        {'etat': 'live', 'genre': 'age', 'datable': True, 'texte': ''}]}])
    assert [x['valeur'] for x in c['date']] == ['x']
    assert not c['date_faux']


def test_la_fenetre_d_observation_est_lue_dans_le_produit():
    """Mesurer 26 s après avoir vieilli de 2 h reprochait au produit un
    mensonge qu'il n'avait pas encore eu l'occasion de corriger. La fenêtre
    doit suivre la période servie, pas une constante recopiée."""
    from tools.vertex_1_0.mesurer_hors_ligne import periode_retick_s
    p = periode_retick_s()
    assert p > 0
    assert ("%d000, 'freshness-retick'" % p) in _core(), (
        'la période lue ne correspond plus à la période servie.')


def test_l_instrument_refuse_de_mesurer_si_la_periode_est_introuvable():
    """Un instrument qui ne trouve pas ce qu'il doit lire doit s'ARRÊTER, pas
    retomber sur une valeur par défaut : une fenêtre supposée produirait un
    verdict qui ne veut rien dire."""
    import tools.vertex_1_0.mesurer_hors_ligne as mod
    vrai = mod.RACINE
    mod.RACINE = pathlib.Path(__file__).resolve().parents[1] / '_absent_'
    try:
        with pytest.raises((SystemExit, OSError)):
            mod.periode_retick_s()
    finally:
        mod.RACINE = vrai
