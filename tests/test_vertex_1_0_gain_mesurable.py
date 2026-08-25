"""Vertex 1.0 — UN CORRECTIF INVISIBLE DOIT SE MESURER QUELQUE PART.

Le lot précédent a cessé de demander au courtier des contrats qui n'existent
pas. Son effet est **invisible par construction** : il se voit dans ce qui
n'arrive plus. Le seul moyen de l'observer était de compter les
« Aucune définition de titre trouvée » sur deux journaux du courtier, à la
main — donc personne ne l'aurait fait, et le lot serait resté une intention.

Ce banc garde le compteur qui rend le gain lisible, et surtout **ce qu'il ne
doit pas dire** :

- `part_evitee_pct` vaut `None` tant que rien n'a été proposé. Afficher 0 %
  ferait passer « je n'ai pas mesuré » pour « je n'évite rien » — la même
  faute que `scan_fait: None` corrige ailleurs (D-054).
- une redemande faute de mieux n'est **jamais** comptée comme une économie :
  on refait alors le travail entier.
- la section n'apparaît pas sans source injectée : « rien d'inventé sans
  source » vaut aussi pour un état vrai.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from vertex.observability.diagnostics import system_diagnostics
from vertex.options import strike_memory as M


@pytest.fixture(autouse=True)
def _memoire_neuve():
    M.oublier_tout()
    yield
    M.oublier_tout()


#  ═══════════  1. le compteur dit la vérité, y compris qu'il ignore  ══════════

def test_sans_aucune_mesure_la_part_evitee_est_INCONNUE_pas_zero():
    """0 % dirait « je n'évite rien ». `None` dit « je n'ai rien mesuré ».
    Les deux ne s'affichent pas pareil, et ne se décident pas pareil."""
    s = M.statistiques()
    assert s['strikes_proposes'] == 0
    assert s['part_evitee_pct'] is None


def test_ce_qui_est_evite_est_compte_exactement():
    M.noter_refus('GDDY', '20261016', [97, 98, 99, 101, 102])
    M.filtrer('GDDY', '20261016', [97, 98, 99, 100, 101, 102, 105, 110])
    s = M.statistiques()
    assert s['strikes_proposes'] == 8
    assert s['strikes_evites'] == 5
    assert s['part_evitee_pct'] == 62.5


def test_une_REDEMANDE_faute_de_mieux_n_est_pas_une_economie():
    """La garde anti-aveuglement refait le travail ENTIER. La compter comme
    évitée gonflerait le gain d'un travail intégralement repayé."""
    M.noter_refus('AAPL', '20261016', [300, 305])
    rendus = M.filtrer('AAPL', '20261016', [300, 305])
    assert rendus == [300, 305], "la garde doit bien redemander"
    s = M.statistiques()
    assert s['strikes_evites'] == 0
    assert s['redemandes_faute_de_mieux'] == 1
    assert s['part_evitee_pct'] == 0.0


def test_le_cas_reel_de_GDDY_donne_un_chiffre_parlant():
    """11 refus sur 14 demandés, mesurés sur le compte réel le 25 août 2026 :
    seuls 100, 105 et 110 existent."""
    refuses = [97, 98, 99, 101, 102, 103, 104, 106, 107, 108, 109]
    M.noter_refus('GDDY', '20261016', refuses)
    M.filtrer('GDDY', '20261016', refuses + [100, 105, 110])
    assert M.statistiques()['part_evitee_pct'] == pytest.approx(78.6, abs=0.1)


#  ═══════════  2. la section n'existe pas sans source  ════════════════════════

def test_aucune_section_sans_source_INJECTEE():
    """« Rien d'inventé sans source » vaut aussi pour un état vrai : un banc
    antérieur a déjà refusé une section qui s'importait elle-même."""
    assert 'option_strikes' not in system_diagnostics()


def test_la_section_apparait_quand_la_source_est_fournie():
    d = system_diagnostics(option_strikes=M)
    assert 'option_strikes' in d
    assert set(d['option_strikes']) >= {
        'couples', 'refus_retenus', 'strikes_proposes', 'strikes_evites',
        'redemandes_faute_de_mieux', 'part_evitee_pct'}


def test_la_route_INJECTE_bien_la_memoire():
    """Un compteur parfait que la route n'expose pas n'est visible nulle part."""
    src = (Path(__file__).resolve().parents[1] / 'vertex' / 'app' / 'routes'
           / 'strategy_os_api.py').read_text(encoding='utf-8')
    i = src.index("def diagnostics():")
    bloc = src[i:i + 700]
    assert 'strike_memory' in bloc
    assert 'option_strikes=' in bloc


#  ═══════════  3. l'écran le montre, sans mentir  ═════════════════════════════

def _page():
    return (Path(__file__).resolve().parents[1] / 'vertex' / 'ui' / 'pages'
            / 'system_page.py').read_text(encoding='utf-8')


def test_la_page_Systeme_porte_la_carte_et_son_hote():
    src = _page()
    assert 'id="vx-strikes"' in src
    assert 'diag.option_strikes' in src


def test_l_ecran_distingue_INCONNU_de_ZERO():
    """Le point d'honnêteté. `pct==null` doit avoir sa propre branche."""
    src = _page()
    i = src.index('diag.option_strikes')
    bloc = src[i:i + 1800]
    assert 'pct==null' in bloc, (
        "sans cette branche, « aucune mesure » s'afficherait « 0 % evite »")


def test_l_ecran_dit_qu_aucun_strike_n_est_INVENTE():
    """La carte explique une économie ; sans cette phrase, un lecteur pourrait
    croire que le produit devine des contrats."""
    src = _page()
    i = src.index('diag.option_strikes')
    assert 'invent' in src[i:i + 2600]


def test_l_hote_est_ecrit_sous_la_forme_GARDEE():
    """D-027/D-031 : une écriture DOM nue sur une page qui change de vue
    reprend la main sur un élément supprimé."""
    src = _page()
    i = src.index('diag.option_strikes')
    bloc = src[i:i + 1800]
    assert "($('vx-strikes')||{})" in bloc
    assert "($('vx-strikes-badge')||{})" in bloc
