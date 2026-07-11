"""vertex.research.reporting — rapport d'une expérience (§29)."""


def experiment_report(exp) -> dict:
    return {'name': exp.name, 'state': exp.state,
            'definition': dict(exp.definition),
            'bias_controls': dict(exp.bias_controls),
            'results': dict(exp.results),
            'history': list(exp.history),
            'is_active_signal': exp.state == 'APPROVED'}
