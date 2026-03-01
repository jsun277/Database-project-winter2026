-- Q9:
-- List all items returned by the user, with refund status, amount, restocking fees.

SELECT
  r.return_id,
  r.status AS refund_status,
  r.refund_amount,
  r.restocking_fee,
  r.created_at AS return_created_at,
  o.order_id,
  o.created_at AS order_created_at,
  p.product_id,
  p.name AS product_name,
  oi.variant_key,
  oi.quantity,
  oi.unit_price
FROM returns r
JOIN order_items oi ON oi.order_item_id = r.order_item_id
JOIN orders o ON o.order_id = oi.order_id
JOIN users u ON u.user_id = o.user_id
JOIN products p ON p.product_id = oi.product_id
WHERE u.email = 'sarah@example.com'
ORDER BY r.created_at DESC, r.return_id DESC;