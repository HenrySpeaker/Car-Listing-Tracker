-- name: get_all_alerts
SELECT * FROM listing_alert;

-- name: get_alerts_by_info
SELECT * FROM listing_alert WHERE
(:car_id::integer IS NULL OR car_id=:car_id);

-- name: add_alert!
INSERT INTO listing_alert(car_id, change) VALUES (:car_id, :change);

-- name: delete_all_alerts!
DELETE FROM listing_alert;

-- name: delete_alerts_by_info!
DELETE FROM listing_alert WHERE
(:car_id::integer IS NULL OR car_id=:car_id);