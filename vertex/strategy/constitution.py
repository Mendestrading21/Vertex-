"""vertex.strategy.constitution — chargement et versioning du profil stratégique.

Règles :
- La constitution active est le fichier ``profiles/vertex_strategy_v<N>.json``
  de version la plus élevée.
- Aucune modification automatique : ``propose_new_version`` écrit un fichier de
  version N+1 SEULEMENT si ``confirm=True`` est passé explicitement par un
  humain, et l'ancienne version est toujours conservée (restauration possible).
- Les classes de validation garantissent que tout profil chargé respecte les
  invariants produit (décisions autorisées, bornes de portefeuille, options
  long-only).
"""
from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

PROFILES_DIR = Path(__file__).resolve().parent / 'profiles'
STRATEGY_ID_RE = re.compile(r'^vertex_strategy_v(\d+)$')

ALLOWED_FINAL_DECISIONS = ('ACHETER', 'RENFORCER', 'ATTENDRE', 'REDUIRE', 'REFUSER')

# Libellé + polarité sémantique CANONIQUES de chaque décision finale — SOURCE UNIQUE.
# La polarité applique le contrat visuel Black Glass (« zéro bleu ») : positif → vert,
# prudence → ambre, négatif/risque → rouge. Tout affichage de verdict (badge, pill,
# __VXVOCAB) dérive d'ici : un même verdict = un même mot + une même couleur PARTOUT.
FINAL_DECISION_TONES = {
    'ACHETER':   ('Acheter', 'green'),
    'RENFORCER': ('Renforcer', 'green'),
    'ATTENDRE':  ('Attendre', 'amber'),
    'REDUIRE':   ('Réduire', 'red'),
    'REFUSER':   ('Refuser', 'red'),
}
assert set(FINAL_DECISION_TONES) == set(ALLOWED_FINAL_DECISIONS), \
    'FINAL_DECISION_TONES doit couvrir EXACTEMENT les décisions autorisées'

ANALYSIS_ORDER = (
    'FUNDAMENTAL',
    'CATALYSTS',
    'TECHNICAL_TIMING',
    'SENTIMENT_POSITIONING',
    'PORTFOLIO_COMPATIBILITY',
    'RISK',
    'FINAL_DECISION',
)

# Ce qui est interdit quelle que soit la version du profil (invariant produit).
FORBIDDEN_OPTION_FEATURES = (
    'short_options', 'covered_calls', 'protective_puts',
    'credit_spreads', 'naked_options', 'automatic_execution',
)


class ConstitutionError(ValueError):
    """Profil stratégique invalide ou opération de versioning refusée."""


@dataclass(frozen=True)
class DteRules:
    absolute_minimum: int
    preferred_minimum: int
    preferred_maximum: int
    absolute_maximum: int

    def validate(self) -> None:
        seq = (self.absolute_minimum, self.preferred_minimum,
               self.preferred_maximum, self.absolute_maximum)
        if list(seq) != sorted(seq) or self.absolute_minimum <= 0:
            raise ConstitutionError(f'bornes DTE incohérentes: {seq}')


@dataclass(frozen=True)
class HoldingRules:
    minimum: int
    preferred_minimum: int
    preferred_maximum: int
    maximum: int

    def validate(self) -> None:
        seq = (self.minimum, self.preferred_minimum, self.preferred_maximum, self.maximum)
        if list(seq) != sorted(seq) or self.minimum <= 0:
            raise ConstitutionError(f'durées de détention incohérentes: {seq}')


@dataclass(frozen=True)
class StrategyProfile:
    """Vue validée et immuable de la constitution."""
    strategy_id: str
    display_name: str
    version: int
    style: str
    benchmark: str
    portfolio_min_positions: int
    portfolio_max_positions: int
    portfolio_max_drawdown_pct: float
    stock_max_drawdown_pct: float
    max_stock_weight_pct: float
    max_simultaneous_options: int
    analysis_order: tuple
    allowed_final_decisions: tuple
    options_profile: dict = field(default_factory=dict)
    raw: dict = field(default_factory=dict, repr=False)

    @property
    def dte(self) -> DteRules:
        d = self.options_profile.get('dte', {})
        return DteRules(d.get('absolute_minimum', 60), d.get('preferred_minimum', 90),
                        d.get('preferred_maximum', 210), d.get('absolute_maximum', 270))

    @property
    def holding(self) -> HoldingRules:
        h = self.options_profile.get('holding_period_days', {})
        return HoldingRules(h.get('minimum', 2), h.get('preferred_minimum', 5),
                            h.get('preferred_maximum', 20), h.get('maximum', 28))

    def category(self, name: str) -> dict:
        return dict(self.options_profile.get('categories', {}).get(name, {}))


