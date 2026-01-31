create table if not exists geolocation (
    geolocation_zip_code_prefix varchar(10),
    geolocation_lat float,
    geolocation_lng float,
    geolocation_city varchar(100),
    geolocation_state varchar(2)
);