import typing as tp
from librarius.adapters.repository_contexts import AbstractRepositoryContext


class MemoryRepositoryContext(AbstractRepositoryContext):
    def __init__(self, data: dict = None) -> None:
        self.data = data if data is not None else {}

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def add(self, model) -> None:
        self.data[model.uuid] = model

    def remove(self, model) -> None:
        del self.data[model.uuid]

    def close(self) -> None:
        pass
