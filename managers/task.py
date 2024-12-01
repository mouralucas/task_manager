import uuid

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import TaskModel


class TaskManager:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_task(self, task: TaskModel) -> TaskModel:
        """
        Create a new task
        :param task: The model to be created
        :return: the created task
        """
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)

        return task

    async def complete_task(self, task_id) -> None:
        """
        Update a task setting the status as 'Concluído'
        :param task_id: the task id
        :return: None
        """
        query = update(TaskModel).values(status_id=uuid.UUID('217211e9-adb2-4d6a-a200-6efa38375320')).where(TaskModel.id == task_id)

        await self.session.execute(query)
        await self.session.flush()

        return

    async def delete_task(self, task_id: uuid.UUID) -> bool:
        """
        Remove a task from the database
        :param task_id: the task id
        :return: a boolean indicating if the task was deleted
        """
        query = delete(TaskModel).where(TaskModel.id == task_id)

        try:
            await self.session.execute(query)
            await self.session.flush()

            return True
        except Exception as e:
            return False

    async def get_task_by_id(self, task_id: uuid.UUID) -> TaskModel | None:
        """
        Get a task by its id
        :param task_id: the task id
        :return: The task or None
        """
        query = select(TaskModel).where(TaskModel.id == task_id)

        try:
            result = await self.session.execute(query)
            result = result.scalar_one()
        except Exception as e:
            result = None

        return result

    async def get_tasks(self) -> list[TaskModel]:
        """
        Get all tasks
        :return: A list of all tasks
        """
        query = select(TaskModel).order_by(TaskModel.date)

        tasks = await self.session.execute(query)
        tasks = tasks.mappings().all()

        return [task['TaskModel'] for task in tasks] if tasks else []

    async def create_status(self, statuses):
        """
        Create the status
        :param statuses: the list of statuses model
        :return:
        """
        self.session.add_all(statuses)
        await self.session.flush()
