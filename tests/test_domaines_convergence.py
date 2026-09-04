"""Vertex Test 1.0 · G2 — LE SEUL VRAI DOUBLON N'ÉTAIT PAS UN DOUBLON DE CODE.

`#783` demande de « converger les domaines qui se recouvrent » —
`company/companies`, `data/data_sources`, `portfolio/positions/tracking` — puis
d'en retirer les doublons **sous preuve**.

La carte des domaines (`DOMAIN_MAP.md`, #787) a mesuré que la prémisse ne tenait
pas : **aucune dispute de fichier**, et des recouvrements d'**un seul symbole**
par paire. Restait à savoir ce que ces quatre symboles homonymes étaient
vraiment.

## Les quatre homonymes, mesurés

| symbole | paquets | verdict |
| --- | --- | --- |
| `get` | data / data_sources | profil d'entreprise vs paquet analyste — **collision de nom** |
| `assess` | portfolio / positions | stress d'un panier vs santé d'une thèse — **collision** |
| `build` | portfolio / tracking | risque d'un panier vs cohorte d'options — **collision** |
| `mae_mfe` | positions / tracking | **la même notion financière, calculée deux fois** |

Trois noms génériques qui se rencontrent, et **un seul vrai doublon**.

## Pourquoi celui-là comptait

Deux calculs de la même mesure, ce n'est pas de la duplication de code : c'est
**deux réponses possibles à la même question**. Et elles divergeaient :

```text
entrée                  positions.calculator     tracking.returns
base NÉGATIVE           mae -220 · mfe -200      None · None
None dans la série      TypeError                valeurs filtrées
chaîne numérique        TypeError                coercée
```

La première ligne est la faute : `if not cost_basis` rejette `0` et `None` mais
**laisse passer un négatif**, et rend alors un chiffre parfaitement plausible
tiré d'une entrée absurde. C'est précisément ce que « aucune donnée financière
inventée » interdit — et c'est plus dangereux qu'un plantage, parce que ça ne se
voit pas.

Le contexte aggrave le cas : `positions.calculator.mae_mfe` est **exporté et
testé, mais aucun chemin de production ne l'appelle** (`recalculator` n'utilise
que `enrich_stock`, `enrich_option`, `portfolio_weights`). Un piège posé pour le
prochain appelant.

## La convergence, et ce qu'elle ne fusionne pas

Le calcul de MAE/MFE est désormais **délégué** à `tracking.returns`, seule
implémentation vivante. Mais `drawdown_from_peak` reste calculé localement, et
ce n'est pas un oubli :

```text
drawdown_from_peak   drawdown MAXIMAL subi sur le chemin      [100,120,90,110] -> -25,00
drawdown_from_high   drawdown COURANT depuis le plus haut     [100,120,90,110] ->  -8,33
```

Deux métriques, pas deux implémentations. Les fusionner « pour converger »
aurait remplacé une mesure par une autre — le contraire du service rendu.
"""
import pathlib
import sys

RACINE = pathlib.Path(__file__).resolve().parents[1]
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from vertex.positions.calculator import mae_mfe as _calc  # noqa: E402
from vertex.tracking.returns import drawdown_from_high  # noqa: E402
from vertex.tracking.returns import mae_mfe as _track  # noqa: E402

#: Les cas qui séparaient les deux implémentations. Ils doivent désormais rendre
#: la MÊME chose — c'est la définition opérationnelle de « convergé ».
CAS = [
    ('nominal', 100.0, [100, 120, 90, 110]),
    ('base zero', 0.0, [100, 120]),
    ('base NEGATIVE', -100.0, [100, 120]),
    ('serie vide', 100.0, []),
    ('None dans la serie', 100.0, [100, None, 120]),
    ('chaine numerique', 100.0, [100, '120', 90]),
    ('valeur negative', 100.0, [100, -50]),
]


def _paire(r):
    """(mae, mfe) quel que soit le nom des clés — les deux contrats diffèrent."""
    mae = r.get('mae', r.get('mae_pct'))
    mfe = r.get('mfe', r.get('mfe_pct'))
    return (mae, mfe)


