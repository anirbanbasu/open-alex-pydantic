from pydantic import BaseModel, ConfigDict


class BaseEntity(BaseModel):
    """Base entity model for OpenAlex API."""

    model_config = ConfigDict(
        strict=True,
        frozen=True,
        extra="allow",
        populate_by_name=True,
    )
