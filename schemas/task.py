import uuid
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict, AliasGenerator
from pydantic.alias_generators import to_camel


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True,
                              alias_generator=AliasGenerator(serialization_alias=to_camel))

    id: uuid.UUID = Field(..., description="The unique identifier of the task")
    date: datetime = Field(..., description="The date of the task")
    description: str = Field(..., description="The description of the task")
    status_id: uuid.UUID = Field(..., description="The unique identifier of the status")
    status_name: str | None = Field(None, description="The status of the task")