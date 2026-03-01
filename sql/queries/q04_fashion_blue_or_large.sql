-- Q4 (SQL-only approximation using variant_key):
-- Fashion products available in either blue color OR large size.
-- Assumes variant_key encodes size like "...-L" and/or color like "blue-...".
-- Adjust the LIKE patterns to match your real variant_key naming convention.

SELECT
  p.product_id,
  p.name AS product_name,
  i.variant_key,
  i.quantity
FROM products p
JOIN categories c ON c.category_id = p.category_id
JOIN inventory i ON i.product_id = p.product_id
WHERE (c.slug = 'fashion' OR c.name = 'Fashion')
  AND i.quantity > 0
  AND (
       i.variant_key LIKE '%-L'          -- large size (e.g., aqua-L, blue-L)
       OR LOWER(i.variant_key) LIKE '%blue%'  -- blue color
       OR LOWER(i.variant_key) LIKE '%aqua%'  -- OPTIONAL: treat aqua as blue
  )
ORDER BY p.product_id, i.variant_key;