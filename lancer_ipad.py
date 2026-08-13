#!/usr/bin/env python3
"""VERTEX — lanceur « iPad » : une seule commande, rien à éditer à la main.

    python3 lancer_ipad.py

Ce script fait tout ce qu'il faut pour que Vertex soit joignable depuis un iPad
sur le même Wi-Fi, puis affiche l'adresse à taper dans Safari.

Ce qu'il fait, dans l'ordre :
  1. crée `.env` depuis `.env.example` s'il n'existe pas ;
  2. s'assure qu'un VRAI code d'accès est defini — il en tire un au hasard si la
     valeur est encore le modèle. C'est ce code, et lui seul, qui autorise
     l'écoute réseau : sans lui Vertex n'écoute que 127.0.0.1 et l'iPad ne peut
     rien voir (terminal.py, ligne 7144) ;
  3. NE TOUCHE PAS aux réglages IBKR : ils sont à vous. Il se contente de dire
     ce qu'il lit, pour que `NO_IBKR=1` oublié ne coupe pas la connexion en
     silence — c'est le piège le plus courant ;
  4. détecte l'adresse locale de la machine et affiche l'URL de l'iPad ;
  5. lance Vertex.

Aucun ordre n'est jamais transmis : READONLY est câblé en dur dans le produit.
Ce script ne change rien à cela.
"""
from __future__ import annotations

import os
import re
import secrets
import socket
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent
ENV = RACINE / '.env'
MODELE = RACINE / '.env.example'
PORT = os.environ.get('VERTEX_PORT', '5002')

# Valeurs du modèle : tant qu'elles sont là, le réglage n'a pas été fait.
_PLACEHOLDERS = {'change-moi', 'mets-une-longue-chaine-aleatoire-ici', ''}


def _lire_env(chemin: Path) -> dict:
    if not chemin.exists():
        return {}
    out = {}
    for ligne in chemin.read_text(encoding='utf-8').splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith('#') or '=' not in ligne:
            continue
        cle, _, val = ligne.partition('=')
        out[cle.strip()] = val.strip()
    return out


def _poser(chemin: Path, cle: str, valeur: str) -> None:
    """Écrit `cle=valeur` en remplaçant la ligne existante, commentée ou non."""
    texte = chemin.read_text(encoding='utf-8') if chemin.exists() else ''
    motif = re.compile(r'^#?\s*%s\s*=.*$' % re.escape(cle), re.M)
    if motif.search(texte):
        texte = motif.sub('%s=%s' % (cle, valeur), texte, count=1)
    else:
        texte = texte.rstrip('\n') + '\n%s=%s\n' % (cle, valeur)
    chemin.write_text(texte, encoding='utf-8')


def _ip_locale() -> str | None:
    """L'adresse que la machine présente sur le réseau local.

    On ouvre un socket UDP vers une adresse externe SANS rien envoyer : le
    système choisit l'interface qu'il utiliserait, et on lit son adresse. Aucun
    paquet ne part, aucune connexion n'est établie.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.0.2.1', 1))          # réseau de documentation (RFC 5737)
        ip = s.getsockname()[0]
        return None if ip.startswith('127.') else ip
    except OSError:
        return None
    finally:
        s.close()


def main() -> int:
    print('\n─── VERTEX · préparation de l’accès iPad ───\n')

    # 1. le fichier .env
    if not ENV.exists():
        if not MODELE.exists():
            print('  ✗ ni .env ni .env.example — dépôt incomplet, rien à lancer.')
            return 2
        ENV.write_text(MODELE.read_text(encoding='utf-8'), encoding='utf-8')
        print('  · .env créé depuis .env.example')
    else:
        print('  · .env déjà présent — il n’est pas écrasé')

    conf = _lire_env(ENV)

    # 2. le code d'accès : c'est LUI qui ouvre le réseau local
    code = conf.get('VERTEX_CODE', '')
    if code in _PLACEHOLDERS:
        code = secrets.token_urlsafe(6)
        _poser(ENV, 'VERTEX_CODE', code)
        print('  · code d’accès généré (écrit dans .env)')
    if conf.get('VERTEX_SECRET', '') in _PLACEHOLDERS:
        _poser(ENV, 'VERTEX_SECRET', secrets.token_urlsafe(48))
        print('  · clé de signature générée')

    # 3. IBKR : on ne décide pas à sa place, on dit ce qu'on lit
    conf = _lire_env(ENV)
    no_ibkr, demo = conf.get('NO_IBKR', ''), conf.get('DEMO', '')
    print()
    if no_ibkr == '1':
        print('  ⚠  NO_IBKR=1 dans .env → la connexion IBKR est COUPÉE.')
        print('     C’est le réglage du cloud. Pour vos vraies positions :')
        print('     videz cette ligne (NO_IBKR=) et mettez DEMO=0.')
    elif demo == '1':
        print('  ⚠  DEMO=1 dans .env → données SYNTHÉTIQUES, étiquetées comme telles.')
        print('     Pour vos vraies positions : DEMO=0, et TWS ouvert.')
    else:
        print('  · IBKR actif si TWS/Gateway est ouvert (lecture seule, toujours).')
        print('    Vérifiez ensuite dans Vertex : Système → Connexions.')

    # 4. l'adresse pour l'iPad
    ip = _ip_locale()
    print('\n─── à taper dans Safari, sur l’iPad ───\n')
    if ip:
        print('      http://%s:%s' % (ip, PORT))
    else:
        print('      (adresse locale introuvable — Wi-Fi coupé ?)')
        print('      Réglages → Wi-Fi → (i) vous donnera l’adresse IP.')
    print('\n      code d’accès :  %s\n' % code)
    print('  L’iPad doit être sur le MÊME Wi-Fi, et ce Mac doit rester allumé.')
    print('  Astuce : Partager → « Sur l’écran d’accueil » installe Vertex')
    print('  comme une app plein écran (PWA).\n')
    print('─── lancement ───\n')

    env = dict(os.environ, VERTEX_PORT=PORT)
    try:
        return subprocess.call([sys.executable, str(RACINE / 'terminal.py')], env=env)
    except KeyboardInterrupt:
        print('\n  arrêté.\n')
        return 0


if __name__ == '__main__':
    raise SystemExit(main())
