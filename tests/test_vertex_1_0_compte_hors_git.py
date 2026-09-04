"""Vertex 1.0 — LE NUMÉRO DE COMPTE RÉEL ÉTAIT DANS UN DÉPÔT PUBLIC.

`CLAUDE.md`, invariant : « aucun secret ou **donnée de compte** dans Git ».
`QUALITY_STANDARD` §9 le répète pour les logs et les fixtures publiques.

## Ce qui a été mesuré le 25 août 2026

`git grep` du numéro de compte IBKR réel : **sept fichiers suivis**, et
`gh api repos/… --jq .private` → **`false`**. Le dépôt est public.

| fichier | nature |
|---|---|
| `docs/archives/interface-visuel/VERTEX_VISUAL_COMMAND_CENTER_AUDIT.md` | document d'audit (juillet) |
| `docs/vertex-1.0/DECISIONS.md` (D-019) | registre de décisions |
| `vertex/data_sources/ibkr_news.py` | docstring de mesure |
| `tests/test_vertex_1_0_g5_adaptateurs.py` | ×4, dont l'assertion d'anonymisation |
| `tests/test_vertex_1_0_news_ibkr.py` | docstring de mesure |
| `tests/test_vertex_1_0_reconciliation_pnl.py` | fixture |
| `tests/test_vertex_1_0_scan_ibkr.py` | docstring de mesure |

**La plupart sont de moi** : je les ai écrits en documentant des mesures prises
sur le compte réel, tout en faisant respecter cet invariant par ailleurs. Le
cas le plus ironique : un banc qui vérifie que l'anonymiseur **retire** le
numéro — et qui, pour le vérifier, l'écrivait en clair.

## La correction, et ses deux formes

- **Bancs** : un numéro **fabriqué** (`U8000001`). Il prouve exactement la même
  chose — une chaîne qui ressemble à un numéro de compte — sans en publier un
  vrai. Les 90 bancs concernés passent sans changement d'intention.
- **Documents et docstrings** : le masque `U<masque>`, celui qu'emploient déjà
  `ibkr_replay` et `ibkr_compte`. Aucune valeur n'y était utile.

## Ce que ce lot NE fait PAS, et il faut le dire

**L'historique Git contient toujours le numéro.** Le retirer exige une
réécriture d'historique — décision humaine, pas correction — et le dépôt étant
public depuis des semaines, il a pu être cloné ou indexé. Nettoyer les fichiers
empêche la **prochaine** publication ; cela n'annule pas les précédentes.

## Gravité, dite honnêtement

Un numéro de compte IBKR seul n'ouvre aucun accès : il faut des identifiants et
un second facteur. Ce n'est pas une clé. C'est une **donnée de compte
identifiante**, publiée, que la doctrine du projet interdit explicitement — et
c'est suffisant pour la retirer.
"""
from __future__ import annotations

import re
import subprocess

import pytest

#: Un numéro de compte IBKR : `U` ou `DU` suivi de 7 chiffres ou plus.
#: `U<masque>` et un compte fabriqué court n'y répondent pas.
_COMPTE = re.compile(r'\b(?:DU|U)1[0-9]{7,}\b')

#: Le compte FABRIQUÉ que les bancs emploient. Il ressemble à un numéro sans en
#: être un : `U8000001` a sept chiffres et ne commence pas par 1.
_FICTIF = 'U8000001'


def _fichiers_suivis() -> list:
    r = subprocess.run(['git', 'ls-files'], capture_output=True,
                       encoding='utf-8', errors='replace')
    if r.returncode != 0:
        pytest.skip('git indisponible — la mesure porterait sur rien')
    return [f for f in r.stdout.split('\n') if f.strip()]


#  ═══════════  1. rien qui ressemble à un compte réel dans Git  ═══════════════

def test_AUCUN_numero_de_compte_reel_dans_les_fichiers_suivis():
    """Sept fichiers en portaient un le 25 août 2026, dans un dépôt PUBLIC."""
    coupables = []
    for f in _fichiers_suivis():
        if f.startswith(('.git/', 'tests/fixtures/')):
            continue
        try:
            with open(f, encoding='utf-8', errors='replace') as fh:
                src = fh.read()
        except (OSError, IsADirectoryError):
            continue
        for m in _COMPTE.finditer(src):
            coupables.append('%s : %s' % (f, m.group(0)))
    assert coupables == [], (
        "donnee de compte dans Git (CLAUDE.md l'interdit) :\n"
        + "\n".join(coupables[:20]))


def test_le_recensement_LIT_vraiment_le_depot():
    """Sans ce contrôle, « aucun coupable » signifierait « je n'ai rien lu »."""
    fichiers = _fichiers_suivis()
    assert len(fichiers) > 200, 'depot suspect : %d fichiers suivis' % len(fichiers)
    assert any(f.endswith('CLAUDE.md') for f in fichiers)


