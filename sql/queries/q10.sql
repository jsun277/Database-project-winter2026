-- Q10: avg days between Sarah's purchases
WITH sarah_orders AS (
  SELECT o.order_id, DATE(o.created_at) AS order_date
  FROM orders o
  JOIN users u ON u.user_id = o.user_id
  WHERE u.email = 'sarah@example.com'
),
gaps AS (
  SELECT
    order_date,
    LAG(order_date) OVER (ORDER BY order_date) AS prev_order_date
  FROM sarah_orders
)
SELECT
  AVG(DATEDIFF(order_date, prev_order_date)) AS avg_days_between_purchases
FROM gaps
WHERE prev_order_date IS NOT NULL;