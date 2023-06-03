"""
Create criteria table
"""

from yoyo import step

__depends__ = {'20230521-create-watched-car-table'}

steps = [
    step(apply="""
        CREATE TABLE criteria (
            id SERIAL PRIMARY KEY,
            min_year SMALLINT,
            max_year SMALLINT,
            min_price INTEGER,
            max_price INTEGER,
            max_mileage INTEGER,
            search_distance INTEGER DEFAULT 50,
            no_accidents BOOLEAN DEFAULT TRUE,
            single_owner BOOLEAN DEFAULT FALSE,
            user_id INTEGER REFERENCES user_account(id) ON DELETE CASCADE NOT NULL,
            city_id INTEGER REFERENCES city(id) ON DELETE CASCADE NOT NULL,
            model_id INTEGER REFERENCES model(id) ON DELETE CASCADE,
            body_style_id INTEGER REFERENCES body_style(id) ON DELETE CASCADE,
            CHECK (min_year <= max_year),
            CHECK (min_price <= max_price)
        );
    
    """,

         rollback="DROP TABLE criteria;")
]
