"""
Create watched car table
"""

from yoyo import step

__depends__ = {'20230521-create-model-table'}

steps = [
    step(apply="""
        CREATE TABLE watched_car (
            id SERIAL PRIMARY KEY,
            vin VARCHAR(50) UNIQUE NOT NULL,
            listing_url VARCHAR(200) NOT NULL,
            last_price INTEGER
        );
    """,
         rollback="DROP TABLE watched_car")
]
