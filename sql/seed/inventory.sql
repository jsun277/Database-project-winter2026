-- inventory.sql
-- variant_key ties to MongoDB variants[].key
-- Includes low stock examples (<5)
INSERT INTO inventory (product_id, variant_key, quantity, low_stock_threshold)
VALUES
(1, 'black',   3, 5),     -- low stock
(1, 'white',  10, 5),
(2, 'default', 7, 5),

(3, 'aqua-M',  2, 5),     -- low stock
(3, 'aqua-L',  8, 5),

(4, 'blue-M', 12, 5),
(5, 'default', 6, 5),
(6, 'default', 9, 5);