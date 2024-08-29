from football_base.football.service_layer import unit_of_work
from football_base.football import use_cases

_unit_of_work = unit_of_work.InMemoryUnitOfWork()

home_use_case = use_cases.HomeUseCase(_unit_of_work)

list_leagues_use_case = use_cases.LeaguesListUseCase(_unit_of_work)

insert_league_use_case = use_cases.InsertLeagueUseCase(_unit_of_work)

get_league_use_case = use_cases.GetLeagueUseCase(_unit_of_work)

update_league_use_case = use_cases.UpdateLeagueUseCase(_unit_of_work)

delete_league_use_case = use_cases.DeleteLeagueUseCase(_unit_of_work)