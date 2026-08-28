#!/usr/bin/env python3
"""Vertex 1.0 · SONDE HTTP PARTAGÉE — une panne n'est pas une lenteur.

Six outils de mesure interrogent le produit par HTTP. Les six avaient la même
forme : un délai **plat**, un `except Exception`, et rien d'autre. Une
expiration y devenait indiscernable d'un plantage.

## Le défaut, mesuré le 24 août 2026

`mesurer_surfaces_vides` (délai 8 s) sur la machine live, TWS ouvert :

| passage | état du serveur | « surfaces en erreur » |
|---|---|---:|
| 1 | chaud, scan de 630 s | **4** |
| 2 | redémarré, à froid | **1** |
| 3, 4, 5 | chaud | **0** |

Le produit n'a pas changé entre ces passages. Interrogées une à une avec un
délai généreux, les quatre répondent **200 avec leurs données** en 2,2 à 5,2 s.
L'instrument n'annonçait donc pas des pannes : il annonçait sa propre patience.

C'est le pire défaut possible pour un instrument d'audit. Un outil qui crie
quatre pannes imaginaires apprend à son lecteur à ne plus le lire — et le jour
où la cinquième est réelle, elle passe avec les autres.

## Ce que cette sonde garantit

1. Une **durée mesurée** accompagne chaque appel. Sans elle, aucun avant/après
   n'est possible — et le programme en exige un à chaque lot.
2. Une expiration est `EXPIREE`, jamais `ERREUR` : « je n'ai pas attendu assez
   longtemps » n'est pas « c'est cassé ».
3. Un 200 lent est `LENTE`, jamais `ERREUR` : la donnée est arrivée.
4. Le plafond est **généreux** (60 s) parce que D-024 documente des routes à
   9–31 s. Un plafond plus court ne mesure plus le produit, il mesure l'outil.

## Le seuil de lenteur est une CONVENTION, et le dit

`BUDGET_INTERACTIF = 10.0` s. Ce n'est **pas** une mesure. On a cherché le
budget réel du client : il n'y en a aucun. Le produit contient **un** seul
`AbortController` (`vertex/static/vertex/js/vx-core.js`), et il sert
l'annulation demandée par l'appelant — **aucun minuteur ne le déclenche**.
Rien n'abandonne donc une requête au bout d'un délai.

*Correction.* La première rédaction disait « pas un `AbortController` dans
toute l'UI » : c'était faux, et le gardien qui l'appuyait ne balayait que
`vertex/ui/**/*.py`, jamais le JavaScript servi sous `/static` — où il vit.
Le fond tient (pas de budget de requête), la preuve était mal bornée. Encore
D-031 : un gardien dont le champ est trop étroit certifie ce qu'il n'a pas lu.

Présenter 10 s comme « le moment où le navigateur renonce » serait inventer un
fait, ce que D-039 interdit ailleurs pour les dates. C'est un seuil de confort
déclaré : au-delà, une surface interactive est inutilisable pour un humain, et
l'outil le signale sans prétendre l'avoir mesuré.
"""
from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field

#: Plafond d'attente. Genereux DELIBEREMENT : D-024 documente `/api/positions/
#: state` a 18-31 s et `/api/ibkr/positions` (retiree au lot 2) a 9-11 s. Un plafond de 8 s les
#: declarait en panne a chaque execution.
PLAFOND_DEFAUT = 60.0

#: Seuil de LENTEUR. Convention declaree, pas mesure — voir le docstring.
BUDGET_INTERACTIF = 10.0

ETAT_OK = 'OK'
ETAT_LENTE = 'LENTE'
ETAT_EXPIREE = 'EXPIREE'
ETAT_ERREUR = 'ERREUR'


@dataclass(frozen=True)
class Reponse:
    """Ce qu'une surface a repondu, et ce qu'il a fallu attendre."""

    chemin: str
    statut: int                       #: 0 = aucune reponse HTTP
    charge: object = None             #: JSON decode, ou {'_texte': n} sinon
    texte: str = ''                   #: corps BRUT — les outils qui cherchent
                                      #: une couleur ou un identifiant dans une
                                      #: page en ont besoin, et le refaire en
                                      #: seconde requete doublerait la charge
                                      #: ET mesurerait un autre instant.
    duree_s: float = 0.0
    expiree: bool = False
    erreur: str | None = None
    plafond: float = field(default=PLAFOND_DEFAUT, repr=False)

    @property
    def etat(self) -> str:
        """OK / LENTE / EXPIREE / ERREUR — dans cet ordre de precedence.

        `EXPIREE` passe AVANT `ERREUR` : confondre les deux est exactement le
        defaut que cette sonde existe pour empecher.
        """
        if self.expiree:
            return ETAT_EXPIREE
        if self.statut != 200:
            return ETAT_ERREUR
        return ETAT_LENTE if self.duree_s > BUDGET_INTERACTIF else ETAT_OK

    @property
    def a_repondu(self) -> bool:
        return self.statut == 200


