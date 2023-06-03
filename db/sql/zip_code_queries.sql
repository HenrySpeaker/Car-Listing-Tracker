-- name: get_all_zip_codes
SELECT * FROM zip_code;

-- name: get_city_id_by_zip_code$
SELECT city_id FROM zip_code WHERE zip_code = :zip_code;

-- name: add_zip_code!
INSERT INTO zip_code(zip_code, city_id) VALUES (:zip_code, :city_id);

-- name: delete_all_zip_codes!
DELETE FROM zip_code;

-- name: delete_zip_code!
DELETE FROM zip_code WHERE zip_code = :zip_code;