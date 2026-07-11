"""vertex.research.registry — registre des expériences (§29)."""
from .factory import Experiment, LifecycleError


class ExperimentRegistry:
    def __init__(self):
        self._experiments = {}

    def add(self, exp: Experiment):
        if exp.name in self._experiments:
            raise LifecycleError(f'expérience déjà enregistrée: {exp.name}')
        self._experiments[exp.name] = exp

    def get(self, name: str) -> Experiment:
        return self._experiments[name]

    def by_state(self, state: str):
        return [e for e in self._experiments.values() if e.state == state]

    def active_signals(self):
        """Seules les expériences APPROVED produisent des signaux actifs."""
        return self.by_state('APPROVED')
