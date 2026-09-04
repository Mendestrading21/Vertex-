"""
LOT 387 — QUELS TESTS ÉCRIVENT DANS LE VRAI DESK, ET UN QUI POUVAIT LE DÉTRUIRE.

Le lot 386 avait mesuré que la suite complète **réécrit** `desk_data.json`
(md5 f30f5d7da49a → c6beebcf97f0) mais **sans perte** — 6 clés avant et après,
`data` byte-identique. Ce lot descend au fichier de test, et la conclusion
change.

## Le dénominateur, mesuré et non deviné

Quinze fichiers de test touchent au desk. Mesure empirique — chacun rejoué
depuis un état de référence restauré à l'octet :

```
14 / 15   n'écrivent PAS dans le vrai desk   (11 redirigent `persist.cache_path`
                                              vers un tmp_path, 3 ne font que lire)
 1 / 15   écrit                              test_desk_cycle.py
```

Mon premier périmètre — un `grep` sur `desk/push|desk/restore` — n'en voyait que
4 et **manquait tous les `persist.save_json('desk_data.json', …)` directs**, dont
certains écrivent une SEULE clé. Encore une fois : le périmètre de l'outil
mentait, et seule la mesure empirique a donné le bon dénominateur.

## Ce que le seul écrivain faisait vraiment

`test_desk_roundtrip_is_faithful` lit le desk réel, **écrase `myNotes`** par un
marqueur, pousse, vérifie la fidélité, puis restaure. `myNotes` n'est pas une
clé inventée : c'est une **clé synchronisée** (`{"NVDA": "note"}`), présente dans
les trois listes de sync et dotée de ses accesseurs — **les notes par titre du
trader**.

La restauration n'était **pas** protégée. Prouvé par mutation (assertion de
fidélité inversée) :

```
cas 1 — test au vert       : note rendue = True
cas 2 — assertion en échec : note rendue = False
        contenu laissé      : {"guard": "lot84-guard-1786233158"}
```

**Une assertion en échec laissait les notes du trader remplacées par un marqueur
de test, définitivement.** Et le filet ne rattraperait pas grand-chose : le lot
362 a établi que le snapshot est pris **une fois par jour avant la première
écriture** — la suite consomme ce créneau.

Pourquoi le lot 386 n'avait rien vu : **l'utilisateur n'a aujourd'hui aucune
note** (6 clés, `myNotes` absente). Le chemin de perte existait, sans matière à
perdre. *Un « aucune perte constatée » ne vaut que si on vérifie qu'il y avait
quelque chose à perdre.*

## Ce que ce lot fait

Un `try/finally` dans `test_desk_cycle.py` — **fichier de test, aucune
production touchée** — et les gardiens ci-dessous : le recensement des écrivains
et le verrou sur ce `finally`.
"""
import ast
import os

import pytest

DOSSIER = 'tests'

# Seul fichier autorisé à écrire dans le VRAI desk, avec sa justification.
# Tout autre écrivain doit rediriger `persist.cache_path` vers un dossier
# temporaire — c'est la règle que 11 fichiers sur 15 appliquent déjà.
ECRIVAINS_AUTORISES = {
    # Vérifie le contrat bout-en-bout des routes /api/desk sur le blob réel ;
    # remise en état sous `finally` (verrouillée plus bas).
    'test_desk_cycle.py',
}

# Fichiers qui POSTENT sur une route desk sans rediriger, mais dont l'écriture
# n'aboutit JAMAIS — justification vérifiée par un test dédié plus bas.
# {fichier: (code de rejet attendu, nombre de sites d'écriture exemptés)}
# Le nombre de sites est gelé : l'exemption porte sur CE site-là, pas sur le
# fichier entier (voir `test_l_exemption_ne_couvre_pas_un_ecrivain_ajoute…`).
ECRITURES_REJETEES = {
    # Pousse un blob de 3 Mo pour vérifier le plafond de payload : rejeté en
    # 413 par Flask AVANT d'atteindre la route. Mesuré : n'écrit pas.
    'test_production.py': (413, 1),
}

# Dénominateur mesuré au lot 387 : 15 fichiers touchent au desk.
MIN_FICHIERS_DESK = 12


def _fichiers_tests():
    return sorted(n for n in os.listdir(DOSSIER)
                  if n.startswith('test_') and n.endswith('.py'))


def _source(nom):
    return open(os.path.join(DOSSIER, nom), encoding='utf-8').read()


def _touche_le_desk(src):
    return 'desk_data' in src or "'/api/desk" in src or '"/api/desk' in src


def _ecrit_le_desk(src):
    """Écriture = POST sur une route desk, ou save_json direct sur le blob."""
    return ("post('/api/desk" in src or 'post("/api/desk' in src
            or "save_json('desk_data.json'" in src
            or 'save_json("desk_data.json"' in src)


