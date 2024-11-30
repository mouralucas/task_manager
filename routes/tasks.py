from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from schemas.request.task import CreateTaskRequest, DeleteTaskRequest, CompleteTaskRequest
from schemas.response.task import CreateTaskResponse, DeleteTaskResponse, GetTaskResponse, CompleteTaskResponse
from backend.database import get_session
from services.task import TaskService

router = APIRouter(prefix="/task")


@router.post('', summary='Create a new task', status_code=status.HTTP_201_CREATED)
async def create_new_task(
        task: CreateTaskRequest,
        session: AsyncSession = Depends(get_session)
) -> CreateTaskResponse:
    return await TaskService(session=session).create_task(task=task)


@router.patch('/complete', summary='Mark a task as completed')
async def complete_task(
        task: CompleteTaskRequest,
        session: AsyncSession = Depends(get_session),
) -> CompleteTaskResponse:
    return await TaskService(session=session).complete_task(task=task)

@router.delete('', summary='Delete a task')
async def delete_task(
        task: DeleteTaskRequest,
        session: AsyncSession = Depends(get_session),
) -> DeleteTaskResponse:
    return await TaskService(session=session).delete_task(task=task)


@router.get('', summary='List all tasks')
async def list_tasks(
        session: AsyncSession = Depends(get_session),
) -> GetTaskResponse:
    return await TaskService(session=session).get_tasks()
