-- Q8:
-- Retrieve all orders placed by Sarah, showing:
-- order IDs, item details, payment methods, shipping options, status.

SELECT
  o.order_id,
  o.created_at,
  o.status,
  o.shipping_option,
  o.subtotal,
  o.tax,
  o.shipping_cost,
  o.total,
  pm.method_type AS payment_method,
  pm.last_four,
  p.product_id,
  p.name AS product_name,
  oi.variant_key,
  oi.quantity,
  oi.unit_price
FROM orders o
JOIN users u ON u.user_id = o.user_id
JOIN payment_methods pm ON pm.payment_method_id = o.payment_method_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
WHERE u.email = 'sarah@example.com'
ORDER BY o.created_at DESC, o.order_id, oi.order_item_id;