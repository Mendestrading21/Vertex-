"""Vertex Test 1.0 — UNE PANNE N'EST PAS UNE LENTEUR.

Six outils de mesure interrogent le produit par HTTP. Les six avaient la même
forme : un délai **plat**, un `except Exception`, et rien d'autre.

## Le défaut, mesuré le 24 août 2026 (machine live, TWS ouvert)

`mesurer_surfaces_vides` a annoncé, sur un produit **inchangé** :

| passage | état du serveur | « surfaces en erreur » |
|---|---|---:|
| 1 | chaud, scan de 630 s | **4** |
| 2 | redémarré, à froid | **1** |
| 3, 4, 5 | chaud | **0** |
| 6 | scan venant de finir | **5** |

Jamais les mêmes routes. Interrogées une à une avec un délai généreux, toutes
répondaient **200 avec leurs données** en 2,2 à 5,2 s. L'instrument
n'annonçait pas des pannes du produit : il annonçait sa propre patience.

C'est le pire défaut possible pour un instrument d'audit. Un outil qui crie
quatre pannes imaginaires apprend à son lecteur à ne plus le lire — et le jour
où la cinquième est réelle, elle passe avec les autres.

## Le second fantôme

`/api/cockpit` et `/api/comite` sortaient « VIDE À EXAMINER » sur un serveur
fraîchement redémarré. Cause mesurée : `last_scan: null` — le scan n'avait pas
encore tourné. Les deux se sont remplies **dès le scan terminé**. Le produit
annonçait lui-même son état sur `/healthz` ; l'instrument ne le lui demandait
jamais, et envoyait l'auditeur chercher un défaut inexistant.

## Ce que ces bancs gardent

Que le défaut ne revienne pas *dans un septième outil*. Corriger le fichier où
le symptôme apparaît laisse la classe entière en place — D-027, déjà payé deux
fois.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from tools.mesures._sonde_http import (BUDGET_INTERACTIF, PLAFOND_DEFAUT,
                                          Reponse, appeler)

OUTILS = Path(__file__).resolve().parents[1] / "tools" / "mesures"
SONDE = OUTILS / "_sonde_http.py"

#: `urlopen`, `requests.get`, `httpx` — trois orthographes du même appel. Un
#: gardien qui n'en connaît qu'une certifie un fichier qu'il n'a pas lu (D-031).
_APPEL_NU = re.compile(
    r"urllib\.request\.urlopen|requests\.(get|post)\s*\(|httpx\.(get|post)\s*\(")


#  ═══════════  1. une expiration n'est pas une panne  ═════════════════════════

def _rep(**kw):
    base = {'chemin': '/api/x', 'statut': 200, 'duree_s': 0.1}
    base.update(kw)
    return Reponse(**base)


def test_une_EXPIRATION_a_son_propre_etat():
    """« Je n'ai pas attendu assez longtemps » n'est pas « c'est cassé »."""
    assert _rep(statut=0, expiree=True).etat == 'EXPIREE'


def test_l_expiration_PRIME_sur_l_erreur():
    """L'ordre compte : `statut == 0` est vrai dans les deux cas. Tester
    l'erreur d'abord ramènerait exactement le défaut qu'on corrige."""
    assert _rep(statut=0, expiree=True, erreur='expiree apres 60 s').etat == 'EXPIREE'


def test_une_VRAIE_panne_reste_une_erreur():
    """Contre-épreuve. Séparer l'expiration ne doit pas désarmer la détection
    des pannes — sinon l'instrument ne crie plus jamais."""
    assert _rep(statut=500).etat == 'ERREUR'
    assert _rep(statut=404).etat == 'ERREUR'
    assert _rep(statut=0, erreur='connexion refusee').etat == 'ERREUR'


def test_un_200_LENT_reste_un_200():
    """La donnée est arrivée. La compter comme une panne fabrique un défaut."""
    r = _rep(duree_s=BUDGET_INTERACTIF + 5)
    assert r.etat == 'LENTE'
    assert r.a_repondu is True, "une lenteur ne retire pas la reponse"


def test_un_200_RAPIDE_n_est_pas_signale():
    assert _rep(duree_s=0.2).etat == 'OK'


def test_le_plafond_couvre_les_routes_LENTES_documentees():
    """D-024 documente `/api/positions/state` à 18–31 s. Un plafond de 8 s la
    déclarait en panne à chaque exécution — le défaut, littéralement."""
    assert PLAFOND_DEFAUT > 31.0


