"""
vertex/data/macro_calendar.py — CALENDRIER MACRO RÉEL (Fed · NFP · CPI).

Les trois rendez-vous qui font bouger les indices, DATÉS :

- FOMC : dates de réunion PUBLIÉES par la Réserve fédérale (calendrier
  officiel 2026) — la décision tombe le 2ᵉ jour à 14h ET.
- NFP  : rapport emploi — règle officielle BLS : premier vendredi du mois.
- CPI  : inflation — publication BLS vers la mi-mois ; la date exacte varie
  de quelques jours → marquée « date indicative » (approx=True), jamais
  présentée comme certaine.

Aucun réseau : tout est calculé/localisé ici. Sert Market Calendar et la
timeline de l'Options Lab. Analyse only.
"""

from datetime import date, timedelta

# Calendrier FOMC 2026 publié par la Fed (jour de DÉCISION = 2e jour).
FOMC_2026 = [
    date(2026, 1, 28), date(2026, 3, 18), date(2026, 4, 29), date(2026, 6, 17),
    date(2026, 7, 29), date(2026, 9, 16), date(2026, 10, 28), date(2026, 12, 9),
]


def _first_friday(year, month):
    d = date(year, month, 1)
    return d + timedelta(days=(4 - d.weekday()) % 7)


def _mid_month(year, month):
    """CPI : publication BLS ≈ mi-mois (10-15). On pointe le 13, marqué indicatif."""
    return date(year, month, 13)


def events(horizon_days=120, today=None):
    """Les événements macro à venir, triés par date.

    [{date:'YYYY-MM-DD', dte:int, kind:'FOMC'|'NFP'|'CPI', label, importance,
      approx:bool, note}]
    """
    today = today or date.today()
    limit = today + timedelta(days=horizon_days)
    out = []
    for d in FOMC_2026:
        if today <= d <= limit:
            out.append({'kind': 'FOMC', 'date': d.isoformat(), 'approx': False,
                        'label': 'Décision Fed (FOMC)', 'importance': 'haute',
                        'note': 'taux + conférence Powell 14h30 ET — volatilité indices/taux'})
    y, m = today.year, today.month
    for _ in range(max(1, horizon_days // 28) + 1):
        for maker, kind, label, imp, approx, note in (
            (_first_friday, 'NFP', 'Emploi US (NFP)', 'haute', False,
             'premier vendredi 8h30 ET — chocs sur taux et dollar'),
            (_mid_month, 'CPI', 'Inflation US (CPI)', 'haute', True,
             'publication BLS vers la mi-mois (date indicative) — pivot du récit Fed'),
        ):
            d = maker(y, m)
            if today <= d <= limit:
                out.append({'kind': kind, 'date': d.isoformat(), 'approx': approx,
                            'label': label, 'importance': imp, 'note': note})
        m += 1
        if m > 12:
            m, y = 1, y + 1
    for e in out:
        e['dte'] = (date.fromisoformat(e['date']) - today).days
    out.sort(key=lambda e: e['date'])
    return out


__all__ = ['events', 'FOMC_2026']
