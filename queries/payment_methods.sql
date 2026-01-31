SELECT 
    c.customer_state AS state,
    UPPER(SUBSTR(op.payment_type, 1, 1)) || SUBSTR(op.payment_type, 2) AS payment_method,
    COUNT(DISTINCT op.order_id) AS order_count,
    ROUND(SUM(op.payment_value), 2) AS total_value,
    ROUND(AVG(op.payment_value), 2) AS avg_payment
FROM order_payments op
INNER JOIN orders o ON op.order_id = o.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state, op.payment_type
ORDER BY state, order_count DESC;