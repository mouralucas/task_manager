from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project description
    project_name: str = "Lista de tarefas"
    project_description: str = "Serviço para gerenciar lista de tarefas"
    project_version: str = "0.0.1"

    # Database and test settings
    finance_database_url: str = 'sqlite+aiosqlite:///test_db.sqlite3'
    test_database_url: str = 'sqlite+aiosqlite:///:memory:'
    echo_sql: bool = False
    echo_test_sql: bool = True
    test: bool = False

settings = Settings()
