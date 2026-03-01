USE ecommerce;

SHOW TABLES;

SELECT COUNT(*) AS users FROM users;
SELECT COUNT(*) AS categories FROM categories;
SELECT COUNT(*) AS products FROM products;
SELECT COUNT(*) AS inventory_rows FROM inventory;
SELECT COUNT(*) AS addresses FROM addresses;
SELECT COUNT(*) AS payment_methods FROM payment_methods;
SELECT COUNT(*) AS orders FROM orders;
SELECT COUNT(*) AS order_items FROM order_items;
SELECT COUNT(*) AS returns FROM returns;

-- FK integrity checks (should all be 0)
SELECT COUNT(*) AS bad_orders_pm
FROM orders o LEFT JOIN payment_methods pm ON pm.payment_method_id = o.payment_method_id
WHERE pm.payment_method_id IS NULL;

SELECT COUNT(*) AS bad_orders_addr
FROM orders o LEFT JOIN addresses a ON a.address_id = o.shipping_address_id
WHERE a.address_id IS NULL;

SELECT COUNT(*) AS bad_items_orders
FROM order_items oi LEFT JOIN orders o ON o.order_id = oi.order_id
WHERE o.order_id IS NULL;

SELECT COUNT(*) AS bad_items_products
FROM order_items oi LEFT JOIN products p ON p.product_id = oi.product_id
WHERE p.product_id IS NULL;

SELECT COUNT(*) AS bad_returns_items
FROM returns r LEFT JOIN order_items oi ON oi.order_item_id = r.order_item_id
WHERE oi.order_item_id IS NULL;

-- Sanity join (Sarah's orders)
SELECT o.order_id, o.created_at, p.name, oi.variant_key, oi.quantity, oi.unit_price
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE o.user_id = 1
ORDER BY o.order_id, oi.order_item_id;