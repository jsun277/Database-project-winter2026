-- Q12: top 3 co-purchased products with "headphones"
WITH headphones AS (
  SELECT product_id
  FROM products
  WHERE LOWER(name) LIKE '%headphones%'
  LIMIT 1
)
SELECT
  p2.product_id,
  p2.name,
  COUNT(DISTINCT oi1.order_id) AS co_purchase_orders
FROM order_items oi1
JOIN order_items oi2
  ON oi1.order_id = oi2.order_id
 AND oi1.product_id <> oi2.product_id
JOIN headphones h
  ON oi1.product_id = h.product_id
JOIN products p2
  ON p2.product_id = oi2.product_id
GROUP BY p2.product_id, p2.name
ORDER BY co_purchase_orders DESC
LIMIT 3;