"""
Add state_id column to cities table
"""

from yoyo import step

__depends__ = {'20230530-create-states-table'}

steps = [
    step(apply="""
        ALTER TABLE city
        ADD COLUMN state_id INTEGER NOT NULL REFERENCES us_state(id) ON DELETE CASCADE;
    """,

         rollback="ALTER TABLE city DROP COLUMN state_id;")
]
