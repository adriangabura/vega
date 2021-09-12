import typing as tp
from librarius.adapters.repository_contexts import AbstractRepositoryContext

if tp.TYPE_CHECKING:
    from librarius.adapters.queries import AbstractQueryConstructor


class MemoryRepositoryContext(AbstractRepositoryContext):
    def __init__(self, data: dict = None):
        super().__init__()
        self.data = data if data is not None else {}

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass

    def query(self, query_object: "AbstractQueryConstructor"):
        pass

    def add(self, model) -> None:
        self.data[model.uuid] = model

    def remove(self, model) -> None:
        del self.data[model.uuid]

