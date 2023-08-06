"""
Add model year to watched_car table
"""

from yoyo import step

__depends__ = {'20230728-drop-watched-car-criteria-table'}

steps = [
    step(apply="ALTER TABLE watched_car ADD COLUMN model_year SMALLINT;",
         rollback="ALTER TABLE watched_car DROP COLUMN model_year;")
]
