-- Q13: days since last purchase + total order count per user
SELECT
  u.user_id,
  u.email,
  COUNT(o.order_id) AS total_orders,
  MAX(o.created_at) AS last_purchase_at,
  CASE
    WHEN MAX(o.created_at) IS NULL THEN NULL
    ELSE DATEDIFF(CURDATE(), DATE(MAX(o.created_at)))
  END AS days_since_last_purchase
FROM users u
LEFT JOIN orders o
  ON o.user_id = u.user_id
GROUP BY u.user_id, u.email
ORDER BY total_orders DESC, last_purchase_at DESC;