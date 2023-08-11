"""
Add last_alerted timestamp column to users table
"""

from yoyo import step

__depends__ = {'20230806-add-model-year-to-watched-car-table'}

steps = [
    step(apply="ALTER TABLE user_account ADD COLUMN last_alerted TIMESTAMP WITH TIME ZONE DEFAULT NOW();",
         rollback="ALTER TABLE user_account DROP COLUMN last_alerted;")
]
