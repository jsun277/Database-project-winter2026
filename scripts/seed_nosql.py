"""
NoSQL Seed Script — Juniper
Seeds MongoDB, Redis, and Neo4j from SQL CSVs.

Requires:
  pip install pymongo redis neo4j faker

Usage:
  python seed_nosql.py <csv_directory> [neo4j_password]

Example:
  python seed_nosql.py ./csv_data myNeo4jPass
"""

import csv, random, json, sys, os, time
from datetime import datetime, timedelta
from collections import defaultdict
from itertools import combinations

try:
    from pymongo import MongoClient
    from faker import Faker
    import redis as redis_lib
    from neo4j import GraphDatabase
except ImportError as e:
    print(f"Missing: {e}\nRun: pip install pymongo redis neo4j faker")
    sys.exit(1)

fake = Faker()
Faker.seed(42)
random.seed(42)

# ── Config ────────────────────────────────────────────────────
CSV_DIR = sys.argv[1] if len(sys.argv) > 1 else "."
NEO4J_PASS = sys.argv[2] if len(sys.argv) > 2 else "password"

MONGO_URI    = "mongodb://localhost:27017/"
REDIS_HOST   = "localhost"
REDIS_PORT   = 6379
NEO4J_URI    = "bolt://localhost:7687"
NEO4J_USER   = "neo4j"

SARAH_ID = 1
NUM_USERS = 1000
NUM_PRODUCTS = 5000

# ── Load CSVs ─────────────────────────────────────────────────
def load_csv(name):
    path = os.path.join(CSV_DIR, name)
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

print("Loading CSVs...")
categories_csv  = load_csv("categories.csv")
products_csv    = load_csv("products.csv")
inventory_csv   = load_csv("inventory.csv")
orders_csv      = load_csv("orders.csv")
order_items_csv = load_csv("order_items.csv")
users_csv       = load_csv("users.csv")

# Build lookups
product_info = {}
for i, row in enumerate(products_csv, 1):
    product_info[i] = {
        "category_id": int(row["category_id"].strip()),
        "name": row["name"].strip(),
        "base_price": float(row["base_price"].strip()),
    }

cat_names = {}
for i, row in enumerate(categories_csv, 1):
    cat_names[i] = row["name"].strip()

inv_by_product = defaultdict(list)
for row in inventory_csv:
    pid = int(row["product_id"].strip())
    inv_by_product[pid].append({
        "variant_key": row["variant_key"].strip(),
        "quantity": int(row["quantity"].strip()),
    })

order_products = defaultdict(list)
for row in order_items_csv:
    oid = int(row["order_id"].strip())
    pid = int(row["product_id"].strip())
    order_products[oid].append(pid)

order_user = {}
for i, row in enumerate(orders_csv, 1):
    order_user[i] = int(row["user_id"].strip())

user_names = {}
for i, row in enumerate(users_csv, 1):
    user_names[i] = f"{row['first_name'].strip()} {row['last_name'].strip()}"

print(f"  {len(product_info)} products, {len(categories_csv)} categories")
print(f"  {len(order_products)} orders, {len(order_items_csv)} order items")
print(f"  {len(inv_by_product)} products with inventory")


# ══════════════════════════════════════════════════════════════
#  MONGODB
# ══════════════════════════════════════════════════════════════
print("\n═══ MongoDB ═════════════════════════════════════════")
mongo = MongoClient(MONGO_URI)
db = mongo["ecommerce"]

# ── product_attributes (5,000 docs) ──────────────────────────
print("Seeding product_attributes...")

