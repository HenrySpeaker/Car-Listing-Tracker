"""
Add criteria_id column in watched_car
"""

from yoyo import step

__depends__ = {'20230725-add-previous-price-column-to-watched-cars'}

steps = [
    step(apply="ALTER TABLE watched_car ADD COLUMN criteria_id INTEGER REFERENCES criteria(id) ON DELETE CASCADE;",
         rollback="ALTER TABLE watched_car DROP COLUMN criteria_id;")
]