def _validate_raw(raw: dict) -> None:
    sid = raw.get('strategy_id', '')
    if not STRATEGY_ID_RE.match(sid):
        raise ConstitutionError(f'strategy_id invalide: {sid!r}')
    version = raw.get('version')
    if int(STRATEGY_ID_RE.match(sid).group(1)) != version:
        raise ConstitutionError('version incohérente entre strategy_id et champ version')
    if raw.get('target_is_guarantee') is not False:
        raise ConstitutionError('target_is_guarantee doit être false — aucune promesse de performance')
    decisions = tuple(raw.get('allowed_final_decisions', ()))
    if set(decisions) != set(ALLOWED_FINAL_DECISIONS):
        raise ConstitutionError(f'décisions finales non conformes: {decisions}')
    order = tuple(raw.get('analysis_order', ()))
    if order != ANALYSIS_ORDER:
        raise ConstitutionError(f"ordre d'analyse non conforme: {order}")
    tgt = raw.get('portfolio_target_positions', {})
    if not (1 <= int(tgt.get('minimum', 0)) <= int(tgt.get('maximum', 0))):
        raise ConstitutionError('portfolio_target_positions invalide')
    if raw.get('portfolio_max_drawdown_pct', 0) >= 0 or raw.get('stock_max_drawdown_pct', 0) >= 0:
        raise ConstitutionError('les drawdowns max doivent être négatifs')
    if int(raw.get('max_simultaneous_options', 0)) < 1:
        raise ConstitutionError('max_simultaneous_options doit être >= 1')
    opt = raw.get('options_profile', {})
    if opt:
        if opt.get('primary_direction') != 'LONG_CALL':
            raise ConstitutionError('primary_direction doit rester LONG_CALL')
        for feature in FORBIDDEN_OPTION_FEATURES:
            if opt.get(feature):
                raise ConstitutionError(f'fonctionnalité options interdite activée: {feature}')
        dte = opt.get('dte', {})
        DteRules(dte.get('absolute_minimum', 60), dte.get('preferred_minimum', 90),
                 dte.get('preferred_maximum', 210), dte.get('absolute_maximum', 270)).validate()
        hold = opt.get('holding_period_days', {})
        HoldingRules(hold.get('minimum', 2), hold.get('preferred_minimum', 5),
                     hold.get('preferred_maximum', 20), hold.get('maximum', 28)).validate()


def _profile_from_raw(raw: dict) -> StrategyProfile:
    _validate_raw(raw)
    tgt = raw['portfolio_target_positions']
    return StrategyProfile(
        strategy_id=raw['strategy_id'],
        display_name=raw['display_name'],
        version=int(raw['version']),
        style=raw.get('style', ''),
        benchmark=raw.get('benchmark', 'SPY'),
        portfolio_min_positions=int(tgt['minimum']),
        portfolio_max_positions=int(tgt['maximum']),
        portfolio_max_drawdown_pct=float(raw['portfolio_max_drawdown_pct']),
        stock_max_drawdown_pct=float(raw['stock_max_drawdown_pct']),
        max_stock_weight_pct=float(raw.get('max_stock_weight_pct', 15)),
        max_simultaneous_options=int(raw.get('max_simultaneous_options', 3)),
        analysis_order=tuple(raw['analysis_order']),
        allowed_final_decisions=tuple(raw['allowed_final_decisions']),
        options_profile=copy.deepcopy(raw.get('options_profile', {})),
        raw=copy.deepcopy(raw),
    )


def list_versions(profiles_dir: Path = PROFILES_DIR) -> list[int]:
    versions = []
    for p in sorted(profiles_dir.glob('vertex_strategy_v*.json')):
        m = STRATEGY_ID_RE.match(p.stem)
        if m:
            versions.append(int(m.group(1)))
    return sorted(versions)


def load_profile(version: int | None = None, profiles_dir: Path = PROFILES_DIR) -> StrategyProfile:
    """Charge la constitution (dernière version par défaut), validée."""
    versions = list_versions(profiles_dir)
    if not versions:
        raise ConstitutionError(f'aucun profil dans {profiles_dir}')
    version = versions[-1] if version is None else version
    if version not in versions:
        raise ConstitutionError(f'version {version} introuvable (disponibles: {versions})')
    raw = json.loads((profiles_dir / f'vertex_strategy_v{version}.json').read_text(encoding='utf-8'))
    return _profile_from_raw(raw)


def diff_profiles(old: dict, new: dict, prefix: str = '') -> list[str]:
    """Différences lisibles entre deux profils (pour confirmation humaine)."""
    changes = []
    keys = sorted(set(old) | set(new))
    for k in keys:
        path = f'{prefix}{k}'
        if k not in old:
            changes.append(f'+ {path} = {new[k]!r}')
        elif k not in new:
            changes.append(f'- {path} (supprimé, valait {old[k]!r})')
        elif isinstance(old[k], dict) and isinstance(new[k], dict):
            changes.extend(diff_profiles(old[k], new[k], prefix=f'{path}.'))
        elif old[k] != new[k]:
            changes.append(f'~ {path} : {old[k]!r} → {new[k]!r}')
    return changes


def propose_new_version(changes: dict, confirm: bool = False,
                        profiles_dir: Path = PROFILES_DIR) -> dict:
    """Propose une version N+1 de la constitution.

    Sans ``confirm=True`` (action humaine explicite), RIEN n'est écrit :
    la fonction retourne seulement le diff. L'ancienne version reste sur
    disque dans tous les cas — restauration = recharger l'ancienne version.
    """
    current = load_profile(profiles_dir=profiles_dir)
    new_raw = copy.deepcopy(current.raw)
    _deep_update(new_raw, changes)
    new_version = current.version + 1
    new_raw['version'] = new_version
    new_raw['strategy_id'] = f'vertex_strategy_v{new_version}'
    _validate_raw(new_raw)  # une proposition invalide est refusée avant tout écrit
    diff = diff_profiles(current.raw, new_raw)
    result = {'current_version': current.version, 'proposed_version': new_version,
              'diff': diff, 'written': False}
    if confirm:
        path = profiles_dir / f'vertex_strategy_v{new_version}.json'
        path.write_text(json.dumps(new_raw, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        result['written'] = True
        result['path'] = str(path)
    return result


def _deep_update(base: dict, patch: dict) -> None:
    for k, v in patch.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            _deep_update(base[k], v)
        else:
            base[k] = v
