from sqlalchemy.ext.asyncio import AsyncSession

from managers.task import TaskManager
from models.task import TaskModel
from schemas.request.task import CreateTaskRequest, DeleteTaskRequest, UpdateTaskRequest
from schemas.response.task import CreateTaskResponse, DeleteTaskResponse, UpdateTaskResponse, GetTaskResponse
from schemas.task import TaskSchema


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.task_manager = TaskManager(session)

    async def create_task(self, task: CreateTaskRequest) -> CreateTaskResponse:
        new_task_model = TaskModel(**task.model_dump())

        new_task = await self.task_manager.create_task(new_task_model)

        response = CreateTaskResponse(
            task=TaskSchema.model_validate(new_task),
        )

        return response


    async def update_task(self, task: UpdateTaskRequest) -> UpdateTaskResponse:
        pass


    async def delete_task(self, task: DeleteTaskRequest) -> DeleteTaskResponse:
        deleted = await self.task_manager.delete_task(task.id)

        response = DeleteTaskResponse(
            deleted=deleted,
            task_id=task.id,
        )

        return response

    async def get_tasks(self):
        tasks = await self.task_manager.get_tasks()

        response = GetTaskResponse(
            tasks=[TaskSchema.model_validate(task) for task in tasks],
        )

        return response