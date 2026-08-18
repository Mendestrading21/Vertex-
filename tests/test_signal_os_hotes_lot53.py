"""SIGNAL OS · LOT 53 — LES QUINZE HÔTES DE LA FICHE, ET TROIS ACCUSATIONS RETIRÉES.

Réserve SIGNAL-OS-52 §6.4 : les autres sorties de la fiche n'avaient jamais été
vérifiées au pixel. `tools/mesurer_hotes_resolus.py` les vérifie maintenant, en
nominal **et sous coupure totale des données**. Verdict : **les quinze hôtes
aboutissent dans les deux modes**, et sous coupure chacun dit sa panne par un
bandeau nommé. Aucun défaut produit.

## Pourquoi ce fichier tient si peu de choses

J'ai voulu un gardien statique : « chaque `async function load*` contient un
`catch` qui peint ». Mesuré sur les six loaders, ma détection en donnait **quatre
sur six** — `loadDecisionStack` était compté comme ne peignant pas, alors que le
navigateur le voit afficher « ⚠ Décision indisponible » sous coupure. La cause
est banale et connue de cette série : une expression régulière `[^}]*` ne
traverse pas des accolades imbriquées. **C'est comparer par le texte ce qui doit
l'être par la structure.**

Livrer ce gardien, c'était livrer un test faux pour deux loaders sur six. Le
comportement se prouve au navigateur ; ce fichier ne tient donc que des faits
**structurels**, vérifiables par sous-chaîne sans rien interpréter :

1. les quinze hôtes existent et portent leur squelette — sans lui, l'instrument
   du lot 53 devient aveugle, car c'est le squelette qui **définit** un hôte ;
2. les trois disclosures que l'instrument doit ouvrir portent toujours leur
   libellé — sinon il ne les trouve plus et mesure moins que la fiche ne montre.

Un gardien qui tient peu et le tient vraiment vaut mieux qu'un gardien qui
promet tout et se trompe deux fois sur six.
"""
import re

import pytest

#  Mesuré : la fiche sert quinze `%%LOADING%%`. C'est le nombre d'endroits où
#  le produit promet du contenu.
HOTES_ATTENDUS = 15

#  Les libellés que `tools/mesurer_hotes_resolus.py` clique, dans l'ordre où un
#  humain les rencontre. « Évidence historique » est imbriquée dans « Analyse
#  approfondie » : sans elle, `#an-evidence` reste hors de portée — mesuré.
DISCLOSURES = ('Analyse approfondie', 'Évidence historique', 'Contextes du dossier')


@pytest.fixture(scope='module')
def corps(tmp_path_factory):
    from vertex.services import persist
    sauve = persist._BASE_DIR
    persist._BASE_DIR = str(tmp_path_factory.mktemp('hotes53'))
    import terminal
    texte = terminal.app.test_client().get('/analysis/HOTE53').get_data(as_text=True)
    persist._BASE_DIR = sauve
    return texte


def test_la_fiche_sert_bien_ses_quinze_squelettes(corps):
    """LE SQUELETTE DÉFINIT L'HÔTE. `mesurer_hotes_resolus.py` marque, au premier
    instant, tout parent de `.vx-skeleton` — c'est sa définition d'un hôte, et
    c'est la bonne : seul un élément qui a promis du contenu peut manquer à sa
    promesse. Retirer un squelette rend donc l'instrument aveugle sur cet hôte,
    **sans aucun symptôme visible**."""
    n = len(re.findall(r'class="vx-skeleton"', corps))
    assert n == HOTES_ATTENDUS, (
        'la fiche sert %d squelettes au lieu de %d : l\'instrument du lot 53 '
        'mesurera un nombre d\'hotes different de ce que la page promet. Si le '
        'changement est voulu, mettre a jour HOTES_ATTENDUS **et** relancer '
        '`python tools/mesurer_hotes_resolus.py --couper`' % (n, HOTES_ATTENDUS))


@pytest.mark.parametrize('libelle', DISCLOSURES)
def test_la_disclosure_que_l_instrument_ouvre_existe_toujours(corps, libelle):
    """L'instrument atteint les hôtes repliés en CLIQUANT ces libellés — le
    geste du produit. Si l'un change de texte, l'outil ne le trouve plus et
    conclut « non demandé » sur un hôte qu'il aurait dû mesurer : une
    sous-couverture silencieuse, le pire genre."""
    assert libelle in corps, (
        'le libelle « %s » a disparu : `tools/mesurer_hotes_resolus.py` ne sait '
        'plus ouvrir cette disclosure et cessera de mesurer ce qu\'elle '
        'contient, sans le dire' % libelle)


def test_chaque_hote_reste_dans_un_conteneur_adressable(corps):
    """Les hôtes anonymes sont adressés par `[data-body]`, et le peintre les
    atteint par `#id [data-body]`. Ce test tient le contrat des deux côtés."""
    #  ON VISE LA DÉFINITION DU PEINTRE, PAS LE MOTIF. Première version : je
    #  cherchais la sous-chaîne `querySelector('#'+id+' [data-body]')`. Elle
    #  apparaît DEUX fois — dans `body()` et dans le `$b` de `loadAnalyst`.
    #  Contre-épreuve : j'ai cassé la cible du vrai peintre, et le test est
    #  resté vert, satisfait par l'occurrence voisine. C'est la troisième fois
    #  de cette série qu'une occurrence voisine me donne un gardien creux.
    assert ("function body(id,html){const el=document.querySelector"
            "('#'+id+' [data-body]');") in corps, (
        'le peintre `body(id, html)` ne cible plus `#id [data-body]` : les '
        'hotes anonymes de la fiche deviennent inatteignables')
    assert corps.count('data-body') >= 10, (
        'moins de dix conteneurs `data-body` : la moitie des hotes de la fiche '
        'a disparu ou change de convention')
