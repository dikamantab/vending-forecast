import os
import pandas as pd
from datetime import datetime
from app.database import SessionLocal
from app import models

def import_sales_from_excel(path):
    df = pd.read_excel(path)
    db = SessionLocal()
    try:
        for _, row in df.iterrows():
            sale = models.Sale(
                machine_id = row.get('machine_id') or row.get('location') or 'unknown',
                product = row['product'],
                qty = int(row['qty']),
                timestamp = pd.to_datetime(row['timestamp']).to_pydatetime()
            )
            db.add(sale)
        db.commit()
    finally:
        db.close()

def process_pending_folder(folder):
    for fname in os.listdir(folder):
        if fname.lower().endswith(('.xls', '.xlsx')):
            path = os.path.join(folder, fname)
            try:
                import_sales_from_excel(path)
                os.remove(path)
                print("Imported and removed", path)
            except Exception as e:
                print("Error importing", path, e)