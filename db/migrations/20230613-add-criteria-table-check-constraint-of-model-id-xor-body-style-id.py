"""
Add criteria table check constraint of model_id XOR body_style_id
"""

from yoyo import step

__depends__ = {
    '20230613-change-body-styles-to-reflect-capitalized-first-letters'}

steps = [
    step(apply="""
        ALTER TABLE criteria ADD CONSTRAINT model_XOR_body_style CHECK (num_nonnulls(model_id, body_style_id) = 1);
    """,
         rollback="""
        ALTER TABLE criteria DROP CONSTRAINT model_XOR_body_style RESTRICT;
    """)
]
