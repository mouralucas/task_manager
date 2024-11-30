import uuid

from pydantic import BaseModel, ConfigDict, AliasGenerator, Field
from pydantic.alias_generators import to_snake
from datetime import datetime


class CreateTaskRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=AliasGenerator(alias=to_snake))

    date: datetime = Field(..., description='The date of the task')
    description: str = Field(..., description='The description of the task')
    status_id: uuid.UUID = Field(uuid.UUID('5836a901-6e05-4d5c-b20b-c4b447636de7'), description='The id of task status. The default is \'Ativo\'')


class CompleteTaskRequest(BaseModel):
    id: uuid.UUID = Field(..., alias='taskId', description='The id of the task')


class DeleteTaskRequest(BaseModel):
    id: uuid.UUID = Field(..., alias='taskId', description='The id of the task')
