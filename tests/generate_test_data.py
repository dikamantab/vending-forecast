import pandas as pd
import numpy as np

# Parameters
np.random.seed(42)
start_date = "2025-11-01"
end_date = "2025-11-30"
skus = [204021, 204022, 204023]  # numeric SKUs like your real data
products = ["TEH KOTAK 300 ML", "AIR MINERAL 600 ML", "KOPI SUSU 200 ML"]
vm_codes = ["VMJPNM001", "VMJPNM002"]
order_id_start = 1764000000000

# Generate date range
dates = pd.date_range(start=start_date, end=end_date, freq="D")

data = []
order_id = order_id_start

for date in dates:
    for sku, product in zip(skus, products):
        # Simulate 1-3 transactions per day per product
        n_transactions = np.random.randint(1, 4)
        for _ in range(n_transactions):
            vm_code = np.random.choice(vm_codes)
            jumlah = np.random.randint(1, 6)  # 1-5 units
            harga = {"TEH KOTAK 300 ML": 4400, "AIR MINERAL 600 ML": 3800, "KOPI SUSU 200 ML": 5200}[product]
            gross = jumlah * harga
            
            # Random time during the day
            hour = np.random.randint(8, 22)
            minute = np.random.randint(0, 60)
            second = np.random.randint(0, 60)
            waktu_transaksi = f"{date.strftime('%d-%m-%Y')} {hour:02d}:{minute:02d}:{second:02d}"
            
            data.append([
                order_id,
                vm_code,
                order_id,
                f"Mid-server-{order_id}",
                0,
                product,
                sku,
                np.random.randint(1, 10),
                jumlah,
                harga,
                gross,
                "midtrans",
                waktu_transaksi
            ])
            order_id += 1

# Create DataFrame
df = pd.DataFrame(data, columns=[
    "No", "VM Code", "Order ID", "MID", "TID", "Product", "SKU", "slot",
    "Jumlah", "Harga asli", "Gross", "Metode Bayar", "Waktu Transaksi"
])

# Save to Excel
df.to_excel("test_data_30_days.xlsx", index=False)
print("✅ Generated test_data_30_days.xlsx with 30 days of history for 3 products.")
print(f"Total rows: {len(df)}")
print(f"Date range: {df['Waktu Transaksi'].iloc[0]} → {df['Waktu Transaksi'].iloc[-1]}")