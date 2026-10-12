-- Monthly revenue by customer, newest first.
SELECT u.name,
       COUNT(o.id)                AS orders,
       SUM(o.total_cents) / 100.0 AS revenue
FROM users AS u
LEFT JOIN orders AS o ON o.user_id = u.id
WHERE o.created_at >= NOW() - INTERVAL '30 days'
GROUP BY u.name
HAVING SUM(o.total_cents) > 50000
ORDER BY revenue DESC;
