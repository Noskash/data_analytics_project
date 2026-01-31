create table if not exists order_reviews (
    review_id varchar(32),
    order_id varchar(32),
    review_score int,
    review_comment_title varchar(255),
    review_comment_message text,
    review_creation_date datetime,
    review_answer_timestamp datetime,
    foreign key (order_id) references orders(order_id)
);