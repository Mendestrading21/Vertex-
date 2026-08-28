"""vertex.engines.advice — L'AUTORITÉ DE CONSEIL A UN NOM (lot 10).

## Pourquoi une façade, et pas une fusion

Trois décideurs coexistaient sans hiérarchie déclarée :

- `decide.py` — verdicts du scan (ACHETER FORT … ÉVITER), appelé par le
  monolithe ;
- `skyler_core.decide` — le packet complet de la fiche : score40, hard
  gates, scénarios, audit trail, `ENGINE_VERSION` ;
- `executive.decide` — Strategy OS, sur le packet et le profil.

Le contrat du skill exige UNE autorité : `AdviceEngine.evaluate(snapshot)
→ AdviceResult`. Mais unifier les SÉMANTIQUES changerait des verdicts — et
un verdict ne change que sur décision humaine, jamais dans un lot de
convergence. Cette façade fait donc l'autre moitié du travail : elle NOMME
l'autorité, fige sa signature, et DÉLÈGUE strictement au décideur du packet
— le seul des trois qui porte hard gates, audit trail et version.

Les deux autres restent des producteurs : `decide.py` produit le verdict de
scan qui entre dans le packet comme PREUVE (`detail['verdict']`), et
`executive` consomme le packet en aval. Leur retrait éventuel appartient à
un lot moteur dédié, avec golden cases et validation humaine.

## Contrat

- `evaluate(snapshot)` où `snapshot = {'symbol', 'detail', ...contextes}` ;
- rend l'`AdviceResult` du décideur du packet, PLUS `advice_provenance`
  (moteur + version) — un conseil sans version n'est pas auditable ;
- un snapshot vide rend un refus honnête (`decision: None`), jamais un
  verdict fabriqué.

⛔ ANALYSE SEULEMENT — aucun ordre, aucune promesse.
"""
from __future__ import annotations

import hashlib
import json

from vertex.engines import skyler_core as _sk

#: Les contextes que le décideur du packet accepte, dans son ordre nommé.
_CONTEXTES = ('market', 'events', 'anomaly', 'as_of', 'demo', 'options_ctx',
              'portfolio_ctx', 'red_team', 'calibration', 'data_quality_ctx',
              'reconciliation_ctx', 'fundamental_ctx')


def empreinte_snapshot(snapshot: dict | None) -> str:
    """Empreinte sha256 du snapshot d'entrée (JSON canonique trié).

    Contrôle 074 : c'est elle qui relie un conseil à SON entrée — deux
    snapshots identiques ont la même empreinte, tout champ changé la change.
    """
    canonique = json.dumps(snapshot or {}, ensure_ascii=False,
                           sort_keys=True, default=str)
    return hashlib.sha256(canonique.encode('utf-8')).hexdigest()


class AdviceEngine:
    """Autorité unique de conseil. Une classe-espace-de-noms, pas un état."""

    @staticmethod
    def evaluate(snapshot: dict | None) -> dict:
        snapshot = snapshot or {}
        sym = str(snapshot.get('symbol') or '').upper()
        detail = snapshot.get('detail')
        if not sym or not isinstance(detail, dict):
            #  Sans symbole (ou detail difforme), il n'y a rien à évaluer.
            #  Mais un detail VIDE part bien au décideur : c'est LUI qui sait
            #  rendre le refus structuré « données insuffisantes » (note
            #  READONLY, générateur, audit) — six bancs de fuzz épinglent
            #  cette forme, et la façade ne doit pas la réinventer en plus
            #  pauvre.
            return {'decision': None,
                    'reason': 'snapshot sans symbole — aucun conseil possible',
                    'advice_provenance': {
                        'engine': 'skyler_core',
                        'version': _sk.ENGINE_VERSION,
                        'via': 'AdviceEngine.evaluate',
                        'snapshot_fingerprint': empreinte_snapshot(snapshot)}}
        kwargs = {k: snapshot[k] for k in _CONTEXTES if k in snapshot}
        result = _sk.decide(sym, detail, **kwargs)
        result['advice_provenance'] = {
            'engine': 'skyler_core',
            'version': _sk.ENGINE_VERSION,
            'via': 'AdviceEngine.evaluate',
            'snapshot_fingerprint': empreinte_snapshot(snapshot)}
        return result


def rejouer(snapshot: dict | None, conseil_enregistre: dict) -> dict:
    """Rejoue un conseil depuis son snapshot et PROUVE la reproduction.

    Contrôle 074 de l'audit-150. Deux vérifications distinctes :
    1. `empreinte_verifiee` — le conseil enregistré vient-il bien de CE
       snapshot ? (comparaison d'empreintes d'entrée) ;
    2. `identique` + `differences` — la ré-évaluation reproduit-elle le
       conseil champ par champ (JSON canonique) ? La provenance est comparée
       hors empreinte (elle référence l'entrée, déjà couverte par 1).
    Aucun champ n'est déclaré « volatil » : le décideur est mesuré
    bit-identique ; toute divergence future sera VISIBLE ici, jamais
    silencieusement tolérée.
    """
    emp = empreinte_snapshot(snapshot)
    prov = (conseil_enregistre or {}).get('advice_provenance') or {}
    empreinte_verifiee = prov.get('snapshot_fingerprint') == emp

    frais = AdviceEngine.evaluate(snapshot)
    differences = []

    def _canon(v):
        return json.dumps(v, ensure_ascii=False, sort_keys=True, default=str)

    cles = sorted(set(frais) | set(conseil_enregistre or {}))
    for k in cles:
        a, b = frais.get(k), (conseil_enregistre or {}).get(k)
        if k == 'advice_provenance':
            a = {x: y for x, y in (a or {}).items() if x != 'snapshot_fingerprint'}
            b = {x: y for x, y in (b or {}).items() if x != 'snapshot_fingerprint'}
        if _canon(a) != _canon(b):
            differences.append(k)
    return {'identique': not differences,
            'differences': differences,
            'empreinte_verifiee': empreinte_verifiee,
            'empreinte_snapshot': emp,
            'read_only': True,
            'note': ('replay déterministe — preuve de reproduction, jamais '
                     'un nouveau conseil')}


__all__ = ['AdviceEngine', 'empreinte_snapshot', 'rejouer']