#  ═══════════  2. toute réponse porte sa DURÉE  ═══════════════════════════════

def test_chaque_appel_rapporte_une_duree():
    """Sans durée, aucun avant/après n'est possible — et le programme en exige
    un à chaque lot. Aucun des six outils n'en mesurait une."""
    r = appeler('http://127.0.0.1:1', '/inexistant', plafond=0.5)
    assert r.duree_s >= 0.0
    assert r.chemin == '/inexistant'


def test_un_hote_injoignable_rend_une_reponse_et_ne_LEVE_pas():
    """Un instrument qui s'interrompt sur la première surface muette ne mesure
    rien de celles d'après."""
    r = appeler('http://127.0.0.1:1', '/x', plafond=0.5)
    assert isinstance(r, Reponse)
    assert r.statut == 0 and r.erreur


#  ═══════════  3. l'état de CHAUFFE se demande au produit  ════════════════════

def test_ne_pas_savoir_n_est_pas_savoir_que_NON():
    """Produit injoignable : `scan_fait` vaut `None`, jamais `False`. Rendre
    `False` ferait passer une ignorance pour une mesure."""
    from tools.mesures._sonde_http import sonder_pret
    p = sonder_pret('http://127.0.0.1:1', plafond=0.5)
    assert p['joignable'] is False
    assert p['scan_fait'] is None


#  ═══════════  4. le classement des surfaces  ═════════════════════════════════

def test_une_surface_vide_AVANT_le_premier_scan_n_est_pas_suspecte():
    """Le fantôme mesuré : `/api/cockpit` et `/api/comite` vides avec
    `last_scan: null`, pleines dès le scan terminé."""
    from tools.mesures.mesurer_surfaces_vides import classer
    assert classer('/api/cockpit', 200, {}, scan_fait=False) == 'PAS_ENCORE_PRET'


def test_mais_une_surface_vide_sur_un_produit_CHAUD_reste_suspecte():
    """Contre-épreuve. Un gardien qui excuse tout ne garde plus rien : c'est
    précisément là qu'ont vécu les trois défauts d'écran creux."""
    from tools.mesures.mesurer_surfaces_vides import classer
    assert classer('/api/market/summary', 200, {}, scan_fait=True) == 'VIDE_A_EXAMINER'


def test_une_expiration_ne_devient_pas_une_surface_EN_ERREUR():
    from tools.mesures.mesurer_surfaces_vides import classer
    assert classer('/api/x', 0, None, expiree=True) == 'EXPIREE'


#  ═══════════  5. la classe entière, pas le fichier du symptôme  ══════════════

def test_AUCUN_outil_n_appelle_le_produit_hors_de_la_sonde():
    """D-027 : corriger le site où le symptôme apparaît laisse la classe en
    place. Le défaut vivait dans SIX fichiers ; le septième s'écrira avec un
    délai plat si rien ne l'en empêche."""
    coupables = []
    for f in sorted(OUTILS.glob('*.py')):
        if f.name == SONDE.name:
            continue
        for n, ligne in enumerate(f.read_text(encoding='utf-8').splitlines(), 1):
            if _APPEL_NU.search(ligne):
                coupables.append('%s:%d  %s' % (f.name, n, ligne.strip()[:70]))
    assert coupables == [], (
        "appel HTTP nu hors de la sonde partagee — une expiration y "
        "redeviendra indiscernable d'une panne :\n" + "\n".join(coupables))


def test_le_gardien_VOIT_un_appel_nu_qu_on_lui_montre(tmp_path):
    """Contre-épreuve n°1 : sans elle, un gardien qui ne trouve jamais rien
    passerait pour un gardien qui garde."""
    for forme in ("with urllib.request.urlopen(u, timeout=8) as r:",
                  "r = requests.get(url, timeout=5)",
                  "r = httpx.get(url)"):
        assert _APPEL_NU.search(forme), forme


def test_le_gardien_NE_signale_PAS_la_forme_partagee():
    """Contre-épreuve n°2 : un gardien qui refuse aussi la correction est
    desactivé au premier commit pressé."""
    assert not _APPEL_NU.search("rep = appeler(base, chemin, plafond=60)")
    assert not _APPEL_NU.search("from tools.mesures._sonde_http import appeler")


