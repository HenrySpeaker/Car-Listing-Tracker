"""
Create states table
"""

from yoyo import step

__depends__ = {'20230530-create-listing-alerts-table'}

steps = [
    step(apply="""
            CREATE TABLE us_state (
                id SERIAL PRIMARY KEY,
                state_name VARCHAR(20) NOT NULL UNIQUE
            );
        """,
         rollback="DROP TABLE us_state;")
]
