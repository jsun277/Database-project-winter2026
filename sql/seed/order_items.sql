-- order_items.sql
-- Orders assumed:
--   order_id 1..5 in insertion order
-- Products assumed:
--   product_id 1..6 in insertion order

INSERT INTO order_items (order_id, product_id, variant_key, quantity, unit_price)
VALUES
-- Order 1 (Sarah): headphones + dress + vase
(1, 1, 'black',   1, 149.99),
(1, 3, 'aqua-M',  1,  59.99),
(1, 5, 'default', 1,  89.99),

-- Order 2 (Sarah): earbuds
(2, 2, 'default', 1,  89.99),

-- Order 3 (Sarah): dress (different size)
(3, 3, 'aqua-L',  1,  59.99),

-- Order 4 (Mike): headphones
(4, 1, 'white',   1, 149.99),

-- Order 5 (Ava): vase
(5, 5, 'default', 1,  89.99);