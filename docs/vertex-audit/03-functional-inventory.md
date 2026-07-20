# 03 — Inventaire fonctionnel (par espace) & anti-fausse-fonctionnalité

Pour chaque espace : la (les) question(s) de la boucle de décision auxquelles il répond, l'état, et les risques
de **fausse fonctionnalité** (§25 : bouton sans handler, lien `#`, filtre inopérant, statut live menteur, graphe
décoratif, mock silencieux). À valider bloc par bloc via `vertex-product-auditor`.

## Boucle de décision (rappel)
OBSERVER → COMPRENDRE → DÉTECTER → ÉVALUER → DÉCIDER → **PRÉPARER** (jamais exécuter) → SURVEILLER → MESURER → APPRENDRE.

## Par espace
| Espace | Questions couvertes | État | À vérifier / findings |
|---|---|---|---|
| **Dashboard** `/` | Que se passe-t-il ? régime, breadth, opportunités, alertes, brief | riche (briefing.py) | densité à maîtriser ; chaque bloc = une question (pas « parce que dispo ») |
| **Opportunités** | Quelle opportunité ? screener/options/anomalies/calendar | fonctionnel | FCT-01 : filtres screener doivent réellement filtrer (à prouver) |
| **Portefeuille** | Quelle exposition/risque ? positions, greeks, watchlist | fonctionnel | provenance des valeurs (IBKR vs estimé) à afficher partout |
| **Analyse** `/analysis/<sym>` | Pourquoi ? fiche canonique (physique, scorecard, fondamentaux) | mûr (récemment enrichi) | payload fiche ~8 Mo (perf, voir `10`) ; vides forcés corrigés |
| **Options** | Quels scénarios ? chaîne, IV/skew, greaks, scénarios, events | fonctionnel | RT-01 collision route ; greeks broker vs `MODEL_ESTIMATE` étiquetés |
| **Performance** | Quel résultat ? overview, journal, track-record, learnings | fonctionnel | chiffres réels seulement ; pas de perf inventée |
| **Intelligence** | Quelle confiance ? analyst (IA), comité, stratégie, impacts, recherche, mémoire | fonctionnel | IA lecture seule (17 outils d'ordre interdits) ; « je ne sais pas » possible |
| **Système** | État réel ? connections, data, automations, settings, archive | fonctionnel | statut IBKR = socket réel, pas flag config (voir `09`) |

## Findings transverses
- **FCT-01 (P2)** — Auditer chaque bouton/onglet/filtre : handler présent, action réelle, état résultant visible.
  Méthode : `vertex-product-auditor` page par page + capture Playwright + `/api/client-log`=0.
- **FCT-02 (P1)** — Aucun libellé/CTA ne doit suggérer une **transmission d'ordre** (invariant lecture seule).
  Le Desk/Préparation produit un **ticket à coller** ; vocabulaire : « préparer », « simuler », jamais « envoyer ».
- **FCT-03 (P2)** — Cohérence de vocabulaire (§27) : signal ≠ recommandation ≠ décision ≠ ordre. Vérifier via
  `__VXVOCAB` (`recommendation.py`) qu'un même concept = un même mot dans code/UI.

Détail page par page à produire dans `docs/vertex-audit/pages/<route>.md` (gabarit `templates/page-audit-template.md`).
