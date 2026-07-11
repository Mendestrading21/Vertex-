"""vertex.ai.prompt_builder — prompts de l'analyste d'investissement (§28)."""
from __future__ import annotations

import json

from .models import ANALYSIS_RESPONSE_SCHEMA, AnalysisRequest
from .strategy_context import build_strategy_context

SYSTEM_ROLE = """Tu es l'analyste d'investissement de Vertex Strategy (lecture seule).
Ton rôle : lire les résultats des moteurs déterministes, interpréter les
contradictions, structurer la thèse, jouer l'avocat du diable, expliquer les
anomalies et comparer les scénarios — en français.

Interdits absolus :
- tu ne calcules JAMAIS toi-même RSI, ATR, Greeks, R:R, corrélations, prix
  théoriques, probabilités ou scores (les moteurs déterministes font foi) ;
- tu ne produis JAMAIS la décision finale (elle appartient au moteur exécutif) ;
- aucun langage de certitude (« garanti », « sans risque », « 99 % sûr ») ;
- aucune notion d'ordre, d'exécution ou de taille de position finale.

Réponds UNIQUEMENT avec un objet JSON respectant exactement ce schéma :
{schema}
"""


def build_system_prompt() -> str:
    schema_desc = {
        'required': {k: t.__name__ for k, t in ANALYSIS_RESPONSE_SCHEMA['required'].items()},
        'optional': {k: t.__name__ for k, t in ANALYSIS_RESPONSE_SCHEMA['optional'].items()},
    }
    return SYSTEM_ROLE.format(schema=json.dumps(schema_desc, ensure_ascii=False, indent=2))


def build_user_prompt(request: AnalysisRequest) -> str:
    parts = [
        f'## Contexte stratégique\n{json.dumps(build_strategy_context(), ensure_ascii=False)}',
        f'## Dossier moteur pour {request.symbol}\n'
        f'{json.dumps(request.packet, ensure_ascii=False, default=str)[:24000]}',
    ]
    if request.user_notes:
        parts.append(f'## Notes de l’utilisateur\n{request.user_notes[:2000]}')
    if request.question:
        parts.append(f'## Question posée\n{request.question[:1000]}')
    else:
        parts.append('## Tâche\nAnalyse complète : thèse, avocat du diable, '
                     'contradictions entre moteurs, lecture des anomalies.')
    return '\n\n'.join(parts)
