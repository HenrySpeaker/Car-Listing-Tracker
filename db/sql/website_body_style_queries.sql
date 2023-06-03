-- name: get_all_website_body_styles
SELECT * FROM website_body_style;

-- name: get_website_body_style_info
SELECT * FROM website_body_style WHERE body_style_id = :body_style_id;

-- name: add_website_body_style!
INSERT INTO website_body_style(body_style_id, website_name, website_body_name) VALUES (:body_style_id, :website_name, :website_body_name);

-- name: delete_all_website_body_styles!
DELETE FROM website_body_style;

-- name: delete_specific_website_body_style!
DELETE FROM website_body_style WHERE body_style_id = :body_style_id;