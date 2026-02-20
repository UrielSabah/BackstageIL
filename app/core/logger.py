import logging

_configured_logger_names: set[str] = set()


def setup_logger(name: str) -> logging.Logger:
    """Return a logger with a single StreamHandler. Configures each name only once."""
    logger = logging.getLogger(name)
    if name not in _configured_logger_names:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("[%(asctime)s] %(levelname)s in %(name)s: %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        _configured_logger_names.add(name)
    return logger