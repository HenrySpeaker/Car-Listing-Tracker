"""
Create zip-code-to-city table
"""

from yoyo import step

__depends__ = {'20230518-create-city-table'}

steps = [
    step(apply="""
        CREATE TABLE zip_code (
             id SERIAL PRIMARY KEY,
             zip_code INTEGER NOT NULL UNIQUE,
             city_id INTEGER NOT NULL REFERENCES city(id) ON DELETE CASCADE
        );
    """,
         rollback="DROP TABLE zip_code;")
]
