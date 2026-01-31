SELECT 
    STRFTIME('%Y-%m', o.order_purchase_timestamp) AS month,
    c.customer_state AS state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS monthly_revenue,
    ROUND(AVG(oi.price + oi.freight_value), 2) AS avg_order_value
FROM orders o
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY STRFTIME('%Y-%m', o.order_purchase_timestamp), c.customer_state
ORDER BY month, state;