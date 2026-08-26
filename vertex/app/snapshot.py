"""vertex/app/snapshot.py — UNE REQUÊTE DE PAGE NE COLLECTE PAS.

`QUALITY_STANDARD.md` §8 exige qu'un cache ait un propriétaire et une politique ;
`AUDIT-TOTAL-2026-08-25.md` P0.1 exige qu'une route interactive serve un
snapshot borné plutôt que de lancer une collecte. Ce module est le propriétaire
unique de ce comportement.

## Le défaut mesuré, sur le SHA `73de92f5`

`/api/ticker/<sym>`, compte réel, TWS ouvert :

| situation | 1er appel | appels suivants |
|---|---:|---:|
| au calme | 3,30–3,64 s | 1,28–1,41 s |
| **sous charge** (5 titres neufs d'affilée) | **28–48 s** | — |
| sorties HTTPS coupées | 6,1 s | **6,1 s — le cache ne sert à rien** |

Et surtout, **cinq demandes simultanées du même titre** :

```text
fil 2, 3, 4, 5 :  28,2 s        fil 1 : 136,9 s
```

Aucune coalescence : cinq requêtes identiques refont chacune tout le travail.
C'est le défaut que `singleflight` ferme.

## Trois états, pas deux

Un magasin qui ne connaît que « frais / absent » force la route à attendre.
Celui-ci en connaît trois :

1. **FRAIS** — la valeur est dans sa fenêtre : servie telle quelle ;
2. **RASSIS** — la valeur a dépassé sa fenêtre mais existe : servie
   **immédiatement**, marquée, et un rafraîchissement part en fond ;
3. **ABSENT** — rien à servir : on construit, **une seule fois**, même si dix
   appelants demandent en même temps.

Le troisième cas attend, et c'est voulu : il n'y a rien d'honnête à servir, et
fabriquer une coquille vide serait l'invention que le produit s'interdit.

## Ce que ce module ne fait pas

Il ne fabrique aucune donnée, ne choisit aucune source et ne juge aucune
qualité. Il transporte ce que le constructeur lui rend, avec l'instant où ça a
été observé et reçu. Un magasin qui « comblerait » une absence serait un
inventeur de chiffres.

Il ne remplace pas non plus `ibkr_scheduler` (file du courtier, priorités,
disjoncteur) ni `source_router` (escalade de sources). Il se place **au-dessus**
d'eux, sur le chemin de la requête, et n'en duplique aucune responsabilité.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field

#: Les six états que toute surface doit savoir distinguer (`QUALITY_STANDARD`
#: §1). Ils décrivent la DONNÉE, jamais l'humeur de l'instrument.
LIVE = 'LIVE'
DELAYED = 'DELAYED'
STALE = 'STALE'
DEMO = 'DEMO'
OFFLINE = 'OFFLINE'
MISSING = 'MISSING'

ETATS = (LIVE, DELAYED, STALE, DEMO, OFFLINE, MISSING)

#: Repos après un échec de reconstruction. Sans lui, une source en panne
#: fabriquerait un fil par visiteur : une panne de fournisseur deviendrait une
#: panne de serveur.
REPOS_APRES_ECHEC_S = 30.0


@dataclass(frozen=True)
class Meta:
    """Ce que vaut la valeur servie — jamais séparable d'elle."""

    etat: str = MISSING
    source: str | None = None
    observe_a: float | None = None      #: instant de l'observation (epoch)
    recu_a: float | None = None         #: instant de réception par Vertex
    age_s: float | None = None
    fraicheur_s: float | None = None    #: fenêtre au-delà de laquelle c'est rassis
    rafraichissement_en_cours: bool = False
    erreur: str | None = None
    qualite: str | None = None

    def vers_dict(self) -> dict:
        return {'etat': self.etat, 'source': self.source,
                'observe_a': self.observe_a, 'recu_a': self.recu_a,
                'age_s': (round(self.age_s, 3) if self.age_s is not None else None),
                'fraicheur_s': self.fraicheur_s,
                'rafraichissement_en_cours': self.rafraichissement_en_cours,
                'erreur': self.erreur, 'qualite': self.qualite}


