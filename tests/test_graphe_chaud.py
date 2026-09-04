"""Vertex Test 1.0 — SERVIR UN GRAPHE DATÉ VAUT MIEUX QUE FAIRE ATTENDRE 15 s.

Mesuré le 24 août 2026 sur le produit live, TWS ouvert, par l'instrument
corrigé au lot précédent :

| appel | durée |
|---|---:|
| premier après un scan | **15,1 s** |
| second | **0,007 s** |

`/api/skyler/graph` est lu par la page **Portefeuille**. Le scan retourne
régulièrement — `last_scan` est passé de 16:34:36 à 17:08:45 pendant la
mesure — et sa clé de fraîcheur inclut `scan_ts` : **à chaque cycle, un
visiteur repayait 15 s.**

## Deux défauts, pas un

1. **Le verrou du mémo était relâché AVANT la construction.** Deux visiteurs
   simultanés fabriquaient donc le même graphe, chacun pour 15 s.
2. **Attendre n'était pas nécessaire.** Le graphe du scan précédent est une
   réponse utilisable ; ce qui manquait, c'était de dire qu'elle date.

## Ce que ce lot ne fait PAS

Il ne sert jamais un graphe daté **en silence**. La charge porte `fraicheur`,
`age_s` et `reconstruction_en_cours`, la route par symbole les recopie, et le
pied de carte affiche « SCAN PRÉCÉDENT ». Le pied passait `Date.now()` — il
annonçait « mis à jour maintenant » pour un graphe pouvant dater de plusieurs
scans : un âge faux est pire qu'un âge absent.

Le **tout premier** visiteur attend toujours : il n'y a rien d'honnête à
servir, et fabriquer un graphe vide serait l'invention que le produit
s'interdit.
"""
from __future__ import annotations

import threading
import time

import pytest

from vertex.app.routes import analysis_api as A


@pytest.fixture(autouse=True)
def _memo_neuf():
    """Chaque banc part d'un magasin vide — sinon le premier test réchauffe les
    suivants et ils mesureraient un cas qu'ils croient tester.

    Depuis la migration vers `vertex/app/snapshot.py`, le mécanisme est celui
    du magasin PARTAGÉ : le graphe n'a plus sa propre implantation
    stale-while-revalidate. Les intentions gardées ci-dessous sont inchangées."""
    A._KG_MAGASIN.oublier_tout()
    yield
    A._KG_MAGASIN.oublier_tout()


def _chantier_en_cours():
    return any(e.chantier for e in A._KG_MAGASIN._entrees.values())


def _attendre_chantier(secondes=10.0):
    fin = time.monotonic() + secondes
    while _chantier_en_cours() and time.monotonic() < fin:
        time.sleep(0.02)


def _faux_graphe(marque='a'):
    return {'as_of': marque, 'demo': False, 'engine_version': '0.1.0',
            'edges': [], 'nodes': [], 'hidden_dependencies': [],
            'research_questions': [], 'marque': marque}


#  ═══════════  1. une seule construction, meme a N visiteurs  ═════════════════

@pytest.fixture(autouse=True)
def _magasin_vide():
    #  `monkeypatch` defait le remplacement de `_kg_construire`, mais le faux
    #  graphe qu'il a produit RESTE dans le magasin de snapshots. Les bancs
    #  suivants le recevaient et tombaient sur `KeyError: 'as_of'` — selon le
    #  seul ordre alphabetique des noms de fichiers.
    from vertex.app.routes import analysis_api as _A
    _A._KG_MAGASIN.oublier_tout()
    yield
    _A._KG_MAGASIN.oublier_tout()


def test_DIX_visiteurs_simultanes_ne_construisent_QU_UNE_fois(monkeypatch):
    """Le verrou était relâché avant la construction : dix visiteurs
    fabriquaient dix fois le même graphe, à 15 s pièce."""
    appels = []
    depart = threading.Barrier(10)

    def _lent():
        appels.append(1)
        time.sleep(0.25)
        return _faux_graphe()

    monkeypatch.setattr(A, '_kg_construire', _lent)
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))

    def _visiteur():
        depart.wait(timeout=10)
        A._kg_build()

    fils = [threading.Thread(target=_visiteur) for _ in range(10)]
    for f in fils:
        f.start()
    for f in fils:
        f.join(timeout=20)
    assert len(appels) == 1, "%d constructions au lieu d'une" % len(appels)


