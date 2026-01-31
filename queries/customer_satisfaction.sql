SELECT 
    c.customer_state AS state,
    orv.review_score,
    COUNT(DISTINCT orv.order_id) AS order_count,
    ROUND(AVG(oi.price + oi.freight_value), 2) AS avg_order_value,
    ROUND(AVG(DATE_DIFF('day', o.order_purchase_timestamp, o.order_delivered_customer_date)), 1) AS avg_delivery_days
FROM order_reviews orv
INNER JOIN orders o ON orv.order_id = o.order_id
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered' 
  AND o.order_delivered_customer_date IS NOT NULL
GROUP BY c.customer_state, orv.review_score
ORDER BY state, orv.review_score;