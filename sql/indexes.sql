-- indexes.sql (MySQL 8+)
-- Purpose: baseline + performance indexes for the required query set.
-- Note: PRIMARY KEY / UNIQUE constraints already create indexes automatically.
-- (e.g., users.email UNIQUE, inventory UNIQUE(product_id, variant_key),
--  order_items UNIQUE(order_id, product_id, variant_key), returns UNIQUE(order_item_id))

/* ----------------------------
   USERS / ADDRESSES / PAYMENTS
----------------------------- */
CREATE INDEX idx_addresses_user_default
  ON addresses (user_id, is_default);

CREATE INDEX idx_payment_methods_user_default
  ON payment_methods (user_id, is_default);

/* ----------------------------
   PRODUCTS / CATEGORIES
----------------------------- */
-- Supports category browsing and joins
CREATE INDEX idx_products_category_active
  ON products (category_id, is_active);

-- Optional: helps if you sort/filter products by creation time often
CREATE INDEX idx_products_created_at
  ON products (created_at);

/* ----------------------------
   INVENTORY / STOCK
----------------------------- */
-- Low-stock query (quantity < 5)
CREATE INDEX idx_inventory_quantity
  ON inventory (quantity);

-- Optional: if you frequently filter by variant_key across products
CREATE INDEX idx_inventory_variant_key
  ON inventory (variant_key);

/* ----------------------------
   ORDERS
----------------------------- */
-- Common: fetch a user's orders, most recent first
CREATE INDEX idx_orders_user_created
  ON orders (user_id, created_at);

-- Time-window queries (e.g., last 30 days)
CREATE INDEX idx_orders_created_at
  ON orders (created_at);

-- Optional: status dashboards / fulfillment queues
CREATE INDEX idx_orders_status_created
  ON orders (status, created_at);

/* ----------------------------
   ORDER ITEMS
----------------------------- */
-- Join orders -> order_items fast
CREATE INDEX idx_order_items_order_id
  ON order_items (order_id);

-- Join products -> order_items fast (popularity / co-purchase base)
CREATE INDEX idx_order_items_product_id
  ON order_items (product_id);

-- Co-purchase patterns: “bought together with X” benefits from (product_id, order_id)
CREATE INDEX idx_order_items_product_order
  ON order_items (product_id, order_id);

/* ----------------------------
   RETURNS
----------------------------- */
-- Returns by status or time
CREATE INDEX idx_returns_status_created
  ON returns (status, created_at);

CREATE INDEX idx_returns_created_at
  ON returns (created_at);
