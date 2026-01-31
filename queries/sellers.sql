create table if not exists sellers (
    seller_id varchar(32) primary key,
    seller_zip_code_prefix varchar(10),
    seller_city varchar(100),
    seller_state varchar(2)
);