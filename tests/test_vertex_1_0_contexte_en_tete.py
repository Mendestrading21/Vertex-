"""Vertex 1.0 — LES TUILES D'EN-TÊTE ÉTAIENT LES DERNIÈRES SERVIES, DONC LES PREMIÈRES SACRIFIÉES.

## Ce qui a été vu, le 26 août 2026, sur le desk réel

Le Dashboard affichait **`n/d` partout** sur sa première rangée : Dow Jones,
S&P 500, Nasdaq, Russell 2000, VIX, SMI, USD/CHF, or, pétrole, argent, BTC,
ETH. Et en dessous : « S&P 500 indisponible », « VIX indisponible »,
« participation indisponible ».

Pendant ce temps `/healthz` répondait :

```text
"scanned": 513,  "universe": 518,  "scan_error": null,  "status": "ok"
```

**Le scan se déclarait sain.** Aucune erreur, 513 titres traités.

## La cause

`_scan_once` composait sa file ainsi :

```python
_syms = syms_scan + [BENCH, '^VIX', '^GSPC', ...] + _COMMO + _MACRO_TK
```

Les **513 actions d'abord**, le contexte de marché **à la fin**. Or
`_download_universe` abandonne tout le reste après **trois lots vides
d'affilée** — le backoff anti-429, parfaitement légitime en soi.

Quand Yahoo limite le débit en fin de scan, ce sont donc **exactement** les
seize symboles de l'en-tête qui sont sacrifiés. Et l'abandon était **muet** :
`break`, sans un mot.

Vérifié le même jour, en appelant yfinance directement : `^GSPC` 7 680,36,
`^IXIC` 26 113,75, `^DJI` 53 547,62, `^VIX` 15,44, `GC=F` 4 682,10. **La donnée
existait.** Ce n'était pas la source, c'était la file.

## La correction

Seize symboles portent la **lecture d'ensemble** de la page d'accueil ; les 513
autres en portent une ligne chacun. Les servir en premier ne coûte rien et
garantit l'en-tête même quand la queue tombe.

Et l'abandon se **nomme** désormais : combien de symboles, lesquels restent sans
donnée après le filet Stooq, et pourquoi. Un abandon silencieux se lit comme une
absence chez la source — et on cherche alors du mauvais côté.
"""
from __future__ import annotations

import os

import pytest

os.environ.setdefault('NO_IBKR', '1')
os.environ.setdefault('START_ON_IMPORT', '0')


def _contexte(T):
    return ([T.BENCH, '^VIX', '^GSPC', '^IXIC', '^DJI', '^RUT']
            + [c[0] for c in T._COMMO] + [m[0] for m in T._MACRO_TK])


#  ═══════════  1. le contexte passe avant l'univers  ══════════════════════════

def test_le_contexte_de_marche_est_dans_le_PREMIER_lot():
    """Le cœur du correctif. `_download_universe` télécharge par lots de 50 et
    peut couper après trois lots vides : ce qui n'est pas dans le premier lot
    n'est jamais garanti."""
    import terminal as T
    ctx = _contexte(T)
    syms = ctx + [t for t in T.UNIVERSE if t not in ctx]
    assert len(ctx) <= 50, 'le contexte ne tient plus dans un lot : %d' % len(ctx)
    assert all(t in syms[:50] for t in ctx)


def test_les_indices_du_Dashboard_sont_tous_couverts():
    """Ce que la première rangée affiche doit être ce que le scan demande."""
    import terminal as T
    ctx = set(_contexte(T))
    for tk in ('^GSPC', '^IXIC', '^DJI', '^RUT', '^VIX'):
        assert tk in ctx, tk


def test_les_matieres_et_la_macro_aussi():
    import terminal as T
    ctx = set(_contexte(T))
    for tk in ('GC=F', 'SI=F', 'BTC-USD', 'CL=F'):
        assert tk in ctx, tk
    for tk in ('^IRX', '^TNX', '^TYX'):
        assert tk in ctx, tk


def test_AUCUN_symbole_n_est_demande_DEUX_fois():
    """Un doublon dans la file coûte un aller-retour pour rien, et fausse le
    compte de l'univers."""
    import terminal as T
    ctx = _contexte(T)
    syms = ctx + [t for t in T.UNIVERSE if t not in ctx]
    assert len(syms) == len(set(syms)), 'doublons : %d' % (len(syms) - len(set(syms)))


def test_l_univers_ENTIER_reste_demande():
    """Contre-épreuve : réordonner ne doit rien perdre. Un correctif qui
    amputerait l'univers pour sauver l'en-tête serait pire que le défaut."""
    import terminal as T
    ctx = _contexte(T)
    syms = ctx + [t for t in T.UNIVERSE if t not in ctx]
    manquants = [t for t in T.UNIVERSE if t not in syms]
    assert manquants == [], manquants


def test_le_code_SERVI_place_bien_le_contexte_en_tete():
    """Le banc ci-dessus reconstruit la liste ; celui-ci vérifie que
    `_scan_once` fait la même chose — sans quoi on testerait sa propre copie."""
    import inspect
    import terminal as T
    src = inspect.getsource(T._scan_once)
    i_ctx = src.index('_contexte =')
    i_syms = src.index('_syms = _contexte')
    assert i_ctx < i_syms
    assert 'syms_scan + [BENCH' not in src, (
        "l'ancienne file mettait l'univers en premier")


#  ═══════════  2. l'abandon ne se tait plus  ══════════════════════════════════

def test_l_abandon_apres_lots_vides_est_NOMME():
    """`break` sans un mot : le Dashboard affichait « n/d » et le scan
    annonçait « aucune erreur »."""
    import inspect
    import terminal as T
    src = inspect.getsource(T._download_universe)
    assert '_abandonnes' in src
    i = src.index('bad_batches >= 3')
    #  Fenetre large : le commentaire qui explique le defaut vit entre le test
    #  et l'enregistrement, et une fenetre trop etroite accusait a tort.
    j = src.index('break', i)
    assert '_abandonnes.extend' in src[i:j], (
        "l'abandon doit etre enregistre AVANT le break")


def test_le_rapport_d_abandon_distingue_ce_que_STOOQ_a_rattrape():
    """Un symbole abandonné par Yahoo puis servi par Stooq ne manque plus :
    le compter comme perdu ferait chercher un défaut inexistant."""
    import inspect
    import terminal as T
    src = inspect.getsource(T._download_universe)
    assert 'restes_sans_donnee' in src
    i = src.index('restants =')
    assert 'not in frames' in src[i:i + 120]


def test_le_rapport_est_ABSENT_quand_rien_n_a_ete_abandonne():
    """Contre-épreuve : un bloc toujours présent ne distingue plus rien, et une
    surface qui l'affiche crierait au débit limité à chaque scan sain."""
    import inspect
    import terminal as T
    src = inspect.getsource(T._download_universe)
    assert "} if _abandonnes else None" in src


#  ═══════════  3. le scan sain n'est pas dégradé  ═════════════════════════════

def test_le_mode_DEMO_recoit_la_meme_file():
    """La démo doit montrer les mêmes tuiles : un en-tête vide en démo se lit
    comme un produit cassé."""
    import inspect
    import terminal as T
    src = inspect.getsource(T._scan_once)
    i = src.index('_syms = _contexte')
    assert '_demo_universe(_syms)' in src[i:i + 700]


def test_le_benchmark_reste_le_PREMIER_servi():
    """Sans lui, `_scan_once` s'arrête sur « aucune donnée marché » : c'est le
    symbole dont tout le reste dépend."""
    import terminal as T
    assert _contexte(T)[0] == T.BENCH
