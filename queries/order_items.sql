create table if not exists order_items (
    order_id varchar(32),
    order_item_id int,
    product_id varchar(32),
    seller_id varchar(32),
    shipping_limit_date datetime,
    price decimal(10, 2),
    freight_value decimal(10, 2),
    primary key (order_id, order_item_id),
    foreign key (order_id) references orders(order_id),
    foreign key (product_id) references products(product_id),
    foreign key (seller_id) references sellers(seller_id)
);