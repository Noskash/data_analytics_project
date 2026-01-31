SELECT 
    c.customer_state AS state,
    COALESCE(pct.product_category_name_english, 'Unknown') AS category,
    COUNT(DISTINCT oi.order_id) AS order_count,
    ROUND(SUM(oi.price), 2) AS total_revenue,
    ROUND(AVG(oi.price), 2) AS avg_price,
    COUNT(DISTINCT oi.product_id) AS unique_products
FROM order_items oi
INNER JOIN products p ON oi.product_id = p.product_id
LEFT JOIN product_category_translation pct ON p.product_category_name = pct.product_category_name
INNER JOIN orders o ON oi.order_id = o.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state, pct.product_category_name_english
HAVING COUNT(DISTINCT oi.order_id) > 10
ORDER BY state, total_revenue DESC;