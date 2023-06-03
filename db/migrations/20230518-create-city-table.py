"""
Create city table
"""

from yoyo import step

__depends__ = {'20230511-create-user-table'}

steps = [
    step(apply="""
        CREATE TABLE city (
            id SERIAL PRIMARY KEY,
            city_name VARCHAR(100) UNIQUE NOT NULL
        );
    """,
         rollback="DROP TABLE city;")
]
