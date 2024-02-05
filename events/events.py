from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.future import select
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import sessionmaker

# Database connection setup
DATABASE_URL = "postgresql+asyncpg://postgres:testpassword@localhost:5432/events_db"
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()

# Pydantic models for request and response
class EventBase(BaseModel):
    name: str
    description: str
    date: datetime
    location: str

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventInDBBase(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# SQLAlchemy models
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )

# FastAPI app instance
app = FastAPI()

# Dependency to get database session
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# CRUD operations and route handlers
@app.post("/events/", response_model=EventInDBBase)
async def create_event(event: EventCreate, db: AsyncSession = Depends(get_db)):    
    new_event = Event(**event.dict())
    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event

@app.get("/events/", response_model=list[EventInDBBase])
async def read_events(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    async with db() as session:
        result = await session.execute(select(Event).offset(skip).limit(limit))
        events = result.scalars().all()
        return events

@app.get("/events/{event_id}", response_model=EventInDBBase)
async def read_event(event_id: int, db: AsyncSession = Depends(get_db)):
    async with db() as session:
        result = await session.execute(select(Event).where(Event.id == event_id))
        event = result.scalars().first()
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

# Add additional CRUD operations for update and delete as needed.
