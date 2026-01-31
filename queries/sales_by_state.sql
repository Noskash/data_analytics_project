SELECT 
    c.customer_state AS state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS total_revenue,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers,
    RANK() OVER (ORDER BY SUM(oi.price + oi.freight_value) DESC) AS revenue_rank,
    ROUND(100.0 * SUM(oi.price + oi.freight_value) / 
        (SELECT SUM(price + freight_value) FROM order_items), 2) AS revenue_share_pct
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;