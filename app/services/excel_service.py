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
            sale = models.VendingSale(
                order_id = row.get('Order Id') or row.get('location') or 'unknown',
                vm_code = row.get('VM Code') or row.get('location') or 'unknown',
                product_name = row['Product'],
                sku = row['SKU'],
                slot = int(row['slot']),
                quantity = int(row['Jumlah']),
                price = int(row['Harga asli']),
                gross = int(row['Gross']),
                payment_method = row['Metode Bayar'],
                transaction_time = datetime.strptime(row['Waktu Transaksi'], '%d-%m-%Y %H:%M:%S')
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