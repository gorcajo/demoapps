import os


DEFAULTS = {
    'min': 1,
    'max': 1000,
}


def get(key: str) -> int:
    return int(os.getenv(key, DEFAULTS[key]))