#  ═══════════  2. le motif voit ce qu'il doit voir, et rien d'autre  ══════════

#: Une chaîne qui a **exactement la forme** d'un numéro de compte réel, sans en
#: être un. Elle sert de contre-épreuve au motif.
#:
#: Elle est construite par CONCATÉNATION et non écrite d'un bloc : écrite en
#: clair, elle serait elle-même un « numéro de compte » aux yeux du recensement,
#: et ce banc — le gardien — ferait échouer le gardien. La première version de
#: ce fichier employait le VRAI numéro ici ; elle n'est passée que parce que le
#: fichier n'était pas encore suivi par Git.
_FORME_REELLE = 'U1' + '9999999'


def test_le_motif_RECONNAIT_un_numero_de_cette_FORME():
    """Contre-épreuve. Un gardien qui ne trouve jamais rien passerait pour un
    gardien qui garde — D-031, payé quatre fois dans ce programme."""
    for vrai in (_FORME_REELLE, 'D' + _FORME_REELLE,
                 'le compte %s a refuse' % _FORME_REELLE):
        assert _COMPTE.search(vrai), vrai


def test_ce_FICHIER_ne_contient_lui_meme_aucun_numero_reel():
    """Le gardien doit se soumettre à sa propre règle.

    Ma première version ne s'y soumettait pas : elle écrivait le vrai numéro
    comme contre-épreuve, et ne passait que parce que le fichier n'était pas
    encore suivi. Un gardien exempté de sa règle est le prochain coupable.
    """
    with open(__file__, encoding='utf-8') as fh:
        assert _COMPTE.search(fh.read()) is None


def test_le_motif_ne_signale_PAS_le_masque_ni_le_compte_fabrique():
    """Un gardien qui refuse aussi la correction est désactivé au premier
    commit pressé."""
    for sain in ('U<masque>', _FICTIF, 'DU<masque>', 'compte masque',
                 'UNKNOWN', 'USD', 'U1'):
        assert not _COMPTE.search(sain), sain


def test_le_motif_ne_signale_pas_un_TICKER_ni_une_reference_ordinaire():
    """Contre-épreuve de largeur : un motif trop gourmand aurait accusé du
    texte parfaitement sain, et un gardien qui crie sur tout finit ignoré."""
    for sain in ('AAPL', 'CUSIP 037833100', 'lot 218', 'v215', 'ISIN US0378331005'):
        assert not _COMPTE.search(sain), sain


#  ═══════════  3. les bancs prouvent toujours le masquage  ════════════════════

def test_l_anonymiseur_retire_encore_un_numero_de_compte():
    """Le banc le plus ironique du lot : il vérifie que l'anonymiseur retire un
    numéro de compte — et, pour le vérifier, il en écrivait un VRAI. Un numéro
    fabriqué prouve exactement la même chose.

    `anonymiser` prend un RELEVÉ, pas une chaîne : ma première version de ce
    banc parlait à une API qui n'existe pas.
    """
    from vertex.data_sources import ibkr_replay as R
    out = R.anonymiser({'compte': _FICTIF, 'note': 'le compte %s a refuse' % _FICTIF})
    assert out['compte'] == R.MASQUE_COMPTE
    assert _FICTIF not in out['note']
    assert R.MASQUE_COMPTE in out['note']


def test_l_anonymiseur_reconnait_aussi_le_format_DU():
    """Un compte papier IBKR commence par `DU`. L'oublier publierait tous les
    relevés de démonstration."""
    from vertex.data_sources import ibkr_replay as R
    assert R.anonymiser({'compte': 'DU8000001'})['compte'] == R.MASQUE_COMPTE


def test_le_temoin_de_fuite_VOIT_encore_un_numero_de_compte():
    """`contient_donnee_sensible` rend la LISTE des traces — liste vide =
    publiable. C'est ce témoin, écrit séparément de l'anonymiseur, qui empêche
    « je n'ai rien trouvé » de passer pour « il n'y a rien »."""
    from vertex.data_sources import ibkr_replay as R
    traces = R.contient_donnee_sensible({'note': 'compte %s' % _FICTIF})
    assert traces, 'le temoin ne voit plus un numero de compte'
    assert 'identifiant de compte' in traces[0]


def test_le_temoin_ne_signale_PAS_un_releve_deja_anonymise():
    """Contre-épreuve : un témoin qui crie sur la correction bloquerait toute
    publication, y compris légitime."""
    from vertex.data_sources import ibkr_replay as R
    assert R.contient_donnee_sensible(R.anonymiser({'compte': _FICTIF})) == []
