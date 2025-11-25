from fastapi import APIRouter
from app.services.ml_service import ml_service
from app.schemas import PredictRequest
import pandas as pd

router = APIRouter()

@router.post("/predict")
def predict(req: PredictRequest):
    df = pd.DataFrame(req.records)
    preds = ml_service.predict(df)
    return {"predictions": preds.tolist()}