"""vertex/app/exposition.py — SUR QUELLES INTERFACES LE DESK ÉCOUTE, ET POURQUOI.

## Le défaut, mesuré le 25 août 2026

La décision d'écoute vivait en ligne dans `terminal.py` :

```python
lan_ok = AUTH_ON or os.environ.get('VERTEX_LAN') == '1' or 'PORT' in os.environ
host = '0.0.0.0' if lan_ok else '127.0.0.1'
```

…et la **phrase qui l'explique** était écrite **deux fois ailleurs**, à partir
d'une supposition. Les deux mentaient.

**Au démarrage.** Avec `PORT` défini et sans code, le produit écoute sur toutes
les interfaces et annonce « **VERTEX_LAN=1 — SANS code !** » — en nommant une
variable qui n'est pas définie. L'opérateur va la chercher dans son `.env`, ne
la trouve pas, et conclut que le message est périmé. Son desk est ouvert.

**Sur la page Système.** La carte « Verrou d'accès » affirmait, sans code :

> « par sécurité, le serveur n'écoute que **127.0.0.1** (pas d'accès WiFi/LAN) »

C'est faux dès que `VERTEX_LAN=1` ou `PORT` est posé. **L'écran de sécurité
affirmait une protection absente**, à propos du portefeuille réel de
l'utilisateur.

## Ce que ce module change, et ce qu'il ne change pas

Il ne change **aucun comportement d'écoute** : la règle est reprise à
l'identique, y compris `PORT` — un hébergeur comme Render impose ce port et
exige `0.0.0.0`, et l'y contraindre casserait le déploiement.

Il donne à cette règle **un seul propriétaire**. La cause du défaut n'était pas
la règle, c'était qu'elle était *décrite* à deux endroits qui ne la lisaient
pas. Un texte qui n'est pas dérivé de l'état qu'il décrit finit toujours par
mentir.
"""
from __future__ import annotations

import os

#: L'écoute est restreinte à la machine locale.
LOCAL = '127.0.0.1'

#: L'écoute est ouverte à toutes les interfaces.
TOUTES = '0.0.0.0'

MOTIF_VERROU = 'VERROU'          #: un code d'accès est exigé
MOTIF_LAN = 'VERTEX_LAN'         #: ouverture explicitement demandée, sans code
MOTIF_PORT = 'PORT'              #: hébergeur (Render…) qui impose le port
MOTIF_LOCAL = 'LOCAL'            #: rien n'est ouvert


def exposition(auth_on: bool, env=None) -> dict:
    """Où le serveur écoute, pourquoi, et s'il est protégé.

    Rend toujours les mêmes clés :

    - `hote` : `127.0.0.1` ou `0.0.0.0` ;
    - `ouvert_au_reseau` : booléen ;
    - `motif` : lequel des quatre cas s'applique ;
    - `protege` : un code est-il exigé — **indépendant** de l'ouverture ;
    - `expose_sans_code` : le cas dangereux, nommé pour qu'on puisse l'afficher.

    `motif` est calculé dans l'ORDRE de la règle : le verrou d'abord, puis
    l'ouverture explicite, puis l'hébergeur. Sans cet ordre, un desk protégé
    tournant sur Render se décrirait « ouvert par l'hébergeur » alors que le
    code le protège de toute façon.
    """
    env = os.environ if env is None else env
    lan_demande = env.get('VERTEX_LAN') == '1'
    port_impose = 'PORT' in env
    #  Le mode demo se lit de l'ENV, pas de la config importee : ce module est
    #  le proprietaire de la decision de demarrage et doit rester importable
    #  sans tirer la configuration entiere. La regle est celle de config.py.
    demo = env.get('DEMO', '1' if env.get('NO_IBKR') == '1' else '0') == '1'
    ouvert = bool(auth_on or lan_demande or port_impose)
    if auth_on:
        motif = MOTIF_VERROU
    elif lan_demande:
        motif = MOTIF_LAN
    elif port_impose:
        motif = MOTIF_PORT
    else:
        motif = MOTIF_LOCAL
    return {
        'hote': TOUTES if ouvert else LOCAL,
        'ouvert_au_reseau': ouvert,
        'motif': motif,
        'protege': bool(auth_on),
        #  Le seul cas reellement dangereux : joignable depuis le reseau, et
        #  rien ne demande d'identifiant. Le nommer permet a l'ecran de le dire
        #  au lieu de promettre une protection absente.
        'expose_sans_code': bool(ouvert and not auth_on),
        #  Lot 4 — le cas dangereux ne DEMARRE plus : un desk PRIVE (non demo)
        #  joignable du reseau sans code refusait d'etre protege mais pas de
        #  servir. L'avertissement devient un refus. La demo reste la voie
        #  publique legitime (et elle n'ecrit pas quand elle est exposee) ;
        #  le verrou reste la voie protegee ; loopback reste la voie locale.
        'demarrage_refuse': bool(ouvert and not auth_on and not demo),
        'raison': (
            'DEMARRAGE REFUSE : le desk serait joignable du reseau '
            '(%s) sans authentification, avec un portefeuille prive. '
            'Trois issues : definir VERTEX_CODE ; lancer en demo (DEMO=1) ; '
            'ou rester en loopback (retirer VERTEX_LAN/PORT).' % (
                MOTIF_LAN if lan_demande and not auth_on else MOTIF_PORT)
        ) if (ouvert and not auth_on and not demo) else '',
    }


def phrase(etat: dict) -> str:
    """Une ligne qui décrit l'état RÉEL — jamais une intention.

    C'est cette fonction qui manquait : la même vérité, servie au démarrage et
    à l'écran, dérivée du même calcul.
    """
    if not etat['ouvert_au_reseau']:
        return ("acces reseau local : NON (127.0.0.1 seul) — aucun code defini, "
                "le desk n'est joignable que depuis cette machine")
    if etat['motif'] == MOTIF_VERROU:
        return ("acces reseau local : OUI (0.0.0.0) — protege par VERTEX_CODE")
    if etat['motif'] == MOTIF_LAN:
        return ("acces reseau local : OUI (0.0.0.0) — VERTEX_LAN=1, SANS CODE : "
                "toute personne sur ce reseau peut lire le portefeuille")
    return ("acces reseau local : OUI (0.0.0.0) — impose par la variable PORT "
            "(hebergeur), SANS CODE : definis VERTEX_CODE pour proteger l'acces")
