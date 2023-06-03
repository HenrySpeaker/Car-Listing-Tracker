"""
Create listing alerts table
"""

from yoyo import step

__depends__ = {'20230523-create-watched-car-criteria-table'}

steps = [
    step(apply="""
                CREATE TYPE listing_change AS ENUM (
                    'price_drop',
                    'new_listing'
                );

                CREATE TABLE listing_alerts (
                    id SERIAL PRIMARY KEY,
                    car_id INTEGER REFERENCES watched_car(id) ON DELETE CASCADE,
                    user_id INTEGER REFERENCES user_account(id) ON DELETE CASCADE,
                    change listing_change NOT NULL
                );
    """,
         rollback="""DROP TABLE listing_alerts;
                     DROP TYPE IF EXISTS listing_change CASCADE;
         """)
]
