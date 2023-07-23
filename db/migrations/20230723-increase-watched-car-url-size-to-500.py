"""
Increase watched car url size to 500
"""

from yoyo import step

__depends__ = {'20230723-update-listing-alerts-table-name'}

steps = [
    step(apply="ALTER TABLE watched_car ALTER COLUMN listing_url TYPE VARCHAR(500);",
         rollback="ALTER TABLE watched_car ALTER COLUMN listing_url TYPE VARCHAR(200);")
]
