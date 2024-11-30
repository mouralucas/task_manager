import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from models.task import TaskModel


class TaskManager:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def create_task(self, task: TaskModel) -> TaskModel:
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)

        return task

    async def update_task(self, task: TaskModel) -> None:
        pass

    async def delete_task(self, task_id: uuid.UUID) -> bool:
        query = delete(TaskModel).where(TaskModel.id == task_id)

        try:
            await self.session.execute(query)
            await self.session.flush()

            return True
        except Exception as e:
            return False

    async def get_task_by_id(self, task_id: int) -> TaskModel:
        pass

    async def get_tasks(self) -> list[TaskModel]:
        query = select(TaskModel).order_by(TaskModel.date)

        tasks = await self.session.execute(query)
        tasks = tasks.mappings().all()

        return [task['TaskModel'] for task in tasks] if tasks else []

