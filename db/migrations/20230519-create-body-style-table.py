"""
Create body style table
"""

from yoyo import step

__depends__ = {'20230519-create-make-table'}

steps = [
    step(apply="""
        CREATE TYPE body_style_type AS ENUM (
                'convertible',
                'coupe',
                'hatchback',
                'minivan',
                'sedan',
                'suv',
                'truck',
                'wagon'
                );

        CREATE TABLE body_style (
            id SERIAL PRIMARY KEY,
            body_style body_style_type UNIQUE NOT NULL
        );
    """,
         rollback="""DROP TABLE body_style; DROP TYPE IF EXISTS body_style_type CASCADE;""")
]
