# VERTEX TRACKING ENGINE — moteur de suivi analytique (§14-18)

> « Suivre » crée un suivi **hypothétique et horodaté** — jamais une position
> réelle, jamais un gain encaissé. Livré et **prouvé** (tests + navigateur).

## Principe (honnêteté)
Un suivi mesure la performance d'une idée **depuis l'instant où elle est
marquée**, contre SPY. Tout gain est étiqueté « **Rendement hypothétique depuis
le suivi** ». On n'utilise jamais l'ask comme prix d'achat simulé silencieux ;
une référence absente donne le statut **DATA_REQUIRED** (jamais un prix inventé).

## Modules (`vertex/tracking/`)
- **models.py** — modèle canonique (`is_hypothetical` toujours vrai), statuts
  ACTIVE / STOPPED / EXPIRED / DATA_REQUIRED, types de référence
  MID / LAST / CLOSE / MARK / FALLBACK.
- **reference_price.py** — choix honnête : action = mid → last → close (marché
  fermé) → fallback identifié ; option = mid → mark → last (avec avertissement)
  → DATA_REQUIRED. Jamais l'ask seul.
- **returns.py** — rendement simple, MAE/MFE, drawdown depuis le plus haut,
  ajustement de split. None si donnée absente.
- **benchmark.py** — rendement SPY sur la fenêtre + alpha depuis le suivi.
- **performance.py** — synthèse (rendement, SPY, alpha, MFE/MAE, drawdown,
  durée, changement de décision/score) + étiquette hypothétique + limites.
- **repository.py** — persistance `tracking.json` (gitignorée), CRUD,
  snapshots horodatés, arrêt (gèle le résultat, **conserve l'historique**),
  réactivation (**nouvel identifiant**, ne modifie pas l'ancien). Déterministe :
  identifiants/horodatages fournis par l'appelant.

## API (§33) — `vertex/app/routes/tracking_api.py`, lecture seule
| route | rôle |
|---|---|
| `POST /api/tracking` | crée un suivi (prix de référence honnête depuis le scan / le body option) |
| `GET /api/tracking` | liste + résumé |
| `GET /api/tracking/summary` | compteurs |
| `GET /api/tracking/<id>` | détail |
| `PATCH /api/tracking/<id>` | met à jour décision/score/thèse |
| `GET /api/tracking/<id>/performance` | performance depuis le suivi (vs SPY) |
| `GET /api/tracking/<id>/history` | snapshots + résultat final |
| `POST /api/tracking/<id>/stop` | arrête (gel + historique) |
| `POST /api/tracking/<id>/restart` | réactive comme nouveau suivi |

## Page `/tracking` (§17)
Approfondissement du **Portefeuille** (le nav reste à huit espaces ; entrée
« Suivis → » depuis le Portefeuille). Affiche : résumé, **Suivis actifs**
(référence + type, actuel, rendement hypo., SPY, alpha, MFE/MAE, décision
initiale), et **Suivis clôturés** (historique). Bannière « Rendements 100 %
hypothétiques ». Dates **absolues** d'abord (§21).

## Automatisations (§30)
Jobs enregistrés au scheduler : `TRACKING_REFRESH`, `TRACKING_SNAPSHOT`,
`EOD_TRACKING_SNAPSHOT`.

## Preuve
- **767 tests OK** (+23 : 21 `tests/test_tracking.py` couvrant les cas nommés
  §34 + garde-fous page/API/no-order).
- Flux réel vérifié sur serveur démo : ACN → référence 198,00 (LAST), performance
  « Rendement hypothétique depuis le suivi », arrêt qui gèle le résultat.
- Navigateur Chromium `/tracking` → **0 erreur console** ; « réf. requise »
  honnête pour les titres sans prix.
- READONLY : aucun chemin d'ordre dans `vertex/tracking/*` ni l'API (testé).
  `tracking.json` gitignoré (donnée runtime). Service worker `td-shell-v12`.

## Limites restantes (honnêteté §2)
- Total return (dividendes/splits) séparé du price return : le price return est
  livré ; le total return complet reste à câbler quand la donnée dividende est
  disponible.
- Suivi d'options : la marque actuelle doit être fournie (pas de flux Greeks
  live sans IBKR) ; theta cumulé / évolution IV/delta non encore calculés.
- Bouton « Suivre » intégré depuis le Portefeuille ; les points d'entrée
  Opportunités/Analyse/Options restent à ajouter.
