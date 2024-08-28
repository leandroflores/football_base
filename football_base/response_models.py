import abc

def create_response(response: dict) -> "APIResponse":
    responses = {
        "CREATED": APICreatedResponse,
        "SUCCESS": APISuccessResponse,
        "NEW_RECORD": APICreatedResponse,
        "ERROR": APIErrorResponse,
        "UNAUTHORIZED": APIUnauthorizedResponse,
        "FORBIDDEN": APIForbiddenResponse,
    }
    try:
        message: str = response.get("message", None)
        result: object = response.get("result", None)
        status: str = response["status"]

        return responses[status](message, result)
    except KeyError:
        return APINoContentResponse(None, None)

class APIResponse(abc.ABC):

    def __init__(
            self, 
            http_code: int, 
            http_status: str, 
            message: str, 
            result: list
    ) -> None:
        super().__init__()
        self.http_code = http_code
        self.http_status = http_status
        self.message = message
        self.result  = result

    def get_return_data(self) -> dict:
        if self.message:
            return {"message": self.message}
        return {"result": self.result}

    def __str__(self) -> str:
        return f"{self.http_code}: {self.http_status}"


class APICreatedResponse(APIResponse):

    def __init__(self, message: str, result: list) -> None:
        super().__init__(200, "OK", message, result)


class APISuccessResponse(APIResponse):

    def __init__(self, message: str, result: list) -> None:
        super().__init__(201, "CREATED", message, result)

class APINoContentResponse(APIResponse):

    def __init__(self, message: str, result: list) -> None:
        super().__init__(204, "NO_CONTENT", message, result)

class APIErrorResponse(APIResponse):
    
    def __init__(self, message: str, result: list) -> None:
        super().__init__(400, "BAD_REQUEST", message, result)

class APIUnauthorizedResponse(APIResponse):
    
    def __init__(self, message: str, result: list) -> None:
        super().__init__(401, "UNAUTHORIZED", message, result)

class APIForbiddenResponse(APIResponse):
    
    def __init__(self, message: str, result: list) -> None:
        super().__init__(403, "FORBIDDEN", message, result)