def _redirige_le_cache(src):
    """DEUX mécanismes valides, tous deux en usage dans la suite.

    Ma première version ne connaissait que `cache_path` et accusait donc
    `test_desk_routes.py`, qui redirige par `_BASE_DIR` — du code parfaitement
    sain. Un gardien qui accuse du code sain finit désactivé (leçon du lot 383).
    """
    return any(m in src for m in (
        "setattr(persist, 'cache_path'", 'setattr(persist, "cache_path"',
        "setattr(persist, '_BASE_DIR'", 'setattr(persist, "_BASE_DIR"'))


# ── 1. Le dénominateur ──────────────────────────────────────────────────────

def test_le_detecteur_voit_bien_les_fichiers_qui_touchent_au_desk():
    """Sans dénominateur, le recensement ci-dessous passerait pour complet en
    couvrant zéro fichier (leçon des lots 375-377, 385)."""
    n = sum(1 for f in _fichiers_tests() if _touche_le_desk(_source(f)))
    assert n >= MIN_FICHIERS_DESK, (
        'seulement %d fichiers de test touchant au desk (15 mesurés au lot '
        '387) — détecteur cassé : ne pas se fier au recensement' % n)


def test_le_detecteur_distingue_bien_ecriture_et_lecture():
    """Anti-vide du second détecteur : s'il ne voyait AUCUNE écriture, la
    propriété centrale serait vraie pour la mauvaise raison."""
    ecrivains = [f for f in _fichiers_tests() if _ecrit_le_desk(_source(f))]
    assert ecrivains, 'le détecteur d\'écriture ne trouve plus rien — cassé'


# ── 2. LA propriété : personne n'écrit dans le vrai desk sans le dire ───────

def test_aucun_test_n_ecrit_dans_le_vrai_desk_sans_redirection():
    """Un test qui écrit `desk_data.json` sans rediriger `persist.cache_path`
    touche les DONNÉES PERSONNELLES de l'utilisateur. Le lot 362 a montré qu'un
    push partiel remplace le blob ENTIER : une seule clé poussée efface les
    autres, et le filet ne rend que l'état d'avant la première écriture du jour.
    """
    coupables = [f for f in _fichiers_tests()
                 if f not in ECRIVAINS_AUTORISES
                 and f not in ECRITURES_REJETEES
                 and _ecrit_le_desk(_source(f))
                 and not _redirige_le_cache(_source(f))]
    assert not coupables, (
        'ces tests écrivent dans le VRAI desk sans rediriger `cache_path` ni '
        '`_BASE_DIR` vers un dossier temporaire : %s — soit ajouter la '
        'redirection (12 fichiers le font déjà), soit les inscrire dans '
        'ECRIVAINS_AUTORISES avec leur justification ET une remise en état '
        'sous `finally`' % ', '.join(coupables))


def test_les_ecritures_dites_rejetees_le_sont_vraiment():
    """Une exemption ne vaut que si sa raison est vérifiable. Ces fichiers
    poussent sans redirection : ils ne sont tolérés que parce que la requête
    est refusée AVANT d'atteindre le stockage."""
    for nom, (code, _n) in sorted(ECRITURES_REJETEES.items()):
        src = _source(nom)
        assert 'status_code == %d' % code in src, (
            '%s est exempté au motif d\'un rejet %d, mais plus aucun test n\'y '
            'vérifie ce code : l\'exemption est devenue une supposition'
            % (nom, code))


def test_l_exemption_ne_couvre_pas_un_ecrivain_ajoute_apres_coup():
    """L'exemption porte sur UN site d'écriture précis, pas sur le fichier
    entier. La preuve ROUGE l'a montré : avec une exemption au fichier, un
    écrivain ajouté dans `test_production.py` passait en silence. On gèle donc
    le NOMBRE de sites, fixé à la mesure."""
    for nom, (_code, attendus) in sorted(ECRITURES_REJETEES.items()):
        arbre = ast.parse(_source(nom))
        sites = [n for n in ast.walk(arbre)
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                 and n.func.attr == 'post'
                 and any(isinstance(a, ast.Constant) and isinstance(a.value, str)
                         and a.value.startswith('/api/desk') for a in n.args)]
        assert len(sites) == attendus, (
            '%s : %d écritures desk trouvées, %d exemptée(s) au lot 387 — un '
            'site a été ajouté dans un fichier exempté : vérifier qu\'il '
            'redirige ou qu\'il est lui aussi rejeté avant écriture'
            % (nom, len(sites), attendus))


def test_le_recensement_des_ecrivains_ne_se_perime_pas():
    """Anti-péremption : une autorisation qui ne correspond plus à rien doit
    être retirée, sinon la liste blanche couvre un cas disparu."""
    for nom in sorted(ECRIVAINS_AUTORISES):
        chemin = os.path.join(DOSSIER, nom)
        assert os.path.exists(chemin), \
            'écrivain autorisé disparu, retirer du recensement : %s' % nom
        assert _ecrit_le_desk(_source(nom)), (
            '%s n\'écrit plus dans le desk : retirer son autorisation'
            % nom)


