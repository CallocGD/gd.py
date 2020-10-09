from collections.abc import Mapping, Sequence, Set
from functools import partial
import json

from yarl import URL

from gd.typing import Any, Dict, Optional, TypeVar, Union, cast

__all__ = ("NamedDict", "default", "dump", "dumps", "load", "loads")

T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class NamedDict(Dict[K, V]):
    """Improved version of stdlib dictionary, which implements attribute key access."""

    def copy(self) -> Dict[K, V]:
        return self.__class__(super().copy())

    def __setattr__(self, attr: str, value: V) -> None:
        if attr in self.__dict__:
            self.__dict__[attr] = value
        else:
            self[cast(K, attr)] = value

    def __getattr__(self, attr: str) -> V:
        return self[cast(K, attr)]

    def get(  # type: ignore
        self, key: K, default: Union[Optional[V], T] = None
    ) -> Union[Optional[V], T]:
        try:
            return self[key]
        except KeyError:
            return default


def default(some_object: T) -> Any:
    if hasattr(some_object, "__json__"):
        return some_object.__json__()  # type: ignore

    elif isinstance(some_object, (Sequence, Set)):
        return list(some_object)

    elif isinstance(some_object, Mapping):
        return dict(some_object)

    elif isinstance(some_object, URL):
        return str(some_object)

    else:
        raise TypeError(
            f"Object of type {type(some_object).__name__!r} is not JSON-serializable."
        ) from None


dump = partial(json.dump, default=default)
dumps = partial(json.dumps, default=default)
load = partial(json.load, object_hook=NamedDict)
loads = partial(json.loads, object_hook=NamedDict)