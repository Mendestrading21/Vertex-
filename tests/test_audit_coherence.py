"""tests/test_audit_coherence.py — SKYLER LOT 66 : audit total, volet cohérence.

AUDIT TOTAL (demande utilisateur : « tout doit être cohérent, chaque
chiffre ») — volets exécutés en réel :

- 137 routes GET balayées : 94×200, 41 redirections héritées, un seul
  400 STRUCTURÉ (/api/options/simulate sans paramètres), AUCUN 5xx ;
- boutons : 0 non câblé sur les 8 pages ; 0 erreur console ;
- INCOHÉRENCE RÉELLE trouvée : la tuile « Breadth » du briefing affichait
  `above50` (50 %) SANS étiquette, alors que la page Marchés vers
  laquelle elle pointe affiche « Breadth >MM200 » (45 %) — et le diff
  « depuis ta dernière visite » du MÊME fichier comparait `above200` :
  la tuile était incohérente avec son propre historique.

Corrigé : `breadthOf` canonicalise sur `above200` (la métrique de la
grammaire de régime et de Marchés), repli `above50` — et la TUILE PORTE
L'ÉTIQUETTE de la métrique réellement affichée (« Breadth >MM200 » ou
« Breadth >MM50 ») : le même chiffre, nommé pareil, partout.

Shell visible → SW v121 → v122.
"""
import re

PAGE = 'vertex/ui/pages/briefing.py'


def _src():
    return open(PAGE, encoding='utf-8').read()


def test_breadth_prefers_canonical_mm200():
    src = _src()
    body = src[src.index('function breadthOf'):src.index('function vCls')]
    # above200 doit être essayé AVANT above50 (métrique canonique)
    assert body.index('above200') < body.index('above50')


def test_breadth_tile_labels_its_metric():
    src = _src()
    assert 'MM200' in src
    # plus jamais « Breadth » nu : l'étiquette est construite avec la métrique
    assert "kpiTile('Breadth'," not in src
    assert "kpiTile('Breadth'+(" in src


def test_guarded_literals_intact():
    src = _src()
    assert "kpiTile('VIX',vixHtml,''" in src
    assert 'Aucun historique de comparaison disponible' in src


def test_service_worker_bumped_to_at_least_v122():
    import terminal
    body = terminal.app.test_client().get('/sw.js').get_data(as_text=True)
    m = re.search(r"td-shell-v(\d+)", body)
    assert m and int(m.group(1)) >= 122
    assert 'td-shell-v121' not in body
