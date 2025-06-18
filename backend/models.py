from pydantic import BaseModel
from typing import List
from datetime import datetime

class Detection(BaseModel):
    timestamp: datetime
    objects: List[str]
