import abc

from football_base.db import InMemoryDataBase
from football_base.football.domain.entities import League

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def save_league(self, league: League) -> None:
        ...

    @abc.abstractmethod
    def list_leagues(self) -> list[League]:
        ...

class InMemoryRepository(AbstractRepository):
    
    def __init__(self, database: InMemoryDataBase) -> None:
        self.database = database
    
    def save_league(self, league: League) -> None:
        self.database.save_league(league.to_dict())

    def list_leagues(self) -> list[League]:
        leagues: list[dict] = self.database.list_leagues()
        return [League.from_dict(league) for league in leagues]