def test_une_base_negative_ne_produit_plus_de_chiffre_invente():
    """LE DÉFAUT. Un coût de revient négatif rendait `mae -220 · mfe -200` —
    un chiffre plausible tiré d'une entrée absurde. Plus dangereux qu'un
    plantage, parce qu'il ne se voit pas."""
    r = _calc(-100.0, [100, 120])
    assert r['mae'] is None and r['mfe'] is None, (
        'une base NEGATIVE produit de nouveau un chiffre : %s — « aucune '
        'donnee financiere inventee » est viole' % r)
    assert r['drawdown_from_peak'] is None


def test_les_deux_implementations_s_accordent_sur_tous_les_cas():
    """LA PROPRIÉTÉ. Deux calculs de la même mesure sont deux réponses
    possibles à la même question ; converger, c'est qu'il n'y en ait plus
    qu'une."""
    divergences = []
    for nom, base, valeurs in CAS:
        try:
            a = _paire(_calc(base, valeurs))
        except Exception as exc:  # noqa: BLE001
            a = ('LEVE', type(exc).__name__)
        try:
            b = _paire(_track(base, valeurs))
        except Exception as exc:  # noqa: BLE001
            b = ('LEVE', type(exc).__name__)
        if a != b:
            divergences.append((nom, a, b))
    assert not divergences, (
        'les deux implementations de MAE/MFE divergent de nouveau : %s'
        % divergences)


def test_le_cas_nominal_est_inchange():
    """La convergence ne devait rien changer à ce qui marchait."""
    r = _calc(1000.0, [1000, 1200, 900, 1100])
    assert r['mfe'] == 20.0 and r['mae'] == -10.0


def test_le_calcul_est_bien_DELEGUE_et_non_recopie():
    """Recopier le calcul corrigé aurait « convergé » le résultat du jour et
    rouvert la divergence au prochain ajustement. La délégation est ce qui
    tient dans le temps."""
    src = (RACINE / 'vertex' / 'positions' / 'calculator.py').read_text(encoding='utf-8')
    corps = src.split('def mae_mfe(')[1]
    assert 'from vertex.tracking.returns import' in corps, (
        'le calcul de MAE/MFE n\'est plus delegue a la couche canonique : '
        'deux implementations vont redivergent')
    #  La coercion doit venir de la MEME source, sinon les deux fonctions
    #  acceptent des entrees differentes et le desaccord revient par la bande.
    assert '_num' in corps, (
        'la coercion des valeurs n\'est plus celle de la couche canonique : '
        'les deux fonctions n\'accepteront plus les memes entrees')


def test_les_deux_drawdowns_sont_des_metriques_DIFFERENTES():
    """CONTRE-EXEMPLE. `drawdown_from_peak` n'a pas été fusionné avec
    `drawdown_from_high`, et ce n'est pas un oubli : l'un est le drawdown
    MAXIMAL subi sur le chemin, l'autre le drawdown COURANT depuis le plus
    haut. Les fusionner « pour converger » remplacerait une mesure par une
    autre."""
    serie = [100, 120, 90, 110]
    maximal = _calc(100.0, serie)['drawdown_from_peak']
    courant = drawdown_from_high(serie)
    assert maximal == -25.0, maximal
    assert courant == -8.33, courant
    assert maximal != courant, (
        'les deux drawdowns rendent la meme valeur : l\'un des deux a ete '
        'remplace par l\'autre, et une mesure a disparu du produit')


def test_les_trois_autres_homonymes_restent_des_collisions_de_nom():
    """Ils portent le même nom et répondent à des questions différentes.
    Les « converger » sans preuve détruirait une séparation qui tient."""
    import inspect

    from vertex.data import company as d_company
    from vertex.data_sources import analyst_deep
    from vertex.portfolio import historical_stress, legacy_basket_risk
    from vertex.positions import thesis_health
    from vertex.tracking import option_cohort

    paires = [
        ('get', d_company.get, analyst_deep.get),
        ('assess', historical_stress.assess, thesis_health.assess),
        ('build', legacy_basket_risk.build, option_cohort.build),
    ]
    for nom, a, b in paires:
        sa = list(inspect.signature(a).parameters)
        sb = list(inspect.signature(b).parameters)
        assert sa != sb, (
            '« %s » a desormais la MEME signature des deux cotes (%s) : ce '
            'n\'est peut-etre plus une collision de nom mais un vrai doublon '
            '— le mesurer avant de conclure' % (nom, sa))