def test_les_retardataires_recoivent_bien_le_graphe(monkeypatch):
    """Contre-épreuve : sérialiser ne doit pas rendre `None` aux attendants."""
    monkeypatch.setattr(A, '_kg_construire', lambda: _faux_graphe('x'))
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))
    recus = []
    fils = [threading.Thread(target=lambda: recus.append(A._kg_build()))
            for _ in range(5)]
    for f in fils:
        f.start()
    for f in fils:
        f.join(timeout=20)
    assert len(recus) == 5
    assert all(r['marque'] == 'x' for r in recus)


#  ═══════════  2. le premier visiteur attend, et c'est VOULU  ═════════════════

def test_le_TOUT_premier_visiteur_attend_et_recoit_du_LIVE(monkeypatch):
    """Sans graphe antérieur, il n'y a rien d'honnête à servir. Rendre une
    coquille vide serait l'invention que le produit s'interdit."""
    monkeypatch.setattr(A, '_kg_construire', lambda: _faux_graphe('premier'))
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))
    g = A._kg_build()
    assert g['marque'] == 'premier'
    assert g['fraicheur'] == A.FRAICHEUR_LIVE
    assert g['reconstruction_en_cours'] is False


#  ═══════════  3. un graphe date est servi VITE, et DIT qu'il date  ═══════════

def test_apres_un_scan_le_visiteur_est_servi_SANS_attendre(monkeypatch):
    """Le cœur du lot : 15,1 s → immédiat."""
    monkeypatch.setattr(A, '_kg_construire', lambda: _faux_graphe('ancien'))
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))
    A._kg_build()                                   # premier visiteur, il paie

    def _tres_lent():
        time.sleep(5)
        return _faux_graphe('neuf')

    monkeypatch.setattr(A, '_kg_construire', _tres_lent)
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-2',))   # le scan a tourné
    t0 = time.monotonic()
    g = A._kg_build()
    duree = time.monotonic() - t0
    assert duree < 1.0, "le visiteur a attendu %.1f s" % duree
    assert g['marque'] == 'ancien', "c'est bien l'ancien qui est servi"


def test_et_il_DIT_que_le_graphe_date(monkeypatch):
    """Servir du périmé en silence serait pire que la lenteur retirée."""
    monkeypatch.setattr(A, '_kg_construire', lambda: _faux_graphe('ancien'))
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))
    A._kg_build()
    monkeypatch.setattr(A, '_kg_construire',
                        lambda: (time.sleep(5), _faux_graphe('neuf'))[1])
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-2',))
    g = A._kg_build()
    assert g['fraicheur'] == A.FRAICHEUR_STALE
    assert g['age_s'] is not None and g['age_s'] >= 0
    assert g['reconstruction_en_cours'] is True


def test_un_graphe_A_JOUR_n_est_PAS_marque_date(monkeypatch):
    """Contre-épreuve. Une mention présente partout ne distingue plus rien."""
    monkeypatch.setattr(A, '_kg_construire', lambda: _faux_graphe('a'))
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))
    A._kg_build()
    g = A._kg_build()
    assert g['fraicheur'] == A.FRAICHEUR_LIVE
    assert g['reconstruction_en_cours'] is False


def test_la_fraicheur_n_est_PAS_ecrite_dans_le_memo(monkeypatch):
    """Elle est ajoutée sur une copie. La figer dans la valeur mémoïsée
    donnerait un âge qui ne bouge plus — un chiffre daté faux, précisément le
    défaut que ce lot corrige côté écran."""
    monkeypatch.setattr(A, '_kg_construire', lambda: _faux_graphe('a'))
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))
    A._kg_build()
    stocke = list(A._KG_MAGASIN._entrees.values())[0].valeur
    assert 'fraicheur' not in stocke
    assert 'age_s' not in stocke


#  ═══════════  4. un echec ne detruit rien et ne fait pas tempete  ════════════

