"""
Create watched-car-criteria-table
"""

from yoyo import step

__depends__ = {'20230522-create-criteria-table'}

steps = [
    step(apply="""
        CREATE TABLE watched_car_criteria (
            id SERIAL PRIMARY KEY,
            criteria_id INTEGER REFERENCES criteria(id) ON DELETE CASCADE NOT NULL,
            watched_car_id INTEGER REFERENCES watched_car(id) ON DELETE CASCADE NOT NULL,
            UNIQUE(criteria_id, watched_car_id)
        );
    """,
         rollback="DROP TABLE watched_car_criteria;")
]
