-- name: get_all_makes
SELECT * FROM make;

-- name: get_make_info^
SELECT * FROM make WHERE make_name = :make_name;

-- name: get_make_by_id^
SELECT * FROM make WHERE id = :id LIMIT 1;

-- name: add_make!
INSERT INTO make (make_name) VALUES (:make_name);

-- name: delete_all_makes!
DELETE FROM make;

-- name: delete_make_by_name!
DELETE FROM make WHERE make_name = :make_name;