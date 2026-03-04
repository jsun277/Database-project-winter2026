-- Q11: non-conversion rate for carts (requires carts table / imported carts)
SELECT
  ROUND(
    100 * SUM(CASE WHEN converted_order_id IS NULL THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS pct_carts_not_converted
FROM carts
WHERE created_at >= NOW() - INTERVAL 30 DAY;