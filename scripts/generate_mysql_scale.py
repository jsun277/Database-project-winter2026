import csv
import random
from datetime import datetime, timedelta

random.seed(42)

OUT_DIR = "data/generated"

N_USERS = 1000
N_PRODUCTS = 5000
N_ORDERS = 100000
AVG_ITEMS_PER_ORDER = 3      # target ~300k order_items
RETURN_RATE = 0.03            # 3% of order_items (only for delivered)

# ---------------------------------------------------------------------------
# Realistic reference data
# ---------------------------------------------------------------------------

CATEGORIES = [
    ("Electronics", "electronics"),
    ("Fashion", "fashion"),
    ("Home Decor", "home-decor"),
    ("Sports & Outdoors", "sports-outdoors"),
    ("Books", "books"),
    ("Toys & Games", "toys-games"),
    ("Beauty", "beauty"),
    ("Grocery", "grocery"),
    ("Automotive", "automotive"),
    ("Pet Supplies", "pet-supplies"),
]

# Products per category (name templates, price range)
PRODUCT_TEMPLATES = {
    "Electronics": (
        ["Wireless Headphones", "Bluetooth Speaker", "USB-C Hub", "Webcam",
         "Mechanical Keyboard", "Gaming Mouse", "Portable Charger", "Smart Watch",
         "Tablet Stand", "LED Desk Lamp", "Monitor Arm", "Noise Canceller",
         "Earbuds", "Power Strip", "HDMI Cable"],
        (15.0, 499.99),
    ),
    "Fashion": (
        ["Summer Dress", "Denim Jacket", "Linen Shirt", "Cargo Pants",
         "Wool Sweater", "Running Shoes", "Canvas Sneakers", "Silk Scarf",
         "Leather Belt", "Baseball Cap", "Maxi Skirt", "Hoodie",
         "Polo Shirt", "Chino Shorts", "Puffer Vest"],
        (19.99, 199.99),
    ),
    "Home Decor": (
        ["Ceramic Vase", "Wall Art Print", "Throw Pillow", "Scented Candle",
         "Table Lamp", "Area Rug", "Picture Frame", "Bookend Set",
         "Woven Basket", "Curtain Panel", "Decorative Tray", "Wall Clock",
         "Plant Pot", "Door Mat", "String Lights"],
        (9.99, 149.99),
    ),
    "Sports & Outdoors": (
        ["Yoga Mat", "Resistance Bands", "Water Bottle", "Hiking Backpack",
         "Jump Rope", "Foam Roller", "Camping Lantern", "Tennis Racket",
         "Basketball", "Cycling Gloves", "Swim Goggles", "Fishing Rod",
         "Dumbbell Set", "Running Armband", "Cooler Bag"],
        (8.99, 249.99),
    ),
    "Books": (
        ["Python Cookbook", "Data Science Handbook", "Design Patterns",
         "Clean Code", "SQL Fundamentals", "Machine Learning Guide",
         "Web Dev Bootcamp", "Algorithms Explained", "Cloud Architecture",
         "DevOps Handbook", "JavaScript Mastery", "Linux Administration",
         "Network Security", "API Design", "Database Internals"],
        (12.99, 59.99),
    ),
    "Toys & Games": (
        ["Building Blocks", "Board Game Classic", "Puzzle 1000pc", "RC Car",
         "Art Supply Kit", "Card Game Pack", "Plush Toy", "Science Kit",
         "Action Figure", "Dollhouse Set", "Train Set", "Kite",
         "Yo-Yo Pro", "Marble Run", "Strategy Game"],
        (7.99, 89.99),
    ),
    "Beauty": (
        ["Moisturizer SPF30", "Lip Balm Set", "Face Serum", "Hair Oil",
         "Nail Polish Kit", "Eye Cream", "Body Lotion", "Sunscreen SPF50",
         "Makeup Brush Set", "Shampoo Bar", "Perfume Mist", "Clay Mask",
         "Toner Pads", "Hand Cream", "Exfoliating Scrub"],
        (5.99, 79.99),
    ),
    "Grocery": (
        ["Organic Coffee Beans", "Granola Mix", "Olive Oil Extra Virgin",
         "Dark Chocolate Bar", "Almond Butter", "Green Tea Pack",
         "Dried Mango", "Protein Bar Box", "Honey Raw", "Pasta Variety",
         "Hot Sauce Trio", "Trail Mix", "Coconut Water", "Oat Milk",
         "Spice Rack Set"],
        (3.99, 39.99),
    ),
    "Automotive": (
        ["Phone Mount", "Dash Cam", "Tire Inflator", "Car Vacuum",
         "Seat Cushion", "Sun Shade", "Floor Mat Set", "Jump Starter",
         "LED Headlights", "Trunk Organizer", "Air Freshener Pack",
         "Steering Wheel Cover", "Cargo Net", "Ice Scraper", "Wiper Blades"],
        (6.99, 129.99),
    ),
    "Pet Supplies": (
        ["Dog Bed", "Cat Tower", "Pet Shampoo", "Chew Toy",
         "Automatic Feeder", "Leash Set", "Fish Tank Filter", "Bird Perch",
         "Grooming Kit", "Travel Carrier", "Training Pads", "Catnip Toy",
         "Water Fountain", "Collar Tag", "Treat Dispenser"],
        (4.99, 99.99),
    ),
}

