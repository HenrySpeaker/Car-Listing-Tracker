"""
Create make table
"""

from yoyo import step

__depends__ = {'20230519-create-zip-code-table'}

steps = [
    step(apply="""
        CREATE TABLE MAKE (
            id SERIAL PRIMARY KEY,
            make_name VARCHAR(50) UNIQUE NOT NULL
        );
    """,
         rollback="DROP TABLE make;"
         )
]
