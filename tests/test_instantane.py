"""Vertex Test 1.0 — CINQ DEMANDES DU MÊME TITRE, UNE SEULE COLLECTE.

## Le défaut mesuré sur le SHA `73de92f5`, compte réel, TWS ouvert

`/api/ticker/<sym>` :

| situation | 1er appel | appels suivants |
|---|---:|---:|
| au calme | 3,30–3,64 s | 1,28–1,41 s |
| **sous charge** (5 titres neufs d'affilée) | **28–48 s** | — |
| démo (`DEMO=1 NO_IBKR=1`) | 2,02–2,91 s | 0,81–0,95 s |
| IBKR absent | 2,13–2,47 s | 0,80–0,86 s |
| sorties HTTPS coupées | 6,1 s | **6,1 s — le cache ne sert à rien** |

Et cinq demandes **simultanées du même titre neuf** :

```text
fil 2, 3, 4, 5 :  28,2 s        fil 1 : 136,9 s
```

Aucune coalescence. Cinq requêtes identiques refont chacune tout le travail, et
l'une a mis **deux minutes dix-sept**.

Deux défauts d'honnêteté au passage : sous coupure réseau la route rend
**HTTP 200** avec `pack.error = "IndexError: single positional indexer is
out-of-bounds"` — une exception Python brute servie comme état — et aucun champ
`LIVE / DELAYED / STALE / DEMO / OFFLINE / MISSING` n'existait dans la charge.

## Ce que ces bancs gardent

Le magasin sert vite **sans jamais mentir** : ce qui est rassis le dit, ce qui
manque n'est pas comblé, et un échec n'efface pas le dernier état connu.
"""
from __future__ import annotations

import threading
import time

import pytest

from vertex.app import snapshot as S


@pytest.fixture()
def magasin():
    m = S.Magasin('banc')
    yield m
    m.oublier_tout()


def _attendre_calme(m, secondes=10.0):
    """La reconstruction est asynchrone : l'attendre EXPLICITEMENT vaut mieux
    qu'espérer que l'ordonnanceur l'ait faite avant l'assertion suivante."""
    fin = time.monotonic() + secondes
    while time.monotonic() < fin:
        if not any(e.chantier for e in m._entrees.values()):
            return True
        time.sleep(0.02)
    return False


#  ═══════════  1. LA coalescence — le défaut à 136,9 s  ═══════════════════════

def test_DIX_demandes_simultanees_du_meme_titre_ne_collectent_QU_UNE_fois(magasin):
    """Le cœur du lot. Mesuré avant : cinq demandes identiques, cinq collectes,
    dont une à 136,9 s."""
    appels = []
    depart = threading.Barrier(10)

    def _lent():
        appels.append(1)
        time.sleep(0.3)
        return {'v': 1}

    def _visiteur():
        depart.wait(timeout=15)
        magasin.servir('AAPL', _lent, fraicheur_s=60)

    fils = [threading.Thread(target=_visiteur) for _ in range(10)]
    for f in fils:
        f.start()
    for f in fils:
        f.join(timeout=30)
    assert len(appels) == 1, '%d collectes au lieu d une' % len(appels)


def test_les_retardataires_recoivent_bien_la_valeur(magasin):
    """Contre-épreuve : coalescer ne doit pas rendre `None` aux attendants."""
    recus = []

    def _c():
        time.sleep(0.1)
        return {'v': 42}

    fils = [threading.Thread(
        target=lambda: recus.append(magasin.servir('X', _c, fraicheur_s=60)[0]))
        for _ in range(6)]
    for f in fils:
        f.start()
    for f in fils:
        f.join(timeout=30)
    assert len(recus) == 6
    assert all(r == {'v': 42} for r in recus)


def test_deux_titres_DIFFERENTS_ne_se_bloquent_pas(magasin):
    """Un verrou global sérialiserait tout le produit derrière le titre le plus
    lent — exactement la file partagée qui produisait les 28–48 s."""
    ordre = []

    def _lent():
        time.sleep(0.4)
        ordre.append('lent')
        return {'v': 'lent'}

    def _vite():
        ordre.append('vite')
        return {'v': 'vite'}

    t = threading.Thread(target=lambda: magasin.servir('LENT', _lent, fraicheur_s=60))
    t.start()
    time.sleep(0.05)
    magasin.servir('VITE', _vite, fraicheur_s=60)
    assert ordre[0] == 'vite', "le titre rapide a attendu le lent"
    t.join(timeout=10)


#  ═══════════  2. rassis servi TOUT DE SUITE, et qui le DIT  ══════════════════