# Variant keys per category — fashion gets color-size combos (needed for Q4)
FASHION_COLORS = ["black", "white", "blue", "red", "aqua", "navy", "green", "pink"]
FASHION_SIZES = ["S", "M", "L", "XL"]
ELECTRONICS_VARIANTS = ["black", "white", "silver", "space-gray"]
HOME_VARIANTS = ["default", "natural", "white", "black"]
GENERAL_VARIANTS = ["default"]

VARIANT_MAP = {
    "Electronics": ELECTRONICS_VARIANTS,
    "Fashion": None,           # special: color-size combos
    "Home Decor": HOME_VARIANTS,
    "Sports & Outdoors": GENERAL_VARIANTS,
    "Books": ["default"],
    "Toys & Games": GENERAL_VARIANTS,
    "Beauty": GENERAL_VARIANTS,
    "Grocery": GENERAL_VARIANTS,
    "Automotive": GENERAL_VARIANTS,
    "Pet Supplies": GENERAL_VARIANTS,
}

FIRST_NAMES = [
    "Sarah", "Mike", "Ava", "James", "Emma", "Liam", "Olivia", "Noah",
    "Sophia", "Lucas", "Mia", "Ethan", "Isabella", "Mason", "Charlotte",
    "Logan", "Amelia", "Aiden", "Harper", "Elijah", "Evelyn", "Jackson",
    "Luna", "Sebastian", "Aria", "Mateo", "Chloe", "Henry", "Penelope",
    "Owen", "Layla", "Alexander", "Riley", "Daniel", "Zoey", "William",
    "Nora", "Jack", "Lily", "Benjamin", "Eleanor", "Leo", "Hannah",
    "Caleb", "Hazel", "Ryan", "Violet", "Nathan", "Aurora", "Dylan",
]
LAST_NAMES = [
    "Connor", "Lee", "Patel", "Smith", "Johnson", "Williams", "Brown",
    "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
    "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "White", "Harris", "Thompson",
    "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King",
    "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
    "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Chen",
]

STREETS = [
    "Lake Shore Dr", "Main St", "Broadway", "Market St", "Elm St",
    "Oak Ave", "Pine Rd", "Maple Blvd", "Cedar Ln", "Walnut Way",
    "Park Ave", "River Rd", "Hill St", "Spring St", "Sunset Blvd",
]
CITIES_STATES = [
    ("Chicago", "IL", "606"), ("San Francisco", "CA", "941"),
    ("New York", "NY", "100"), ("Austin", "TX", "787"),
    ("Seattle", "WA", "981"), ("Denver", "CO", "802"),
    ("Portland", "OR", "972"), ("Boston", "MA", "021"),
    ("Miami", "FL", "331"), ("Nashville", "TN", "372"),
]

RETURN_REASONS = [
    "Too small", "Too large", "Wrong color", "Defective item",
    "Not as described", "Changed my mind", "Arrived damaged",
    "Better price found", "Duplicate order", "Not satisfied",
]


def wcsv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def make_fashion_variants():
    """Generate 2-4 color-size variant keys for a fashion product."""
    n_colors = random.randint(1, 3)
    n_sizes = random.randint(2, 4)
    colors = random.sample(FASHION_COLORS, n_colors)
    sizes = random.sample(FASHION_SIZES, n_sizes)
    return [f"{c}-{s}" for c in colors for s in sizes]


