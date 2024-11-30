import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class StatusSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=AliasGenerator(serialization_alias=to_camel))

    id: uuid.UUID = Field(..., description="Unique identifier for the status")
    name: str = Field(..., description="Name of the status")
    description: str | None = Field(None, description="Description of the status")


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=AliasGenerator(serialization_alias=to_camel))

    id: uuid.UUID = Field(..., description="The unique identifier of the task")
    date: datetime = Field(..., description="The date of the task")
    description: str = Field(..., description="The description of the task")
    status_id: uuid.UUID = Field(..., description="The unique identifier of the status")
    status: StatusSchema = Field(..., description="The status of the task")