@dataclass
class _Entree:
    valeur: object = None
    source: str | None = None
    observe_a: float | None = None
    recu_a: float | None = None
    etat_frais: str = LIVE            #: l'état à annoncer TANT QUE c'est frais
    jeton: object = None              #: signature de validité (voir `servir`)
    qualite: str | None = None
    erreur: str | None = None
    chantier: bool = False            #: une reconstruction est en vol
    echec_a: float | None = None
    verrou: threading.Lock = field(default_factory=threading.Lock)


class Magasin:
    """Snapshots datés, servis sans attendre, reconstruits une seule fois.

    Le verrou de construction est PAR CLÉ : deux titres différents se
    construisent en parallèle, mais le même titre jamais deux fois. Un verrou
    global sérialiserait tout le produit derrière le titre le plus lent.
    """

    def __init__(self, nom: str) -> None:
        self.nom = nom
        self._entrees: dict[str, _Entree] = {}
        self._verrou = threading.Lock()
        self.metriques = {'demandes': 0, 'frais': 0, 'rassis': 0, 'absents': 0,
                          'constructions': 0, 'coalescees': 0, 'echecs': 0,
                          'duree_construction_s': []}

    #  ── lecture ───────────────────────────────────────────────────────────
    def _entree(self, clef: str) -> _Entree:
        with self._verrou:
            e = self._entrees.get(clef)
            if e is None:
                e = self._entrees[clef] = _Entree()
            return e

    def servir(self, clef: str, constructeur, *, fraicheur_s: float,
               etat_frais: str = LIVE, plafond_s: float | None = None,
               attendre: bool = True, jeton=None):
        """(valeur, Meta). Ne lève jamais : une route ne doit pas mourir.

        `constructeur()` rend soit la valeur, soit `(valeur, infos)` où `infos`
        peut porter `source`, `observe_a`, `qualite`, `etat`.

        `attendre=False` : quand RIEN n'existe encore, on ne bloque pas — on
        lance la construction en fond et on rend `MISSING` avec
        `rafraichissement_en_cours`. C'est le mode des routes interactives :
        `AUDIT-TOTAL-2026-08-25` P0.1 borne la première réponse froide à 1,5 s,
        et une collecte mesurée à 28–48 s ne tient dans aucun budget.

        `attendre=True` reste le mode des appelants qui n'ont rien d'autre à
        montrer — le graphe de connaissance, par exemple, dont une page entière
        dépend.

        `jeton` : une signature de VALIDITÉ, distincte de l'âge. Certaines
        valeurs ne périment pas avec le temps mais avec leur entrée — le graphe
        de connaissance est déterministe pour un scan donné, et c'est le scan
        qui le périme, pas l'horloge. Quand le jeton change, la valeur devient
        **rassie** : servie tout de suite, marquée, reconstruite en fond.

        Sans ce mécanisme, il aurait fallu changer de CLÉ à chaque scan — et une
        clé neuve est une entrée *absente*, donc une attente, alors qu'un
        graphe parfaitement utilisable était disponible.
        """
        self.metriques['demandes'] += 1
        e = self._entree(clef)
        maintenant = time.time()

        if e.valeur is not None and e.recu_a is not None:
            age = maintenant - e.recu_a
            perime_par_jeton = (jeton is not None and e.jeton != jeton)
            if age <= fraicheur_s and not perime_par_jeton:
                self.metriques['frais'] += 1
                return e.valeur, self._meta(e, age, fraicheur_s, e.etat_frais)
            #  RASSIS : on sert tout de suite et on reconstruit derrière.
            self.metriques['rassis'] += 1
            lance = self._lancer_fond(clef, constructeur, etat_frais, jeton)
            return e.valeur, self._meta(e, age, fraicheur_s, STALE,
                                        chantier=lance or e.chantier)

        #  ABSENT : rien d'honnête à servir.
        self.metriques['absents'] += 1
        if not attendre:
            #  On ne fabrique pas de coquille : on avoue l'absence, on lance la
            #  collecte en fond, et l'appelant sert ce qu'il a déjà par ailleurs.
            lance = self._lancer_fond(clef, constructeur, etat_frais, jeton)
            return None, Meta(etat=OFFLINE if e.erreur else MISSING,
                              erreur=e.erreur, fraicheur_s=fraicheur_s,
                              rafraichissement_en_cours=lance or e.chantier)
        self._construire(clef, constructeur, etat_frais, plafond_s=plafond_s,
                         jeton=jeton)
        e = self._entree(clef)
        if e.valeur is None:
            return None, Meta(etat=OFFLINE if e.erreur else MISSING,
                              erreur=e.erreur, fraicheur_s=fraicheur_s,
                              rafraichissement_en_cours=e.chantier)
        age = time.time() - (e.recu_a or maintenant)
        return e.valeur, self._meta(e, age, fraicheur_s, e.etat_frais)

    def _meta(self, e: _Entree, age: float, fraicheur_s: float, etat: str,
              chantier: bool | None = None) -> Meta:
        return Meta(etat=etat, source=e.source, observe_a=e.observe_a,
                    recu_a=e.recu_a, age_s=age, fraicheur_s=fraicheur_s,
                    rafraichissement_en_cours=(e.chantier if chantier is None
                                               else chantier),
                    erreur=e.erreur, qualite=e.qualite)

    #  ── construction ──────────────────────────────────────────────────────
    def _construire(self, clef: str, constructeur, etat_frais: str,
                    plafond_s: float | None = None, jeton=None) -> None:
        """Sérialisée par clé : les retardataires attendent puis relisent."""
        e = self._entree(clef)
        deja = e.recu_a
        with e.verrou:
            #  Quelqu'un a pu construire pendant qu'on attendait le verrou.
            if (e.recu_a is not None and e.recu_a != deja
                    and (jeton is None or e.jeton == jeton)):
                self.metriques['coalescees'] += 1
                return
            debut = time.monotonic()
            try:
                brut = constructeur()
            except Exception as exc:                          # noqa: BLE001
                #  Un échec n'efface JAMAIS la valeur précédente : servir daté
                #  vaut infiniment mieux qu'une section vide.
                self.metriques['echecs'] += 1
                e.erreur = ('%s: %s' % (type(exc).__name__, exc))[:200]
                e.echec_a = time.time()
                return
            valeur, infos = (brut if isinstance(brut, tuple) and len(brut) == 2
                             else (brut, {}))
            infos = infos or {}
            self.metriques['constructions'] += 1
            self.metriques['duree_construction_s'].append(
                round(time.monotonic() - debut, 3))
            del self.metriques['duree_construction_s'][:-200]
            e.valeur = valeur
            e.source = infos.get('source')
            e.qualite = infos.get('qualite')
            e.observe_a = infos.get('observe_a')
            e.etat_frais = infos.get('etat') or etat_frais
            e.jeton = jeton
            e.recu_a = time.time()
            e.erreur = infos.get('erreur')
            e.echec_a = None

    def _lancer_fond(self, clef: str, constructeur, etat_frais: str,
                     jeton=None) -> bool:
        e = self._entree(clef)
        if e.chantier:
            return False
        if e.echec_a and (time.time() - e.echec_a) < REPOS_APRES_ECHEC_S:
            return False
        e.chantier = True

        def _travail():
            try:
                self._construire(clef, constructeur, etat_frais, jeton=jeton)
            finally:
                e.chantier = False

        threading.Thread(target=_travail, name='snapshot-%s' % self.nom,
                         daemon=True).start()
        return True

    #  ── observabilité ─────────────────────────────────────────────────────
    def statistiques(self) -> dict:
        """De quoi juger le magasin, pas de quoi le flatter.

        `hit_ratio_pct` vaut `None` tant qu'aucune demande n'est arrivée :
        rendre 100 % ferait passer « je n'ai rien mesuré » pour « parfait ».
        """
        m = self.metriques
        d = m['demandes']
        durees = sorted(m['duree_construction_s'])
        return {
            'nom': self.nom, 'entrees': len(self._entrees),
            'demandes': d, 'frais': m['frais'], 'rassis': m['rassis'],
            'absents': m['absents'], 'constructions': m['constructions'],
            'coalescees': m['coalescees'], 'echecs': m['echecs'],
            'hit_ratio_pct': (round((m['frais'] + m['rassis']) / d * 100, 1)
                              if d else None),
            'construction_p50_s': (durees[len(durees) // 2] if durees else None),
            'construction_p95_s': (durees[max(0, int(len(durees) * 0.95) - 1)]
                                   if durees else None),
        }

    def oublier_tout(self) -> None:
        with self._verrou:
            self._entrees.clear()
        for k, v in list(self.metriques.items()):
            self.metriques[k] = [] if isinstance(v, list) else 0
