-- name: get_all_body_styles
SELECT * FROM body_style;

-- name: get_body_style_info^
SELECT * FROM body_style WHERE body_style_name = :body_style_name;

-- name: get_body_style_by_id^
SELECT * FROM body_style WHERE id = :id LIMIT 1;

-- name: add_body_style!
INSERT INTO body_style(body_style_name) VALUES (:body_style_name);

-- name: delete_all_body_styles!
DELETE FROM body_style;

