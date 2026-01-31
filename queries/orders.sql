create table if not exists orders (
    order_id varchar(32) primary key,
    customer_id varchar(32),
    order_status varchar(20),
    order_purchase_timestamp datetime,
    order_approved_at datetime,
    order_delivered_carrier_date datetime,
    order_delivered_customer_date datetime,
    order_estimated_delivery_date date,
    foreign key (customer_id) references customers(customer_id)
);