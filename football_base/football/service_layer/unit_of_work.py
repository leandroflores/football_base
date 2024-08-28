import abc

from football_base.db import InMemoryDataBase
from football_base.football.adapters import repository

MEMORY_BD: InMemoryDataBase = InMemoryDataBase()

class AbstractUnitOfWork(abc.ABC):
    repository: repository.AbstractRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self
    
    def __exit__(self, *args) -> None:
        self.rollback()

    @abc.abstractmethod
    def commit(self) -> None:
        ...

    @abc.abstractmethod
    def rollback(self) -> None:
        ...

class InMemoryUnitOfWork(AbstractUnitOfWork):

    def __init__(self, database: InMemoryDataBase = MEMORY_BD) -> None:
        self.database = database
        super().__init__()

    def __enter__(self) -> "AbstractUnitOfWork":
        self.repository = repository.InMemoryRepository(self.database)
        return super().__enter__()

    def __exit__(self, *args):
        return super().__exit__(*args)

    def commit(self):
        ...

    def rollback(self):
        ...