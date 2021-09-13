import typing as tp
from librarius.adapters.repository_contexts import AbstractRepositoryContext


class MemoryRepositoryContext(AbstractRepositoryContext):
    def __init__(self, data: dict = None) -> None:
        self.data = data if data is not None else {}

    def commit(self) -> tp.NoReturn:
        pass

    def rollback(self) -> tp.NoReturn:
        pass

    def add(self, model) -> tp.NoReturn:
        self.data[model.uuid] = model

    def remove(self, model) -> tp.NoReturn:
        del self.data[model.uuid]

    def close(self) -> tp.NoReturn:
        pass
