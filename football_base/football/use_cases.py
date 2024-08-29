import abc

from enum import Enum
from football_base.utils import update_attributes
from football_base.football.domain.entities import League
from football_base.football.domain.readers import LeagueReader
from football_base.football.service_layer.unit_of_work import AbstractUnitOfWork

class Status(Enum):
    CREATED: str = "Created"
    ERROR: str = "Error"
    SUCCESS: str = "Success"
    UNAUTHORIZED: str = "Unauthorized"

class UseCase(abc.ABC):

    def __init__(self, unit_of_work: AbstractUnitOfWork) -> None:
        super().__init__()
        self.unit_of_work = unit_of_work

    @abc.abstractmethod
    def execute(self, parameters: dict) -> dict:
        ...

    def response(self, status: Status, message: str) -> dict:
        return {
            "status": status.name,
            "message": message,
        }

    def result(self, status: Status, result: list) -> dict:
        return {
            "status": status.name,
            "result": result,
        }
    
class HomeUseCase(UseCase):
    START_MESSAGE: str = "Football Base Service"

    def execute(self, parameters: dict) -> dict:
        return self.response(
            Status.SUCCESS,
            self.START_MESSAGE,
        )

class LeaguesListUseCase(UseCase):

    def execute(self, _: dict) -> dict:

        with self.unit_of_work:
            leagues: list[dict] = []
            for league in self.unit_of_work.repository.list_leagues():
                leagues.append(league.get_status())

        return self.result(Status.SUCCESS, leagues)
    
class InsertLeagueUseCase(UseCase):

    def execute(self, parameters: dict) -> dict:
        with self.unit_of_work:
            league_name: str = parameters["name"]
            record = LeagueReader(parameters).get_record()
            league = League.from_dict(record)
            self.unit_of_work.repository.save_league(league)
            self.unit_of_work.commit()
    
        message = f"League '{league_name}' successfully created."
        return self.response(Status.CREATED, message)

class GetLeagueUseCase(UseCase):

    def execute(self, parameters: dict) -> dict:

        league_id: int = parameters["league_id"]
        with self.unit_of_work:
            league = self.unit_of_work.repository.get_league_by_id(league_id)

            if not league:
                return self.response(Status.ERROR, f"League not found for id: {league_id}.")            
    
        return self.result(Status.SUCCESS, league.get_attributes())

class UpdateLeagueUseCase(UseCase):

    def execute(self, parameters: dict) -> dict:
        league_id: int = parameters["league_id"]
        with self.unit_of_work:
            league = self.unit_of_work.repository.get_league_by_id(league_id)

            if not league:
                return self.response(Status.ERROR, f"League not found for id: {league_id}.")
            
            update_attributes(league, parameters)
            self.unit_of_work.repository.save_league(league)
            self.unit_of_work.commit()
    
        message = f"League (Id = {league_id})' successfully updated."
        return self.response(Status.SUCCESS, message)
    
class DeleteLeagueUseCase(UseCase):

    def execute(self, parameters: dict) -> dict:
        league_id: int = parameters["league_id"]
        with self.unit_of_work:
            
            deleted = self.unit_of_work.repository.delete_league(league_id)
            if not deleted:
                return self.response(Status.ERROR, f"League not found for id: {league_id}.")

            self.unit_of_work.commit()
    
        message = f"League (Id = {league_id})' successfully deleted."
        return self.response(Status.SUCCESS, message)