def test_une_reconstruction_qui_ECHOUE_n_efface_pas_le_dernier_graphe(monkeypatch):
    """Servir un graphe daté reste infiniment plus utile qu'une section vide."""
    monkeypatch.setattr(A, '_kg_construire', lambda: _faux_graphe('bon'))
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))
    A._kg_build()

    def _casse():
        raise RuntimeError('source indisponible')

    monkeypatch.setattr(A, '_kg_construire', _casse)
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-2',))
    A._kg_build()
    _attendre_chantier()
    g = A._kg_build()
    assert g['marque'] == 'bon', "le dernier graphe connu a ete perdu"
    assert g['fraicheur'] == A.FRAICHEUR_STALE
    assert 'source indisponible' in (g.get('reconstruction_erreur') or '')


def test_un_echec_repete_ne_lance_PAS_un_fil_par_visiteur(monkeypatch):
    """Sans repos, un graphe qui ne se construit plus fabriquerait un fil à
    chaque requête — une panne de source deviendrait une panne de serveur."""
    monkeypatch.setattr(A, '_kg_construire', lambda: _faux_graphe('bon'))
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-1',))
    A._kg_build()
    essais = []

    def _casse():
        essais.append(1)
        raise RuntimeError('nope')

    monkeypatch.setattr(A, '_kg_construire', _casse)
    monkeypatch.setattr(A, '_kg_clef', lambda: ('scan-2',))
    for _ in range(20):
        A._kg_build()
        time.sleep(0.02)
    _attendre_chantier()
    assert len(essais) <= 2, "%d relances pour 20 visiteurs" % len(essais)
    from vertex.app import snapshot as _S
    assert _S.REPOS_APRES_ECHEC_S > 0


#  ═══════════  5. la route PAR SYMBOLE ne perd pas la fraicheur  ══════════════

def test_la_route_par_symbole_RECOPIE_la_fraicheur():
    """Elle assemble sa charge champ par champ : les oublier ferait servir un
    graphe daté présenté comme courant, sur une route entière."""
    src = (A.__file__ or '')
    import pathlib
    texte = pathlib.Path(src).read_text(encoding='utf-8')
    bloc = texte[texte.index('def api_skyler_graph_sym'):]
    bloc = bloc[:bloc.index('@bp.route', 10)]
    for champ in ("'fraicheur'", "'age_s'", "'reconstruction_en_cours'"):
        assert champ in bloc, "champ %s absent de la route par symbole" % champ


#  ═══════════  6. l'ecran dit l'age REEL, pas « maintenant »  ═════════════════

def test_le_pied_de_carte_n_annonce_plus_maintenant():
    """`Date.now()` promettait « mis a jour maintenant » pour une charge
    pouvant dater de plusieurs minutes. Un age faux est pire qu'un age absent :
    il empeche de se mefier.

    L'ancre d'origine — le bloc `renderHiddenDeps` — n'existe plus sous cette
    forme dans Black Glass ; l'intention, elle, est intacte et se verifie mieux
    a l'echelle de la page : AUCUN pied de carte ne se date de l'instant du
    rendu. Ils lisent `window.__pfTs`, pose une seule fois quand les cotations
    ARRIVENT.
    """
    import pathlib
    page = (pathlib.Path(A.__file__).resolve().parents[3]
            / 'vertex' / 'ui' / 'pages' / 'portfolio_page.py')
    src = page.read_text(encoding='utf-8')
    assert 'window.__pfTs=' in src, (
        "l'instant d'arrivee des cotations n'est plus retenu")
    fautifs = [l.strip()[:90] for l in src.splitlines()
               if 'updateIndicator(Date.now()' in l or 'timestamp:Date.now()' in l]
    assert fautifs == [], (
        'un pied de carte se date de l instant du RENDU, pas de celui de la '
        'donnee : %r' % fautifs)


def test_le_banc_verrait_le_defaut_s_il_revenait():
    """Contre-epreuve : sans elle, « aucun fautif » pourrait vouloir dire
    « je n ai rien lu »."""
    faux = ["    <div>${VX.updateIndicator(Date.now(),'x','live')}</div>"]
    fautifs = [l for l in faux if 'updateIndicator(Date.now()' in l]
    assert len(fautifs) == 1
