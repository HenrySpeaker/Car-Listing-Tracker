"""
Make zip code the geographic center in criteria
"""

from yoyo import step

__depends__ = {
    '20230613-add-criteria-table-check-constraint-of-model-id-xor-body-style-id'}

steps = [
    step(apply="""
            ALTER TABLE criteria DROP COLUMN IF EXISTS city_id;
            ALTER TABLE criteria ADD COLUMN IF NOT EXISTS zip_code_id INTEGER REFERENCES zip_code(id) ON DELETE CASCADE NOT NULL;
        """,
         rollback="""
            ALTER TABLE criteria DROP COLUMN IF EXISTS zip_code_id;
            ALTER TABLE criteria ADD COLUMN IF NOT EXISTS city_id INTEGER REFERENCES city(id) ON DELETE CASCADE NOT NULL;
         """)
]
