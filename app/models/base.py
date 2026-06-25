from pydantic import BaseModel, ConfigDict, Field


class DocumentModel(BaseModel):
    """Base for MongoDB document schemas."""

    model_config = ConfigDict(populate_by_name=True)

    id: str | None = Field(default=None, alias="_id")
