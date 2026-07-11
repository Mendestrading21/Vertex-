"""vertex.observability.logging — journalisation structurée (sans secret)."""
import logging

REDACTED_KEYS = ('secret', 'api_key', 'token', 'password', 'authorization')


def get_logger(name: str = 'vertex') -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def redact(payload: dict) -> dict:
    """Masque toute clé sensible avant journalisation."""
    return {k: ('***' if any(s in k.lower() for s in REDACTED_KEYS) else v)
            for k, v in (payload or {}).items()}
