-- Q3:
-- Return items (product + variant) that are low in stock (< 5).

SELECT
  i.product_id,
  p.name AS product_name,
  i.variant_key,
  i.quantity
FROM inventory i
JOIN products p ON p.product_id = i.product_id
WHERE i.quantity < 5
ORDER BY i.quantity ASC, i.product_id, i.variant_key;