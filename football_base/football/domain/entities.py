from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class League:
    id: Optional[int]
    name: str
    season: str
    details: str
    country: str
    games: list["Match"] # type: Set[Game]

    @staticmethod
    def from_dict(adict: dict) -> "League":
        return League(
            id=adict.get("id", None),
            name=adict["name"],
            season=adict["season"],
            details=adict["details"],
            country=adict["country"],
            games=[],
        )

    def get_status(self) -> dict:
        return {
            "name": self.name,
            "season": self.season,
            "country": self.country,
        }
    
    def get_attributes(self) -> dict:
        attributes: dict = self.__dict__.copy()
        del attributes["id"]
        return attributes

    def add_game(self, game: "Match"):
        self.games.append(game)
    
    def games_list(self) -> list["Match"]:
        return self.games

    def to_dict(self) -> dict:
        return self.__dict__

    def __eq__(self, object: object) -> bool:
        return self.id == object.id

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{self.name} - {self.season}"
    
@dataclass
class Stadium:
    id: Optional[int]
    name: str
    city: str
    country: str
    
    @staticmethod
    def from_dict(adict: dict) -> "Stadium":
        return Stadium(
            id=adict.get("id", None),
            name=adict["name"],
            city=adict["city"],
            country=adict["country"],
        )


@dataclass
class Team:
    id: Optional[int]
    name: str
    code: str
    city: str
    country: str

    @staticmethod
    def from_dict(adict: dict) -> "Team":
        return Team(
            id=adict.get("id", None),
            name=adict["name"],
            code=adict["code"],
            city=adict["city"],
            country=adict["country"],
        )
    
@dataclass
class Match:
    id: Optional[int]
    league: League
    round: str
    stadium: Stadium
    day_hour: datetime
    home_team: Team
    home_goals: int
    home_et_goals: Optional[int]
    home_pk_goals: Optional[int]
    away_team: Team
    away_goals: int
    away_et_goals: Optional[int]
    away_pk_goals: Optional[int]

    