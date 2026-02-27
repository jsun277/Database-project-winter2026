-- seed_all.sql
-- Runs all seed scripts in FK-safe order.

USE ecommerce;

START TRANSACTION;

SOURCE sql/seed/users.sql;
SOURCE sql/seed/categories.sql;
SOURCE sql/seed/products.sql;
SOURCE sql/seed/inventory.sql;
SOURCE sql/seed/addresses.sql;
SOURCE sql/seed/payment_methods.sql;
SOURCE sql/seed/orders.sql;
SOURCE sql/seed/order_items.sql;
SOURCE sql/seed/returns.sql;

COMMIT;