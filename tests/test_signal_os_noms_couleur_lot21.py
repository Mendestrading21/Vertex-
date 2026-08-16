"""SIGNAL OS · LES NOMS DE COULEUR CESSENT DE MENTIR.

## Le constat

L'identité est violette (`#9B7BFF`) depuis la refonte. Le produit la nommait
encore sous **quatre générations d'alias périmés** :

| famille | ce que le nom promet | ce que la valeur rend |
| --- | --- | --- |
| `--vx-ember-*` | braise | violet |
| `--vx-signal-*` | vert « Signal Green » | violet |
| `--vx-orange-*` | orange | violet |
| `--vx-copper-*` | cuivre | violet |

Un commentaire de `tokens.css` décrivait même la chaîne comme « rampe *orange*
legacy → *cuivre* Ember » — trois couleurs citées, aucune exacte.

Même défaut que le fichier `chart-theme-obsidian-copper.js` renommé plus tôt :
**un nom qui ment coûte à chaque lecture**, et il ne se voit pas à l'écran.

## Ce qui a été fait

**113 sites** renommés vers la rampe canonique `--vx-violet-*` dans les six
fichiers consommateurs. Le bloc d'alias survit dans `tokens.css`, marqué
**DÉPRÉCIÉ**, pour ne pas casser une référence extérieure — mais **plus aucun
consommateur du produit ne le nomme**.

## Le piège évité, et il était du genre silencieux

Ma première version définissait `--vx-violet-soft` à `.12`. Or **ce nom existe
déjà** plus bas dans le même `:root`, à `.16`, pour le violet **sémantique** des
options. La seconde déclaration l'aurait emporté, et `--vx-brand-soft` serait
passé de `.12` à `.16` : le fond des actions primaires aurait changé de teinte
**sans qu'aucun test ne le dise** — exactement le défaut que ce lot prétend
corriger. La valeur vit désormais sur `--vx-brand-soft`, et l'alias s'y réfère.

## La preuve

Relevé navigateur des jetons résolus **et** des couleurs réellement peintes, sur
**10 pages**, avant et après : **0 écart**. Un renommage pur doit se prouver,
pas se supposer.
"""

import io
import os
import re

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Les noms périmés. `copper` sans suffixe compris — d'où la frontière de mot.
_PERIMES = re.compile(r'--vx-(?:ember|signal|orange|copper)(?:-[a-z0-9]+)?(?![a-z0-9-])')

# tokens.css DÉFINIT les alias : c'est leur domicile légitime, et les y
# interdire reviendrait à exiger leur suppression, ce qui casserait toute
# référence extérieure. Le gardien porte sur les CONSOMMATEURS.
_DOMICILE = os.path.join('vertex', 'static', 'vertex', 'css', 'tokens.css')


def _fichiers():
    for base, dirs, noms in os.walk(os.path.join(_ROOT, 'vertex')):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for n in noms:
            if n.endswith(('.py', '.css', '.js')):
                chemin = os.path.join(base, n)
                rel = os.path.relpath(chemin, _ROOT)
                if rel.replace('\\', '/') == _DOMICILE.replace('\\', '/'):
                    continue
                yield rel, io.open(chemin, encoding='utf-8').read()


def test_aucun_consommateur_ne_nomme_un_alias_deprecie():
    """Le cœur du lot. Un alias réintroduit ne casse rien — il rend juste le
    code faux à la lecture, durablement et sans symptôme."""
    fautifs = []
    for rel, src in _fichiers():
        # La PROSE peut nommer les alias : c'est même nécessaire pour expliquer
        # pourquoi on ne les emploie plus. On ne retient donc que les usages
        # `var(--vx-…)`, c'est-à-dire les emplois RÉELS.
        for m in re.finditer(r'var\(\s*(--vx-[a-z0-9-]+)', src):
            if _PERIMES.fullmatch(m.group(1)):
                fautifs.append('%s : %s' % (rel, m.group(1)))
    assert not fautifs, (
        'un nom de couleur déprécié est revenu dans le produit :\n  '
        + '\n  '.join(sorted(set(fautifs)))
        + '\nEmployer la rampe canonique `--vx-violet-*` (ou `--vx-brand-*`). '
          'Les alias `ember` / `signal` / `orange` / `copper` rendent tous le '
          'même violet : leur nom ment.')


def test_les_alias_survivent_dans_leur_domicile():
    """CONTRE-EXEMPLE du test précédent. Il aurait été facile de « finir le
    travail » en supprimant le bloc d'alias — et de casser toute référence
    extérieure au dépôt, sans filet. Ils restent définis, et dépréciés."""
    src = io.open(os.path.join(_ROOT, _DOMICILE), encoding='utf-8').read()
    for nom in ('--vx-ember-500', '--vx-orange-500', '--vx-copper-light',
                '--vx-signal-500'):
        assert (nom + ':') in src, (
            'l\'alias %s a été SUPPRIMÉ au lieu d\'être déprécié : toute '
            'référence extérieure au dépôt casse sans avertissement.' % nom)
    assert 'DÉPRÉCIÉ' in src, (
        'les alias ne sont plus marqués comme dépréciés : rien n\'empêche '
        'quelqu\'un de croire qu\'ils sont le nom courant.')


def test_le_jeton_doux_de_marque_garde_sa_valeur():
    """LE test qui compte, parce que c'est le défaut que j'ai failli
    introduire. `--vx-violet-soft` existe DÉJÀ à .16 pour le violet sémantique
    des options ; y domicilier le doux de MARQUE (.12) l'aurait fait écraser
    par la déclaration suivante, et le fond des actions primaires aurait changé
    de teinte en silence.

    On tient donc les deux valeurs, distinctes, et le sens de la référence.
    """
    src = io.open(os.path.join(_ROOT, _DOMICILE), encoding='utf-8').read()
    assert '--vx-brand-soft:rgba(155,123,255,.12);' in src, (
        'le doux de marque n\'est plus défini par une valeur propre : '
        'vérifier qu\'il n\'a pas été redirigé vers `--vx-violet-soft`, qui '
        'vaut .16 et appartient au violet sémantique des options.')
    assert '--vx-violet-soft:rgba(155,123,255,.16);' in src, (
        'le violet sémantique des options a changé de valeur ou de nom.')
    # Le SENS de la référence : l'alias pointe vers la marque, pas l'inverse.
    assert '--vx-ember-soft:var(--vx-brand-soft);' in src, (
        'la valeur du doux de marque est redevenue domiciliée dans un alias '
        'déprécié : la source de vérité ne doit pas porter un nom périmé.')


def test_le_nuancier_officiel_montre_la_rampe_canonique():
    """`/design-system` existe pour donner la référence. Il listait quatre
    générations de noms périmés — la page qui documente le design documentait
    des noms faux."""
    src = io.open(os.path.join(_ROOT, 'vertex', 'ui', 'pages',
                               'design_system_page.py'), encoding='utf-8').read()
    assert '_MARQUE = [' in src, 'le groupe de marque a été renommé ou retiré'
    bloc = src[src.index('_MARQUE = ['):]
    bloc = bloc[:bloc.index(']')]
    assert '--vx-violet-500' in bloc and '--vx-orange-500' not in bloc, (
        'le nuancier officiel montre de nouveau des alias dépréciés au lieu '
        'de la rampe canonique.')
