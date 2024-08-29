import abc

from football_base.db import InMemoryDataBase
from football_base.football.domain.entities import League
from sqlalchemy.orm import Session
from typing import Optional

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def save_league(self, league: League) -> None:
        ...
    
    @abc.abstractmethod
    def get_league_by_id(self, league_id: int) -> Optional[League]:
        ...

    @abc.abstractmethod
    def delete_league(self, league_id: int) -> bool:
        ...

    @abc.abstractmethod
    def list_leagues(self) -> list[League]:
        ...

class InMemoryRepository(AbstractRepository):
    
    def __init__(self, database: InMemoryDataBase) -> None:
        self.database = database
    
    def save_league(self, league: League) -> None:
        if not league.id:
            self.database.save_league(league.to_dict())
        else:
            self.database.update_league(league.to_dict())

    def get_league_by_id(self, league_id: int) -> Optional[League]:
        record = self.database.get_league_by_id(league_id)
        if record:
            return League.from_dict(record)
        return None

    def delete_league(self, league_id: int) -> bool:
        return self.database.delete_league(league_id)

    def list_leagues(self) -> list[League]:
        leagues: list[dict] = self.database.list_leagues()
        return [League.from_dict(league) for league in leagues]
    
class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session: Session) -> None:
        self.session = session

    def save_league(self, league: League) -> None:
        self.session.add(league)

    def get_league_by_id(self, league_id: int) -> Optional[League]:
        try:
            return self.session.query(League).filter_by(station_id=league_id).one()
        except NoResultFound:
            return None