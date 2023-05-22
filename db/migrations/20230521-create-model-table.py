"""
Create model table
"""

from yoyo import step

__depends__ = {'20230520-create-website-body-style-table'}

steps = [
    step(apply="""
        CREATE TABLE model (
            id SERIAL PRIMARY KEY,
            model_name VARCHAR(50),
            make_id INTEGER REFERENCES make(id) ON DELETE CASCADE,
            body_style_id INTEGER REFERENCES body_style(id) ON DELETE CASCADE
        );
    """,
         rollback="""DROP TABLE model;""")
]
