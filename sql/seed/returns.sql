-- returns.sql
-- Return the dress from Sarah's Order 1.
-- In order_items.sql above, that dress row is the 2nd inserted item overall => order_item_id = 2
INSERT INTO returns (order_item_id, reason, status, refund_amount, restocking_fee, created_at)
VALUES
(2, 'Too small', 'refunded', 54.99, 5.00, '2026-02-20 14:00:00');