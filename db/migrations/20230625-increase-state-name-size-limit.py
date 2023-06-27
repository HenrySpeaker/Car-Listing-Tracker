"""
Increase state name size limit
"""

from yoyo import step

__depends__ = {
    '20230622-make-zip-code-the-geographic-center-in-criteria'}

steps = [
    step(apply="""ALTER TABLE us_state
                  ALTER COLUMN state_name
                  SET DATA TYPE VARCHAR(100);""",
         rollback="""ALTER TABLE us_state
                     ALTER COLUMN state_name
                     SET DATA TYPE VARCHAR(20);""")
]
