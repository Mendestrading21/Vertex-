"""vertex.research.robustness — PSR/DSR/PBO et sensibilité (§29)."""
from vertex.validation.out_of_sample import build as validate_equity  # noqa: F401


def parameter_sensitivity(run_fn, base_params: dict, bumps: dict) -> dict:
    """Réévalue run_fn(params) autour des paramètres de base — une stratégie
    dont le résultat s'effondre au moindre bump est sur-optimisée."""
    base = run_fn(base_params)
    variants = {}
    for key, values in bumps.items():
        variants[key] = []
        for v in values:
            params = dict(base_params)
            params[key] = v
            variants[key].append({'value': v, 'result': run_fn(params)})
    results = [r['result'] for rs in variants.values() for r in rs
               if isinstance(r['result'], (int, float))]
    fragile = bool(results) and isinstance(base, (int, float)) and base > 0 \
        and any(r < base * 0.3 for r in results)
    return {'base': base, 'variants': variants, 'fragile': fragile}