def test_une_valeur_RASSIE_est_servie_sans_attendre(magasin):
    appels = []

    def _c():
        appels.append(1)
        if len(appels) > 1:
            time.sleep(5)          # la reconstruction est longue
        return {'n': len(appels)}

    magasin.servir('A', _c, fraicheur_s=0.01)
    time.sleep(0.05)
    t0 = time.monotonic()
    valeur, meta = magasin.servir('A', _c, fraicheur_s=0.01)
    duree = time.monotonic() - t0
    assert duree < 1.0, 'le visiteur a attendu %.2f s' % duree
    assert valeur == {'n': 1}, "c est bien l ancienne valeur qui est servie"
    assert meta.etat == S.STALE
    assert meta.rafraichissement_en_cours is True
    assert meta.age_s is not None and meta.age_s > 0


def test_une_valeur_FRAICHE_n_est_PAS_marquee_rassise(magasin):
    """Contre-épreuve. Une mention présente partout ne distingue plus rien."""
    magasin.servir('A', lambda: {'v': 1}, fraicheur_s=60)
    _, meta = magasin.servir('A', lambda: {'v': 2}, fraicheur_s=60)
    assert meta.etat == S.LIVE
    assert meta.rafraichissement_en_cours is False


def test_le_tout_PREMIER_appelant_attend_et_c_est_voulu(magasin):
    """Sans valeur antérieure, il n'y a rien d'honnête à servir. Rendre une
    coquille vide serait l'invention que le produit s'interdit."""
    valeur, meta = magasin.servir('NEUF', lambda: {'v': 1}, fraicheur_s=60)
    assert valeur == {'v': 1}
    assert meta.etat == S.LIVE


#  ═══════════  3. ce qui manque n'est jamais comblé  ══════════════════════════

def test_une_construction_qui_ECHOUE_ne_rend_ni_zero_ni_coquille(magasin):
    def _casse():
        raise RuntimeError('source injoignable')

    valeur, meta = magasin.servir('KO', _casse, fraicheur_s=60)
    assert valeur is None, 'aucune valeur inventee'
    assert meta.etat == S.OFFLINE
    assert 'source injoignable' in (meta.erreur or '')


def test_un_constructeur_qui_rend_None_donne_MISSING_pas_OFFLINE(magasin):
    """Ne pas trouver n'est pas être en panne : deux causes, deux gestes."""
    valeur, meta = magasin.servir('VIDE', lambda: None, fraicheur_s=60)
    assert valeur is None
    assert meta.etat == S.MISSING
    assert meta.erreur is None


def test_un_ECHEC_n_efface_JAMAIS_le_dernier_instantane(magasin):
    """Servir daté vaut infiniment mieux qu'une section vide."""
    magasin.servir('A', lambda: {'v': 'bon'}, fraicheur_s=0.01)
    time.sleep(0.05)

    def _casse():
        raise RuntimeError('nope')

    valeur, meta = magasin.servir('A', _casse, fraicheur_s=0.01)
    _attendre_calme(magasin)
    assert valeur == {'v': 'bon'}, 'le dernier instantane connu a ete perdu'
    assert meta.etat == S.STALE


def test_un_echec_REPETE_ne_lance_pas_un_fil_par_visiteur(magasin):
    """Sans repos, une panne de fournisseur devient une panne de serveur."""
    magasin.servir('A', lambda: {'v': 1}, fraicheur_s=0.01)
    time.sleep(0.05)
    essais = []

    def _casse():
        essais.append(1)
        raise RuntimeError('nope')

    for _ in range(20):
        magasin.servir('A', _casse, fraicheur_s=0.01)
        time.sleep(0.01)
    _attendre_calme(magasin)
    assert len(essais) <= 2, '%d relances pour 20 visiteurs' % len(essais)
    assert S.REPOS_APRES_ECHEC_S > 0


#  ═══════════  4. la provenance voyage avec la valeur  ════════════════════════

def test_le_constructeur_peut_declarer_source_instant_et_qualite(magasin):
    _, meta = magasin.servir(
        'A', lambda: ({'v': 1}, {'source': 'IBKR', 'observe_a': 1000.0,
                                 'qualite': 'REELLE'}),
        fraicheur_s=60)
    assert meta.source == 'IBKR'
    assert meta.observe_a == 1000.0
    assert meta.qualite == 'REELLE'
    assert meta.recu_a is not None, "l instant de RECEPTION est distinct"


def test_un_constructeur_peut_imposer_son_etat_DEMO_ou_DELAYED(magasin):
    """Une donnée de démo reste étiquetée démo même fraîche : l'état décrit la
    NATURE de la donnée, pas la patience du magasin."""
    _, meta = magasin.servir('A', lambda: ({'v': 1}, {'etat': S.DEMO}),
                             fraicheur_s=60)
    assert meta.etat == S.DEMO


def test_tous_les_etats_du_standard_qualite_existent():
    assert set(S.ETATS) == {'LIVE', 'DELAYED', 'STALE', 'DEMO', 'OFFLINE',
                            'MISSING'}


#  ═══════════  5. le magasin se mesure, sans se flatter  ══════════════════════