ATTR_TEMPLATES = {
    1: lambda: {
        "battery_life": random.choice(["5h","10h","15h","20h","30h","40h","50h"]),
        "connectivity": random.choice(["Bluetooth 5.0","Bluetooth 5.3","USB-C","Wi-Fi","Wired"]),
        "weight": f"{random.randint(50,800)}g",
        "warranty": random.choice(["1 year","2 years","3 years"]),
        "noise_cancelling": random.choice([True, False]),
    },
    2: lambda: {
        "material": random.choice(["Cotton","Polyester","Silk","Linen","Wool","Denim","Cashmere"]),
        "care": random.choice(["Machine wash cold","Hand wash","Dry clean only"]),
        "style": random.choice(["A-line","Fitted","Oversized","Slim fit","Regular","Relaxed"]),
        "season": random.choice(["Spring","Summer","Fall","Winter","All-season"]),
    },
    3: lambda: {
        "dimensions": f'{random.randint(3,40)}x{random.randint(3,30)}x{random.randint(2,20)} in',
        "material": random.choice(["Ceramic","Glass","Wood","Metal","Rattan","Fabric","Stone"]),
        "weight": f"{round(random.uniform(0.2,10.0),1)} kg",
        "care": random.choice(["Wipe clean","Hand wash","Dishwasher safe","Dust only"]),
    },
    4: lambda: {
        "weight": f"{round(random.uniform(0.1,5.0),1)} kg",
        "material": random.choice(["Nylon","Polyester","Rubber","Carbon fiber","Aluminum","Steel"]),
        "waterproof": random.choice([True, False]),
        "size": random.choice(["One size","S-XL","Adjustable"]),
    },
    5: lambda: {
        "format": random.choice(["Hardcover","Paperback","Digital","Audiobook"]),
        "pages": random.randint(80, 900),
        "language": random.choice(["English","Spanish","French","Bilingual"]),
        "publisher": random.choice(["O'Reilly","Penguin","HarperCollins","Wiley","No Starch"]),
    },
    6: lambda: {
        "age_range": random.choice(["3+","6+","8+","12+","16+","All ages"]),
        "players": random.choice(["1","1-2","2-4","2-6","1-8"]),
        "material": random.choice(["Plastic","Wood","Cardboard","Plush","Mixed"]),
        "battery_required": random.choice([True, False]),
    },
    7: lambda: {
        "volume": f"{random.choice([15,30,50,100,200,500])} ml",
        "skin_type": random.choice(["All","Oily","Dry","Sensitive","Combination"]),
        "organic": random.choice([True, False]),
        "scent": random.choice(["Unscented","Floral","Citrus","Woody","Fresh"]),
    },
    8: lambda: {
        "weight": f"{random.choice([100,200,250,500,1000])}g",
        "organic": random.choice([True, False]),
        "allergens": random.choice(["None","Gluten","Nuts","Dairy","Soy"]),
        "shelf_life": random.choice(["6 months","1 year","2 years","3 months"]),
    },
    9: lambda: {
        "compatibility": random.choice(["Universal","Sedan","SUV","Truck","Compact"]),
        "material": random.choice(["Rubber","Plastic","Leather","Metal","Microfiber"]),
        "warranty": random.choice(["6 months","1 year","2 years","Lifetime"]),
        "color": random.choice(["Black","Gray","Beige","Carbon"]),
    },
    10: lambda: {
        "pet_type": random.choice(["Dog","Cat","Bird","Fish","Small animal","Universal"]),
        "material": random.choice(["Plastic","Fabric","Wood","Stainless steel","Rope"]),
        "size": random.choice(["Small","Medium","Large","XL","Adjustable"]),
        "washable": random.choice([True, False]),
    },
}

