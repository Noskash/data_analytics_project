create table if not exists products (
    product_id varchar(32) primary key,
    product_category_name varchar(50),
    product_name_lenght int,
    product_description_lenght int,
    product_photos_qty int,
    product_weight_g int,
    product_length_cm decimal(10, 2),
    product_height_cm decimal(10, 2),
    product_width_cm decimal(10, 2)
);