from pydantic import BaseModel, ConfigDict


class Brief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    summary: str
    key_points: list[str]
    sources: list[str]
