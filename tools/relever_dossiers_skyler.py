"""tools/relever_dossiers_skyler.py — LA FILE D'ATTENTE, RENDUE DÉCIDABLE.

`docs/skyler/STATUS.md`, bilan n°18, dans ses propres termes : « 26 dossiers ·
7 à chiffrer · 7 arbitrages humains », « corrections engagées 0 · gardiens 0 ·
octets servis modifiés 0, sur vingt lots », et « dix bilans — n°9 à n°18 —
attendent une réponse ». Cette file ne se vide pas en travaillant davantage :
elle se vide par des arbitrages. Encore faut-il pouvoir arbitrer.

Or on ne le pouvait pas. Le relevé du lot 527 (`docs/skyler/DOSSIERS.md`) s'est
arrêté à son époque et ne détaille que **cinq** dossiers ; les rapports vont
aujourd'hui jusqu'au lot 629. Lire dix bilans pour retrouver ce qui attend une
décision, c'est le contraire d'une file décidable.

## Ce que cet outil fait — et ce qu'il NE reproduit PAS

Il applique les règles du lot 527 à la totalité des rapports, pas à une tranche.
**Mais il ne retrouve pas ses chiffres**, et il faut le dire avant de s'en
servir : sur le périmètre du 527 lui-même (lots ≤ 527), cet outil relève **44**
dossiers là où le 527 en annonçait **35** — 15 contre 10 rangs lus dans un
titre. Un seul nombre coïncide, et c'est le plus contrôlé : **5 dossiers de
rang 4 fiables**, que le 527 avait justement retrouvés par un chemin
indépendant.

Le désaccord n'est pas une surprise : `DOSSIERS.md` existe précisément parce que
les comptes publiés se contredisaient — « le total annoncé vaut toujours un de
moins que la somme de sa propre répartition, sur douze occurrences publiées ».
Un troisième compte qui prétendrait trancher serait un quatrième problème.
**Ce relevé-ci ne tranche pas : il dit ses règles, et elles sont dans ce
fichier.**

Les règles :

- une entrée naît d'une section `## Classement` qui annonce un rang de 1 à 4 ;
- un rapport qui **refuse** (« aucun dossier », « rang 0 ») n'en produit pas ;
- **auto-attribution** : un identifiant `NNN-A` n'est retenu que si `NNN` est le
  numéro du rapport lui-même — le 526 avait rangé « 511-A » sous le lot 512
  parce que le rapport du 512 cite le dossier du précédent ;
- **TITRE vs CORPS** : un rang écrit dans le titre de section est fiable ; un
  rang qui n'apparaît que dans le texte peut désigner un rang *rejeté*
  (« ce n'est pas un rang 2, c'est un rang 4 ») — fragile, et dit comme tel.

## Ce qu'il ne fait pas

**Il n'arbitre rien.** Il ne dit pas si un dossier mérite d'être corrigé,
chiffré ou abandonné : il met chaque dossier sur une ligne, avec son rang, sa
fiabilité et son rapport, pour qu'une décision tienne en un mot. Décider à la
place de l'utilisateur serait exactement la faute que la gouvernance interdit.

Usage : python tools/relever_dossiers_skyler.py [--md fichier.md]
"""
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
RAPPORTS = RACINE / 'docs' / 'refactor' / 'validation'

_REFUS = ('aucun dossier', 'rang 0', 'pas de dossier')
_RANG_TITRE = re.compile(r'##\s*Classement[^\n]*?rang\s*([1-4])', re.I)
_RANG_CORPS = re.compile(r'\brang\s*([1-4])\b', re.I)
_ID = re.compile(r'\b(\d{3})-([A-Z])\b')
#  `**Rang N**` en tête de section : le rang est AFFIRMÉ, pas discuté.
_RANG_AMORCE = re.compile(r'\*\*rang\s*([1-4])\*\*', re.I)


def _section(texte, titre='## Classement'):
    """Le corps de la section, jusqu'au prochain titre de même niveau."""
    i = texte.find(titre)
    if i < 0:
        return None, None
    fin = texte.find('\n## ', i + 1)
    entier = texte[i:] if fin < 0 else texte[i:fin]
    ligne = entier.split('\n', 1)[0]
    return ligne, entier


def _sujet(texte):
    """Le titre H1 du rapport — ce que le dossier dit, en une ligne."""
    for ligne in texte.split('\n'):
        if ligne.startswith('# '):
            return ligne[2:].strip()
    return '(sans titre)'


def relever():
    out = []
    for chemin in sorted(RAPPORTS.glob('SKYLER-LOT-*.md')):
        m = re.search(r'SKYLER-LOT-(\d+)\.md$', chemin.name)
        if not m:
            continue
        lot = int(m.group(1))
        texte = chemin.read_text(encoding='utf-8', errors='replace')
        ligne, corps = _section(texte)
        if corps is None:
            continue
        bas = corps.lower()
        if any(r in bas for r in _REFUS):
            continue
        mt = _RANG_TITRE.search(ligne)
        if mt:
            rang, fiabilite = int(mt.group(1)), 'TITRE'
        else:
            #  TROISIÈME QUALITÉ, mesurée et non prévue par le lot 527.
            #  Sa dichotomie titre/corps traitait comme « fragile » tout rang
            #  absent du titre. Or l'écrasante majorité des rapports ouvrent
            #  leur section par `**Rang N** — …` : le rang y est AFFIRMÉ, pas
            #  discuté. Vérifié sur échantillon (416, 417, 418). Un rang qui
            #  n'apparaît que plus loin, lui, peut désigner un rang REJETÉ
            #  (« ce n'est pas un rang 2, c'est un rang 4 ») — celui-là seul
            #  reste fragile.
            debut = corps.split('\n', 1)[1].lstrip() if '\n' in corps else ''
            ma = _RANG_AMORCE.match(debut)
            if ma:
                rang, fiabilite = int(ma.group(1)), 'AMORCE'
            else:
                mc = _RANG_CORPS.search(corps)
                if not mc:
                    continue
                rang, fiabilite = int(mc.group(1)), 'CORPS'
        #  Auto-attribution : l'identifiant doit porter le numéro du rapport.
        ident = next((f'{a}-{b}' for a, b in _ID.findall(corps)
                      if int(a) == lot), None)
        out.append({'lot': lot, 'id': ident or f'{lot}-?', 'rang': rang,
                    'fiabilite': fiabilite, 'sujet': _sujet(texte),
                    'rapport': f'docs/refactor/validation/{chemin.name}'})
    return out


