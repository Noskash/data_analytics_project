create table if not exists customers (
    customer_id varchar(32) primary key,
    customer_unique_id varchar(32),
    customer_zip_code_prefix varchar(10),
    customer_city varchar(100),
    customer_state varchar(2)
);