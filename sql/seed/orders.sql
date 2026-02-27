-- orders.sql
-- Assumes:
--   Sarah payment_method_id = 1 (first row in payment_methods)
--   Sarah default shipping address_id = 1 (first row in addresses)
--   Orders use precomputed totals per denormalization plan.

INSERT INTO orders
(user_id, payment_method_id, shipping_address_id, shipping_option,
 subtotal, tax, shipping_cost, total, status, expected_delivery, created_at)
VALUES
-- Sarah orders (user_id=1)
(1, 1, 1, 'standard', 239.98, 19.20,  8.99, 268.17, 'delivered', '2026-02-10', '2026-02-05 10:00:00'),
(1, 1, 1, 'expedited', 89.99,  7.20, 12.99, 110.18, 'delivered', '2026-02-18', '2026-02-15 12:00:00'),
(1, 1, 1, 'standard',  59.99,  4.80,  8.99,  73.78, 'confirmed', '2026-03-01', '2026-02-24 09:30:00'),

-- Mike order (user_id=2), address_id=3, payment_method_id=3
(2, 3, 3, 'standard', 149.99, 12.00,  8.99, 170.98, 'confirmed', '2026-03-02', '2026-02-26 15:00:00'),

-- Ava order (user_id=3), address_id=4, payment_method_id=4
(3, 4, 4, 'standard',  89.99,  7.20,  8.99, 106.18, 'delivered', '2026-02-20', '2026-02-17 11:10:00');