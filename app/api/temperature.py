from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import TemperatureIn

router = APIRouter()

@router.post("/temperature/receive")
def receive_temp(payload: TemperatureIn, db: Session = Depends(get_db)):
    temp = models.Temperature(
    machine_id = payload.machine_id,
    temperature = payload.temperature,
    humidity = payload.humidity,
    timestamp = payload.timestamp
    )
    db.add(temp)
    db.commit()
    return {"status": "ok"}