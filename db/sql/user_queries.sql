-- name: get_all_users
SELECT * FROM user_account;

-- name: get_user_by_username^
SELECT * FROM user_account WHERE username = :username LIMIT 1;

-- name: get_user_by_email^
SELECT * FROM user_account WHERE email = :email LIMIT 1;

-- name: get_user_by_id^
SELECT * FROM user_account WHERE id = :id LIMIT 1;

-- name: add_user!
INSERT INTO user_account(username, email, password_hash, notification_frequency) VALUES (:username, :email, :password_hash, :notification_frequency);

-- name: update_username_by_email!
UPDATE user_account SET username = :username WHERE email = :email;

-- name: update_email_by_username!
UPDATE user_account SET email = :email WHERE username = :username;

-- name: update_password_hash_by_username!
UPDATE user_account SET password_hash = :password_hash WHERE username = :username;

-- name: update_notification_frequency_by_username!
UPDATE user_account SET notification_frequency = :notification_frequency WHERE username = :username;

-- name: update_login_time_by_username!
UPDATE user_account SET last_login = :last_login WHERE username = :username;

--name: update_last_alerted_by_id!
UPDATE user_account SET last_alerted = :last_alerted WHERE id = :id;

--name: update_user_info!
UPDATE user_account SET 
username = :username, 
email = :email,
notification_frequency = :notification_frequency 
WHERE id = :id;

-- name: delete_all_users!
DELETE FROM user_account;

-- name: delete_user_by_username!
DELETE FROM user_account WHERE username = :username;