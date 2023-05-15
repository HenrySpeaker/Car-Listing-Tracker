-- name: get_all_users
SELECT * FROM user_account;

-- name: get_user_by_name^
SELECT * FROM user_account WHERE username = :username LIMIT 1;

-- name: get_user_by_email^
SELECT * FROM user_account WHERE email = :email LIMIT 1;

-- name: add_user!
INSERT INTO user_account(username, email, password_hash, notification_frequency) VALUES (:username, :email, :password_hash, :notification_frequency);

-- name: update_username_by_email
UPDATE user_account(username) SET username = :username WHERE email = :email;

-- name: delete_all_users
DELETE FROM user_account;