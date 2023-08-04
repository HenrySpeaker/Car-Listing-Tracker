"""
Drop user_id column in listing alerts
"""

from yoyo import step

__depends__ = {'20230728-add-criteria-id-column-in-watched-car'}

steps = [
    step(apply="ALTER TABLE listing_alert DROP COLUMN user_id;",
         rollback="ALTER TABLE listing_alert ADD COLUMN user_id INTEGER REFERENCES user_account(id) ON DELETE CASCADE;")
]
