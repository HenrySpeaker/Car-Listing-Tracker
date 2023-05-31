-- name: get_all_states
SELECT * FROM us_state;

-- name: get_state_by_name^
SELECT * FROM us_state WHERE state_name = :state_name;

-- name: add_state!
INSERT INTO us_state (state_name) VALUES (:state_name);

-- name: delete_all_states!
DELETE FROM us_state;