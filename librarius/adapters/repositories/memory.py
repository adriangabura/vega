import typing as tp

from librarius.domain.models import Entity
from librarius.types import Reference
from librarius.adapters.repositories import AbstractRepository

if tp.TYPE_CHECKING:
    from librarius.types import Reference
    from librarius.domain.models import Entity
    from librarius.adapters.repositories.contexts import MemoryRepositoryContext


class MemoryRepository(AbstractRepository):
    name: tp.ClassVar[str] = "memory"

    def __init__(self, context: "MemoryRepositoryContext"):
        super().__init__(context)

    def find(self, reference: "Reference") -> tp.Union["Entity", None]:
        if reference in self.context.data:
            return self.context.data.get(reference, None)

    def add(self, entity: "Entity") -> bool:
        reference = str(entity.uuid)
        if self.context.data.get(reference, None):
            return False
        else:
            self.context.data[reference] = entity
            return True

    def remove(self, reference: "Reference") -> bool:
        try:
            del self.context.data[reference]
        except KeyError as error:
            print(error)
            return False
        else:
            return True
