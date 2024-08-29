import abc

from football_base.config import get_postgres_url
from football_base.db import InMemoryDataBase
from football_base.football.adapters import repository

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MEMORY_BD: InMemoryDataBase = InMemoryDataBase()
SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        get_postgres_url()
    )
)
    
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

class SqlAlchemyUnitOfWork(AbstractUnitOfWork):

    def __init__(self, session_factory = SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    def __enter__(self) -> AbstractUnitOfWork:
        self.session = self.session_factory()
        self.session.expire_on_commit = False
        self.repository = repository.SQLAlchemyRepository(self.session)
        return super().__enter__()
    
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()