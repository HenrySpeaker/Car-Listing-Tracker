-- name: get_all_alerts
SELECT * FROM listing_alert;

-- name: add_alert!
INSERT INTO listing_alert(car_id, user_id, change) VALUES (:car_id, :user_id, :change);

-- name: delete_all_alerts!
DELETE FROM listing_alert;