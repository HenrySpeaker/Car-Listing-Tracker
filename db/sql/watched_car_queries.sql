-- name: get_all_watched_cars
SELECT * FROM watched_car;

-- name: get_watched_car_by_vin^
SELECT * FROM watched_car WHERE vin = :vin LIMIT 1;

-- name: add_watched_car!
INSERT INTO watched_car (vin, listing_url, last_price) VALUES (:vin, :listing_url, :last_price);

-- name: delete_all_watched_cars!
DELETE FROM watched_car;

-- name: delete_watched_car_by_vin!
DELETE FROM watched_car WHERE vin = :vin;