def test_sans_aucune_demande_le_hit_ratio_est_INCONNU_pas_cent(magasin):
    """Rendre 100 % ferait passer « je n'ai rien mesuré » pour « parfait » —
    même faute que D-054/D-065."""
    assert magasin.statistiques()['hit_ratio_pct'] is None


def test_les_compteurs_distinguent_frais_rassis_absent_et_coalesce(magasin):
    magasin.servir('A', lambda: {'v': 1}, fraicheur_s=60)   # absent -> construit
    magasin.servir('A', lambda: {'v': 1}, fraicheur_s=60)   # frais
    s = magasin.statistiques()
    assert s['absents'] == 1 and s['frais'] == 1
    assert s['constructions'] == 1
    assert s['hit_ratio_pct'] == 50.0


def test_les_durees_de_construction_donnent_p50_et_p95(magasin):
    """Sans p95, aucun budget n'est vérifiable — et le programme en exige un."""
    for i in range(5):
        magasin.servir('K%d' % i, lambda: {'v': 1}, fraicheur_s=60)
    s = magasin.statistiques()
    assert s['construction_p50_s'] is not None
    assert s['construction_p95_s'] is not None


def test_la_liste_des_durees_est_BORNEE(magasin):
    """Un produit qui tourne des semaines ne doit pas garder une mesure par
    requête — la fuite lente que personne ne voit avant qu'elle compte."""
    for i in range(400):
        magasin.servir('K%d' % i, lambda: {'v': 1}, fraicheur_s=60)
    assert len(magasin.metriques['duree_construction_s']) <= 200


#  ═══════════  6. une route ne meurt jamais à cause du magasin  ═══════════════

def test_servir_ne_LEVE_jamais(magasin):
    """Une route qui meurt rend 500 ; un magasin honnête rend OFFLINE."""
    for casse in (lambda: (_ for _ in ()).throw(ValueError('x')),
                  lambda: (_ for _ in ()).throw(KeyError('y'))):
        valeur, meta = magasin.servir('K', casse, fraicheur_s=60)
        assert valeur is None and meta.etat == S.OFFLINE
        magasin.oublier_tout()


#  ═══════════  7. le JETON — périmer par la dépendance, pas par l'horloge  ════

def test_un_JETON_qui_change_rend_la_valeur_rassie_pas_absente(magasin):
    """Certaines valeurs ne périment pas avec le temps mais avec leur entrée :
    le graphe de connaissance est déterministe pour un scan donné.

    Changer de CLÉ à chaque scan aurait fait d'un graphe parfaitement
    utilisable une entrée « absente », donc une attente de 15 s. Le jeton le
    rend RASSIS : servi tout de suite, marqué, reconstruit en fond."""
    magasin.servir('g', lambda: {'v': 1}, fraicheur_s=9999, jeton='scan-1')
    valeur, meta = magasin.servir('g', lambda: (time.sleep(5), {'v': 2})[1],
                                  fraicheur_s=9999, jeton='scan-2')
    assert valeur == {'v': 1}, "l ancienne valeur doit etre servie"
    assert meta.etat == S.STALE
    assert meta.rafraichissement_en_cours is True


def test_un_JETON_inchange_laisse_la_valeur_FRAICHE(magasin):
    """Contre-épreuve : sinon tout serait rassis en permanence et la mention
    ne distinguerait plus rien."""
    magasin.servir('g', lambda: {'v': 1}, fraicheur_s=9999, jeton='scan-1')
    _, meta = magasin.servir('g', lambda: {'v': 2}, fraicheur_s=9999,
                             jeton='scan-1')
    assert meta.etat == S.LIVE
    assert meta.rafraichissement_en_cours is False


def test_le_jeton_finit_par_etre_ADOPTE_apres_reconstruction(magasin):
    """Sans cela, la valeur resterait rassie pour toujours et un fil de fond
    repartirait à chaque visite — une reconstruction perpétuelle."""
    magasin.servir('g', lambda: {'v': 1}, fraicheur_s=9999, jeton='scan-1')
    magasin.servir('g', lambda: {'v': 2}, fraicheur_s=9999, jeton='scan-2')
    _attendre_calme(magasin)
    valeur, meta = magasin.servir('g', lambda: {'v': 3}, fraicheur_s=9999,
                                  jeton='scan-2')
    assert valeur == {'v': 2}
    assert meta.etat == S.LIVE, "le jeton neuf doit avoir ete adopte"


def test_sans_jeton_le_comportement_est_INCHANGE(magasin):
    """Aucune régression pour les appelants qui n'en passent pas — la fiche
    d'un titre, par exemple, périme bien par l'âge."""
    magasin.servir('a', lambda: {'v': 1}, fraicheur_s=9999)
    _, meta = magasin.servir('a', lambda: {'v': 2}, fraicheur_s=9999)
    assert meta.etat == S.LIVE
