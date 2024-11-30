import uuid

from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_camel

from schemas.task import TaskSchema


class CreateTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=AliasGenerator(serialization_alias=to_camel))

    task: TaskSchema = Field(..., description="The task created")


class UpdateTaskResponse(BaseModel):
    pass


class DeleteTaskResponse(BaseModel):
    deleted: bool = Field(..., description="Whether the task was deleted")
    task_id: uuid.UUID = Field(..., description="The id of deleted task")


class GetTaskResponse(BaseModel):
    tasks: list[TaskSchema] = Field(..., description="List of all tasks")