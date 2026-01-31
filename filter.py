"""
Aggressive data reduction to get under 100MB for GitHub
Keeps only recent data with all relationships intact
"""

import pandas as pd
import os

SOURCE = "source/"
OUTPUT = "source/new/"  # Changed to source/new/ to match ddl.py

if not os.path.exists(OUTPUT):
    os.makedirs(OUTPUT)

print("=" * 70)
print("AGGRESSIVE DATA REDUCTION FOR GITHUB (<100MB)")
print("=" * 70)
print()

# Strategy: Keep only last 3 months of 2018 data
print("📅 Step 1: Filter orders to last 3 months...")
orders = pd.read_csv(f"{SOURCE}orders.csv")
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

print(f"  Original orders: {len(orders):,}")
print(f"  Date range: {orders['order_purchase_timestamp'].min()} to {orders['order_purchase_timestamp'].max()}")

# Keep only June-August 2018 (3 months)
filtered_orders = orders[
    (orders['order_purchase_timestamp'] >= '2018-06-01') & 
    (orders['order_purchase_timestamp'] < '2018-09-01')
]
print(f"  Filtered orders (Jun-Aug 2018): {len(filtered_orders):,}")

order_ids = set(filtered_orders['order_id'])
customer_ids = set(filtered_orders['customer_id'])

# Step 2: Filter all related tables
print()
print("📦 Step 2: Filter related tables...")

order_items = pd.read_csv(f"{SOURCE}order_items.csv")
order_items_filtered = order_items[order_items['order_id'].isin(order_ids)]
print(f"  Order items: {len(order_items):,} → {len(order_items_filtered):,}")

seller_ids = set(order_items_filtered['seller_id'])
product_ids = set(order_items_filtered['product_id'])

order_payments = pd.read_csv(f"{SOURCE}order_payments.csv")
order_payments_filtered = order_payments[order_payments['order_id'].isin(order_ids)]
print(f"  Order payments: {len(order_payments):,} → {len(order_payments_filtered):,}")

order_reviews = pd.read_csv(f"{SOURCE}order_reviews.csv")
order_reviews_filtered = order_reviews[order_reviews['order_id'].isin(order_ids)]
print(f"  Order reviews: {len(order_reviews):,} → {len(order_reviews_filtered):,}")

customers = pd.read_csv(f"{SOURCE}customers.csv")
customers_filtered = customers[customers['customer_id'].isin(customer_ids)]
print(f"  Customers: {len(customers):,} → {len(customers_filtered):,}")

products = pd.read_csv(f"{SOURCE}products.csv")
products_filtered = products[products['product_id'].isin(product_ids)]
print(f"  Products: {len(products):,} → {len(products_filtered):,}")

sellers = pd.read_csv(f"{SOURCE}sellers.csv")
sellers_filtered = sellers[sellers['seller_id'].isin(seller_ids)]
print(f"  Sellers: {len(sellers):,} → {len(sellers_filtered):,}")

# Geolocation - sample only 10% to save space
print()
print("📍 Step 3: Aggressively reduce geolocation...")
geolocation = pd.read_csv(f"{SOURCE}geolocation.csv")
geolocation_small = geolocation.sample(frac=0.1, random_state=42)
print(f"  Geolocation: {len(geolocation):,} → {len(geolocation_small):,} (90% reduction)")

# Category translation - keep all (tiny file)
category_translation = pd.read_csv(f"{SOURCE}product_category_translation.csv")
print(f"  Category translation: {len(category_translation):,} (kept all)")

# Step 3: Save all filtered data
print()
print("💾 Step 4: Saving filtered files...")
filtered_orders.to_csv(f"{OUTPUT}orders.csv", index=False)
order_items_filtered.to_csv(f"{OUTPUT}order_items.csv", index=False)
order_payments_filtered.to_csv(f"{OUTPUT}order_payments.csv", index=False)
order_reviews_filtered.to_csv(f"{OUTPUT}order_reviews.csv", index=False)
customers_filtered.to_csv(f"{OUTPUT}customers.csv", index=False)
products_filtered.to_csv(f"{OUTPUT}products.csv", index=False)
sellers_filtered.to_csv(f"{OUTPUT}sellers.csv", index=False)
geolocation_small.to_csv(f"{OUTPUT}geolocation.csv", index=False)
category_translation.to_csv(f"{OUTPUT}product_category_translation.csv", index=False)

print()
print("=" * 70)
print("✅ DONE!")
print("=" * 70)
print()
print(f"Overall reduction: {100 - (len(filtered_orders)/len(orders))*100:.1f}%")
print()
print("Next steps:")
print("1. Delete old my.db: rm my.db")
print("2. Run: python ddl.py")
print("3. Check size: ls -lh my.db")
print("4. If still >100MB, change date to '2018-07-01' (only 2 months)")
print()
print("Expected result: my.db should be 30-50 MB")