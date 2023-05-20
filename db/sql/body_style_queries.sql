-- name: get_all_body_styles
SELECT * FROM body_style;

-- name: get_body_style_info^
SELECT * FROM body_style WHERE body_style = :body_style;

-- name: add_body_style!
INSERT INTO body_style(body_style) VALUES (:body_style);

-- name: delete_all_body_styles!
DELETE FROM body_style;

