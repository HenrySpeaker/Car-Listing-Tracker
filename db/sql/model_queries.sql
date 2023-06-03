-- name: get_all_models
SELECT * FROM model;

-- name: get_model_by_make_id
SELECT * FROM model WHERE make_id = :make_id;

-- name: get_model_by_make_name
SELECT * FROM model WHERE make_id = (SELECT id FROM make WHERE make_name = :make_name LIMIT 1);

-- name: get_model_by_body_style_id
SELECT * FROM model WHERE body_style_id = :body_style_id;

-- name: get_model_by_body_style_name
SELECT * FROM model WHERE body_style_id = (SELECT id FROM body_style WHERE body_style_name = :body_style_name);

-- name: add_model!
INSERT INTO model(model_name, make_id, body_style_id) VALUES (:model_name, :make_id, :body_style_id);

-- name: delete_all_models!
DELETE FROM model;

-- name: delete_model_by_model_name!
DELETE FROM model WHERE model_name = :model_name;

