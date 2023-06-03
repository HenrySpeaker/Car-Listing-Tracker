-- name: get_all_watched_car_criteria
SELECT * FROM watched_car_criteria;

-- name: get_watched_car_criteria_by_info
SELECT * FROM watched_car_criteria
WHERE
    (:criteria_id::integer IS NULL OR criteria_id = :criteria_id) AND
    (:watched_car_id::integer IS NULL OR watched_car_id = :watched_car_id); 

-- name: add_watched_car_criteria!
INSERT INTO watched_car_criteria (criteria_id, watched_car_id) VALUES (:criteria_id, :watched_car_id);

-- name: delete_all_watched_car_criteria!
DELETE FROM watched_car_criteria;

-- name: delete_watched_car_criteria_by_info!
DELETE FROM watched_car_criteria
WHERE
    (:criteria_id::integer IS NULL OR criteria_id = :criteria_id) AND
    (:watched_car_id::integer IS NULL OR watched_car_id = :watched_car_id); 