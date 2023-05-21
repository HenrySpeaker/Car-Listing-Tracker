"""
Create website body style table
"""

from yoyo import step

__depends__ = {'20230519-create-body-style-table'}

steps = [
    step(apply="""
        CREATE TYPE website_name_type AS ENUM (
            'truecar',
            'autotrader'
        );

        CREATE TABLE website_body_style (
            id SERIAL PRIMARY KEY,
            body_style_id INTEGER REFERENCES body_style(id) ON DELETE CASCADE,
            website_name website_name_type,
            website_body_name VARCHAR(50)
        );
    """,
         rollback="""
         DROP TABLE website_body_style;
         DROP TYPE IF EXISTS website_name_type CASCADE;
         """)
]
