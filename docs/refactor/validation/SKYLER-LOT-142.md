# SKYLER V2 — LOT 142 : passe n°17 — fraîcheur par domaine en barres de staleness (Système)

Date : 2026-08-07 · Branche : `agent/skyler-v2-lot-142`
(base : `integration/vertex-skyler-v2` @ `de75b48`, fraîchement fetchée).
**DIRECTIVE ESTHÉTIQUE MAXIMALE.** Moteurs INTACTS — diff =
system_page.py + SW + gardiens + docs.

## 1. Diagnostic (captures AVANT, /system?view=data & automations)

Automatisations : table des jobs déjà correcte (badges + honnêteté
« jamais exécuté »). Données : la table FRAÎCHEUR PAR DOMAINE
affichait l'ÂGE en texte nu — « 8 s » et « 20477 min » se lisaient
avec le même poids visuel alors que l'un est frais et l'autre
rassis de 14 jours.

## 2. Amélioration (fraîcheur, system_page.py)

```text
l'âge devient une MINI-BARRE de verre de STALENESS relative
  (échelle = âge max connu parmi les domaines) : les domaines
  frais restent discrets, LE PLUS RASSIS (companies, 20 481 min)
  saute aux yeux en pleine barre negative
couleur par état : frais → positive, différé → warning, hors
  ligne → negative · sans âge connu → pas de barre (honnête —
  garde d.age_s == null AVANT Number(), car Number(null) = 0)
color-mix sur tokens uniquement — AUCUN littéral couleur nouveau
```

SW `td-shell-v150` → `td-shell-v151` + 4 gardiens.

## 3. Preuves

```text
python -m pytest tests/ -q → 1984 passed, 2 skipped
tools/rc_short_audit.js → GO — 0 défaut (SW v151)
tools/user_journeys.js → 14 étapes, 0 échec, 0 erreur console
Responsive 8 × 3 → 0 débordement, 0 erreur
Captures desktop 1440 AVANT/APRÈS envoyées (vue Données)
```

## 4. Suite

LOT 143 : passe n°18 (dernières poches restantes, puis nouvelle
tournée de vérification transversale des 8 espaces).
