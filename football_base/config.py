import os

def get_postgres_url() -> str:
    host: str = os.environ.get("DB_HOST")
    port: int = os.environ.get("DB_PORT")
    password: str = os.environ.get("DB_PASSWORD")
    user: str = os.environ.get("DB_USER")
    db_name: str = os.environ.get("DB_NAME")
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url() -> str:
    host: str = os.environ.get("API_HOST", "localhost")
    port: str = 7000 if host == "localhost" else 70
    return f"http://{host}:{port}"