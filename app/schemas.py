from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TemperatureIn(BaseModel):
    machine_id: Optional[str]
    temperature: float
    humidity: Optional[float]
    timestamp: datetime

class SalesUpload(BaseModel):
    machine_id: str
    product: str
    qty: int
    timestamp: datetime

class PredictRequest(BaseModel):
    records: List[dict]