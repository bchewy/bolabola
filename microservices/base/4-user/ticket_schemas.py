from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TicketBase(BaseModel):
    event_id: int
    venue_id: int
    seat_id: int

class TicketOwned(TicketBase):
    user_id: int
    purchased_at: datetime