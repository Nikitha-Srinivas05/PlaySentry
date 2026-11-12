from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress, field_validator


class EventCreate(BaseModel):
    timestamp: datetime
    source: Literal["game_server", "agent", "pcap"]
    event_type: str = Field(min_length=1, max_length=50, pattern=r"^[a-z0-9_]+$")
    src_ip: IPvAnyAddress | None = None
    username: str | None = Field(default=None, max_length=100)
    details: dict = Field(default_factory=dict)

    @field_validator("timestamp")
    @classmethod
    def ensure_timezone(cls, v: datetime) -> datetime:
        return v if v.tzinfo else v.replace(tzinfo=timezone.utc)

    @field_validator("details")
    @classmethod
    def limit_details_size(cls, v: dict) -> dict:
        if len(str(v)) > 2000:
            raise ValueError("details too large (max 2000 characters)")
        return v


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    received_at: datetime