def main():
    cat_names = [c[0] for c in CATEGORIES]

    # ------------------------------------------------------------------
    # Users — sarah@example.com is always user_id=1
    # ------------------------------------------------------------------
    users = []
    users.append(["sarah@example.com", "$2b$12$dummyhashsarah", "Sarah", "Connor"])
    users.append(["mike@example.com", "$2b$12$dummyhashmike", "Mike", "Lee"])
    users.append(["ava@example.com", "$2b$12$dummyhashava", "Ava", "Patel"])

    used_emails = {"sarah@example.com", "mike@example.com", "ava@example.com"}
    for i in range(4, N_USERS + 1):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        email = f"{first.lower()}.{last.lower()}{i}@example.com"
        while email in used_emails:
            email = f"{first.lower()}.{last.lower()}{random.randint(1000, 9999)}@example.com"
        used_emails.add(email)
        users.append([email, "$2b$12$dummyscalehash", first, last])

    wcsv(f"{OUT_DIR}/users.csv",
         ["email", "password_hash", "first_name", "last_name"], users)

    # ------------------------------------------------------------------
    # Categories
    # ------------------------------------------------------------------
    wcsv(f"{OUT_DIR}/categories.csv", ["name", "slug"], CATEGORIES)

    # ------------------------------------------------------------------
    # Products — round-robin across categories, realistic names
    # ------------------------------------------------------------------
    products = []
    for i in range(1, N_PRODUCTS + 1):
        cat_id = ((i - 1) % len(CATEGORIES)) + 1
        cat_name = cat_names[cat_id - 1]
        templates, (lo, hi) = PRODUCT_TEMPLATES[cat_name]
        base_name = random.choice(templates)
        name = f"{base_name} #{i}"
        price = round(random.uniform(lo, hi), 2)
        products.append([cat_id, name,
                         f"{base_name} - quality {cat_name.lower()} product",
                         price, f"https://img/p{i}", 1])

    wcsv(f"{OUT_DIR}/products.csv",
         ["category_id", "name", "description", "base_price", "image_url", "is_active"],
         products)

    # ------------------------------------------------------------------
    # Inventory — fashion gets color-size variants; ~10% low stock for Q3
    # ------------------------------------------------------------------
    inventory = []
    for pid in range(1, N_PRODUCTS + 1):
        cat_id = products[pid - 1][0]
        cat_name = cat_names[cat_id - 1]

        if cat_name == "Fashion":
            variants = make_fashion_variants()
        else:
            pool = VARIANT_MAP[cat_name]
            variants = random.sample(pool, random.randint(1, len(pool)))

        for vk in variants:
            qty = random.randint(0, 4) if random.random() < 0.10 else random.randint(5, 200)
            inventory.append([pid, vk, qty, 5])

    wcsv(f"{OUT_DIR}/inventory.csv",
         ["product_id", "variant_key", "quantity", "low_stock_threshold"],
         inventory)

    # ------------------------------------------------------------------
    # Addresses — 1-2 per user; Sarah's pinned to match seed
    # ------------------------------------------------------------------
    addresses = []
    user_addr_map = {}   # uid -> [address_id, ...]
    addr_id = 0
    for uid in range(1, N_USERS + 1):
        n_addr = 2 if uid <= 3 else random.choices([1, 2], weights=[0.8, 0.2])[0]
        city, state, zip_pre = random.choice(CITIES_STATES)
        user_addr_map[uid] = []
        for j in range(n_addr):
            addr_id += 1
            street = f"{random.randint(1, 9999)} {random.choice(STREETS)}"
            zipcode = f"{zip_pre}{random.randint(10, 99)}"
            addresses.append([uid, street, city, state, zipcode, "USA",
                              1 if j == 0 else 0])
            user_addr_map[uid].append(addr_id)

    # Pin Sarah's addresses
    addresses[0] = [1, "123 Lake Shore Dr", "Chicago", "IL", "60601", "USA", 1]
    addresses[1] = [1, "500 W Madison St", "Chicago", "IL", "60661", "USA", 0]

    wcsv(f"{OUT_DIR}/addresses.csv",
         ["user_id", "street", "city", "state", "zip_code", "country", "is_default"],
         addresses)

    # ------------------------------------------------------------------
    # Payment methods — 1-2 per user; Sarah's pinned
    # ------------------------------------------------------------------
    payment_methods = []
    user_pm_map = {}     # uid -> [pm_id, ...]
    pm_id = 0
    for uid in range(1, N_USERS + 1):
        n_pm = 2 if uid == 1 else random.choices([1, 2], weights=[0.85, 0.15])[0]
        user_pm_map[uid] = []
        for j in range(n_pm):
            pm_id += 1
            if j == 0:
                method, last4 = "credit_card", str(random.randint(1000, 9999))
            else:
                method = random.choice(["credit_card", "paypal", "debit_card"])
                last4 = str(random.randint(1000, 9999)) if method != "paypal" else ""
            payment_methods.append([uid, method, last4, 1 if j == 0 else 0])
            user_pm_map[uid].append(pm_id)

    payment_methods[0] = [1, "credit_card", "4242", 1]
    payment_methods[1] = [1, "paypal", "", 0]

    wcsv(f"{OUT_DIR}/payment_methods.csv",
         ["user_id", "method_type", "last_four", "is_default"],
         payment_methods)

    # ------------------------------------------------------------------
    # Orders + order_items + returns
    # ------------------------------------------------------------------
    orders = []
    order_items = []
    returns = []
    base_date = datetime(2025, 1, 1)
    order_id = 0
    order_item_id = 0

    def create_order(uid, status_override=None, created_override=None):
        nonlocal order_id, order_item_id

        pmid = random.choice(user_pm_map[uid])
        addrid = random.choice(user_addr_map[uid])
        shipping_opt = random.choice(["standard", "expedited", "overnight"])
        ship_cost = {"standard": 8.99, "expedited": 12.99, "overnight": 19.99}[shipping_opt]

        created = created_override or (
            base_date + timedelta(days=random.randint(0, 420),
                                  minutes=random.randint(0, 1440)))
        status = status_override or random.choices(
            ["confirmed", "shipped", "delivered"], weights=[0.2, 0.3, 0.5])[0]

        k = max(1, int(random.gauss(AVG_ITEMS_PER_ORDER, 1)))
        subtotal = 0.0
        items = []
        for _ in range(k):
            pid = random.randint(1, N_PRODUCTS)
            cat_name = cat_names[products[pid - 1][0] - 1]
            if cat_name == "Fashion":
                vk = f"{random.choice(FASHION_COLORS)}-{random.choice(FASHION_SIZES)}"
            else:
                vk = random.choice(VARIANT_MAP[cat_name])
            qty = random.randint(1, 3)
            unit_price = float(products[pid - 1][3])
            subtotal += unit_price * qty
            items.append((pid, vk, qty, unit_price))

        tax = round(subtotal * 0.08, 2)
        total = round(subtotal + tax + ship_cost, 2)
        expected = (created.date() + timedelta(days=random.randint(2, 7))).isoformat()

        order_id += 1
        orders.append([uid, pmid, addrid, shipping_opt,
                       round(subtotal, 2), tax, ship_cost, total, status,
                       expected, created.strftime("%Y-%m-%d %H:%M:%S")])

        for (pid, vk, qty, unit_price) in items:
            order_item_id += 1
            order_items.append([order_id, pid, vk, qty, unit_price])
            if status == "delivered" and random.random() < RETURN_RATE:
                refund = round(unit_price * qty * 0.9, 2)
                fee = round(unit_price * qty - refund, 2)
                returns.append([order_item_id, random.choice(RETURN_REASONS),
                                random.choice(["refunded", "initiated", "denied"]),
                                refund, fee,
                                (created + timedelta(days=random.randint(5, 30)))
                                .strftime("%Y-%m-%d %H:%M:%S")])

    # --- Guaranteed Sarah orders (Q8 / Q9 need these) ---
    create_order(1, "delivered", datetime(2026, 2, 5, 10, 0, 0))
    create_order(1, "delivered", datetime(2026, 2, 15, 12, 0, 0))
    create_order(1, "confirmed", datetime(2026, 2, 24, 9, 30, 0))

    # Guarantee at least one return for Sarah
    sarah_has_return = any(
        oi[0] <= 2 for oi in [r for r in returns]  # order_item_ids from orders 1-2
    )
    if not sarah_has_return:
        oi = order_items[0]  # first item from Sarah's first order
        unit_price, qty = float(oi[4]), int(oi[3])
        refund = round(unit_price * qty * 0.9, 2)
        fee = round(unit_price * qty - refund, 2)
        returns.append([1, "Too small", "refunded", refund, fee,
                        "2026-02-20 14:00:00"])

    # --- Remaining orders across all users ---
    for _ in range(N_ORDERS - order_id):
        create_order(random.randint(1, N_USERS))

    wcsv(f"{OUT_DIR}/orders.csv",
         ["user_id", "payment_method_id", "shipping_address_id", "shipping_option",
          "subtotal", "tax", "shipping_cost", "total", "status",
          "expected_delivery", "created_at"],
         orders)
    wcsv(f"{OUT_DIR}/order_items.csv",
         ["order_id", "product_id", "variant_key", "quantity", "unit_price"],
         order_items)
    wcsv(f"{OUT_DIR}/returns.csv",
         ["order_item_id", "reason", "status", "refund_amount", "restocking_fee",
          "created_at"],
         returns)

    # ------------------------------------------------------------------
    print("CSV generation done.")
    print(f"  Users:           {len(users)}")
    print(f"  Categories:      {len(CATEGORIES)}")
    print(f"  Products:        {len(products)}")
    print(f"  Inventory rows:  {len(inventory)}")
    print(f"  Addresses:       {len(addresses)}")
    print(f"  Payment methods: {len(payment_methods)}")
    print(f"  Orders:          {len(orders)}")
    print(f"  Order items:     {len(order_items)}")
    print(f"  Returns:         {len(returns)}")
    print(f"Output directory:  {OUT_DIR}")


if __name__ == "__main__":
    main()
