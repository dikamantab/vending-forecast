import xgboost as xgb
import pandas as pd
from app.config import settings

class MLService:
    def __init__(self, model_path="app/ml/xgb_model_2.json"):
        # path = model_path or settings.ML_MODEL_PATH
        # self.model = joblib.load(path)
        path = model_path or settings.ML_MODEL_PATH
        self.model = xgb.Booster()
        self.model.load_model(path)

    def predict(self, df: pd.DataFrame):
        # If you have preprocessing pipeline saved as joblib, load it here and transform.
        # preds = self.model.predict(df)
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"Expected Dataframe, got {type(df)}")

        if df.empty:
            raise ValueError("Dataframe is empty")

        # # Ensure all columns are numeric
        # if not all(df.dtypes.apply(lambda x: np.issubdtype(x, np.number))):
        #     non_numeric = df.dtypes[~df.dtypes.apply(lambda x: np.issubdtype(x, np.number))]
        #     raise ValueError(f"Non-numeric columns: {list(non_numeric)}")
        
        dmatrix = xgb.DMatrix(df)
        preds = self.model.predict(dmatrix)
        return preds
    
    def preprocess_for_model(self, raw_df: pd.DataFrame) -> pd.DataFrame:
        """
        Docstring for preprocess_for_model
        Convert raw transaction data into model-ready features.
        
        Assumes raw_df has columns:
        1. SKU
        2. Jumlah
        3. Harga asli
        4. Waktu Transaksi
        """

        # 1. Use SKU as "Category"
        df = raw_df.copy()
        df["date"] = pd.to_datetime(
            df["Waktu Transaksi"],
            format="%d-%m-%Y %H:%M:%S"
        ).dt.normalize()

        # 2. Aggregate daily sales per SKU
        daily = df.groupby(["SKU", "date"]).agg(
            Total_Jumlah=("Jumlah", "sum"),
            Harga_asli=("Harga asli", "mean")
        ).reset_index()

        # 3. Encode SKU
        # all_skus = sorted(daily["SKU"].unique())
        # sku_to_id = {sku: i for i, sku in enumerate(all_skus)}
        daily["Category"] = daily["SKU"]

        # 4. Add time
        daily["DayOfWeek"] = daily["date"].dt.dayofweek
        daily["Month"] = daily["date"].dt.month

        # 5. Add lag & rolling features (per SKU)
        daily = daily.sort_values(["SKU", "date"])
        daily["Sales_Lag_1"] = daily.groupby("SKU")['Total_Jumlah'].shift(1)
        daily['Sales_Lag_7'] = daily.groupby("SKU")['Total_Jumlah'].shift(7)
        # daily["Sales_RollingMean_7"] = (
        #     daily.groupby("SKU")["Total_Jumlah"]
        #     .rolling(window=7, min_periods=1)
        #     .mean()
        #     .reset_index(level=0, drop=True)
        #     .shift(1)
        # )
        # daily["Sales_RollingMean_14"] = (
        #     daily.groupby("SKU")["Total_Jumlah"]
        #     .rolling(window=14, min_periods=1)
        #     .mean()
        #     .reset_index(level=0, drop=True)
        #     .shift(1)
        # )
        daily["Sales_RollingMean_7"] = (
            daily.groupby("SKU")["Total_Jumlah"]
            .transform(lambda x: x.rolling(7, min_periods=1).mean().shift(1))
        )
        daily["Sales_RollingMean_14"] = (
            daily.groupby("SKU")["Total_Jumlah"]
            .transform(lambda x: x.rolling(14, min_periods=1).mean().shift(1))
        )

        # 6. Clean up
        daily = daily.dropna()
        daily = daily.rename(columns={"Harga_asli": "Harga asli"})

        # 7. Select features in order
        feature_order = [
            'Category', 'Total_Jumlah', 'Harga asli', 'Sales_Lag_1', 'Sales_Lag_7',
            'Sales_RollingMean_7', 'Sales_RollingMean_14', 'DayOfWeek', 'Month'
        ]

        return daily[feature_order]
    
ml_service = MLService() 