product_attrs = []
for pid in range(1, NUM_PRODUCTS + 1):
    info = product_info[pid]
    cat_id = info["category_id"]
    gen = ATTR_TEMPLATES.get(cat_id, ATTR_TEMPLATES[1])

    variants = []
    for inv in inv_by_product.get(pid, [{"variant_key": "default"}]):
        vk = inv["variant_key"] if isinstance(inv, dict) else inv
        variant = {"key": vk, "sku": f"C{cat_id}-{pid}-{vk.upper()[:6]}"}
        if "-" in vk and cat_id == 2:
            parts = vk.split("-", 1)
            variant["color"] = parts[0].title()
            variant["size"] = parts[1].upper()
        elif vk != "default":
            variant["color"] = vk.replace("-", " ").title()
        variants.append(variant)

    if not variants:
        variants = [{"key": "default", "sku": f"C{cat_id}-{pid}-DEF"}]

    product_attrs.append({
        "product_id": pid,
        "category_id": cat_id,
        "category": cat_names.get(cat_id, f"Category{cat_id}"),
        "attributes": gen(),
        "variants": variants,
    })

db.product_attributes.drop()
db.product_attributes.insert_many(product_attrs)
db.product_attributes.create_index("product_id", unique=True)
db.product_attributes.create_index("category_id")
db.product_attributes.create_index("category")
print(f"  ✓ {len(product_attrs)} product_attributes docs")

# ── carts ─────────────────────────────────────────────────────
print("Seeding carts...")
cart_users = random.sample(range(1, NUM_USERS + 1), k=200)
if SARAH_ID not in cart_users:
    cart_users[0] = SARAH_ID

carts = []
for uid in cart_users:
    items = []
    for _ in range(random.randint(1, 5)):
        pid = random.randint(1, NUM_PRODUCTS)
        inv_list = inv_by_product.get(pid, [])
        vk = random.choice(inv_list)["variant_key"] if inv_list else "default"
        items.append({
            "product_id": pid,
            "variant_key": vk,
            "quantity": random.randint(1, 3),
            "price": product_info[pid]["base_price"],
            "added_at": fake.date_time_between(start_date="-7d", end_date="now").isoformat() + "Z",
        })
    ts = fake.date_time_between(start_date="-7d", end_date="now")
    carts.append({
        "user_id": uid,
        "items": items,
        "device": random.choice(["tablet", "laptop", "mobile"]),
        "updated_at": ts.isoformat() + "Z",
        "created_at": (ts - timedelta(hours=random.randint(1, 48))).isoformat() + "Z",
    })

db.carts.drop()
db.carts.insert_many(carts)
db.carts.create_index("user_id", unique=True)
print(f"  ✓ {len(carts)} cart docs")

# ── user_events (500K) ────────────────────────────────────────
print("Seeding user_events (500K)...")
EVENT_TYPES   = ["product_view", "search", "click", "add_to_cart", "purchase"]
EVENT_WEIGHTS = [0.45, 0.20, 0.20, 0.10, 0.05]
DEVICES       = ["tablet", "laptop", "mobile"]
REFERRERS     = ["category_page", "search_results", "homepage", "recommendation", "direct", "external"]
SEARCH_TERMS  = [
    "headphones","wireless earbuds","summer dress","blue dress","ceramic vase",
    "running shoes","laptop stand","phone case","watch","backpack","sunglasses",
    "sneakers","candle","throw pillow","desk lamp","bluetooth speaker","yoga mat",
    "water bottle","tote bag","wall art","cat tower","dog food","car vacuum",
    "board game","face cream","cookbook","protein bar","fishing rod","perfume",
]

db.user_events.drop()
BATCH = 10000
total = 0
batch = []
t0 = time.time()

