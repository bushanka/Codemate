from datetime import datetime
from typing import List
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class Choice(BaseModel):
    index: int
    message: Message


class Usage(BaseModel):
    prompt_tokens: int
    total_tokens: int
    tokens_per_second: float
    completion_tokens: int


class Timestamps(BaseModel):
    request_time: datetime
    start_time_generation: datetime
    end_time_generation: datetime
    queue_wait_time: float
    generation_time: float


class AIResponse(BaseModel):
    request_id: int
    response_id: int
    model: str
    provider: str
    choices: List[Choice]
    usage: Usage
    timestamps: Timestamps

    def to_text(self):
        return self.choices[0].message.content