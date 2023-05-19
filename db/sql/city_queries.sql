-- name: get_all_cities
SELECT * FROM city;

-- name: get_city_id$
SELECT id FROM city WHERE city_name = :city_name;

-- name: add_city!
INSERT INTO city(city_name) VALUES (:city_name);

-- name: delete_all_cities!
DELETE FROM city;

-- name: delete_city_by_name!
DELETE FROM city WHERE city_name = :city_name;