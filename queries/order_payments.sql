create table if not exists order_payments (
    order_id varchar(32),
    payment_sequential int,
    payment_type varchar(20),
    payment_installments int,
    payment_value decimal(10, 2),
    primary key (order_id, payment_sequential),
    foreign key (order_id) references orders(order_id)
);