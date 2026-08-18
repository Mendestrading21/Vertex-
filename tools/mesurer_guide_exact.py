"""tools/mesurer_guide_exact.py — LE GUIDE QUI PILOTE CHAQUE SESSION DIT-IL VRAI ?

`CLAUDE.md` est le document à plus fort effet de levier du dépôt : il est lu au
début de **chaque** session et décide de ce qu'on cherche, de ce qu'on croit
mesuré, et de ce qu'on ne revérifie pas. **Rien ne le vérifiait.**

Il a dérivé, et de la façon la plus banale : il annonçait `terminal.py` à
**7 158 lignes** — le chiffre du lot 323 — alors que le fichier en compte
**7 275**. Personne n'a menti ; le code a bougé et la phrase est restée. C'est
exactement le défaut que toute cette série traque ailleurs, appliqué au document
qui la gouverne.

## Ce que l'outil vérifie — et seulement ce qui est vérifiable

1. **Chaque fichier cité existe.** Un guide qui pointe vers un fichier disparu
   est pire qu'un guide muet : il envoie chercher là où il n'y a rien.
2. **Le compte de lignes de `terminal.py`** annoncé est le vrai.
3. **La liste des modules `vertex/ui/*.py`** annoncée comme « complète, mesurée »
   l'est encore.
4. **Les cinq reliques supprimées** le sont toujours.
5. **`READONLY = True`** — l'invariant produit absolu.

Il ne juge **pas** les affirmations d'opinion ni les récits de lots : elles ne
sont pas mécaniquement vérifiables, et prétendre le contraire serait le genre de
garantie creuse que ce dépôt passe son temps à démonter.

## Deux pièges que ce fichier a déjà tendus, et qui sont traités ici

- **Les noms nus.** Le guide cite parfois `briefing.py` sans son chemin. Mon
  premier relevé les déclarait introuvables : c'était mon extraction, pas le
  guide. On résout donc un nom nu en cherchant dans l'arbre.
- **Les citations de fichiers SUPPRIMÉS.** Le guide mentionne `vertex/ui/journal.py`
  **pour dire qu'il n'existe plus** — le compter comme une référence morte serait
  reprocher au guide d'être exact.

## Anti-vacuité

`--temoin` insère dans une copie en mémoire une citation vers un fichier qui
n'existe pas, et exige que l'outil la dénonce. Sans lui, « aucune référence
morte » et « je ne sais pas voir » rendent le même chiffre.

Usage : python tools/mesurer_guide_exact.py [--temoin]
"""
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_GUIDE = os.path.join(RACINE, 'CLAUDE.md')

#  Fichiers que le guide cite POUR DIRE QU'ILS N'EXISTENT PLUS. Les exiger
#  présents reprocherait au guide d'être exact. La liste est explicite : un
#  fichier n'y entre que si le guide dit noir sur blanc qu'il a été supprimé.
_CITES_COMME_SUPPRIMES = {
    'vertex/ui/journal.py',
}

_RELIQUES = ('options_lab', 'journal', 'vault', 'signals', 'strategy_os')


def _guide(temoin=False):
    with open(_GUIDE, encoding='utf-8') as f:
        t = f.read()
    if temoin:
        t += ('\n- Témoin : voir `tools/ce_fichier_nexiste_pas_temoin.py` pour la '
              'marche à suivre.\n')
    return t


def _resoudre(ref):
    """Rend le chemin réel d'une référence, ou None. Un nom nu est cherché."""
    direct = os.path.join(RACINE, ref)
    if os.path.exists(direct):
        return ref
    if '/' in ref:
        return None
    #  NOM NU : le guide écrit parfois `briefing.py` sans son chemin. Le déclarer
    #  introuvable serait accuser le guide de ma propre extraction.
    for base, dirs, noms in os.walk(RACINE):
        dirs[:] = [d for d in dirs if d not in ('.git', '__pycache__', 'node_modules')]
        if ref in noms:
            return os.path.relpath(os.path.join(base, ref), RACINE)
    return None


def _lignes(chemin):
    with open(os.path.join(RACINE, chemin), encoding='utf-8') as f:
        return sum(1 for _ in f)


def verifier(temoin=False):
    """Rend (mortes, ecarts) — références introuvables et chiffres faux."""
    t = _guide(temoin)
    mortes, ecarts = [], []

    refs = sorted(set(re.findall(r'`([A-Za-z0-9_./-]+\.(?:py|js|css|json|md|bat))`', t)))
    for ref in refs:
        if ref in _CITES_COMME_SUPPRIMES:
            continue
        if _resoudre(ref) is None:
            mortes.append(ref)

    #  Le compte de lignes annonce pour terminal.py.
    m = re.search(r'`terminal\.py`\s*\(\*\*([\d   ]+)\s*lignes\*\*', t)
    if not m:
        ecarts.append(('terminal.py', 'aucun compte de lignes annonce',
                       'le guide ne dit plus la taille du monolithe'))
    else:
        dit = int(re.sub(r'[^\d]', '', m.group(1)))
        vrai = _lignes('terminal.py')
        if dit != vrai:
            ecarts.append(('terminal.py', '%d lignes annoncees' % dit,
                           '%d lignes reelles' % vrai))

    #  La liste des modules vertex/ui/*.py, annoncee « complete, mesuree ».
    reels = {n[:-3] for n in os.listdir(os.path.join(RACINE, 'vertex', 'ui'))
             if n.endswith('.py') and n != '__init__.py'}
    m = re.search(r'Modules `vertex/ui/\*\.py` restants\s*:\s*([^—]+)—', t)
    if m:
        dits = set(re.findall(r'`([a-z_]+)`', m.group(1)))
        if dits != reels:
            ecarts.append(('vertex/ui/*.py',
                           'guide : %s' % ', '.join(sorted(dits)),
                           'reel : %s' % ', '.join(sorted(reels))))

    #  Les cinq reliques, annoncees supprimees.
    for r in _RELIQUES:
        if os.path.exists(os.path.join(RACINE, 'vertex', 'ui', '%s.py' % r)):
            ecarts.append(('relique %s' % r, 'annoncee supprimee', 'presente sur disque'))

    #  READONLY, invariant produit absolu.
    with open(os.path.join(RACINE, 'vertex', 'app', 'config.py'), encoding='utf-8') as f:
        cfg = f.read()
    if not re.search(r'^READONLY\s*=\s*True', cfg, re.M):
        ecarts.append(('READONLY', 'annonce True dans le guide',
                       'INTROUVABLE dans vertex/app/config.py'))

    return mortes, ecarts, len(refs)


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if '--temoin' in argv:
        mortes, _, _ = verifier(temoin=True)
        vu = 'tools/ce_fichier_nexiste_pas_temoin.py' in mortes
        print('TEMOIN : %s' % ('DENONCE — le detecteur mord' if vu
                               else '*** PASSE INAPERCU ***'))
        return 0 if vu else 2

    mortes, ecarts, n = verifier()
    print('CLAUDE.md — %d fichiers cites' % n)

    print('\n=== REFERENCES MORTES (le guide envoie chercher ou il n\'y a rien) ===')
    print('  aucune.' if not mortes else '')
    for r in mortes:
        print('  %s' % r)

    print('\n=== CHIFFRES ET LISTES FAUX ===')
    print('  aucun.' if not ecarts else '')
    for quoi, dit, vrai in ecarts:
        print('  %-18s %s  ->  %s' % (quoi, dit, vrai))

    return 1 if (mortes or ecarts) else 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
