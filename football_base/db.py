import abc

LEAGUE_TABLE_NAME: str = "leagues"

class Database(abc.ABC):
    database: dict[str, list] = {}

    def __init__(self) -> None:
        super().__init__()
        self._start_database()

    def table_names(self) -> list[str]:
        ...

    def _start_database(self) -> None:
        for table_name in self.table_names():
            self.database[table_name] = []

    def _table(self, table_name: str) -> list[dict]:
        try:
            return self.database[table_name]
        except KeyError:
            return []

    def next_id(self, table: str) -> int:
        return len(self._table(table)) + 1
        
    def insert(self, table: str, record: dict) -> dict:
        record["id"] = self.next_id(table)
        self._table(table).append(record)
        return record
    
    def select(self, table: str, field: str, value: object) -> list[dict]:
        records: list[dict] = []
        for record in self._table(table):
            if record[field] == value:
                records.append(record)
        return records
    
    def get(self, table: str, field: str, value: object) -> dict:
        for record in self._table(table):
            if record[field] == value:
                return record
        return {}
    
    def get_by_id(self, table: str, id: int) -> dict:
        return self.get(table, "id", id)
    
    def update(self, table: str, record_updated: dict) -> bool:
        for record in self._table(table):
            if record["id"] == record_updated["id"]:
                record.update(record_updated)
                return True
        return False
    
    def delete(self, table: str, record: dict) -> None:
        self._table(table).remove(record)

    def delete_by_id(self, table: str, id: int) -> bool:
        record = self.get_by_id(table, id)
        if record:
            self.delete(table, record)
            return True
        return False
    
    def list(self, table: str) -> list[dict]:
        return self._table(table)

class InMemoryDataBase(Database):

    def __init__(self) -> None:
        super().__init__()

    def table_names(self) -> list[str]:
        return [
            LEAGUE_TABLE_NAME,
        ]

    def save_league(self, record: dict) -> None:
        if record["id"] is None:
            self.insert_league(record)
        else:
            self.update_league(record)
    
    def insert_league(self, record: dict) -> dict:
        return self.insert(LEAGUE_TABLE_NAME, record)

    def update_league(self, record: dict) -> bool:
        self.update(LEAGUE_TABLE_NAME, record)

    def get_league_by_id(self, id: int) -> dict:
        return self.get_by_id(LEAGUE_TABLE_NAME, id)
    
    def delete_league(self, league_id: str) -> bool:
        station: dict = self.get_league_by_id(league_id)
        if station and "id" in station and station["id"]:
            return self.delete_by_id(LEAGUE_TABLE_NAME, station["id"])
        return False
    
    def list_leagues(self) -> list:
        return self.list(LEAGUE_TABLE_NAME)