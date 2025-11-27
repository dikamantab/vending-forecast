import xgboost as xgb
import pandas as pd
from app.config import settings

class MLService:
    def __init__(self, model_path="app/ml/xgb_model.json"):
        # path = model_path or settings.ML_MODEL_PATH
        # self.model = joblib.load(path)
        path = model_path or settings.ML_MODEL_PATH
        self.model = xgb.Booster()
        self.model.load_model(path)

    def predict(self, df: pd.DataFrame):
        # If you have preprocessing pipeline saved as joblib, load it here and transform.
        preds = self.model.predict(df)
        return preds
    
ml_service = MLService()