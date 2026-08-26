"""vertex/data_sources/macro_observation.py — UNE SÉRIE MACRO N'EST PAS UN TITRE.

`SOURCES-APIS-OPEN-SOURCE`, section FRED/BLS : « Créer un `MacroObservation`
commun ».

## Pourquoi un modèle distinct d'`Observation`

`storage/point_in_time.Observation` porte un `Instrument` — `conid`, `cik`,
`ticker`, `exchange`, `isin`. Une série `CUUR0000SA0` n'a rien de tout cela ;
la loger dans un champ `ticker` abîmerait l'identité des titres pour un gain
nul, et le premier lecteur qui chercherait un ticker y trouverait un code BLS.

Ce modèle porte donc **le même contrat de provenance**, avec les mêmes noms —
`observed_at`, `available_at`, `received_at`, `provider`, `quality`,
`revision` — pour rester compatible avec `exiger_disponibilite`, qui accepte
tout objet portant `available_at`. Le contrat est partagé ; l'identité ne l'est
pas.

## Le piège que ce modèle rend visible

Une série macro a **deux dates**, et les confondre est un look-ahead :

- `observed_at` : la période que la valeur **décrit** — le CPI de juillet 2026
  décrit juillet ;
- `available_at` : l'instant où elle est devenue **connaissable** — ce même CPI
  est publié à la mi-août.

Utiliser un CPI de juillet en juillet donnerait à un rétrotest une information
que le marché n'avait pas. C'est exactement le défaut que la Phase 2 rend
impossible plutôt qu'improbable, et le critère d'acceptation de la Phase 3 :
« backfill point-in-time sans look-ahead ».

**L'API BLS v1 ne fournit pas la date de publication.** Mesuré le 26 août
2026 : une observation a pour seules clés `footnotes`, `latest`, `period`,
`periodName`, `value`, `year`. `available_at` reste donc **vide**, et
`exiger_disponibilite` refuse ces valeurs comme preuve historique — elles
restent parfaitement utilisables pour décrire le présent.
"""
from __future__ import annotations

import calendar
import datetime as _dt
from dataclasses import dataclass, field

from .models import utc_now_iso

#: Fréquences reconnues des périodes BLS/FRED.
MENSUELLE, TRIMESTRIELLE, ANNUELLE, SEMESTRIELLE = 'M', 'Q', 'A', 'S'


@dataclass
class MacroObservation:
    """Une valeur macro, ce qu'elle décrit, et quand elle fut connaissable.

    `available_at` vide signifie **inconnu**, jamais « immédiatement
    disponible ». Le remplir avec `received_at` — l'erreur naturelle — ferait
    croire qu'une statistique publiée à la mi-août était lisible fin juillet.
    """

    series_id: str
    valeur: float
    unite: str
    frequence: str
    observed_at: str                    # la periode DECRITE
    available_at: str = ''              # quand c'est devenu connaissable
    provider: str = ''
    provider_record_id: str = ''
    libelle: str = ''
    quality: str = 'MEASURED'
    revision: int = 0
    #: Valeur precedente TELLE QUE CONNUE avant revision, quand la source la
    #: donne. `None` = la source ne la donne pas ; jamais une valeur devinee.
    precedente: float | None = None
    notes: tuple = field(default_factory=tuple)
    received_at: str = field(default_factory=utc_now_iso)

    @property
    def disponibilite_connue(self) -> bool:
        return bool(self.available_at)

    def to_dict(self) -> dict:
        return {
            'series_id': self.series_id, 'valeur': self.valeur,
            'unite': self.unite, 'frequence': self.frequence,
            'observed_at': self.observed_at, 'available_at': self.available_at,
            'received_at': self.received_at, 'provider': self.provider,
            'provider_record_id': self.provider_record_id,
            'libelle': self.libelle, 'quality': self.quality,
            'revision': self.revision, 'precedente': self.precedente,
            'notes': list(self.notes),
            'disponibilite_connue': self.disponibilite_connue,
        }


def fin_de_periode(annee: int, periode: str) -> str:
    """La DERNIÈRE date de la période décrite, en ISO.

    `M07` de 2026 → `2026-07-31`. C'est la fin de la période, pas son début :
    une statistique mensuelle décrit le mois **entier**, et la dater au 1er
    laisserait croire qu'elle décrivait déjà le mois à son premier jour.

    Rend `''` pour une période illisible — on ne devine pas une date.
    """
    try:
        annee = int(annee)
    except (TypeError, ValueError):
        return ''
    p = str(periode or '').strip().upper()
    try:
        if p.startswith('M') and p[1:].isdigit():
            mois = int(p[1:])
            if mois == 13:                       # M13 = moyenne annuelle BLS
                return _dt.date(annee, 12, 31).isoformat()
            if not 1 <= mois <= 12:
                return ''
            return _dt.date(annee, mois,
                            calendar.monthrange(annee, mois)[1]).isoformat()
        if p.startswith('Q') and p[1:].isdigit():
            t = int(p[1:])
            if not 1 <= t <= 4:
                return ''
            mois = t * 3
            return _dt.date(annee, mois,
                            calendar.monthrange(annee, mois)[1]).isoformat()
        if p in ('A01', 'A'):
            return _dt.date(annee, 12, 31).isoformat()
        if p.startswith('S') and p[1:].isdigit():
            mois = 6 if p[1:] == '1' else 12
            return _dt.date(annee, mois,
                            calendar.monthrange(annee, mois)[1]).isoformat()
    except ValueError:
        return ''
    return ''


def frequence_de(periode: str) -> str:
    """`M07` → `M`. Rend `''` quand la forme est inconnue."""
    p = str(periode or '').strip().upper()
    if p.startswith('M') and p[1:].isdigit():
        return MENSUELLE
    if p.startswith('Q') and p[1:].isdigit():
        return TRIMESTRIELLE
    if p.startswith('S') and p[1:].isdigit():
        return SEMESTRIELLE
    if p in ('A01', 'A'):
        return ANNUELLE
    return ''


def couverture(observations) -> dict:
    """Ce que ce lot d'observations permet — et ce qu'il interdit.

    Sans ce bloc, un consommateur croirait pouvoir dater ces valeurs dans le
    passé. Le nombre d'observations sans `available_at` est **compté**, pas
    seulement signalé : « certaines » n'aide personne à décider.
    """
    obs = list(observations or [])
    sans = [o for o in obs if not getattr(o, 'available_at', '')]
    return {
        'observations': len(obs),
        'sans_date_de_disponibilite': len(sans),
        'utilisable_comme_preuve_historique': not sans and bool(obs),
        'note': ("une observation sans `available_at` decrit le PRESENT mais ne "
                 "peut pas fonder une preuve sur le passe : la dater a sa "
                 "periode de reference donnerait a un retrotest une information "
                 "que le marche n'avait pas encore"),
        'read_only': True,
    }