for i in range(500_000):
    uid = SARAH_ID if random.random() < 0.05 else random.randint(1, NUM_USERS)
    etype = random.choices(EVENT_TYPES, weights=EVENT_WEIGHTS, k=1)[0]
    ts = fake.date_time_between(start_date="-6M", end_date="now")

    event = {
        "user_id": uid,
        "event_type": etype,
        "timestamp": ts,
        "device": random.choice(DEVICES),
        "metadata": {"referrer": random.choice(REFERRERS)},
    }

    if etype == "search":
        term = random.choice(SEARCH_TERMS)
        event["search_query"] = term
        event["product_id"] = None
        event["page_url"] = f"/search?q={term.replace(' ', '+')}"
        event["duration_seconds"] = None
    else:
        pid = random.randint(1, NUM_PRODUCTS)
        event["product_id"] = pid
        event["search_query"] = None
        cat_id = product_info[pid]["category_id"]
        slug = cat_names.get(cat_id, "misc").lower().replace(" & ", "-").replace(" ", "-")
        event["page_url"] = f"/products/{slug}/{pid}"
        event["duration_seconds"] = random.randint(3, 180) if etype == "product_view" else None
        if etype in ("product_view", "click"):
            event["metadata"]["position_in_list"] = random.randint(1, 20)

    batch.append(event)
    if len(batch) >= BATCH:
        db.user_events.insert_many(batch)
        total += len(batch)
        batch = []
        if total % 100_000 == 0:
            print(f"    {total:,}/500,000  ({time.time()-t0:.0f}s)")

if batch:
    db.user_events.insert_many(batch)
    total += len(batch)

db.user_events.create_index([("user_id", 1), ("timestamp", -1)])
db.user_events.create_index([("event_type", 1), ("timestamp", -1)])
db.user_events.create_index([("product_id", 1), ("event_type", 1)])
db.user_events.create_index("timestamp")
print(f"  ✓ {total:,} user_events ({time.time()-t0:.0f}s)")

print(f"\nMongoDB summary:")
for col in ["product_attributes", "carts", "user_events"]:
    print(f"  {col}: {db[col].count_documents({}):,}")
mongo.close()


# ══════════════════════════════════════════════════════════════
#  REDIS
# ══════════════════════════════════════════════════════════════
print("\n═══ Redis ═══════════════════════════════════════════")
r = redis_lib.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
r.flushdb()

# ── Sessions ──────────────────────────────────────────────────
print("Seeding sessions...")
DEVICES = ["tablet", "laptop", "mobile"]
session_users = random.sample(range(1, NUM_USERS + 1), k=150)
if SARAH_ID not in session_users:
    session_users[0] = SARAH_ID

for uid in session_users:
    device = random.choice(DEVICES)
    cart_doc = next((c for c in carts if c["user_id"] == uid), None)
    cart_items = cart_doc["items"] if cart_doc else []
    recently_viewed = [random.randint(1, NUM_PRODUCTS) for _ in range(random.randint(3, 10))]

    session_data = {
        "user_id": uid,
        "active_device": device,
        "devices": list(set([device, random.choice(DEVICES)])),
        "cart": {"items": cart_items[:5], "updated_at": datetime.now().isoformat() + "Z"},
        "recently_viewed": recently_viewed,
        "last_activity": datetime.now().isoformat() + "Z",
    }
    r.set(f"session:{uid}", json.dumps(session_data, default=str))
    r.expire(f"session:{uid}", 86400)

print(f"  ✓ {len(session_users)} sessions")

# ── Cart cache ────────────────────────────────────────────────
print("Seeding cart cache...")
for cart in carts:
    r.set(f"cart:{cart['user_id']}", json.dumps(cart, default=str))
    r.expire(f"cart:{cart['user_id']}", 86400)
print(f"  ✓ {len(carts)} carts")

# ── Stock counters ────────────────────────────────────────────
print("Seeding stock counters...")
stock_count = 0
for row in inventory_csv:
    pid = row["product_id"].strip()
    vk = row["variant_key"].strip()
    qty = row["quantity"].strip()
    r.set(f"stock:{pid}:{vk}", qty)
    r.expire(f"stock:{pid}:{vk}", 60)
    stock_count += 1
print(f"  ✓ {stock_count} stock counters")

# ── Recently viewed ───────────────────────────────────────────
print("Seeding recently viewed...")
rv_users = random.sample(range(1, NUM_USERS + 1), k=300)
if SARAH_ID not in rv_users:
    rv_users[0] = SARAH_ID
