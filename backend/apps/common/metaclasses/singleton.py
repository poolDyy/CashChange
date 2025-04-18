from threading import Lock
from typing import Any


__all__ = ['SingletonMeta']


class SingletonMeta(type):
    """Потокобезопасный Singleton."""

    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
