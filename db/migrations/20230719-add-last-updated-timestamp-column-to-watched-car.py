"""
Add last_updated timestamp column to watched_car
"""

from yoyo import step

__depends__ = {'20230625-remove-unique-city-name-constraint'}

steps = [
    step(apply="ALTER TABLE watched_car ADD COLUMN last_update TIMESTAMP WITH TIME ZONE DEFAULT clock_timestamp();",
         rollback="ALTER TABLE watched_car DROP COLUMN last_update;")
]
