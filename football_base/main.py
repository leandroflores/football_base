from fastapi import FastAPI, Request, Response
from football_base import di
from football_base.request_models import League
from football_base.response_models import create_response

app: FastAPI = FastAPI()

STATUS_CODES: dict[str, int] = {
    "ERROR": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "SUCCESS": 200,
    "CREATED": 201,
    "NO_CONTENT": 204,
}

def get_status_code(status: str) -> int:
    try:
        return STATUS_CODES[status]
    except KeyError:
        return STATUS_CODES["NO_CONTENT"]

@app.get("/")
def home(response: Response) -> dict:
    result = di.home_use_case.execute({})
    return_data = create_response(result).get_return_data()

    response.status_code = get_status_code(result["status"])

    return return_data

@app.get("/leagues/")
def leagues_list(
    response: Response,
) -> dict:

    result = di.list_leagues_use_case.execute({})
    return_data = create_response(result).get_return_data()

    response.status_code = get_status_code(result["status"])

    return return_data

@app.post("/league/")
def insert_league(
    league: League, 
    response: Response,
) -> dict:

    parameters = league.to_dict()
    result = di.insert_league_use_case.execute(parameters)
    return_data = create_response(result).get_return_data()

    response.status_code = get_status_code(result["status"])

    return return_data

@app.get("/league/{league_id}")
def get_league(
    league_id: int,
    response: Response,
) -> dict:

    parameters: dict = {}
    parameters["league_id"] = league_id

    result = di.get_league_use_case.execute(parameters)
    return_data = create_response(result).get_return_data()

    response.status_code = get_status_code(result["status"])

    return return_data

@app.put("/league/{league_id}")
def update_league(
    league_id: int,
    league: League, 
    response: Response,
) -> dict:

    parameters: dict = {}
    parameters["league_id"] = league_id
    parameters.update(league.to_dict())
    
    result = di.update_league_use_case.execute(parameters)
    return_data = create_response(result).get_return_data()

    response.status_code = get_status_code(result["status"])

    return return_data

@app.delete("/league/{league_id}")
def delete_league(
    league_id: int,
    response: Response,
) -> dict:

    parameters: dict = {}
    parameters["league_id"] = league_id
    
    result = di.delete_league_use_case.execute(parameters)
    return_data = create_response(result).get_return_data()

    response.status_code = get_status_code(result["status"])

    return return_data
