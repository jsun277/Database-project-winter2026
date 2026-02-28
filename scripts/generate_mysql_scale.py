import csv
import random
from datetime import datetime, timedelta

random.seed(42)

OUT_DIR = "data/generated"

N_USERS = 1000
N_CATEGORIES = 10
N_PRODUCTS = 5000
N_ORDERS = 100000
AVG_ITEMS_PER_ORDER = 3      # target ~300k order_items
RETURN_RATE = 0.03           # 3% of order_items (only for delivered)

def wcsv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)

def main():
    # users
    users = []
    for i in range(1, N_USERS + 1):
        users.append([f"user{i}@example.com", "$2b$12$dummyscalehash", f"First{i}", f"Last{i}"])
    wcsv(f"{OUT_DIR}/users.csv",
         ["email", "password_hash", "first_name", "last_name"],
         users)

    # categories
    categories = []
    for i in range(1, N_CATEGORIES + 1):
        categories.append([f"Category{i}", f"category-{i}"])
    wcsv(f"{OUT_DIR}/categories.csv", ["name", "slug"], categories)

    # products
    products = []
    for i in range(1, N_PRODUCTS + 1):
        cat_id = random.randint(1, N_CATEGORIES)
        price = round(random.uniform(5.0, 300.0), 2)
        products.append([cat_id, f"Product {i}", f"Description for product {i}", price, f"https://img/{i}", 1])
    wcsv(f"{OUT_DIR}/products.csv",
         ["category_id", "name", "description", "base_price", "image_url", "is_active"],
         products)

    # inventory: 1 variant per product for speed
    inventory = []
    for pid in range(1, N_PRODUCTS + 1):
        qty = random.randint(0, 200)
        inventory.append([pid, "default", qty, 5])
    wcsv(f"{OUT_DIR}/inventory.csv",
         ["product_id", "variant_key", "quantity", "low_stock_threshold"],
         inventory)

    # addresses: 1 per user (important: this makes address_id align with user_id if inserted cleanly)
    addresses = []
    for uid in range(1, N_USERS + 1):
        addresses.append([uid, f"{uid} Main St", "Chicago", "IL", f"{60000 + (uid % 9999)}", "USA", 1])
    wcsv(f"{OUT_DIR}/addresses.csv",
         ["user_id", "street", "city", "state", "zip_code", "country", "is_default"],
         addresses)

    # payment methods: 1 per user (payment_method_id aligns with user_id if inserted cleanly)
    payment_methods = []
    for uid in range(1, N_USERS + 1):
        last4 = str((1000 + uid) % 10000).zfill(4)
        payment_methods.append([uid, "credit_card", last4, 1])
    wcsv(f"{OUT_DIR}/payment_methods.csv",
         ["user_id", "method_type", "last_four", "is_default"],
         payment_methods)

    # orders + items + returns
    orders = []
    order_items = []
    returns = []

    base_date = datetime(2025, 1, 1)
    order_id = 1
    order_item_id = 1

    for _ in range(N_ORDERS):
        uid = random.randint(1, N_USERS)
        pmid = uid
        addrid = uid

        shipping_opt = random.choice(["standard", "expedited", "overnight"])
        ship_cost = {"standard": 8.99, "expedited": 12.99, "overnight": 19.99}[shipping_opt]

        created = base_date + timedelta(days=random.randint(0, 420), minutes=random.randint(0, 1440))
        status = random.choices(["confirmed", "shipped", "delivered"], weights=[0.2, 0.3, 0.5])[0]

        k = max(1, int(random.gauss(AVG_ITEMS_PER_ORDER, 1)))
        subtotal = 0.0
        items = []
        for __ in range(k):
            pid = random.randint(1, N_PRODUCTS)
            qty = random.randint(1, 3)
            unit_price = round(random.uniform(5.0, 300.0), 2)
            subtotal += unit_price * qty
            items.append((pid, "default", qty, unit_price))

        tax = round(subtotal * 0.08, 2)
        total = round(subtotal + tax + ship_cost, 2)
        expected = (created.date() + timedelta(days=random.randint(2, 7))).isoformat()

        orders.append([uid, pmid, addrid, shipping_opt,
                       round(subtotal, 2), tax, ship_cost, total, status,
                       expected, created.strftime("%Y-%m-%d %H:%M:%S")])

        for (pid, vkey, qty, unit_price) in items:
            order_items.append([order_id, pid, vkey, qty, unit_price])

            if status == "delivered" and random.random() < RETURN_RATE:
                refund = round(unit_price * qty * 0.9, 2)
                fee = round(unit_price * qty - refund, 2)
                returns.append([order_item_id, "Not satisfied", "refunded", refund, fee,
                                (created + timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d %H:%M:%S")])

            order_item_id += 1

        order_id += 1

    wcsv(f"{OUT_DIR}/orders.csv",
         ["user_id", "payment_method_id", "shipping_address_id", "shipping_option",
          "subtotal", "tax", "shipping_cost", "total", "status", "expected_delivery", "created_at"],
         orders)

    wcsv(f"{OUT_DIR}/order_items.csv",
         ["order_id", "product_id", "variant_key", "quantity", "unit_price"],
         order_items)

    wcsv(f"{OUT_DIR}/returns.csv",
         ["order_item_id", "reason", "status", "refund_amount", "restocking_fee", "created_at"],
         returns)

    print("CSV generation done.")
    print(f"Users: {len(users)} | Products: {len(products)} | Orders: {len(orders)}")
    print(f"OrderItems: {len(order_items)} | Returns: {len(returns)}")
    print("Output directory:", OUT_DIR)

if __name__ == "__main__":
    main()