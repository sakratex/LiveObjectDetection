from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class DetectionItem(BaseModel):
    class_name: str = Field(..., alias="class")
    confidence: float
    box: List[int]

class Detection(BaseModel):
    timestamp: datetime
    objects: List[DetectionItem]