# ── 3. Le verrou : l'écrivain autorisé doit remettre en état QUOI QU'IL ARRIVE

@pytest.mark.parametrize('nom', sorted(ECRIVAINS_AUTORISES))
def test_l_ecrivain_autorise_restaure_sous_finally(nom):
    """LA propriété du lot 387. Sans `finally`, une assertion en échec laisse
    les données personnelles dans l'état du test — prouvé par mutation : les
    notes du trader remplacées par `{"guard": "lot84-guard-…"}`.
    """
    arbre = ast.parse(_source(nom))
    fautifs = []
    for fn in ast.walk(arbre):
        if not (isinstance(fn, ast.FunctionDef) and fn.name.startswith('test_')):
            continue
        ecrit = any(
            isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
            and n.func.attr == 'post'
            and any(isinstance(a, ast.Constant) and isinstance(a.value, str)
                    and a.value.startswith('/api/desk') for a in n.args)
            for n in ast.walk(fn))
        if not ecrit:
            continue
        protege = any(isinstance(n, ast.Try) and n.finalbody for n in ast.walk(fn))
        if not protege:
            fautifs.append(fn.name)
    assert not fautifs, (
        '%s : ces tests écrivent dans le VRAI desk sans remise en état sous '
        '`finally` — une assertion en échec laisserait les données '
        'personnelles de l\'utilisateur dans l\'état du test : %s'
        % (nom, ', '.join(fautifs)))


def test_la_remise_en_etat_repousse_bien_l_etat_initial():
    """Le `finally` ne suffit pas s'il repousse autre chose que l'état lu au
    départ. Vérifie que le payload restauré DÉRIVE bien de `d0`.

    ⚠ Version précédente : elle cherchait la chaîne exacte
    `'data': d0.get('data')`. Le durcissement de #783/G2 — le serveur conserve
    désormais une clé qu'un push omet — a obligé le `finally` à passer par une
    variable (`retour = dict(d0.get('data') or {})`, plus la clé du test vidée
    EXPLICITEMENT, sans quoi le marqueur resterait dans le desk réel). La chaîne
    littérale a disparu ; l'intention, elle, est mieux tenue qu'avant.

    D'où une vérification par l'AST plutôt que par le texte : la valeur postée
    doit être `d0.get('data')` **ou** un nom construit à partir de `d0` dans ce
    même `finally`. Un payload qui ne descend pas de `d0` échoue toujours."""
    import ast as _ast
    arbre = _ast.parse(_source('test_desk_cycle.py'))
    fn = next(n for n in _ast.walk(arbre)
              if isinstance(n, _ast.FunctionDef)
              and n.name == 'test_desk_roundtrip_is_faithful')
    essai = next(n for n in _ast.walk(fn) if isinstance(n, _ast.Try) and n.finalbody)
    corps = essai.finalbody

    def _cite_d0(noeud):
        return any(isinstance(x, _ast.Name) and x.id == 'd0'
                   for x in _ast.walk(noeud))

    #  Les noms locaux du `finally` bâtis à partir de `d0`.
    issus_de_d0 = {c.id for st in corps if isinstance(st, _ast.Assign)
                   and _cite_d0(st.value)
                   for c in st.targets if isinstance(c, _ast.Name)}

    postes = [n for st in corps for n in _ast.walk(st)
              if isinstance(n, _ast.Call) and isinstance(n.func, _ast.Attribute)
              and n.func.attr == 'post']
    assert postes, 'le `finally` ne repousse plus rien'
    for appel in postes:
        charge = next((k.value for k in appel.keywords if k.arg == 'json'), None)
        assert isinstance(charge, _ast.Dict), 'payload de remise en etat illisible'
        valeur = next((v for k, v in zip(charge.keys, charge.values)
                       if isinstance(k, _ast.Constant) and k.value == 'data'), None)
        assert valeur is not None, 'la remise en etat ne poste plus de `data`'
        descend = _cite_d0(valeur) or (isinstance(valeur, _ast.Name)
                                       and valeur.id in issus_de_d0)
        assert descend, (
            'la remise en etat ne repousse plus l\'etat initial `d0` : elle '
            'ecrirait autre chose que ce que l\'utilisateur avait')


# ── 4. La clé touchée est bien une donnée personnelle synchronisée ──────────

def test_la_cle_touchee_est_bien_une_donnee_personnelle():
    """Ce qui donne son poids au reste. Si `myNotes` cessait d'être une clé
    synchronisée, le risque changerait de nature et ce lot serait à rejouer."""
    statique = open('vertex/static/vertex/js/vx-entities.js', encoding='utf-8').read()
    repli = open('vertex/ui/pages/system_page.py', encoding='utf-8').read()
    assert "'myNotes'" in statique, \
        'myNotes n\'est plus une clé de sync servie — rejouer le lot 387'
    assert "'myNotes'" in repli, \
        'myNotes absente du repli servi de /system — rejouer le lot 387'
