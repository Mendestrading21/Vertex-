"""tests/test_audit_fiche_opportunites.py — SKYLER LOT 69 : cohérence fiche ↔ Opportunités.

Volet 4 de l'AUDIT TOTAL, sur les 3 premiers symboles de /api/command
(ACN/AOS/MMM) — verdicts croisés en navigateur réel :

- les DEUX moteurs coexistent et DIVERGENT légitimement (command :
  ACHETER/RENFORCER · Skyler canonique : REFUSER 18-19/40 REFUS_WATCH) —
  et la HIÉRARCHIE EST DITE aux deux endroits : Opportunités affiche les
  deux sections étiquetées (« score Vertex /100 » et « CLASSEMENT SKYLER
  — SCORE CANONIQUE /40 », « un score ne déclenche jamais un ordre ») ;
  la fiche dit « la décision finale unique reste REFUSER — les verdicts
  techniques sont des entrées du moteur exécutif ». Aucun même champ
  affiché avec deux valeurs. SAIN — vérifié, dit ;

- UNE lacune de traçabilité réelle : les cartes SHORTLIST affichaient le
  score nu (« 81 », « 74 », « 73 ») sans son échelle, alors que la
  dominante dit « 84 /100 ». Corrigé : le score des cartes shortlist
  porte « /100 » — tout score affiché porte son échelle, partout.

Shell visible → SW v122 → v123.
"""
import re

PAGE = 'vertex/ui/pages/opportunities_page.py'


def _src():
    return open(PAGE, encoding='utf-8').read()


def test_shortlist_score_carries_scale():
    line = next((l for l in _src().splitlines() if 'vx-op-tk-score' in l), None)
    assert line, 'score de carte shortlist introuvable'
    assert '/100' in line, 'le score shortlist doit porter son échelle /100'


def test_service_worker_bumped_to_at_least_v123():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 123
    assert 'td-shell-v122' not in body
