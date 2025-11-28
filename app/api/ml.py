from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ml_service import ml_service
from app.schemas import PredictRequest
from io import BytesIO
import pandas as pd

router = APIRouter()

@router.post("/predict")
def predict(req: PredictRequest):
    df = pd.DataFrame(req.records)
    preds = ml_service.predict(df)
    return {"predictions": preds.tolist()}

@router.post("/predict2/file")
async def predict_from_excel(file: UploadFile = File(...)):
    # Reject if not excel
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Invalid file format. Only Excel files (.xlsx, .xls) are allowed.")
    
    # Process uploaded file
    try:
        # Read File
        contents = await file.read()
        df_raw = pd.read_excel(BytesIO(contents))

        # Validate columns
        expected_cols = {"VM Code", "Order ID", "Product", "SKU", "Jumlah", "Harga asli", "Gross", "Waktu Transaksi"}
        if not expected_cols.issubset(df_raw.columns):
            missing = expected_cols - set(df_raw.columns)
            raise HTTPException(status_code=400, detail=f"Missing columns: {', '.join(missing)}")

        # Preprocessing needed column
        FEATURE_COLUMNS = ["VM Code", "Order ID", "Product", "SKU", "Jumlah", "Harga asli", "Gross", "Waktu Transaksi"]
        if not set(FEATURE_COLUMNS).issubset(df_raw.columns):
            missing_feats = set(FEATURE_COLUMNS) - set(df_raw.columns)
            raise HTTPException(status_code=400, detail=f"Missing feature columns: {missing_feats}")
        
        df_features = df_raw[FEATURE_COLUMNS].copy()

        # Ensure numeric
        df_features = df_features.astype(float)

        # Run prediction
        preds = ml_service.predict(df_features)

        # return as list
        df_raw["prediction"] = preds

        return {
            "filename": file.filename,
            "predictions": preds.tolist(),
            "preview": df_raw.head().to_dict(orient="records")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")