def appeler(base: str, chemin: str, *, plafond: float = PLAFOND_DEFAUT,
            entetes: dict | None = None) -> Reponse:
    """Interroge une surface et rend TOUJOURS une `Reponse` — jamais une levee.

    Un outil de mesure qui s'interrompt sur la premiere surface muette ne
    mesure rien : c'est pour cela que tout est capture et rendu.
    """
    url = base.rstrip('/') + chemin
    req = urllib.request.Request(url, headers=entetes or {})
    debut = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=plafond) as r:
            brut, statut = r.read(), r.status
    except urllib.error.HTTPError as e:
        #  Un 4xx/5xx est une REPONSE : le serveur a parle, et son code est la
        #  mesure. L'ecraser en `statut=0` perdrait la seule information utile.
        return Reponse(chemin, e.code, None, '', time.monotonic() - debut,
                       erreur='HTTP %s' % e.code, plafond=plafond)
    except (socket.timeout, TimeoutError):
        return Reponse(chemin, 0, None, '', time.monotonic() - debut,
                       expiree=True,
                       erreur='expiree apres %.1f s' % plafond, plafond=plafond)
    except urllib.error.URLError as e:
        #  `URLError` enveloppe l'expiration du socket sous-jacent : sans ce
        #  deballage, une expiration redevient une « erreur », et la sonde
        #  reproduirait le defaut qu'elle corrige.
        cause = getattr(e, 'reason', None)
        if isinstance(cause, (socket.timeout, TimeoutError)):
            return Reponse(chemin, 0, None, '', time.monotonic() - debut,
                           expiree=True, erreur='expiree apres %.1f s' % plafond,
                           plafond=plafond)
        return Reponse(chemin, 0, None, '', time.monotonic() - debut,
                       erreur=str(cause or e)[:160], plafond=plafond)
    except Exception as e:                                     # noqa: BLE001
        return Reponse(chemin, 0, None, '', time.monotonic() - debut,
                       erreur=str(e)[:160], plafond=plafond)
    duree = time.monotonic() - debut
    texte = brut.decode('utf-8', 'replace')
    try:
        return Reponse(chemin, statut, json.loads(brut), texte, duree,
                       plafond=plafond)
    except ValueError:
        #  Pas du JSON : une page HTML est une reponse valide pour les outils
        #  qui mesurent des espaces. On conserve sa TAILLE comme charge — et
        #  son corps entier dans `texte`.
        return Reponse(chemin, statut, {'_texte': len(brut)}, texte, duree,
                       plafond=plafond)


def sonder_pret(base: str, *, plafond: float = 15.0) -> dict:
    """L'etat de CHAUFFE du produit, demande au produit lui-meme.

    Une surface alimentee par le scan est vide tant que le scan n'a pas tourne.
    C'est un etat TRANSITOIRE, pas un defaut — et le produit l'annonce sur
    `/healthz` (`last_scan: null`). Mesure du 24 aout 2026 : sur un serveur
    fraichement redemarre, `/api/cockpit` et `/api/comite` sortaient
    « vides A EXAMINER » alors que `last_scan` valait `null`. L'outil envoyait
    l'auditeur chercher un defaut qui n'existait pas.

    Rend `{'joignable', 'scan_fait', 'last_scan', 'scan_age', 'scannes'}`.
    `scan_fait` vaut `None` quand le produit n'a pas repondu : ne pas savoir
    n'est pas savoir que non.
    """
    rep = appeler(base, '/healthz', plafond=plafond)
    if not rep.a_repondu or not isinstance(rep.charge, dict):
        return {'joignable': False, 'scan_fait': None, 'last_scan': None,
                'scan_age': None, 'scannes': None}
    d = rep.charge
    return {'joignable': True,
            'scan_fait': d.get('last_scan') is not None,
            'last_scan': d.get('last_scan'),
            'scan_age': d.get('scan_age'),
            'scannes': d.get('scanned')}
