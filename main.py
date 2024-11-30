import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.database import sessionmanager
from backend.settings import settings
from models.task import TaskStatusModel
from routes import tasks
from sqlalchemy.dialects.postgresql import insert as pg_insert


@asynccontextmanager
async def lifespan(app: FastAPI):
    await sessionmanager.init_database()

    # add task status
    async with sessionmanager.session() as session:
        status_list = [
            {
                'id': uuid.UUID('5836a901-6e05-4d5c-b20b-c4b447636de7'),
                'name': 'Ativo',
                'description': 'Tarefa ativa',
            },
            {
                'id': uuid.UUID('b36f1443-9bdf-4484-aeb3-65fe51236d0c'),
                'name': 'Cancelado',
                'description': 'Tarefa cancelada',
            }
        ]
        for i in status_list:
            new_row = pg_insert(TaskStatusModel).values(i).on_conflict_do_nothing(index_elements=['id'])
            await session.execute(new_row)
        await session.commit()

    yield


app = FastAPI(
    title=settings.project_name,
    description=settings.project_description,
    version=settings.project_version,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.include_router(tasks.router, tags=["tasks"])
