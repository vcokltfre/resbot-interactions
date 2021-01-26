from pydantic import BaseModel


class Interaction(BaseModel):
    id: int
    type: int
    data: dict
    guild_id: int
    channel_id: int
    member: dict
    token: str
    version: int