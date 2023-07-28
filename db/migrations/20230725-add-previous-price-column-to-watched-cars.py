"""
Add previous price column to watched cars
"""

from yoyo import step

__depends__ = {'20230723-increase-watched-car-url-size-to-500'}

steps = [
    step(apply="ALTER TABLE watched_car ADD COLUMN prev_price INTEGER;",
         rollback="ALTER TABLE watched_car DROP COLUMN prev_price;")
]
