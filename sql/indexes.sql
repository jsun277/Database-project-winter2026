-- indexes.sql

CREATE INDEX idx_addresses_user_default
  ON addresses (user_id, is_default);

CREATE INDEX idx_payment_methods_user_default
  ON payment_methods (user_id, is_default);

CREATE INDEX idx_products_category_active
  ON products (category_id, is_active);

CREATE INDEX idx_products_created_at
  ON products (created_at);

CREATE INDEX idx_inventory_quantity
  ON inventory (quantity);

CREATE INDEX idx_inventory_variant_key
  ON inventory (variant_key);

CREATE INDEX idx_orders_user_created
  ON orders (user_id, created_at);

CREATE INDEX idx_orders_created_at
  ON orders (created_at);

CREATE INDEX idx_orders_status_created
  ON orders (status, created_at);

CREATE INDEX idx_order_items_order_id
  ON order_items (order_id);

CREATE INDEX idx_order_items_product_id
  ON order_items (product_id);

CREATE INDEX idx_order_items_product_order
  ON order_items (product_id, order_id);

CREATE INDEX idx_returns_status_created
  ON returns (status, created_at);

CREATE INDEX idx_returns_created_at
  ON returns (created_at);