for uid in rv_users:
    key = f"views:{uid}"
    r.delete(key)
    r.rpush(key, *[str(random.randint(1, NUM_PRODUCTS)) for _ in range(random.randint(3, 15))])
    r.expire(key, 604800)
print(f"  ✓ {len(rv_users)} recently-viewed lists")

print(f"\nRedis summary: {r.dbsize()} keys")


# ══════════════════════════════════════════════════════════════
#  NEO4J
# ══════════════════════════════════════════════════════════════
print("\n═══ Neo4j ═══════════════════════════════════════════")
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))

with driver.session() as session:
    print("Clearing existing data...")
    session.run("MATCH (n) DETACH DELETE n")

    print("Creating constraints...")
    for q in [
        "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.user_id IS UNIQUE",
        "CREATE CONSTRAINT product_id IF NOT EXISTS FOR (p:Product) REQUIRE p.product_id IS UNIQUE",
        "CREATE CONSTRAINT category_name IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE",
    ]:
        try:
            session.run(q)
        except Exception:
            pass

    # Categories
    print("Creating category nodes...")
    for i, row in enumerate(categories_csv, 1):
        session.run("CREATE (:Category {category_id: $cid, name: $name})", cid=i, name=row["name"].strip())
    print(f"  ✓ {len(categories_csv)} categories")

    # Users (batch)
    print("Creating user nodes...")
    ubatch = []
    for i, row in enumerate(users_csv, 1):
        ubatch.append({"user_id": i, "name": f"{row['first_name'].strip()} {row['last_name'].strip()}"})
        if len(ubatch) >= 500:
            session.run("UNWIND $b AS u CREATE (:User {user_id: u.user_id, name: u.name})", b=ubatch)
            ubatch = []
    if ubatch:
        session.run("UNWIND $b AS u CREATE (:User {user_id: u.user_id, name: u.name})", b=ubatch)
    print(f"  ✓ {len(users_csv)} users")

    # Products + BELONGS_TO (batch)
    print("Creating product nodes...")
    pbatch = []
    for pid in range(1, NUM_PRODUCTS + 1):
        info = product_info[pid]
        pbatch.append({
            "product_id": pid, "name": info["name"],
            "category": cat_names.get(info["category_id"], "Unknown"),
            "category_id": info["category_id"],
        })
        if len(pbatch) >= 500:
            session.run("""
                UNWIND $b AS p
                CREATE (prod:Product {product_id: p.product_id, name: p.name, category: p.category})
                WITH prod, p
                MATCH (c:Category {category_id: p.category_id})
                CREATE (prod)-[:BELONGS_TO]->(c)
            """, b=pbatch)
            pbatch = []
    if pbatch:
        session.run("""
            UNWIND $b AS p
            CREATE (prod:Product {product_id: p.product_id, name: p.name, category: p.category})
            WITH prod, p
            MATCH (c:Category {category_id: p.category_id})
            CREATE (prod)-[:BELONGS_TO]->(c)
        """, b=pbatch)
    print(f"  ✓ {NUM_PRODUCTS} products + BELONGS_TO")

    # PURCHASED edges
    print("Creating PURCHASED relationships...")
    t0 = time.time()
    purch_batch = []
    purch_count = 0
    for oid, pids in order_products.items():
        uid = order_user.get(oid)
        if uid is None:
            continue
        odate = orders_csv[oid - 1]["created_at"].strip() if oid <= len(orders_csv) else "2026-01-01"
        for pid in pids:
            purch_batch.append({"user_id": uid, "product_id": pid, "order_id": oid, "date": odate})
        if len(purch_batch) >= 2000:
            session.run("""
                UNWIND $b AS p
                MATCH (u:User {user_id: p.user_id})
                MATCH (prod:Product {product_id: p.product_id})
                CREATE (u)-[:PURCHASED {order_id: p.order_id, date: p.date}]->(prod)
            """, b=purch_batch)
            purch_count += len(purch_batch)
            purch_batch = []
            if purch_count % 50000 == 0:
                print(f"    {purch_count:,} edges...")
    if purch_batch:
        session.run("""
            UNWIND $b AS p
            MATCH (u:User {user_id: p.user_id})
            MATCH (prod:Product {product_id: p.product_id})
            CREATE (u)-[:PURCHASED {order_id: p.order_id, date: p.date}]->(prod)
        """, b=purch_batch)
        purch_count += len(purch_batch)
    print(f"  ✓ {purch_count:,} PURCHASED edges ({time.time()-t0:.0f}s)")

    # FREQUENTLY_BOUGHT_WITH
    print("Computing co-purchase relationships...")
    t0 = time.time()
    co_purchase = defaultdict(int)
    for oid, pids in order_products.items():
        uniq = list(set(pids))
        if len(uniq) < 2:
            continue
        for p1, p2 in combinations(sorted(uniq[:10]), 2):
            co_purchase[(p1, p2)] += 1

    significant = {k: v for k, v in co_purchase.items() if v >= 3}
    print(f"  {len(significant):,} significant pairs")

    fbw_batch = []
    fbw_count = 0
    for (p1, p2), count in significant.items():
        conf = round(count / max(sum(1 for ps in order_products.values() if p1 in ps), 1), 3)
        fbw_batch.append({"p1": p1, "p2": p2, "count": count, "confidence": conf})
        if len(fbw_batch) >= 1000:
            session.run("""
                UNWIND $b AS x
                MATCH (a:Product {product_id: x.p1})
                MATCH (b:Product {product_id: x.p2})
                CREATE (a)-[:FREQUENTLY_BOUGHT_WITH {count: x.count, confidence: x.confidence}]->(b)
                CREATE (b)-[:FREQUENTLY_BOUGHT_WITH {count: x.count, confidence: x.confidence}]->(a)
            """, b=fbw_batch)
            fbw_count += len(fbw_batch)
            fbw_batch = []
    if fbw_batch:
        session.run("""
            UNWIND $b AS x
            MATCH (a:Product {product_id: x.p1})
            MATCH (b:Product {product_id: x.p2})
            CREATE (a)-[:FREQUENTLY_BOUGHT_WITH {count: x.count, confidence: x.confidence}]->(b)
            CREATE (b)-[:FREQUENTLY_BOUGHT_WITH {count: x.count, confidence: x.confidence}]->(a)
        """, b=fbw_batch)
        fbw_count += len(fbw_batch)
    print(f"  ✓ {fbw_count * 2:,} FREQUENTLY_BOUGHT_WITH edges ({time.time()-t0:.0f}s)")

    # Summary
    print("\nNeo4j summary:")
    for rec in session.run("MATCH (n) RETURN labels(n)[0] AS l, COUNT(*) AS c"):
        print(f"  {rec['l']}: {rec['c']:,}")
    for rec in session.run("MATCH ()-[r]->() RETURN type(r) AS t, COUNT(*) AS c"):
        print(f"  {rec['t']}: {rec['c']:,}")

driver.close()


# ══════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("✅ ALL NoSQL STORES SEEDED SUCCESSFULLY")
print("=" * 55)
print(f"""
Verify in DataGrip (MongoDB):
  db.product_attributes.findOne({{product_id: 1}})
  db.user_events.countDocuments({{}})
  db.carts.findOne({{user_id: 1}})

Verify in DataGrip (Redis):
  GET session:1
  GET stock:1:black
  LRANGE views:1 0 -1

Verify in Neo4j Desktop:
  MATCH (u:User {{user_id: 1}})-[:PURCHASED]->(p) RETURN p.name LIMIT 10
  MATCH (p1)-[r:FREQUENTLY_BOUGHT_WITH]->(p2)
    RETURN p1.name, p2.name, r.count ORDER BY r.count DESC LIMIT 10
""")
