from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Device(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    org_id: str = Field(index=True)
    deployment_id: Optional[int] = Field(default=None, index=True)
    device_id: str = Field(index=True)
    hostname: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    agent_version: Optional[str] = None
    status: str = "active"  # active | paused | offline
    first_seen_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen_at: datetime = Field(default_factory=datetime.utcnow)
    last_error: Optional[str] = None
    notes: Optional[str] = None
