import typing as tp
import abc
from dataclasses import dataclass
from librarius.adapters.repositories import PublicationsRepository


@dataclass
class AbstractRepositoryCollection(abc.ABC):
    pass

print(AbstractRepositoryCollection())