-- Q1 (SQL portion):
-- Retrieve all products in the Fashion category + their available variants.
-- In our architecture, rich attributes (material, detailed size/color) live in MongoDB,
-- but MySQL provides the canonical product + inventory variant keys.

SELECT
  p.product_id,
  p.name AS product_name,
  p.base_price,
  p.description,
  i.variant_key,
  i.quantity
FROM products p
JOIN categories c ON c.category_id = p.category_id
JOIN inventory i ON i.product_id = p.product_id
WHERE (c.slug = 'fashion' OR c.name = 'Fashion')
ORDER BY p.product_id, i.variant_key;