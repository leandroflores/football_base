import abc

class Reader(abc.ABC):
    parameters: dict

    def __init__(self, parameters: dict) -> None:
        self.parameters = parameters

    @abc.abstractmethod
    def get_record(self) -> dict:
        raise NotImplementedError

    def _is_valid_key(self, key: str) -> bool:
        return key in self.parameters and self.parameters[key]

    def get_value(self, functions: dict, default_value: object) -> object:
        for key in functions.keys():
            if self._is_valid_key(key):
                value = self.parameters[key]
                function = functions[key]
                return function(value)
        return default_value
    
class LeagueReader(Reader):

    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)

    def get_record(self) -> dict:
        record = {}
        record["name"] = self.parameters["name"]
        record["season"] = self.parameters["season"]
        record["details"] = self.parameters["details"]
        record["country"] = self.parameters["country"]
        return record