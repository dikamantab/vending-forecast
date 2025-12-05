import xgboost as xgb

model = xgb.Booster()
model.load_model("app/ml/xgb_model_2.json")  # or whatever your path is

# Get feature names
feature_names = model.feature_names
print("Model expects these features:")
print(feature_names)