def test_la_sonde_elle_meme_reste_le_SEUL_endroit_qui_ouvre_une_socket():
    src = SONDE.read_text(encoding='utf-8')
    assert len(_APPEL_NU.findall(src)) == 1, (
        "la sonde doit ouvrir UNE socket, en un seul endroit")


#  ═══════════  6. le seuil de lenteur est une convention, et le dit  ══════════

def test_le_seuil_de_lenteur_est_DECLARE_comme_convention():
    """On a cherché le budget réel du client : il n'y en a aucun — pas un
    `AbortController` dans toute l'UI. Présenter 10 s comme « le moment où le
    navigateur renonce » serait inventer un fait (D-039 l'interdit pour les
    dates ; la règle ne change pas parce qu'il s'agit d'une durée)."""
    src = SONDE.read_text(encoding='utf-8')
    assert 'convention' in src.lower()
    assert 'AbortController' in src, (
        "le motif du choix doit rester ECRIT la ou le seuil est defini")




#: Un abandon PAR DELAI : un minuteur qui declenche `.abort()`, ou le sucre
#: `AbortSignal.timeout(...)`. C'est CELA, un budget de requete — pas la
#: simple presence d'un `AbortController`.
_BUDGET_CLIENT = re.compile(
    r"setTimeout\([^;]{0,120}\.abort\(\)|AbortSignal\.timeout\s*\(")


def test_aucun_MINUTEUR_n_abandonne_une_requete_cote_client():
    """Le jour où l'UI se donne un budget de requête, ce banc tombe — et le
    seuil ci-dessus cesse d'être une convention pour devenir mesurable.

    **Ce banc a déjà eu tort.** Sa première version cherchait
    `AbortController` dans `vertex/ui/**/*.py` seulement, et concluait qu'il
    n'y en avait aucun. Il y en a un, dans
    `vertex/static/vertex/js/vx-core.js` — le JavaScript servi, que le
    balayage ne regardait pas. D-031, une fois de plus : un gardien dont le
    champ est trop étroit certifie ce qu'il n'a pas lu.

    Ce qui compte n'était d'ailleurs pas la PRÉSENCE d'un `AbortController` —
    celui-ci sert l'annulation demandée par l'appelant — mais qu'aucun
    **minuteur** ne le déclenche.
    """
    racine = Path(__file__).resolve().parents[1] / "vertex"
    fichiers = list(racine.rglob('*.js')) + list(racine.rglob('*.py'))
    assert len(fichiers) > 100, "corpus suspect : %d fichiers" % len(fichiers)
    minuteurs = []
    for f in fichiers:
        try:
            src = f.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        if _BUDGET_CLIENT.search(src):
            minuteurs.append(str(f.relative_to(racine)))
    if minuteurs:
        pytest.fail(
            "l'UI a maintenant un budget de requete (%s) : remplacer la "
            "convention BUDGET_INTERACTIF par cette mesure reelle"
            % ', '.join(minuteurs))


def test_le_gardien_du_budget_VOIT_un_minuteur_qu_on_lui_montre():
    """Contre-épreuve, absente de la première version — c'est précisément son
    absence qui a laissé passer l'erreur."""
    for forme in ("const t = setTimeout(() => ctl.abort(), 8000);",
                  "signal: AbortSignal.timeout(5000)"):
        assert _BUDGET_CLIENT.search(forme), forme


def test_le_gardien_du_budget_NE_signale_PAS_une_annulation_par_l_appelant():
    """L'`AbortController` de `vx-core.js` propage l'annulation demandée par
    l'appelant. Le signaler ferait tomber le banc sur un produit sain."""
    forme = ("const ctl = new AbortController();\n"
             "if (signal) signal.addEventListener('abort', () => ctl.abort());")
    assert not _BUDGET_CLIENT.search(forme)


def test_le_corpus_du_gardien_couvre_le_JAVASCRIPT_SERVI():
    """La borne exacte qui manquait. Sans ce banc, le champ pourrait se
    rétrécir à nouveau sans que rien ne le dise."""
    racine = Path(__file__).resolve().parents[1] / "vertex"
    js = list(racine.rglob('*.js'))
    assert any('vx-core.js' in str(f) for f in js), (
        "le balayage ne voit pas vx-core.js — c'est la que vit "
        "l'AbortController que la premiere version a manque")
