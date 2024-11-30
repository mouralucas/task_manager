from sqlalchemy.ext.asyncio import AsyncSession

from managers.task import TaskManager
from models.task import TaskModel
from schemas.request.task import CreateTaskRequest, DeleteTaskRequest, CompleteTaskRequest
from schemas.response.task import CreateTaskResponse, DeleteTaskResponse, GetTaskResponse, CompleteTaskResponse
from schemas.task import TaskSchema


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session
        self.task_manager = TaskManager(session)

    async def create_task(self, task: CreateTaskRequest) -> CreateTaskResponse:
        """
        Create the new task, by default all new tasks are created with 'Ativo' status
        :param task: The information about the new task
        :return: The created task
        """
        new_task_model = TaskModel(**task.model_dump())

        new_task = await self.task_manager.create_task(new_task_model)

        response = CreateTaskResponse(
            task=TaskSchema.model_validate(new_task),
        )

        return response

    async def complete_task(self, task: CompleteTaskRequest) -> CompleteTaskResponse:
        """
        Change task status to 'complete'
        :param task: task to be completed
        :return: The task updated
        """
        await self.task_manager.complete_task(task.id)
        task = await self.task_manager.get_task_by_id(task.id)

        response = CompleteTaskResponse(
            task=TaskSchema.model_validate(task),
        )

        return response

    async def delete_task(self, task: DeleteTaskRequest) -> DeleteTaskResponse:
        """
        Delete the selected test, defined by its id
        :param task: The task to delete
        :return: Whether the task was deleted and its id
        """
        deleted = await self.task_manager.delete_task(task.id)

        response = DeleteTaskResponse(
            deleted=deleted,
            task_id=task.id,
        )

        return response

    async def get_tasks(self):
        """
        Get all tasks
        :return: The list of all tasks
        """
        tasks = await self.task_manager.get_tasks()

        response = GetTaskResponse(
            tasks=[TaskSchema.model_validate(task) for task in tasks],
        )

        return response
