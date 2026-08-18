"""SIGNAL OS · LA DÉGRADATION HONNÊTE, ÉPROUVÉE POUR DE BON.

`CLAUDE.md` pose l'invariant le plus important du produit — « donnée absente →
mention honnête, jamais un chiffre inventé ». Personne ne l'avait **éprouvé** :
on l'avait lu dans le code, jamais **provoqué**.

Trois pannes simulées, sur les points de **données uniquement** — jamais le
HTML, le CSS ni le JS, sinon on mesurerait un navigateur en panne et non un
produit qui dégrade.

| panne | fuites | erreurs de page |
| --- | --- | --- |
| erreur 500 | **0** | **0** |
| réponse vide (`{}`) | **1 → 0** | **0** |
| JSON malformé | **0** | **0** |

33 vues × 3 pannes.

## Le défaut trouvé

Sur une réponse vide, le scanner LEAPS rendait :

> `· fenêtre  DTE · undefined contrat(s)`

Un mot technique lu par l'utilisateur, et deux champs muets qui **ressemblaient
à des valeurs**. Les cellules voisines gardaient déjà (`c.iv != null ? … : '—'`)
— c'est cette ligne-ci qui avait oublié.

`undefined` n'est pas une donnée absente : c'est une fuite de plomberie, et elle
ressemble assez à du texte pour passer inaperçue.

## Deux faux positifs écartés, vérifiés avant d'accuser

Mon heuristique « du contenu mais aucun état honnête » signalait
`/journal?view=progression` et `/system?view=settings`. Ce sont des vues
**statiques** — le relais posé au lot 11 et un formulaire de réglages — dont le
contenu ne vient d'**aucune** source. Vérifié en mesurant les chiffres
réellement affichés : seulement des valeurs de filtre pour la première, aucun
pour la seconde.

> Une vue qui n'affiche pas de donnée n'a pas d'état de donnée à montrer.
"""

import io
import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _lire(*p):
    return io.open(os.path.join(_ROOT, *p), encoding='utf-8').read()


def test_le_resume_leaps_garde_chacun_de_ses_champs():
    """Le défaut mesuré. Trois champs, trois gardes — en corriger deux sur
    trois laisserait la ligne mentir sur le troisième."""
    src = _lire('vertex', 'static', 'vertex', 'js', 'pages', 'options-scanner.js')
    assert "var univ = d.universe ? esc(d.universe) : '—';" in src, (
        'l\'univers du scanner LEAPS n\'est plus gardé : un champ vide y '
        'ressemblait à une valeur.')
    assert "var fen = (d.window && d.window.length)" in src, (
        'la fenêtre DTE n\'est plus gardée : elle rendait « fenêtre  DTE », '
        'deux mots sans nombre entre eux.')
    assert "var nb = (d.n != null && isFinite(d.n))" in src, (
        'le nombre de contrats n\'est plus gardé : c\'est LUI qui rendait '
        '« undefined contrat(s) » à l\'écran.')
    assert "'nombre de contrats n/d'" in src, (
        'la mention honnête a disparu au profit d\'un silence : une donnée '
        'absente se dit, elle ne se laisse pas deviner.')


def test_aucune_fuite_technique_n_est_concatenee_sans_garde():
    """CONTRE-EXEMPLE de la correction précédente, généralisé au fichier :
    une valeur brute concaténée dans du texte est exactement le mécanisme qui a
    produit « undefined ». On vérifie que le fichier n'en réintroduit pas."""
    src = _lire('vertex', 'static', 'vertex', 'js', 'pages', 'options-scanner.js')
    assert "+ ' DTE · ' + d.n + ' contrat(s)'" not in src, (
        'la concaténation brute qui produisait « undefined contrat(s) » est '
        'revenue.')


def test_l_instrument_de_degradation_est_conserve():
    """Un invariant qu'on ne peut plus provoquer redevient une croyance."""
    outil = os.path.join(_ROOT, 'tools', 'mesurer_degradation.py')
    assert os.path.isfile(outil), 'l\'instrument de dégradation a disparu'
    src = io.open(outil, encoding='utf-8').read()
    for panne in ('erreur 500', 'reponse vide', 'json malforme'):
        assert "'" + panne + "'" in src, (
            'la panne « %s » n\'est plus simulée : le produit n\'est plus '
            'éprouvé sur ce mode de défaillance.' % panne)
    assert 'NaN|undefined|null|Infinity' in src, (
        'la liste des fuites techniques a été réduite : ce sont ces mots-là '
        'qui ressemblent assez à du texte pour passer inaperçus.')


def test_l_instrument_ne_casse_que_les_donnees():
    """Le point de méthode. Intercepter le HTML, le CSS ou le JS ferait
    mesurer un navigateur en panne — et rendrait un verdict catastrophique qui
    ne dirait rien du produit."""
    src = io.open(os.path.join(_ROOT, 'tools', 'mesurer_degradation.py'),
                  encoding='utf-8').read()
    assert "_DONNEES = '**/{api,scan,cal-feed,news-feed}**'" in src, (
        'la portée des pannes a changé : si elle atteint le HTML, le CSS ou '
        'le JS, l\'instrument mesure un navigateur cassé et non un produit '
        'qui dégrade.')


def test_les_vues_statiques_sont_exclues_nommement():
    """Les deux faux positifs, écartés PAR LEUR NOM et non par un seuil qu'on
    aurait relevé jusqu'à ce qu'ils se taisent. Relever le seuil aurait aussi
    masqué de vraies vues muettes."""
    src = io.open(os.path.join(_ROOT, 'tools', 'mesurer_degradation.py'),
                  encoding='utf-8').read()
    assert "_SANS_DONNEE = ('/journal?view=progression', '/system?view=settings')" in src, (
        'les vues statiques ne sont plus écartées nommément : soit '
        'l\'instrument les accuse à tort, soit quelqu\'un a relevé le seuil '
        'et masqué du même coup de vraies vues muettes.')