def feuille(dossiers):
    lignes = [
        '# SKYLER V2 — LA FILE D\'ATTENTE, UNE LIGNE PAR DÉCISION', '',
        '> Produit par `tools/relever_dossiers_skyler.py`, qui applique les',
        '> règles du lot 527 à **tous** les rapports — le relevé d\'origine',
        '> s\'arrêtait à son époque et ne détaillait que cinq dossiers.',
        '> **Rien n\'est arbitré ici** : chaque ligne attend un mot.', '',
        '> ⚠ **Ce compte ne retrouve pas celui du 527** : sur son propre',
        '> périmètre (lots ≤ 527), cet outil relève **44** dossiers là où le 527',
        '> en annonçait **35**. Un seul nombre coïncide, et c\'est le plus',
        '> contrôlé — **5 dossiers de rang 4 fiables**. Le désaccord n\'est pas',
        '> une surprise : `DOSSIERS.md` existe parce que les comptes publiés se',
        '> contredisaient déjà. Ce relevé ne tranche pas ce différend ; il dit',
        '> ses règles, et elles sont lisibles dans l\'outil.', '',
        'Choix possibles, un par ligne : **corriger** · **chiffrer** ·',
        '**abandonner** · **garder en observation**.', '',
        'Un identifiant `NNN-?` veut dire que le rapport **ne se nomme pas** dans',
        'sa section de classement : le dossier existe, son étiquette n\'a jamais',
        'été écrite. C\'est un fait sur les rapports, pas une lacune de l\'outil.', '']
    par_rang = {}
    for d in dossiers:
        par_rang.setdefault(d['rang'], []).append(d)
    lignes.append('| rang | dossiers |')
    lignes.append('| --- | --- |')
    for r in sorted(par_rang):
        lignes.append('| %d | %d |' % (r, len(par_rang[r])))
    lignes.append('| **total** | **%d** |' % len(dossiers))
    lignes.append('')
    n = lambda q: sum(1 for d in dossiers if d['fiabilite'] == q)   # noqa: E731
    lignes += [
        '', '**Trois qualités de rang, et elles ne se valent pas.**', '',
        '| qualité | ce que ça veut dire | dossiers |',
        '| --- | --- | --- |',
        '| `TITRE` | le rang est écrit dans le titre de section | %d |' % n('TITRE'),
        '| `AMORCE` | le rang est **affirmé** en tête de section (`**Rang N**`) | %d |' % n('AMORCE'),
        '| `CORPS` | le rang n\'apparaît que plus loin — il peut désigner un rang **rejeté** | %d |' % n('CORPS'),
        '',
        'Les **%d** premiers (`TITRE` + `AMORCE`) sont ceux sur lesquels une '
        'décision peut se prendre sans rouvrir le rapport. Les **%d** derniers '
        'demandent une lecture avant d\'être tranchés.'
        % (n('TITRE') + n('AMORCE'), n('CORPS')), '']
    for r in sorted(par_rang):
        lignes.append('## Rang %d' % r)
        lignes.append('')
        lignes.append('| dossier | fiabilité | ce que le rapport dit | décision |')
        lignes.append('| --- | --- | --- | --- |')
        for d in sorted(par_rang[r], key=lambda x: x['lot']):
            sujet = d['sujet'].replace('|', '·')
            if len(sujet) > 96:
                sujet = sujet[:93] + '…'
            lignes.append('| [`%s`](../%s) | %s | %s |  |'
                          % (d['id'], d['rapport'].replace('docs/', ''),
                             d['fiabilite'], sujet))
        lignes.append('')
    return '\n'.join(lignes) + '\n'


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    dossiers = relever()
    if not dossiers:
        print('AVEUGLE — aucun dossier relevé sur %d rapports : la règle '
              'd\'extraction ne mord plus, refus de publier une file vide.'
              % len(list(RAPPORTS.glob('SKYLER-LOT-*.md'))))
        return 2
    print('rapports SKYLER-LOT : %d · dossiers releves : %d'
          % (len(list(RAPPORTS.glob('SKYLER-LOT-*.md'))), len(dossiers)))
    for q, quoi in (('TITRE', 'rang dans le titre de section  (fiable)'),
                    ('AMORCE', 'rang AFFIRME en tete de section (fiable)'),
                    ('CORPS', 'rang plus loin dans le texte   (fragile)')):
        print('   %-7s %s : %d'
              % (q, quoi, sum(1 for d in dossiers if d['fiabilite'] == q)))
    for r in sorted({d['rang'] for d in dossiers}):
        print('   rang %d : %d' % (r, sum(1 for d in dossiers if d['rang'] == r)))
    if '--md' in argv:
        cible = pathlib.Path(argv[argv.index('--md') + 1])
        cible.write_text(feuille(dossiers), encoding='utf-8')
        print('\nfeuille ecrite : %s' % cible)
    return 0


if __name__ == '__main__':
    code = main()
    print('EXIT=%d' % code)
    sys.exit(code)
