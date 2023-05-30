-- name: get_all_alerts
SELECT * FROM listing_alerts;

-- name: add_alert!
INSERT INTO listing_alerts(car_id, user_id, change) VALUES (:car_id, :user_id, :change);

-- name: delete_all_alerts!
DELETE FROM listing_alerts;