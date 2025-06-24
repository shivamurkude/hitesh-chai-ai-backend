from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
import uuid

class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: Literal["user", "ai"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ProcessingStep(BaseModel):
    step: Literal["analyze", "think", "output"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    success: bool
    message: Message
    processing_steps: List[ProcessingStep] = []
    error: Optional[str] = None

class StreamStep(BaseModel):
    step: Literal["analyze", "think", "output"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    is_complete: bool = False

class ChatHistoryResponse(BaseModel):
    success: bool
    messages: List[Message] = []
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    version: str = "1.0.0" 