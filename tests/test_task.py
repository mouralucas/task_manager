import asyncio
import json
import uuid
from sqlalchemy.dialects.postgresql import insert as pg_insert
import pytest
import pytest_asyncio
from httpx import AsyncClient
from starlette import status

from backend.database import test_sessionmanager, get_session
from main import app
from managers.task import TaskManager
from models.task import Base, TaskStatusModel


@pytest_asyncio.fixture(scope='function')
async def test_session():
    async with test_sessionmanager.connect() as connection:
        """
            For testing, all tables are dropped and then created again
        """
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with test_sessionmanager.session() as session:
        yield session


@pytest_asyncio.fixture(scope='function', autouse=True)
def override_db_session(test_session):
    """
    Overrides the database session, in this case using test_sessionmanager.
    In session end it rolls back all database operations.
    """
    app.dependency_overrides[get_session] = lambda: test_session


@pytest_asyncio.fixture(scope='function', autouse=True)
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def create_status(test_session):
    status_list = [
        TaskStatusModel(
            id=uuid.UUID('5836a901-6e05-4d5c-b20b-c4b447636de7'),
            name='Ativo',
            description='Tarefa ativa',
        ),
        TaskStatusModel(
            id=uuid.UUID('217211e9-adb2-4d6a-a200-6efa38375320'),
            name='Concluído',
            description='Tarefa concluída',
        ),
        TaskStatusModel(
            id=uuid.UUID('b36f1443-9bdf-4484-aeb3-65fe51236d0c'),
            name='Cancelado',
            description='Tarefa cancelada',
        )
    ]
    await TaskManager(test_session).create_status(status_list)


@pytest.mark.asyncio
async def test_task(client, create_status):
    # Cria uma nova tarefa
    payload = {
        "date": "2024-12-01T13:06:16.774Z",
        "description": "Tarefa de teste"
    }
    response = await client.post("/task", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    assert 'task' in data
    assert 'id' in data['task']
    assert 'date' in data['task']
    assert 'description' in data['task']
    assert 'status' in data['task']
    assert 'name' in data['task']['status']
    assert 'Ativo' == data['task']['status']['name']

    tarefa_1_id = data['task']['id']

    # Busca as tarefas disponíveis
    response = await client.get('/task')
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'tasks' in data
    assert type(data['tasks']) is list
    assert len(data['tasks']) == 1

    # Cria uma segunda tarefa
    payload = {
        "date": "2024-11-30T15:10:00.774Z",
        "description": "Outra de teste"
    }
    response = await client.post("/task", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()

    tarefa_2_id = data['task']['id']

    # Verifica se existem 2 tarefas cadastradas
    response = await client.get('/task')
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(data['tasks']) == 2

    # Marca a tarefa 1 como concluída
    payload = {
        'taskId': tarefa_1_id
    }
    response = await client.patch("/task/complete", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert 'task' in data
    assert 'status' in data['task']
    assert 'name' in data['task']['status']
    assert 'Concluído' == data['task']['status']['name']
